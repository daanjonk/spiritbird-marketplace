---
name: shopify-blog-publisher
description: End-to-end Shopify blog article publisher. Takes a blog idea from ideation through keyword research, competitive SERP analysis, SEO-optimized writing, AI image generation, and publishing to Shopify — all in one production-ready flow. Use this skill whenever the user wants to publish a blog post to their Shopify store, write a blog article for Shopify, do keyword research for a blog, or says things like "publish a blog", "new blog post", "write an article for the shop", "blog for Shopify", "create a blog post", "SEO blog", "write content for the store", or any variation of wanting to research, write, and publish blog content to their Shopify webshop. Also trigger when the user asks about blog SEO, content strategy for Shopify, or optimizing blog posts for search.
---

# Shopify Blog Publisher

Publishes a production-ready, SEO-optimized blog article to a Shopify store in one flow: idea → research → outline → write → image → publish.

## The Flow

```
Phase 0: Ideation, Context & Autonomy Level
Phase 1: Keyword Research (DataForSEO MCP)
Phase 2: SERP & Competitive Analysis
Phase 2b: AI Optimization (optional — user opts in at Phase 0)
Phase 3: Outline & Structure
Phase 4: Blog Writing (Brand-Aligned)
Phase 5: Image Generation (Kie AI)
Phase 6: Publish to Shopify
```

Each phase builds on the previous. Don't skip phases unless the user explicitly says to. At each phase transition, read the relevant reference file for detailed instructions.

---

## Phase 0: Ideation, Context & Autonomy Level

This is the entry point. Before any API calls, understand what we're building, why, and how much control the user wants.

**Step 1 — Get the idea.** The user provides a topic, product, or content idea. If vague, ask one focused follow-up.

**Step 2 — Ask three key questions (present all at once using AskUserQuestion):**

Question 1 — **Goal:** "What's the goal for this blog post?"
- Traffic (high-volume keywords) · Conversion (commercial intent) · Education (informational) · Product launch (weave product in)

Question 2 — **Optimization scope:** "SEO only, or also AI search optimization?"
- SEO only (~$0.07 API cost) — keyword research + SERP analysis
- SEO + AI (~$0.18 API cost) — adds LLM mentions analysis

Question 3 — **Autonomy level:** "How hands-on do you want to be?"

Present these as numbered options:
1. **Full autopilot** — I research, write, generate the image, and save as draft. You only review the final draft in Shopify.
2. **Outline check + final review** — I pause after the outline for your approval, then write + generate image + publish as draft. You review the final post before it goes live.
3. **Full control** — I pause after the outline, after the written article, and after the image. You approve each step before I continue.

These autonomy levels control which phases require user confirmation:

| Phase | Level 1 (Autopilot) | Level 2 (Outline + Final) | Level 3 (Full control) |
|-------|-------------------|-------------------------|---------------------|
| Keyword selection | Auto-pick best | Auto-pick best | Pause for approval |
| Outline | Auto-approve | **Pause for approval** | **Pause for approval** |
| Written article | Auto-approve | **Pause for approval** | **Pause for approval** |
| Image | Auto-approve | Auto-approve | **Pause for approval** |
| Publish | Save as draft | Save as draft | User chooses draft/live |

At level 1, the entire flow runs end-to-end and saves as a draft for the user to review in Shopify admin. At level 3, nothing moves forward without explicit approval. Level 2 is the sweet spot for most users — it catches structural issues early (outline) and lets them review the final product, but doesn't slow down the middle.

Store all three answers — they gate which API calls happen, how content is structured, and where the flow pauses.

**Step 3 — Load brand context.** Read these from the Shopify Brain vault:
- `Brand/tone-of-voice.md` — writing style and rules
- `Brand/icp.md` — who we write for
- `Brand/customer-voice.md` — real customer language to weave in

---

## Phase 1: Keyword Research

Read `references/keyword-research.md` for all DataForSEO MCP tool calls, interpretation guidance, and keyword selection strategy.

**Summary:** Use the DataForSEO MCP tools directly (suggestions, ideas, related keywords) → filter by difficulty and intent aligned with the user's goal → present a table with 1 primary + 3-5 secondary keywords → get user confirmation (unless autonomy level 1 or 2, in which case auto-select and log the reasoning).

---

## Phase 2: SERP & Competitive Analysis

Read `references/serp-analysis.md` for SERP commands, content parsing, and competitor analysis.

**Summary:** Pull live top-10 results → parse the top 2-3 ranking articles for structure and word count → check SERP competitors → identify content gaps and featured snippet opportunities.

