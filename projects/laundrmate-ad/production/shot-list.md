# Laundrmate Ad — Shot List & Higgsfield Generation Plan

Clips must be generated and saved in **exact numerical order**. Filenames are
fixed — the Colab merge notebook concatenates them by sorted filename.

## Credit budget — HARD CAP: 800 credits total

| Stage | Model | Clips | Cost |
|---|---|---|---|
| Character/location reference stills | Nano Banana Pro (~2 cr) | 8 stills (family, executive, shop interior, storefront, hero garments) | ~16 |
| Draft motion tests | Wan 2.5 Fast (~9 cr) | 11 AI clips (all except 03, 12, 14) | ~99 |
| Final render — hero realism | Google Veo 3 (~58 cr) | 7 clips: 01, 04, 06, 07, 08, 10, 13 | ~406 |
| Final render — standard | Google Veo 3 Fast (~22 cr) | 4 clips: 02, 05, 09, 11 | ~88 |
| 3D text/UI clips in post (FFmpeg/motion graphics) | — no generation | 3 clips: 03 (app UI), 12 (offer card), 14 (final CTA) | 0 |
| **Committed subtotal** | | | **~609** |
| Retry reserve (draft re-rolls, up to ~3 Veo 3 re-renders) | | | ~191 |
| **Total** | | | **≤ 800** |

Rules:

- Full Veo 3 is reserved for the clips where machine/human realism carries the
  ad (opening, pickup, washing, drying, ironing, delivery). Never for drafts.
- Clips 03, 12 and 14 are pure 3D interface/text per the direction — build them
  as real motion graphics in post instead of AI generation. This costs zero
  credits and guarantees pixel-exact text (phone number, offer dates, services
  list), which AI video cannot reliably produce.
- Draw from the retry reserve only after a clip fails the continuity checklist;
  if the reserve runs low, downgrade remaining retries to Veo 3 Fast or Kling
  3.0 (~8–10 cr) before touching full Veo 3 again.
- Track spend after every batch with the Higgsfield balance tool; stop and
  re-plan if committed + spent would exceed 800.

Batch parallel generations to maximise concurrent slots.

## Continuity anchors (reuse in every relevant prompt)

- **Storefront:** illuminated signboard reading exactly `LAUNDRMATE` with
  `The Laundry Company` beneath. Never regenerate with altered spelling.
- **Family:** mother (30s), daughter (~8, school-age), father (office wear),
  grandmother (cotton/silk saree). Same faces and clothing all day.
- **Delivery executive:** one man, Laundrmate-branded uniform + branded delivery
  bike. Same person for pickup (morning) and delivery (evening).
- **Hero garments (tagged, tracked through every stage):** daughter's school
  uniform, father's light-blue office shirt, grandmother's silk saree. Plus
  curtains, mats, shoes.
- **The bag:** one branded laundry bag — identical at home handover and shop
  arrival.
- **Shop interior:** one consistent layout — front counter, sorting tables with
  tagged baskets, washer row, dryer row, ironing stations, packing bench,
  separate shoe/mat area.
- **Light:** morning (clips 01–05), midday (clips 06–11), late afternoon /
  evening (clips 12–14).

## Clips

