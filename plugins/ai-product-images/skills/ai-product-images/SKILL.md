---
name: ai-product-images
description: Generate AI product images and upload them to Shopify products. Uses Kie AI for image generation (SeeDream 5 Lite, Flux 2 Pro) and Shopify Files for hosting product reference photos. For existing Shopify products, uses the product's existing CDN images as reference; for new products, uploads local files directly to Shopify Files. Use this skill whenever the user wants to create product photos, generate product images, add images to Shopify products, replace product photos, create studio-style product shots, create UGC-style content, or says things like "generate images for my products", "create product photos", "add AI images to Shopify", "make product pictures", "studio shots for products", "UGC images", "mirror selfie shots", "lifestyle product photos", or any variation of wanting AI-generated imagery for Shopify products. Also trigger when the user mentions product images in combination with Kie AI or Shopify.
---

# AI Product Image Generator for Shopify

Generates clean, studio-style AI product images and uploads them directly to Shopify products.

---

## Setup (REQUIRED — do this before first use)

### 1. Shopify CLI Authentication

Authenticate with your Shopify store via the Shopify CLI (one-time setup):

```bash
shopify store auth --store <your-store>.myshopify.com --scopes read_products,write_products,write_files
```

This stores credentials securely — no custom apps, API keys, or config files needed. Ask the user for their store domain at the start of the flow if not already known.

### 2. Kie AI MCP (image generation)

The Kie AI MCP connector must be installed in the Claude environment. No API key needed in config — the MCP handles authentication.

### 3. Model Reference Images (optional — for model+product shots)

If you want AI-generated photos of a model wearing/holding your products:

1. Upload 2-3 photos of your model to Shopify Files (Settings → Files), or drop them in the chat and Claude will upload them
2. Save the permanent CDN URLs — you'll provide them when using Mode A

These URLs should be permanent Shopify CDN links (e.g., `https://cdn.shopify.com/s/files/...`). Leave empty if you only need product-on-white-background shots.

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

**The rule: if a product photo exists (provided by user, already on Shopify, or as a local file), it MUST be included as a reference image in the Kie AI call. Never generate from text description alone when a photo is available.**

Why this matters: without the real photo as a visual anchor, the AI interprets "beige" as whatever shade it imagines. The result looks plausible but doesn't match the actual product — and that's unacceptable for ecommerce where customers expect to receive exactly what they see.

### Step 0: Get a public URL for the product photo (before any generation)

Kie AI requires publicly accessible image URLs. Before generating anything, make sure you have a URL for the product photo.

**Which route to use:**

- **Product already exists on Shopify with images** → **Route A** — use existing CDN URLs directly
- **User provides a local file, drops an image in chat, or points to a file on their computer** → **Route B** — upload to Shopify Files to get a permanent CDN URL
- **User provides a public URL** (e.g., from a website) → use `fileCreate` with `originalSource` directly (simplified Route B — skip staged upload)
- **No image available at all** → **Mode C fallback** — text-to-image with a warning

**Route A — Product already exists on Shopify (use existing CDN images):**

Use the Shopify CLI to retrieve the product's existing image CDN URLs:
```bash
shopify store execute --store <store>.myshopify.com --query 'query ($id: ID!) { product(id: $id) { id title handle media(first: 10) { nodes { ... on MediaImage { id image { url altText } } } } } }' --variables '{"id": "gid://shopify/Product/<id>"}'
```

The response includes image URLs hosted on Shopify's CDN (`cdn.shopify.com`). These are permanent, public, and immediately usable — pass them directly to Kie AI. Pick the clearest/most representative image as the reference.

If the existing product has no images, fall through to Route B.

**Route B — Upload a local file to Shopify Files (for new products or user-provided images):**

This is a 4-step process that takes ~10 seconds total:

**Step 1: Get file info and create a staged upload target**

```bash
# Get the file size first
stat -f%z "<local_file_path>"

# Create staged upload target
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation stagedUploadsCreate($input: [StagedUploadInput!]!) { stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } } }' \
  --variables '{"input": [{"resource": "FILE", "filename": "<filename.ext>", "mimeType": "<mime_type>", "fileSize": "<size_in_bytes>", "httpMethod": "POST"}]}'
```

Common MIME types: `image/webp`, `image/jpeg`, `image/png`, `image/gif`.

**Step 2: Upload the file to the staged URL**

Use `curl` with the parameters returned from Step 1. Build a multipart form POST with each parameter as a form field, and the file as the last field:

```bash
curl -s -X POST "<staged_url>" \
  -F 'Content-Type=<mime_type>' \
  -F 'success_action_status=201' \
  -F 'acl=private' \
  -F 'key=<key_value>' \
  -F 'x-goog-date=<date_value>' \
  -F 'x-goog-credential=<credential_value>' \
  -F 'x-goog-algorithm=<algorithm_value>' \
  -F 'x-goog-signature=<signature_value>' \
  -F 'policy=<policy_value>' \
  -F "file=@<local_file_path>"
```

All parameter names and values come directly from the `parameters` array in Step 1. Include every parameter exactly as returned. The file field must be last. Expect HTTP 201 on success.

