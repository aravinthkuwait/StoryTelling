#!/usr/bin/env python3
"""Insert hard pauses at chosen word boundaries — the trailer staccato the TTS won't hold.

Usage: staccato.py IN.wav OUT.wav word:occurrence:gap [word:occurrence:gap ...]
Gaps are placed AFTER the named word's end, timed from Whisper word boundaries.
"""
import subprocess
import sys

from faster_whisper import WhisperModel

src, dst, *specs = sys.argv[1:]
targets = []
for s in specs:
    w, occ, gap = s.split(":")
    targets.append((w.lower(), int(occ), float(gap)))

model = WhisperModel("small", compute_type="int8")
segs, _ = model.transcribe(src, language="en", word_timestamps=True,
                           vad_filter=False, condition_on_previous_text=False)
words = [(float(w.start), float(w.end), w.word.strip().strip(".,!?'\"").lower())
         for s in segs for w in (s.words or []) if w.word.strip()]

seen = {}
cuts = []
for a, b, t in words:
    seen[t] = seen.get(t, 0) + 1
    for tw, occ, gap in targets:
        if t == tw and seen[t] == occ:
            cuts.append((b, gap))
cuts.sort()

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", src], capture_output=True, text=True,
                           check=True).stdout.strip())

parts, prev = [], 0.0
for i, (at, gap) in enumerate(cuts):
    p = f"/tmp/_sc{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{prev}", "-to", f"{at}",
                    "-i", src, "-ar", "48000", "-ac", "2", p], check=True)
    parts.append(p)
    g = f"/tmp/_sg{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-t", str(gap),
                    "-i", "anullsrc=r=48000:cl=stereo", "-ar", "48000", "-ac", "2", g],
                   check=True)
    parts.append(g)
    prev = at
tail = "/tmp/_sctail.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{prev}", "-to", f"{dur}",
                "-i", src, "-ar", "48000", "-ac", "2", tail], check=True)
parts.append(tail)

with open("/tmp/_sclist.txt", "w") as f:
    for p in parts:
        f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", "/tmp/_sclist.txt", "-ar", "48000", "-ac", "2", dst], check=True)
print(f"staccato {src} -> {dst}: {len(cuts)} gaps at "
      + ", ".join(f"{a:.2f}s+{g}" for a, g in cuts))