| # | File | Time | Scene | Content summary | Match cut OUT |
|---|---|---|---|---|---|
| 01 | `clip_01_opening_banner.mp4` | 0–4s | 1 | 1s premium 3D logo reveal → close-up of illuminated LAUNDRMATE banner → fast push-in through entrance → staff opening shop, clean organised machines/counters/racks | Folded garments on shop rack → |
| 02 | `clip_02_customer_need.mp4` | 4–9s | 2 | Match cut to garments at family home. School uniform, office shirt, saree, curtains, mats, shoes laid out. Daughter asks about tomorrow's uniform; mother opens phone. No flying clothes | Mother's phone screen → |
| 03 | `clip_03_booking.mp4` | 9–13s | 3 | Clean 3D phone UI: `Book Pickup` → `Pickup Confirmed` → `Free Doorstep Pickup` → `Call or WhatsApp: 98847 12121` | App confirmation → delivery bike |
| 04 | `clip_04_pickup.mp4` | 13–18s | 4 | Branded bike arrives, rider parks safely, greets customer, tags orders, garments placed separately in branded bag. ONE continuous movement: handover → close bag → lift → onto bike → rides off. Digital confirmation shown | Bag on bike riding away → |
| 05 | `clip_05_receiving_sorting.mp4` | 18–23s | 5 | SAME bag arrives at shop. Tag scanned. Sorting: whites / colours / delicates / sarees separated; shoes+mats to different area; curtains separate; tagged baskets per order; care labels checked | Sorted basket carried toward washer → |
| 06 | `clip_06_washing_load.mp4` | 23–27s | 6a | Realistic sequence: door opened → sorted uniforms/shirts loaded → detergent measured → settings selected → door closed → machine starts | Drum starts turning → |
| 07 | `clip_07_washing_montage.mp4` | 27–31s | 6b | Quick shots: tumbling through glass (clean water, controlled foam); curtains in larger machine; mats in heavy-duty area; shoes brushed separately; dry-cleaning station distinct | Washing drum → dryer drum |
| 08 | `clip_08_drying.mp4` | 31–36s | 7 | Cycle ends, careful unloading. Tumble dryer drum turning; sarees air-dried; curtains separate; shoes on drying rack; mats separate. Employee checks temperature + timer. Short time-lapse for drying time | Dryer door → ironing board |
| 09 | `clip_09_dryclean_saree.mp4` | 36–41s | 8 | Silk saree inspection, dry-cleaning treatment, saree roll polishing, saree pre-pleating, blazer care. Close-ups of hands checking fabric and stains | Finished saree → ironing station |
| 10 | `clip_10_steam_ironing.mp4` | 41–47s | 9 | Professional ironing table: check garment → position shirt → steam iron, wrinkles release → collar and sleeves pressed → hung/folded. Saree with temperature control; school uniform sharp finish. Iron always in human hands | Folded shirt → packed shirt |
| 11 | `clip_11_qc_packing.mp4` | 47–52s | 10 | Stain inspection, button/zip check, perfect folding, individual packing, name + order number labels, packed into clean delivery bag, checked against digital list | Packed bag → offer card |
| 12 | `clip_12_offer_card.mp4` | 52–55s | 11 | Premium 3D offer card, exact wording: SPECIAL OFFER FOR CASAGRAND ASTA CUSTOMERS / 10% OFF ON DRY WASH / FOR ORDERS ABOVE ₹500 / VALID FROM 31-07-2026 TO 07-08-2026. Dates fully visible | Offer card → bag on bike |
| 13 | `clip_13_delivery.mp4` | 55–58s | 12 | Same executive collects packed order, secures on bike, rides to home (late-afternoon light). Family receives: packed uniform, ironed shirt, clean saree, curtains, shoes/mats. Daughter in uniform, father in shirt, grandmother checks saree. Natural satisfaction, no exaggeration | Happy family → montage |
| 14 | `clip_14_final_cta.mp4` | 58–60s | 13 | Fast montage (storefront, washer, dryer, iron, packed order, bike, customer) → 3D logo + full CTA text block: services list, 5 BRANCHES, FREE PICKUP & DELIVERY, CALL OR WHATSAPP 98847 12121, www.laundrmates.com | End |

Total: 60s. Average internal shot length 1.5–3s.

## Prompting rules for every clip

Append to each generation prompt:

- "Realistic commercial cinematography, no fantasy effects, no floating
  clothes, machines and garments behave physically correctly."
- Negative/exclusion guidance: frozen frames, black frames, distorted machine
  doors or controls, foam outside machines, duplicate people, morphing faces,
  text artefacts.
- On-screen text clips (03, 12, 14): text must be pixel-exact. If a generation
  misspells anything, regenerate or overlay clean typography in post — never
  ship AI-mangled text.
- Reference the locked character/location stills (image-to-video) for clips
  containing the family, executive, or shop so identities stay consistent.

## Draft → final workflow

1. Generate reference stills (Nano Banana Pro) → approve identities.
2. Generate the 11 AI clips as drafts (Wan 2.5 Fast), in parallel batches;
   build clips 03, 12 and 14 as motion graphics in post (zero credits).
3. Review against `continuity-checklist.md`; regenerate failures as drafts,
   drawing from the retry reserve.
4. Only after the full 14-clip sequence plays as one continuous story:
   re-render approved clips at final quality — Veo 3 for the 7 hero clips,
   Veo 3 Fast for the 4 standard clips — staying under the 800-credit cap.
5. Merge with the Colab notebook; mux the three language VO tracks.
