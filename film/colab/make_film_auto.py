# -*- coding: utf-8 -*-
# =============================================================================
#  THE MAGIC LAMP OF KINDNESS — அன்பின் அதிசய விளக்கு
#  ONE-CLICK Google Colab build: auto-downloads every image, composites the
#  Genie, generates Tamil voice, and exports one ~5-min film for download.
#
#  HOW TO USE: paste this whole file into a single Google Colab cell and run it.
#  (No Drive, no manual uploads.) Output: magic_lamp_of_kindness.mp4 downloads.
#
#  If a couple of image URLs ever 403 (private CDN), those shots become captioned
#  cards and the film still completes; re-download those from your Higgsfield
#  library and drop them in /content/dl/ as <shot>.png (or <shot>_bg.png).
# =============================================================================

import os, sys, subprocess, asyncio, threading, textwrap, urllib.request, ssl

# ------------------------------------------------------------------ installs --
subprocess.run("pip -q install edge-tts moviepy==1.0.3 imageio-ffmpeg pillow",
               shell=True, check=False)
subprocess.run("apt-get -qq install -y fonts-noto ffmpeg >/dev/null 2>&1",
               shell=True, check=False)

import edge_tts
from moviepy.editor import (ImageClip, AudioFileClip, CompositeAudioClip,
    CompositeVideoClip, ColorClip, concatenate_videoclips, afx)
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------- config ---
W, H, FPS, XFADE, ZOOM = 1920, 1080, 24, 0.6, 0.06
OUTPUT = "/content/magic_lamp_of_kindness.mp4"
DL = "/content/dl"; os.makedirs(DL, exist_ok=True)
MUSIC_PATH, MUSIC_DB = "", -22     # optional: local bg-music mp3
FONT = next((f for f in [
    "/usr/share/fonts/truetype/noto/NotoSansTamil-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansTamil-Regular.ttf"] if os.path.exists(f)), None)

CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/"

