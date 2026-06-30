#!/usr/bin/env python3
"""
Stitch the 8 Higgsfield cinematic clips into ONE voiced cinematic film.

The 8 clips live on your Higgsfield account (this environment can't download
them). So the workflow is:

  1. Download the 8 clips from Higgsfield (the job IDs are listed in
     clips/README.md, in story order).
  2. Save them as:  projects/grandma-idly/clips/01.mp4 ... 08.mp4
  3. Run:
       OpenMontage/.venv/bin/python projects/grandma-idly/stitch_cinematic.py

What it does (all local, no API key needed):
  * time-stretches each 5s clip to match its Tamil narration line
    (gentle slow-motion) and muxes the modern Google Tamil voice
    (committed under narration/),
  * adds intro + end title cards (reused from build_video.py),
  * applies the same cinematic grade + film grain + 2.39 letterbox,
  * writes out/paati_idli_cinematic.mp4.

Tested with stand-in clips; drop in the real clips and it produces the film.
"""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import build_video as bv  # reuse SCENES, render_card_clip, W/H/FPS, _ffdur

ROOT  = Path(__file__).resolve().parent
CLIPS = ROOT / "clips"
NARR  = ROOT / "narration"
OUT   = bv.OUT
OUT.mkdir(parents=True, exist_ok=True)

def scene_clip(scene) -> Path:
    """Stretch one downloaded clip to its narration length + mux the voice."""
    src = CLIPS / f"{scene['id']:02d}.mp4"
    mp3 = NARR / f"scene{scene['id']:02d}.mp3"
    narr = bv._ffdur(mp3)
    seg  = max(narr + 1.6, 8.5)                 # 0.6s lead + ~1s tail
    cdur = bv._ffdur(src)
    pts  = seg / cdur                            # >1 => slow-motion
    out  = OUT / f"cine{scene['id']:02d}.mp4"
    vf = (f"setpts={pts:.4f}*PTS,"
          f"scale={bv.W}:{bv.H}:force_original_aspect_ratio=increase,"
          f"crop={bv.W}:{bv.H},fps={bv.FPS},"
          f"fade=t=in:st=0:d=0.6,fade=t=out:st={seg-0.7:.2f}:d=0.7,format=yuv420p")
    af = (f"adelay=600|600,apad,atrim=0:{seg:.2f},"
          f"afade=t=in:st=0:d=0.4,afade=t=out:st={seg-0.6:.2f}:d=0.6")
    subprocess.run(["ffmpeg","-y","-an","-i",str(src),"-i",str(mp3),
        "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]",
        "-map","[v]","-map","[a]","-t",f"{seg:.2f}",
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-r",str(bv.FPS), str(out)],
        check=True, capture_output=True)
    return out

def assemble_cinematic(clips) -> Path:
    listf = OUT / "concat_cine.txt"
    listf.write_text("".join(f"file '{p.name}'\n" for p in clips))
    body = OUT / "body_cine.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listf),
        "-c","copy", str(body)], check=True, capture_output=True)
    dur = bv._ffdur(body)
    bar = 92
    vf = (f"curves=r='0/0 0.5/0.53 1/1':g='0/0 0.5/0.49 1/0.98':b='0/0.02 0.5/0.46 1/0.93',"
          f"eq=contrast=1.06:saturation=1.08:brightness=0.01,noise=alls=9,"
          f"drawbox=x=0:y=0:w=iw:h={bar}:color=black:t=fill,"
          f"drawbox=x=0:y=ih-{bar}:w=iw:h={bar}:color=black:t=fill,"
          f"fade=t=in:st=0:d=1.0,fade=t=out:st={dur-1.2:.2f}:d=1.2")
    final = OUT / "paati_idli_cinematic.mp4"
    subprocess.run(["ffmpeg","-y","-i",str(body),
        "-f","lavfi","-i","sine=frequency=110:sample_rate=44100",
        "-f","lavfi","-i","sine=frequency=164.81:sample_rate=44100",
        "-filter_complex",
        f"[0:v]{vf}[v];[1:a]volume=0.04[a1];[2:a]volume=0.03[a2];"
        f"[a1][a2]amix=inputs=2[pad];"
        f"[pad]atrim=0:{dur:.2f},afade=t=in:st=0:d=2,afade=t=out:st={dur-2:.2f}:d=2[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:weights='1 0.5'[a]",
        "-map","[v]","-map","[a]","-t",f"{dur:.2f}",
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-movflags","+faststart", str(final)],
        check=True, capture_output=True)
    return final

def main():
    missing = [i for i in range(1, 9) if not (CLIPS / f"{i:02d}.mp4").exists()]
    if missing:
        print(f"Missing clips {missing} in {CLIPS}/")
        print("Download the 8 clips from Higgsfield (see clips/README.md) as 01.mp4..08.mp4.")
        sys.exit(1)
    clips = []
    for s in bv.SCENES:
        print(f"==> scene {s['id']}: {s['sub']}")
        clips.append(scene_clip(s))
    intro = bv.render_card_clip("intro", "பாட்டியின் இட்லி கடை", "A Short Film",
                                ((14,18,40),(4,5,14),(255,196,90)), dur=5.5)
    end   = bv.render_card_clip("end", "அன்புடன்", "With love",
                                ((40,28,16),(12,8,4),(255,206,120)), dur=7.0)
    final = assemble_cinematic([intro] + clips + [end])
    print(f"\nDONE -> {final}  ({bv._ffdur(final):.1f}s)")

if __name__ == "__main__":
    main()
