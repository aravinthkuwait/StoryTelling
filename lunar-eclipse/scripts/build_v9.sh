#!/bin/bash
set -e
cd /home/user
L=$1
export HF_WORKFLOWS="${HF_WORKFLOWS:-/home/user/.higgsfield/workflows}"
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj"
CARD="$B/hf_20260826_061407_7c8c29cf-50ec-4671-a0c7-be765d662852.mp4"
CL=(ab4578d1-9ff6-401d-afe3-5a50f5332dee 88eb422e-9d1b-44c4-9df5-c751ceab6618 \
2ed862c3-58ce-4f79-b44a-0a929b0c475a 15f359b2-9123-4874-aec9-c6c29d5ce68a \
4bd50e70-aa1a-4d39-9335-4eb6e3a76791 8c12c116-b1c7-4303-8109-bd97aed11d3c \
209d377c-92a3-4d3e-870e-746fdb05a97e 3bbed19c-0077-47ae-9fbc-f7d49de085d4)
EN=(hf_20260825_180814_f4259524-1088-46b2-a4df-fae4c9f5f204.wav \
hf_20260825_180816_2fbf3536-37c1-4895-9bb5-5eede98744e6.wav \
hf_20260825_180814_92b532af-3bc0-46ee-8e05-27abcd45f760.wav \
hf_20260825_180814_9d834f4e-040b-439a-b5da-ee711a77a27b.wav \
hf_20260825_180815_32afcd98-1d36-4bf0-abc1-266cd7dc3835.wav \
hf_20260825_180814_3b828b45-8f9e-4a65-beab-7945edc61673.wav \
hf_20260825_180815_04c11280-0654-4aab-b031-260bb721e94e.wav \
hf_20260825_180815_42cb1519-b142-4eb9-9ab2-d836a50eab94.wav)
TA=(c377356a-d7b2-478b-8783-9b229b6c8ef5 fe258571-7982-4ec1-b642-d680ae4e29ca \
b210ddf6-6234-45f8-9c75-fbee59cff628 c1059cb8-d32d-49bd-afac-5b4006aea86b \
c6d665ad-3dba-4b35-ab6d-e28d451b6254 e6e09046-67d4-44b7-bff0-8f251207b508 \
94d800cc-2eb4-41ce-b74e-3cc4e24b3698 41c5dc27-f08a-4c48-82af-3459f4280713)

mkdir -p fonts w6/clips "w6/$L/voices" "w6/$L/seg" "w6/$L/out"
bash "$HF_WORKFLOWS/subtitles/scripts/fetch_fonts.sh" >/dev/null 2>&1 || true
cp "$HF_WORKFLOWS/subtitles/scripts/fonts/"*.ttf fonts/ 2>/dev/null || true
[ -s fonts/NotoSansTamil-Bold.ttf ] || curl -sSfL -o fonts/NotoSansTamil-Bold.ttf 'https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSansTamil/hinted/ttf/NotoSansTamil-Bold.ttf'
[ -s stars.png ] || python3 mkfx.py
[ -s title_text.png ] || python3 mktext.py
echo "ASSETS_OK"

EXT=wav
for i in 1 2 3 4 5 6 7 8; do
  [ -s "w6/clips/clip$i.mp4" ] || curl -sSf -o "w6/clips/clip$i.mp4" "$B/hf_20260825_173807_${CL[$((i-1))]}.mp4" &
done; wait
# v9 narration: 03 Countdown Urgency throughout (speech_rate -2, hard stops, no staccato)
for i in 1 2 3 4 5 6 7 8; do
  ffmpeg -y -v error -i "/home/user/v9/voices/raw$i" -ar 48000 -ac 2 "w6/$L/voices/voice$i.wav"
done
echo "VOICES_OK"
[ -s w6/music.m4a ] || curl -sSf -o w6/music.m4a "$B/hf_20260825_180852_20a8b16c-78f6-48c2-987b-0affb3a098d0.m4a"
[ -s w6/card.mp4 ] || curl -sSf -o w6/card.mp4 "$CARD"
echo "DL_OK"

