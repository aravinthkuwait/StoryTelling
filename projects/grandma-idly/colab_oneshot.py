# ============================================================================
#  பாட்டியின் இட்லி கடை — Paati's Idli Shop  ·  ONE-CELL cinematic builder
#  Paste this whole block into a single Google Colab cell and press Run (▶).
#  Optional: paste a Google Cloud Text-to-Speech API key below for the best
#  Tamil voice; leave it "" to use the free gTTS voice automatically.
# ============================================================================
GOOGLE_API_KEY = ""                         # <-- optional, for Google Chirp3-HD voice
TTS_VOICE      = "ta-IN-Chirp3-HD-Achernar" # or ...-Kore / ...-Sulafat / ta-IN-Wavenet-A
TTS_RATE       = 0.85

import os, json, base64, urllib.request, subprocess, pathlib, requests
os.system("apt-get -qq install -y ffmpeg fonts-noto-core >/dev/null 2>&1")
os.system("pip -q install pillow gTTS requests >/dev/null 2>&1")
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1280, 720, 24
TAMIL_BOLD = "/usr/share/fonts/truetype/noto/NotoSansTamil-Bold.ttf"
LATIN      = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
for d in ("clips", "narration", "out"):
    pathlib.Path(d).mkdir(exist_ok=True)

CLIP_URLS = {
 1:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_180601_d828045d-8e3b-4b76-b713-62374d4c795d.mp4",
 2:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181110_a4c8fb1b-452b-4140-b182-764cc5269dbf.mp4",
 3:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181112_0da26fa1-8772-47ec-9c8e-24a660a2470a.mp4",
 4:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181114_1a85a020-01a8-48b8-a345-d4169ff0cd03.mp4",
 5:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181117_3a0beab7-5b95-49f4-90b8-593d3099ab88.mp4",
 6:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181119_5d778da8-e46a-420d-8a94-bd52a2509e2a.mp4",
 7:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181122_17e880a6-5193-46c7-ac3f-c367cd78c89f.mp4",
 8:"https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260630_181123_3e557378-5356-4d0a-b92d-c76c9284c82b.mp4",
}
SCENES = [
 (1,"பாட்டியின் இட்லி கடை","Paati's Idli Shop","அதிகாலை நான்கு மணி. ஊரே தூங்கும் நேரம். ஒரு சிறிய விளக்கு மட்டும் எரிகிறது. அது பாட்டியின் இட்லி கடை."),
 (2,"முப்பது வருடம்","Thirty years, the same little shop","எழுபது வயது கமலா பாட்டி. முப்பது வருடமாக இதே கடை. மாவை அரைத்து, அடுப்பை மூட்டி, நாளைத் தொடங்குகிறாள்."),
 (3,"சுடச்சுட இட்லி","Soft as cotton, steaming hot","வெண்ணிற இட்லிகள், பஞ்சு போல மென்மை. சுடச்சுட சாம்பார், மணக்கும் சட்னி. தெருவெல்லாம் வாசம் பரவுகிறது."),
 (4,"காலை வாடிக்கையாளர்கள்","The morning regulars arrive","முதல் வாடிக்கையாளர்கள். வேலைக்குச் செல்லும் தொழிலாளர்கள். பள்ளிச் சிறுவர்கள். அனைவருக்கும் பாட்டியின் சிரிப்பு இலவசம்."),
 (5,"பசி நிற்காது, கண்ணா","“Hunger can't wait, child. Eat.”","ஒரு நாள், காசு இல்லாத ஒரு சிறுவன். பாட்டி சிரித்தாள். பசி நிற்காது கண்ணா, சாப்பிடு. இரண்டு இட்லி, அன்போடு."),
 (6,"வருடங்கள் ஓடின","The years rolled on","வருடங்கள் ஓடின. அந்தச் சிறுவன் படித்தான், வளர்ந்தான், ஊரை விட்டுச் சென்றான். ஆனால் அந்த ருசியை மறக்கவில்லை."),
 (7,"அவன் திரும்பி வந்தான்","One day, he came back","ஒரு நாள் அவன் திரும்பி வந்தான். அதே தெரு, அதே கடை, அதே பாட்டி. பாட்டி, ஞாபகம் இருக்கா? பாட்டி சிரித்தாள்."),
 (8,"சிறிய கடை, பெரிய இதயம்","A small shop. A big heart.","சிறிய கடை. பெரிய இதயம். பாட்டியின் இட்லி வெறும் உணவல்ல. அது அன்பு. அதுதான் இந்த ஊரின் காலை."),
]

