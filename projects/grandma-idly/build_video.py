#!/usr/bin/env python3
"""
Paati's Idli Shop — a fully-offline, zero-cost cinematic short.

Free/offline toolchain only (this environment blocks cloud TTS + AI video gen):
  * Narration : espeak-ng  (Tamil, offline, no API key)
  * Visuals   : Pillow      (illustrated cinematic scene stills)
  * Motion    : ffmpeg      (Ken Burns zoom/pan, film grade, grain, letterbox)

Usage:
  python build_video.py            # render the whole film
  python build_video.py --scene 1  # render only scene 1 (quick visual test)
"""
from __future__ import annotations
import argparse, math, os, subprocess, sys, json, base64, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- Voice config (modern Google Tamil neural TTS, with espeak fallback) ------
TTS_VOICE = os.environ.get("TTS_VOICE", "ta-IN-Chirp3-HD-Achernar")
TTS_RATE  = float(os.environ.get("TTS_RATE", "0.85"))

def _google_key() -> str:
    k = os.environ.get("GOOGLE_API_KEY", "").strip()
    if k:
        return k
    envp = Path(__file__).resolve().parents[2] / "OpenMontage" / ".env"
    if envp.exists():
        for ln in envp.read_text().splitlines():
            if ln.startswith("GOOGLE_API_KEY="):
                return ln.split("=", 1)[1].strip()
    return ""

ROOT = Path(__file__).resolve().parent
ASSETS, AUDIO, OUT = ROOT / "assets", ROOT / "audio", ROOT / "out"
for d in (ASSETS, AUDIO, OUT):
    d.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24
TAMIL_BOLD = "/usr/share/fonts/truetype/noto/NotoSansTamil-Bold.ttf"
TAMIL_REG  = "/usr/share/fonts/truetype/noto/NotoSerifTamil-Regular.ttf"
LATIN      = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"  # elegant Latin serif

def F(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)

# ---------------------------------------------------------------- story --------
# Each scene: tamil narration (espeak), big Tamil title, English subtitle,
# a color palette (top,bottom gradient + accent) and a motif drawer.
SCENES = [
    dict(id=1, title="பாட்டியின் இட்லி கடை", sub="Paati's Idli Shop",
         narr="அதிகாலை நான்கு மணி. ஊரே தூங்கும் நேரம். ஒரு சிறிய விளக்கு மட்டும் எரிகிறது. அது பாட்டியின் இட்லி கடை.",
         pal=(( 18, 24, 48),(  6,  8, 20),(255,196, 90)), motif="dawn"),
    dict(id=2, title="முப்பது வருடம்", sub="Thirty years, the same little shop",
         narr="எழுபது வயது கமலா பாட்டி. முப்பது வருடமாக இதே கடை. மாவை அரைத்து, அடுப்பை மூட்டி, நாளைத் தொடங்குகிறாள்.",
         pal=(( 40, 26, 22),( 14,  9,  8),(255,150, 70)), motif="stove"),
    dict(id=3, title="சுடச்சுட இட்லி", sub="Soft as cotton, steaming hot",
         narr="வெண்ணிற இட்லிகள், பஞ்சு போல மென்மை. சுடச்சுட சாம்பார், மணக்கும் சட்னி. தெருவெல்லாம் வாசம் பரவுகிறது.",
         pal=(( 36, 40, 30),( 12, 16, 10),(255,228,170)), motif="idli"),
    dict(id=4, title="காலை வாடிக்கையாளர்கள்", sub="The morning regulars arrive",
         narr="முதல் வாடிக்கையாளர்கள். வேலைக்குச் செல்லும் தொழிலாளர்கள். பள்ளிச் சிறுவர்கள். அனைவருக்கும் பாட்டியின் சிரிப்பு இலவசம்.",
         pal=(( 24, 34, 46),(  8, 12, 18),(120,200,255)), motif="people"),
    dict(id=5, title="பசி நிற்காது, கண்ணா", sub="“Hunger can't wait, child. Eat.”",
         narr="ஒரு நாள், காசு இல்லாத ஒரு சிறுவன். பாட்டி சிரித்தாள். பசி நிற்காது கண்ணா, சாப்பிடு. இரண்டு இட்லி, அன்போடு.",
         pal=(( 46, 22, 30),( 16,  7, 11),(255,120,140)), motif="give"),
    dict(id=6, title="வருடங்கள் ஓடின", sub="The years rolled on",
         narr="வருடங்கள் ஓடின. அந்தச் சிறுவன் படித்தான், வளர்ந்தான், ஊரை விட்டுச் சென்றான். ஆனால் அந்த ருசியை மறக்கவில்லை.",
         pal=(( 30, 28, 44),( 10,  9, 16),(180,160,255)), motif="time"),
    dict(id=7, title="அவன் திரும்பி வந்தான்", sub="One day, he came back",
         narr="ஒரு நாள் அவன் திரும்பி வந்தான். அதே தெரு, அதே கடை, அதே பாட்டி. பாட்டி, ஞாபகம் இருக்கா? பாட்டி சிரித்தாள்.",
         pal=(( 38, 30, 20),( 14, 10,  6),(255,180, 90)), motif="return"),
    dict(id=8, title="சிறிய கடை, பெரிய இதயம்", sub="A small shop. A big heart.",
         narr="சிறிய கடை. பெரிய இதயம். பாட்டியின் இட்லி வெறும் உணவல்ல. அது அன்பு. அதுதான் இந்த ஊரின் காலை.",
         pal=(( 44, 32, 18),( 16, 11,  6),(255,206,120)), motif="heart"),
]

