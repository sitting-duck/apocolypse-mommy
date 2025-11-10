# apocolypse-mommy
# Telegram Bot (FastAPI Webhooks) + ngrok + Ollama (Streaming)

This guide walks you from **zero → a live Telegram bot** that answers using a **local Ollama model**, with **webhook delivery**, **ngrok tunnel**, and **streaming replies** for snappy UX.

> Works on macOS. Adjust accordingly for Linux/Windows.

---

## 0) Prerequisites

- Python **3.10+**
- Git
- (Optional but handy) Homebrew: https://brew.sh/
- A Telegram account (for **@BotFather**)
- An **ngrok** account (free): https://ngrok.com/



### MacOS Server Side Environment Setup
```bash
# note : author using python 3.14.0 at time of writing
python -m venv .venv && source .venv/bin/activate

# if you want my exact same package versions
pip install requirements.txt

# if you want latest package versions
pip install "python-telegram-bot==21.*" fastapi uvicorn httpx

brew install ngrok/ngrok/ngrok
```
Note:
uvicorn is a fast ASGI web server for Python. You use it to run async web apps like FastAPI or Starlette—it listens on a port and serves your app over HTTP so services (like Telegram via your webhook) can reach it.

Quick facts:

ASGI server (async-friendly; supports websockets, high concurrency).

Very lightweight and fast (can use uvloop, httptools).

Simple CLI to start your app.

### ngrok set up
Go to ngrok.com → Sign up (free) or Log in. <br>
<img width="1427" height="670" alt="image" src="https://github.com/user-attachments/assets/3b51ad6d-06b0-47ea-95fb-caf2ff5e8b13" /> <br>

In the dashboard, find Getting Started → Your Authtoken. <br>
<img width="1560" height="713" alt="image" src="https://github.com/user-attachments/assets/9379260e-d518-456b-91e0-eae6328be971" /><br>

```bash
ngrok config add-authtoken <YOUR_TOKEN>  # once, from ngrok dashboard
ngrok http 8000

brew install jq

```


### Create new bot in Telegram
<img width="385" height="632" alt="image" src="https://github.com/user-attachments/assets/c1857b1e-f81b-4821-bea0-14b62b755b9f" /> <br>
Search for @BotFather to begin a chat with BotFather. You can interact with BotFather to create your own bots. <br> 
Once you find BotFather click the Open button pictured above <br>
<br>
<img width="394" height="542" alt="image" src="https://github.com/user-attachments/assets/8cdba8a5-6c51-4435-a7c1-a78a259b77bc" /> <br>
Click the "Create a New Bot" button pictured above. <br>
<br>
<img width="406" height="692" alt="image" src="https://github.com/user-attachments/assets/e1cdaec4-b443-4d14-83c7-4eee1d5e9254" /> <br>
Fill out the form and click the "Create Bot" button pictured above. <br>
<br> 
<img width="401" height="442" alt="image" src="https://github.com/user-attachments/assets/3765bff1-fa9e-4722-b2e2-a4b6db7ef703" /><br>
Click the copy button to copy your telegram bot token. We are going to create a Github Secret for this secret token. It is a character string that should NOT be pasted into your source code. That is a security vulnerability. <br>

### Store the Bot Token
Let's add this secret using the CLI. If you haven't already, install gh. (GitHub CLI) = convenience tool for GitHub-specific tasks (APIs). It doesn’t replace git; it complements it, whereas the `git` command line tool is mostly used for version control tasks such as merges, pushes, commits, etc. <br>

```bash
brew install gh 
```

Now let's create the secret. Paste your own token string you copied from Telegram instead of "12345:ABC..." <br>
We upload it to Github. 
```bash
gh auth login
gh secret set TELEGRAM_BOT_TOKEN -b"123456:ABC..."
```
We also add it to our local environment and make it remain between sessions by appending it to our ~/.zshrc file. 
```bash
echo 'export TELEGRAM_BOT_TOKEN="123456:ABC..."' >> ~/.zshrc
exec zsh   # or: source ~/.zshrc
echo "$TELEGRAM_BOT_TOKEN"
```

### Create Webhook (MacOS)
Webhooks (production): Telegram pushes updates to your HTTPS URL. Best for reliable, scalable deployment. There is another method called long-polling for setting up the chat bot for dev purposes I will not go into, since I believe setting up the webhook is rather simple and fast. <br>

Create a webhook secret. I like to use openssl on the command line to do. Open SSL comes with MacOS. <br>
```
# OpenSSL generate (make it URL-safe & trim padding):
openssl rand -base64 48 | tr '+/' '-_' | tr -d '=' | head -c 64
# copy that output string to use in your next command.

export WEBHOOK_SECRET=aStrongSecret123
gh secret set TELEGRAM_BOT_TOKEN -b"123456:ABC..."
```

