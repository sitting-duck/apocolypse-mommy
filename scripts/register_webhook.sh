#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".env"

# --- Load env file (initial) ---
./scripts/load_env.sh "$ENV_FILE" >/dev/null

# --- Ensure jq is installed ---
if ! command -v jq >/dev/null; then
  echo "Please: brew install jq"
  exit 1
fi

# --- Generate WEBHOOK_SECRET if missing ---
if [ -z "${WEBHOOK_SECRET:-}" ]; then
  echo "WEBHOOK_SECRET is empty — generating new secret..."
  NEW_SECRET=$(openssl rand -base64 48 | tr '+/' '-_' | tr -d '=' | head -c 64)

  # Append or replace in .env
  if grep -q "^WEBHOOK_SECRET=" "$ENV_FILE"; then
    # Replace existing line
    sed -i '' "s|^WEBHOOK_SECRET=.*|WEBHOOK_SECRET=\"$NEW_SECRET\"|" "$ENV_FILE"
  else
    # Append new line
    echo "WEBHOOK_SECRET=\"$NEW_SECRET\"" >> "$ENV_FILE"
  fi

  echo "Generated new WEBHOOK_SECRET and wrote to $ENV_FILE."
  # Reload environment after modification
  ./scripts/load_env.sh "$ENV_FILE" >/dev/null
else
  echo "Existing WEBHOOK_SECRET found."
fi

# --- Check ngrok tunnel availability ---
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels \
  | jq -r '.tunnels[] | select(.public_url | startswith("https")) | .public_url' | head -n1)

if [[ -z "${NGROK_URL}" || "${NGROK_URL}" == "null" ]]; then
  echo "❌ No https ngrok tunnel detected."
  echo "👉 Start ngrok first: ./scripts/run_ngrok.sh"
  exit 1
fi

echo "Registering webhook to ${NGROK_URL}/telegram/${TELEGRAM_BOT_TOKEN}"

# --- Register webhook with Telegram ---
curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${NGROK_URL}/telegram/${TELEGRAM_BOT_TOKEN}" \
  -d "secret_token=${WEBHOOK_SECRET}" \
  -d "drop_pending_updates=true" \
  -d 'allowed_updates=["message","callback_query"]' | jq

# --- Confirm ---
echo "Webhook info:"
curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | jq

