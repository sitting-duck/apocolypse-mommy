# Telegram Bot on Windows (FastAPI Webhooks) + ngrok + Ollama (Streaming)

This is an end-to-end Windows guide using PowerShell (not WSL). You’ll run a FastAPI webhook, expose it with ngrok, and answer via a local Ollama model with streaming replies. <br>

### Prereqs

Python 3.10+ for Windows → https://www.python.org/downloads/windows/

Git for Windows → https://git-scm.com/download/win

Ollama for Windows → https://ollama.com/download

ngrok (install below)

Telegram account to talk to @BotFather

### Create your bot with BotFather

In Telegram, open @BotFather → /newbot

Name it; pick a unique username ending with bot

Copy the HTTP API token (looks like 123456:ABC-...) — keep it secret

(Optional: /setdescription, /setuserpic, /setcommands.)

### Project setup (repo + venv + deps)
```bash
# clone or create a folder
git clone https://github.com/<you>/<repo>.git
cd <repo>

# create & activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install deps
pip install "python-telegram-bot==21.*" fastapi uvicorn httpx

```
Install & set up ngrok (Windows)

Install one of:

Winget

winget install Ngrok.Ngrok


Chocolatey

choco install ngrok


Or download & add ngrok.exe to PATH → https://ngrok.com/download

Authenticate (once):

Log in at https://dashboard.ngrok.com
 → copy Authtoken

In PowerShell:

ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>

persist env vars
```bash
setx TELEGRAM_BOT_TOKEN "123456:ABC..."
setx WEBHOOK_SECRET "yourStrongSecret123"
setx OLLAMA_URL "http://127.0.0.1:11434"
setx OLLAMA_MODEL "qwen2.5"
setx NUM_PREDICT "220"
setx NUM_CTX "2048"
setx KEEP_ALIVE "30m"
```
### generate webhook secret
each bot should have its own unique webhook secret
```bash
# Generate 32 random bytes and encode URL-safe Base64 (no + / =)
$bytes  = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$secret = [Convert]::ToBase64String($bytes).TrimEnd('=').Replace('+','-').Replace('/','_')

# Use it now (current shell) and persist for future shells
$env:WEBHOOK_SECRET = $secret
setx WEBHOOK_SECRET "$secret"

$secret  # prints the value
```
### terminal A fastapi app
```bash
# In your project folder
.\.venv\Scripts\Activate.ps1

# Env vars for this session
$env:TELEGRAM_BOT_TOKEN = "123456:ABC..."
$env:WEBHOOK_SECRET     = "yourStrongSecret123"
$env:OLLAMA_URL         = "http://127.0.0.1:11434"
$env:OLLAMA_MODEL       = "qwen2.5"
$env:NUM_PREDICT        = "220"
$env:NUM_CTX            = "2048"
$env:KEEP_ALIVE         = "30m"

uvicorn main:app --reload --port 8000
```

### Terminal B — Expose with ngrok
```bash
.\.venv\Scripts\Activate.ps1
ngrok http 8000

```




