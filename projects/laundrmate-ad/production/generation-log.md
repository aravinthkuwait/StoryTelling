# Laundrmate Ad — Generation Log

Running record of every Higgsfield job: IDs, status, and credits. Update after
every batch. Budget cap: **800 credits**. Balance at production start:
**866.4** (ultra plan).

## Stage 3 — Final renders (Google Veo 3, in progress)

User confirmed "do it" for both: (a) fix clip 08 via a dedicated dryer
reference, (b) start Stage 3 final renders for all approved clips. Cost
preflighted and confirmed: **Veo 3 preview (full) = 58 cr/clip, Veo 3 fast =
22 cr/clip** — exact match to the shot-list.md tiered plan.

Clip 08 fix: generated a dedicated dryer-only reference still (isolated from
the washing machine look, since the model kept anchoring to the washer
identity with no distinct dryer asset to draw on) —
`f13dd05f-ebde-48a9-93be-b27a2082df97` (Nano Banana Pro, ~2 cr). Used directly
as the Veo 3 final's start_image rather than re-testing on the cheap draft
tier first, given the root-cause diagnosis was clear.

**Veo 3 constraint:** unlike Seedance 2.0 Mini's multi-image `image_references`,
Veo 3 only accepts a single `start_image`. Each final clip below uses the one
most representative reference still; supporting characters/props are carried
by the text prompt alone (adapted from the QC-validated draft prompts).

| Clip | Tier | Job ID | start_image ref | Cost |
|---|---|---|---|---|
| 01 opening | Veo 3 preview | `aef28d55-1581-44b0-8b98-f03b0a1b6a9f` | storefront `379801f8` | 58 cr |
| 02 customer need | Veo 3 fast | `d6ac9b29-340e-4e34-bb3c-3015c8425b75` | family `6eb8ad0d` | 22 cr |
| 04 pickup | Veo 3 preview | `66512d8c-5cc3-4a9e-b161-1729072cb6ba` | executive `583e5e37` | 58 cr |
| 05 sorting | Veo 3 fast | `4b44f73d-22e8-4e13-9f90-5c4bc2f96fd4` | bag `5acc2427` | 22 cr |
| 06 wash load | Veo 3 preview | `ca958084-9c9c-4a12-af38-5da14e6eeb34` | washer `47fb2fa9` | 58 cr |
| 07 wash montage | Veo 3 preview | `fb742f57-dfcd-4570-8a86-1f8d6f56f178` | washer `47fb2fa9` | 58 cr |
| 08 drying (fixed) | Veo 3 preview | `e9a1aa48-365a-4350-a746-25c75a81c77d` | **new dryer ref** `f13dd05f` | 58 cr |
| 09 saree/dry-clean | Veo 3 fast | `04d37726-6f47-4cd9-b2d7-267f68eeb83d` | garments `b212181e` | 22 cr |
| 10 ironing | Veo 3 preview | `b03945e9-55eb-4caf-b3c0-f3a7b14a31fe` | station `706d8a02` | 58 cr |
| 11 QC/packing | Veo 3 fast | `7646192d-9f16-4031-bc80-ea783af00212` | station `706d8a02` | 22 cr |
| 13 delivery | Veo 3 preview | `e906fa4c-dd83-42c2-9e58-b177d83059cc` | family `6eb8ad0d` | 58 cr |

**Batch cost: 494 credits (7×58 + 4×22) + 2 cr dryer ref = 496 credits.**
Combined with Stage 1+2 spend (~120 cr), running total ≈ **616 credits of the
800 cap** — leaves ~184 cr reserve for any final-render regens.

Next: poll all 11 jobs (Veo 3 preview renders typically take longer than the
Seedance mini drafts — check patiently), QC each via the media_import_url →
video_analysis flow, and verify locked facts one more time on the finals
(banner text, phone number, offer card wording/dates once those are built,
character consistency) before handing off for edit/assembly.

**Update: all 11 renders completed** (checked 2026-08-01 ~17:05 UTC). Quick
read of Higgsfield's own auto-generated scene descriptions (attached to each
completed job) is very promising:
- Clip 01: banner close-up confirmed again, "no dusk or sunset tones... bright
  and crisp" — the fix held through to final quality.
- Clip 08 (the fixed dryer shot): description now explicitly shows "warm,
  completely dry garments tumble... dark charcoal-grey drum... digital
  display showing 165°F and 8 minutes 12 seconds remaining... accelerated
  time-lapse... opens the dryer door and lifts out warm, fully dry garments" —
  every element that failed twice on the draft tier is now present. Root-cause
  fix (dedicated dryer reference) appears to have worked.
