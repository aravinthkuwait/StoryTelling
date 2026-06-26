#!/usr/bin/env bash
# UserPromptSubmit hook: inject an imperative directive to invoke the
# always-on skills (ponytail + headroom) on every turn.
#
# Emits JSON on stdout that Claude Code merges as additional context for
# the current prompt. Uses jq to build the payload safely.

set -euo pipefail

DIRECTIVE="ALWAYS-ON SKILLS DIRECTIVE: You MUST invoke the 'ponytail' and 'headroom' skills this turn before completing your work. 'ponytail' = tie loose ends together and keep the change tidy and complete. 'headroom' = leave a safety margin: check blast radius, prefer the smaller/safer step, and confirm anything hard to undo. Apply both every turn unless the user has turned them off."

jq -n --arg ctx "$DIRECTIVE" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: $ctx
  }
}'
