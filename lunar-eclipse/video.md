# Lunar Eclipse Video — Final Cinematic Cut (9:16)

## v4 SUSPENSE FINAL — English (The Night Shift Star voice) — 2026-08-25

- **URL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/07bf4aa8-2479-43cd-8ebd-71d2f8ef719b.mp4 (`07bf4aa8-2479-43cd-8ebd-71d2f8ef719b`)
- 96.8s, thumbnail card at start (1.4s) AND end (1.8s)
- Voice: user clone (element `5da742e5`), seed_audio, speech_rate −8, suspense pauses
- Voice chain: highpass 75Hz, −2.5dB@300Hz, +3.5dB@4.2kHz, compressor, cinematic echo
- Music: sonilo_music dark suspense bed (job `20a8b16c`), looped to length, ducked
  under voice (sidechain), −14 LUFS master
- Captions: whisper-timed animated fly-in, Montserrat, amber accents
- Scenes slow-mo stretched to narration (up to 1.69×)

## Tamil version — same voice, same video — 2026-08-25

- **URL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/ddaffd9f-adc6-4fa0-b823-440be5369a00.mp4 (`ddaffd9f-adc6-4fa0-b823-440be5369a00`)
- 92.5s, Tamil narration in the SAME cloned voice via `text2speech_v2` variant
  `minimax` (seed_audio produced garbled Tamil — whisper-verified; minimax verified clean)
- Tamil VO job IDs: c377356a, fe258571, b210ddf6, c1059cb8, c6d665ad, e6e09046, 94d800cc, 41c5dc27
- Captions (REDONE 2026-08-25): display the EXACT authored Tamil script text.
  Whisper supplies only the clock — per-segment word timestamps on each clean
  voice take — and the authored words are mapped proportionally onto that
  timeline, then chunked into ≤3-word cues. 37 cues, 84% runtime coverage
  (gaps only at narration pauses), Noto Sans Tamil Bold 52px, animated fly-in.
  Verified: caption-region pixel check at every mid-cue confirms glyphs render.
  Builder scripts: `ta_exact_caps.py` (timing+text mapping), `srt2ass_ta.py`
- Same suspense music bed, echo chain, thumbnail start+end cards

---

## v2 FINAL — realistic style, cloned voice, title card, animated captions (2026-08-25)

- **FINAL (animated captions):** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/fcaf8c61-0f6b-4bd0-bfdc-df12b82ba1d2.mp4 (`fcaf8c61-0f6b-4bd0-bfdc-df12b82ba1d2`)
- **Alternate (static captions):** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/f90bd50f-4541-4deb-a93f-847803c1ef4b.mp4 (`f90bd50f-4541-4deb-a93f-847803c1ef4b`)
- **Thumbnail (4K 9:16, "THE MOON GOES DARK / AUG 28"):** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/23248fe9-a28c-4e3e-bd3f-d88bff10306b.png (`23248fe9-a28c-4e3e-bd3f-d88bff10306b`)
- **Specs:** 1080×1920, 30 fps, 75.0 s (1.4 s title card + 8 scenes), −16 LUFS
- **Voice:** cloned from the user's uploaded sample (element `5da742e5-ac1e-4f1f-8850-93b914c24c5f`, "Lunar Eclipse Narrator"); each scene retimed to the narration (slow-motion stretch up to 1.35× where needed, no audio time-stretch)
- **Visuals:** Kling 3.0 pro, documentary-real prompts (handheld micro-shake, film grain, animated people/objects: pointing figure with breath fog, swaying grass, birds, rolling clouds, thumb-scroll)
- **Captions:** whisper-timed, script-exact words; v3 burn = animated ASS (fast pop/fly-in alternating up/down, Montserrat ExtraBold caps, amber accent word per cue)
- **Thumbnail render:** nano_banana_pro 4K, text baked via workflow overlay (beast style)
- **v2 scene job IDs (Kling 3.0 pro):** ab4578d1, 88eb422e, 2ed862c3, 15f359b2, 4bd50e70, 8c12c116, 209d377c, 3bbed19c
- **Cloned VO job IDs (seed_audio, 44.1 kHz):** 27a53725, 7e0fbb48, b638edb4, 01ce2811, d1e9b8d5, 181c5d68, e631bed6, 9e4eaee6
- **YouTube monetization prep:** original scripted narration + user's own voice (transformative, not template content); tick "Altered content / synthetic media" disclosure at upload since realistic scenes are AI-generated.

