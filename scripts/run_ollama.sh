#!/usr/bin/env bash
# scripts/run_ollama.sh
# Start Ollama in the FOREGROUND (current terminal) so you can see logs.
# It will:
#  - load .env (if present) just to echo OLLAMA_MODEL/URL
#  - stop any background services / stale processes
#  - ensure port 11434 is free
#  - exec `ollama serve` in the foreground
#
# Usage:
#   chmod +x scripts/run_ollama.sh
#   ./scripts/run_ollama.sh [PATH_TO_ENV]        # default: .env

set -euo pipefail

ENV_FILE="${1:-.env}"
API="http://127.0.0.1:11434"
PORT="11434"

# --- load .env (non-invasive; for echo only) ---
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC2046,SC2002
  export $(cat "$ENV_FILE" \
    | grep -E '^[[:space:]]*(#|$)|^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*=' -v \
    | sed -e 's/^[[:space:]]*export[[:space:]]*//' )
fi
: "${OLLAMA_MODEL:=qwen2.5}"
: "${OLLAMA_URL:=http://127.0.0.1:11434}"

echo "=== Ollama foreground runner ==="
echo "Env file: $ENV_FILE (if present)"
echo "OLLAMA_URL: $OLLAMA_URL"
echo "OLLAMA_MODEL (tip only): $OLLAMA_MODEL"
echo

# --- helpers ---
is_up() { curl -sSf "$API/api/version" >/dev/null 2>&1; }
port_in_use() { lsof -i TCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; }

stop_ollama() {
  echo "Stopping any running Ollama…"
  # Homebrew service
  if command -v brew >/dev/null 2>&1; then
    brew services stop ollama 2>/dev/null || true
  fi
  # launchd agent (GUI session)
  launchctl bootout "gui/$UID/com.ollama.ollama" 2>/dev/null || true
  # any leftover processes
  pkill -f "[o]llama" 2>/dev/null || true

  # wait for port to be released
  for _ in {1..30}; do
    if ! port_in_use; then
      echo "Port $PORT is free."
      return 0
    fi
    sleep 0.2
  done
  echo "WARN: Port $PORT still appears busy." >&2
}

# --- main ---
stop_ollama

echo
echo "Launching: ollama serve (foreground)"
echo "Press Ctrl+C to stop."
echo

# Important: run in the foreground so you can see all logs
exec ollama serve