**Step 3: Create the file in Shopify using the resourceUrl**

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt createdAt fileStatus } userErrors { field message } } }' \
  --variables '{"files": [{"alt": "<product name>", "contentType": "IMAGE", "originalSource": "<resourceUrl_from_step1>"}]}'
```

**Step 4: Poll for the permanent CDN URL** (file processing takes ~5 seconds)

```bash
shopify store execute --store <store>.myshopify.com \
  --query 'query { node(id: "<file_gid_from_step3>") { ... on MediaImage { id image { url width height } fileStatus } } }'
```

Wait 5 seconds before first poll. If `fileStatus` is `READY` and `image.url` is present, you have your permanent CDN URL. If still `UPLOADED` or `PROCESSING`, wait 3 more seconds and poll again (max 5 polls).

**Result:** A permanent `https://cdn.shopify.com/...` URL ready for Kie AI.

**Route B (simplified) — User provides a public URL:**

If the user provides an image that's already publicly accessible (e.g., from a website), skip the staged upload and use `fileCreate` directly:

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt createdAt fileStatus } userErrors { field message } } }' \
  --variables '{"files": [{"alt": "<product name>", "contentType": "IMAGE", "originalSource": "<public_url>"}]}'
```

Then poll for the CDN URL as in Step 4 above.

Never silently fall back to text-only generation. Always inform the user when you can't use their product photo as reference.

### Image URL ordering in the Kie AI call

When combining model references with a product image, the product image always goes LAST — this position gets the strongest "preserve this" signal from the prompt:
```python
image_urls = [
    MODEL_REF_1,   # model angle 1
    MODEL_REF_2,   # model angle 2
    "<PRODUCT_IMAGE_URL>"  # actual product photo (Shopify CDN) — ALWAYS LAST
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

Ask the user for their model reference image URLs at the start of the flow, or check if they've been provided previously. These should be permanent Shopify CDN URLs. Example:

```
Model reference URLs:
- https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/model_front.png?v=...
- https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/model_side.png?v=...
```

These must be permanently hosted on Shopify CDN (they won't expire). They show the same model from different angles.

### How to upload/update model reference images

If the user wants to add or change model reference images:
1. The user drops the model photos in the chat or points to local files
2. Upload them to Shopify Files using the Route B staged upload flow (see Step 0)
3. Save the permanent CDN URLs for use in Mode A

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
   → Existing product with images: use Shopify CDN URLs directly (Route A)
   → New product / user provides file: upload to Shopify Files → get CDN URL (Route B)
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

Use the **Shopify CLI** for all Shopify API calls. The user must have authenticated with `shopify store auth` first (see Setup).

### Step 1: List products

```bash
shopify store execute --store <store>.myshopify.com --query 'query ($first: Int!) { products(first: $first) { edges { node { id title handle status featuredMedia { ... on MediaImage { image { url altText } } } } } } }' --variables '{"first": 20}'
```

To search for specific products:
```bash
shopify store execute --store <store>.myshopify.com --query 'query ($first: Int!, $query: String) { products(first: $first, query: $query) { edges { node { id title handle status } } } }' --variables '{"first": 20, "query": "title:*search term*"}'
```

To browse collections first:
```bash
shopify store execute --store <store>.myshopify.com --query 'query { collections(first: 20) { edges { node { id title handle } } } }'
```

### Step 2: Get full product details

For each selected product:
```bash
shopify store execute --store <store>.myshopify.com --query 'query ($id: ID!) { product(id: $id) { id title handle descriptionHtml status media(first: 10) { nodes { ... on MediaImage { id image { url altText } } } } variants(first: 5) { nodes { id title price } } } }' --variables '{"id": "gid://shopify/Product/<id>"}'
```

---

## Phase 1.5: Get Product Reference Image

Before generating, you need a reference image URL. See Step 0 for the full routing logic.

### For existing Shopify products (Route A)

You already retrieved the product in Phase 1. Use the image CDN URLs from that response — no extra step needed. Pick the clearest/most representative image.

### For new products or user-provided images (Route B)

The user drops an image in the chat, points to a file on their computer (Downloads folder, workspace, etc.), or provides a URL. Follow the Route B staged upload flow from Step 0 to get a permanent Shopify CDN URL.

If there's no image available at all, fall back to Mode C (text-to-image) with a warning to the user.

---

## Phase 2: Generate Image (Kie AI)

### Mode A: Model + Product (DEFAULT for wearable products)

This is the primary mode for apparel, accessories, and anything a model can wear/hold. It passes the model reference images + the product image to the AI, which generates the model wearing the actual product.

#### Step 1: Prepare the image URLs array

You MUST have a product image URL at this point (Shopify CDN URL from Route A or B — see Step 0). If you don't, stop and get one first.

Pass the model references first, then the product image last:

```python
image_urls = [
    "<model_ref_1>",          # model angle 1 (Shopify CDN URL)
    "<model_ref_2>",          # model angle 2 (Shopify CDN URL)
    "<product_image_url>"     # the actual product (Shopify CDN) — REQUIRED, ALWAYS LAST
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
    "<model_ref_1>", "<model_ref_2>",
    "<product_image_url>"  # original product photo
]

# Image 2 (uses image 1 as additional reference)
image_urls_2 = [
    "<model_ref_1>", "<model_ref_2>",
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

The rule: **the original product photo always goes in position 1. The AI-generated model shot goes in position 2.**

This gives customers an accurate flat/studio reference image first, with the model shot immediately after to show the product in context. It's the standard ecommerce convention and ensures the thumbnail in collection listings shows the actual product.

**Step 1: Upload the original product photo**

If the original product photo was uploaded to Shopify Files via Route B, it already has a CDN URL. Use `fileCreate` to associate it with the product, or include it when creating the product via `productSet`.

**Step 2: Upload the AI-generated model image**

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt ... on MediaImage { image { url } } } userErrors { field message } } }' \
  --variables '{"files": [{"alt": "<product name> - model shot", "contentType": "IMAGE", "originalSource": "<kie_ai_output_url>"}]}'
```

If the user wants to generate more than one model shot for a new product, continue uploading them — but always keep the original product photo first.

### Existing product: append new image(s) only

When a product already exists on Shopify and already has images, do **not** reorder or replace existing images. Just upload the new AI-generated image(s) to Shopify Files:

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt ... on MediaImage { image { url } } } userErrors { field message } } }' \
  --variables '{"files": [{"alt": "<product name> - model shot", "contentType": "IMAGE", "originalSource": "<kie_ai_output_url>"}]}'
