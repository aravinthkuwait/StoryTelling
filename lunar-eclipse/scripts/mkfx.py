#!/usr/bin/env python3
"""Generate seamless star and cloud overlay tiles for drifting sky effects."""
import random
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
random.seed(20260828)

# ---------- starfield (tileable horizontally) ----------
stars = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(stars)
for _ in range(520):
    x, y = random.randrange(W), random.randrange(H)
    r = random.choice([1, 1, 1, 2, 2, 3])
    v = random.randint(120, 255)
    d.ellipse([x - r, y - r, x + r, y + r], fill=v)
glow = stars.filter(ImageFilter.GaussianBlur(3))
stars = Image.blend(stars, glow, 0.55)

# a few bigger sparkles with cross flares
d = ImageDraw.Draw(stars)
for _ in range(26):
    x, y = random.randrange(W), random.randrange(H)
    L = random.randint(6, 14)
    d.line([x - L, y, x + L, y], fill=200, width=1)
    d.line([x, y - L, x, y + L], fill=200, width=1)
stars = stars.filter(ImageFilter.GaussianBlur(0.7))

tile = Image.new("L", (W * 2, H))
tile.paste(stars, (0, 0))
tile.paste(stars, (W, 0))
tile.convert("RGB").save("stars.png")

# ---------- soft cloud haze (tileable horizontally) ----------
small = Image.new("L", (W // 12, H // 12))
px = small.load()
for y in range(small.height):
    for x in range(small.width):
        px[x, y] = random.randint(0, 255)
cloud = small.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(28))

small2 = Image.new("L", (W // 5, H // 5))
px2 = small2.load()
for y in range(small2.height):
    for x in range(small2.width):
        px2[x, y] = random.randint(0, 255)
detail = small2.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(12))
cloud = Image.blend(cloud, detail, 0.35)

# raise contrast so only wisps show, then fade the top so the moon stays clean
lut = [0 if v < 118 else min(255, int((v - 118) * 2.6)) for v in range(256)]
cloud = cloud.point(lut).filter(ImageFilter.GaussianBlur(10))
grad = Image.new("L", (W, H))
gd = ImageDraw.Draw(grad)
for y in range(H):
    gd.line([(0, y), (W, y)], fill=int(255 * min(1.0, max(0.0, (y / H - 0.18) / 0.55))))
cloud = Image.composite(cloud, Image.new("L", (W, H), 0), grad)

# seamless horizontal wrap: cross-fade the seam
wrap = cloud.copy()
band = 160
for i in range(band):
    a = i / band
    col_l = cloud.crop((i, 0, i + 1, H))
    col_r = cloud.crop((W - band + i, 0, W - band + i + 1, H))
    wrap.paste(Image.blend(col_r, col_l, a), (W - band + i, 0))
ctile = Image.new("L", (W * 2, H))
ctile.paste(wrap, (0, 0))
ctile.paste(wrap, (W, 0))
ctile.convert("RGB").save("clouds.png")
print("FX_TILES_OK stars.png clouds.png")
