#!/usr/bin/env python3
"""Measure the real silence at each segment seam, from the waveform.

Whisper word boundaries overstate gaps — a conservative word-end plus a soft
onset reads as half a second that isn't there. This measures the actual
contiguous sub-threshold span straddling each seam, which is what the style's
0.10-0.30 s pause rule is really about.

Usage: seams.py VO.wav LEN1,LEN2,... CARD_SECONDS
"""
import subprocess
import sys

import numpy as np

vo, lens_csv, card = sys.argv[1], sys.argv[2], float(sys.argv[3])
lens = [float(v) for v in lens_csv.split(",") if v.strip()]

SR, HOP = 48000, int(0.005 * 48000)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vo, "-ac", "1", "-ar", str(SR),
                      "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
n = len(x) // HOP
e = np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(axis=1) + 1e-12)
quiet = e < e.max() * 0.02

acc, bounds = card, []
for l in lens[:-1]:
    acc += l
    bounds.append(acc)

worst, total = 0.0, 0.0
for b in bounds:
    i = min(int(b / 0.005), len(quiet) - 1)
    a = i
    while a > 0 and quiet[a - 1]:
        a -= 1
    c = i
    while c < len(quiet) - 1 and quiet[c]:
        c += 1
    span = (c - a) * 0.005
    total += span
    worst = max(worst, span)
    flag = "" if span <= 0.30 else "   OVER"
    print(f"  seam @{b:6.2f}s   silence {span:.2f}s{flag}")
print(f"SEAMS n={len(bounds)} worst={worst:.2f}s total={total:.2f}s "
      f"{'ALL_WITHIN_0.30' if worst <= 0.30 else 'SOME_OVER'}")
