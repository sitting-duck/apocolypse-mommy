#!/usr/bin/env bash
set -euo pipefail
# ensure only one ngrok is running for this account to avoid confusion
# (free plan supports one online tunnel at a time reliably)
pgrep -f "ngrok http" >/dev/null && { echo "ngrok already running"; exit 0; }
exec ngrok http 8000

