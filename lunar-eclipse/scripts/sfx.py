#!/usr/bin/env python3
"""Synthesise the Shorts sound-effect set. Original audio — nothing licensed in.

Writes whoosh / riser / impact / hit as 48 kHz stereo wavs into sfx/.
Kept deliberately subtle: these sit under the narration, never over it.
"""
import os
import subprocess
import wave

import numpy as np

SR = 48000
os.makedirs("sfx", exist_ok=True)


def write(name, mono, peak=0.5):
    x = mono / (np.abs(mono).max() + 1e-9) * peak
    st = np.stack([x, x], axis=1)
    pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(f"sfx/{name}.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"  sfx/{name}.wav  {len(mono)/SR:.2f}s")


def noise(n):
    return np.random.default_rng(7).standard_normal(n).astype(np.float32)


def onepole_bp(x, f_lo, f_hi):
    """Cheap band-pass: high-pass then low-pass, both one-pole, per-sample cutoffs."""
    y = np.empty_like(x)
    lp = np.empty_like(x)
    prev_hp = prev_lp = 0.0
    for i in range(len(x)):
        a_hi = np.exp(-2 * np.pi * f_hi[i] / SR)
        prev_lp = (1 - a_hi) * x[i] + a_hi * prev_lp
        lp[i] = prev_lp
        a_lo = np.exp(-2 * np.pi * f_lo[i] / SR)
        prev_hp = (1 - a_lo) * lp[i] + a_lo * prev_hp
        y[i] = lp[i] - prev_hp
    return y


# --- whoosh: noise swept up then down through a band, for a shot transition
n = int(0.50 * SR)
t = np.linspace(0, 1, n)
centre = 600 + 4200 * np.sin(np.pi * t) ** 1.5
w = onepole_bp(noise(n), centre * 0.55, centre * 1.9)
write("whoosh", w * np.sin(np.pi * t) ** 1.4, 0.34)

# --- riser: rising band of noise plus a climbing tone, ends on the reveal
n = int(1.30 * SR)
t = np.linspace(0, 1, n)
centre = 400 * (14 ** t)
r = onepole_bp(noise(n), centre * 0.7, centre * 1.6) * 0.8
tone = np.sin(2 * np.pi * np.cumsum(180 * (3.2 ** t)) / SR) * 0.25 * t
write("riser", (r + tone) * (t ** 1.7), 0.32)

# --- impact: soft low thump for an important fact
n = int(0.45 * SR)
t = np.linspace(0, 1, n)
env = np.exp(-7 * t)
body = np.sin(2 * np.pi * np.cumsum(np.linspace(150, 62, n)) / SR) * env
click = onepole_bp(noise(n), np.full(n, 1400.0), np.full(n, 5200.0)) * np.exp(-45 * t) * 0.30
write("impact", body + click, 0.42)

# --- hit: deeper, longer sub for the one major moment
n = int(1.10 * SR)
t = np.linspace(0, 1, n)
env = np.exp(-3.4 * t)
sub = np.sin(2 * np.pi * np.cumsum(np.linspace(120, 41, n)) / SR) * env
air = onepole_bp(noise(n), np.full(n, 220.0), np.full(n, 900.0)) * np.exp(-5.5 * t) * 0.25
write("hit", sub + air, 0.50)

print("SFX_OK")