```

If the user explicitly asks to reorder images, do that — but never reorder silently without their input, as changing image order affects the storefront.

Upload promptly — Kie AI URLs are temporary.

Show the user: product store URL, admin URL, and image details.

---

## Batch Mode

When processing multiple products:

1. Ask the user once: **draft or live?** (see Phase 3)
2. List all target products
3. For each product:
   - Get the product reference image (Route A for existing products, Route B for new ones with user-provided files)
   - Choose mode (model+product for wearables, image-to-image for others)
   - Generate → upload → move to the next product (no review gate per image)
   - If multiple images per product: generate sequentially, chaining each completed image as reference for the next (see "Multi-Image Consistency")
4. You CAN run generation for **different products** in parallel (they don't share styling). But multiple images for the **same product** must be sequential.
5. Show a summary at the end with all product URLs and image counts

No per-image approval needed — the user made their draft/live choice upfront. They can review everything in Shopify admin afterwards and ask for regeneration if needed.

---

## Image Hosting

All images are hosted on **Shopify Files** (CDN). This keeps everything in one place — no third-party dependencies.

### Product reference images → Shopify Files
Product photos used as references for AI generation are uploaded to Shopify Files via the staged upload flow. Benefits:
- Permanent public CDN URL (`cdn.shopify.com/...`)
- No token expiry or shared links to manage
- Fast global CDN delivery
- Managed directly through Shopify admin (Settings → Files)

### Model reference images → Shopify Files
The store's model reference photos are also hosted on Shopify Files. These rarely change and have permanent URLs provided by the user at setup.

### AI-generated images → Shopify Files
After generation, Kie AI provides a temporary URL. Upload to Shopify Files promptly before it expires:

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt ... on MediaImage { image { url } } } userErrors { field message } } }' \
  --variables '{"files": [{"alt": "Description of the image", "contentType": "IMAGE", "originalSource": "<kie_ai_image_url>"}]}'
```

---

## Prerequisites & Dependencies

| Requirement | Purpose | Setup |
|-------------|---------|-------|
| **Shopify CLI** | Product listing, image upload, file management | `shopify store auth --store <store>.myshopify.com --scopes read_products,write_products,write_files` |
| **Kie AI MCP** | AI image generation (SeeDream, Flux) | Connect in Claude Code MCP settings |

That's it — just two dependencies. No Cloudinary, no custom apps, no API keys in config files.

---

## Error Handling

- **Shopify CLI not authenticated**: Ask the user to run `shopify store auth --store <store>.myshopify.com --scopes read_products,write_products,write_files`
- **Staged upload access denied**: Re-run `shopify store auth` with `write_files` scope included
- **Staged upload curl fails**: Check that all parameters from `stagedUploadsCreate` are included exactly as returned. The file field must be last in the curl command.
- **File processing stuck**: If `fileStatus` is still `PROCESSING` after 5 polls (~25 seconds), the file may be corrupted or too large. Ask the user to try a different image.
- **Product not found**: Double-check the product ID (must be in `gid://shopify/Product/<id>` format). Use the list products query to find the right one.
- **Image upload fails**: Verify the image URL is publicly accessible. Kie AI URLs are temporary — upload promptly after generation.
- **Kie AI generation fails**: Retry with a simplified prompt. If persistent, try a different model.
- **Kie AI URL expired**: If too much time passes between generation and upload, the URL may expire. Regenerate the image.
- **Model looks inconsistent**: Try using only 2 reference images instead of 3, or try different reference angles. Simpler prompts work better.
- **Product looks distorted in model shot**: Simplify the prompt. Focus on "wearing this exact [product]" and keep other instructions minimal.
- **Network errors**: Retry once, then inform the user.
