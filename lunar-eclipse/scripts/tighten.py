#!/usr/bin/env python3
"""Cut dead space out of a narration take without changing playback speed.

The Shorts style wants micro-pauses of 0.10-0.30 s and no long gaps between
ordinary sentences. The TTS inserts much longer ones. This finds every internal
silence on Whisper word boundaries and shortens it to a floor, so the delivery
tightens through editing rather than through time-stretching (which the style
rules forbid).

Usage: tighten.py IN OUT [MAX_GAP] [FLOOR] [REVEAL_GAP=t1,t2,...]
  gaps longer than MAX_GAP collapse to FLOOR, except those beginning within
  0.4 s of a REVEAL_GAP time, which collapse to 0.30 s instead (the style's
  upper bound, reserved for reveals).
"""
import subprocess
import sys

from faster_whisper import WhisperModel

src, dst = sys.argv[1], sys.argv[2]
MAX_GAP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.30
FLOOR = float(sys.argv[4]) if len(sys.argv) > 4 else 0.14
reveals = []
if len(sys.argv) > 5 and sys.argv[5].strip():
    reveals = [float(v) for v in sys.argv[5].split(",") if v.strip()]

model = WhisperModel("small", compute_type="int8")
segs, _ = model.transcribe(src, language="en", word_timestamps=True,
                           vad_filter=False, condition_on_previous_text=False)
words = [(float(w.start), float(w.end)) for s in segs for w in (s.words or [])
         if w.word.strip()]
if len(words) < 2:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-ar", "48000",
                    "-ac", "2", dst], check=True)
    print(f"tighten {src}: too few words, copied")
    raise SystemExit

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", src],
                           capture_output=True, text=True, check=True).stdout.strip())

# keep [speech_start .. speech_end], collapsing the long internal gaps
parts, saved = [], 0.0
prev_end = words[0][0]
for k in range(1, len(words)):
    gap = words[k][0] - words[k - 1][1]
    if gap <= MAX_GAP:
        continue
    target = 0.30 if any(abs(words[k - 1][1] - r) < 0.4 for r in reveals) else FLOOR
    parts.append((prev_end, words[k - 1][1], target))
    saved += gap - target
    prev_end = words[k][0]
parts.append((prev_end, min(words[-1][1] + 0.12, dur), 0.0))

files = []
for i, (a, b, pad) in enumerate(parts):
    p = f"/tmp/_tg{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a}", "-to", f"{b}",
                    "-i", src, "-ar", "48000", "-ac", "2", p], check=True)
    files.append(p)
    if pad > 0:
        g = f"/tmp/_tgp{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-t", str(pad),
                        "-i", "anullsrc=r=48000:cl=stereo", "-ar", "48000", "-ac", "2", g],
                       check=True)
        files.append(g)

with open("/tmp/_tglist.txt", "w") as f:
    for p in files:
        f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", "/tmp/_tglist.txt", "-ar", "48000", "-ac", "2", dst], check=True)

out = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", dst], capture_output=True, text=True,
                           check=True).stdout.strip())
print(f"tighten {src} -> {dst}: {len(parts)-1} gaps trimmed, "
      f"{saved:.2f}s removed, {dur:.2f}s -> {out:.2f}s, "
      f"{len(words)/out*60:.0f} wpm")
