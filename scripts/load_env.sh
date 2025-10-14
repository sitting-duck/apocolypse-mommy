# scripts/load_env.sh
#!/usr/bin/env sh
set -e

ENV_FILE="${1:-.env}"
ZSHRC="${HOME}/.zshrc"
BACKUP="${ZSHRC}.bak.$(date +%Y%m%d%H%M%S)"

[ -f "$ENV_FILE" ] || { echo "ERROR: $ENV_FILE not found"; return 1 2>/dev/null || exit 1; }

# One-time backup (ignore errors if ~/.zshrc doesn't exist yet)
cp "$ZSHRC" "$BACKUP" 2>/dev/null || true

set_export() {
  key="$1"; val="$2"
  # escape for sed replacement
  esc=$(printf '%s' "$val" | sed -e 's/[\/&]/\\&/g')
  if grep -q "^export $key=" "$ZSHRC" 2>/dev/null; then
    sed -i '' "s|^export $key=.*$|export $key=\"$esc\"|" "$ZSHRC"
  elif grep -q "^$key=" "$ZSHRC" 2>/dev/null; then
    sed -i '' "s|^$key=.*$|export $key=\"$esc\"|" "$ZSHRC"
  else
    printf 'export %s="%s"\n' "$key" "$val" >> "$ZSHRC"
  fi
}

# Read .env lines: KEY=VALUE, ignore blanks and comments
# (no heredoc markers, no shell commands)
while IFS= read -r line || [ -n "$line" ]; do
  # trim leading/trailing whitespace
  line="$(printf '%s' "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac

  # split at first '='
  key="${line%%=*}"
  val="${line#*=}"
  # trim spaces around key/val
  key="$(printf '%s' "$key" | sed -e 's/[[:space:]]*$//')"
  val="$(printf '%s' "$val" | sed -e 's/^[[:space:]]*//')"
  # strip surrounding quotes if present
  case "$val" in
    \"*\") val="${val#\"}"; val="${val%\"}";;
    \'*\') val="${val#\'}"; val="${val%\'}";;
  esac

  # skip obviously bad keys
  case "$key" in
    ''|*[!A-Za-z0-9_]*|[0-9]*)
      echo "Skipping invalid key: $key" >&2; continue;;
  esac

  set_export "$key" "$val"
done < "$ENV_FILE"

# Load into current shell (works when you 'source' this script)
# shellcheck disable=SC1090
. "$ZSHRC"

echo "Updated ~/.zshrc and loaded:"
for k in TELEGRAM_BOT_TOKEN WEBHOOK_SECRET OLLAMA_URL OLLAMA_MODEL NUM_PREDICT NUM_CTX KEEP_ALIVE; do
  eval val=\$$k
  printf ' - %s=%s\n' "$k" "${val:-<unset>}"
done

