#!/usr/bin/env bash
# Publish: flip draft -> false, commit everything, push to master.
# The GitHub Actions workflow then rebuilds and deploys the site (~1 minute).
#
# Usage:
#   ./scripts/publish.sh                          # publish everything already staged/modified
#   ./scripts/publish.sh content/posts/foo.md     # also un-draft this post
#   ./scripts/publish.sh content/posts/foo.md "Add post about X"

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

FILE="${1:-}"
MSG="${2:-}"

if [ -n "$FILE" ]; then
  if [ ! -f "$FILE" ]; then
    echo "No such file: $FILE"
    exit 1
  fi
  if grep -qE '^draft:[[:space:]]*true[[:space:]]*$' "$FILE"; then
    perl -pi -e 's/^draft:\s*true\s*$/draft: false/' "$FILE"
    echo "Un-drafted: $FILE"
  else
    echo "Note: $FILE is not marked draft: true (nothing to flip)."
  fi
fi

# Refuse to push while a draft would silently stay unpublished.
DRAFTS="$(grep -rlE '^draft:[[:space:]]*true[[:space:]]*$' content/posts 2>/dev/null || true)"
if [ -n "$DRAFTS" ]; then
  echo
  echo "Still in draft (will NOT be published):"
  printf '  %s\n' $DRAFTS
  echo
fi

git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit — site is already up to date."
  exit 0
fi

git commit -q -m "${MSG:-Publish post ($(date +%Y-%m-%d))}"
git push origin master

echo
echo "Pushed to origin/master."
echo "Watch the build : https://github.com/pinxiong/pinxiong.github.io/actions"
echo "Live site       : https://xiongpin.dev"
