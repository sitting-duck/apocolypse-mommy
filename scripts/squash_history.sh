#!/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-main}"
BACKUP="backup-${BRANCH}-$(date +%Y%m%d%H%M%S)"

git checkout "$BRANCH"
git pull --rebase origin "$BRANCH"

echo "Creating backup branch: $BACKUP"
git branch "$BACKUP"
git push origin "$BACKUP"

git checkout --orphan temp-"$BRANCH"
git add -A
git commit -m "Initial commit"

git branch -D "$BRANCH"
git branch -m "$BRANCH"

echo "Force pushing new single-commit history to origin/$BRANCH"
git push -f origin "$BRANCH"

echo "Done. Old history preserved at origin/$BACKUP"

