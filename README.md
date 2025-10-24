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

cp ./.env.tmp ./.env

# note : author using python 3.14.0 at time of writing
python -m venv .venv && source .venv/bin/activate

# if you want my exact same package versions
pip install -r requirements.txt

brew install ngrok/ngrok/ngrok
brew install jq
brew install ollama
```

### ngrok set up
NGrok is a service that will allow you to have up to 3 free endpoints.<br>
Go to ngrok.com → Sign up (free) or Log in. <br>
<img width="1427" height="670" alt="image" src="https://github.com/user-attachments/assets/3b51ad6d-06b0-47ea-95fb-caf2ff5e8b13" /> <br>

In the dashboard, find Getting Started → [Your Authtoken.](https://dashboard.ngrok.com/get-started/your-authtoken) <br>
<img width="1560" height="713" alt="image" src="https://github.com/user-attachments/assets/9379260e-d518-456b-91e0-eae6328be971" /><br>

Paste the token into `NGROK_TOKEN` in your `.env` file. 

# Webhook
Run `scripts/register_webhook.sh`. Check your `.env` file to make sure `WEBHOOK_SECRET` has a value. The script creates one using OpenSSL but if for some reason it fails you can use any string generator and just create one yourself, paste it into `.env`, and then run `scripts/register_webhook.sh`.


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
Click the copy button to copy your telegram bot token and paste into your .env file for `TELEGRAM_BOT_TOKEN`. 

## Run everything (2 terminals)

### Terminal A — run your app
```bash
scripts/run_app.sh
```
Copy the **https** URL it prints (e.g., `https://xyz.ngrok.app`) and paste it into your .env file for `PUBLIC_URL`.


### Terminal C - Ollama
```bash
./scripts/check_ollama.sh
ollama serve
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


