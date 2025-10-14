# Honey Bot – Mac Backend Setup (Streamer + ngrok + Ollama + Affiliate Hints)

FastAPI + python-telegram-bot (v21), **Ollama** for LLM, **ngrok** for the public webhook, and a tiny **affiliate catalog** that suggests links after replies. It also includes scripts so you don’t have to memorize commands.

---

## 0) What you get

- **FastAPI** server with Telegram webhook at  
  `/telegram/<YOUR_BOT_TOKEN>`
- **Streaming** replies from Ollama  
  (tries `/api/chat`, falls back to `/api/generate`, and finally `/v1/chat/completions`)
- **Non-spammy affiliate suggestions** (local `affiliate_catalog.py`)
- **Scripts** to load env, run app, run ngrok, and (un)register webhooks

---

## 1) Prereqs (one-time)

```bash
# If you don’t have Homebrew yet:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.11 git jq
brew install --cask ngrok

# Optional (if you use GitHub CLI for secrets, etc.)
brew install gh
```

**Ollama:**
- Install via app or brew cask:  
  `brew install --cask ollama`
- Start server in a terminal so you can see logs:
  ```bash
  ollama serve
  ```

---

## 2) Clone + venv + deps

```bash
git clone https://github.com/<you>/apocolypse-mommy.git
cd apocolypse-mommy

python3 -m venv .venv
source .venv/bin/activate

# If you have requirements.txt (we do):
pip install -r requirements.txt
# Otherwise:
# pip install fastapi uvicorn httpx "python-telegram-bot==21.*"
```

---

## 3) Environment file

Create `.env` in the repo root (**don’t commit it**):

```bash
TELEGRAM_BOT_TOKEN=8376899944:AAH...NcFA
WEBHOOK_SECRET=yourStrongSecret123
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5
NUM_PREDICT=220
NUM_CTX=2048
KEEP_ALIVE=30m

# (optional PA-API while you wait for access)
# PAAPI_ACCESS_KEY=...
# PAAPI_SECRET_KEY=...
# PAAPI_PARTNER_TAG=apocalypsemeowmeow-20
# PAAPI_MARKETPLACE=www.amazon.com
```

> We also keep these in `~/.zshrc` so new terminals have them. The loader script will sync `.env` → `~/.zshrc` and then source it.

---

## 4) Scripts we use

Create a `scripts/` directory with these files (you already have them, documenting for completeness).

### `scripts/load_env.sh`
- Reads `.env`, writes/export lines into `~/.zshrc` (idempotent), and sources them **into the current shell**.  
- **Always `source` this script**, never just run it.

```bash
# usage in your shell or other scripts:
source scripts/load_env.sh
```

### `scripts/run_app.sh`
- Ensures venv + deps, sources env, runs Uvicorn (with `--reload` for dev).

```bash
./scripts/run_app.sh
```

### `scripts/run_ngrok.sh`
- Starts `ngrok http 8000` (no duplicates).

```bash
./scripts/run_ngrok.sh
# Inspector: http://127.0.0.1:4040
```

### `scripts/register_webhook.sh`
- Reads the current **https** forward URL from ngrok’s local API and calls Telegram `setWebhook` with:
  - `url = https://<ngrok>/telegram/<YOUR_BOT_TOKEN>`
  - `secret_token = $WEBHOOK_SECRET`
  - `drop_pending_updates = true`
  - `allowed_updates = ["message","callback_query"]`

```bash
./scripts/register_webhook.sh
```

### `scripts/unregister_webhook.sh`
- Deletes the webhook (use this before switching machines).

```bash
./scripts/unregister_webhook.sh
```


---

## 5) Affiliate catalog

File: `affiliate_catalog.py` (sit next to `main.py`).  
We store a small curated list (title + affiliate URL + tags). The bot inserts **1–3 relevant links** after normal replies, and `/buy <keywords>` returns links explicitly.

> Add or edit items anytime; tags drive the lightweight matching.

---

## 6) Running (3 terminals)

**Terminal A – App**
```bash
./scripts/run_app.sh
# health: curl -s http://127.0.0.1:8000/healthz
```

**Terminal B – ngrok**
```bash
./scripts/run_ngrok.sh
# note: keep this running; copy the https forwarding URL if needed
```

**Terminal C – Set webhook to current ngrok URL**
```bash
./scripts/register_webhook.sh
# verify:
curl -sS "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo" | jq
```

**In Telegram:**
- `/start` – should reply “Webhook online ✅ …”
- Send a normal message (e.g., “power outage prep for 3 days”) – streamed reply + a small affiliate block.
- `/buy radio` – explicit catalog lookup.

---

## 7) Ollama notes

- If you see 404s on `/api/chat` and `/api/generate`, we now **also** fall back to the **OpenAI-compatible** `/v1/chat/completions`.  
- Ensure a model is available:
  ```bash
  ollama list
  ollama pull qwen2.5
  ```
- Default endpoint URL is `http://127.0.0.1:11434` (matches `OLLAMA_URL` in `.env`).

---

## 8) Webhook hygiene (when switching machines)

1. Remove old webhook:
   ```bash
   ./scripts/unregister_webhook.sh
   ```
2. Start app + ngrok on the new machine, then:
   ```bash
   ./scripts/register_webhook.sh
   ```

---

## 9) Troubleshooting

- **403 in ngrok inspector** → `WEBHOOK_SECRET` mismatch (value in `.env` must match the one sent in `register_webhook.sh`).  
- **404 to `/telegram/<token>`** → wrong bot token hitting your server (another bot still pointing to your ngrok). Delete that bot’s webhook.  
- **No traffic at all** → `getWebhookInfo` URL doesn’t match current ngrok. Re-run `register_webhook.sh`.  
- **Ollama connection errors** → is `ollama serve` running? Model pulled? `curl -s 127.0.0.1:11434/api/version` should return a JSON object.  
- **Env not loaded** → remember to `source scripts/load_env.sh` at least once per terminal session (our runner script does this for you).

---

## 10) Security

- Treat `.env` and `~/.zshrc` values as **secrets** (don’t commit).  
- Rotate your Telegram bot token via **@BotFather** if you ever paste it publicly.  
- Amazon Associates links: include a visible disclosure on your site/channel.

---

## 11) Useful references (quick)

- Ngrok inspector: `http://127.0.0.1:4040`  
- Health: `http://127.0.0.1:8000/healthz`  
- Telegram webhook info:
  ```bash
  curl -sS "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo" | jq
  ```

---

Happy shipping! 🚀
