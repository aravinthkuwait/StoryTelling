# THE MAGIC LAMP OF KINDNESS — அன்பின் அதிசய விளக்கு

**Production package for a ~5‑minute cinematic Tamil family‑fantasy film.**
Inspired by *Aladdin*, Disney·Pixar, and South‑Indian cinema.

This folder is a **complete, generation‑ready production bible**. It contains
everything an AI‑video pipeline (Higgsfield → Nano Banana / Wan / Kling / Veo 3,
or any equivalent text‑to‑image / image‑to‑video stack) needs to produce the
film **shot by shot with strict character consistency**, plus the narration,
dialogue, music, edit and assembly plan.

> **Why a package and not a finished video?**
> Photoreal Pixar‑style generation requires the Higgsfield (or equivalent) image/video
> tools to be connected to the session. At authoring time those tools were **not
> connected** in this environment. This package is built so the film can be generated
> the moment a generation backend is available — by an agent or by a human — without
> any further creative decisions.

---

## 1. File map

| File | What it is |
|---|---|
| `README.md` | This overview + how to run the pipeline. |
| `01_character_bible.md` | **STRICT** reusable prompt blocks for all 7 characters + key props. The single source of truth for consistency. Paste these verbatim into every prompt. |
| `02_screenplay.md` | Full shot‑by‑shot screenplay. Tamil dialogue + transliteration + English, narration, and per‑scene timing. The story spine. |
| `03_shot_list.md` | Every shot as a row: ID, duration, camera, action, characters, audio. The production checklist. |
| `04_generation_prompts.md` | Copy‑paste **image** and **video** prompts for every shot, with the recommended model per the credit hierarchy. |
| `05_audio_and_music.md` | Narration script with timecodes, full dialogue list, music cues, SFX, and TTS/voice guidance. |
| `06_assembly_plan.md` | Edit Decision List (EDL): clip order, durations, transitions, on‑screen text, end credits, and the OpenMontage/ffmpeg assembly recipe. |
| `07_production_runbook.md` | Step‑by‑step "press play" instructions to actually generate + assemble once a backend is connected, including batching and QC. |

Read them in order the first time. During production, work from `03_shot_list.md`
and `04_generation_prompts.md`, with `01_character_bible.md` open beside you.

---

## 2. The film at a glance

- **Runtime:** ~5:00 (300 s), 9 scenes, ~46 shots.
- **Language:** Tamil (modern, natural), with English subtitles available.
- **Aspect / format:** 16:9, 4K UHD (3840×2160), HDR, 24 fps. Cinematic.
- **Look:** Disney·Pixar realism — soft volumetric light, rich skin/eye detail,
  expressive faces, warm South‑Indian palette (saffron, gold, teal, rose).
- **Theme:** Money and fame fade; love, family, and kindness endure.
- **Logline:** A work‑obsessed father and his family find an ancient lamp; its
  Genie grants three wishes — wealth and fame leave them empty, until the
  youngest child wishes only for her family's happiness and to help others.

### Scene timing spine

| # | Scene | In–Out | Dur |
|---|---|---|---|
| 1 | Opening — village & family | 0:00–0:35 | 35 s |
| 2 | Family outing | 0:35–1:00 | 25 s |
| 3 | The abandoned palace | 1:00–1:35 | 35 s |
| 4 | The Genie arrives | 1:35–2:00 | 25 s |
| 5 | First wish — wealth | 2:00–2:40 | 40 s |
| 6 | Second wish — fame | 2:40–3:20 | 40 s |
| 7 | Third wish — kindness | 3:20–4:10 | 50 s |
| 8 | Flying‑carpet adventure | 4:10–4:45 | 35 s |
| 9 | Ending — sunset & message | 4:45–5:00 | 15 s |

---

## 3. Production pipeline (the intended flow)

```
character bible ──▶ [1] character reference sheets   (text→image, cheapest model)
                         │  (lock face, hair, costume, body — one canonical image each)
                         ▼
shot list ──────────▶ [2] per‑shot keyframe images    (text→image, reference‑guided)
                         │  (compose each shot; reuse the locked character refs)
                         ▼
                    [3] image→video clips             (animate each keyframe, 5–8 s)
                         │  (drafts on cheap models, finals on premium)
                         ▼
audio plan ─────────▶ [4] narration + dialogue (TTS / VO) + music + SFX
                         ▼
assembly plan ──────▶ [5] edit, transitions, text overlays, color, mix → 5‑min master
```

**Character consistency strategy (critical):** generate **one canonical reference
image per character first** (Step 1), then feed that reference into every
subsequent shot as an image/identity reference. Keep the same seed family per
character where the tool allows. Never re‑describe a character from scratch —
always paste the exact block from `01_character_bible.md`.

---

## 4. Credit hierarchy (from repo `CLAUDE.md`)

When a Higgsfield‑style backend is used, conserve credits:

| Priority | Model | ~Credits | Use for |
|---|---|---|---|
| 1 | Nano Banana Pro | ~2 | Image drafts, character refs, concept tests |
| 2 | Wan 2.5 Fast | ~9 | Video drafts, iteration |
| 3 | Kling 3.0 | ~8–10 | Final video when Veo 3 is overkill |
| 4 | Google Veo 3 Fast | ~22 | Mid‑quality finals |
| 5 | Google Veo 3 | ~58 | **Final render of hero shots only** |
| 6 | Seedance 2.0 | premium | Rare / specific 3D‑CGI needs |

**Rules:** drafts & iteration → Nano Banana Pro / Wan 2.5 Fast. **Never** use Veo 3
for tests/drafts. Veo 3 is permitted for **final hero shots only**. Batch parallel
generations to use concurrent slots. `04_generation_prompts.md` already tags each
shot with its recommended model.

---

## 5. How to actually produce it

See `07_production_runbook.md` for the full step‑by‑step. Short version:

1. Connect a generation backend (Higgsfield MCP, or run OpenMontage with provider keys).
2. Generate the 7 character reference images from `01_character_bible.md`.
3. Walk `03_shot_list.md` top to bottom; for each shot use the prompt from
   `04_generation_prompts.md` (image → then animate to video).
4. Produce narration/dialogue/music per `05_audio_and_music.md`.
5. Assemble per `06_assembly_plan.md`.

Everything downstream is deterministic from these documents.
