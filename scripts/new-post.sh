#!/usr/bin/env bash
# Create a new English post from the 4-part archetype, then start a local preview.
#
# Usage:
#   ./scripts/new-post.sh "How I Cut EC2 Cold Start by 40%"
#
# The post is created as a DRAFT (draft: true), so it will NOT go live even if
# you push. Preview it with the dev server, edit it, and when it is ready run
# ./scripts/publish.sh to flip it live.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if [ $# -lt 1 ]; then
  echo "Usage: ./scripts/new-post.sh \"My article title\""
  exit 1
fi

TITLE="$1"
SLUG="$(printf '%s' "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"

if [ -z "$SLUG" ]; then
  echo "Could not derive a filename from that title. Use ASCII letters/digits."
  exit 1
fi

FILE="content/posts/${SLUG}.md"
if [ -e "$FILE" ]; then
  echo "Already exists: $FILE"
  exit 1
fi

hugo new "posts/${SLUG}.md" >/dev/null

# hugo new derives the title from the filename; restore the human-readable one.
TITLE="$TITLE" FILE="$FILE" python3 - <<'PY'
import io, os, re
path, title = os.environ["FILE"], os.environ["TITLE"]
s = io.open(path, encoding="utf-8").read()
s = re.sub(r'^title:.*$', 'title: "%s"' % title.replace('"', '\\"'), s, count=1, flags=re.M)
io.open(path, "w", encoding="utf-8").write(s)
PY

echo
echo "Created  : $FILE"
echo "Live URL : https://xiongpin.dev/posts/${SLUG}/  (after publish)"
echo
echo "Preview  : hugo server -D      -> http://localhost:1313"
echo "Publish  : ./scripts/publish.sh \"$FILE\""
echo
