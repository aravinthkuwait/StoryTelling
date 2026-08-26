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
- **Delivery defaults to the Aravinth High-Retention Shorts style below** for every Short,
  unless a specific different delivery is requested. The channel's ten alternate reads
  (see `lunar-eclipse/video.md`) remain available when asked for by name. 48 kHz output.
- **Verify every generated take before using it.** Transcribe with Whisper, `vad_filter=False`
  (VAD ON can silently swallow a stutter). Reject any take with an adjacent duplicate word,
  a dropped word, or an inserted one. Known failure modes:
  - seed_audio auto-completes clichés — it rewrote "the final one before autumn" back into
    "the last full moon of summer" twice. `text2speech_v2` / minimax does not.
  - seed_audio stutters on single-word sentences ("The Moon. Turns. To shadow." → "turns, turns").
  - **A sentence ending in "Sun." is read as "Sunday"** — the TTS treats it as the weekday
    abbreviation. Never leave `Sun.` sentence-final; restructure the line.
- Hard pauses cannot be requested from the TTS — neither engine honours ellipses or full stops
  as real gaps. Splice them in post with `staccato.py`, which cuts on Whisper word boundaries.
- Post chain (DRY — no reverb/echo): highpass 80 Hz, −2.0 dB @300 Hz, +2.5 dB @4 kHz,
  gentle compression (`acompressor=threshold=-20dB:ratio=2.8:attack=8:release=200:makeup=3`)
- **Never add `aecho`/reverb to this voice.** A slap-back delay repeats every word ~85 ms
  later and smears consonants, which reads as stuttering and unclear speech. The suspense
  comes from pacing and the ducked music bed, not from room effects.
- Music beds stay ducked under the voice (sidechain compress, bed ≈ 0.30 volume,
  final loudnorm −14 LUFS)

## Aravinth High-Retention Shorts Voice Style (DEFAULT for every Short)

Apply automatically to every YouTube Short unless a different delivery is explicitly
requested. This governs **script and voice together** — never write prose and then speed
up the TTS.

**Identity.** Narration uses Aravinth's own cloned voice element (above). Keep his natural
accent, timbre, pronunciation character and male vocal identity. Never imitate, clone or
reproduce anyone else's vocal identity — only general delivery principles are borrowed.
The result should sound like Aravinth after becoming very good at Shorts storytelling.

**Delivery.** Fast, energetic, confident, conversational, curiosity-driven — a knowledgeable
friend urgently telling you something fascinating. Never a newsreader, corporate presenter,
audiobook, ad announcer, or someone plainly reading text.

**Pacing — 175–200 wpm, dynamic.** Never a constant speed. Normal info fast; exciting info
slightly faster; an important revelation slows slightly; a micro-pause before a major fact
and a very short one after, then regain momentum immediately. Minimal dead space.

**Pauses.** Mostly micro-pauses of **0.10–0.30 s**. No long gaps between ordinary sentences;
longer pauses only around a major reveal. `"Scientists just discovered something… [micro]
that shouldn't be possible."` — not a full stop and silence.

**Sentence rhythm.** Short. Short. Then one slightly longer explanation. Then another punch.
No long paragraphs.

**Emphasis.** 1–3 important words per sentence, never every word. Emphasis comes from slight
intensity, pitch movement, clearer articulation and a tiny pacing change. Never shouting.

**Pitch and energy.** No flat pitch. Immediate energy at the open; curious rising tone on
interesting information; higher on a surprise; slightly lower when serious; slow plus stronger
emphasis on the major reveal; confident downward finish.

**First 2 seconds are critical.** Never "Hello everyone", "Welcome back", "Today we're going
to", "In this video". Open on the strongest hook, and make it an information gap the viewer
needs closed.

**Curiosity loop.** hook → question → partial answer → new question → reveal → meaning.
Never reveal everything at once.

**Dialogue.** Speak to one viewer, not an audience. Use connective phrases sparingly and
never repetitively: "But here's the strange part…", "Now look closely.", "But wait.",
"Here's why that matters."

**Emotional movement.** Curiosity → excitement → surprise → explanation → wonder. Never hold
maximum excitement throughout; contrast is what makes the peaks land.

**Human feel.** Do not make it unnaturally perfect. Keep subtle breathing, natural consonants,
small pitch variation and human timing. No synthetic breathing or exaggerated acting.

**Punctuation controls performance.** Comma = tiny continuation. Period = short reset.
Ellipsis = suspense, only when genuinely needed. Dash = sudden emphasis. Question mark =
curiosity lift. Line break = new spoken beat.

**Visual sync.** Narration beats and picture must not run independently. "Look at this" shows
the thing immediately; a stated number appears on screen; "here's the strange part" changes
shot, zoom or camera move. Cuts, zooms, text animations, image changes and SFX land on
narration beats.

**Music.** Subtle cinematic bed, always below the narration. Slight dip/tension before a
reveal, slight rise during it, controlled impact after. Licensed or generated assets only.

**Sound effects.** Sparingly, only where they serve the story: whoosh on transitions, soft
impact on an important fact, riser before a revelation, low hit on a major moment, ambience
where it fits. Never one on every transition.

**Originality / monetization.** Every video is an original Aravinth production. Never copy
another creator's script, voice, audio, dialogue sequence, catchphrases, or shot-for-shot
edit — take general delivery principles only, and add original research, explanation,
storytelling and editing. Continue ticking YouTube's "Altered or synthetic content"
disclosure at upload.

**Final audio polish.** Trim excessive dead space, keep natural breathing, gentle compression,
consistent loudness, tame harsh peaks, music under narration, no clipping.
**Never simply accelerate finished audio to create speed** — speed comes from performance and
script rhythm.

**Target feeling:** "I need to keep listening — the next sentence might reveal something."
Fast but understandable. Energetic but not shouting. Cinematic but conversational. Polished
but human. High-retention but not clickbait. And it must still sound like Aravinth.

### What this style requires of the build pipeline

The lunar-eclipse pipeline was built for the slow suspense read and currently contradicts
this style in three measurable ways. Fix these when building to it:

- **Rate.** v9 measured ~100 wpm (122 words over 73.8 s of speech). The target is 175–200 wpm,
  i.e. roughly 1.8–2× faster. `speech_rate` must go to ≈ 0 … +2, and it must be *measured*
  after generation, not assumed — wpm depends on script density as much as on the rate knob.
- **Script length.** At 175–200 wpm a 60–75 s Short needs ≈ 200–240 spoken words, not ~120.
  Write more content rather than stretching footage; never pad with silence.
- **Dead space.** `build_v*.sh` adds a 0.25 s lead delay and a 0.65 s tail pad to every
  segment (≈ 7 s of silence across 8 blocks). Cut both hard for this style. `staccato.py`
  gaps must come down to 0.10–0.30 s and appear only at reveals, not on every punch word.

Footage timing already supports it: the stretch floor of 0.70 in `build_v9.sh` lets a shot
play up to 1.43× faster so it keeps pace with a quick line instead of drifting in slow motion.

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
