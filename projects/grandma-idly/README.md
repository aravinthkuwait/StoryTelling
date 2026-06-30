# பாட்டியின் இட்லி கடை — Paati's Idli Shop

A ~2-minute cinematic Tamil short about a grandmother who has run a tiny idli
shop for thirty years, and the boy she once fed for free who comes back grown up.

**Built 100% free and offline** — no API keys, no GPU, no cloud calls (this
environment blocks cloud TTS and AI video generation). Toolchain:

| Layer | Tool | Notes |
|---|---|---|
| Narration | `espeak-ng` (`-v ta`) | Offline Tamil TTS — robotic, but real Tamil voice, zero cost |
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

This is a **stylized motion-graphic short**, not photoreal live action, and the
narration is a synthetic (espeak) Tamil voice — those are the honest limits of a
fully-free, offline, network-restricted build. For photoreal cinematic footage
use AI video gen (Veo/Kling/Seedance — paid), and for a natural Tamil voice add a
Google Cloud TTS or ElevenLabs key (free tiers exist) to `OpenMontage/.env`.