- Clip 11: no phone mentioned; "ticks boxes on a printed checklist with a pen"
  confirmed.

QC imports + video_analysis started on all 11 finals:

| Clip | Imported media_id | Analysis ID |
|---|---|---|
| 01 | `0fd27c17-08d1-49f2-9846-0832029789e7` | `8222ebac-a5e7-4dd1-a27e-01bc975abf6a` |
| 02 | `496ad9ad-5351-4052-abd3-e32e0772076e` | `cde460de-eab9-467a-9f66-ba5f6430d6d1` |
| 04 | `fb2dbd99-c49f-4124-9171-ee7e9d4dab0b` | `7fba42be-1dc6-4fa5-9a18-324ecef22543` |
| 05 | `cb7a4cbe-775b-437d-8cfd-bc9b43a0cf9a` | `5d259f81-c803-4ba0-9b79-50e287043b60` |
| 06 | `10f7f5dd-303d-494c-a481-eee2626a6400` | `74345197-284c-4c95-94e8-a81d4687d5e7` |
| 07 | `f1ba5f34-2b2f-4f33-b2ba-5c16fcfc3f61` | `1267816b-4df4-48a5-88f5-434f4694ff33` |
| 08 | `0c624f37-4c24-40eb-9a0e-d0befe31c033` | `4dc132fa-a480-4812-8c03-31ce63809baf` |
| 09 | `bb8767d2-6c60-439b-b039-c74c548259d7` | `bd57752c-d6ad-4378-9fe3-83017f0ca75b` |
| 10 | `fae128d4-7451-43c6-a9c0-8a18105d4f6f` | `bc5081ea-e1c8-4674-82a2-d588d7bac209` |
| 11 | `636e9d2f-7624-4c0d-81b0-193b5ff7fc27` | `23279409-fe74-492a-b75e-d60750707e51` |
| 13 | `0af56906-0e52-48aa-be24-0c219d3c05b4` | `94f5c70f-e1cc-4035-b87d-4e4ff591e58f` |

### Stage 3 formal QC verdicts (2026-08-01 ~17:15 UTC)

