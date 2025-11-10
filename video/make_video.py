#!/usr/bin/env python3
"""
make_video.py — Daily Survival Video Generator + Broadcaster

On each run:
  1) Pick a random survival topic
  2) Generate a ~30s script (Ollama if available, else fallback template)
  3) TTS voiceover (Edge-TTS with macOS 'say' fallback)
  4) Download free stock footage from Pexels
  5) Stitch clips to ~30s with MoviePy, overlay voice, export MP4 + SRT
  6) (Optional) Burn the SRT into the video using ffmpeg
  7) Send the video:
      - to all chats in subscribers.json (populated by your Honey bot via /subscribe)
      - and/or to explicit targets in TARGET_CHAT (comma-separated: @channel, -100123..., etc.)

Environment (via .env or ~/.zshrc):
  PEXELS_API_KEY=...
  OLLAMA_URL=http://127.0.0.1:11434
  OLLAMA_MODEL=qwen2.5
  VOX=en-US-JennyNeural
  TELEGRAM_BOT_TOKEN=123456:ABC...
  SUBSCRIBERS_FILE=/path/to/subscribers.json
  VIDEO_DIR=daily_videos
  EXPORT_BITRATE=3500k
  TARGET_CHAT=@my_channel,-1001234567890
  TTS_BACKEND=edge|say   # optional; default tries edge then falls back to 'say' on macOS

New toggles:
  CAPTIONS_MODE=burn|sidecar|both   # default burn
  SEND_VARIANT=burned|plain         # default auto: burned if possible else plain

Requirements:
  pip install moviepy requests edge-tts python-dotenv
  ffmpeg must be installed and on PATH (with libass for subtitles).
"""

import os, re, random, shutil, datetime, tempfile, asyncio, json, sys, subprocess
from pathlib import Path
from typing import List, Tuple

import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from dotenv import load_dotenv

# ---------- Generation parameters ----------
TARGET_SECONDS = 30
MIN_CLIP = 5
MAX_CLIP = 12
MAX_DOWNLOADS = 6

RANDOM_TOPICS = [
    "72-hour blackout checklist", "wildfire evacuation plan",
    "winter storm essentials", "go-bag for two adults",
    "water storage basics", "NOAA weather radio—why it matters",
    "first-aid for cuts and bleeding", "safe lighting during outages",
    "phone power when the grid is down", "storm prep 24 hours out"
]

# Subtitle styling for burn-in (libass force_style) or None for default
SRT_STYLE = None
# Example:
# SRT_STYLE = "FontName=Arial,FontSize=28,Outline=2,Shadow=1,PrimaryColour=&H00FFFFFF&"

# ---------- Utilities ----------
def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

# ---------- Script generation (Ollama or fallback) ----------
def script_from_template(topic: str) -> str:
    return (f"Today’s survival tip: {topic}. Store at least one gallon of water per person per day, "
            f"keep shelf-stable food and a manual can opener, and use battery lanterns for safe indoor light. "
            f"Carry a NOAA weather radio and a charged power bank for phones. "
            f"Pack a compact first-aid kit with a trauma bandage and gloves. "
            f"Simple steps done now make a stressful situation safer and easier.")

