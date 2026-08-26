# Lunar Eclipse Video — Final Cinematic Cut (9:16)

## v11 CURRENT — block seams closed (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/901e8b9b-535c-4a03-9428-401ca24cf45c.mp4 (`901e8b9b-535c-4a03-9428-401ca24cf45c`) — 93.1 s
- **TAMIL:** unchanged, still v6 — `d081d860-dc25-4f34-aece-c366d99313bb`, older wording.

### The v10 seam figure was measured with the wrong instrument

v10 reported seams of 0.36-0.70 s. That came from **Whisper word-boundary timings**, which
systematically overstate gaps: a conservative word-end plus a soft consonant onset reads as
half a second of silence that isn't in the audio. `seams.py` now measures the actual
contiguous sub-threshold span straddling each seam from the waveform (5 ms RMS frames,
2 % of peak), which is what the style's pause rule is really about.

Three changes closed them at source:

- `TRIM` stripped **trailing** silence only. It now strips leading silence too, so a take
  cannot start with a beat of room tone.
- Tail pad `+0.12 s` -> **`+0.06 s`**, lead delay `60 ms` -> **`40 ms`**: a 0.10 s seam
  budget, the bottom of the style's 0.10-0.30 s range.
- The measurement runs **inside the build**, so a regression shows up in the log.

Measured on this cut:

| seam | silence |
|---|---|
| 15.73 s | 0.24 s |
| 25.85 s | 0.20 s |
| 32.74 s | 0.00 s |
| 51.20 s | 0.00 s |
| 62.88 s | 0.00 s |
| 74.65 s | 0.11 s |
| 87.11 s | 0.00 s |

**worst 0.24 s, all within 0.30 s** (total 0.55 s across 7 seams).

