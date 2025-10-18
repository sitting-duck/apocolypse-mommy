#!/usr/bin/env bash
set -euo pipefail

# 1) Ensure venv exists
if [[ ! -d .venv ]]; then
  echo "[setup] creating venv..."
  python3 -m venv .venv
fi

# 2) Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# 3) Ensure deps (prefer requirements.txt if you have it)
if [[ -f requirements.txt ]]; then
  pip install -r requirements.txt
else
  pip install fastapi uvicorn httpx "python-telegram-bot==21.*"
fi

# 4) Load env
if [[ -f ./scripts/load_env.sh ]]; then
  source ./scripts/load_env.sh
fi

# 5) Run app (use python -m to avoid PATH issues)
exec python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

