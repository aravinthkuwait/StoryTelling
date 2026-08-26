#!/usr/bin/env python3
"""Crisp transparent title-text overlay for the animated cartoon cards."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONT = "/home/user/fonts/Montserrat-ExtraBold.ttf"
LINES = [("AUGUST 28", 118), ("MOON GOES DARK", 104)]

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

blocks = []
for text, size in LINES:
    f = ImageFont.truetype(FONT, size)
    bb = d.textbbox((0, 0), text, font=f, stroke_width=12)
    blocks.append((text, f, bb[2] - bb[0], bb[3] - bb[1]))

gap = 26
total = sum(b[3] for b in blocks) + gap * (len(blocks) - 1)
y = int(H * 0.70) - total // 2

for text, f, tw, th in blocks:
    x = (W - tw) // 2
    d.text((x, y + 8), text, font=f, fill=(0, 0, 0, 150), stroke_width=12,
           stroke_fill=(0, 0, 0, 150))
    d.text((x, y), text, font=f, fill=(255, 255, 255, 255), stroke_width=12,
           stroke_fill=(0, 0, 0, 255))
    y += th + gap

img.save("title_text.png")
print("TITLE_TEXT_OK")