Nothing was clipped by the tighter joins - each seam was transcribed in a +/-2.2 s window and
reads cleanly across the boundary ("...not for long. | This is the Corn Moon", "...set up,
just look up | and there's something else", and so on). The caption aligner still matches
**213/213** words, at 0.951.

Net effect: 95.4 s -> **93.1 s**, and 138 -> **140 wpm**.

Everything else carries over from v10 unchanged: 213-word script, `tighten.py` micro-pauses,
ping-pong for short clips, the nine-cue SFX bed, the moving music bed, beat pulses and cut
flares.

Builder scripts: `build_v11.sh`, `seams.py`, `tighten.py`, `sfx.py`, `mksfx_bed.py`.

---


## v10 — first cut in the Aravinth High-Retention Shorts style (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/6c9e210b-8a31-4dc2-9a9e-a5b6bd0e2913.mp4 (`6c9e210b-8a31-4dc2-9a9e-a5b6bd0e2913`) — 95.4 s
- **TAMIL:** unchanged, still v6 — `d081d860-dc25-4f34-aece-c366d99313bb`, older wording.

Denser script (213 words vs v9's 122), hook in the first two seconds, curiosity loop,
a real numeric reveal, plus the first sound-effect layer and moving music bed.

### The rate ceiling — measured, not assumed

The style asks for 175–200 wpm. **The TTS will not go there.** Probed on the same 53-word
paragraph:

| | wpm |
|---|---|
| minimax `speech_rate` 0 | 121 |
| minimax `speech_rate` +2 | 117 |
| seed_audio `speech_rate` 0 | 114 |
| seed_audio `speech_rate` +5 | 123 |

**`speech_rate` barely does anything** — on minimax, +2 came back *slower* than 0. seed_audio
responds weakly (114 → 123 across a 5-point swing). The knob is close to cosmetic, which also
means the earlier "Countdown Urgency at −2" vs "suspense at −8" distinction was coming from
the wording, not the parameter.

What actually buys speed is removing dead space, which the style explicitly requires.
`tighten.py` cuts every internal silence over 0.30 s down to 0.14 s on Whisper word
boundaries — editing, never time-stretching, which rule 18 forbids. That took the takes from
123 wpm to **138 wpm** on the finished cut (v9 was ~100). Reaching 175–200 would need a
different TTS engine or the time-stretch the style rules out.

### Ping-pong instead of extreme slow motion

A denser line on a short clip demanded absurd stretch — block 1 wanted **2.47×** from a 6.0 s
shot. Above 1.45× the build now plays the shot forward then reversed, doubling its length, and
re-computes from there. Block 1 fell to 1.24×, block 4 to 0.94×, block 5 to 0.84×.

### Sound effects — all original, generated not licensed

`sfx.py` synthesises four cues from noise and sine sweeps (nothing licensed in, so nothing to
clear): **whoosh** 0.50 s, **riser** 1.30 s, **impact** 0.45 s, **hit** 1.10 s.
`mksfx_bed.py` then places them on **real narration beats** — Whisper locates the anchor word
in the finished voice track, so the riser lands on the reveal and the impact lands on the
number actually being spoken. 9 cues placed:

- riser + impact on "one point four **million**" (39.4 s), impact on "**quarter**" (42.4 s)
- the single low **hit** on "that's not **coincidence**" (61.6 s)
- whooshes on alternate cuts only — rule 16 says not one on every transition

Measured in the finished mix: hit **+4.3 dB**, whoosh **+4.5 dB** against the second before.
All SFX are sidechained under the voice, so cues during speech stay deliberately subtle.

### Music that moves

The bed is no longer a flat 0.30. It dips before each reveal and lifts through it, via a
per-frame volume expression built from the reveal timestamps. Measured on the bed alone:

| reveal | dip before | lift during |
|---|---|---|
| 39.4 s | −5.3 dB | +4.1 dB |
| 61.5 s | −4.0 dB | +4.3 dB |
| 77.8 s | −7.7 dB | +1.8 dB |

### Verified

- 212 words over 92.5 s of speech = **138 wpm**.
- Zero adjacent duplicate words; **zero repeats of any word within 4 s**.
- Captions 213/213 words, similarity 0.944, 53 cues.
- Padding cut from 0.25 s lead + 0.65 s tail to 0.06 s + 0.12 s.

**Known residual:** ~10 seams between blocks still run 0.36–0.70 s, above the style's 0.30 s
ceiling. `tighten.py` only works inside a take; the seams are set by segment assembly, and
closing them means re-timing the video too. Worth fixing in the next build.

Builder scripts: `build_v10.sh`, `tighten.py`, `sfx.py`, `mksfx_bed.py`, `manifest_en.json`.

---


## v9 — 03 Countdown Urgency, footage re-timed to the read (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/9fe8916e-206d-49e5-9f96-b6d5282e3bab.mp4 (`9fe8916e-206d-49e5-9f96-b6d5282e3bab`) — 75.5 s
- **TAMIL:** unchanged, still v6 — `d081d860-dc25-4f34-aece-c366d99313bb` (91.9 s), older wording.

All eight blocks use **style 03 Countdown Urgency** (`speech_rate −2`): clipped, present
tense, hard stops, no trailing thoughts. Runtime 75.5 s, down from v8's 78.4 s and v7's 92.0 s.

### The cut now runs to the audio, not against it

The old timing rule was `stretch = max(LEN/CLIP, 1.0)` — footage could only ever be slowed
down. Against an urgent read that fights the pace: every shot drifts in slow motion while
the voice pushes. v9 changes the floor to **0.70**, so a shot whose line is shorter than it
plays *faster* than realtime (up to 1.43×) instead of being trimmed:

| seg | stretch | |
|---|---|---|
| 1 | 1.323 | slow-mo (clip shorter than the line) |
| 2 | 1.176 | slow-mo |
| 3 | 0.972 | ~realtime |
| 4 | 1.486 | slow-mo |
| 5 | 1.177 | slow-mo |
| 6 | 0.866 | **sped up** |
| 7 | 0.700 | **sped up to the 1.43× floor** |
| 8 | 1.045 | ~realtime |

Also tightened for the faster read: opening card 1.4 s → **1.0 s**, end card 1.8 s → **1.4 s**,
beat pulse deepened and sharpened (`ZOOM_AMP 0.05→0.065`, `ZOOM_SIG 0.005→0.0035`) and the
cut flares strengthened (`FLARE_AMP 0.20→0.24`). `mkbeats.py` now reads these from the
environment so a future video can dial its own intensity.

### A capped stretch truncated a line — caught before publish

The first v9 pass capped slow-motion at 1.45×. Block 4 needed 1.486×, so its video came out
14.567 s against 14.920 s of audio and `-shortest` clipped 0.35 s off "Just look up." The
upper cap was wrong: only the speed-up floor is needed. Removed, and every segment now
verified `video ≥ audio` before the concat.

### Four takes rejected, one for a genuinely odd reason

- Block 1 came back "the moon **tone** turns to shadow" — a word inserted from nowhere.
- Block 2 turned "the final **one** before autumn" into "the final **moon**", recreating the
  exact repeat this whole thread has been about.
- Block 7 inserted "catching **in** the photos".
- Block 5 said "the Moon blocked the **Sunday**". Not a mishearing — an isolated clip with no
  surrounding context still says it. **The TTS reads a sentence-final "Sun." as the weekday
  abbreviation.** Rewritten as "the Sun went dark behind the Moon" so `Sun` is never
  sentence-final. This is now a standing rule in `CLAUDE.md`.

All four regenerated on minimax and re-verified.

### Script

| # | Line |
|---|---|
| 1 | August 28th. The Moon turns to shadow. One night. Don't miss it. |
| 2 | This is the Corn Moon. The final one before autumn. And this year, it doesn't just rise. |
| 3 | It gets partially eaten. Earth slides between the Sun and the Moon. |
| 4 | A dark bite grows across the surface. Right in front of you. No telescope. Nothing to set up. Just look up. |
| 5 | Two weeks ago, the Sun went dark behind the Moon. This time, Earth returns the favor. |
| 6 | It peaks after moonrise. Visible across the Americas, Europe, and Africa. Then it's gone. |
| 7 | So here's my question. When it happens, are you outside? Or are you scrolling, and seeing the photos tomorrow, wishing you'd looked? |
| 8 | Tell me below. I'm reading every single one. |

### Verified on the finished cut

- Zero adjacent duplicate words; **zero repeats of any word within 4 s**, whole video.
- Every segment's video ≥ its audio — nothing truncated.
- Captions: 122/122 words, similarity **0.980**, 33 cues.
- 55/55 beat pulses fire (median motion lift 4.44, up from 2.53 in v8).
- 7/7 cut flares fire, **+55 to +67 luma** measured against the pre-FX frames.

Builder script: `build_v9.sh`, manifest `manifest_en.json`, beat/flare generator `mkbeats.py`.

---


## v8 — Hard-Cut Thriller + Direct Address (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/0b65fc74-e823-4c61-9253-40bd840c7718.mp4 (`0b65fc74-e823-4c61-9253-40bd840c7718`) — 78.4 s
- **TAMIL:** unchanged, still v6 — `d081d860-dc25-4f34-aece-c366d99313bb` (91.9 s).
  Its script is the older wording, so the two languages no longer match line for line.

### The chosen read

Blocks 1–6 use **style 06 Hard-Cut Thriller** (`speech_rate −4`); blocks 7–8 switch to
**style 08 Direct Address** (`speech_rate −3`). The script already turns at block 7 — it
stops narrating and starts asking — so the voice drops out of trailer mode for the last
twelve seconds. Same cloned voice throughout, so the switch reads as intent.

The rewrite runs 78.4 s against v7's 92.0 s: the trailer style is simply tighter.

| # | Line |
|---|---|
| 1 | August 28th. The Moon turns to shadow. Don't miss it. |
| 2 | This is the Corn Moon. The final one before autumn. But this year, it doesn't just rise. |
| 3 | It gets partially eaten. Earth slides between the Sun and the Moon. |
| 4 | And a dark bite grows across the surface. Right in front of you. No telescope. Nothing to set up. Just look up. |
| 5 | Two weeks ago, the Moon blocked the Sun. Now Earth returns the favor. |
| 6 | It peaks after moonrise. Visible across the Americas, Europe, and Africa. And then it's gone. |
| 7 | So here's my question, and I actually want an answer. When it happens, are you going outside to watch? Or will you forget, scroll past this, and see the photos tomorrow wishing you'd looked? |
| 8 | Tell me below. I'm reading every single one. |

### Staccato is built in post, not asked of the TTS

Style 06's punch — *The Moon. Turns. To shadow.* — is the one thing neither engine will
hold. seed_audio stutters on single-word sentences (it produced "the moon turns, turns to
shadow"); minimax and an ellipsis variant both smooth the fragments into one phrase
(measured: no gap above 0.25 s anywhere). So `staccato.py` inserts the gaps after the fact,
cutting on Whisper word boundaries and splicing silence:

- block 1 — 0.24 s after *Moon*, 0.24 s after *turns*
- block 4 — 0.26 s after *surface*, 0.30 s after *you*, 0.24 s after *telescope*
- block 6 — 0.26 s after *moonrise*, 0.34 s after *Africa*

Seven gaps total. Engineer hard pauses in the edit; do not expect the TTS to honour them.

### Two takes rejected before they shipped

- **Block 1** dropped the word *August* outright — speech began at 1.12 s with "28th".
- **Block 4**'s "a dark bite cuts into the surface" came back genuinely slurred: Whisper
  small *and* medium, plus an isolated 3 s clip, all heard "dark white curves". Reworded to
  "a dark bite grows across the surface", which reads clean.

Both regenerated on `text2speech_v2` / minimax. Every take is transcribed before it is used.

### Verified on the finished cut

- Zero adjacent duplicate words; **zero repeats of any word within 4 s**, whole video.
- Captions realigned: 131/131 words, similarity **0.989**, 33 cues.
- 55/55 beat zoom pulses fire; all 7 cut flares fire (+31 to +59 luma; cut 3 measures
  +46 against its own pre-FX frames — a naive window reads it low only because the shot
  cuts bright at that instant).
- One long-form Whisper pass garbled block 6, but the take, the voice stem and the final
  mix each transcribe it correctly in isolation — decoder drift, not an audio defect.

Builder scripts: `build_v8.sh`, `staccato.py`, manifest `manifest_en.json`.
Style reference for future videos: 10 delivery styles with punch words and TTS-ready lines.

---


## v7 — English script de-duplicated (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/635ee8b3-4dd6-4348-8a32-35df6ec1ce6b.mp4 (`635ee8b3-4dd6-4348-8a32-35df6ec1ce6b`) — 92.0 s
- **TAMIL FINAL:** unchanged from v6 — `d081d860-dc25-4f34-aece-c366d99313bb` (91.9 s)

### What "words are repeating" actually was

Reported again at 10–14 s. Word timings on the v6 video clock:

    12.42–12.94  "Moon"   <- "This is the Corn Moon"
    14.24–14.60  "moon"   <- "the last full moon of summer"

Not an audio defect. The acoustic self-similarity scan over each raw take finds
nothing but sustained vowels, and Whisper **with VAD off** (small *and* medium)
transcribes no doubled word in any take. The word *moon* is simply spoken twice
inside two seconds with the same falling contour, so it lands as a stutter.
(The earlier v6 check used `vad_filter=True`, which can collapse a repeat — that
was the wrong instrument and is why the first pass came back clean.)

Three lines carried the same pattern and were reworded:

| # | was | now |
|---|---|---|
| 2 | "the Corn Moon — the last full **moon** of summer" | "the Corn Moon. The final one before autumn." |
| 4 | "**No** telescope. **No** equipment." | "No telescope. Nothing to set up." |
| 7 | "**are you going** outside to watch — or **are you going** to forget" | "are you actually going outside to watch? Or will you forget" |

### seed_audio auto-completes clichés — use minimax for block 2

seed_audio rendered blocks 4 and 7 correctly but **twice ignored block 2's edit**,
speaking "the last full moon of summer" for both *"the last one of summer"* and
*"the final one before autumn"*. A control line ("The night sky goes very quiet…")
came back verbatim, so the model follows prompts in general — it snaps that one
highly-clichéd phrase back to its language prior. `text2speech_v2` variant
`minimax`, same cloned voice element, rendered it correctly on the first try, so
block 2 now comes from minimax and the rest stay on seed_audio.

### Verified on the finished English cut

- Zero adjacent duplicate words; **zero repeats of any word within 4 s**, whole video.
- Voice-only stem: 1 acoustic candidate (a cross-sentence prosody match, no lexical
  repeat). The 79 candidates in the full mix are the looping music bed — the bed
  alone yields 235, all at a 0.15 s lag, i.e. the musical pulse.
- Captions realigned to the new wording: 128/128 words, similarity 0.969, 33 cues.
- Effects intact: 55/55 beat zoom pulses fire; all 7 cut flares fire (+20 to +71 luma;
  cut 6 measures +56.6 against its own pre-FX frames — a naive window there reads
  negative only because the scene cuts bright→dark at that instant).

Builder script: `build_v7.sh`, manifest `manifest_en.json`.

---


## v6 — beat zoom pulses, cut flares, dry (echo-free) voice (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/a16771f8-3c9f-41a9-b141-5f2050beeb34.mp4 (`a16771f8-3c9f-41a9-b141-5f2050beeb34`) — 96.2 s
- **TAMIL FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/d081d860-dc25-4f34-aece-c366d99313bb.mp4 (`d081d860-dc25-4f34-aece-c366d99313bb`) — 91.9 s
- Thumbnail unchanged from v5 (`0fadbf7d-a8d6-4a0e-9a6d-ac56bfedf7f8`), still used as the
  animated card at both the start (1.4 s) and the end (1.8 s).

### Voice fix — the word doubling is gone

The v4/v5 chain ended in `aecho=0.62:0.5:85:0.16`. That slap-back repeated every word
~85 ms later and smeared consonants, which is what read as "words repeating / not smooth".
Diagnosed by whisper-transcribing all 8 raw takes: **no stutter exists in any take** — the
doubling was entirely the echo. v6 uses a dry chain and no reverb of any kind:

    highpass=f=80,
    equalizer=f=300:t=q:w=1.4:g=-2.0,
    equalizer=f=4000:t=q:w=1.4:g=2.5,
    acompressor=threshold=-20dB:ratio=2.8:attack=8:release=200:makeup=3

Verified on the finished mix: whisper transcribes 131 words with **zero adjacent duplicate
words**, and the caption aligner matches 129/129 script words at 0.96 similarity.
Suspense now comes from pacing and the ducked bed, not from room effects.

### Zoom pulse on beats

`mkbeats.py` runs spectral-flux onset detection over the music bed (2048/512 STFT,
adaptive local-mean threshold ×1.35, peak-pick with a 0.55 s minimum gap, top 55 onsets)
and emits a `zoompan` expression — a Gaussian bump per beat, capped at 1.055×:

    z = min(1.055, 1 + 0.05*(Σ exp(-((on/30 - b)^2)/0.005)))

55 beats detected. Verified: every one of the 55 shows a frame-to-frame motion spike above
its local baseline (median lift 3.12, min 0.99, max 59.18) — the pulse fires on all of them.

### Light flares on cuts

The same script emits an `eq` expression driven by the 7 scene boundaries — a brightness
and saturation flash ~±60 ms wide at each cut:

    brightness = 0.20*(Σ exp(-((t - c)^2)/0.0008))
    saturation = 1 + 0.16*(Σ …)

Verified: mean-luma lift at the 7 cut times is +24.1, +27.3, +46.2, +46.6, +47.7, +62.6,
+72.9 against the surrounding baseline — visible on every cut.

Star drift, cloud haze, music bed, ducking, captions and cards are unchanged from v5.
Builder scripts: `mkfx.py`, `mktext.py`, `mkbeats.py`, `ta_exact_caps.py`, `srt2ass2.py`.

NOTE: v5's links (`79029e42…` EN, `7e46b281…` TA) still hold the previous cut; the v5
upload credentials had expired, so v6 was published to new URLs.

---


## v5 — sky FX + cartoon animated cards (2026-08-26)

- **ENGLISH FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/79029e42-f185-4410-a7f8-0e3ce0af66fc.mp4 (`79029e42-f185-4410-a7f8-0e3ce0af66fc`) — 96.9 s
- **TAMIL FINAL:** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/7e46b281-b112-473a-bc48-6f55bb6472a8.mp4 (`7e46b281-b112-473a-bc48-6f55bb6472a8`) — 92.6 s
- **CARTOON THUMBNAIL (4K 9:16):** https://d2ol7oe51mr4n9.cloudfront.net/user_3FXuOlg1HqS8yvURHbzZgj2jNLj/0fadbf7d-a8d6-4a0e-9a6d-ac56bfedf7f8.png (`0fadbf7d-a8d6-4a0e-9a6d-ac56bfedf7f8`)
  - nano_banana_pro cartoon art (glowing moon + sun + sparkle stars + swirling clouds),
    title "AUGUST 28 / MOON GOES DARK" baked with the thumbnail workflow (beast style)
- **Animated cards:** the same cartoon art animated with Kling 3.0 i2v (job `7c8c29cf`) —
  twinkling stars, breathing moon/sun glow, drifting clouds — used for the 1.4 s opening
  card and 1.8 s end card, with the title text composited on top so it stays crisp
- **Sky effects on all 8 live scenes:** procedurally generated seamless tiles
  (`mkfx.py`) screen-blended over the footage —
  drifting starfield (14 px/s, sine twinkle, 0.32 opacity) + slow cloud haze
  (5 px/s, 0.11 opacity, faded out at the top so the moon stays clean).
  Verified: upper-sky mean brightness rises +2.7 to +8.6 vs the pre-FX cut.
- Voice, suspense music bed, ducking and caption styling unchanged from v4;
  EN captions whisper-aligned to script (0.95 similarity), TA captions exact script text.

NOTE: the older links (`07bf4aa8…` EN, `ddaffd9f…` TA) still hold the previous,
effect-free cut — their upload credentials expired, so v5 was published to new URLs.

---


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
