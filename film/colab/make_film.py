# -*- coding: utf-8 -*-
# =============================================================================
#  THE MAGIC LAMP OF KINDNESS — அன்பின் அதிசய விளக்கு
#  Google Colab assembler: storyboard images  ->  one ~5-min film w/ Tamil voice
# =============================================================================
#  HOW TO USE (Colab):
#   1. Runtime > Change runtime type > (CPU is fine; GPU not needed).
#   2. Put your storyboard images in a Google Drive folder, one file per shot,
#      named EXACTLY by shot id:  S1.1.png  S1.2.png ... S9.3.png  CR.png
#      (also add GENIE.png = the golden genie portrait, used for blocked shots).
#      Use film/storyboard/MANIFEST.md to know which generated image is which shot.
#   3. Set IMAGES_DIR below to that folder. Run all cells top to bottom.
#   4. The finished film downloads as  magic_lamp_of_kindness.mp4
#
#  Any shot with no image file becomes a captioned placeholder card, so the
#  video is always complete end-to-end. Voice is generated automatically.
# =============================================================================

# =========================== CELL 1 — install ================================
# !pip -q install edge-tts moviepy==1.0.3 imageio-ffmpeg pillow
# !apt-get -qq install -y fonts-noto ffmpeg >/dev/null      # Noto Tamil font + ffmpeg
# (uncomment the two lines above when running in Colab)

import os, asyncio, math, glob, textwrap, subprocess, shutil

# =========================== CELL 2 — config =================================
from google.colab import drive  # comment out if not using Drive
drive.mount('/content/drive')

IMAGES_DIR = "/content/drive/MyDrive/MagicLamp/images"   # <-- your images folder
OUTPUT     = "/content/magic_lamp_of_kindness.mp4"
WORK       = "/content/work"; os.makedirs(WORK, exist_ok=True)

W, H, FPS  = 1920, 1080, 24            # 1080p; images are downscaled to fit
XFADE      = 0.6                       # crossfade seconds between shots
ZOOM       = 0.06                      # Ken Burns zoom amount per shot
MUSIC_PATH = ""                        # optional: path to a background-music mp3 (else leave "")
MUSIC_DB   = -22                       # music loudness under the voice

# A Tamil-capable font (installed by fonts-noto). Fallback search below.
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoSansTamil-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansTamil-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifTamil-Regular.ttf",
]
FONT = next((f for f in FONT_CANDIDATES if os.path.exists(f)), None)

# ---- Genie compositing (gets the Genie into the 9 filter-blocked shots) ------
# The Genie can't be generated inside these scenes (NSFW filter), so we generated
# each SCENE WITHOUT the Genie ("<shot>_bg.png") plus a transparent Genie cut-out
# ("GENIE_cut.png", = remove_background of the golden portrait) and paste him in.
GENIE_CUT = "GENIE_cut.png"
# shot -> (cx, cy, height_frac, flip_horizontal, alpha)
#   cx,cy = Genie CENTER as a fraction of the frame; height_frac = his height / H.
COMPOSITE = {
 "S4.1": (0.50, 0.34, 0.62, False, 1.00),   # rising from the smoke column
 "S4.3": (0.80, 0.52, 0.72, True , 1.00),   # right, facing the family
 "S5.6": (0.19, 0.54, 0.72, False, 1.00),   # left, beside the family
 "S6.5": (0.75, 0.56, 0.70, True , 1.00),   # right, beside Mirthula
 "S7.5": (0.17, 0.54, 0.66, False, 1.00),   # left, hands toward the girl
 "S7.6": (0.85, 0.26, 0.34, True , 1.00),   # small, upper-right of the montage
 "S8.1": (0.18, 0.54, 0.72, False, 1.00),   # left, presenting the carpet
 "S8.5": (0.80, 0.56, 0.42, True , 0.85),   # small, among the family
 "S9.2": (0.72, 0.46, 0.60, False, 0.55),   # fading (low alpha) in the swirl
}

