"""
Laundrmate Advertisement — ONE-SCRIPT BUILD (Google Colab)
============================================================
Paste this whole file into a single Colab cell (or `!python` it after
uploading) and run once. It downloads every finished clip, normalizes them to
a matching frame rate/resolution/codec, concatenates them into a silent
master, then muxes in the three language voiceover tracks to produce:

    Laundrmate_Advertisement_Tamil.mp4
    Laundrmate_Advertisement_English.mp4
    Laundrmate_Advertisement_Hindi.mp4

WHAT YOU MUST SUPPLY BEFORE THIS PRODUCES THE REAL FINAL AD
-------------------------------------------------------------
Three things are not ready yet and are marked "TODO" below:

1. CLIP_01 — the opening banner shot failed AI generation twice (Veo 3 kept
   reverting to a wide dusk-lit exterior with random pedestrians instead of
   the required banner close-up). The fix is to build it as a short
   motion-graphics card (LAUNDRMATE wordmark on the teal panel) cut into the
   already-passing shop-interior footage — see generation-log.md for the
   full writeup. Until that file exists, this script falls back to the
   flawed AI clip so the pipeline still runs end-to-end; swap in the fixed
   file the moment it's built.
2. CLIP_03, CLIP_12, CLIP_14 — pure 3D/motion-graphics clips (booking app UI,
   offer card, final call-to-action) per shot-list.md's zero-AI-cost plan.
   Not yet built. Placeholders point at nothing — fill in real file paths/
   URLs once produced, or the script will skip them and the ad will be
   short those three beats.
3. VO_TAMIL / VO_ENGLISH / VO_HINDI — no voiceover audio has been recorded or
   generated yet. Point these at your three narration files (see
   production/voiceover-scripts.md for the exact script text) before running,
   or the three outputs will be silent (video only, no narration).

Everything else (clips 02, 04, 05, 06, 07, 08, 09, 10, 11, 13) is a
QC-confirmed final Veo 3 render and the URL is filled in already.
"""

import os
import re
import json
import glob
import shlex
import subprocess

# ---------------------------------------------------------------------------
# 1. CONFIGURATION — edit this block, then just run the whole script
# ---------------------------------------------------------------------------

BASE = "/content/Laundrmate"
FPS = 25
WIDTH, HEIGHT = 1920, 1080

# Clip number -> source. Can be an https:// URL or a local file path
# (e.g. "/content/drive/MyDrive/Laundrmate/clip_01_final.mp4").
CLIPS = {
    "01": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170243_aef28d55-1581-44b0-8b98-f03b0a1b6a9f.mp4",  # TODO: known-flawed AI render — replace with the fixed hybrid clip once built (see generation-log.md, clip 01 recommendation)
    "02": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170251_d6ac9b29-340e-4e34-bb3c-3015c8425b75.mp4",
    "03": None,  # TODO: booking app UI — 3D motion-graphics clip, not yet built
    "04": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_173102_75b2e4c9-0542-41ee-9c68-a87c22bff782.mp4",  # v2: mother-identity fixed; setting drifted to indoor/sunset — accepted with caveat
    "05": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170458_4b44f73d-22e8-4e13-9f90-5c4bc2f96fd4.mp4",
    "06": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170302_ca958084-9c9c-4a12-af38-5da14e6eeb34.mp4",
    "07": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_174108_b0846efc-2a50-427b-a67e-106bf955409c.mp4",  # v2: brand-safety fix (no more "Miele" text)
    "08": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170338_e9a1aa48-365a-4350-a746-25c75a81c77d.mp4",  # dedicated-dryer-reference fix confirmed
    "09": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170502_04d37726-6f47-4cd9-b2d7-267f68eeb83d.mp4",
    "10": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170356_b03945e9-55eb-4caf-b3c0-f3a7b14a31fe.mp4",
    "11": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170411_7646192d-9f16-4031-bc80-ea783af00212.mp4",
    "12": None,  # TODO: offer card — 3D motion-graphics clip, not yet built
    "13": "https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/hf_20260801_170437_e906fa4c-dd83-42c2-9e58-b177d83059cc.mp4",
    "14": None,  # TODO: final CTA (logo + services + phone) — 3D motion-graphics clip, not yet built
}

# Point these at your three narration audio files once recorded/generated.
# Leave as None to build a silent (video-only) master for each language.
VO_TAMIL = None    # e.g. "/content/drive/MyDrive/Laundrmate/vo_tamil.wav"
VO_ENGLISH = None  # e.g. "/content/drive/MyDrive/Laundrmate/vo_english.wav"
VO_HINDI = None    # e.g. "/content/drive/MyDrive/Laundrmate/vo_hindi.wav"

# Optional shared background music, ducked under the voiceover.
MUSIC_BED = None  # e.g. "/content/drive/MyDrive/Laundrmate/music_bed.wav"

# ---------------------------------------------------------------------------
# 2. PIPELINE — no need to edit below this line
# ---------------------------------------------------------------------------

CLIPS_DIR = os.path.join(BASE, "clips")
NORM_DIR = os.path.join(BASE, "normalized")
OUT_DIR = os.path.join(BASE, "output")
for d in (CLIPS_DIR, NORM_DIR, OUT_DIR):
    os.makedirs(d, exist_ok=True)


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, **kw)