---

## v1 (Grady preset voice, 65 s) — superseded

Generated with Higgsfield on 2026-08-25.

## Final video

- **URL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/4b3e8d34-85e5-46fc-971f-4f80bd1b7d3f.mp4
- **Media ID:** `4b3e8d34-85e5-46fc-971f-4f80bd1b7d3f`
- **Specs:** 1080×1920 (9:16), 30 fps, 65.3 s, H.264 + AAC, loudness-normalized to −16 LUFS
- **Voiceover:** Grady (Higgsfield preset, deep male narrator), one take per scene,
  each scene cut to its narration length (audio fitted per frame)
- **Captions:** burned-in, bold Montserrat ExtraBold caps, whisper-timed against the
  narration with script-exact wording (similarity 0.99, all 129 words timed, 36 cues)
- **Credits spent:** ~126 (8 scene clips on Kling 3.0 pro + 8 VO takes + assembly)

## Scene breakdown (storyboard → final timing)

| # | Narration | Visual | Length |
|---|---|---|---|
| 1 | "On August 28th, the Moon turns to shadow…" | Full-frame Moon close-up, shadow creeping, high contrast | 5.7 s |
| 2 | "This is the Corn Moon…" | Golden harvest moon rising over treeline, warm tones | 8.7 s |
| 3 | "It gets partially eaten…" | Minimal Sun–Earth–Moon shadow-cone diagram | 7.0 s |
| 4 | "…a dark bite carves into the surface… Just look up." | Eclipse timelapse → ground-level silhouette POV | 10.0 s |
| 5 | "Two weeks ago the Moon blocked the Sun…" | Split screen: solar corona vs. lunar shadow bite | 5.8 s |
| 6 | "It peaks after moonrise… And then it's gone." | Earth from space (Americas/Europe/Africa) → moon fading into cloud | 9.5 s |
| 7 | "So here's my question…" | Crowd watching the sky → lonely phone-scrolling in the dark | 14.5 s |
| 8 | "Tell me below. I'm reading every single one." | Hero moon shot reprise, clean lower third | 3.6 s |

Note: the storyboard's 30-second grid was extended to ~65 s because the full script
runs ~60 s at natural narration pace; every scene keeps its storyboard visual and
is timed exactly to its voiceover line.

## Scene clip job IDs (Kling 3.0 pro, 9:16, sound off)

1. `4fe7b067-e033-4dbb-91d8-3ff83c3d9ade`
2. `cf069c0d-73ed-46e7-ad8b-92c3d7ac8dc7`
3. `ad7ee41b-df8f-46f2-ab54-8c78b5bc214b`
4. `9c79e2a0-cdc8-481c-bdf3-10c6df110b3c`
5. `4ee0d990-e0e1-400e-b506-c67d3c00f018`
6. `a470e034-b798-467d-85e3-c75f06933322`
7. `428827a1-1bd2-40d6-9bd8-ccfc77d92d91`
8. `81a26483-645e-4814-888a-9e5bbcf9e32d`

## Voiceover take job IDs (seed_audio, voice: Grady)

1. `1828c69a-4d78-4d8f-a7f5-98fc7bcb773b`  (5.2 s)
2. `4fbf864b-f13f-4d0e-af8a-92396f0f42a0`  (8.2 s)
3. `f68f9e50-dd95-45ec-ae0a-25c5547cd17f`  (6.6 s)
4. `9d60dc78-a2a3-4d70-82be-e5eb3102a555`  (9.6 s)
5. `48391548-4830-44c1-bed5-b7a86d48b6dc`  (5.3 s)
6. `fc8ebef8-cf86-4ddd-bf18-1571c2de2955`  (9.0 s)
7. `f4193ea2-6d35-489d-a12e-fdc145a5f7ed`  (14.0 s)
8. `75c0fea2-bd76-48ce-bc19-a440177c9e35`  (3.1 s)

## Assembly pipeline (Higgsfield sandbox)

Per scene: trim VO tail silence → scene length = VO + 0.55 s → clip trimmed to
length, scaled/padded to 1080×1920 @30 fps (x264 CRF 18) → 0.2 s audio lead-in →
concat all 8 → loudnorm −16 LUFS → whisper-timed captions (script-exact words) →
bold Montserrat burn → upload + confirm.
