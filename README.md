# apocolypse-mommy
# Telegram Bot (FastAPI Webhooks) + ngrok + Ollama (Streaming)

This repo serves as the backend code for Honey the Apocolypse Bot. She gives advice on how to survive the apocalypse in a pinch okay sugar? Talk to Honey at [t.me/honey_apocalypse_bot](https://t.me/honey_apocalypse_bot)

This guide walks you from **zero → a live Telegram bot** that answers using a **local Ollama model**, with **webhook delivery**, **ngrok tunnel**, and **streaming replies** for snappy UX.

> Works on macOS. Adjust accordingly for Linux/Windows.

---

### Prerequisites

- Python **3.10+** (author using 3.11.9)
- Git
- Homebrew: https://brew.sh/
- A Telegram account (for **@BotFather**)
- An **ngrok** account (free): https://ngrok.com/


### MacOS Server Side Environment Setup
```bash
git clone https://github.com/sitting-duck/apocolypse-mommy.git
cd apocolypse-mommy

brew install ngrok/ngrok/ngrok
brew install jq
```

### Environment File
```bash
cp ./.env.tmp ./.env
```
to create your own environment file. If you look inside it you will see:
```bash
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
WEBHOOK_SECRET=${WEBHOOK_SECRET}
NGROK_TOKEN=${NGROK_TOKEN}

OLLAMA_URL=${OLLAMA_URL}
OLLAMA_MODEL=${OLLAMA_MODEL}
NUM_PREDICT=220
NUM_CTX=2048
KEEP_ALIVE=30m

```

When you run `./scripts/run_app.sh` it will parse your `.env` file and pass the needed info to the app. The `${}` indicates an environment variable. As you collect this info we need for our environment you are welcome to create these environment variables manually using export, to store them in your zshrc or to paste them directly into your .env file. .gitignore will have `.env` ignored so all of your secret tokens will not go to version control.


### ngrok set up
NGrok is a service that will allow you to have up to 3 free endpoints.<br>
Go to ngrok.com → Sign up (free) or Log in. <br>
<img width="1427" height="670" alt="image" src="https://github.com/user-attachments/assets/3b51ad6d-06b0-47ea-95fb-caf2ff5e8b13" /> <br>

In the dashboard, find Getting Started → Your Authtoken. <br>
<img width="1560" height="713" alt="image" src="https://github.com/user-attachments/assets/9379260e-d518-456b-91e0-eae6328be971" /><br>

Copy that token string and paste it into your .env file: <br>


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
Click the copy button to copy your telegram bot token and paste into your .env file for TELEGRAM_BOT_TOKEN.<br>

### Create Webhook
Create a webhook secret. I like to use openssl on the command line to do this since OpenSSL comes with MacOS. <br>
```
# OpenSSL generate (make it URL-safe & trim padding):
openssl rand -base64 48 | tr '+/' '-_' | tr -d '=' | head -c 64

# copy that output string and paste directly into your .env file for WEBHOOK_SECRET
```

## 5) Run everything (3 terminals)

### Terminal A — run your app
```bash
python ./scripts/run_app.sh
```

### Terminal B — expose it
```bash
ngrok http 8000
```
Copy the **https** URL it prints (e.g., `https://xyz.ngrok.app`) and paste it into your .env file for `PUBLIC_URL`.

Inspector UI: http://127.0.0.1:4040



### Terminal C — register the webhook
```bash
source ./scripts/load_env.sh

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