# =========================== CELL 3 — the film ===============================
# Each shot: id, duration(s), genie=True if the (blocked) golden-genie stand-in
# should be used when its own image is missing, and the spoken lines.
# line = (speaker, tamil_text, english_subtitle).  speaker drives the TTS voice.
SHOTS = [
 ("S1.1",6,False,[("narrator","சில நேரங்களில் பணம் நமக்கு எல்லாவற்றையும் தரும் போல தோன்றும்...","Sometimes it feels as if money can give us everything...")]),
 ("S1.2",6,False,[("narrator","ஆனால் அன்பு தான் வாழ்க்கையை முழுமையாக்கும்.","...but it is love that makes life whole.")]),
 ("S1.3",5,False,[]),
 ("S1.4",5,False,[]),
 ("S1.5",5,False,[]),
 ("S1.6",4,False,[("hamruthaa","அப்பா, என்னோட பாரு!","Appa, look at me!")]),
 ("S1.7",4,False,[]),
 ("S2.1",6,False,[("nandini","இன்று ஒரு நாள் வேலை இல்லாமல் குடும்பத்தோட வெளிய போவோமா?","Just for one day, no work — shall we go out together as a family?")]),
 ("S2.2",5,False,[("aravinth","இப்போ வேலை ரொம்ப இருக்கு நந்தினி...","There's so much work right now, Nandini...")]),
 ("S2.3",5,False,[("aravinth","சரி... இன்னைக்கு வேலை வேண்டாம். போகலாம்!","Alright... no work today. Let's go!")]),
 ("S2.4",5,False,[]),
 ("S2.5",4,False,[]),
 ("S3.1",7,False,[("mirthula","வாவ்... இது ஒரு பழைய அரண்மனை!","Whoa... it's an old palace!")]),
 ("S3.2",7,False,[]),
 ("S3.3",7,False,[("hamruthaa","அம்மா... அங்க ஏதோ பிரகாசிக்குது!","Mommy... something is shining over there!")]),
 ("S3.4",5,False,[]),
 ("S3.5",5,False,[("hamruthaa","ஹிஹி! குரங்கு டான்ஸ் ஆடுது!","Hehe! The monkey is dancing!")]),
 ("S3.6",4,False,[]),
 ("S4.1",7,True ,[("genie","நான் ஆயிரம் வருடங்களாக இந்த விளக்கில் இருந்த ஜீனி!","I am the Genie who has lived in this lamp for a thousand years!")]),
 ("S4.2",7,False,[("hamruthaa","நீங்க கார்டூன்ல வர்ற ஜீனி மாதிரி இருக்கீங்க!","You look just like the Genie from the cartoons!")]),
 ("S4.3",7,True ,[("genie","உங்களுக்கு மூணு ஆசைகள் தர்றேன். யோசிச்சு கேளுங்க!","I grant you three wishes. Choose them wisely!")]),
 ("S4.4",4,False,[]),
 ("S5.1",6,False,[("aravinth","எனக்கு நிறைய பணம் வேண்டும்!","I wish for a lot of money!")]),
 ("S5.2",7,False,[]),
 ("S5.3",7,False,[]),
 ("S5.4",8,False,[]),
 ("S5.5",6,False,[("nandini","இவ்வளவு இருந்தும்... ஏன் இவ்வளவு வெறுமை?","With all of this... why does it feel so empty?")]),
 ("S5.6",6,True ,[("genie","பணம் மட்டும் சந்தோஷத்தை தராது.","Money alone cannot bring happiness.")]),
 ("S6.1",6,False,[("mirthula","நான் உலகம் முழுக்க புகழ் பெற வேண்டும்!","I wish to become famous all over the world!")]),
 ("S6.2",8,False,[]),
 ("S6.3",8,False,[]),
 ("S6.4",8,False,[("mirthula","எல்லாரும் இருக்காங்க... ஆனா யாரும் என்கூட இல்ல.","Everyone is here... but no one is with me.")]),
 ("S6.5",10,True,[("genie","புகழ் மட்டும் வாழ்க்கையை நிறைவு செய்யாது.","Fame alone cannot make a life complete.")]),
 ("S7.1",7,False,[("nandini","ஹம்ருதா, நீ என்ன ஆசைப்படுற, செல்லம்?","Hamruthaa, what do you wish for, my dear?")]),
 ("S7.2",6,False,[]),
 ("S7.3",10,False,[("hamruthaa","எங்க குடும்பம் எப்பவும் சந்தோஷமா இருக்கணும்... நாம எல்லாருக்கும் உதவி செய்யணும்.","I wish our family is always happy... and that we help everyone.")]),
 ("S7.4",6,False,[]),
 ("S7.5",6,True ,[]),
 ("S7.6",15,True,[("narrator","ஒரு சின்ன அன்பான ஆசை... உலகத்தையே மாத்திச்சு.","One small loving wish... changed the whole world.")]),
 ("S8.1",6,True ,[("genie","இந்தாங்க, உங்க குடும்பத்துக்கு ஒரு பரிசு!","Here — a gift for your family!")]),
 ("S8.2",7,False,[]),
 ("S8.3",7,False,[]),
 ("S8.4",7,False,[]),
 ("S8.5",8,True ,[("genie","உண்மையான மந்திரம் அன்பு தான்.","The real magic is love.")]),
 ("S9.1",6,False,[]),
 ("S9.2",5,True ,[("narrator","பணம், புகழ், செல்வம் எல்லாம் ஒருநாள் மறைந்து போகும்...","Money, fame, and riches will all fade one day...")]),
 ("S9.3",4,False,[("narrator","ஆனால் அன்பும், குடும்பமும், பிறருக்கு உதவும் மனமும் என்றென்றும் வாழும்.","...but love, family, and a heart that helps others live forever.")]),
 ("CR"  ,6,False,[]),
]

