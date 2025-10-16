# main.py — FastAPI webhook + python-telegram-bot v21 + Ollama (streaming)
#         + affiliate suggester + concise replies + early length cap

import os, json, logging
from time import monotonic
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.constants import ChatAction
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from affiliate_catalog import find_matches, preset_for_scenario

logging.basicConfig(level=logging.INFO)

# --- Env/config ---
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var.")

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
OLLAMA_URL     = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL   = os.environ.get("OLLAMA_MODEL", "qwen2.5")

# Speed/perf knobs (tune to taste)
NUM_PREDICT = int(os.environ.get("NUM_PREDICT", "180"))   # fewer tokens => snappier + shorter
NUM_CTX     = int(os.environ.get("NUM_CTX", "2048"))
KEEP_ALIVE  = os.environ.get("KEEP_ALIVE", "30m")

# NEW: cap total streamed characters (prevents giant edits and hitting 4096)
MAX_TOTAL_CHARS = int(os.environ.get("MAX_TOTAL_CHARS", "3500"))

# --- Build PTB app ---
tg_app = Application.builder().token(BOT_TOKEN).build()

# --- Streaming call to Ollama ---
async def stream_ollama(prompt: str, sys_prompt: str | None = None):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": (
            ([{"role": "system", "content": sys_prompt}] if sys_prompt else [])
            + [{"role": "user", "content": prompt}]
        ),
        "stream": True,
        "options": {
            "num_predict": NUM_PREDICT,
            "num_ctx": NUM_CTX,
            # slightly stricter sampling to reduce rambles
            "temperature": float(os.getenv("TEMP", "0.3")),
            "top_p": float(os.getenv("TOP_P", "0.9")),
            "repeat_penalty": float(os.getenv("REPEAT_PENALTY", "1.15")),
        },
        "keep_alive": KEEP_ALIVE,
    }
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                chunk = (data.get("message", {}) or {}).get("content", "")
                if chunk:
                    yield chunk

# --- Helpers for Telegram edits/limits ---
MAX_LEN = 4096

async def edit_throttled(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    new_full_text: str,
    last_edit_time: float,
    last_text: str,
    min_interval: float = 0.25,
):
    """
    Edit no more than ~4 times/sec and only if the visible text changed.
    Shows the tail while streaming if over the 4096-char limit.
    """
    display = new_full_text if len(new_full_text) <= MAX_LEN else new_full_text[-MAX_LEN:]

    if display == last_text:
        return last_edit_time, last_text

    now = monotonic()
    if (now - last_edit_time) < min_interval:
        return last_edit_time, last_text

    try:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=display or "…")
    except BadRequest as e:
        if "not modified" not in str(e).lower():
            raise
    return now, display

async def send_final(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    full_text: str,
    last_text: str,
):
    """
    Finalize the message: ensure the edited message has the first chunk,
    then send any overflow as new messages (Telegram cap 4096).
    """
    first = (full_text[:MAX_LEN] or "…")
    if first != last_text:
        try:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=first)
        except BadRequest as e:
            if "not modified" not in str(e).lower():
                raise
    i = MAX_LEN
    while i < len(full_text):
        await context.bot.send_message(chat_id=chat_id, text=full_text[i:i+MAX_LEN])
        i += MAX_LEN

# --- Affiliate helpers ---
def _fmt_aff_line(item) -> str:
    return f"• {item.title}\n  {item.url}"

async def maybe_suggest_affiliates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = (update.message.text or "").lower()
    matches = find_matches(user_msg, max_items=2)
    presets = preset_for_scenario(user_msg)
    seen, suggestions = set(), []
    for it in (matches + presets):
        if it.url not in seen:
            suggestions.append(it); seen.add(it.url)
    if suggestions:
        blurb = "*Helpful gear for this topic:*\n" + "\n".join(_fmt_aff_line(it) for it in suggestions)
        await update.message.reply_text(blurb, disable_web_page_preview=False)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Webhook online ✅  Streaming model replies. Send me a message.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – status\n"
        "/help – this help\n"
        "/buy <keywords> – quick affiliate links"
    )

async def buy_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /buy <keywords>  e.g., /buy radio")
    q = " ".join(context.args)
    items = find_matches(q, max_items=3)
    if not items:
        return await update.message.reply_text("No matching items yet—try different keywords.")
    text = "*Suggested items:*\n" + "\n".join(_fmt_aff_line(it) for it in items)
    await update.message.reply_text(text, disable_web_page_preview=False)

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    # Show typing…
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Placeholder message to edit as we stream
    msg = await update.message.reply_text("…")
    buffer = ""
    last_edit = 0.0
    last_text = "…"

    # NEW: concise system prompt to keep answers short
    concise_sys_prompt = (
        "You are a helpful, concise assistant replying for a Telegram bot. "
        "Keep answers under ~180 words (≈900 characters) unless the user asks for details. "
        "Prefer short bullets for steps; avoid long stories."
    )

    try:
        async for chunk in stream_ollama(user_text, sys_prompt=concise_sys_prompt):
            buffer += chunk

            # NEW: stop early if getting too long; avoids giant edits & 4096 cap
            if len(buffer) >= MAX_TOTAL_CHARS:
                buffer = buffer[:MAX_TOTAL_CHARS] + "\n\n…(truncated for length)"
                break

            last_edit, last_text = await edit_throttled(
                context, chat_id, msg.message_id, buffer, last_edit, last_text
            )

        # Final LLM reply flush (splits >4096 into multiple messages)
        await send_final(context, chat_id, msg.message_id, buffer or "No response.", last_text)

        # After replying, lightly suggest affiliate links if relevant
        await maybe_suggest_affiliates(update, context)

    except Exception as e:
        logging.exception("Streaming error")
        try:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=f"Model error: {e}")
        except BadRequest:
            await context.bot.send_message(chat_id=chat_id, text=f"Model error: {e}")

# Register handlers
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("help", help_cmd))
tg_app.add_handler(CommandHandler("buy", buy_cmd))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

# --- FastAPI + PTB lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await tg_app.initialize()
    yield
    await tg_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.post(f"/telegram/{BOT_TOKEN}")
async def telegram_webhook(request: Request):
    # Verify Telegram secret header if set
    if WEBHOOK_SECRET and request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="bad secret")
    update = Update.de_json(await request.json(), tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}