def ffdur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1", str(p)], capture_output=True, text=True).stdout.strip())
def F(p,s): return ImageFont.truetype(p,s,layout_engine=ImageFont.Layout.RAQM)

def vgrad(top,bot):
    img=Image.new("RGB",(W,H),top); px=img.load()
    for y in range(H):
        t=y/(H-1); t=t*t*(3-2*t)
        px_row=(int(top[0]+(bot[0]-top[0])*t),int(top[1]+(bot[1]-top[1])*t),int(top[2]+(bot[2]-top[2])*t))
        for x in range(W): px[x,y]=px_row
    return img
def glow(d,cx,cy,rad,color,layers=14,maxa=120):
    for i in range(layers,0,-1):
        a=int(maxa*(i/layers)**2); r=int(rad*i/layers)
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=color+(a,))
def vignette():
    v=Image.new("L",(W,H),0); d=ImageDraw.Draw(v)
    d.ellipse([-W*0.3,-H*0.3,W*1.3,H*1.3],fill=255); v=v.filter(ImageFilter.GaussianBlur(160))
    return Image.new("RGB",(W,H),(0,0,0)), v
def wrap(d,text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def google_tts(text,out_mp3):
    if not GOOGLE_API_KEY.strip(): return False
    body={"input":{"text":text},"voice":{"languageCode":"ta-IN","name":TTS_VOICE},
          "audioConfig":{"audioEncoding":"MP3","speakingRate":TTS_RATE}}
    req=urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize?key="+GOOGLE_API_KEY.strip(),
        data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=60)); open(out_mp3,"wb").write(base64.b64decode(r["audioContent"])); return True
    except Exception as e:
        print("  google tts -> gTTS fallback:",str(e)[:90]); return False
def gtts_tts(text,out_mp3):
    from gtts import gTTS; gTTS(text,lang="ta").save(out_mp3)

def card_clip(cid,title,sub,pal,dur):
    top,bot,accent=pal
    img=vgrad(top,bot).convert("RGBA")
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(ov); glow(gd,W/2,H*0.46,260,accent,maxa=70); img.alpha_composite(ov)
    dark,mask=vignette(); img=Image.composite(img.convert("RGB"),dark,mask).convert("RGBA")
    d=ImageDraw.Draw(img); tf=F(TAMIL_BOLD,84); lines=wrap(d,title,tf,W*0.84); y0=H*0.40-len(lines)*46
    for i,ln in enumerate(lines):
        tw=d.textlength(ln,font=tf); y=y0+i*96
        d.text(((W-tw)/2+2,y+2),ln,font=tf,fill=(0,0,0,170)); d.text(((W-tw)/2,y),ln,font=tf,fill=(255,244,228,255))
    sf=F(LATIN,32); sw=d.textlength(sub,font=sf); d.text(((W-sw)/2,H*0.66),sub,font=sf,fill=(225,210,190,235))
    d.line([W*0.42,H*0.74,W*0.58,H*0.74],fill=accent+(200,),width=2)
    still=f"out/card_{cid}.png"; img.convert("RGB").save(still); frames=int(dur*FPS)
    vf=(f"scale={W*2}:{H*2},zoompan=z='min(zoom+0.0004,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={W}x{H}:fps={FPS},fade=t=in:st=0:d=0.8,fade=t=out:st={dur-0.9:.2f}:d=0.9,format=yuv420p")
    out=f"out/card_{cid}.mp4"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",still,"-f","lavfi","-i",
        "anullsrc=channel_layout=stereo:sample_rate=44100","-filter_complex",f"[0:v]{vf}[v]",
        "-map","[v]","-map","1:a","-t",f"{dur:.2f}","-c:v","libx264","-preset","medium","-crf","21",
        "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-r",str(FPS),out],
        check=True,capture_output=True)
    return out