def fetch(number, source):
    dest = os.path.join(CLIPS_DIR, f"clip_{number}.mp4")
    if source is None:
        return None
    if source.startswith("http://") or source.startswith("https://"):
        sh(f"curl -sSL -o {shlex.quote(dest)} {shlex.quote(source)}")
    else:
        sh(f"cp {shlex.quote(source)} {shlex.quote(dest)}")
    return dest


def probe_duration(path):
    r = sh(
        f"ffprobe -v error -show_entries format=duration -of json {shlex.quote(path)}"
    )
    return float(json.loads(r.stdout)["format"]["duration"])


def normalize(path, number):
    out = os.path.join(NORM_DIR, f"clip_{number}.mp4")
    vf = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p"
    )
    sh(
        f"ffmpeg -y -i {shlex.quote(path)} -vf {shlex.quote(vf)} "
        f"-r {FPS} -fps_mode cfr -c:v libx264 -preset slow -crf 17 -an "
        f"-movflags +faststart {shlex.quote(out)}"
    )
    return out


def build_silent_master():
    ordered_numbers = sorted(CLIPS.keys(), key=int)
    normalized = []
    skipped = []
    for number in ordered_numbers:
        source = CLIPS[number]
        if not source:
            skipped.append(number)
            continue
        print(f"[{number}] fetching...")
        raw = fetch(number, source)
        print(f"[{number}] normalizing...")
        normalized.append(normalize(raw, number))

    if skipped:
        print(
            f"\n!! SKIPPING clips {', '.join(skipped)} — no source configured yet. "
            "The assembled video will be missing these beats. See the CLIPS "
            "dict at the top of this script.\n"
        )

    concat_list = os.path.join(NORM_DIR, "concat.txt")
    with open(concat_list, "w") as f:
        for n in normalized:
            f.write(f"file '{n}'\n")

    master = os.path.join(OUT_DIR, "Laundrmate_Master_Silent.mp4")
    sh(
        f"ffmpeg -y -f concat -safe 0 -i {shlex.quote(concat_list)} "
        f"-c:v libx264 -preset slow -crf 17 -r {FPS} -fps_mode cfr "
        f"-pix_fmt yuv420p -movflags +faststart {shlex.quote(master)}"
    )
    dur = probe_duration(master)
    print(f"Master built: {master} ({dur:.1f}s, {len(normalized)}/{len(ordered_numbers)} clips)")
    return master


def mux_language(master, lang_name, vo_path):
    out = os.path.join(OUT_DIR, f"Laundrmate_Advertisement_{lang_name}.mp4")
    if vo_path is None and MUSIC_BED is None:
        sh(f"cp {shlex.quote(master)} {shlex.quote(out)}")
        print(f"[{lang_name}] no VO/music supplied — wrote silent copy: {out}")
        return out

    inputs = [f"-i {shlex.quote(master)}"]
    if vo_path:
        inputs.append(f"-i {shlex.quote(vo_path)}")
    if MUSIC_BED:
        inputs.append(f"-i {shlex.quote(MUSIC_BED)}")

    if vo_path and MUSIC_BED:
        filt = (
            "[2:a]volume=0.25[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0,"
            "aresample=async=1:first_pts=0[a]"
        )
        maps = "-map 0:v:0 -map [a]"
    elif vo_path:
        filt = "[1:a]aresample=async=1:first_pts=0[a]"
        maps = "-map 0:v:0 -map [a]"
    else:  # music only
        filt = "[1:a]aresample=async=1:first_pts=0[a]"
        maps = "-map 0:v:0 -map [a]"

    cmd = (
        f"ffmpeg -y {' '.join(inputs)} -filter_complex {shlex.quote(filt)} "
        f"{maps} -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "
        f"{shlex.quote(out)}"
    )
    sh(cmd)
    print(f"[{lang_name}] wrote: {out}")
    return out


def qc(path):
    print(f"=== QC: {os.path.basename(path)} ===")
    dur = probe_duration(path)
    print(f"  duration: {dur:.1f}s (target ~60s)")
    for name, flt in (
        ("black frames", "blackdetect=d=0.1:pix_th=0.10"),
        ("frozen video", "freezedetect=n=-60dB:d=0.5"),
    ):
        r = subprocess.run(
            f"ffmpeg -i {shlex.quote(path)} -vf {flt} -an -f null - 2>&1",
            shell=True, capture_output=True, text=True,
        )
        hits = [l for l in r.stdout.splitlines() if "black_start" in l or "freeze_start" in l]
        print(f"  {name}: {'NONE' if not hits else 'DETECTED — ' + str(len(hits)) + ' hit(s)'}")


def main():
    print("=== Step 1/3: building silent master from all configured clips ===")
    master = build_silent_master()

    print("\n=== Step 2/3: muxing the three language versions ===")
    outputs = [
        mux_language(master, "Tamil", VO_TAMIL),
        mux_language(master, "English", VO_ENGLISH),
        mux_language(master, "Hindi", VO_HINDI),
    ]

    print("\n=== Step 3/3: QC pass ===")
    for out in outputs:
        qc(out)

    print("\nDone. Final files:")
    for out in outputs:
        print(" -", out)
    print(
        "\nBefore calling this final, manually check against "
        "production/continuity-checklist.md — banner spelling, phone number "
        "98847 12121, offer dates 31-07-2026 to 07-08-2026, and whether any "
        "TODO clips above are still missing from the timeline."
    )


if __name__ == "__main__":
    main()
