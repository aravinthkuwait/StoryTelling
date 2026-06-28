# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Default Skills (always-on)

These skills are active on **every turn** of every session — they are enforced
by hooks under `.claude/hooks/` and registered in `.claude/settings.json`, and
do not need to be invoked manually:

- **ponytail** (`.claude/skills/ponytail/SKILL.md`) — tie loose ends together.
  Before finishing any turn, confirm the change is complete, the working tree
  reflects intent, and nothing was left half-done.
- **headroom** (`.claude/skills/headroom/SKILL.md`) — leave a safety margin.
  Before acting, check scope, blast radius, and reversibility; prefer the
  smaller, safer step and confirm anything hard to undo.

Enforcement:

- `.claude/hooks/enforce-skills.sh` — a `UserPromptSubmit` hook that injects an
  imperative directive to invoke **ponytail** + **headroom** every turn.
- `.claude/hooks/session-banner-ponytail.sh` and
  `.claude/hooks/session-banner-headroom.sh` — `SessionStart` banner hooks that
  announce each always-on skill at the start of a session.

To disable for a session, tell Claude "stop ponytail" / "stop headroom".

## Higgsfield Credit Optimization

When using Higgsfield AI for video/image generation, follow this model hierarchy to conserve credits:

| Priority | Model | Credits | When to use |
|---|---|---|---|
| 1 | Nano Banana Pro | ~2 cr | Image drafts, concept tests |
| 2 | Wan 2.5 Fast | ~9 cr | Video drafts, iteration |
| 3 | Kling 3.0 | ~8-10 cr | Final video if Veo 3 is overkill |
| 4 | Google Veo 3 Fast | ~22 cr | Mid-quality final |
| 5 | Google Veo 3 | ~58 cr | **Final render only** |
| 6 | Seedance 2.0 | premium | Rare / specific need |

### Rules
- **Drafts & iteration** → always use Wan 2.5 Fast or Nano Banana Pro (cheapest options)
- **NEVER** use Google Veo 3 (~58 cr) for test or draft generations
- **Final render only** → Google Veo 3 is permitted for the final polished output
- Batch parallel generations to maximize concurrent slots per plan
