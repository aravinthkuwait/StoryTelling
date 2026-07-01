# Colab film assembler — `make_film.py`

Turns the storyboard images + Tamil voice into one ~5‑minute film
(`magic_lamp_of_kindness.mp4`), 1080p, with Ken Burns motion, crossfades,
Tamil narration/dialogue (via `edge-tts` neural voices), and burned‑in Tamil
subtitles. No API key needed.

## One-click build (recommended): `make_film_auto.py`
Paste the whole of **`make_film_auto.py`** into a single Google Colab cell and run it —
that's it. Every image URL (all 48 shots + the 12 Genie composites + the cut-out) is baked
in, so it auto-downloads everything, composites the Genie, generates the Tamil voice, and
downloads `magic_lamp_of_kindness.mp4`. No Drive, no uploads. (If a CDN URL ever 403s, that
shot becomes a caption card and the film still finishes; drop a replacement in `/content/dl/`
as `<shot>.png` or `<shot>_bg.png`.)

`make_film.py` (below) is the manual/Drive-folder variant if you'd rather supply files yourself.

## Quick start (manual variant — `make_film.py`)
1. Open [Google Colab](https://colab.research.google.com/), New notebook.
2. Paste `make_film.py` into a cell (or upload it and `%run make_film.py`). The
   first commented block installs deps — uncomment those `!pip` / `!apt` lines.
3. Create a Google Drive folder, e.g. `MyDrive/MagicLamp/images/`, and drop your
   storyboard images in it, **named by shot id**: `S1.1.png`, `S1.2.png`, … ,
   `S9.3.png`, `CR.png`, plus `GENIE.png` (the golden genie portrait).
4. Set `IMAGES_DIR` to that folder, then Run all. The MP4 auto‑downloads.

Any shot whose file is missing becomes a captioned placeholder card, so the
video is always end‑to‑end.

### Getting the Genie into all 9 blocked shots (compositing)
The Genie can't be generated *inside* 9 scenes (Higgsfield NSFW filter), so instead
we ship each of those scenes **without** the Genie plus a **transparent cut‑out** of
him, and the script pastes him in. To use it, add these files to `images/`:
- `GENIE_cut.png` — the transparent golden‑Genie cut‑out (job `6404dd29`).
- `S4.1_bg.png, S4.3_bg.png, S5.6_bg.png, S6.5_bg.png, S7.5_bg.png, S7.6_bg.png,
  S8.1_bg.png, S8.5_bg.png, S9.2_bg.png` — the Genie‑free backgrounds
  (job IDs in [`../storyboard/MANIFEST.md`](../storyboard/MANIFEST.md) → "Genie SOLVED").

The script's `COMPOSITE` dict controls where the Genie sits in each shot
(`center‑x, center‑y, height, flip, alpha`) — tweak to taste. Priority per shot:
your own `<shot>.png` → composited `<shot>_bg.png` + `GENIE_cut.png` → `GENIE.png`
stand‑in → caption card. So once you drop in the 10 files above, **all 48 shots show
the Genie**.

## Getting the images out of Higgsfield
In your Higgsfield client, open each generation and download the PNG, then
rename it to its shot id. Which job = which shot is in
[`../storyboard/MANIFEST.md`](../storyboard/MANIFEST.md) and
[`../refs/MANIFEST.md`](../refs/MANIFEST.md). Canonical golden genie portrait =
`23c9bd18-…` → save as `GENIE.png`.

## Voices
`edge-tts` has two Tamil voices (Pallavi F, Valluvar M); the script varies
rate/pitch per character (deep grand Genie, child‑like Hamruthaa, warm
narrator, etc.). Edit the `VOICES` map to taste. For higher‑quality Tamil VO,
swap in ElevenLabs/Azure `ta-IN` and drop the resulting mp3s in place of the
`synth()` output.

## Options (top of the script)
- `W,H,FPS` — resolution / frame rate (default 1920×1080 @ 24).
- `XFADE` — crossfade seconds between shots; `ZOOM` — Ken Burns strength.
- `MUSIC_PATH` — optional background‑music mp3 (ducked under the voice by `MUSIC_DB`).
- Timings/lines live in the `SHOTS` list — matches `../03_shot_list.md` and
  `../05_audio_and_music.md`.

## Notes
- Runs on a free CPU runtime (no GPU needed); render ~a few minutes.
- Music is intentionally **not** bundled — add your own licensed track via `MUSIC_PATH`.
