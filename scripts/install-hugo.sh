#!/usr/bin/env bash
#
# Installs the exact Hugo version that CI pins, read straight out of the workflow
# so local preview and the deployed build can never drift apart.
#
#   macOS  -> ~/.local/bin/hugo        (no sudo)
#   Linux  -> /usr/local/bin/hugo      (via the .deb package)
#
# Used both by the dev container (postCreateCommand) and on a fresh laptop.
# Safe to re-run; it exits early when the pinned version is already present.
#
# Note on macOS packaging: up to ~0.152 Hugo published a .tar.gz for macOS and
# has since moved to a .pkg only. This script handles both, and extracts the
# .pkg with pkgutil so no sudo and no installer step is needed.
#
# In China, GitHub release downloads are slow. Point the script at any mirror:
#   HUGO_RELEASE_BASE=https://gh-proxy.com/https://github.com/gohugoio/hugo/releases/download \
#     ./scripts/install-hugo.sh
#
set -euo pipefail

cd "$(dirname "$0")/.."

WORKFLOW=".github/workflows/hugo.yml"
[ -f "$WORKFLOW" ] || { echo "error: $WORKFLOW not found" >&2; exit 1; }

HUGO_VERSION="$(grep -oE 'HUGO_VERSION:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+' "$WORKFLOW" \
  | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"

if [ -z "${HUGO_VERSION}" ]; then
  echo "error: could not read HUGO_VERSION from $WORKFLOW" >&2
  exit 1
fi

if command -v hugo >/dev/null 2>&1; then
  CURRENT="$(hugo version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
  if [ "$CURRENT" = "$HUGO_VERSION" ]; then
    echo "Hugo ${HUGO_VERSION} already installed: $(command -v hugo)"
    exit 0
  fi
  echo "Found Hugo ${CURRENT}; installing the pinned ${HUGO_VERSION} instead."
fi

case "$(uname -m)" in
  x86_64 | amd64) ARCH=amd64 ;;
  arm64 | aarch64) ARCH=arm64 ;;
  *)
    echo "error: unsupported architecture $(uname -m)" >&2
    exit 1
    ;;
esac

RELEASE_BASE="${HUGO_RELEASE_BASE:-https://github.com/gohugoio/hugo/releases/download}"
BASE="${RELEASE_BASE}/v${HUGO_VERSION}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

# Absolute path to the binary we install; it is not necessarily on PATH yet.
INSTALLED=""

case "$(uname -s)" in
  Darwin)
    TARGET_DIR="${HOME}/.local/bin"
    mkdir -p "${TARGET_DIR}"

    # Preferred: .tar.gz (Hugo <= ~0.152). Falls back to the .pkg that newer
    # releases ship instead.
    TGZ="hugo_extended_${HUGO_VERSION}_darwin-universal.tar.gz"
    PKG="hugo_extended_${HUGO_VERSION}_darwin-universal.pkg"

    if curl -fSL --retry 2 -o "${TMP_DIR}/hugo.tgz" "${BASE}/${TGZ}" 2>/dev/null; then
      echo "Downloaded ${TGZ}"
      tar xzf "${TMP_DIR}/hugo.tgz" -C "${TMP_DIR}"
      install -m 0755 "${TMP_DIR}/hugo" "${TARGET_DIR}/hugo"
    else
      echo "No macOS tarball for ${HUGO_VERSION}; downloading ${PKG} ..."
      curl -fSL --retry 3 -o "${TMP_DIR}/hugo.pkg" "${BASE}/${PKG}"

      if ! pkgutil --expand-full "${TMP_DIR}/hugo.pkg" "${TMP_DIR}/pkg" 2>/dev/null; then
        # Older macOS: expand, then unpack the payload by hand.
        pkgutil --expand "${TMP_DIR}/hugo.pkg" "${TMP_DIR}/pkg"
        ( cd "${TMP_DIR}/pkg" && cat Payload | tar xf - )
      fi

      PAYLOAD="$(find "${TMP_DIR}/pkg" -type f -name hugo -size +5M | head -1)"
      if [ -z "${PAYLOAD}" ]; then
        echo "error: could not locate the hugo binary inside ${PKG}" >&2
        exit 1
      fi
      xattr -d com.apple.quarantine "${PAYLOAD}" 2>/dev/null || true
      install -m 0755 "${PAYLOAD}" "${TARGET_DIR}/hugo"
    fi

    INSTALLED="${TARGET_DIR}/hugo"
    echo "Installed: ${INSTALLED}"
    case ":${PATH}:" in
      *":${TARGET_DIR}:"*) ;;
      *)
        echo
        echo "NOTE: ${TARGET_DIR} is not on your PATH. Add it to ~/.zshrc:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo
        ;;
    esac
    ;;
  Linux)
    FILE="hugo_extended_${HUGO_VERSION}_linux-${ARCH}.deb"
    echo "Downloading ${FILE} ..."
    curl -fSL --retry 3 -o "${TMP_DIR}/hugo.deb" "${BASE}/${FILE}"
    sudo dpkg -i "${TMP_DIR}/hugo.deb" >/dev/null
    INSTALLED="$(command -v hugo || true)"
    echo "Installed: ${INSTALLED}"
    ;;
  *)
    echo "error: unsupported OS $(uname -s)" >&2
    exit 1
    ;;
esac

echo
if [ -x "${INSTALLED}" ]; then
  "${INSTALLED}" version
elif command -v hugo >/dev/null 2>&1; then
  hugo version
fi
echo
echo "Next:"
echo "  hugo server -D                        # live preview on port 1313"
echo "  hugo server -D --bind 0.0.0.0         # ...when running inside the dev container"
echo "  ./scripts/new-post.sh \"My title\"      # start a new post"