If the user opted into **AI optimization** at Phase 0, also run the AI analysis steps described in that reference (LLM mentions + AI search volume).

---

## Phase 3: Outline & Structure

Read `references/content-structure.md` for heading hierarchy rules, featured snippet targets, TOC format, internal linking plan, and the outline template.

**Summary:** Build a detailed H1/H2/H3/H4 outline informed by SERP data → include featured snippet targets from People Also Ask → plan internal links using real store URLs → propose meta title, description, and URL handle → present outline to user for approval (unless autonomy level 1).

### Fetching product & collection data for internal links

Use the **Shopify CLI** to fetch product and collection data. The user must have authenticated with `shopify store auth` first (see Prerequisites).

```bash
# List products (names, handles, URLs)
shopify store execute --store <store>.myshopify.com --query 'query { products(first: 20) { edges { node { id title handle status featuredMedia { ... on MediaImage { image { url altText } } } } } } }'

# List collections
shopify store execute --store <store>.myshopify.com --query 'query { collections(first: 20) { edges { node { id title handle } } } }'
```

Use these for all product/collection data throughout the flow (product names, URLs, handles, descriptions, images). They provide real-time store data.

---

## Phase 4: Blog Writing

Read `references/writing-guide.md` for brand voice rules, customer-voice integration, SEO on-page requirements, and output format.

**Summary:** Write 1,500-2,500 words following the approved outline in the brand voice (warm, trustworthy, proof-led). Weave in customer language naturally. Resolve all internal links to real URLs. Optimize for featured snippets with 40-60 word answer blocks.

### Product Preview Blocks

When linking to products in the blog, don't just use plain text hyperlinks — embed visual product preview blocks that show the product image, name, price, and a link. These convert significantly better because readers can see what they're clicking on.

Use the Shopify CLI to fetch product details including images:
```bash
shopify store execute --store <store>.myshopify.com --query 'query ($id: ID!) { product(id: $id) { id title handle descriptionHtml media(first: 10) { nodes { ... on MediaImage { image { url altText } } } } variants(first: 5) { nodes { id title price } } } }' --variables '{"id": "gid://shopify/Product/<id>"}'
```

Then render them as HTML blocks in the article body:

```html
<div class="blog-product-card" style="border: 1px solid #e5e5e5; border-radius: 8px; padding: 16px; margin: 24px 0; display: flex; align-items: center; gap: 16px; text-decoration: none;">
  <img src="<product_image_url>" alt="<product_title>" style="width: 120px; height: 120px; object-fit: cover; border-radius: 6px;" />
  <div>
    <h4 style="margin: 0 0 4px 0; font-size: 1.1em;"><a href="/products/<handle>" style="color: inherit; text-decoration: none;">Product Name</a></h4>
    <p style="margin: 0 0 8px 0; color: #666; font-size: 0.9em;">Short product description or variant info</p>
    <span style="font-weight: 600;">€XX.XX</span>
    <a href="/products/<handle>" style="margin-left: 12px; color: #2c6e49; font-weight: 500;">View product →</a>
  </div>
</div>
```

Use 1-2 product preview blocks per article — place them after a relevant section where the product is naturally mentioned. Don't overdo it; the blog should still read as content, not a catalog page. Plain text internal links are still fine for collection pages and other blog posts.

Present complete article with SEO metadata for user approval (unless autonomy level 1).

---

## Phase 5: Image Generation

Generate a featured image using Kie AI:

```
mcp__kie-ai__kie_generate_image(
    model="nano-banana-pro",
    prompt="<detailed prompt based on blog topic and brand aesthetic>",
    aspect_ratio="16:9",
    resolution="2K",
    output_format="jpg"
)
```

### Polling — be patient

Image generation can take time. Poll with `mcp__kie-ai__kie_get_task_status(task_id="<id>")` every **30 seconds** (not more frequently — the generation needs time). Allow up to **4 minutes** (8 polls) before deciding it's stuck.

Polling schedule:
1. Submit generation request → get task_id
2. Wait 30 seconds → first poll
3. If not complete, wait another 30 seconds → second poll
4. Continue every 30 seconds up to 8 polls (4 minutes total)
5. If still not complete after 8 polls → try fallback model
6. If fallback also fails after 4 minutes → inform user, offer to skip image or retry manually

Read `references/publishing.md` for image prompt guidelines and fallback models.

Present the image to the user (unless autonomy level 1 or 2). Offer to regenerate if needed.

