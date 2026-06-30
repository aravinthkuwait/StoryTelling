# பாட்டியின் இட்லி கடை — Paati's Idli Shop

A ~2-minute cinematic Tamil short about a grandmother who has run a tiny idli
shop for thirty years, and the boy she once fed for free who comes back grown up.

**Built 100% free and offline** — no API keys, no GPU, no cloud calls (this
environment blocks cloud TTS and AI video generation). Toolchain:

| Layer | Tool | Notes |
|---|---|---|
| Narration | Google Cloud TTS (`ta-IN-Chirp3-HD`) | Modern neural Tamil voice. Needs `GOOGLE_API_KEY` in `OpenMontage/.env`. Falls back to offline `espeak-ng -v ta` (robotic) when no key is set |
| Visuals | Pillow | Illustrated cinematic scene stills, Tamil + English typography |
| Motion / grade | ffmpeg | Ken Burns zoom/pan, warm color grade, film grain, 2.39 letterbox, intro/end cards |
| Fonts | Noto Sans/Serif Tamil + Noto Serif | Tamil shaping via Pillow + libraqm |

## Rebuild

```bash
# from repo root, using the OpenMontage venv (Pillow already installed there)
OpenMontage/.venv/bin/python projects/grandma-idly/build_video.py
# single scene (quick visual test):
OpenMontage/.venv/bin/python projects/grandma-idly/build_video.py --scene 5
```

System packages required: `espeak-ng`, `ffmpeg`, `fonts-noto-core`
(`apt-get install -y espeak-ng ffmpeg fonts-noto-core`).

Output: `out/paati_idli_shop.mp4` (1280×720, ~123s). Intermediate per-scene
clips and assets are gitignored; only the final mp4 and this script are tracked.

## Quality note

This is a **stylized motion-graphic short**, not photoreal live action. The
narration now uses a **modern Google Chirp3-HD Tamil neural voice** (set
`GOOGLE_API_KEY` in `OpenMontage/.env`); without a key it falls back to the
offline espeak voice (robotic). Swap voices with `TTS_VOICE=ta-IN-Chirp3-HD-Kore`
(38 Tamil voices available) and pace with `TTS_RATE`. For photoreal cinematic
footage use AI video gen (Veo/Kling/Seedance — paid).
