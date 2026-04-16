---
name: ai-product-images
description: Generate AI product images and upload them to Shopify products. Uses Kie AI for image generation (SeeDream 5 Lite, Flux 2 Pro) and the Cloudinary MCP for sourcing product reference photos. For existing Shopify products, uses the product's existing Shopify CDN images as reference; for new products, sources reference images from Cloudinary. Use this skill whenever the user wants to create product photos, generate product images, add images to Shopify products, replace product photos, create studio-style product shots, create UGC-style content, or says things like "generate images for my products", "create product photos", "add AI images to Shopify", "make product pictures", "studio shots for products", "UGC images", "mirror selfie shots", "lifestyle product photos", or any variation of wanting AI-generated imagery for Shopify products. Also trigger when the user mentions product images in combination with Kie AI, Cloudinary, or Shopify.
---

# AI Product Image Generator for Shopify

Generates clean, studio-style AI product images and uploads them directly to Shopify products.

---

## Setup (REQUIRED — do this before first use)

Before using this skill, you need to configure three things in `scripts/config.py`:

### 1. Shopify Store Credentials

Create a custom app in your Shopify admin (Settings → Apps → Develop apps):

| Field | Where to find it |
|-------|-----------------|
| `STORE` | Your myshopify.com domain (e.g. `my-brand.myshopify.com`) |
| `CLIENT_ID` | Custom app → API credentials → Client ID |
| `CLIENT_SECRET` | Custom app → API credentials → Client secret (starts with `shpss_`) |

**Required app scopes**: `read_products`, `write_products`, `write_files`

### 2. Cloudinary (product reference images)

