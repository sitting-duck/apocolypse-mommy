#!/usr/bin/env bash
set -euo pipefail
./scripts/load_env.sh

if ! command -v jq >/dev/null; then
  echo "Please: brew install jq"; exit 1
fi

# Get the current https forwarding URL from local ngrok API
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels \
  | jq -r '.tunnels[] | select(.public_url | startswith("https")) | .public_url' | head -n1)

if [[ -z "${NGROK_URL}" || "${NGROK_URL}" == "null" ]]; then
  echo "No https ngrok tunnel detected. Start ngrok first: ./scripts/run_ngrok.sh"; exit 1
fi

echo "Registering webhook to ${NGROK_URL}/telegram/${TELEGRAM_BOT_TOKEN}"

curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${NGROK_URL}/telegram/${TELEGRAM_BOT_TOKEN}" \
  -d "secret_token=${WEBHOOK_SECRET}" \
  -d "drop_pending_updates=true" \
  -d 'allowed_updates=["message","callback_query"]' | jq

echo "Webhook info:"
curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | jq