---

## Phase 6: Publish to Shopify

Read `references/publishing.md` for the full publish flow including SEO metafields.

**The publishing flow uses the Shopify CLI** (`shopify store auth` + `shopify store execute`) for article creation and SEO metafields. No custom scripts or tokens needed.

**Summary:**
1. Ensure user has run `shopify store auth` (see Prerequisites)
2. Create article via `shopify store execute --allow-mutations` with the `articleCreate` GraphQL mutation
3. Set SEO metafields via `shopify store execute --allow-mutations` with the `metafieldsSet` mutation
4. Confirm with user: show live URL, admin URL, SEO metadata, status

At autonomy levels 1 and 2, always publish as **draft** (`isPublished: false`). At level 3, ask the user whether to publish live or save as draft.

---

## Configuration

### Prerequisites

Before using this skill, the user needs:

1. **Shopify CLI** installed and authenticated:
   ```bash
   shopify store auth --store <your-store>.myshopify.com --scopes write_content,read_content,read_products
   ```
   This is a one-time setup. The CLI stores credentials securely.

2. **DataForSEO MCP** connected in Claude Code (handles keyword research, SERP analysis)
3. **Kie AI MCP** connected in Claude Code (handles image generation)

At the start of the flow, ask the user for their store domain if not already known. Use it in all `shopify store execute` commands.

### Data Access — What to Use When

| Need | Tool | How |
|------|------|-----|
| Product names, URLs, images, prices | **Shopify CLI** | `shopify store execute --query '...'` |
| Collection names, URLs | **Shopify CLI** | `shopify store execute --query '...'` |
| Blog article creation & publishing | **Shopify CLI** | `shopify store execute --allow-mutations --query '...'` |
| SEO metafields on articles | **Shopify CLI** | `shopify store execute --allow-mutations --query '...'` |
| Keyword research | **DataForSEO MCP** | Direct MCP tool calls |
| SERP analysis | **DataForSEO MCP** | Direct MCP tool calls |
| AI search data | **DataForSEO MCP** | Direct MCP tool calls |
| Image generation | **Kie AI MCP** | Direct MCP tool calls |

All tools handle authentication automatically. No API keys, tokens, or custom scripts needed.

### Credentials
- DataForSEO: Handled by MCP connection · Shopify: Handled by Shopify CLI · Kie AI: Handled by MCP connection

### Default Market
- **Location**: "United States" · **Language**: "en"
- Override per-request: UK = "United Kingdom", Netherlands = "Netherlands" (language_code: "nl"), etc.

### API Cost Per Blog Post
- SEO only: ~$0.07 · SEO + AI: ~$0.18

---

## Reference Files

| File | When to read | What's in it |
|------|-------------|-------------|
| `references/keyword-research.md` | Phase 1 | DataForSEO MCP tool calls, keyword selection, interpretation |
| `references/serp-analysis.md` | Phase 2/2b | SERP analysis, content parsing, AI optimization (all via DataForSEO MCP) |
| `references/content-structure.md` | Phase 3 | Heading hierarchy, snippets, TOC, outline template |
| `references/writing-guide.md` | Phase 4 | Brand voice, customer-voice, SEO on-page, product preview blocks |
| `references/publishing.md` | Phase 5-6 | Image gen (polling), Shopify publish, SEO metafields |

---

## Error Handling

- **DataForSEO MCP fails**: If a DataForSEO MCP tool returns an error, show the error to the user and suggest adjusting the keyword or market. Common issues: invalid location name, keyword too long, or API rate limits.
- **DataForSEO AI endpoints fail**: The AI optimization tools (`ai_optimization_keyword_data_search_volume`, `ai_opt_llm_ment_search`) can take longer to respond than regular SEO tools. If they time out, retry once. If still failing, skip the AI optimization step and proceed with SEO-only data.
- **Shopify CLI not authenticated**: Ask the user to run `shopify store auth --store <store>.myshopify.com --scopes write_content,read_content,read_products`
- **Shopify article creation fails**: Check `userErrors` in the GraphQL response. Common issues: missing required fields, duplicate handle, insufficient scopes.
- **SEO metafields fail**: Check `userErrors` in the GraphQL response. May need `write_content` scope.
- **Kie AI image not ready**: Poll every 30 seconds, max 4 minutes. If stuck, try fallback model `flux-2/pro-text-to-image`. If that also fails, inform user.
- **Content parsing timeout**: Skip URL, try next top result.
- **Network errors**: Retry once, then inform user.
