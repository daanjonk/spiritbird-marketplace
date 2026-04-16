# Publishing — Phase 5 (Image) & Phase 6 (Shopify)

How to generate the featured image and publish the finished article with full SEO metadata.

---

## Phase 5: Image Generation

### Image Prompt Guidelines

The image should work as a blog header — wide format, visually appealing, on-brand.

**Brand aesthetic to match:**
- Warm, natural colours — organic textures, soft cotton, nature elements
- Premium but approachable — not sterile stock photography
- Think: natural light, real materials, gentle tones
- Avoid: neon colours, corporate/stock photo clichés, fast-fashion vibes, overly busy compositions

**Prompt structure:**
Start with the subject, add style/mood, specify what to avoid.

Example: "A flat-lay arrangement of colourful organic cotton children's clothing on a natural linen background, warm natural lighting, soft shadows, premium editorial photography style, pastel and earth tones, clean composition with negative space for text overlay"

### Generation Call

```
mcp__kie-ai__kie_generate_image(
    model="nano-banana-pro",
    prompt="<detailed prompt>",
    aspect_ratio="16:9",
    resolution="2K",
    output_format="jpg"
)
```

### Polling — Be Patient

Image generation can take anywhere from 30 seconds to 2+ minutes. Polling too aggressively wastes calls and doesn't speed anything up.

```
mcp__kie-ai__kie_get_task_status(task_id="<task_id>")
```

**Polling schedule:**
- Poll every **30 seconds** (not 10, not 15 — 30)
- Maximum **8 polls** = 4 minutes total wait time
- If status is still "processing" after 8 polls → move to fallback

This is important because image generation models sometimes need the full 2 minutes, especially for complex prompts or high-resolution outputs. Polling every few seconds just fills the conversation with "still processing" messages without helping.

### Fallback

If Nano Banana Pro fails or times out after 4 minutes, try:
```
mcp__kie-ai__kie_generate_image(
    model="flux-2/pro-text-to-image",
    prompt="<same or simplified prompt>",
    aspect_ratio="16:9"
)
```

Apply the same 30-second polling / 4-minute max to the fallback model. If both models fail, inform the user and offer options: skip the image for now (publish without), retry manually later, or try a completely different prompt.

Present the image to the user. Offer to regenerate with adjustments if needed. (At autonomy level 1 or 2, auto-accept the image and proceed to publishing.)

---

## Phase 6: Publish to Shopify

### How publishing works

We use the **Shopify CLI** (`shopify store execute`) with the `articleCreate` GraphQL mutation. No custom scripts or tokens — the CLI handles authentication after the user runs `shopify store auth` once.

### Step 1: Ensure Authentication

The user must have authenticated with Shopify CLI:

```bash
shopify store auth --store <store>.myshopify.com --scopes write_content,read_content,read_products
```

This is a one-time setup. The CLI stores credentials securely.

### Step 2: Find the Blog ID (if not known)

```bash
shopify store execute --store <store>.myshopify.com --query 'query { blogs(first: 5) { edges { node { id title handle } } } }'
```

The blog ID will be in format `gid://shopify/Blog/123456789`.

### Step 3: Create the Article

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation CreateArticle($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id title handle body summary tags image { altText url } } userErrors { code field message } } }' \
  --variables '{
    "article": {
      "blogId": "gid://shopify/Blog/<blog_id>",
      "title": "<article title>",
      "handle": "<seo-optimized-url-slug>",
      "body": "<full HTML body>",
      "summary": "<excerpt, under 160 chars>",
      "tags": ["<tag1>", "<tag2>", "<tag3>"],
      "isPublished": false,
      "image": {
        "url": "<kie AI CDN url>",
        "altText": "<descriptive alt text with primary keyword, under 125 chars>"
      }
    }
  }'
```

At autonomy levels 1 and 2, always use `"isPublished": false` (draft). At level 3, ask the user.

**Handle rules:**
- Lowercase, hyphens only (no underscores, no spaces)
- Include primary keyword
- Strip filler words (a, the, and, of, for)
- Under 60 characters
- Example: `organic-cotton-kids-clothes-guide`

**Image alt text:**
- Descriptive, includes primary keyword naturally
- Under 125 characters
- Not just "blog image" — describe what's actually in the image
- Example: "Colourful organic cotton children's pyjamas arranged on natural linen"

The response returns the article with its ID, title, handle, tags, and image. Extract the article ID (format: `gid://shopify/Article/123`) for the next step.

### Step 4: Set SEO Metafields

After the article is created, set the SEO title and meta description via the `metafieldsSet` mutation:

```bash
shopify store execute --store <store>.myshopify.com --allow-mutations \
  --query 'mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { metafields { key namespace value } userErrors { field message } } }' \
  --variables '{
    "metafields": [
      {
        "ownerId": "gid://shopify/Article/<article_id>",
        "namespace": "global",
        "key": "title_tag",
        "value": "<optimized title, 50-60 chars>",
        "type": "single_line_text_field"
      },
      {
        "ownerId": "gid://shopify/Article/<article_id>",
        "namespace": "global",
        "key": "description_tag",
        "value": "<meta description, 150-160 chars>",
        "type": "single_line_text_field"
      }
    ]
  }'
```

This sets:
- `global.title_tag` → appears as `<title>` in the HTML head (what shows in Google search results)
- `global.description_tag` → appears as `<meta name="description">` (the snippet text in search results)

Without this step, Shopify falls back to the article title and excerpt — which may not be SEO-optimized.

### Step 5: Confirm Publication

Show the user:

```
Article published!

Live URL: https://<store>.myshopify.com/blogs/<blog-handle>/<handle>
Admin URL: https://<store>.myshopify.com/admin/articles/<numeric_id>
Status: Draft (or Published)

SEO metadata set:
- Title: <seo title>
- Description: <meta description>
- Handle: <url slug>
- Image alt: <alt text>
```

Offer to switch to draft if they published by accident, or to make further edits via the admin URL.

---

## Post-Publish Checklist

After publishing, remind the user to:
1. **Check the live page** — verify formatting, images, and links render correctly
2. **Submit to Google Search Console** — request indexing for faster discovery
3. **Share on social** — the Open Graph tags are auto-generated by Shopify from the article metadata
4. **Monitor in 2-4 weeks** — check Google Search Console for impressions and ranking position