# Direct shot images (36) --------------------------------------------------- #
IMG = {
 "S1.1":"hf_20260701_015843_026a9faf-cc60-49c6-b7d9-f6de091106b8.png",
 "S1.2":"hf_20260701_015844_b7a19fda-f249-48a7-a0aa-9778d60e1eda.png",
 "S1.3":"hf_20260701_015848_f80e539d-9692-4cd6-954a-8da89fed3ce3.png",
 "S1.4":"hf_20260701_015851_25fb5a9b-766b-486d-9ac2-0c2af7dc05d8.png",
 "S1.5":"hf_20260701_015853_77f969c2-ba0c-491d-a043-fc6d488073e5.png",
 "S1.6":"hf_20260701_015856_b57a24e5-3a11-4ee1-aa94-0e7722fbc33c.png",
 "S1.7":"hf_20260701_015859_50461832-f6dc-4b53-b3d7-4c15c7dd2d81.png",
 "S2.1":"hf_20260701_020024_78b84464-2116-4096-a6de-cf62b515ab23.png",
 "S2.2":"hf_20260701_020027_24ec0857-9505-4845-946f-0e9907eb91a5.png",
 "S2.3":"hf_20260701_020030_369dda94-d818-4ae6-b648-02bcfdc52ed5.png",
 "S2.4":"hf_20260701_020032_53eec590-3916-4ea2-9965-97e00c59b03d.png",
 "S2.5":"hf_20260701_020035_1bbcf54b-e272-4350-8131-24ba1f888004.png",
 "S3.1":"hf_20260701_020038_361d2dd1-360a-478d-b1f5-59a0ee3079f0.png",
 "S3.2":"hf_20260701_020040_28e9003f-dfee-4c3b-9620-d2cfa090622b.png",
 "S3.3":"hf_20260701_044608_793ce3b3-d77c-4a51-a038-5fcf6fabb9f4.png",
 "S3.4":"hf_20260701_044611_96afa08a-02c0-432c-afb8-d50d95c385fd.png",
 "S3.5":"hf_20260701_020048_237f8d42-6254-4584-b682-bce00baf5714.png",
 "S3.6":"hf_20260701_044614_89802e08-b072-4d61-85e8-eec54e002daa.png",
 "S4.4":"hf_20260701_020119_1911222b-9ef5-4c3d-8784-26bd6c6407c1.png",
 "S5.1":"hf_20260701_020122_53de9538-15b5-47ee-a494-47bb687ba4c2.png",
 "S5.2":"hf_20260701_020124_4f1e6ab4-5b7a-4256-84e0-4eb48fa5b0c4.png",
 "S5.3":"hf_20260701_020127_3e9c7fba-7af8-41fb-8967-b5c0d387c96b.png",
 "S5.4":"hf_20260701_020129_3e69f01f-a11e-45d0-9276-0e9326730c5b.png",
 "S5.5":"hf_20260701_020133_375c3ad1-65d4-440a-9ad3-ff54319cef10.png",
 "S6.1":"hf_20260701_020150_66152963-05f9-4d83-8a5d-fafccc4fe8d1.png",
 "S6.2":"hf_20260701_020153_201fac3a-7c5e-49de-af49-24d57c57cd52.png",
 "S6.3":"hf_20260701_020155_1cd52ba4-b9ef-41c0-b081-d2c6939d9bd8.png",
 "S6.4":"hf_20260701_020158_e2295957-b5f1-49cc-9486-0ebbd6dc33b2.png",
 "S7.2":"hf_20260701_020206_c8edf5d5-f162-457c-88cf-845b7939276c.png",
 "S7.3":"hf_20260701_020209_73c903a7-3acc-4be0-9b05-303f3bcaf7e2.png",
 "S7.4":"hf_20260701_031034_68f3f56a-657b-4739-8d9f-8de1fa3d3ab4.png",
 "S8.2":"hf_20260701_020232_482af5fd-8c87-486d-b60f-2606953d71c9.png",
 "S8.3":"hf_20260701_020234_c242a6af-3d00-49f6-b0a0-0db5c315be0b.png",
 "S8.4":"hf_20260701_020237_d075e745-1a9d-49d7-a6a3-4a4ede493502.png",
 "S9.1":"hf_20260701_020243_fce64bac-12db-4bd4-bc5b-bd86365da376.png",
 "S9.3":"hf_20260701_020247_9bd50910-6f33-408c-ada1-781e215622c2.png",
}
# Genie-free backgrounds (12) — Genie is composited on top ------------------ #
BG = {
 "S4.1":"hf_20260701_043447_a46b468c-1b2a-4db7-a2ef-01a4aa53ea58.png",
 "S4.2":"hf_20260701_044530_04dad970-cfdf-4cc6-a61c-f44a8cb7bf41.png",
 "S4.3":"hf_20260701_043448_c24f42a1-4993-48f2-b826-d191e444e149.png",
 "S5.6":"hf_20260701_043449_a3d298aa-1c6f-430a-8f0c-18b7b5621e04.png",
 "S6.5":"hf_20260701_043450_d66c68e8-416b-4878-b777-437fd5303a5a.png",
 "S7.1":"hf_20260701_044532_278c3163-903b-4d28-a808-cfe3bb38aa69.png",
 "S7.5":"hf_20260701_043958_bbcd234c-1ccb-45b4-b879-e6c41300f8eb.png",
 "S7.6":"hf_20260701_043458_4f2c68d8-c0bb-467c-830a-86b613d3df5b.png",
 "S8.1":"hf_20260701_043500_686fa39e-763f-4be2-83b6-73c15d0d5ed8.png",
 "S8.5":"hf_20260701_043502_7d393ea5-2ae2-43b1-a159-8b7db517a0b8.png",
 "S9.2":"hf_20260701_043504_b890dc6e-8a4e-4a15-abac-df7019116707.png",
 "CR" :"hf_20260701_044534_9d09477b-1efb-40a0-b733-f99ccd9ae72a.png",
}
GENIE_CUT = "hf_20260701_043446_6404dd29-303c-4c2f-999d-db45698075d6.png"
# Genie placement per composited shot: (cx, cy, height_frac, flip_h, alpha) --- #
PLACE = {
 "S4.1":(0.50,0.34,0.60,False,1.0), "S4.2":(0.50,0.33,0.55,False,1.0),
 "S4.3":(0.80,0.52,0.72,True ,1.0), "S5.6":(0.19,0.54,0.72,False,1.0),
 "S6.5":(0.75,0.56,0.70,True ,1.0), "S7.1":(0.82,0.45,0.55,True ,1.0),
 "S7.5":(0.17,0.54,0.66,False,1.0), "S7.6":(0.85,0.26,0.34,True ,1.0),
 "S8.1":(0.18,0.54,0.72,False,1.0), "S8.5":(0.80,0.56,0.42,True ,0.9),
 "S9.2":(0.72,0.46,0.60,False,0.55),"CR" :(0.16,0.50,0.72,False,1.0),
}