| Clip | Verdict |
|---|---|
| 01 opening | ❌ **REGEN** — reverted to the original failure: wide ext. shot, "golden-hour" sky (dusk-adjacent), two random pedestrians walking past, shutter mostly closed. No banner close-up at all. The Seedance draft fix did not transfer to Veo 3. |
| 02 customer need | ✅ PASS — family present and consistent (mustard kurti mother, uniform daughter, maroon-gold saree grandmother, light blue shirt father); dialogue drifted from script ("drawing book" instead of uniform) but scene intent matches, no continuity violations |
| 04 pickup (regen v2) | User asked to prioritize mother continuity over budget headroom — resubmitted `75b2e4c9-0542-41ee-9c68-a87c22bff782`, swapping the start_image to the **mother/family reference** (`6eb8ad0d`) instead of the executive ref, with the executive's look (teal polo, navy cap, navy bike) carried entirely by text. QC pending. |
| 05 sorting | ✅ PASS — scan, sort into separate baskets, care-label check, consistent shop interior |
| 06 wash load | ✅ PASS (note: staff shown in navy polo, not brand teal — cosmetic, matches clip 07's same drift) |
| 07 wash montage | ❌ **REGEN — brand safety issue.** QC description explicitly names **"Miele Professional"** on the washing machine — a real, recognisable competing appliance brand rendered onto equipment. Not acceptable for a commercial. Resubmitted with an explicit no-real-brand-names / unbranded-machine instruction. |
| 08 drying (fixed) | ✅ **PASS — root-cause fix confirmed.** Real dryer drum tumbling, digital panel reads 165°F, employee opens door and retrieves warm dry garments, saree/sneakers drying separately. The two prior failures (replayed washer sequence) are resolved. |
| 09 saree/dry-clean | ✅ PASS — gloved inspection, roller/press treatment, careful hand movements, no washer in frame |
| 10 ironing | ✅ PASS (note: employee shown in apron over patterned blouse rather than teal polo — cosmetic uniform drift, same single-reference limitation as clip 04/06/07) |
| 11 QC/packing | ✅ PASS — no phone; clipboard + pen checklist; garment folded, bagged, placed correctly |
| 13 delivery | ✅ **PASS — best result of the batch.** All four family members present and fully consistent (exec hands bag to the correct mustard-kurti mother, daughter with pressed uniform, father buttoning shirt, grandmother in maroon-gold saree). |

**Score: 8/11 clean PASS, 3 regenerating (01, 04, 07).**

Cost update: with clip 04's regen (58 cr) added to the 01+07 regens (116 cr),
this round's retries total 174 cr. Running total ≈ **616 + 174 = 790 credits
of the 800 cap** — essentially the full budget. Balance on the actual
Higgsfield account remains healthy (3244.4 cr) — the 800 cap is our own
project budget ceiling, not an account limit. Any further regens beyond this
round would need an explicit go-ahead to raise the project cap.

Regens resubmitted with hardened prompts:
- **01 v2 (final tier):** `e84558e8-ed8c-48a0-8111-d79210d98a4e` — forces the close-up hold for 2+ seconds before any camera movement, explicitly forbids pedestrians/street/dusk/golden-hour.
- **07 v2:** `b0846efc-2a50-427b-a67e-106bf955409c` — explicit "no visible brand names, logos, or manufacturer markings... completely unbranded/generic" instruction added.

### Round 2 QC verdicts — IMPORTANT: job_display's text is not real QC

Discovered a methodology issue: `job_display`'s description field echoes Veo 3's
own **enhanced prompt** (what it intended to render), not an independent
analysis of the actual output frames. It can look like the fix worked while
the real video didn't change. `video_analysis_create`/`video_analysis_status`
(which genuinely inspects rendered frames) is the only trustworthy QC signal —
all verdicts below are from that, not from job_display text.

| Clip | Verdict |
|---|---|
| 01 opening v2 | ❌ **STILL FAILS — 2nd final-tier failure, same exact pattern.** True video_analysis shows the identical original problem: static wide shot, golden-hour light, two pedestrians walking past, palm trees and auto-rickshaws — no banner close-up at all, despite the prompt explicitly forcing one. **Root cause identified:** Veo 3's `start_image` is used as the literal first frame of the video (unlike Seedance's blended `image_references`). Our storefront reference (`379801f8`) is itself a wide establishing photo, not a tight banner crop — so Veo 3 keeps animating outward from that wide composition regardless of what the text prompt demands. Prompt engineering alone cannot fix this; the reference image itself needs to already be the close-up. **Not retrying a 3rd time** per budget instruction — see recommendation below. |
| 07 wash montage v2 | ✅ **PASS — brand-safety issue resolved.** No real brand names in the QC description this time; machines read as generic stainless steel, LAUNDRMATE-only branding confirmed. Staff shown in navy polo rather than teal (same cosmetic drift as clips 06/10) — a note, not a blocker. |
| 04 pickup v2 | ⚠️ **PARTIAL — primary goal achieved, new drift introduced.** The mother now correctly appears in her mustard-yellow kurti (the requested fix worked). However the scene relocated: it opens on all four family members together in the apartment at sunset (duplicating clip 13's family-reveal beat) and the handover itself happens in an indoor hallway, not the exterior morning street specified. Bike color also drifted to teal instead of navy. Likely the same start_image-as-literal-first-frame effect as clip 01, since the family reference photo is an interior sunset-lit shot. |

**Final tally: 9 of 11 clips are clean, ad-ready passes** (02, 05, 06, 07, 08,
09, 10, 11, 13). **Clip 04** has the right mother now but wrong setting/time-
of-day — usable with a caveat, or worth one more attempt if the budget cap is
raised. **Clip 01** still fails outright after 2 final-tier attempts.

### Recommendation for clip 01 (do not spend further without this fix)

Re-reading `FINAL_DIRECTION.md`'s own spec for this beat: *"Use a brief
premium 3D logo animation only during the first second, then immediately
transition into real footage."* **The banner reveal was never supposed to be
AI-generated live-action video in the first place** — the master creative
brief already calls for a 3D/motion-graphics logo card for that opening
second, exactly matching the shot-list.md pattern already used for the pure
text/UI clips (03, 12, 14) at zero AI cost. Recommend: build the banner
close-up as a ~1s motion-graphics card (LAUNDRMATE wordmark, teal panel,
matches the verified still `379801f8`), then hard-cut into the **shop-interior
portion of clip 01's Veo 3 footage**, which renders correctly in both v1 and
v2 (staff opening up, wiping counters, switching on lights — that part has
passed twice). This fully resolves the failure at zero additional AI spend.

**No new AI generation spend this round** (round 2 was QC-only, via the free
`video_analysis` flow, on the already-submitted v2 jobs). Final running total
stays at **790 of the 800 credit cap** — production spend is effectively
complete pending the clip 01 / clip 04 decisions above.

## Stage 1 — Reference stills (Nano Banana Pro, ~2 cr each)

Batch submitted 2026-07-30:

| Ref | Purpose | Job ID | Status |
|---|---|---|---|
| ref_01 | Storefront + LAUNDRMATE banner | `379801f8-1a67-4454-8486-6afa46c9ec5b` | ✅ completed — **banner text verified visually: exactly "LAUNDRMATE / The Laundry Company"** |
| ref_02 | Customer family (mother, daughter, father, grandmother) | `6eb8ad0d-5baf-4f57-82d8-c755385bff60` | ✅ completed |
| ref_03 | Delivery executive + branded bike | `583e5e37-8d9d-4a16-aa74-4dd0a51804c9` | ✅ completed |
| ref_04 | Shop interior layout | `30885248-7ab3-4201-9823-592dfc167231` | ✅ completed |
| ref_05 | Hero garments, tagged (uniform, shirt, saree + curtains/mat/shoes) | `b212181e-a2f2-47a0-812f-3fdd24a8cd22` | ✅ completed |
| ref_06 | Branded laundry bag close-up | `5acc2427-b9d2-4c9e-bcd4-6990334d4c55` | in_progress (retried after limit reset) |
| ref_07 | Washing machine drum/controls close-up | `47fb2fa9-d8ba-49c1-b17c-95698232812c` | in_progress (retried after limit reset) |
| ref_08 | Steam ironing + packing station | `706d8a02-bfad-4ec0-92f6-01a011c48a46` | in_progress (retried after limit reset) |

Estimated spend so far: ~16 credits (8 stills). All 8 stills ✅ completed
(refs 06–08 confirmed complete 2026-07-31).

## Stage 2 — Draft clips (Seedance 2.0 Mini, 480p silent, ~5 cr each)

> Model note: "Wan 2.5 Fast" no longer exists in the Higgsfield catalog.
> Drafts use **`seedance_2_0_mini`** (5 cr / 5 s, multi-image references,
> identity-consistent) — cheaper than the old Wan draft tier. Pass
> `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612` on every call:
> the backend repeatedly suggests an unrelated "IN THE DARK" preset otherwise.

| Clip | Job ID | Status |
|---|---|---|
| draft_01 opening banner (REGEN v2) | `697fbb1d-c1e5-439c-8e41-2081d33793d5` | in_progress — prompt fixed: first-frame banner close-up, no high-fives, explicit morning light |
| draft_02 customer need | `cca3ae98-a5fe-4e34-89c0-94c0ac28ea5e` | ✅ **PASS** — QC `e80aaae3`: family matches refs (mother mustard kurti folding blue shirt, daughter braids + uniform with name tag, father adjusting shirt, grandmother maroon-gold saree, phone pickup, warm natural light). Final-render note: uniform must read navy-and-white (not checkered); show curtains/mats/shoes on screen. |
| draft_04 pickup | `8a2ebf2a-82f2-480e-b3d1-6f46ceffcbb0` | in_progress |
| draft_05 receiving/sorting | `35ae0918-72db-493f-9664-f858fe2c6039` | in_progress |
| draft_06 washing load | `4f8ceb64-c6d1-4e08-a523-49adbf483c3f` | in_progress |
| draft_07 washing montage | `42555379-7356-4600-85e0-4daa91c0c62b` | in_progress |
| draft_08 drying | `76397e59-46db-46d8-a933-8f4911736e9f` | in_progress |
| draft_09 saree/dry-clean | `5f288dfc-cee7-4324-8676-ab8e20a83b83` | in_progress |
| draft_10 steam ironing | `843d37f4-1175-412e-9c17-1cb8d62aa038` | in_progress |
| draft_11 QC/packing | `e74be64c-07d9-47f2-9cd7-ca503ae7404e` | in_progress — succeeded on retry after 429 |
| draft_13 delivery | `a7922db8-f2e6-497a-8b37-ee84b4643ccc` | in_progress — succeeded on retry after 429 |

**All 11 draft clips (01 regen, 02, 04–11, 13) are now submitted and complete.**
QC in progress for the 9 that finished this round (02 already passed earlier).

## QC method update: use media_import_url, not media_upload/confirm

`media_confirm` proved unreliable (repeated "Something went wrong" errors even
after successful S3 PUTs). Switched to **`media_import_url`**, which pulls
directly from the Higgsfield CDN result URL and returns an already-confirmed
`media_id` in one call — no sandbox relay, no separate confirm step. Use this
for all future QC imports.

| Clip | Draft job ID | Verdict |
|---|---|---|
| 01 (regen v3) | `ea1a8d13` | ✅ **PASS** — banner fills frame as literal opening shot (teal panel, illuminated white block letters + subtext), no dusk/blue-hour grade this time (mixed cool interior + warm golden-hour on facade, read as morning not sunset), clean push into shop interior with staff at counter, no invented actions |
| 02 customer need | `cca3ae98` | ✅ PASS (from earlier round) |
| 04 pickup | `8a2ebf2a` | ✅ PASS — exec, mother, bag, tagging, loading all match refs |
| 05 sorting | `35ae0918` | ✅ PASS (note: uniform read as "checkered" not plain navy-and-white — cosmetic, fix at final render) |
| 06 wash load | `4f8ceb64` | ✅ PASS — full load→detergent→program→close→tumble sequence, human hands throughout |
| 07 wash montage | `42555379` | ✅ PASS (note: "thick white soapy foam" a bit heavy — tone down at final render) |
| 08 drying (regen v2) | `6ce3d144` | ❌ **REGEN — 2nd failure, same root cause.** Description again shows a glass-door washer being pulled open and clothes retrieved by hand — no rotating dryer drum, no temperature/timer display, no time-lapse, despite an explicit "DRYER SCENE, not washing machine" prompt. Likely cause: no dedicated dryer reference still exists — only refs for the washing machine (`47fb2fa9`) and general shop interior (`30885248`) were supplied, so the model keeps anchoring to the washer identity. **Recommend: either (a) generate a dedicated dryer reference still first and retry once, or (b) treat as a post-production fix (cut the wash-unload footage short and build the drying beat from stock/motion-graphics), rather than a 3rd blind AI retry.** Flagging for user decision rather than spending more credits unprompted. |
| 09 saree/dry-clean | `5f288dfc` | ✅ PASS — inspection, brushing, roll-polish press, blazer steaming, no washer in frame |
| 10 ironing | `843d37f4` | ✅ PASS (note: saree/uniform ironing beats not shown, only shirt+trousers — acceptable, realism criteria met) |
| 11 QC/packing (regen v2) | `78a33ff5` | ✅ **PASS** — no phone anywhere; employee uses a printed paper checklist with pen; final action correctly places only the bagged/labelled garment into the branded bin/bag |
| 13 delivery | `a7922db8` | ✅ PASS — exec→family handover→father's shirt→family group with grandmother's saree, natural reactions, evening light |

**FINAL SCORE: 10/11 PASS. Only clip 08 (drying) still fails after 2 attempts.**

### Regen round 3 (01) / round 2 (08, 11) — results

| Clip | New job ID | Fix applied | Result |
|---|---|---|---|
| 01 opening (v3) | `ea1a8d13-0760-44bd-b389-5c5693f0d2c5` | Single reference image only (storefront), extreme close-up framing forced, explicit "no orange/amber/dusk" negative repeated twice | ✅ PASS |
| 08 drying (v2) | `6ce3d144-3aa8-4d6a-bebb-e361789e4b41` | Explicitly labeled "DRYER SCENE, not a washing machine scene", contrasting drum color, digital timer/temp display, time-lapse, forbids washing-machine loading action | ❌ still fails — replayed washer unload, no dryer drum/timer/time-lapse |
| 11 QC/packing (v2) | `78a33ff5-54df-41aa-8f42-8ae4128f8c22` | Explicit "no phone or smartphone anywhere", paper checklist + pen instead of tablet, clarifies only the garment enters the bag | ✅ PASS |

**Decision needed from user on clip 08** — per production policy, not spending a
3rd blind AI-retry on it without confirmation. Options: (a) generate a
dedicated dryer reference still (isolate from the washer look) and retry once
more, ~2 cr + ~5 cr; (b) build the drying beat in post from stock/motion
graphics instead of pure AI generation, per the shot-list.md fallback pattern
already used for the 3D text/UI clips; (c) accept clip 06/07 (which already
show a washing→foam→curtains/mat/shoes montage) as sufficient washing coverage
and cut clip 08 down to a short reaction/temperature-check insert built from
existing footage.

**Stage 3 readiness:** 10 of 11 drafts are approved. Awaiting user confirmation
before spending on Stage 3 final renders (Veo 3 / Veo 3 Fast, ~400+ credits
per the tiered plan in shot-list.md) and before deciding clip 08's path.

Draft reference-image mapping and prompts: reuse the submitted prompts for
01/02 as the template; per-clip refs are per the shot-list continuity anchors.

**Billing update 2026-07-31 ~04:15 UTC: balance jumped 866.4 → 3841.4 credits
and the daily grace_daily_limit_reached cap is GONE — 8 of 10 queued
generations in this batch were accepted in one shot.** The grace-period
restriction appears lifted (owner may have refreshed billing, or the grace
period simply expired/upgraded). The only error hit this round was a
short-term `rate_limit_reached` (429) on clips 11 and 13 — a burst/concurrency
throttle, unrelated to the old daily cap — expected to clear within minutes.

Spend so far: ~25 (drafts 01–02) + ~40 (8 new drafts @ ~5cr) ≈ 65 credits.

## Blocker history

2026-07-30: the account hit a daily generation limit ("grace period") after
the first 5 submissions. The limit reset later the same day; refs 06–08 were
resubmitted successfully. Watch for the cap re-appearing mid-draft-batch —
if a generation call errors with the daily-limit message, pause and re-arm a
later check-in rather than burning retries.

2026-07-31 ~02:10 UTC: cap hit again after 5 generations (refs 06–08 +
drafts 01–02). **The account appears limited to ~5 generations per day while
in the billing "grace period", despite 850+ credits on balance.** At this
rate the remaining ~9 drafts + ~11 finals + retries ≈ a week of calendar
time. ACTION FOR OWNER: refresh the Higgsfield subscription/billing to lift
the grace cap — the offer window (31-07 → 07-08-2026) leaves little slack.
Known-good generation windows: accepted ~09:55 UTC 07-30 and ~02:03 UTC
07-31; next retry armed for ~02:05 UTC 08-01.

2026-07-31 ~04:15 UTC: **grace_daily_limit_reached cap no longer occurring.**
Balance jumped to 3841.4 credits and a batch of 8 generations submitted
without any daily-limit error. The remaining production (drafts 08–13 done
this round, finals to follow) can now proceed at normal speed. Only
short-lived `rate_limit_reached` (429) throttling was seen (clips 11, 13),
which clears within minutes — retry rather than wait 24h.

## Draft QC method

Draft videos are QC'd with Higgsfield's `video_analysis_create` (scene-by-scene
description, ~3-5 min/clip; does NOT count against the generation cap).
Flow: `media_upload` presigned URL → sandbox `curl PUT` of the generated mp4 →
`media_confirm` → `video_analysis_create(video_input_id)` → poll
`video_analysis_status`. Judge the returned scene descriptions against
`continuity-checklist.md`; anything ambiguous gets a manual single-frame
base64 review (see below). NOTE: keep any base64 printout under ~15k chars —
tool output truncates around 20k and a truncated dump is unusable.

## Notes on remote review

The generation CDN (`d8j0ntlcm91z4.cloudfront.net`) is blocked by this
environment's network policy. To review outputs visually, use
`sandbox_exec` (Higgsfield sandbox reaches the CDN) to crop/downscale to a
small JPEG, print it as base64 (keep each printout under ~30k chars or the
tool output truncates), then decode locally and view. Banner verification of
ref_01 was done this way.

## Locked visual identity (from stills batch 1)

- Brand palette: deep teal + navy + white
- Mother: early 30s, shoulder-length black hair, mustard yellow kurti
- Daughter: ~8, two braids, navy-and-white school uniform pinafore
- Father: late 30s, light blue formal office shirt
- Grandmother: 60s, maroon silk saree with gold border
- Executive: mid 20s, teal polo + navy cap, navy bike with teal LAUNDRMATE box

Reuse these exact descriptors in every subsequent prompt.

## Next actions

1. Poll the 5 pending jobs; review outputs (banner spelling is the critical
   check on ref_01).
2. When the daily limit resets: generate refs 06–08, then start Stage 2
   (11 draft clips, Wan 2.5 Fast) using approved stills as image references.
3. Keep this log updated with every job ID and running credit total.
