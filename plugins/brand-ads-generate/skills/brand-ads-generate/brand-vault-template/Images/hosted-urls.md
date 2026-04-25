# Hosted Image URLs

This file is the single source of truth for which local images have already been uploaded to a public CDN. **Always check here before staging a new upload** — if a local file already has a URL listed below, reuse the URL instead of running the upload flow again.

The `brand-ads-generate` skill reads this file (read-only) to map local image paths to the public URLs it passes to the image-to-image model.

> **Hosting is your choice.** The skill is hosting-agnostic. Use whatever you have — Shopify Files, Cloudinary, S3, imgur, even a personal CDN. The only requirement is a stable public URL the image model can fetch from.

---

## reference-pack/ — character + product source-of-truth

| Local file | Public URL | Uploaded |
|---|---|---|
| `<!-- TODO: e.g. reference-pack/00-front-original.png -->` | `<!-- TODO: e.g. https://cdn.shopify.com/.../front.png -->` | `<!-- TODO: YYYY-MM-DD -->` |
| | | |

## Creative ideas/ — cross-industry inspiration references

These are NOT for promotion — only fed to the image-to-image model as inspiration for visual style, composition, mood, color palette. The skill instructs the model to use them for *style only* and to ignore their text/logos/products.

| Local file | Public URL | Uploaded |
|---|---|---|
| `<!-- TODO -->` | `<!-- TODO -->` | `<!-- TODO -->` |
| | | |

## Creative ideas/ad-winners/ — cherry-picked past outputs

Outputs from past `brand-ads-generate` runs that you've promoted into the reference pool because they tested well and you want to use them as anchor references for future runs.

| Local file | Public URL | Uploaded |
|---|---|---|
| `<!-- TODO -->` | `<!-- TODO -->` | `<!-- TODO -->` |
| | | |

---

## Upload procedure (when adding a new file)

1. Confirm the file isn't already in a table above. If it is, reuse the URL. Don't re-upload.
2. Run whatever upload flow you use. Examples:
   - **Shopify Files** — `shopify-image-host` skill if you have it, otherwise the `stagedUploadsCreate` → POST → `fileCreate` flow.
   - **Cloudinary** — `cloudinary uploader.upload(path)` via SDK or web UI.
   - **S3 / R2 / spaces** — your usual `aws s3 cp` or web console.
   - **imgur** — drag-and-drop via web UI; copy the direct link (right-click → "copy image URL", make sure it ends in `.png` / `.jpg`).
   - **Personal CDN / static site** — `scp` and copy the public URL.
3. Add a row to the relevant table above with:
   - The local path (relative to the workspace root)
   - The returned public URL
   - Today's date in `YYYY-MM-DD` format
4. Do not commit URLs that require auth — the image model needs unauthenticated GET access.

The `brand-ads-generate` skill reads this file but never writes to it. All updates are manual.
