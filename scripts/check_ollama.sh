#!/usr/bin/env bash
set -euo pipefail

is_up() { curl -sSf http://127.0.0.1:11434/api/version >/dev/null 2>&1; }

if is_up; then
  echo "Ollama is running."
else
  echo "Starting Ollama…"
  if command -v brew >/dev/null && brew services list | grep -q "^ollama"; then
    brew services start ollama || true
  else
    launchctl kickstart -k gui/$UID/com.ollama.ollama || ollama serve &
  fi

  # wait up to ~8s
  for i in {1..16}; do
    is_up && { echo "Ollama is up."; exit 0; }
    sleep 0.5
  done
  echo "Ollama failed to start."
  exit 1
fi