# Speaker -> (edge-tts voice, rate, pitch). Only 2 Tamil voices exist; we vary
# rate/pitch to give each character a distinct feel.
VOICES = {
 "narrator":  ("ta-IN-ValluvarNeural", "-6%",  "-2Hz"),
 "aravinth":  ("ta-IN-ValluvarNeural", "+0%",  "+0Hz"),
 "genie":     ("ta-IN-ValluvarNeural", "-8%",  "-8Hz"),   # deep & grand
 "nandini":   ("ta-IN-PallaviNeural",  "-2%",  "+0Hz"),
 "mirthula":  ("ta-IN-PallaviNeural",  "+6%",  "+8Hz"),
 "hamruthaa": ("ta-IN-PallaviNeural",  "+8%",  "+22Hz"),  # child-like
}

# =========================== CELL 4 — voice (edge-tts) =======================
import edge_tts
from moviepy.editor import (ImageClip, AudioFileClip, CompositeAudioClip,
                            CompositeVideoClip, ColorClip, concatenate_videoclips,
                            concatenate_audioclips, afx)
from moviepy.audio.AudioClip import AudioClip as _AC
from PIL import Image, ImageDraw, ImageFont

async def _tts(text, voice, rate, pitch, out):
    await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(out)

def synth(text, speaker, out):
    v, r, p = VOICES.get(speaker, VOICES["narrator"])
    asyncio.get_event_loop().run_until_complete(_tts(text, v, r, p, out))
    return out

# =========================== CELL 5 — image helpers ==========================
def _composite_genie(bg_rgb, genie_rgba, place):
    """Paste the transparent Genie cut-out onto a background per placement tuple."""
    cx, cy, hf, flip, alpha = place
    if flip:
        genie_rgba = genie_rgba.transpose(Image.FLIP_LEFT_RIGHT)
    gw, gh = genie_rgba.size
    th = max(1, int(H * hf)); g = genie_rgba.resize((max(1, int(gw * th / gh)), th), Image.LANCZOS)
    if alpha < 1.0:
        g.putalpha(g.split()[3].point(lambda v: int(v * alpha)))
    x = int(W * cx - g.size[0] / 2); y = int(H * cy - g.size[1] / 2)
    out = bg_rgb.convert("RGBA"); out.alpha_composite(g, (x, y))
    return out.convert("RGB")

def _find(name_no_ext):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(IMAGES_DIR, name_no_ext + ext)
        if os.path.exists(p):
            return p
    return None

def load_or_placeholder(shot_id, is_genie, caption):
    """Return a PIL RGB image WxH: final file > composited genie-on-bg > stand-in > card."""
    # 1) a finished flat image for this shot, if you have one
    p = _find(shot_id)
    if p:
        return _fit(Image.open(p).convert("RGB"))
    # 2) composite the Genie cut-out onto this shot's genie-free background
    if shot_id in COMPOSITE:
        bg = _find(shot_id + "_bg")
        cut = os.path.join(IMAGES_DIR, GENIE_CUT)
        if bg and os.path.exists(cut):
            return _composite_genie(_fit(Image.open(bg).convert("RGB")),
                                    Image.open(cut).convert("RGBA"), COMPOSITE[shot_id])
        if bg:
            return _fit(Image.open(bg).convert("RGB"))   # background alone if no cut-out yet
    # 3) golden Genie portrait stand-in
    if is_genie:
        g = _find("GENIE")
        if g:
            return _fit(Image.open(g).convert("RGB"))
    # 4) captioned placeholder card
    return _card(shot_id, caption)

