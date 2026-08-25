#!/usr/bin/env python3
"""Tamil captions: EXACT authored script words, timed from Whisper speech timing.

For each segment, Whisper supplies the clock (word timestamps on that segment's
clean voice take); the displayed words come only from the authored manifest.
"""
import json
import os
import sys
from faster_whisper import WhisperModel

VOICEDIR = os.environ.get("VOICEDIR", "w6/voices")
MANIFEST = "manifest_ta.json"
TITLE_CARD = 1.4      # start card length
VO_DELAY = 0.25       # adelay applied to each segment's voice
TAIL_PAD = 0.65       # segment length = trimmed VO + this

blocks = json.load(open(MANIFEST, encoding="utf-8"))["blocks"]
model = WhisperModel("small", compute_type="int8")

import subprocess


def dur(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def whisper_words(path):
    segs, _ = model.transcribe(path, language="ta", word_timestamps=True,
                               vad_filter=True)
    ws = []
    for s in segs:
        for w in s.words or []:
            if w.word.strip():
                ws.append((float(w.start), float(w.end)))
    return ws


cues = []
offset = TITLE_CARD

for b in blocks:
    i = b["block"]
    path = f"{VOICEDIR}/trim{i}.wav"
    d = dur(path)
    seg_len = d + TAIL_PAD
    words = b["vo_line"].split()
    M = len(words)

    wts = whisper_words(path)
    if len(wts) >= 2:
        speech_start, speech_end = wts[0][0], wts[-1][1]
        bounds = [w[0] for w in wts] + [wts[-1][1]]
    else:
        speech_start, speech_end = 0.0, d
        bounds = [0.0, d]
    speech_end = max(speech_end, speech_start + 0.8)
    N = len(bounds) - 1

    def at(frac):
        """Time at fractional position through the spoken words."""
        x = frac * N
        k = min(int(x), N - 1)
        f = x - k
        return bounds[k] + (bounds[k + 1] - bounds[k]) * f

    # authored word j spans [at(j/M), at((j+1)/M)] within this take
    wtimes = [(at(j / M), at((j + 1) / M)) for j in range(M)]

    # chunk authored words into short, readable cues
    chunk, chunks = [], []
    for j, w in enumerate(words):
        chunk.append(j)
        text_len = sum(len(words[k]) + 1 for k in chunk)
        span = wtimes[chunk[-1]][1] - wtimes[chunk[0]][0]
        if len(chunk) >= 3 or text_len >= 26 or span >= 2.2:
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)

    base = offset + VO_DELAY
    for c in chunks:
        st = base + wtimes[c[0]][0]
        en = base + wtimes[c[-1]][1]
        en = max(en, st + 0.55)
        en = min(en, offset + seg_len - 0.05)
        if en <= st:
            continue
        cues.append((st, en, " ".join(words[k] for k in c)))

    print(f"seg{i} vo={d:.2f} words={M} whisper_words={len(wts)} cues={len(chunks)}")
    offset += seg_len

# de-overlap
for k in range(1, len(cues)):
    if cues[k][0] < cues[k - 1][1]:
        st, en, t = cues[k - 1]
        cues[k - 1] = (st, min(en, cues[k][0] - 0.02), t)


def fmt(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


out = sys.argv[1] if len(sys.argv) > 1 else "w6/out/caps_exact.srt"
with open(out, "w", encoding="utf-8") as f:
    n = 0
    for st, en, t in cues:
        if en <= st:
            continue
        n += 1
        f.write(f"{n}\n{fmt(st)} --> {fmt(en)}\n{t}\n\n")
print(f"TOTAL_CUES={n} -> {out}")