def gen_script_ollama(topic: str, ollama_url: str, model: str) -> str:
    prompt = (
        "Write a 30-second, 65–85 word script in a calm, practical tone for a survival/preparedness short.\n"
        f"Topic: {topic}\n"
        "Requirements:\n"
        "- Direct, prescriptive tips\n"
        "- No fear-mongering\n"
        "- End with a one-sentence takeaway\n"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You write concise 30-second scripts for survival tips."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.5, "num_predict": 200}
    }
    try:
        r = requests.post(f"{ollama_url}/api/chat", json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        text = (data.get("message", {}) or {}).get("content", "").strip()
        return text or script_from_template(topic)
    except Exception:
        return script_from_template(topic)

# ---------- TTS (Edge-TTS with macOS 'say' fallback) ----------
def _tts_say(text: str, voice_hint: str, out_mp3: Path):
    """
    macOS offline fallback using 'say' -> AIFF -> AAC/MP4 via ffmpeg.
    Attempts a simple mapping from Edge voice names to macOS voices.
    """
    voice_map = {
        "en-US-JennyNeural": "Samantha",
        "en-US-GuyNeural": "Alex",
    }
    mac_voice = voice_map.get(voice_hint, "Samantha")
    aiff = out_mp3.with_suffix(".aiff")
    subprocess.run(["say", "-v", mac_voice, "-r", "190", "-o", str(aiff), text], check=True)
    tmp_m4a = out_mp3.with_suffix(".m4a")
    subprocess.run(["ffmpeg", "-y", "-i", str(aiff), "-c:a", "aac", str(tmp_m4a)], check=True)
    shutil.move(str(tmp_m4a), str(out_mp3))
    try:
        aiff.unlink(missing_ok=True)
    except Exception:
        pass

async def _edge_tts_stream_and_srt(text: str, voice: str, out_mp3: Path) -> str:
    """
    Streams Edge-TTS audio to out_mp3 while collecting WordBoundary timings,
    then returns an SRT string built from those timings.
    """
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=voice, rate="+0%")

    word_boundaries = []
    TICKS_PER_SEC = 10_000_000

    with open(out_mp3, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                w = chunk.get("text") or chunk.get("word") or ""
                offset_s = float(chunk["offset"]) / TICKS_PER_SEC
                dur_s    = float(chunk["duration"]) / TICKS_PER_SEC
                word_boundaries.append({"text": w, "offset": offset_s, "duration": dur_s})

    return _build_srt_from_boundaries(text, word_boundaries)

def gen_tts_with_timings(text: str, voice: str, out_mp3: Path) -> tuple[Path, str | None]:
    """
    Returns (mp3_path, srt_text_or_None).
    - If Edge-TTS is used successfully: returns SRT text aligned to true timings.
    - If macOS 'say' fallback is used: returns None (caller should fall back to even SRT).
    """
    backend = os.getenv("TTS_BACKEND", "").lower().strip()
    if backend == "say":
        if sys.platform != "darwin":
            raise RuntimeError("TTS_BACKEND=say requires macOS.")
        _tts_say(text, voice, out_mp3)
        return out_mp3, None

    # Try Edge-TTS first (either explicitly or default)
    try:
        srt_text = asyncio.run(_edge_tts_stream_and_srt(text, voice, out_mp3))
        return out_mp3, srt_text
    except Exception as e:
        print(f"[TTS] Edge-TTS failed ({e}).", file=sys.stderr)
        if backend == "edge":
            raise
        if sys.platform == "darwin":
            print("[TTS] Falling back to macOS 'say'.")
            _tts_say(text, voice, out_mp3)
            return out_mp3, None
        else:
            raise

# ---------- SRT helpers ----------
def _split_sentences(text: str) -> list[str]:
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    return sents or [text.strip()]

def _tokenize(s: str) -> list[str]:
    return re.findall(r"\S+", s)

def _build_srt_from_boundaries(full_text: str, boundaries: list[dict]) -> str:
    """
    Convert Edge-TTS word boundaries to sentence-level SRT.
    boundaries entries: {"offset": seconds, "duration": seconds, "text": "word"}
    """
    sentences = _split_sentences(full_text)
    sent_tokens = [_tokenize(s) for s in sentences]
    all_tokens = [tok for group in sent_tokens for tok in group]

    # If mismatch, fall back to even SRT
    if not boundaries or len(boundaries) < max(3, int(0.6 * len(all_tokens))):
        return make_srt(full_text, TARGET_SECONDS)

    n = min(len(all_tokens), len(boundaries))
    token_times = [(b["offset"], b["offset"] + b["duration"]) for b in boundaries[:n]]

    idx = 0
    entries = []
    for s_idx, toks in enumerate(sent_tokens, start=1):
        if not toks:
            continue
        start_idx = idx
        end_idx = min(idx + len(toks) - 1, n - 1)
        start_t = token_times[start_idx][0]
        end_t = token_times[end_idx][1]
        idx = end_idx + 1
        start_t = max(0.0, min(float(start_t), float(TARGET_SECONDS - 0.2)))
        end_t   = max(start_t + 0.01, min(float(end_t), float(TARGET_SECONDS)))
        entries.append((s_idx, start_t, end_t, sentences[s_idx-1]))

    def fmt(t: float):
        h = int(t // 3600); t -= h*3600
        m = int(t // 60); t -= m*60
        s = int(t); ms = int((t - s) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    lines = []
    for i, start, end, sent in entries:
        lines.append(f"{i}\n{fmt(start)} --> {fmt(end)}\n{sent}\n")
    return "\n".join(lines)

def make_srt(text: str, total_seconds: float) -> str:
    chunks = [c.strip() for c in re.split(r'(?<=[.!?])\s+', text) if c.strip()]
    if not chunks:
        chunks = [text.strip()]
    per = total_seconds / len(chunks)
    def fmt(t: float):
        h = int(t // 3600); t -= h*3600
        m = int(t // 60); t -= m*60
        s = int(t); ms = int((t - s) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    out = []
    cur = 0.0
    for i, c in enumerate(chunks, 1):
        start = cur; end = min(total_seconds, cur + per)
        out.append(f"{i}\n{fmt(start)} --> {fmt(end)}\n{c}\n")
        cur = end
    return "\n".join(out)

# ---------- Pexels video search & download ----------
def pexels_search_videos(api_key: str, query: str, per_page: int = 15) -> List[dict]:
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": per_page}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("videos", [])

def choose_video_files(video_item: dict) -> List[Tuple[str, int]]:
    files = video_item.get("video_files", [])
    out = []
    for f in files:
        if f.get("file_type") == "video/mp4":
            out.append((f.get("link"), int(f.get("height") or 0)))
    out.sort(key=lambda x: x[1], reverse=True)
    return out

def download_binary(url: str, dest: Path):
    with requests.get(url, stream=True, timeout=90) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            shutil.copyfileobj(r.raw, f)

def fetch_stock_clips(api_key: str, query: str, tmpdir: Path) -> List[Path]:
    vids = pexels_search_videos(api_key, query)
    paths: List[Path] = []
    random.shuffle(vids)
    for v in vids:
        files = choose_video_files(v)
        if not files:
            continue
        pick = files[min(1, len(files)-1)]  # mid/high quality file
        dest = tmpdir / f"pexels_{v.get('id')}.mp4"
        try:
            download_binary(pick[0], dest)
            paths.append(dest)
            if len(paths) >= MAX_DOWNLOADS:
                break
        except Exception:
            continue
    return paths

# ---------- Build final video ----------
def build_video(clips: List[Path], voice_mp3: Path, out_path: Path, bitrate: str = "3500k"):
    audio = AudioFileClip(str(voice_mp3))
    target = TARGET_SECONDS

    vclips = []
    total = 0.0
    for p in clips:
        try:
            vc = VideoFileClip(str(p))
            dur = float(vc.duration or 0.0)
            seg = min(MAX_CLIP, max(MIN_CLIP, dur if dur < MAX_CLIP else MAX_CLIP))
            sub = vc.subclip(0, min(seg, dur)).without_audio()
            vclips.append(sub)
            total += sub.duration
            if total >= target:
                break
        except Exception:
            continue
    if not vclips:
        raise RuntimeError("No usable clips downloaded.")

    video = concatenate_videoclips(vclips, method="compose").set_duration(target)
    final = video.set_audio(audio)
    final.write_videofile(str(out_path), codec="libx264", audio_codec="aac", fps=30, bitrate=bitrate)

    # Cleanup
    for vc in vclips:
        try: vc.close()
        except: pass
    try: audio.close()
    except: pass
    try: video.close()
    except: pass

# ---------- Burn-in subtitles with ffmpeg ----------
def burn_in_subtitles(in_mp4: Path, srt_path: Path, out_mp4: Path | None = None) -> Path:
    """
    Uses ffmpeg subtitles filter (libass) to burn SRT onto the video.
    If SRT_STYLE is set, apply basic styling via force_style.
    """
    srt_escaped = str(srt_path).replace("\\", "/")
    vf = f"subtitles='{srt_escaped}'"
    if SRT_STYLE:
        vf = f"subtitles='{srt_escaped}':force_style='{SRT_STYLE}'"

    if out_mp4 is None:
        out_mp4 = in_mp4.with_name(in_mp4.stem + "_subbed.mp4")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(in_mp4),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)
    return out_mp4

# ---------- Telegram sending ----------
def load_subscribers(subscribers_file: Path) -> list[int]:
    try:
        raw = Path(subscribers_file).read_text(encoding="utf-8")
        data = json.loads(raw)
        return [int(x) for x in data]
    except Exception:
        return []

def send_video_to_telegram(token: str, chat_id: str, video_path: Path, caption: str = "Daily Survival Tip 🎒"):
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    with open(video_path, "rb") as vf:
        files = {"video": ("video.mp4", vf, "video/mp4")}
        data = {"chat_id": str(chat_id), "caption": caption, "disable_notification": "true"}
        r = requests.post(url, data=data, files=files, timeout=120)
        if r.status_code != 200:
            try: msg = r.json()
            except Exception: msg = r.text
            raise RuntimeError(f"sendVideo failed for {chat_id}: {msg}")

def broadcast_video(token: str, subscribers: list[int], video_path: Path, caption: str):
    if not subscribers:
        print("No subscribers; skipping subscriber broadcast.")
        return
    for cid in subscribers:
        try:
            send_video_to_telegram(token, str(cid), video_path, caption=caption)
            print(f"Sent video to subscriber {cid}")
        except Exception as e:
            print(f"Failed to send to {cid}: {e}", file=sys.stderr)

def send_to_targets(token: str, targets_csv: str, video_path: Path, caption: str):
    targets = [t.strip() for t in targets_csv.split(",") if t.strip()]
    if not targets:
        return
    for t in targets:
        try:
            send_video_to_telegram(token, t, video_path, caption=caption)
            print(f"Sent video to target {t}")
        except Exception as e:
            print(f"Failed to send to {t}: {e}", file=sys.stderr)

# ---------- Main ----------
def main():
    load_dotenv()

    # Env
    pexels_key = os.getenv("PEXELS_API_KEY", "")
    if not pexels_key:
        raise SystemExit("Missing PEXELS_API_KEY (export it in ~/.zshrc and reference via .env).")

    ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5")
    voice = os.getenv("VOX", "en-US-JennyNeural")
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    subs_file = Path(os.getenv("SUBSCRIBERS_FILE", "subscribers.json"))
    outdir = Path(os.getenv("VIDEO_DIR", "daily_videos"))
    bitrate = os.getenv("EXPORT_BITRATE", "3500k")
    target_chat = os.getenv("TARGET_CHAT", "").strip()

    # Caption toggles
    captions_mode = os.getenv("CAPTIONS_MODE", "burn").lower().strip()   # burn|sidecar|both
    send_variant = os.getenv("SEND_VARIANT", "").lower().strip()         # burned|plain
    if send_variant not in ("burned", "plain", ""):
        send_variant = ""
    if captions_mode not in ("burn", "sidecar", "both"):
        captions_mode = "burn"

    ensure_dir(outdir)
    work = Path(tempfile.mkdtemp(prefix="dailyvid_"))

    topic = random.choice(RANDOM_TOPICS)
    date = datetime.date.today().isoformat()
    base_slug = f"daily_video_{slugify(topic)}_{date}"

    try:
        # 1) Script
        script = gen_script_ollama(topic, ollama_url, model)
        (outdir / f"script_{date}.txt").write_text(script, encoding="utf-8")

        # 2) TTS (returns optional, perfectly-synced SRT text when Edge-TTS is used)
        voice_mp3 = work / f"voice_{date}.mp3"
        voice_mp3, srt_from_tts = gen_tts_with_timings(script, voice, voice_mp3)

        # 3) Download stock videos
        query = topic.split(":")[0].split("—")[0]
        clips = fetch_stock_clips(pexels_key, query, work)
        if not clips:
            clips = fetch_stock_clips(pexels_key, "survival emergency preparedness", work)
        if not clips:
            raise RuntimeError("No clips found from Pexels API.")

        # 4) Build video
        out_plain = outdir / f"{base_slug}.mp4"
        build_video(clips, voice_mp3, out_plain, bitrate=bitrate)

        # 5) Captions (always write sidecar SRT)
        srt_text = srt_from_tts if srt_from_tts else make_srt(script, TARGET_SECONDS)
        srt_path = outdir / f"{base_slug}.srt"
        srt_path.write_text(srt_text, encoding="utf-8")

        # 6) Burn (optional, based on CAPTIONS_MODE)
        out_burned = None
        if captions_mode in ("burn", "both"):
            try:
                out_burned = burn_in_subtitles(out_plain, srt_path)
                print(f"✅ Burned captions: {out_burned}")
            except subprocess.CalledProcessError as e:
                print(f"[WARN] Burn-in failed (ffmpeg). Sending plain video instead. Error: {e}", file=sys.stderr)

        # Choose which file to send
        if not send_variant:
            # Auto default: if we have burned or chose burn mode, prefer burned; else plain
            if out_burned and captions_mode in ("burn", "both"):
                chosen = out_burned
            else:
                chosen = out_plain
        else:
            chosen = out_burned if (send_variant == "burned" and out_burned) else out_plain

        # Status
        print(f"✅ Generated (plain): {out_plain}")
        print(f"✅ Generated SRT: {srt_path}")
        if out_burned:
            print(f"✅ Generated (burned): {out_burned}")
        print(f"➡️  Will send: {chosen}")

        # 7) Broadcast via Telegram
        if not token:
            print("No TELEGRAM_BOT_TOKEN set; skipping Telegram send.")
        else:
            caption = f"Daily Survival Tip 🎒 — {topic}"

            # subscribers (from /subscribe)
            subs = load_subscribers(subs_file)
            broadcast_video(token, subs, chosen, caption=caption)

            # explicit targets (channels/groups)
            if target_chat:
                send_to_targets(token, target_chat, chosen, caption=caption)

    finally:
        shutil.rmtree(work, ignore_errors=True)

if __name__ == "__main__":
    main()
