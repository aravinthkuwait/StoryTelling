# Laundrmate Advertisement Project

A ~60-second fast, premium, realistic commercial for **Laundrmate — The Laundry
Company**, told as **one continuous real-life story**: customer booking →
pickup → laundry processing → drying → ironing → packing → delivery.

## Project files

| File | Purpose |
|---|---|
| [`FINAL_DIRECTION.md`](FINAL_DIRECTION.md) | **Locked final direction** — scenes, style rules, realism constraints, offer, contact details. Source of truth. |
| [`production/shot-list.md`](production/shot-list.md) | Numbered clip-by-clip Higgsfield generation plan (14 clips, exact filenames/order), continuity anchors, model policy, prompting rules. |
| [`production/voiceover-scripts.md`](production/voiceover-scripts.md) | Full Tamil / English / Hindi voiceover + subtitle scripts for all scenes. |
| [`production/continuity-checklist.md`](production/continuity-checklist.md) | Continuity + realism + locked-text QA checklist, run on drafts and on the final master. |
| [`notebooks/Laundrmate_FFmpeg_Merge.ipynb`](notebooks/Laundrmate_FFmpeg_Merge.ipynb) | Google Colab FFmpeg notebook (multi-cell version): normalizes the numbered clips, merges without freezes/black gaps/fps changes, muxes the three language VO tracks, runs QC. |
| [`production/colab_build_three_languages.py`](production/colab_build_three_languages.py) | **One-script Colab build.** Paste into a single Colab cell and run: fetches every finished clip by URL, normalizes, concatenates, muxes all three language voiceovers, and QCs the output in one pass. Clip URLs for all QC-approved final renders are already filled in; see the file's header for the 3 things still outstanding (clip 01's fix, the 3 motion-graphics clips, and the voiceover audio) before it produces the true final ad. |
| [`production/generation-log.md`](production/generation-log.md) | Full generation history: every Higgsfield job ID, QC verdict, credit spend, and the root-cause diagnosis for clip 01 and clip 04's outstanding issues. |

## Workflow

1. **Reference stills** — lock characters/locations with Nano Banana Pro.
2. **Drafts** — generate the 11 AI clips with Wan 2.5 Fast (clips 03, 12, 14
   are motion graphics built in post); iterate until the sequence plays as one
   continuous story (run the continuity checklist).
3. **Final renders** — Veo 3 for the 7 hero clips, Veo 3 Fast for the 4
   standard clips, within the **800-credit production cap** (see budget in
   `production/shot-list.md`).
4. **Merge** — run the Colab notebook to produce the silent master and the
   three deliverables:
   `Laundrmate_Advertisement_Tamil.mp4`, `Laundrmate_Advertisement_English.mp4`,
   `Laundrmate_Advertisement_Hindi.mp4`.
5. **Pre-export verification** — full checklist pass; locked facts
   (phone `98847 12121`, offer dates `31-07-2026` to `07-08-2026`, banner text)
   verified frame-by-frame.

## Non-negotiables

- One connected story — no random disconnected clips.
- Opens on the Laundrmate shop banner; 3D logo only ~1 second.
- Laundry process must look technically believable; 3D only for logo, labels,
  app UI, offer card, phone number, final CTA.
- Same family, same delivery executive, same bag, same tagged garments, same
  shop interior throughout. Morning → midday → evening light progression.