# The film: (id, seconds, [(speaker, tamil, english_subtitle)]) --------------- #
SHOTS = [
 ("S1.1",6,[("narrator","சில நேரங்களில் பணம் நமக்கு எல்லாவற்றையும் தரும் போல தோன்றும்...","Sometimes it feels as if money can give us everything...")]),
 ("S1.2",6,[("narrator","ஆனால் அன்பு தான் வாழ்க்கையை முழுமையாக்கும்.","...but it is love that makes life whole.")]),
 ("S1.3",5,[]),("S1.4",5,[]),("S1.5",5,[]),
 ("S1.6",4,[("hamruthaa","அப்பா, என்னோட பாரு!","Appa, look at me!")]),("S1.7",4,[]),
 ("S2.1",6,[("nandini","இன்று ஒரு நாள் வேலை இல்லாமல் குடும்பத்தோட வெளிய போவோமா?","One day, no work — shall we go out together as a family?")]),
 ("S2.2",5,[("aravinth","இப்போ வேலை ரொம்ப இருக்கு நந்தினி...","There's so much work right now, Nandini...")]),
 ("S2.3",5,[("aravinth","சரி... இன்னைக்கு வேலை வேண்டாம். போகலாம்!","Alright... no work today. Let's go!")]),
 ("S2.4",5,[]),("S2.5",4,[]),
 ("S3.1",7,[("mirthula","வாவ்... இது ஒரு பழைய அரண்மனை!","Whoa... it's an old palace!")]),("S3.2",7,[]),
 ("S3.3",7,[("hamruthaa","அம்மா... அங்க ஏதோ பிரகாசிக்குது!","Mommy... something is shining over there!")]),("S3.4",5,[]),
 ("S3.5",5,[("hamruthaa","ஹிஹி! குரங்கு டான்ஸ் ஆடுது!","Hehe! The monkey is dancing!")]),("S3.6",4,[]),
 ("S4.1",7,[("genie","நான் ஆயிரம் வருடங்களாக இந்த விளக்கில் இருந்த ஜீனி!","I am the Genie who has lived in this lamp for a thousand years!")]),
 ("S4.2",7,[("hamruthaa","நீங்க கார்டூன்ல வர்ற ஜீனி மாதிரி இருக்கீங்க!","You look just like the Genie from the cartoons!")]),
 ("S4.3",7,[("genie","உங்களுக்கு மூணு ஆசைகள் தர்றேன். யோசிச்சு கேளுங்க!","I grant you three wishes. Choose them wisely!")]),("S4.4",4,[]),
 ("S5.1",6,[("aravinth","எனக்கு நிறைய பணம் வேண்டும்!","I wish for a lot of money!")]),
 ("S5.2",7,[]),("S5.3",7,[]),("S5.4",8,[]),
 ("S5.5",6,[("nandini","இவ்வளவு இருந்தும்... ஏன் இவ்வளவு வெறுமை?","With all of this... why does it feel so empty?")]),
 ("S5.6",6,[("genie","பணம் மட்டும் சந்தோஷத்தை தராது.","Money alone cannot bring happiness.")]),
 ("S6.1",6,[("mirthula","நான் உலகம் முழுக்க புகழ் பெற வேண்டும்!","I wish to become famous all over the world!")]),
 ("S6.2",8,[]),("S6.3",8,[]),
 ("S6.4",8,[("mirthula","எல்லாரும் இருக்காங்க... ஆனா யாரும் என்கூட இல்ல.","Everyone is here... but no one is with me.")]),
 ("S6.5",10,[("genie","புகழ் மட்டும் வாழ்க்கையை நிறைவு செய்யாது.","Fame alone cannot make a life complete.")]),
 ("S7.1",7,[("nandini","ஹம்ருதா, நீ என்ன ஆசைப்படுற, செல்லம்?","Hamruthaa, what do you wish for, my dear?")]),("S7.2",6,[]),
 ("S7.3",10,[("hamruthaa","எங்க குடும்பம் எப்பவும் சந்தோஷமா இருக்கணும்... நாம எல்லாருக்கும் உதவி செய்யணும்.","I wish our family is always happy... and that we help everyone.")]),
 ("S7.4",6,[]),("S7.5",6,[]),
 ("S7.6",15,[("narrator","ஒரு சின்ன அன்பான ஆசை... உலகத்தையே மாத்திச்சு.","One small loving wish... changed the whole world.")]),
 ("S8.1",6,[("genie","இந்தாங்க, உங்க குடும்பத்துக்கு ஒரு பரிசு!","Here — a gift for your family!")]),
 ("S8.2",7,[]),("S8.3",7,[]),("S8.4",7,[]),
 ("S8.5",8,[("genie","உண்மையான மந்திரம் அன்பு தான்.","The real magic is love.")]),
 ("S9.1",6,[]),
 ("S9.2",5,[("narrator","பணம், புகழ், செல்வம் எல்லாம் ஒருநாள் மறைந்து போகும்...","Money, fame, and riches will all fade one day...")]),
 ("S9.3",4,[("narrator","ஆனால் அன்பும், குடும்பமும், பிறருக்கு உதவும் மனமும் என்றென்றும் வாழும்.","...but love, family, and a heart that helps others live forever.")]),
 ("CR" ,7,[]),
]
VOICES = {"narrator":("ta-IN-ValluvarNeural","-6%","-2Hz"),"aravinth":("ta-IN-ValluvarNeural","+0%","+0Hz"),
 "genie":("ta-IN-ValluvarNeural","-8%","-8Hz"),"nandini":("ta-IN-PallaviNeural","-2%","+0Hz"),
 "mirthula":("ta-IN-PallaviNeural","+6%","+8Hz"),"hamruthaa":("ta-IN-PallaviNeural","+8%","+22Hz")}

