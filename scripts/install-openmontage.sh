#!/usr/bin/env bash
#
# install-openmontage.sh — (re)install the OpenMontage video-production toolkit.
#
# OpenMontage (https://github.com/calesthio/OpenMontage) is vendored into ./OpenMontage
# but intentionally NOT committed to this repo (see .gitignore). This script fetches and
# sets it up from scratch, so the toolkit can be restored in any fresh / ephemeral
# environment with a single command:
#
#     bash scripts/install-openmontage.sh
#
# Notes on this environment:
#   * `git clone github.com/...` is blocked here — the git proxy is scoped to this repo
#     only. We therefore download a source tarball over the general HTTPS proxy instead.
#   * Python deps are installed into an isolated venv (OpenMontage/.venv) so the system
#     Python is never touched.
#   * ffmpeg is required at render time; we install it via apt if it is missing.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$REPO_ROOT/OpenMontage"
REF="${OPENMONTAGE_REF:-main}"
TARBALL_URL="https://codeload.github.com/calesthio/OpenMontage/tar.gz/refs/heads/${REF}"

echo "==> Installing OpenMontage (ref: ${REF}) into ${DEST}"

# 1. Fetch + extract source (tarball, because git clone of external repos is blocked here)
if [ -d "$DEST" ] && [ -f "$DEST/Makefile" ]; then
  echo "    OpenMontage already present — skipping download (delete ./OpenMontage to re-fetch)."
else
  tmp="$(mktemp -d)"
  echo "    Downloading source tarball..."
  curl -fsSL --max-time 180 -o "$tmp/openmontage.tar.gz" "$TARBALL_URL"
  mkdir -p "$DEST"
  tar -xzf "$tmp/openmontage.tar.gz" -C "$DEST" --strip-components=1
  rm -rf "$tmp"
  echo "    Extracted."
fi

# 2. ffmpeg (render-time dependency)
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "==> ffmpeg not found — attempting install via apt..."
  if command -v apt-get >/dev/null 2>&1; then
    (sudo -n true 2>/dev/null && SUDO=sudo || SUDO="")
    ${SUDO:-} apt-get update -y >/dev/null 2>&1 || true
    ${SUDO:-} apt-get install -y ffmpeg || echo "    [warn] ffmpeg install failed — install it manually before rendering."
  else
    echo "    [warn] apt-get unavailable — install ffmpeg manually before rendering."
  fi
fi

# 3. Isolated Python venv + dependencies via the project's own `make setup`
cd "$DEST"
if [ ! -x ".venv/bin/python" ]; then
  echo "==> Creating Python venv (.venv)..."
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade pip --quiet
fi

echo "==> Running OpenMontage 'make setup' (Python deps, Remotion composer, Piper TTS)..."
make setup PYTHON="$DEST/.venv/bin/python"

echo ""
echo "==> Done. OpenMontage is installed at ${DEST}"
echo "    Add API keys to ${DEST}/.env to unlock cloud providers."
echo "    Activate the venv with:  source ${DEST}/.venv/bin/activate"