def scene_clip(sid):
    src=f"clips/{sid:02d}.mp4"; mp3=f"narration/scene{sid:02d}.mp3"
    narr=ffdur(mp3); seg=max(narr+1.6,8.5); pts=seg/ffdur(src)
    vf=(f"setpts={pts:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
        f"fade=t=in:st=0:d=0.6,fade=t=out:st={seg-0.7:.2f}:d=0.7,format=yuv420p")
    af=(f"adelay=600|600,apad,atrim=0:{seg:.2f},afade=t=in:st=0:d=0.4,afade=t=out:st={seg-0.6:.2f}:d=0.6")
    out=f"out/cine{sid:02d}.mp4"
    subprocess.run(["ffmpeg","-y","-an","-i",src,"-i",mp3,"-filter_complex",f"[0:v]{vf}[v];[1:a]{af}[a]",
        "-map","[v]","-map","[a]","-t",f"{seg:.2f}","-c:v","libx264","-preset","medium","-crf","20",
        "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-r",str(FPS),out],
        check=True,capture_output=True)
    return out
def assemble(clips):
    open("out/concat.txt","w").write("".join(f"file '{pathlib.Path(p).name}'\n" for p in clips))
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i","out/concat.txt","-c","copy","out/body.mp4"],check=True,capture_output=True)
    dur=ffdur("out/body.mp4"); bar=92
    vf=(f"curves=r='0/0 0.5/0.53 1/1':g='0/0 0.5/0.49 1/0.98':b='0/0.02 0.5/0.46 1/0.93',"
        f"eq=contrast=1.06:saturation=1.08:brightness=0.01,noise=alls=9,"
        f"drawbox=x=0:y=0:w=iw:h={bar}:color=black:t=fill,drawbox=x=0:y=ih-{bar}:w=iw:h={bar}:color=black:t=fill,"
        f"fade=t=in:st=0:d=1.0,fade=t=out:st={dur-1.2:.2f}:d=1.2")
    final="out/paati_idli_cinematic.mp4"
    subprocess.run(["ffmpeg","-y","-i","out/body.mp4","-f","lavfi","-i","sine=frequency=110:sample_rate=44100",
        "-f","lavfi","-i","sine=frequency=164.81:sample_rate=44100","-filter_complex",
        f"[0:v]{vf}[v];[1:a]volume=0.04[a1];[2:a]volume=0.03[a2];[a1][a2]amix=inputs=2[pad];"
        f"[pad]atrim=0:{dur:.2f},afade=t=in:st=0:d=2,afade=t=out:st={dur-2:.2f}:d=2[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:weights='1 0.5'[a]","-map","[v]","-map","[a]","-t",f"{dur:.2f}",
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
        "-movflags","+faststart",final],check=True,capture_output=True)
    return final

print("1/4  downloading clips...")
for i,url in CLIP_URLS.items():
    r=requests.get(url,timeout=120)
    if r.status_code!=200 or not r.content:
        raise SystemExit(f"Clip {i} failed (HTTP {r.status_code}). Open it in Higgsfield, copy the .mp4 URL, replace CLIP_URLS[{i}].")
    open(f"clips/{i:02d}.mp4","wb").write(r.content); print(f"   clip {i}: {len(r.content)//1024} KB")
print("2/4  synthesizing Tamil narration...")
for sid,title,sub,narr in SCENES:
    out=f"narration/scene{sid:02d}.mp3"
    if not google_tts(narr,out): gtts_tts(narr,out)
    print(f"   scene {sid}: {ffdur(out):.1f}s")
print("3/4  stitching...")
clips=[scene_clip(sid) for sid,_,_,_ in SCENES]
intro=card_clip("intro","பாட்டியின் இட்லி கடை","A Short Film",((14,18,40),(4,5,14),(255,196,90)),5.5)
end=card_clip("end","அன்புடன்","With love",((40,28,16),(12,8,4),(255,206,120)),7.0)
final=assemble([intro]+clips+[end])
print(f"4/4  DONE -> {final}  ({ffdur(final):.1f}s)")
from IPython.display import HTML, display
display(HTML('<video width=640 controls src="data:video/mp4;base64,'+base64.b64encode(open(final,"rb").read()).decode()+'"></video>'))
from google.colab import files; files.download(final)
