# Ad Generation Method — Cross-Industry Inspiration → On-Brand Creative

A universally applicable workflow for turning visual inspiration from *any* industry into on-brand ad creative for *your* brand, using an image-to-image model. The model does the creative interpretation; you control the brand context and the references.

---

## Folder structure

```
your-workspace/
├── Brand/                              ← who you are (read by you, distilled into prompts)
│   ├── positioning.md
│   ├── customer-voice.md               ← verbatim customer quotes — high-leverage
│   ├── visual-rules.md                 ← color/typography/logo non-negotiables
│   └── ad-playbook.md                  ← what makes a "good" ad for you
│
├── reference-pack/                     ← your brand's canonical anchor images
│   └── brand-anchor.png                ← always passed as image_urls[1]
│                                          (your model + product + logo, locked)
│
├── Creative ideas/                     ← drop inspiration images here
│   ├── inspiration-1.jpg               ← from any industry — skincare, perfume,
│   ├── inspiration-2.jpg                  tech, hospitality, anything
│   └── inspiration-N.jpg
│
├── Creative ideas/ad-winners/          ← cherry-picked outputs you keep
│   ├── winner-1.png                       (and re-host on CDN for future use)
│   └── winner-N.png
│
├── ads/                                ← run outputs (one folder per generation run)
│   └── YYYY-MM-DD-HHMM-<run-name>/
│       ├── BRIEF.md                    ← what was generated and why
│       └── 9-16/                       ← outputs grouped by aspect ratio
│           └── *.png
│
└── hosted-urls.md                      ← single source of truth: local file → CDN URL
                                           (never re-upload a file already in this table)
```

---

## The 7 steps

### 1. Read the brand context
Open the files in `Brand/` and identify what's load-bearing for ads: positioning one-liner, customer voice quotes (verbatim is gold), visual non-negotiables, the "good ad" definition. You will compress these into a single prompt block in step 4.

### 2. Collect cross-industry inspiration
Drop 3–10 visual reference images into `Creative ideas/`. They can be from any industry. What you're collecting is *aesthetic ideas*: composition, color palette, character pose energy, text treatment, layout — not products or copy.

### 3. Host inspiration images on a CDN
Image-to-image models need public URLs, not local files. Upload each inspiration image to a CDN (Shopify Files, Cloudinary, S3 — whichever you use) and add the resulting URL to `hosted-urls.md`. Re-uploading wastes time and pollutes your file pool — always check the table first.

### 4. Write ONE brand-context prompt
Write a single prompt template you'll reuse across every generation. The structure that works:

```
BRAND: <one-paragraph who you are, what you sell, what makes you different,
        customer voice quotes, visual signature, positioning vs competitors>

REFERENCES:
- Image 1 (inspiration): use ONLY for visual style, composition, mood,
  color palette, pose energy, layout, on-image text treatment.
  Do NOT reproduce its text, logos, brand names, or characters.
- Image 2 (brand anchor): your model + product + logo. Use as the
  brand anchor. You decide framing, pose, scene, composition.

GOAL: stop the scroll. Be bold. Surprise me. You decide how to visualize this.
9:16 vertical (or whatever ratio).
```

The same prompt is reused for every generation in the run — only the inspiration image changes. This is the experiment: same brand context + different aesthetics = different on-brand interpretations.

### 5. Generate
For each inspiration image, call the image-to-image model with **two reference URLs**:

```
image_urls[0] = inspiration URL    (style/mood/layout)
image_urls[1] = brand anchor URL   (model/product/logo)
```

Order matters — earlier references weight slightly higher for visual style. Inspiration first, brand anchor second.

Fire all generations in parallel; they're independent. Poll for completion, download outputs to `ads/<timestamp-run-name>/`.

### 6. Cherry-pick winners
Review every output. Pick the 1–6 that actually stop the scroll. Be ruthless — most will be near-misses, and that's fine.

### 7. Save winners + clean up
- Move winners to `Creative ideas/ad-winners/`
- Upload winners to the CDN (so they can become anchor references for future runs)
- Add rows to `hosted-urls.md`
- Delete the rest of the run folder

Winners now live in two places: on disk for review, on the CDN for reuse.

---

## What makes this work

> **One brand-context prompt + many inspiration references = many on-brand visual interpretations.**

The image model does the creative translation. You don't prescribe the scene — you prescribe *who you are* and let the model figure out how to visualize you in the style of the inspiration.

The brand-context prompt is doing real work, not decoration: when written well, the model will pull verbatim customer-voice lines into headlines, respect color rules unprompted, and place your logo correctly — none of which were specifically requested in the prompt.

---

## Prompt-template anchor (what NOT to do)

- ❌ Don't prescribe the scene yourself ("model running on a rooftop at sunset"). You become the bottleneck.
- ❌ Don't let the inspiration's text/logo/products leak into your output. Be explicit: "use ONLY for style."
- ❌ Don't change the brand-context prompt between runs. Same prompt every time = clean comparison of inspiration sources.
- ❌ Don't anchor to your own previous outputs as reference. They cause regression-to-the-mean. Anchor to the raw cross-industry source.

---

## Recommended model

- **Default:** `gpt-image-2-image-to-image` — strongest on-image text rendering, character consistency.
- **Fidelity-first alternative:** `nano-banana-pro` — sharper output, supports up to 8 references, higher cost.
- **UGC-mood alternative:** `seedream/5-lite-image-to-image` — most photorealistic for natural lifestyle scenes, weaker on long text.

Always ask the user which model to use. Never silently default.
