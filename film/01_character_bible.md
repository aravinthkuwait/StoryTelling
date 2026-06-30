# 01 — CHARACTER & ASSET BIBLE (STRICT CONSISTENCY)

This is the **single source of truth** for how every character and key prop looks.
Character consistency is a hard requirement of the brief: **same face, hairstyle,
body shape, and costume in every shot.**

## How to use this file

1. **Lock references first.** Before any shot, generate **one canonical reference
   image per character** using the "Reference image prompt" below (cheapest model:
   Nano Banana Pro). Save it as `refs/<name>.png`. This is the character's identity.
2. **Always reuse the reference.** For every shot, pass the saved reference image
   to the generator as an identity/style reference AND paste the character's
   **Consistency block** verbatim into the prompt. Never improvise a new description.
3. **One seed family per character.** Where the tool exposes seeds, keep each
   character on a stable seed (see "Seed" below) so micro‑features stay constant.
4. **Negative prompt** (apply to every generation): `inconsistent face, changing
   age, different hairstyle, wrong costume, extra fingers, deformed hands, warped
   face, plastic skin, dead eyes, text artifacts, watermark, logo, duplicate
   characters, lowres, blurry`.

A "Consistency block" is the short, dense descriptor you paste into prompts. The
"Reference image prompt" is the longer one‑time prompt used only to mint the
reference image.

---

## GLOBAL STYLE TOKEN (paste into every prompt)

> **STYLE:** Disney·Pixar‑style 3D animated realism, ultra‑cinematic 4K UHD, HDR,
> soft volumetric lighting, shallow depth of field, warm South‑Indian color palette
> (saffron, gold, teal, rose), highly expressive faces, detailed luminous eyes with
> catchlights, subsurface‑scattering skin, gentle film grain, 24fps cinematic motion,
> 16:9. Family‑friendly, wholesome, emotional.

Abbreviation used in shot prompts: **`[STYLE]`** = the block above.

---

## 1. ARAVINTH — the father (அரவிந்த்)

- **Role:** Hardworking father, age 35. Believes money matters most; learns better.
- **Seed:** `ARAVINTH‑1001`

**Consistency block (paste verbatim):**
> **ARAVINTH:** a 35‑year‑old Tamil man, warm brown skin, oval face, neat medium‑length
> black beard, thick black eyebrows, kind tired dark‑brown eyes, black‑framed rectangular
> spectacles, short black side‑parted hair, average athletic build, medium height. Wears a
> **light‑blue half‑sleeve casual cotton shirt** (collar, two chest buttons open) and
> **cream chino trousers**, brown leather watch on left wrist, simple brown sandals.

**Reference image prompt (one‑time, Nano Banana Pro):**
> [STYLE] Character reference sheet of ARAVINTH — a 35‑year‑old Tamil man, warm brown skin,
> oval face, neat medium black beard, black‑framed rectangular glasses, short side‑parted
> black hair, kind tired eyes; wearing a light‑blue half‑sleeve cotton shirt and cream chinos,
> brown wristwatch. Neutral grey studio background, soft key light, full‑body and face
> close‑up, T‑pose neutral expression, consistent design turnaround. No text.

---

## 2. NANDINI — the mother (நந்தினி)

- **Role:** Loving, wise mother, age 40. The film's emotional anchor.
- **Seed:** `NANDINI‑1002`

**Consistency block:**
> **NANDINI:** a 40‑year‑old Tamil woman, warm brown skin, soft round‑oval face, gentle
> expressive dark eyes, **black hair mixed with natural grey/white streaks** tied in a low
> bun with a small jasmine flower, small bindi. Wears a **simple elegant cotton saree, teal
> with a thin gold border** over a maroon blouse, modest gold jhumka earrings and thin bangles.
> Calm, warm, motherly posture.

**Reference image prompt:**
> [STYLE] Character reference sheet of NANDINI — a 40‑year‑old Tamil woman, warm brown skin,
> kind round face, black hair with natural grey/white streaks in a low bun with a jasmine
> flower, small bindi, gold jhumka earrings; wearing a teal cotton saree with thin gold border
> over a maroon blouse. Neutral grey studio background, soft light, full‑body and face close‑up,
> neutral warm expression, consistent turnaround. No text.

---

## 3. MIRTHULA — elder daughter (மிர்துலா)

- **Role:** Intelligent, brave 13‑year‑old. Dreamer; later wishes for fame.
- **Seed:** `MIRTHULA‑1003`

**Consistency block:**
> **MIRTHULA:** a 13‑year‑old Tamil girl, warm brown skin, bright curious dark eyes, round
> youthful face, **long straight black hair past her shoulders** (sometimes a thin braid),
> slim child build. Wears a **knee‑length pink cotton frock with short sleeves** and small
> white floral print, white leggings, pink slip‑on shoes. Expressive, lively, brave.

**Reference image prompt:**
> [STYLE] Character reference sheet of MIRTHULA — a 13‑year‑old Tamil girl, warm brown skin,
> long straight black hair past shoulders, bright curious eyes, round youthful face; wearing a
> knee‑length pink cotton frock with tiny white floral print and white leggings. Neutral grey
> studio background, soft light, full‑body and face close‑up, neutral expression, consistent
> turnaround. No text.

---

## 4. HAMRUTHAA — younger daughter (ஹம்ருதா) — the heart of the film

- **Role:** Innocent, kind‑hearted 6‑year‑old. Finds the lamp; makes the wish that matters.
- **Seed:** `HAMRUTHAA‑1004`