You need the [Cloudinary MCP connector](https://www.cloudinary.com/) installed in your Claude environment.

| Field | Where to find it |
|-------|-----------------|
| `CLOUDINARY_CLOUD_NAME` | Cloudinary Dashboard → Cloud name |
| `CLOUDINARY_PRODUCT_FOLDER` | The folder in Cloudinary where you store product photos (default: `"Shopify product images"`) |

### 3. Model Reference Images (optional — for model+product shots)

If you want AI-generated photos of a model wearing/holding your products:

1. Upload 2-3 photos of your model to Shopify Files (Settings → Files)
2. Copy the permanent CDN URLs
3. Add them to `MODEL_REFS` in `config.py`

Leave `MODEL_REFS` empty if you only need product-on-white-background shots.

### 4. Kie AI (image generation)

Kie AI is accessed via its MCP tool — no API key needed in config. Just make sure the Kie AI MCP connector is installed in your Claude environment.

---

## Modes

Four modes available, in order of preference:

1. **Mode A — Model + Product (best)**: Combines model reference images + product image → model wearing the product. Gives character consistency across the whole store.
2. **Mode B — Image-to-image (good)**: Takes existing product photo and recreates it on a white background. Keeps the actual product accurate.
3. **Mode C — Text-to-image (fallback)**: Generates from product description only. Use when no existing image is available. Won't match the real product.
4. **Mode D — UGC Style**: Generates user-generated-content-style images (mirror selfies, lifestyle shots). Authentic social media feel rather than polished studio look.

Always prefer Mode A when model references are configured and the product is wearable/displayable on a model. Fall back to Mode B for non-wearable products or when no model is set up. Mode C is the last resort for products with no existing photo. Use Mode D when the goal is social media content or an authentic UGC aesthetic rather than traditional ecommerce photography.

---

## CRITICAL: Product Image Reference is MANDATORY

The generated image must be 100% identical to the provided input image — same color, same fabric, same pattern, same design. AI image models will always drift on color, shade, and texture when working from text descriptions alone. The only reliable way to prevent this is to include the actual product photo as a reference image in every Kie AI call.

**The rule: if a product photo exists (in Cloudinary, provided by user, or already on Shopify), it MUST be included as a reference image in the Kie AI call. Never generate from text description alone when a photo is available.**

Why this matters: without the real photo as a visual anchor, the AI interprets "beige" as whatever shade it imagines. The result looks plausible but doesn't match the actual product — and that's unacceptable for ecommerce where customers expect to receive exactly what they see.

### Step 0: Get a public URL for the product photo (before any generation)

Kie AI requires publicly accessible image URLs. Before generating anything, make sure you have a URL for the product photo.

**Which route to use depends on whether the product already exists on Shopify:**

- **Product already exists on Shopify** → Start with Route A (Shopify images). The product likely already has photos on its CDN — use those as the reference.
- **New product (not yet on Shopify)** → Start with Route B (Cloudinary). The reference images live in the Cloudinary product images folder.

**Route A — Product already exists on Shopify (preferred for existing products):**

Use `get-product` to retrieve the product's existing image CDN URLs:
```bash
python3 <skill-path>/scripts/shopify_products.py get-product --token "<token>" --product-id <id>
```

The response includes image URLs hosted on Shopify's CDN (`cdn.shopify.com`). These are permanent, public, and immediately usable — pass them directly to Kie AI. Pick the clearest/most representative image as the reference.

If the existing product has no images, fall through to Route B (Cloudinary) or Route C (user-provided).

**Route B — Product image is in Cloudinary (preferred for new products):**

Search the product images folder in Cloudinary (folder name configured in `config.py` as `CLOUDINARY_PRODUCT_FOLDER`):

```
mcp__Cloudinary_Asset_Management__search-assets({
  "request": {
    "expression": "folder:\"Shopify product images\"",
    "max_results": 50,
    "with_field": ["context", "tags"]
  }
})
```

Each result includes a `secure_url` — that's your permanent public HTTPS URL. Match the product by `display_name` (which corresponds to the product name) or `filename`. Pass the `secure_url` directly to Kie AI.

To find a specific product image by name:
```
mcp__Cloudinary_Asset_Management__search-assets({
  "request": {
    "expression": "folder:\"Shopify product images\" AND display_name:\"<product name>\"",
    "max_results": 5
  }
})
```

The `secure_url` from the response is immediately usable — no shared links, no expiry, no cleanup.

**Route C — User provides a file or image inline:**
Upload it to Cloudinary first so you have a permanent URL:

```
mcp__Cloudinary_Asset_Management__upload-asset({
  "upload_request": {
    "file": "<url-or-base64>",
    "asset_folder": "Shopify product images",
    "display_name": "<product name>",
    "use_filename_as_display_name": false
  }
})
```

The response includes `secure_url` — use that for the Kie AI call. This also stores the image in the product images folder for future use.

If the image only exists inline in the conversation (no file path, no URL), ask the user to re-upload as a file attachment so you can use Route C. If that's not possible, use text-to-image as fallback — but explicitly warn: "I don't have the product photo as a file, so colors and details may not match exactly."

Never silently fall back to text-only generation. Always inform the user when you can't use their product photo as reference.

### Image URL ordering in the Kie AI call

When combining model references with a product image, the product image always goes LAST — this position gets the strongest "preserve this" signal from the prompt:
```python
image_urls = [
    MODEL_REF_1,   # model angle 1
    MODEL_REF_2,   # model angle 2
    "<PRODUCT_IMAGE_URL>"  # actual product photo (Shopify CDN or Cloudinary) — ALWAYS LAST
]
```

### Post-generation verification

After every generation, visually compare the output against the input reference before showing to the user:
- **Color**: Exact same shade? Not lighter, darker, warmer, or cooler.
- **Pattern/print**: Same stripes, florals, solids, textures?
- **Fit/silhouette**: Does the garment shape match the original?
- **Details**: Belt loops, pockets, buttons, stitching — all present?

If any of these don't match, regenerate. Do not upload or present mismatched images to the user.

---

## Model Reference Images (Character Consistency)

The store uses permanent model reference images hosted on Shopify Files (CDN). These give consistent character appearance across all product photos.

### Current model reference URLs

Configured in `scripts/config.py` as `MODEL_REFS`. Example:

```python
MODEL_REFS = [
    "https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/model_front.png?v=...",
    "https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/model_side.png?v=...",
]
```

These must be permanently hosted on Shopify CDN (they won't expire). They show the same model from different angles.

### How to update model reference images

If the user wants to change the model:
1. Upload new model photos to Shopify Files (Settings → Files in the admin, or via the GraphQL API — see `scripts/shopify_products.py upload-file`)
2. Get the permanent CDN URLs from Shopify
3. Update `MODEL_REFS` in `scripts/config.py`

Ideal model reference set: 2-3 images showing the model from different angles, with clear face visibility. The more angles, the better the consistency.

---

## The Flow

```
1. Browse Products
   → List products from the Shopify store, pick which ones need images
2. Ask: Draft or Live?
   → Before generating anything, ask the user: "Should I upload images as draft or publish them live?"
   → This is the ONLY question to ask upfront. After this, proceed without interruption.
3. Get Product Reference Image
   → Existing product: use Shopify CDN image URLs from get-product
   → New product: search Cloudinary product images folder → get secure_url
4. Choose Mode
   → Mode A: Model+Product if model refs exist and product is wearable
   → Mode B: Image-to-image if product has existing photos but isn't wearable
   → Mode C: Text-to-image only if no existing photo available
   → Mode D: UGC Style for social media / lifestyle content
5. Choose Model (see "Choosing the right model" below)
   → Default: SeeDream 5 Lite image-to-image, quality "basic", image_urls for reference images
6. Generate Image(s) (Kie AI)
   → Generate sequentially when multiple images needed (see "Multi-Image Consistency")
   → Poll every 30 seconds — generation takes 150–250 seconds per image
7. Upload to Shopify
   → Upload immediately after generation — no review gate, no "does this look good?" prompt
   → Respect the user's draft/live choice from step 2
```

---

## Phase 1: Browse Products

Use the `scripts/shopify_products.py` script for all Shopify API calls.

### Step 1: Get a fresh access token

```bash
python3 <skill-path>/scripts/shopify_products.py auth
```

Tokens expire every 24 hours, so always start with a fresh one.

### Step 2: List products

```bash
python3 <skill-path>/scripts/shopify_products.py list-products --token "<token>" --limit 20
```

Optional filters:
- `--title "search term"` — find specific products
- `--collection-id <id>` — filter by collection

To browse collections first:
```bash
python3 <skill-path>/scripts/shopify_products.py list-collections --token "<token>"
```

### Step 3: Get full product details

For each selected product:
```bash
python3 <skill-path>/scripts/shopify_products.py get-product --token "<token>" --product-id <id>
```

---

## Phase 1.5: Get Product Reference Image

Before generating, you need a reference image URL. The source depends on whether the product already exists on Shopify (see Step 0 for the full routing logic).

### For existing Shopify products (Route A)

You already retrieved the product in Phase 1 via `get-product`. Use the image CDN URLs from that response — no extra step needed. Pick the clearest/most representative image.

### For new products without Shopify images (Route B — Cloudinary)

Search the product images folder in Cloudinary (folder name from `config.py`):

```
mcp__Cloudinary_Asset_Management__search-assets({
  "request": {
    "expression": "folder:\"Shopify product images\"",
    "max_results": 50,
    "with_field": ["context", "tags"]
  }
})
```

Each result has:
- `display_name` — the human-readable product name (e.g. "Bali Blue Set")
- `secure_url` — the permanent public HTTPS URL to pass to Kie AI
- `width`, `height` — image dimensions
- `format` — file format (jpg, png, etc.)

### Find a specific product image in Cloudinary

Search by display name to match against a product:
```
mcp__Cloudinary_Asset_Management__search-assets({
  "request": {
    "expression": "folder:\"Shopify product images\" AND display_name:\"<product name>\"",
    "max_results": 5
  }
})
```

If there's no matching image in Cloudinary and the Shopify product has no images either, fall back to Mode C (text-to-image) with a warning to the user.

---

## Phase 2: Generate Image (Kie AI)

### Mode A: Model + Product (DEFAULT for wearable products)

This is the primary mode for apparel, accessories, and anything a model can wear/hold. It passes the model reference images + the product image to the AI, which generates the model wearing the actual product.

#### Step 1: Prepare the image URLs array

You MUST have a product image URL at this point (Cloudinary `secure_url` or Shopify CDN URL — see Step 0). If you don't, stop and get one first.

Pass the model references first, then the product image last (use `MODEL_REFS` from `config.py`):

```python
from config import MODEL_REFS

image_urls = [
    *MODEL_REFS,              # model angles (2-3 images)
    "<product_image_url>"     # the actual product (Shopify CDN or Cloudinary) — REQUIRED, ALWAYS LAST
]
```

The AI can handle up to 5 images total (max from Kie AI). Use 2 model refs + 1 product image. If the product has multiple images, pick the clearest/most representative one. The product image in the last position is what the AI will try to preserve.

#### Step 2: Craft the prompt

The prompt needs to tell the AI to combine the model with the product. Always emphasize keeping both the model and product accurate.

**Template for model wearing product:**
```
The woman from the first three reference images wearing the EXACT [PRODUCT NAME] shown in the last image. The [product] must be pixel-perfect identical to the last reference image — same exact color, same exact shade, same print, same pattern, same fabric texture, same design details. Do NOT alter the product in any way. Same model — same face, same body type. She is wearing the exact [product] and appropriate stylish shoes that match the outfit. Full body standing pose, clean pure white background, professional ecommerce product photography, soft studio lighting. No text, no watermark.
```

The explicit reference to "the last image" tells the AI which reference to preserve. Without the product photo as reference, the AI will invent its own interpretation of colors and textures — this is why Step 0 (getting a reference URL) is non-negotiable.

**Variations by product type:**
- **Tops/Jackets**: `...wearing the EXACT [product]. Styled with simple bottoms and appropriate shoes. Focus on the top.`
- **Bottoms/Pants**: `...wearing the EXACT [product]. Styled with a simple top and appropriate shoes. Focus on the bottoms.`
- **Dresses**: `...wearing the EXACT [product]. Full body shot showing the complete dress with appropriate stylish shoes.`
- **Accessories (bags, jewelry)**: `...holding/wearing the EXACT [product]. Focus on the accessory. Appropriate shoes and simple outfit.`
- **Full outfits**: `...wearing the EXACT outfit. Show the complete look with appropriate shoes.`

Always include:
- "Do NOT change the product in any way — keep the exact same print, pattern, colors, fabric, and design"
- "appropriate stylish shoes that match the outfit"
- "clean pure white background, professional ecommerce product photography, soft studio lighting. No text, no watermark."

#### Step 3: Generate

Default model: **SeeDream 5 Lite image-to-image** (`seedream/5-lite-image-to-image`) with `quality: "basic"` (= 2K output). Always pass reference images via `image_urls` (array of strings).

**Budget alternative:** Flux 2 Pro (`flux-2/pro-image-to-image`) at roughly half the cost.

```json
{
  "model": "seedream/5-lite-image-to-image",
  "prompt": "<your prompt>",
  "image_urls": ["<model_ref_1>", "<model_ref_2>", "<product_image_url>"],
  "quality": "basic",
  "aspect_ratio": "1:1"
}
```

Poll for completion:
```
mcp__kie-ai__kie_get_task_status(task_id="<task_id>")
```

Image generation typically takes **150–250 seconds** (2.5–4 minutes). Poll every **30 seconds** — not faster. The model needs time to process reference images and produce high-quality output, so rapid polling just wastes API calls. Start your first poll ~30 seconds after submission, then repeat every 30 seconds until complete.

---

### Mode B: Image-to-Image (for non-wearable products or when no model needed)

Takes the existing product photo and transforms it — e.g., swaps to a white background while keeping the product accurate.

#### Prompt template

```
Place this exact same product on a clean pure white background. Professional ecommerce product photography, soft studio lighting, slight shadow for depth. Keep the product exactly as it is — same design, same colors, same details. Only change the background to white. No text, no watermark.
```

#### Generate

Default model: **SeeDream 5 Lite image-to-image** (`seedream/5-lite-image-to-image`) with `quality: "basic"`.

**Budget alternative:** Flux 2 Pro (`flux-2/pro-image-to-image`) at roughly half the cost.

```json
{
  "model": "seedream/5-lite-image-to-image",
  "prompt": "<your edit prompt>",
  "image_urls": ["<product_image_url>"],
  "quality": "basic",
  "aspect_ratio": "1:1"
}
```

---

### Mode C: Text-to-Image (FALLBACK — no existing photo available)

The AI invents the product appearance. Won't match reality, but useful for placeholder images or conceptual products.

#### Prompt formula

```
Professional product photography of [PRODUCT NAME]. [PRODUCT DESCRIPTION/KEY FEATURES].
Clean white background, soft studio lighting, slight shadow for depth.
Shot from [ANGLE] angle. High resolution, commercial quality, ecommerce ready.
No text, no watermark, no logos.
```

#### Generate

```json
{
  "model": "seedream/5-lite-text-to-image",
  "prompt": "<your crafted prompt>",
  "quality": "basic",
  "aspect_ratio": "1:1"
}
```

---

### Mode D: UGC Style (social media / lifestyle content)

Generates user-generated-content-style images — mirror selfies, lifestyle shots, casual poses. The goal is authenticity over polish: these should look like real customers sharing their outfit on Instagram, not studio photography.

Use Mode D when the user wants social media content, influencer-style shots, or anything that should feel "real" rather than commercial.

#### When to use which model for UGC

- **Ecommerce store product pages** (UGC look but product accuracy matters) → `seedream/5-lite-image-to-image` basic
- **Instagram / social media** (authentic feel, doesn't need to be pixel-perfect) → `flux-2/pro-image-to-image` or `seedream/4.5-edit`
- **Budget batch** → `flux-2/pro-image-to-image` (half the cost)

#### Prompt approach

UGC prompts differ from studio prompts — emphasize casual, realistic qualities: phone camera, natural light, slight grain, real environments (bedroom, bathroom mirror, café). Avoid studio language ("professional lighting", "white background").

**Example prompt (mirror selfie with model reference + product image):**
```
Casual UGC-style iPhone selfie of the woman from image 1 wearing the outfit from image 2. She's taking a mirror selfie in a well-lit bedroom with natural window light. Relaxed candid pose, slight smile, holding phone up. The clothing must be exactly as shown in image 2 — same colors, same fabric, same design. Realistic phone camera quality, slight grain, not overly polished. No studio lighting, no white background. Authentic social media content vibe.
```

Key elements that make UGC prompts work:
- "iPhone selfie" or "phone camera" — sets the realism tone
- "mirror selfie" / specific setting — grounds the scene
- "natural window light" — avoids studio feel
- "slight grain, not overly polished" — prevents the AI from over-beautifying
- Still include the product accuracy instructions — UGC doesn't mean sloppy product representation

#### Generate

**With model reference + product image (recommended):**
```json
{
  "model": "seedream/5-lite-image-to-image",
  "prompt": "<your UGC prompt>",
  "image_urls": ["<model_ref>", "<product_image_url>"],
  "quality": "basic",
  "aspect_ratio": "9:16"
}
```

**For informal social content (SeeDream 4.5):**
Note: SeeDream 4.5 struggles with full outfit accuracy — it tends to drop pieces. Only use for casual, informal content where exact product representation is less critical.
```json
{
  "model": "seedream/4.5-edit",
  "prompt": "<your UGC prompt>",
  "image_urls": ["<model_ref>", "<product_image_url>"],
  "quality": "basic"
}
```

UGC images typically use `aspect_ratio: "9:16"` (vertical/phone format) rather than the square or landscape formats used for ecommerce.

---

### Choosing the right model

- **Professional ecommerce** (white background, product accuracy critical) → **SeeDream 5 Lite image-to-image, quality: basic**
- **UGC for ecommerce store** (mirror selfies, lifestyle) → **SeeDream 5 Lite image-to-image, quality: basic** or **Flux 2 Pro**
- **Social media / Instagram** (informal, less critical) → **Flux 2 Pro** or **SeeDream 4.5**
- **Budget batch** → **Flux 2 Pro** (roughly half the cost)
- **No existing product photo** → **SeeDream 5 Lite text-to-image, quality: basic**

### Model reference

| Model | ID | Params |
|-------|----|--------|
| SeeDream 5 Lite (image-to-image) | `seedream/5-lite-image-to-image` | `quality: "basic"`, `image_urls: [...]` |
| SeeDream 5 Lite (text-to-image) | `seedream/5-lite-text-to-image` | `quality: "basic"` |
| Flux 2 Pro | `flux-2/pro-image-to-image` | `resolution: "2K"`, `image_urls: [...]` |
| SeeDream 4.5 | `seedream/4.5-edit` | `quality: "basic"`, `image_urls: [...]` — use `kie_edit_image` |

### CRITICAL: Correct parameters for `kie_generate_image`

```json
{
  "model": "seedream/5-lite-image-to-image",
  "prompt": "...",
  "image_urls": ["url1", "url2", "url3", "url4"],
  "quality": "basic",
  "aspect_ratio": "1:1"
}
```

- `image_urls` — **not** `image_input`, **not** `images`
- `quality` — for SeeDream models: `"basic"` = 2K, `"high"` = 4K
- `resolution` — for Flux 2 Pro only: `"1K"`, `"2K"`, `"4K"`

---

### Multi-Image Consistency (CRITICAL for 2+ images per product)

When generating multiple images for the same product (e.g., different poses, angles, or styles), the AI can drift between generations — different shoes, slightly different garment details, inconsistent styling. This applies to all product types, not just clothing.

**The rule: always generate images sequentially, and use each completed image as a reference for the next one.**

Here's why this matters: each generation is independent. If you fire off two generations in parallel with only the original product photo as reference, the AI makes independent creative decisions for each — it might pick different shoes, a different belt, slightly different styling. By feeding the completed first image back as a reference, you anchor the second generation to the same visual decisions.

**Workflow for multiple images:**

1. **Image 1**: Generate normally with model references + product image (as described in Mode A/B/D above). Wait for completion (poll every 30 seconds, expect 150–250 seconds).

2. **Image 2+**: Once image 1 is complete, include its output URL as an additional reference image in the `image_urls` array. This tells the AI "match the styling, shoes, accessories, and overall look from this existing shot."

```python
# Image 1 (standard)
image_urls_1 = [
    *MODEL_REFS,
    "<product_image_url>"  # original product photo
]

# Image 2 (uses image 1 as additional reference)
image_urls_2 = [
    MODEL_REFS[0], MODEL_REFS[1],
    "<image_1_output_url>",     # completed first image — for consistency
    "<product_image_url>"       # original product photo — still LAST
]
```

Note: the product photo still goes last (strongest "preserve this" signal). The completed image from the previous generation goes before it, providing style/accessory consistency. You may need to drop one model reference to stay within the 5-image limit.

**Prompt addition for image 2+:**
Add to the prompt: "Match the exact same shoes, accessories, and styling as shown in the third reference image. Only change the pose/angle."

**This applies to ALL product types** — not just clothing. Furniture can drift on background props, jewelry on hand positioning and skin tone, bags on the outfit worn with them. Always chain sequential images through the first completed output.

**Do NOT generate multiple images in parallel for the same product.** The consistency cost is not worth the time savings. Generate one, wait, use it as reference, generate the next.

---

## Phase 3: Draft vs. Live (ask ONCE at the start)

Before generating any images, ask the user one question: **"Should I upload images as draft or publish them live?"**

- **Draft**: Upload images to the product but set the product status to draft (not visible on storefront). The user can review in the Shopify admin and publish when ready.
- **Live**: Upload images and leave the product published. Images go live immediately.

After this choice is made, proceed through the entire generation and upload flow without stopping for approval. Do NOT ask "does this look good?" or "should I upload this?" after each image. The user chose their preference upfront — respect it and keep moving.

If the user later sees something they don't like, they can ask you to regenerate. But the default is: generate → upload → next product. No gates, no interruptions.

---

## Phase 4: Upload to Shopify

The upload logic depends on whether this is a **new product** or an **existing product**.

### New product: original photo first, model shot second

When creating a product from scratch, image order matters — position 1 is what customers see first on the storefront and in collection grids.

The rule: **the original product photo (from Cloudinary) always goes in position 1. The AI-generated model shot goes in position 2.**

This gives customers an accurate flat/studio reference image first, with the model shot immediately after to show the product in context. It's the standard ecommerce convention and ensures the thumbnail in collection listings shows the actual product.

**Step 1: Upload the original Cloudinary product photo as position 1**

```bash
python3 <skill-path>/scripts/shopify_products.py add-image \
  --token "<token>" \
  --product-id <product_id> \
  --image-url "<product_image_url>" \
  --alt "<product name> - product photo" \
  --position 1
```

The Cloudinary `secure_url` is permanent — Shopify will fetch and store the image on its own CDN.

**Step 2: Upload the AI-generated model image as position 2**

```bash
python3 <skill-path>/scripts/shopify_products.py add-image \
  --token "<token>" \
  --product-id <product_id> \
  --image-url "<approved_model_image_url>" \
  --alt "<product name> - model shot" \
  --position 2
```

If the user wants to generate more than one model shot for a new product, continue appending them at position 3, 4, etc. — but always keep the original Cloudinary photo at position 1.

### Existing product: append new image(s) only

When a product already exists on Shopify and already has images, do **not** reorder or replace existing images. Just append the new AI-generated image(s).

```bash
python3 <skill-path>/scripts/shopify_products.py add-image \
  --token "<token>" \
  --product-id <product_id> \
  --image-url "<approved_image_url>" \
  --alt "<product name> - model shot"
```

Omit `--position` so the image appends naturally after existing ones. If the user explicitly asks to set a specific position or reorder images, do that — but never reorder silently without their input, as changing image order affects the storefront.

Upload promptly — Kie AI URLs are temporary.

Show the user: product store URL, admin URL, and image details.

---

## Batch Mode

When processing multiple products:

1. Get auth token once at the start
2. Ask the user once: **draft or live?** (see Phase 3)
3. List all target products
4. For each product:
   - Find the product image in Cloudinary (search by display_name)
   - Choose mode (model+product for wearables, image-to-image for others)
   - Generate → upload → move to the next product (no review gate per image)
   - If multiple images per product: generate sequentially, chaining each completed image as reference for the next (see "Multi-Image Consistency")
5. You CAN run generation for **different products** in parallel (they don't share styling). But multiple images for the **same product** must be sequential.
6. Show a summary at the end with all product URLs and image counts

No per-image approval needed — the user made their draft/live choice upfront. They can review everything in Shopify admin afterwards and ask for regeneration if needed.

---

## Image Hosting

### Product reference images → Cloudinary

Product photos used as references for AI generation are stored in your Cloudinary product images folder (configured in `config.py`). Benefits:
- Permanent public `secure_url` — no shared links or token expiry to manage
- Instant availability — no processing delay
- Fast global CDN delivery
- Searchable by name, tags, and metadata via the Cloudinary MCP
- Images can be uploaded via URL, file path, or base64

### Model reference images → Shopify Files

The store's model reference photos are hosted on Shopify Files (CDN). These rarely change and have permanent URLs configured in `config.py`.

### AI-generated images → Upload to Shopify product

After generation, Kie AI provides a temporary URL. Upload to the Shopify product promptly before it expires.

If you need to permanently host an AI-generated image outside of a product (e.g., for reuse), upload it to Shopify Files:
```bash
python3 <skill-path>/scripts/shopify_products.py upload-file \
  --token "<token>" \
  --url "<kie_ai_image_url>" \
  --alt "Description of the image"
```

---

## Cloudinary MCP Reference

The Cloudinary MCP tools used in this skill:

| Tool | Purpose |
|------|---------|
| `search-assets` | Find product images by folder and display name. Returns `secure_url`. |
| `get-asset-details` | Get full details for a specific image by asset ID. |
| `upload-asset` | Upload new product photos to the product images folder. |
| `search-folders` | Verify the folder exists or find folders by name. |

---

## Prerequisites & Dependencies

This skill requires the following MCP connectors installed in your Claude environment:

| Connector | Purpose | Config needed? |
|-----------|---------|---------------|
| **Kie AI** | AI image generation (SeeDream, Flux) | No (MCP handles auth) |
| **Cloudinary** | Product reference image storage & retrieval | Cloud name in `config.py` |
| **Shopify** | Not an MCP — uses the Python script directly | Credentials in `config.py` |

### Store Details

Configured in `scripts/config.py`:
- `STORE` — Your myshopify.com domain
- `API_VERSION` — Shopify API version (default: `2025-01`)
- `CLIENT_ID` / `CLIENT_SECRET` — Custom app credentials

### Credentials

- Shopify: Client credentials grant flow (configured in `scripts/config.py`)
- Kie AI: MCP tool (no additional auth needed)
- Cloudinary: MCP tool (no additional auth needed — connected via your Claude environment)

---

## Error Handling

- **Shopify token expired**: Re-run `shopify_products.py auth` to get a fresh token.
- **Product not found**: Double-check the product ID. Use `list-products` to find the right one.
- **Image upload fails**: Verify the image URL is publicly accessible. Kie AI URLs are temporary — upload promptly after generation.
- **Kie AI generation fails**: Retry with a simplified prompt. If persistent, try a different model.
- **Kie AI URL expired**: If too much time passes between generation and upload, the URL may expire. Regenerate the image.
- **Cloudinary image not found**: Check that the display_name matches. Try a broader search without the name filter to see all images in the folder.
- **Cloudinary MCP not connected**: The user needs to connect the Cloudinary connector in their Claude environment settings. Search the MCP registry for "Cloudinary" and suggest the connector.
- **Model looks inconsistent**: Try using only 2 reference images instead of 3, or try different reference angles. Simpler prompts work better.
- **Product looks distorted in model shot**: Simplify the prompt. Focus on "wearing this exact [product]" and keep other instructions minimal.
- **Config not set up**: If `config.py` still has placeholder values, remind the user to fill in their credentials before using the skill.
- **Network errors**: Retry once, then inform the user.
