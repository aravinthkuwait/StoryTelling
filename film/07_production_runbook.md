# 07 — PRODUCTION RUNBOOK ("press play")

Step‑by‑step to turn this package into the finished film once a generation backend is
available. Deterministic — no further creative decisions needed.

## 0. Prerequisites

Pick a generation backend:
- **Higgsfield MCP** (preferred for the photoreal look) — must be connected to the session
  so `generate_image` / `generate_video` tools are callable. (At authoring time these were
  **not** connected; verify with a tool search before starting.)
- **or OpenMontage with provider keys** — `bash scripts/install-openmontage.sh`, then add API
  keys to `OpenMontage/.env`. Read `OpenMontage/AGENT_GUIDE.md` first (mandatory per its CLAUDE.md).
- **or any text→image + image→video stack** (the prompts in `04` are backend‑agnostic).

ffmpeg is required at assembly time (installed by the OpenMontage script, or `apt-get install ffmpeg`).

## 1. Lock character references (do this once, cheapest model)

For each of the 7 characters, generate the **Reference image prompt** from
`01_character_bible.md` on **Nano Banana Pro (~2 cr)**. Save to `film/refs/`:

```
film/refs/aravinth.png  nandini.png  mirthula.png  hamruthaa.png
         genie.png       monkey.png   carpet.png
```

Verify each against its Consistency block (face, hair, costume, body). Re‑roll until
correct. **These are the identity anchors for the whole film — do not skip QC here.**

## 2. Draft pass — keyframes (cheap)

Walk `03_shot_list.md` top to bottom. For each shot, use its **IMG** prompt from `04`:
- prepend `[STYLE]`, paste the Consistency block(s) for every character in the shot, and
  **attach the matching `refs/*.png`** as identity reference(s);
- apply the global negative prompt; keep each character on its seed;
- generate on **Nano Banana Pro**. Save as `film/draft/keyframes/SX.Y.png`.

Run the **Consistency checklist** (`01`) on every keyframe. Re‑roll failures.

## 3. Draft pass — motion (cheap)

Animate each approved keyframe with its **VID** prompt on **Wan 2.5 Fast (~9 cr)**.
Save as `film/draft/clips/SX.Y.mp4` at the listed duration. Review timing and motion.

> **Credit rule:** drafts ONLY on Nano Banana / Wan. **Never** Veo 3 for drafts.

## 4. Finals pass

For approved shots, re‑render video on **Kling 3.0 (~8–10 cr)**. For the HERO shots
listed in `03` (`S4.1, S5.2, S7.5, S7.6, S8.3, S8.5`, plus any you elevate), render the
final on **Veo 3 Fast (~22 cr)** or **Veo 3 (~58 cr)** — **finals only, after the draft is
locked.** Save to `film/final/clips/SX.Y.mp4`. Batch in parallel to use concurrent slots.

### Rough credit budget (order of magnitude)

| Pass | Count | Model | ~Each | ~Subtotal |
|---|---|---|---|---|
| Char refs | 7 | Nano Banana Pro | 2 | ~14 |
| Keyframes | ~47 | Nano Banana Pro | 2 | ~94 |
| Video drafts | ~47 | Wan 2.5 Fast | 9 | ~423 |
| Finals (non‑hero) | ~41 | Kling 3.0 | 9 | ~369 |
| Finals (hero) | ~6 | Veo 3 / Fast | 22–58 | ~130–350 |
| **Total** | | | | **~1,030–1,250 cr** |

Reduce by skipping the Wan draft on simple shots, or finishing more shots on Kling
instead of Veo 3. Increase only if re‑rolls are needed. **Confirm the budget with the
stakeholder before the finals pass** — it is the expensive step.

### Low‑cost budget (preferred — cheapest models only, NO Veo 3)

Use this when the directive is "lowest cost / available credits only." Single video
pass on the cheapest model, no premium finals.

| Pass | Count | Model | ~Each | ~Subtotal |
|---|---|---|---|---|
| Char refs | 7 | Nano Banana Pro | 2 | ~14 |
| Keyframes | ~47 | Nano Banana Pro | 2 | ~94 |
| Video (single pass) | ~47 | Wan 2.5 Fast | 9 | ~423 |
| **Subtotal** | | | | **~531** |
| Re‑roll buffer (~15%) | | | | ~80 |
| **Low‑cost total** | | | | **~610 cr** |

Optional small upgrade: finish only the 6 HERO shots on **Kling 3.0** (~+60 cr) →
**~670 cr**, still no Veo 3.

**Cost controls (apply when conserving credits):**
- Generate one keyframe per shot; avoid speculative re‑rolls — fix the prompt instead.
- One video pass on **Wan 2.5 Fast**; do not run a separate Kling/Veo finals pass.
- **Never** use Veo 3 (~58 cr) or Veo 3 Fast (~22 cr) under the low‑cost directive.
- Batch generations to fill concurrent slots (faster, same credit cost).
- **Check the live balance first** (requires the generation backend connected) and stop
  if a pass would exceed available credits.

## 5. Audio

Produce per `05_audio_and_music.md`:
- **VO** (5 narration lines) and **dialogue** (20 lines) via a Tamil‑capable TTS or a human
  Tamil voice actor (Piper has no reliable Tamil voice — see `05`).
- **Music** (M1–M11) — license/score or generate; one motif, resolved at the finale.
- **SFX** per the cue list. Mix to the targets in `05`/`06`.

## 6. Assemble

Follow `06_assembly_plan.md`: lay clips in EDL order, apply the named transitions, add
titles + the final message card + subtitles (`subtitles.srt`, below), grade warm, add
matching film grain, mix audio, export the master MP4 (3840×2160, 24fps, ‑14 LUFS).

## 7. QC before delivery

- [ ] Runtime ≈ 5:00; scene timings match the spine in `README`.
- [ ] Character consistency holds across every shot (spot‑check faces/costumes).
- [ ] All 5 VO lines + 20 dialogue lines present, in sync, correctly translated in subs.
- [ ] HERO shots look premium; transitions land on the beats in `06`.
- [ ] Final message card + end‑credits photo present.
- [ ] Loudness ‑14 LUFS, peaks ≤ ‑1 dBTP; no clipping.

---

## subtitles.srt (English) — ready to use

A matching `film/subtitles.srt` is included in this folder. It carries the English
subtitle for every VO and dialogue line at the timecodes from `05`. Adjust timings to
the final cut as needed (durations may drift a little after the edit).

---

## Notes & guardrails

- This is a **family‑friendly** film; keep all generations wholesome.
- Do not bake the model identifier or any internal tokens into rendered output, filenames,
  or credits.
- If generating autonomously, **stop and confirm before the Veo 3 finals pass** (the costly
  step) per the repo's credit‑optimization rules.
