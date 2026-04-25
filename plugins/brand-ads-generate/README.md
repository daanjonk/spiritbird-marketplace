# brand-ads-generate

A Claude Code skill that turns your brand context + cross-industry inspiration into on-brand paid ad creative — with on-image CTA copy rendered inline by an image-to-image model.

> One brand-context prompt + many inspiration references = many on-brand visual interpretations. The model does the creative translation; you control the brand voice and the references.

The skill is brand-agnostic. Drop it into any workspace, answer ~7 onboarding questions about your brand, drop a few reference + inspiration images on disk, and you're generating ads.

---

## Install (via SpiritBird marketplace)

```bash
# If you don't already have the marketplace:
/plugin marketplace add daanjonk/spiritbird-marketplace

# Install brand-ads-generate AND its required image-generation backend:
/plugin install brand-ads-generate@spiritbird-marketplace
/plugin install kie-ai@spiritbird-marketplace
```

The `kie-ai` plugin provides the image-generation MCP this skill calls. After installing it, you'll be prompted for a Kie AI API key (get one at [kie.ai/api-key](https://kie.ai/api-key)) and it's stored in your system keychain. Restart your Claude session so the MCP connection initializes.

If you already have the marketplace installed and just want this new plugin:

```bash
/plugin marketplace update spiritbird-marketplace
/plugin install brand-ads-generate@spiritbird-marketplace
```

---

## Hosting prerequisite

The skill never uploads images — it reads a local-path → public-URL map you maintain in `Images/hosted-urls.md`. Use whatever hosting you already have:

- **Shopify Files** (built-in if you use the `shopify-blog-publisher` or `ai-product-images` plugins)
- **Cloudinary** / **S3** / **R2** / **imgur** / **personal CDN** — anything that gives a stable public URL

The skill is hosting-agnostic.

---

## 5-minute quickstart

1. **Pick a workspace folder for your brand.** `cd` into it.
2. **Invoke the skill:** ask Claude something like *"generate ads"*, *"create ad variations for my brand"*, or *"make me 5 static ads"*.
3. **First-run onboarding** kicks in if there's no `Brand/` folder. ~7 questions:
   - Brand name + one-liner
   - Visual signature (accent hex, on-image typeface, accent rule)
   - Ideal customer (2–3 sentences)
   - Voice in one line
   - 5–10 verbatim customer quotes (paste from reviews / Reddit / comments)
   - 3–5 forbidden words/phrases
   - The "good ad" rule — the one line that, if broken, the ad failed
4. **The skill writes your brand vault** to disk (mirrors the structure in `skills/brand-ads-generate/brand-vault-template/`).
5. **Drop in images.** Save 3–6 brand anchor images into `Images/reference-pack/` and 3–10 cross-industry inspiration images into `Images/Creative ideas/`. Get them onto a public URL using whatever hosting you use, and add the rows to `Images/hosted-urls.md`.
6. **Re-invoke the skill.** The vault now exists, so it skips onboarding and goes straight into the generation flow: pick source image(s) → pick CTA mode (auto / user-supplied) → pick aspect ratio(s) → pick image model → confirm cost → generate.
7. **Outputs** land in `Images/ads/<YYYY-MM-DD-HHMM>/` with a `BRIEF.md` describing every variant.

---

## Philosophy

This skill is the operational form of the workflow documented in [`Ad-Generation-Method.md`](skills/brand-ads-generate/Ad-Generation-Method.md). Read that file first if you want to understand *why* the skill is designed the way it is. The short version:

> One brand-context prompt + many inspiration references = many on-brand visual interpretations.

You don't prescribe the scene. You prescribe *who you are* and let the model figure out how to visualize you in the style of the inspiration.

---

## What the skill does NOT do

- **Does not upload images** — bring your own hosting; the skill is read-only against `Images/hosted-urls.md`.
- **Does not run video / Reels / TikTok scripts** — static creative only.
- **Does not audit ad performance** — out of scope.
- **Does not work for multiple brands at once** — one workspace = one brand.

---

## Companion plugins in this marketplace

- **`kie-ai`** — required. Provides the image-generation MCP.
- **`ai-product-images`** — complementary. Generates new product photography from scratch (vs. brand-ads-generate which produces ad creative from existing reference images).
- **`shopify-blog-publisher`** — uses the same Kie AI backend for blog featured images.

---

## License

MIT — see the [marketplace LICENSE](../../LICENSE) (if present), or treat as MIT for individual reuse.
