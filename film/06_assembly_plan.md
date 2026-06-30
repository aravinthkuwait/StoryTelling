# 06 — ASSEMBLY PLAN (edit, transitions, text, mix)

How to cut the generated clips, narration, dialogue, music and SFX into the final
~5:00 master. Target: **3840×2160, 24 fps, H.264/H.265 MP4, ‑14 LUFS**.

## Edit Decision List (EDL)

Clips play in shot order from `03_shot_list.md`. Default transition is a clean cut;
specified transitions below are intentional.

| # | Clip | Dur | In→Out | Transition in | Notes / overlays |
|---|---|---|---|---|---|
| 1 | S1.1 | 6s | 0:00 | Fade from black (1s) | Title card option over aerial (see Titles) |
| 2 | S1.2 | 6s | 0:06 | Cut | |
| 3 | S1.3 | 5s | 0:12 | Cut | |
| 4 | S1.4 | 5s | 0:17 | Cut | |
| 5 | S1.5 | 5s | 0:22 | Cut | |
| 6 | S1.6 | 4s | 0:27 | Cut | Hamruthaa line |
| 7 | S1.7 | 4s | 0:31 | Slow push | Hold sad beat to 0:35 |
| 8 | S2.1 | 6s | 0:35 | Soft cut | |
| 9 | S2.2 | 5s | 0:41 | Cut | |
| 10 | S2.3 | 5s | 0:46 | Cut | Warm turn |
| 11 | S2.4 | 5s | 0:51 | Cut | |
| 12 | S2.5 | 4s | 0:56 | Cut | |
| 13 | S3.1 | 7s | 1:00 | **Whip/звук swell** | Palace reveal |
| 14 | S3.2 | 7s | 1:07 | Cut | |
| 15 | S3.3 | 7s | 1:14 | Cut | |
| 16 | S3.4 | 5s | 1:21 | Cut | |
| 17 | S3.5 | 5s | 1:26 | Cut | Comic beat |
| 18 | S3.6 | 4s | 1:31 | Cut → **flash to blue** | Burst |
| 19 | S4.1 | 7s | 1:35 | **From blue flash** | Genie rise (HERO) |
| 20 | S4.2 | 7s | 1:42 | Cut | |
| 21 | S4.3 | 7s | 1:49 | Cut | |
| 22 | S4.4 | 4s | 1:56 | Quick cuts | 4 reactions |
| 23 | S5.1 | 6s | 2:00 | Cut | |
| 24 | S5.2 | 7s | 2:06 | **Golden flash** | Mansion (HERO) |
| 25 | S5.3 | 7s | 2:13 | Cut | Montage |
| 26 | S5.4 | 8s | 2:20 | Slow dissolve (0.5s) | Loneliness |
| 27 | S5.5 | 6s | 2:28 | Cut | Tear |
| 28 | S5.6 | 6s | 2:34 | Cut | Genie lesson |
| 29 | S6.1 | 6s | 2:40 | Cut | |
| 30 | S6.2 | 8s | 2:46 | Fast cuts | Fame montage |
| 31 | S6.3 | 8s | 2:54 | **Hard cut to silence** | Empty stage (HERO) |
| 32 | S6.4 | 8s | 3:02 | Cut | Cries |
| 33 | S6.5 | 10s | 3:10 | Cut | Genie lesson |
| 34 | S7.1 | 7s | 3:20 | Soft cut | |
| 35 | S7.2 | 6s | 3:27 | Slow push | Innocent face (HERO) |
| 36 | S7.3 | 10s | 3:33 | Cut | The wish (HERO) |
| 37 | S7.4 | 6s | 3:43 | Cut | Moved to tears |
| 38 | S7.5 | 6s | 3:49 | **Golden bloom** | Light spreads (HERO) |
| 39 | S7.6 | 15s | 3:55 | Dissolve montage | Kindness (HERO); VO at 3:55 |
| 40 | S8.1 | 6s | 4:10 | Cut | Carpet gift |
| 41 | S8.2 | 7s | 4:16 | Cut | Lift‑off (HERO) |
| 42 | S8.3 | 7s | 4:23 | Cut | Mountains (HERO) |
| 43 | S8.4 | 7s | 4:30 | Cut | Chennai (HERO) |
| 44 | S8.5 | 8s | 4:37 | Cut | Ocean sunset (HERO) |
| 45 | S9.1 | 6s | 4:45 | Soft cut | Sunset |
| 46 | S9.2 | 5s | 4:51 | Cut | Genie departs; VO |
| 47 | S9.3 | 4s | 4:56 | Slow rise | Final text; VO; → fade white |
| 48 | CR | ~6s | 5:00+ | Fade from white | End‑credits photo |

**Total film body ≈ 300 s (5:00).** Credits card runs after.

## Titles & on‑screen text

- **Opening title (optional, over S1.1, ~0:02–0:06):**
  `அன்பின் அதிசய விளக்கு` / *THE MAGIC LAMP OF KINDNESS* — elegant gold serif, gentle
  fade, lower‑third or center. Keep subtle so it doesn't fight the narration.
- **Subtitles:** burn‑in or sidecar `.srt` of the **EN** column from `05`. Position bottom‑center,
  safe‑margin, readable gold/white with soft shadow. (A ready `subtitles.srt` skeleton is in
  `07_production_runbook.md`.)
- **Final message card (S9.3, 4:56–5:00, centered, fade in over particles):**
  ```
  உண்மையான செல்வம் – அன்பு ❤️
  True wealth is Love.

  Love Your Family.   ·   Help Others.   ·   Be Kind.
  ```
- **End credits (over CR):** small cast/character list and "A family fable in Tamil."

## Color & finishing

- Grade for warm South‑Indian palette: lift warm midtones, gentle teal in shadows,
  protect skin tones. HDR pass if delivering HDR; otherwise Rec.709 with a soft filmic curve.
- Add subtle, consistent film grain across all clips so AI‑generated shots match.
- Light vignette on emotional CUs (S1.7, S5.5, S6.4, S7.2/7.3).

## Audio mix (see `05` for targets)

Layers, top to bottom: **VO → Dialogue → SFX → Music**. Duck music ‑9 dB under any
VO/dialogue. Keep S6.3 deliberately near‑silent for impact. Resolve M11 (finale theme)
to full warmth over S9 and the credits.

## OpenMontage / ffmpeg assembly (reference recipe)

If assembling locally once clips + audio exist (OpenMontage Remotion timeline or raw ffmpeg):

```bash
# 1) Concatenate shot clips in EDL order (clips pre‑rendered to the listed durations)
#    Build clips.txt: one  file 'path/to/SX.Y.mp4'  line per EDL row, in order.
ffmpeg -f concat -safe 0 -i clips.txt -c:v libx264 -pix_fmt yuv420p -r 24 video_silent.mp4

# 2) Build the audio bed (VO + dialogue + music + sfx) in your DAW/OpenMontage → mix.wav
#    (timecodes from 05_audio_and_music.md). Then mux:
ffmpeg -i video_silent.mp4 -i mix.wav -c:v copy -c:a aac -b:a 320k -shortest film_master.mp4

# 3) Burn subtitles (optional)
ffmpeg -i film_master.mp4 -vf "subtitles=subtitles.srt:force_style='Alignment=2,FontSize=22'" \
       -c:a copy film_master_subbed.mp4
```

For a polished motion‑graphics/title layer, prefer OpenMontage's Remotion composer
(`OpenMontage/AGENT_GUIDE.md`) to render the title and final message cards, then drop them
onto the timeline at the timecodes above.