if [ ! -s w6/s0.mp4 ]; then
ffmpeg -y -v error -ss 0 -t 1.0 -i w6/card.mp4 -i title_text.png -f lavfi -t 1.0 -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[c];[c][1:v]overlay=0:0,format=yuv420p,fade=t=in:st=0:d=0.15,fade=t=out:st=0.82:d=0.18[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -shortest w6/s0.mp4
ffmpeg -y -v error -ss 2.6 -t 1.4 -i w6/card.mp4 -i title_text.png -f lavfi -t 1.4 -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[c];[c][1:v]overlay=0:0,format=yuv420p,fade=t=in:st=0:d=0.25[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -shortest w6/s9.mp4
fi
echo "CARDS_OK"

VOFX="highpass=f=80,equalizer=f=300:t=q:w=1.4:g=-2.0,equalizer=f=4000:t=q:w=1.4:g=2.5,acompressor=threshold=-20dB:ratio=2.8:attack=8:release=200:makeup=3"
TRIM="areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.2,areverse"
CUTS=""
for i in 1 2 3 4 5 6 7 8; do
  ffmpeg -y -v error -i "w6/$L/voices/voice$i.$EXT" -af "$TRIM,$VOFX" -ar 48000 -ac 2 "w6/$L/voices/trim$i.wav"
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "w6/$L/voices/trim$i.wav")
  C=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "w6/clips/clip$i.mp4")
  LEN=$(python3 -c "print(f'{$D+0.65:.3f}')")
  R=$(python3 -c "print(f'{max($LEN/$C,0.70):.5f}')")
  ffmpeg -y -v error -i "w6/$L/voices/trim$i.wav" -af "adelay=250|250,apad" -t "$LEN" -ar 48000 -ac 2 "w6/$L/seg/a$i.wav"
  ffmpeg -y -v error -i "w6/clips/clip$i.mp4" \
    -vf "setpts=$R*PTS,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p" \
    -an -t "$LEN" -c:v libx264 -preset medium -crf 18 "w6/$L/seg/v$i.mp4"
  ffmpeg -y -v error -i "w6/$L/seg/v$i.mp4" -i "w6/$L/seg/a$i.wav" -c:v copy -c:a aac -b:a 192k -shortest "w6/$L/seg/s$i.mp4"
  echo "$L seg$i vo=$D len=$LEN stretch=$R"
  CUTS="$CUTS $LEN"
done
for i in 1 2 3 4 5 6 7 8; do echo "file '/home/user/w6/$L/seg/s$i.mp4'"; done > "w6/$L/seg/scenes.txt"
ffmpeg -y -v error -f concat -safe 0 -i "w6/$L/seg/scenes.txt" -c copy "w6/$L/out/scenes.mp4"

ffmpeg -y -v error -i "w6/$L/out/scenes.mp4" -loop 1 -i stars.png -loop 1 -i clouds.png -filter_complex \
"[1:v]fps=30,crop=1080:1920:x='mod(t*14\,1080)':y=0,eq=brightness='0.06*sin(2*PI*t/2.2)':eval=frame,setsar=1,format=yuv420p[st];\
[2:v]fps=30,crop=1080:1920:x='mod(t*5\,1080)':y=0,setsar=1,format=yuv420p[cl];\
[0:v][st]blend=all_mode=screen:all_opacity=0.32:shortest=1[b1];\
[b1][cl]blend=all_mode=screen:all_opacity=0.11:shortest=1[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 18 -c:a copy "w6/$L/out/scenes_fx.mp4"
echo "$L FX_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 w6/$L/out/scenes_fx.mp4)"