# ------------------------------------------------------------------- helpers --
_ctx = ssl.create_default_context(); _ctx.check_hostname=False; _ctx.verify_mode=ssl.CERT_NONE
def download(fname, out):
    """Download CDN file (cached). Returns local path or None on failure."""
    p = os.path.join(DL, out)
    if os.path.exists(p) and os.path.getsize(p) > 0: return p
    try:
        req = urllib.request.Request(CDN+fname, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60, context=_ctx) as r, open(p,"wb") as f:
            f.write(r.read())
        return p if os.path.getsize(p) > 0 else None
    except Exception as e:
        print("  ! download failed", out, "->", e); return None

def synth(text, spk, out):
    # Run edge-tts in a fresh thread+loop — robust inside Colab's running loop.
    v,r,p = VOICES.get(spk, VOICES["narrator"]); err={}
    def run():
        try: asyncio.run(edge_tts.Communicate(text,v,rate=r,pitch=p).save(out))
        except Exception as e: err["e"]=e
    th=threading.Thread(target=run); th.start(); th.join()
    if "e" in err: raise err["e"]
    return out

def fit(img):
    iw,ih=img.size; s=max(W/iw,H/ih); img=img.resize((int(iw*s)+1,int(ih*s)+1),Image.LANCZOS)
    iw,ih=img.size; l,t=(iw-W)//2,(ih-H)//2; return img.crop((l,t,l+W,t+H))