**Consistency block:**
> **HAMRUTHAA:** a 6‑year‑old Tamil girl, warm brown skin, big round sparkling dark eyes,
> chubby cheeks, sweet innocent face, **black hair in two high ponytails** tied with small
> red ribbons, small child build. Wears a **bright‑yellow sleeveless frock** with a little
> white collar and a tiny flower, white socks and small white shoes. Curious, giggly, gentle.

**Reference image prompt:**
> [STYLE] Character reference sheet of HAMRUTHAA — a 6‑year‑old Tamil girl, warm brown skin,
> big round sparkling eyes, chubby cheeks, black hair in two high ponytails with red ribbons;
> wearing a bright‑yellow sleeveless frock with white collar. Neutral grey studio background,
> soft light, full‑body and face close‑up, sweet innocent expression, consistent turnaround.
> No text.

---

## 5. GENIE — the Genie (ஜீனி)

- **Role:** Ancient, powerful, funny yet deeply emotional. Comic and wise.
- **Seed:** `GENIE‑1005`

**Consistency block:**
> **GENIE:** a large friendly magical genie with **glowing translucent blue skin**, muscular
> upper body, **no legs — a swirling smoke/wisp tail** instead of legs, bald head with a small
> black topknot and a curled black beard, big expressive golden eyes, broad cartoonish grin.
> Wears **golden ornaments**: thick gold cuffs/bracelets on both wrists, a gold collar‑necklace,
> a jewelled gold earring, a red‑and‑gold sash. Emits soft blue light and floating sparkles.
> Funny, warm, larger than life, very expressive face.

**Reference image prompt:**
> [STYLE] Character reference sheet of the GENIE — a large friendly genie with glowing
> translucent blue skin, muscular torso, swirling blue smoke tail instead of legs, bald head
> with small black topknot and curled beard, big golden eyes, broad grin; gold cuffs, gold
> collar necklace, jewelled earring, red‑gold sash, floating blue sparkles. Dark palace
> background with blue glow, full‑body and face close‑up, friendly expression, consistent
> turnaround. No text.

---

## 6. MONKEY — the monkey (குரங்கு)

- **Role:** Cute, playful, intelligent comic‑relief companion.
- **Seed:** `MONKEY‑1006`

**Consistency block:**
> **MONKEY:** a small cute brown monkey (langur‑like), soft fluffy brown fur, lighter cream
> face and belly, big round amber eyes, long curly tail, expressive eyebrows. Wears a small
> **red scarf** knotted around its neck. Playful, mischievous, intelligent, very expressive.

**Reference image prompt:**
> [STYLE] Character reference sheet of the MONKEY — a small cute brown monkey with soft fluffy
> fur, cream face, big amber eyes, long curly tail, wearing a small red scarf around its neck.
> Neutral background, full‑body and face close‑up, playful expression, consistent turnaround.
> No text.

---

## 7. MAGIC CARPET — the flying carpet (பறக்கும் கம்பளம்)

- **Role:** Sentient flying carpet; gift for the family's adventure.
- **Seed:** `CARPET‑1007`

**Consistency block:**
> **MAGIC CARPET:** a rectangular **red and gold Persian‑style flying carpet** with intricate
> woven floral/paisley patterns, golden tasselled fringe at both ends, and **glowing magical
> golden patterns** that pulse with light. Edges ripple gently as it floats. Subtle sparkle trail.

**Reference image prompt:**
> [STYLE] Reference image of the MAGIC CARPET — a red and gold Persian flying carpet with
> intricate woven paisley patterns, golden tassels, glowing pulsing golden magical lines,
> floating with rippling edges and a faint sparkle trail. Plain dark sky background, three‑quarter
> view. No text.

---

## KEY PROPS & RECURRING SETS (keep consistent)

- **THE LAMP (விளக்கு):** a small antique brass/golden oil lamp, Aladdin‑style with a curved
  spout and a domed lid, ornate engraving, a soft warm glow inside. Dusty when found, gleaming
  after rubbing.
- **THE FAMILY HOUSE:** a small modest South‑Indian village house, white‑washed walls, red‑tiled
  roof, a small front veranda, banana/coconut trees, a tulasi plant in the yard.
- **THE ABANDONED PALACE:** a grand ruined South‑Indian palace, tall stone pillars, broken
  statues, dust motes in golden shafts of light through high windows, cracked floors, vines.
- **THE MANSION (wish 1):** a huge modern luxury mansion, marble floors, chandeliers, glass walls,
  gold décor, luxury cars in the driveway — beautiful but cold and silent.
- **VILLAGE‑TRANSFORMED (wish 3):** the village lush and green, blossoming trees, clean streets,
  smiling well‑fed children and elders, warm golden communal light.

---

## CONSISTENCY CHECKLIST (run on every generated shot)

- [ ] Face matches the reference (same age, features, skin tone).
- [ ] Hair exactly as specified (Hamruthaa = two ponytails + red ribbons; Nandini = grey‑streaked bun; etc.).
- [ ] Costume colors correct (Aravinth blue shirt/cream pants; Hamruthaa yellow frock; Mirthula pink; Nandini teal saree).
- [ ] Body shape/height consistent.
- [ ] Genie always blue with smoke tail + gold ornaments; Monkey always has the red scarf.
- [ ] No extra/duplicate characters, no warped hands, no text artifacts.
- [ ] Lighting and palette match `[STYLE]`.
