#!/usr/bin/env python3
"""Build the sound-effect bed, placed on real narration beats.

Whisper locates the anchor words in the finished voice track, so a riser lands
on the reveal and an impact lands on the number actually being spoken — rather
than on a guessed timestamp. Whooshes go on scene cuts, but only some of them:
the style rule is explicitly "not one on every transition".

Usage: mksfx_bed.py VO.wav DURATION CUTS_CSV OUT.wav REVEALS_OUT.txt
"""
import subprocess
import sys
import wave

import numpy as np
from faster_whisper import WhisperModel

SR = 48000
vo, dur, cuts_csv, out, reveals_out = sys.argv[1:6]
dur = float(dur)
cuts = [float(c) for c in cuts_csv.split(",") if c.strip()]


def load(path):
    with wave.open(path, "rb") as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
        return a.reshape(-1, w.getnchannels())[:, 0].astype(np.float32) / 32768.0


sfx = {n: load(f"sfx/{n}.wav") for n in ("whoosh", "riser", "impact", "hit")}

model = WhisperModel("small", compute_type="int8")
segs, _ = model.transcribe(vo, language="en", word_timestamps=True,
                           vad_filter=False, condition_on_previous_text=False)
words = [(float(w.start), float(w.end), w.word.strip().strip(".,!?'\"").lower())
         for s in segs for w in (s.words or []) if w.word.strip()]


def find(target, nth=1):
    seen = 0
    for a, b, t in words:
        if t == target or t.startswith(target):
            seen += 1
            if seen == nth:
                return a
    return None


bed = np.zeros(int(dur * SR) + SR, dtype=np.float32)
placed, reveals = [], []


def place(name, at, gain=1.0, align="start"):
    if at is None:
        return
    clip = sfx[name] * gain
    i = int((at - (len(clip) / SR if align == "end" else 0.0)) * SR)
    i = max(0, i)
    bed[i:i + len(clip)] += clip[:max(0, len(bed) - i)]
    placed.append(f"{name}@{at:.2f}s")


# major reveal: the scale of Earth's shadow
m = find("million")
if m:
    place("riser", m - 0.05, 0.85, align="end")
    place("impact", m + 0.02, 0.9)
    reveals.append(m)
q = find("quarter")
if q:
    place("impact", q + 0.02, 0.7)

# the one big hit of the video
c = find("coinc")
if c:
    place("hit", c + 0.05, 1.0)
    reveals.append(c)

# the closing question gets a lift, not a bang
qq = find("question")
if qq:
    reveals.append(qq)
    place("whoosh", qq - 0.30, 0.55)

# whooshes on alternate cuts only
for k, cut in enumerate(cuts):
    if k % 2 == 0:
        place("whoosh", cut - 0.14, 0.75)

st = np.stack([bed, bed], axis=1)[:int(dur * SR)]
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())

open(reveals_out, "w").write(",".join(f"{r:.2f}" for r in reveals))
print(f"SFX_BED {len(placed)} cues: {', '.join(placed)}")
print(f"REVEALS {reveals}")