# ------------------------------------------------------------- drawing ---------
def vgrad(top, bot):
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        # ease for a softer falloff
        t = t * t * (3 - 2 * t)
        r = int(top[0] + (bot[0]-top[0]) * t)
        g = int(top[1] + (bot[1]-top[1]) * t)
        b = int(top[2] + (bot[2]-top[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def glow(draw, cx, cy, rad, color, layers=14, maxa=120):
    for i in range(layers, 0, -1):
        a = int(maxa * (i / layers) ** 2)
        r = int(rad * i / layers)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color + (a,))

def motif(name, base, accent):
    """Draw an abstract, warm motif onto an RGBA overlay."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cx, cy = W // 2, int(H * 0.40)
    if name == "dawn":
        glow(d, W*0.30, H*0.30, 230, accent, maxa=90)
        for i in range(70):
            x = (i * 53) % W; y = (i * 97) % int(H*0.7)
            d.ellipse([x, y, x+2, y+2], fill=(255,255,255,70))
        d.rectangle([W*0.42, H*0.55, W*0.58, H*0.78], outline=accent+(180,), width=3)
        glow(d, W*0.50, H*0.62, 40, accent, maxa=160)  # the shop lamp
    elif name == "stove":
        glow(d, cx, cy+60, 150, (255,120,40), maxa=150)
        for k,off in enumerate((-50,0,50)):
            for j in range(5):
                yy = cy+40 - j*26
                d.line([cx+off-8, yy, cx+off+8, yy-14], fill=(255,170,80,180-j*28), width=4)
        d.arc([cx-110, cy+30, cx+110, cy+150], 200, 340, fill=accent+(200,), width=6)
    elif name == "idli":
        for r,c in ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2)):
            x = W*0.32 + c*150; y = H*0.34 + r*120
            glow(d, x, y, 60, (255,255,255), maxa=40)
            d.ellipse([x-52, y-30, x+52, y+30], fill=(248,246,238,255))
            d.ellipse([x-52, y-30, x+52, y+30], outline=accent+(120,), width=2)
        for j in range(6):
            d.line([W*0.5-4, H*0.20 - j*0, W*0.5+4, H*0.16], fill=(255,255,255,0))
    elif name == "people":
        for i,xx in enumerate((0.28,0.40,0.52,0.64)):
            x = W*xx; col = accent if i % 2 else (255,210,150)
            glow(d, x, H*0.44, 46, col, maxa=70)
            d.ellipse([x-20, H*0.34, x+20, H*0.40+0], fill=col+(230,))
            d.rounded_rectangle([x-26, H*0.42, x+26, H*0.66], radius=18, fill=col+(210,))
    elif name == "give":
        glow(d, W*0.38, H*0.44, 70, accent, maxa=120)
        glow(d, W*0.62, H*0.44, 50, (255,220,180), maxa=120)
        d.ellipse([W*0.34, H*0.40, W*0.42, H*0.48], fill=(248,246,238,255))  # idli passed
        d.line([W*0.40, H*0.46, W*0.60, H*0.46], fill=accent+(160,), width=5)
        for i in range(20):
            d.ellipse([W*0.50+i*0-1, H*0.44, W*0.50+1, H*0.44+1], fill=(255,255,255,120))
    elif name == "time":
        glow(d, cx, cy, 120, accent, maxa=70)
        d.ellipse([cx-90, cy-90, cx+90, cy+90], outline=accent+(200,), width=4)
        d.line([cx, cy, cx, cy-60], fill=(255,255,255,220), width=4)
        d.line([cx, cy, cx+46, cy+10], fill=(255,255,255,160), width=4)
        for a in range(0,360,30):
            x=cx+78*math.cos(math.radians(a)); y=cy+78*math.sin(math.radians(a))
            d.ellipse([x-3,y-3,x+3,y+3], fill=accent+(220,))
    elif name == "return":
        glow(d, W*0.50, H*0.40, 180, accent, maxa=80)
        d.rectangle([W*0.40, H*0.46, W*0.60, H*0.74], outline=accent+(200,), width=4)
        d.polygon([(W*0.38,H*0.46),(W*0.50,H*0.34),(W*0.62,H*0.46)], outline=accent+(200,))
        glow(d, W*0.50, H*0.55, 26, accent, maxa=200)
        for i in range(10):  # footsteps approaching the door
            x = W*0.10 + i*(W*0.40/10); y = H*0.80 - i*(H*0.04)
            d.ellipse([x-6, y-4, x+6, y+4], fill=(255,255,255, 40+i*14))
    elif name == "heart":
        glow(d, cx, cy, 150, accent, maxa=110)
        s=70
        d.pieslice([cx-s, cy-s*0.8, cx, cy+s*0.2], 0, 180, fill=accent+(235,))
        d.pieslice([cx, cy-s*0.8, cx+s, cy+s*0.2], 0, 180, fill=accent+(235,))
        d.polygon([(cx-s, cy-s*0.18),(cx+s, cy-s*0.18),(cx, cy+s*0.95)], fill=accent+(235,))
    return ov

def vignette():
    v = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(v)
    d.ellipse([-W*0.30, -H*0.30, W*1.30, H*1.30], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return dark, v

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def render_still(scene) -> Path:
    top, bot, accent = scene["pal"]
    img = vgrad(top, bot).convert("RGBA")
    img.alpha_composite(motif(scene["motif"], bot, accent))
    # vignette
    dark, mask = vignette()
    img = Image.composite(img.convert("RGB"), dark, mask).convert("RGBA")
    d = ImageDraw.Draw(img)
    # Tamil title (upper-mid)
    tf = F(TAMIL_BOLD, 64)
    for ln_i, ln in enumerate(wrap(d, scene["title"], tf, W*0.82)):
        tw = d.textlength(ln, font=tf)
        y = int(H*0.60) + ln_i*78
        d.text(((W-tw)/2+2, y+2), ln, font=tf, fill=(0,0,0,170))
        d.text(((W-tw)/2,   y),   ln, font=tf, fill=(255,244,228,255))
    # English subtitle (lower)
    sf = F(LATIN, 30)
    sw = d.textlength(scene["sub"], font=sf)
    d.text(((W-sw)/2, int(H*0.85)), scene["sub"], font=sf, fill=(225,210,190,235))
    out = ASSETS / f"scene{scene['id']:02d}.png"
    img.convert("RGB").save(out)
    return out

# ------------------------------------------------------------- audio -----------
def _ffdur(path) -> float:
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1", str(path)], capture_output=True, text=True).stdout.strip())

def _google_tts(text, out_mp3) -> bool:
    key = _google_key()
    if not key:
        return False
    body = {"input": {"text": text},
            "voice": {"languageCode": "ta-IN", "name": TTS_VOICE},
            "audioConfig": {"audioEncoding": "MP3", "speakingRate": TTS_RATE}}
    req = urllib.request.Request(
        "https://texttospeech.googleapis.com/v1/text:synthesize?key=" + key,
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
        Path(out_mp3).write_bytes(base64.b64decode(r["audioContent"]))
        return True
    except Exception as e:
        print(f"   [google-tts failed: {str(e)[:120]}] -> falling back to espeak")
        return False

def synth(scene) -> tuple[Path, float]:
    mp3 = AUDIO / f"scene{scene['id']:02d}.mp3"
    if _google_tts(scene["narr"], mp3):
        return mp3, _ffdur(mp3)
    # fallback: offline espeak (robotic)
    wav = AUDIO / f"scene{scene['id']:02d}.wav"
    subprocess.run(["espeak-ng","-v","ta","-s","132","-p","36","-a","170",
                    "-g","8", scene["narr"], "-w", str(wav)], check=True)
    return wav, _ffdur(wav)

# ------------------------------------------------------------- per scene -------
def render_scene(scene) -> Path:
    still = render_still(scene)
    wav, dur = synth(scene)
    seg = max(dur + 4.0, 12.5)         # ~0.6s lead + breathing tail (longer for modern voice)
    frames = int(seg * FPS)
    # alternate slow zoom-in / zoom-out for variety (Ken Burns)
    zin = scene["id"] % 2 == 0
    if zin:
        zexpr = f"min(zoom+0.0006,1.18)"
    else:
        zexpr = f"if(eq(on,0),1.18,max(zoom-0.0006,1.0))"
    px = "iw/2-(iw/zoom/2)+ (sin(on/{0})*20)".format(frames)
    py = "ih/2-(ih/zoom/2)+ (cos(on/{0})*12)".format(frames)
    vf = (f"scale={W*2}:{H*2},zoompan=z='{zexpr}':x='{px}':y='{py}':"
          f"d={frames}:s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d=0.7,fade=t=out:st={seg-0.7:.2f}:d=0.7,format=yuv420p")
    out = OUT / f"scene{scene['id']:02d}.mp4"
    # audio: 0.6s lead silence + narration + pad to seg
    af = (f"adelay=600|600,apad,atrim=0:{seg:.2f},"
          f"afade=t=in:st=0:d=0.4,afade=t=out:st={seg-0.6:.2f}:d=0.6")
    subprocess.run(["ffmpeg","-y","-loop","1","-i",str(still),"-i",str(wav),
        "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]",
        "-map","[v]","-map","[a]","-t",f"{seg:.2f}",
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-r",str(FPS), str(out)],
        check=True, capture_output=True)
    return out

# ------------------------------------------------------------- cards -----------
def render_card(cid, title, sub, pal, big=True) -> Path:
    top, bot, accent = pal
    img = vgrad(top, bot).convert("RGBA")
    glow_ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_ov)
    glow(gd, W/2, H*0.46, 260, accent, maxa=70)
    img.alpha_composite(glow_ov)
    dark, mask = vignette()
    img = Image.composite(img.convert("RGB"), dark, mask).convert("RGBA")
    d = ImageDraw.Draw(img)
    tf = F(TAMIL_BOLD, 84 if big else 64)
    lines = wrap(d, title, tf, W*0.84)
    y0 = H*0.40 - len(lines)*46
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=tf); y = y0 + i*96
        d.text(((W-tw)/2+2, y+2), ln, font=tf, fill=(0,0,0,170))
        d.text(((W-tw)/2,   y),   ln, font=tf, fill=(255,244,228,255))
    sf = F(LATIN, 32)
    sw = d.textlength(sub, font=sf)
    d.text(((W-sw)/2, H*0.66), sub, font=sf, fill=(225,210,190,235))
    # thin rule under subtitle
    d.line([W*0.42, H*0.74, W*0.58, H*0.74], fill=accent+(200,), width=2)
    out = ASSETS / f"card_{cid}.png"
    img.convert("RGB").save(out)
    return out

def render_card_clip(cid, title, sub, pal, dur, big=True) -> Path:
    still = render_card(cid, title, sub, pal, big)
    frames = int(dur * FPS)
    zexpr = "min(zoom+0.0004,1.10)"
    vf = (f"scale={W*2}:{H*2},zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"d={frames}:s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d=0.8,fade=t=out:st={dur-0.9:.2f}:d=0.9,format=yuv420p")
    out = OUT / f"card_{cid}.mp4"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",str(still),
        "-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=44100",
        "-filter_complex", f"[0:v]{vf}[v]",
        "-map","[v]","-map","1:a","-t",f"{dur:.2f}",
        "-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-r",str(FPS), str(out)],
        check=True, capture_output=True)
    return out

# ------------------------------------------------------------- assemble --------
def assemble(scene_clips) -> Path:
    listf = OUT / "concat.txt"
    listf.write_text("".join(f"file '{p.name}'\n" for p in scene_clips))
    body = OUT / "body.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listf),
        "-c","copy", str(body)], check=True, capture_output=True)
    # final cinematic pass: warm grade + film grain + 2.39 letterbox + end fade
    final = OUT / "paati_idli_shop.mp4"
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                  "-of","default=nk=1:nw=1", str(body)], capture_output=True, text=True).stdout.strip())
    bar = 92  # letterbox bar height -> ~2.39:1 feel
    vf = (f"curves=r='0/0 0.5/0.53 1/1':g='0/0 0.5/0.49 1/0.98':b='0/0.02 0.5/0.46 1/0.93',"
          f"eq=contrast=1.06:saturation=1.08:brightness=0.01,"
          f"noise=alls=9,"  # static grain pattern — filmic texture without wrecking compression
          f"drawbox=x=0:y=0:w=iw:h={bar}:color=black:t=fill,"
          f"drawbox=x=0:y=ih-{bar}:w=iw:h={bar}:color=black:t=fill,"
          f"fade=t=in:st=0:d=1.0,fade=t=out:st={dur-1.2:.2f}:d=1.2")
    # gentle low ambient pad under the narration for warmth
    subprocess.run(["ffmpeg","-y","-i",str(body),
        "-f","lavfi","-i","sine=frequency=110:sample_rate=44100",
        "-f","lavfi","-i","sine=frequency=164.81:sample_rate=44100",
        "-filter_complex",
        f"[0:v]{vf}[v];"
        f"[1:a]volume=0.04[a1];[2:a]volume=0.03[a2];"
        f"[a1][a2]amix=inputs=2[pad];"
        f"[pad]atrim=0:{dur:.2f},afade=t=in:st=0:d=2,afade=t=out:st={dur-2:.2f}:d=2[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:weights='1 0.5'[a]",
        "-map","[v]","-map","[a]","-t",f"{dur:.2f}",
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-movflags","+faststart", str(final)],
        check=True, capture_output=True)
    return final

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", type=int, default=0, help="render only this scene id")
    a = ap.parse_args()
    scenes = [s for s in SCENES if (a.scene == 0 or s["id"] == a.scene)]
    clips = []
    for s in scenes:
        print(f"==> scene {s['id']}: {s['sub']}")
        clips.append(render_scene(s))
    if a.scene:
        print("single scene:", clips[0]); return
    print("==> intro + end cards")
    intro = render_card_clip("intro", "பாட்டியின் இட்லி கடை", "A Short Film",
                             ((14,18,40),(4,5,14),(255,196,90)), dur=5.5, big=True)
    end   = render_card_clip("end", "அன்புடன்", "With love",
                             ((40,28,16),(12,8,4),(255,206,120)), dur=7.0, big=True)
    final = assemble([intro] + clips + [end])
    dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
              "-of","default=nk=1:nw=1", str(final)], capture_output=True, text=True).stdout.strip()
    print(f"\nDONE -> {final}  ({float(dur):.1f}s)")

if __name__ == "__main__":
    main()
