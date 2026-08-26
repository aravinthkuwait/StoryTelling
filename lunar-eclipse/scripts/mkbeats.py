#!/usr/bin/env python3
"""Detect music beats and emit ffmpeg expressions for zoom pulses + flare hits."""
import subprocess
import sys

import numpy as np

music, dur, offset, cuts_csv, out = sys.argv[1:6]
dur = float(dur)
offset = float(offset)          # music starts this far before the scenes timeline
cuts = [float(c) for c in cuts_csv.split(",") if c.strip()]

SR = 22050
raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", music, "-ac", "1", "-ar", str(SR),
     "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)

# spectral flux onset detection
N, H = 2048, 512
frames = 1 + (len(x) - N) // H
win = np.hanning(N).astype(np.float32)
mag = np.abs(np.fft.rfft(np.stack([x[i * H:i * H + N] * win for i in range(frames)]), axis=1))
flux = np.maximum(0.0, np.diff(mag, axis=0)).sum(axis=1)
flux = flux / (flux.max() + 1e-9)

# adaptive threshold, then peak pick with a minimum spacing
k = 21
pad = np.pad(flux, (k // 2, k // 2), mode="edge")
local = np.array([pad[i:i + k].mean() for i in range(len(flux))])
cand = [(i, flux[i]) for i in range(1, len(flux) - 1)
        if flux[i] > local[i] * 1.35 and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1]]
cand.sort(key=lambda p: -p[1])

MIN_GAP = 0.55
picked = []
for i, v in cand:
    t = i * H / SR - offset
    if t < 0.4 or t > dur - 0.3:
        continue
    if all(abs(t - p) >= MIN_GAP for p in picked):
        picked.append(t)
    if len(picked) >= 55:
        break
picked.sort()

if len(picked) < 8:                      # fallback: steady pulse
    picked = [t for t in np.arange(1.0, dur - 0.3, 1.6)]

zoom_terms = "+".join(f"exp(-pow(on/30-{b:.2f},2)/0.005)" for b in picked)
zoom = f"min(1.055,1+0.05*({zoom_terms}))"

flare_terms = "+".join(f"exp(-pow(t-{c:.2f},2)/0.0008)" for c in cuts) or "0"
bright = f"0.20*({flare_terms})"
sat = f"1+0.16*({flare_terms})"

with open(out, "w") as f:
    f.write(zoom + "\n" + bright + "\n" + sat + "\n")
print(f"BEATS={len(picked)} CUTS={len(cuts)} -> {out}")
