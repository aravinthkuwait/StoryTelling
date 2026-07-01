# Character Reference Images — generation manifest

Generated with **Higgsfield → Nano Banana Pro** (2K, 16:9, ~2 credits each) from the
reference prompts in `../01_character_bible.md`.

> **Note on storage:** this environment's network policy blocks outbound access to
> Higgsfield's CDN (CloudFront), so the image binaries could not be downloaded into the
> git repo. The images live in the user's **Higgsfield library** and are viewable /
> downloadable there (and were rendered in the Higgsfield widget). This manifest records
> the job IDs so each can be re-displayed with `job_display <id>` or reused as an identity
> reference (`medias:[{value:<job_id>, role:"image"}]`) when generating scene keyframes.

| Character | Job ID | Status | Model |
|---|---|---|---|
| Aravinth | `0eb4348e-4dd8-4cef-9cf0-06bb27b03d12` | completed | nano_banana_pro (2k) |
| Nandini | `85d0664a-2c24-48d6-99d9-0a180e821f3d` | completed | nano_banana_pro (2k) |
| Mirthula | `ba2c60fc-3245-4dfe-a8cd-efff38fecb90` | completed | nano_banana_pro (2k) |
| Hamruthaa | `d4e8468e-5ca0-4823-a59b-c01f7b359aee` | completed | nano_banana_pro (2k) |
| Genie | `563ffaf9-6c81-4345-9621-fac23cd4a5ed` | see note* | nano_banana_pro (2k) |
| Monkey | `22326bbe-7a38-4b72-80c4-27c734908cf5` | completed | nano_banana_pro (2k) |
| Magic Carpet | `b2011e68-510b-48cb-acac-42db647a5839` | completed | nano_banana_pro (2k) |

\* The Genie required re-generation: earlier attempts with a bare blue torso were
auto-flagged by the content filter. The final version is fully robed/turbaned (a
wholesome mascot design) to pass the family-friendly filter.

## Reusing refs for scene keyframes (better consistency)

When generating each scene keyframe, pass the relevant character job IDs as identity
references so faces/costumes stay consistent:

```
generate_image(model="nano_banana_pro", prompt="<shot IMG prompt from 04_generation_prompts.md>",
  medias=[{value:"0eb4348e-...", role:"image"},   # Aravinth
          {value:"d4e8468e-...", role:"image"}])  # Hamruthaa  (etc.)
```

> The user also has **trained character reference elements (Souls)** from a prior project
> (`Aravinth-v2`, `Nandini-v2`, `Mirthula-v2`, `Hamruthaa-v2`). Those lock faces even more
> tightly but use *different costumes* (idli-shop look), so they were not used here; they
> remain an option if face‑lock matters more than matching this film's exact wardrobe.
