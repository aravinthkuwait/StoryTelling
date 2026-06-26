#!/usr/bin/env bash
# SessionStart hook: print a banner announcing the always-on 'headroom' skill.
set -euo pipefail

cat <<'BANNER'
🪜 headroom [always-on]: leave a safety margin — check blast radius, prefer the safer step.
BANNER
