#!/usr/bin/env python3
"""Convert whisper-timed SRT to animated ASS captions (fast pop/fly-in, bold, amber accent).
Font family via CAPFONT env (default Montserrat ExtraBold)."""
import os, re, sys

srt_path, ass_path = sys.argv[1], sys.argv[2]
FONT = os.environ.get("CAPFONT", "Montserrat ExtraBold")

def t2ass(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    cs = int(ms) // 10
    return f"{int(h)}:{int(m):02d}:{int(s):02d}.{cs:02d}"

cues = []
for b in re.split(r"\n\s*\n", open(srt_path, encoding="utf-8").read().strip()):
    lines = [l for l in b.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        continue
    m = re.match(r"(\d\d:\d\d:\d\d,\d{3})\s*-->\s*(\d\d:\d\d:\d\d,\d{3})", lines[1])
    if not m:
        continue
    text = " ".join(lines[2:]).strip()
    if text:
        cues.append((t2ass(m.group(1)), t2ass(m.group(2)), text))

AMBER = r"\c&H45C8FF&"
WHITE = r"\c&HFFFFFF&"

header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,7,3,2,90,90,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

out = [header]
for i, (st, en, text) in enumerate(cues):
    words = text.upper().split()
    li = max(range(len(words)), key=lambda k: len(words[k]))
    words[li] = "{%s}%s{%s}" % (AMBER, words[li], WHITE)
    body = " ".join(words)
    dy = 70 if i % 2 == 0 else -70
    fx = (r"{\an2\move(540,%d,540,1620,0,120)\fscx55\fscy55\alpha&H60&"
          r"\t(0,120,\fscx112\fscy112\alpha&H00&)"
          r"\t(120,220,\fscx100\fscy100)\blur0.6}") % (1620 + dy)
    out.append(f"Dialogue: 0,{st},{en},Cap,,0,0,0,,{fx}{body}\n")

open(ass_path, "w", encoding="utf-8").write("".join(out))
print(f"cues={len(cues)} font={FONT}")