def card(sid,cap):
    im=Image.new("RGB",(W,H))
    for y in range(H):
        t=y/H; im.paste((int(30+40*t),int(18+22*t),int(50+10*t)),(0,y,W,y+1))
    d=ImageDraw.Draw(im)
    if FONT and cap:
        f=ImageFont.truetype(FONT,54); ls=textwrap.wrap(cap,28) or [sid]
        y=(H-sum(f.getbbox(l)[3]+16 for l in ls))//2
        for l in ls: d.text(((W-d.textlength(l,font=f))//2,y),l,font=f,fill=(240,225,190)); y+=f.getbbox(l)[3]+16
    return im

def composite(bg_rgb, genie_rgba, place):
    cx,cy,hf,flip,alpha = place
    if flip: genie_rgba = genie_rgba.transpose(Image.FLIP_LEFT_RIGHT)
    gw,gh=genie_rgba.size; th=max(1,int(H*hf)); g=genie_rgba.resize((max(1,int(gw*th/gh)),th),Image.LANCZOS)
    if alpha<1.0: g.putalpha(g.split()[3].point(lambda v:int(v*alpha)))
    x=int(W*cx-g.size[0]/2); y=int(H*cy-g.size[1]/2)
    out=bg_rgb.convert("RGBA"); out.alpha_composite(g,(x,y)); return out.convert("RGB")

def sub_png(text,out):
    im=Image.new("RGBA",(W,220),(0,0,0,0)); d=ImageDraw.Draw(im)
    if FONT and text:
        f=ImageFont.truetype(FONT,46); ls=textwrap.wrap(text,42) or [text]; y=220-len(ls)*58-20
        for l in ls:
            x=(W-d.textlength(l,font=f))//2
            for dx in(-2,-1,0,1,2):
                for dy in(-2,-1,0,1,2): d.text((x+dx,y+dy),l,font=f,fill=(0,0,0,220))
            d.text((x,y),l,font=f,fill=(255,244,214,255)); y+=58
    im.save(out); return out

def get_image(sid, cap):
    if sid in BG:                                   # composite genie onto background
        bg = download(BG[sid], sid+"_bg.png")
        cut = download(GENIE_CUT, "GENIE_cut.png")
        if bg and cut:
            return composite(fit(Image.open(bg).convert("RGB")), Image.open(cut).convert("RGBA"), PLACE[sid])
        if bg: return fit(Image.open(bg).convert("RGB"))
        return card(sid,cap)
    p = download(IMG[sid], sid+".png") if sid in IMG else None   # direct shot
    return fit(Image.open(p).convert("RGB")) if p else card(sid,cap)

# ------------------------------------------------------------------- build ----
def build(sid,dur,lines):
    cap = lines[0][1] if lines else sid
    fp = os.path.join(DL, sid+"_frame.png"); get_image(sid,cap).save(fp)
    parts,subs,t = [],[],0.4
    for j,(spk,ta,en) in enumerate(lines):
        w=os.path.join(DL,f"{sid}_{j}.mp3"); synth(ta,spk,w); a=AudioFileClip(w)
        parts.append(a.set_start(t)); sp=sub_png(ta,os.path.join(DL,f"{sid}_{j}_s.png"))
        subs.append((sp,t,a.duration+0.3)); t+=a.duration+0.35
    D=max(dur,t+0.3)
    base=ImageClip(fp).set_duration(D).resize(lambda tt:1.0+ZOOM*(tt/D)).set_position("center")
    layers=[ColorClip((W,H),color=(0,0,0)).set_duration(D),base]
    for sp,st,sd in subs: layers.append(ImageClip(sp).set_start(st).set_duration(sd).set_position(("center",H-240)))
    c=CompositeVideoClip(layers,size=(W,H)).set_duration(D)
    if parts: c=c.set_audio(CompositeAudioClip(parts).set_duration(D))
    return c.crossfadein(XFADE) if XFADE>0 else c

print("Font:",FONT,"| building",len(SHOTS),"shots ...")
clips=[]
for i,(sid,dur,lines) in enumerate(SHOTS):
    print(f"  [{i+1:02d}/{len(SHOTS)}] {sid}"); clips.append(build(sid,dur,lines))

# ------------------------------------------------------------------ assemble --
film=concatenate_videoclips(clips,method="compose",padding=-XFADE)
if MUSIC_PATH and os.path.exists(MUSIC_PATH):
    m=AudioFileClip(MUSIC_PATH).fx(afx.audio_loop,duration=film.duration).fx(afx.volumex,10**(MUSIC_DB/20))
    film=film.set_audio(CompositeAudioClip([m,film.audio]) if film.audio else m)
film.write_videofile(OUTPUT,fps=FPS,codec="libx264",audio_codec="aac",bitrate="6000k",threads=4)
print("DONE ->",OUTPUT,f"({film.duration:.1f}s)")

try:
    from google.colab import files; files.download(OUTPUT)
except Exception:
    print("Not in Colab UI — find the file at", OUTPUT)
