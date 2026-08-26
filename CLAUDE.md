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

## OpenMontage video creation

[OpenMontage](https://github.com/calesthio/OpenMontage) is installed in this repo as the
**default agent-driven video production toolkit**. Use it whenever the user asks to create
a video "using OpenMontage" (or asks for a video and OpenMontage is the intended tool).

- **Location:** `./OpenMontage/` (vendored, gitignored — not committed here).
- **If `./OpenMontage/` is missing** (e.g. a fresh / ephemeral container), reinstall it first:
  ```bash
  bash scripts/install-openmontage.sh
  ```
  This fetches the source (tarball, since external `git clone` is blocked in this
  environment), creates an isolated venv at `OpenMontage/.venv`, installs ffmpeg, and runs
  the toolkit's `make setup`.
- **How to drive it:** OpenMontage is agent-first. Before acting on an OpenMontage video
  request, **read `OpenMontage/AGENT_GUIDE.md`** (its `CLAUDE.md` makes this mandatory) — it
  contains the routing rules, pipeline manifests (`OpenMontage/pipeline_defs/`), and stage
  skills (`OpenMontage/skills/`) that determine the workflow.
- **Run Python tools** with the venv interpreter: `OpenMontage/.venv/bin/python`.
- **API keys:** add provider keys to `OpenMontage/.env` (copied from `.env.example`) to
  unlock cloud providers. Piper TTS and the Remotion zero-key demos work without any keys.
- **ffmpeg** is required at render time and is installed by the setup script.

## The Night Shift Star — Channel Voice (MANDATORY)

All videos for the user's YouTube channel **"The Night Shift Star"** must use the
user's cloned Higgsfield voice element:

- **Voice:** "Lunar Eclipse Narrator" — `voice_id: 5da742e5-ac1e-4f1f-8850-93b914c24c5f`,
  `voice_type: "element"` (works with `seed_audio` and `text2speech_v2`)
- Delivery style: suspense/thriller narration — slower pace (`speech_rate` ≈ −5 to −8),
  dramatic pauses via ellipses in the TTS text, 48 kHz output
- Post chain (DRY — no reverb/echo): highpass 80 Hz, −2.0 dB @300 Hz, +2.5 dB @4 kHz,
  gentle compression (`acompressor=threshold=-20dB:ratio=2.8:attack=8:release=200:makeup=3`)
- **Never add `aecho`/reverb to this voice.** A slap-back delay repeats every word ~85 ms
  later and smears consonants, which reads as stuttering and unclear speech. The suspense
  comes from pacing and the ducked music bed, not from room effects.
- Music beds stay ducked under the voice (sidechain compress, bed ≈ 0.30 volume,
  final loudnorm −14 LUFS)

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

## Quality Skills (Hermes — always-on)

- **requesting-code-review**: Security scan + quality gates before every commit.


## Multi-machine Sync Rule (MANDATORY)

This repo is worked on from MULTIPLE machines (PC Claude Code + VPS Hermes).
Before starting ANY task: run `git pull` first (pull the current branch).
Never edit a file without having pulled the latest version first.
If a push is rejected (non-fast-forward): pull, resolve, then push.
Never leave uncommitted changes at end of session — commit + push so the
other machine starts fresh. GitHub is the single source of truth.
