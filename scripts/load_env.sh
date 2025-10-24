# scripts/load_env.sh
#!/usr/bin/env sh
# Usage:
#   source scripts/load_env.sh            # uses ./.env
#   source scripts/load_env.sh path/to/.env
#
# Exports variables from a .env file into the CURRENT shell session only.
# It does NOT write to ~/.zshrc.

set -e

ENV_FILE="${1:-.env}"

# Must be sourced; detect (best-effort)
case "$0" in
  -*|sh|bash|zsh|ksh) : ;;  # okay when sourced
  *)
    printf "NOTE: You should 'source %s' so exports affect your current shell.\n" "$0"
    ;;
esac

[ -f "$ENV_FILE" ] || { echo "ERROR: $ENV_FILE not found"; return 1 2>/dev/null || exit 1; }

exported_keys=""

# Read .env lines: KEY=VALUE, ignore blanks and comments
# Supports optional leading 'export ', and quoted values.
while IFS= read -r line || [ -n "$line" ]; do
  # trim leading/trailing whitespace
  line=$(printf '%s' "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
  [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac

  # allow "export KEY=VALUE"
  case "$line" in
    export\ *) line=${line#export };;
  esac

  # split at first '='
  case "$line" in
    *=*) : ;;
    *)   echo "Skipping (no '='): $line" >&2; continue;;
  esac
  key=${line%%=*}
  val=${line#*=}

  # trim spaces around key/val
  key=$(printf '%s' "$key" | sed -e 's/[[:space:]]*$//')
  val=$(printf '%s' "$val" | sed -e 's/^[[:space:]]*//')

  # strip surrounding quotes if present
  case "$val" in
    \"*\") val=${val#\"}; val=${val%\"} ;;
    \'*\') val=${val#\'}; val=${val%\'} ;;
  esac

  # basic key validation (POSIX-ish var name)
  case "$key" in
    ''|*[!A-Za-z0-9_]*|[0-9]*)
      echo "Skipping invalid key: $key" >&2; continue;;
  esac

  # Export into current shell. Assignments are not word-split.
  # shellcheck disable=SC2163
  export "$key=$val"
  exported_keys="${exported_keys} $key"
done < "$ENV_FILE"

echo "Loaded from $ENV_FILE:"
for k in $exported_keys; do
  eval v=\$$k
  printf " - %s=%s\n" "$k" "${v:-<unset>}"
done
