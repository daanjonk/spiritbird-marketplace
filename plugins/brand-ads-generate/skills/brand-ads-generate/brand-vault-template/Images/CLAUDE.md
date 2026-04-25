# Images/ — directory conventions

## Folder layout

- **`reference-pack/`** — your brand's canonical anchor images. The model + product + logo locked in 3–6 angles. Use these as `image_urls[1]` in the `brand-ads-generate` skill (they hold character + logo consistency across renders).
- **`Creative ideas/`** — cross-industry inspiration. Drop 3–10 images from any industry (skincare, prestige, hospitality, tech — anything). The skill uses these as `image_urls[0]` to translate aesthetic into your brand context.
- **`Creative ideas/ad-winners/`** *(optional)* — cherry-picked outputs from past runs that you want to keep and re-use as reference material. Promote winners here, not into `reference-pack/` (which stays product-photographic).
- **`ads/`** — run outputs. One folder per generation run, named `<YYYY-MM-DD-HHMM>-<run-name>/`. Each contains a `BRIEF.md` and ratio-specific subfolders (`9-16/`, `4-5/`, `1-1/`).

## Hosted URL tracking — read [hosted-urls.md](hosted-urls.md) BEFORE uploading

**Never re-upload a file that already has a public URL.** Always check [hosted-urls.md](hosted-urls.md) first — it's the single source of truth for local-path → CDN-URL mappings. If a row exists, reuse the URL. If not, run the upload flow you use, then add a row.

Why: the `brand-ads-generate` skill needs public URLs as input to image-to-image models. Each upload costs the round-trip and burns a slot in your CDN. Re-uploading wastes time and pollutes the file pool.

When uploading a new file, follow the procedure documented at the bottom of [hosted-urls.md](hosted-urls.md).

## File naming

- **`reference-pack/`**: numeric-letter prefix sorts canonical originals first (`00-front-original.png`), then alphabetical reference angles (`A-headshot.png`, `B-side-left.png`, `C-side-right.png`, `D-closeup-3q.png`).
- **`Creative ideas/`**: keep the original filename if it carries source attribution (e.g. `prestige-boxing-OOYpHUoU.jpeg`); rename only if the original is opaque (e.g. `inspo-33987.png` — note in `hosted-urls.md` what it is).
- **`ads/`**: skill-managed. Don't rename outputs — the BRIEF.md cross-references them by path.

---

*See the parent [CLAUDE.md](../CLAUDE.md) for the brand-vault routing table.*