CUTCSV=$(python3 -c "
lens=[float(v) for v in '$CUTS'.split()]
acc=0.0; out=[]
for l in lens[:-1]:
    acc+=l; out.append(f'{acc:.2f}')
print(','.join(out))")
SDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "w6/$L/out/scenes_fx.mp4")
ZOOM_AMP=0.065 ZOOM_CAP=1.07 ZOOM_SIG=0.0035 FLARE_AMP=0.24 python3 mkbeats.py w6/music.m4a "$SDUR" 1.0 "$CUTCSV" "w6/$L/out/fx2.txt"
ZE=$(sed -n 1p "w6/$L/out/fx2.txt"); BE=$(sed -n 2p "w6/$L/out/fx2.txt"); SE=$(sed -n 3p "w6/$L/out/fx2.txt")
printf "[0:v]zoompan=z='%s':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,eq=brightness='%s':saturation='%s':eval=frame,format=yuv420p[v]\n" \
  "$ZE" "$BE" "$SE" > "w6/$L/out/fx2.filter"
ffmpeg -y -v error -i "w6/$L/out/scenes_fx.mp4" -filter_complex_script "w6/$L/out/fx2.filter" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 18 -c:a copy "w6/$L/out/scenes_fx2.mp4"
echo "$L FX2_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 w6/$L/out/scenes_fx2.mp4)"

printf "file '/home/user/w6/s0.mp4'\nfile '/home/user/w6/%s/out/scenes_fx2.mp4'\nfile '/home/user/w6/s9.mp4'\n" "$L" > "w6/$L/seg/all.txt"
ffmpeg -y -v error -f concat -safe 0 -i "w6/$L/seg/all.txt" -c copy "w6/$L/out/concat.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "w6/$L/out/concat.mp4")
ffmpeg -y -v error -i "w6/$L/out/concat.mp4" -vn -ar 48000 -ac 2 "w6/$L/out/vo.wav"
FO=$(python3 -c "print(f'{$DUR-2.5:.3f}')")
ffmpeg -y -v error -stream_loop -1 -i w6/music.m4a -ar 48000 -ac 2 -t "$DUR" \
  -af "afade=t=in:st=0:d=1.2,afade=t=out:st=$FO:d=2.5,volume=0.30" "w6/$L/out/bed.wav"
ffmpeg -y -v error -i "w6/$L/out/bed.wav" -i "w6/$L/out/vo.wav" -filter_complex \
  "[0:a][1:a]sidechaincompress=threshold=0.028:ratio=7:attack=8:release=420[d];[1:a][d]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[m]" \
  -map "[m]" -ar 48000 -ac 2 "w6/$L/out/mix.wav"
ffmpeg -y -v error -i "w6/$L/out/concat.mp4" -i "w6/$L/out/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "w6/$L/out/final_clean.mp4"
echo "$L CLEAN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 w6/$L/out/final_clean.mp4)"

if [ "$L" = "en" ]; then
  python3 "$HF_WORKFLOWS/subtitles/scripts/audio_to_captions.py" w6/en/out/final_clean.mp4 \
    --srt w6/en/out/caps.srt --mixed --language en --script manifest_en.json > w6/en/out/rep.txt 2>&1
  tail -c 300 w6/en/out/rep.txt
  python3 srt2ass2.py w6/en/out/caps.srt w6/en/out/anim.ass
else
  VOICEDIR=w6/ta/voices python3 ta_exact_caps.py w6/ta/out/caps.srt
  sed 's/,64,/,52,/' srt2ass2.py > srt2ass_ta.py
  CAPFONT="Noto Sans Tamil" python3 srt2ass_ta.py w6/ta/out/caps.srt w6/ta/out/anim.ass
fi
ffmpeg -y -v error -i "w6/$L/out/final_clean.mp4" -vf "ass=w6/$L/out/anim.ass:fontsdir=/home/user/fonts" \
  -c:v libx264 -preset medium -crf 18 -c:a copy "w6/$L/out/final.mp4"
echo "${L}_FINAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 w6/$L/out/final.mp4)"

code=$(curl -sS -o /dev/null -w '%{http_code}' -X PUT -H 'Content-Type: video/mp4' --upload-file "w6/$L/out/final.mp4" "$(cat /home/user/$L.url)")
echo "${L}_PUT -> $code"
[ "$code" = "200" ] && echo "V6_${L}_DONE"