Let's go ahead and append this to our ~/.zshrc file to save this value in between sessions: <br>
```bash
echo 'export WEBHOOK_SECRET="aStrongSecret123"' >> ~/.zshrc
exec zsh   # or: source ~/.zshrc
echo "$WEBHOOK_SECRET"

```

## 5) Run everything (3 terminals)

### Terminal A — run your app
```bash
source .venv/bin/activate
export TELEGRAM_BOT_TOKEN=123456:ABC...    # from BotFather
export WEBHOOK_SECRET=yourStrongSecret123
export OLLAMA_URL=http://127.0.0.1:11434
export OLLAMA_MODEL=qwen2.5                # or llama3.1 / mistral / gemma3
export NUM_PREDICT=220
export NUM_CTX=2048
export KEEP_ALIVE=30m

uvicorn main:app --reload --port 8000
```

#### Persist these env vars in `~/.zshrc` (optional)

> This stores secrets in plain text on your machine. Fine for local dev, but don’t commit them anywhere.

```bash
# append (creates or updates keys if they already exist)
add_or_update() {
  KEY="$1"; VAL="$2"
  if grep -q "^export ${KEY}=" ~/.zshrc; then
    # macOS sed needs the '' arg
    sed -i '' "s/^export ${KEY}=.*/export ${KEY}="${VAL//\//\/}"/" ~/.zshrc
  else
    echo "export ${KEY}="${VAL}"" >> ~/.zshrc
  fi
}

add_or_update TELEGRAM_BOT_TOKEN "123456:ABC..."     # <-- put your real token
add_or_update WEBHOOK_SECRET     "yourStrongSecret123"
add_or_update OLLAMA_URL         "http://127.0.0.1:11434"
add_or_update OLLAMA_MODEL       "qwen2.5"           # or llama3.1 / mistral / gemma3
add_or_update NUM_PREDICT        "220"
add_or_update NUM_CTX            "2048"
add_or_update KEEP_ALIVE         "30m"

# reload the shell
exec zsh   # or: source ~/.zshrc
```

#### Push these secrets to your GitHub repo (with `gh`)

> Run these **in your repo directory**. This stores secrets for **GitHub Actions** so deploy workflows can read them.
> First time only: `brew install gh && gh auth login`

Use your current shell env values:
```bash
gh secret set TELEGRAM_BOT_TOKEN -b"$TELEGRAM_BOT_TOKEN"
gh secret set WEBHOOK_SECRET     -b"$WEBHOOK_SECRET"
gh secret set OLLAMA_URL         -b"$OLLAMA_URL"
gh secret set OLLAMA_MODEL       -b"$OLLAMA_MODEL"
gh secret set NUM_PREDICT        -b"$NUM_PREDICT"
gh secret set NUM_CTX            -b"$NUM_CTX"
gh secret set KEEP_ALIVE         -b"$KEEP_ALIVE"
```

### Terminal B — expose it
```bash
ngrok http 8000
```
Copy the **https** URL it prints (e.g., `https://xyz.ngrok.app`).  
Inspector UI: http://127.0.0.1:4040

### Terminal C — register the webhook
```bash
export TELEGRAM_BOT_TOKEN=123456:ABC...
export WEBHOOK_SECRET=yourStrongSecret123
export PUBLIC_URL=https://xyz.ngrok.app  # from Terminal B

curl -sS -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook"   -d "url=$PUBLIC_URL/telegram/$TELEGRAM_BOT_TOKEN"   -d "secret_token=$WEBHOOK_SECRET"   -d "drop_pending_updates=true"   -d 'allowed_updates=["message","callback_query"]'
```

Verify:
```bash
curl -sS "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo" | python -m json.tool
# Look for result.url, result.pending_update_count, and absence of last_error_message.
```
## 6) Test in Telegram

- Open your bot by its **username** or https://t.me/<your_bot_username>
- Tap **Start** → you should see “Webhook online ✅ …”
- Send a message → you should see a **streaming** reply.
- Watch requests/responses in the ngrok inspector (`http://127.0.0.1:4040`).

---

## 7) Troubleshooting

- **403 in inspector** → secret mismatch. Ensure the same `WEBHOOK_SECRET` in Terminal A and your `setWebhook` call.
- **404/405** → webhook path must be exactly `/telegram/<BOT_TOKEN>` and via **POST**. Re-run `setWebhook`.
- **500** → check Terminal A traceback (missing env var, typos, etc.).
- **No response** → confirm Uvicorn is on `:8000` and ngrok is forwarding to it; use the **https** URL in `setWebhook`.
- **“Message is not modified”** → already handled by the no-op edit safe code above.

---


### Ollama
```bash
export OLLAMA_MODEL="qwen2.5:latest"
```



```bash
uvicorn main:app --reload --port 8000
```



``` bash
brew install ngrok/ngrok/ngrok
ngrok config add-authtoken <TOKEN>
```
