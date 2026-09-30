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
  if grep -qE '^draft:[ \t]*true[ \t]*$' "$FILE"; then
    # NOTE: use [ \t] rather than \s — in perl -p the line still contains its
    # trailing newline, and \s is greedy enough to eat it, which would join the
    # next front-matter key onto the same line.
    perl -pi -e 's/^draft:[ \t]*true[ \t]*$/draft: false/' "$FILE"
    echo "Un-drafted: $FILE"
  else
    echo "Note: $FILE is not marked draft: true (nothing to flip)."
  fi

  # Sanity check: front matter must still start/close with --- and hold draft: false.
  if [ "$(head -1 "$FILE")" != "---" ] || [ "$(grep -cE '^---[ \t]*$' "$FILE")" -lt 2 ] \
     || ! grep -qE '^draft:[ \t]*false[ \t]*$' "$FILE"; then
    echo
    echo "Front matter looks broken in $FILE — not committing. Inspect it:"
    echo "  head -10 \"$FILE\""
    exit 1
  fi
fi

# Refuse to push while a draft would silently stay unpublished.
DRAFTS="$(grep -rlE '^draft:[ \t]*true[ \t]*$' content/posts 2>/dev/null || true)"
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
