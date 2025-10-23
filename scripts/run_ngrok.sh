#!/usr/bin/env bash
set -euo pipefail

# 1) Load env
if [[ -f ./scripts/load_env.sh ]]; then
  source ./scripts/load_env.sh
fi

# 2) Set ngrok token if it hasn't been set already (only needs to be set once)
CFG="${HOME}/.config/ngrok/ngrok.yml"
if [ -f "$CFG" ] && grep -q '^authtoken:' "$CFG"; then
  echo "ngrok authtoken already set in $CFG"
else
  ngrok config add-authtoken "$NGROK_TOKEN"
fi

# ensure only one ngrok is running for this account to avoid confusion
# (free plan supports one online tunnel at a time reliably)
pgrep -f "ngrok http" >/dev/null && { echo "ngrok already running"; exit 0; }
exec ngrok http 8000

