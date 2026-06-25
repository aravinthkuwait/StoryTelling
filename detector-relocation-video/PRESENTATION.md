# Detector Relocation — Cinematic Video Presentation

**Goal:** Take your real field footage and produce a polished, corporate/tech-style
cinematic video that visualizes relocating your metal/survey detector **5 meters**
from its existing location to a proposed new location, on an industrial / construction site.

**Engine:** Higgsfield → Seedance 2.0 (image-to-video + text-to-video)
**Look:** Clean corporate / tech · bright, smooth, professional · subtle HUD/measurement overlays
**Aspect:** 16:9 (use 2.35:1 if you want a more "film" feel) · 4K target

---

## 0. The most important step: keep it YOUR field

So the result looks like the *same* site (not a random AI field), drive the
generation from **your own frames** instead of pure text:

1. From your phone/laptop, open your video and **export 2–3 still frames**:
   - **Frame A** — a clean wide shot showing the detector in its **current** spot.
   - **Frame B** — the **empty new spot** ~5 m away where it will go (if visible).
2. In Higgsfield, upload Frame A and use **Image-to-Video** for the shots below.
   This locks the real ground, sky, equipment, and your detector's look.
3. For continuity, reuse the **last frame** of each generated clip as the **input
   image** for the next clip ("last-frame chaining"). This keeps the site consistent
   across all 5 shots.

> If you can attach the video in a Higgsfield-connected app, use the media-upload
> widget there. In this session the generation tools aren't connected — this file is
> the paste-ready script to run it yourself.

---

## 1. Story / shot list (≈30–40s total)

| # | Beat | Purpose | Length |
|---|------|---------|--------|
| 1 | Establish the site + detector at CURRENT location | Hook + context | 6–8s |
| 2 | Push in on the detector, "CURRENT LOCATION" tag | Identify the asset | 5–6s |
| 3 | The 5 m move — measurement line draws across to the new spot | The core idea | 6–8s |
| 4 | Detector now standing at the NEW location | Payoff | 6–8s |
| 5 | Pull-back / drone reveal, both spots marked, clean end card | Summary | 6–8s |

---

## 2. Paste-ready Seedance 2.0 prompts

> Each block is one clip. Format follows the cinematic hook structure:
> **[2s hook] [scene] [camera] [lighting] [mood] [tech specs]**.
> Use Frame A as the input image for Shot 1, then last-frame-chain the rest.

### Shot 1 — Establish (image-to-video, input = Frame A)
```
Wide aerial establishing shot of an active industrial construction site, a metal
survey detector mounted on a tripod stands in the foreground at its current
position, gravel ground, site fencing and parked equipment in the background.
Slow smooth crane-up and gentle push forward. Bright clean overcast daylight,
soft even lighting, crisp shadows. Professional corporate-tech mood, confident
and precise. Wide-angle lens, high dynamic range, subtle film grain, teal-clean
color grade, 16:9, 4K.
```

### Shot 2 — Identify the detector (image-to-video, last frame of Shot 1)
```
Slow dolly-in toward the survey detector on its tripod, shallow depth of field
gently blurring the busy site behind it, the device sharp and hero-lit. A clean
minimal HUD label fades in reading "CURRENT LOCATION". Bright neutral daylight,
soft key light on the unit. Calm, premium, engineering-presentation mood.
85mm telephoto feel, smooth gimbal motion, high clarity, light film grain,
16:9, 4K.
```

### Shot 3 — The 5 m relocation (text-to-video or image-to-video)
```
Top-down to low-angle tracking shot across the construction-site ground. A clean
animated dashed measurement line draws horizontally from the detector's current
position to an empty marked spot, with a floating tech label "5.0 m". The camera
tracks smoothly alongside the line as it extends. Bright corporate lighting,
crisp blueprint-style overlay graphics, precise and futuristic but minimal.
Smooth lateral dolly, wide-angle, high contrast clean grade, 16:9, 4K.
```

### Shot 4 — Detector at the NEW location (image-to-video, input = Frame B)
```
The survey detector now stands on its tripod at the new position 5 meters away,
firmly placed on the gravel, site activity softly out of focus behind. Gentle
push-in and slight orbit around the device as a HUD label fades in reading
"NEW LOCATION". Bright clean daylight, hero lighting on the unit. Reassuring,
polished corporate-tech mood, sense of resolution. Smooth gimbal, 50mm look,
shallow depth of field, subtle grain, 16:9, 4K.
```

### Shot 5 — Reveal + end card (image-to-video, last frame of Shot 4)
```
Smooth crane-up and pull-back drone reveal of the full construction site, both
the old and new detector positions softly marked with minimal pins connected by
a faint "5 m" line. Camera rises to a clean wide overview. Bright even daylight,
expansive and professional. Confident, finished corporate mood. Wide-angle
aerial, high dynamic range, clean teal grade, slow motion ease-out, 16:9, 4K.
```

---

## 3. Assemble & finish

1. Generate Shots 1–5 in Higgsfield (Seedance 2.0), 16:9, highest resolution.
2. If a clip is soft, run **upscale_video** to 2K/4K.
3. Stitch in any editor (CapCut / Premiere / DaVinci) in order 1→5.
4. Add: a quiet corporate music bed, soft whoosh on the line-draw in Shot 3,
   and your title card ("Detector Relocation Proposal — +5 m").
5. Optional: overlay real on-screen text with the exact bearing/coordinates of
   the new location for a true engineering proposal.

## 4. Tips for the cleanest result

- Keep camera moves **slow and smooth** — corporate/tech reads as controlled, not flashy.
- Hold the **same color grade** across all shots (clean, slightly cool/teal, bright).
- Reuse **last-frame chaining** so the ground and equipment stay identical shot to shot.
- Generate each shot **2–3 times** and keep the steadiest take.
- Keep overlays **minimal** — thin lines, one label at a time — that's what sells "pro".
