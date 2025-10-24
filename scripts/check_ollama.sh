# scripts/check_ollama.sh
#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.env}"

# --- helpers ---
is_up() {
  curl -sSf http://127.0.0.1:11434/api/version >/dev/null 2>&1
}

# Extract a single KEY=value from .env without sourcing the whole file.
# - Handles optional quotes.
# - Ignores commented/blank lines and leading "export ".
get_env() {
  local key="$1"
  [ -f "$ENV_FILE" ] || { echo "WARN: $ENV_FILE not found; using defaults." >&2; return 1; }
  # pick the first non-comment line that starts with KEY=
  local line
  line="$(grep -E '^[[:space:]]*(export[[:space:]]+)?'"$key"'=' "$ENV_FILE" | grep -v '^[[:space:]]*#' | head -n 1 || true)"
  [ -n "$line" ] || return 1
  # strip leading "export " and KEY=
  line="${line#export }"
  line="${line#"$key"=}"
  # trim surrounding whitespace
  line="$(printf '%s' "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  # strip surrounding quotes
  case "$line" in
    \"*\") line="${line#\"}"; line="${line%\"}";;
    \'*\') line="${line#\'}"; line="${line%\'}";;
  esac
  printf '%s' "$line"
}

ensure_model() {
  local model="$1"
  if [ -z "$model" ]; then
    echo "No OLLAMA_MODEL specified; skipping model check." >&2
    return 0
  fi
  # Fast check: does 'ollama show <model>' succeed?
  if ollama show "$model" >/dev/null 2>&1; then
    echo "Model '$model' is available."
    return 0
  fi
  echo "Model '$model' not found locally. Pulling…"
  ollama pull "$model"
  echo "Pulled model '$model'."
}

# --- 1) ensure server is up ---
if is_up; then
  echo "Ollama is running."
else
  echo "Starting Ollama…"
  if command -v brew >/dev/null 2>&1 && brew services list | grep -q "^ollama[[:space:]]"; then
    brew services start ollama || true
  else
    # launchd (GUI session) or fallback to foreground backgrounding
    launchctl kickstart -k "gui/$UID/com.ollama.ollama" 2>/dev/null || ollama serve >/dev/null 2>&1 &
  fi

  # wait up to ~8s
  for _ in {1..16}; do
    if is_up; then
      echo "Ollama is up."
      break
    fi
    sleep 0.5
  done
  if ! is_up; then
    echo "Ollama failed to start." >&2
    exit 1
  fi
fi

# --- 2) ensure requested model exists (from .env) ---
OLLAMA_MODEL="$(get_env OLLAMA_MODEL || true)"
# default if not present in .env
: "${OLLAMA_MODEL:=qwen2.5}"

ensure_model "$OLLAMA_MODEL"