def _fit(img):
    """Cover-fit an image to WxH (crop overflow)."""
    iw, ih = img.size
    scale = max(W / iw, H / ih)
    img = img.resize((int(iw * scale) + 1, int(ih * scale) + 1), Image.LANCZOS)
    iw, ih = img.size
    left, top = (iw - W) // 2, (ih - H) // 2
    return img.crop((left, top, left + W, top + H))

def _card(shot_id, caption):
    """A warm gradient placeholder card with the shot's Tamil caption."""
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        img.paste((int(30 + 40*t), int(18 + 22*t), int(50 + 10*t)), (0, y, W, y+1))
    d = ImageDraw.Draw(img)
    if FONT and caption:
        f = ImageFont.truetype(FONT, 54)
        lines = textwrap.wrap(caption, width=28) or [shot_id]
        th = sum(f.getbbox(l)[3] + 16 for l in lines)
        y = (H - th) // 2
        for l in lines:
            w = d.textlength(l, font=f)
            d.text(((W - w)//2, y), l, font=f, fill=(240, 225, 190))
            y += f.getbbox(l)[3] + 16
    return img

def subtitle_png(text, out):
    """Render a Tamil subtitle strip (transparent) sized W x band."""
    band = 220
    img = Image.new("RGBA", (W, band), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if not (FONT and text):
        img.save(out); return out
    f = ImageFont.truetype(FONT, 46)
    lines = textwrap.wrap(text, width=42) or [text]
    y = band - len(lines)*58 - 20
    for l in lines:
        w = d.textlength(l, font=f)
        x = (W - w)//2
        for dx in (-2,-1,0,1,2):        # outline for readability
            for dy in (-2,-1,0,1,2):
                d.text((x+dx, y+dy), l, font=f, fill=(0,0,0,220))
        d.text((x, y), l, font=f, fill=(255, 244, 214, 255))
        y += 58
    img.save(out); return out

# =========================== CELL 6 — build each shot ========================
def build_shot(i, shot):
    sid, dur, is_genie, lines = shot
    caption = lines[0][1] if lines else sid
    # --- image with Ken Burns zoom ---
    frame_path = os.path.join(WORK, f"{sid}.png")
    load_or_placeholder(sid, is_genie, caption).save(frame_path)

    # --- audio for this shot (sequential TTS lines) ---
    clips, subs = [], []
    t = 0.4
    audio_parts = []
    for j, (spk, ta, en) in enumerate(lines):
        wav = os.path.join(WORK, f"{sid}_{j}.mp3")
        synth(ta, spk, wav)
        a = AudioFileClip(wav)
        audio_parts.append(a.set_start(t))
        # subtitle overlay synced to the line
        sp = os.path.join(WORK, f"{sid}_{j}_sub.png")
        subtitle_png(ta, sp)
        subs.append((sp, t, a.duration + 0.3))
        t += a.duration + 0.35

    shot_dur = max(dur, t + 0.3)

    base = (ImageClip(frame_path).set_duration(shot_dur)
            .resize(lambda tt: 1.0 + ZOOM * (tt / shot_dur))
            .set_position("center"))
    bg = ColorClip((W, H), color=(0, 0, 0)).set_duration(shot_dur)
    layers = [bg, base]
    for sp, st, sd in subs:
        layers.append(ImageClip(sp).set_start(st).set_duration(sd)
                      .set_position(("center", H - 240)))
    clip = CompositeVideoClip(layers, size=(W, H)).set_duration(shot_dur)

    if audio_parts:
        clip = clip.set_audio(CompositeAudioClip(audio_parts).set_duration(shot_dur))
    if XFADE > 0:
        clip = clip.crossfadein(XFADE)
    return clip

print("Font:", FONT)
print("Building", len(SHOTS), "shots ...")
shot_clips = [build_shot(i, s) for i, s in enumerate(SHOTS)]

# =========================== CELL 7 — assemble + export ======================
film = concatenate_videoclips(shot_clips, method="compose", padding=-XFADE)

# optional background music, ducked under the voice
if MUSIC_PATH and os.path.exists(MUSIC_PATH):
    music = (AudioFileClip(MUSIC_PATH).fx(afx.audio_loop, duration=film.duration)
             .fx(afx.volumex, 10 ** (MUSIC_DB / 20)))
    voice = film.audio
    film = film.set_audio(CompositeAudioClip([music, voice]) if voice else music)

film.write_videofile(OUTPUT, fps=FPS, codec="libx264", audio_codec="aac",
                     bitrate="6000k", threads=4)
print("Done ->", OUTPUT, f"({film.duration:.1f}s)")

# =========================== CELL 8 — download ===============================
from google.colab import files
files.download(OUTPUT)
