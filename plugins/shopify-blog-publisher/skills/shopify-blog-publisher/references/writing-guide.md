# Blog Writing Guide — Phase 4

How to write the actual article. Follow the approved outline from Phase 3 exactly — the structure is already validated.

---

## Brand Voice

The voice comes from the Shopify Brain vault (`Brand/tone-of-voice.md`). Here's the condensed version:

### How we sound
- A knowledgeable friend who genuinely cares — calm, warm, confident, honest
- Like the trusted expert at a dinner party who knows their stuff, doesn't oversell, and doesn't judge
- First person "we" when speaking as the brand

### How we don't sound
- A fast-fashion brand running flash sales
- A corporate entity hiding behind vague sustainability claims
- A brand that punches at competitors

### Writing rules
- Short, clear sentences — no fluff, no corporate jargon
- Lead with proof, not claims — show, don't tell
- Acknowledge real parent problems: low-quality fast fashion, environmental guilt, skin sensitivities
- Never use: discount language, urgency tactics, superlatives without evidence, greenwashing buzzwords without substance

---

## Customer-Voice Integration

The Shopify Brain vault has `Brand/customer-voice.md` with 300+ real Trustpilot review quotes. These are gold — they're the exact words the target audience uses.

### How to use them

Don't just quote customers (unless appropriate for a testimonial section). Instead, **mirror their language** naturally in your writing:

| Customer says | You write |
|--------------|-----------|
| "Actually sustainable, not just marketed as sustainable" | "What makes this different from brands that market sustainability without the receipts?" |
| "Kids have eczema and these have been a godsend" | "For parents dealing with eczema-prone skin, the material makes all the difference." |
| "I'd rather quality I can hand down" | "The real value shows up in year two — when the colours haven't faded and you're passing them to a sibling." |
| "Colours haven't faded and the fabric hasn't got any fluffing yet" | "After six months of washing, the prints look the same as day one." |

The goal is emotional recognition — the reader should feel "this brand gets me" without realizing you studied their language.

---

## SEO On-Page Rules

### Primary keyword placement
- In the title (H1)
- In the first paragraph (within the first 100 words)
- In at least 2 H2 headings
- In the meta description
- In the URL handle
- In the featured image alt text

### Secondary keyword distribution
- Distribute naturally throughout — one secondary keyword per H2 section is a good rhythm
- Don't force them. If a secondary keyword doesn't fit a section naturally, skip it.

### Paragraph structure
- 2-3 sentences per paragraph maximum
- One idea per paragraph
- Use transition words between sections (but don't overdo it — "furthermore" and "moreover" feel robotic)

### Lists and formatting
- Use bullet points and numbered lists where they genuinely aid readability
- Bold key phrases that contain target keywords — helps scanning and signals relevance to crawlers
- Don't over-format: if every other sentence is bold or bulleted, nothing stands out

### Featured snippet answer blocks
- For question-based H2 headings, the first paragraph must be a standalone 40-60 word answer
- Write it as if someone asked you the question directly and you had one breath to answer
- Then expand with detail, examples, or evidence in the following paragraphs

---

## Product Preview Blocks

When the article mentions or recommends a specific product, don't just drop a text hyperlink — embed a visual product preview card. These convert significantly better because readers can actually see the product before clicking.

### When to use them
- After a section that naturally mentions or discusses a product
- 1-2 per article maximum (more feels like a catalog page)
- Not for collection links — plain text links are fine for collections and other blog posts

### How to build them

Use the Shopify CLI to get product data:
```bash
shopify store execute --store <store>.myshopify.com --query 'query ($id: ID!) { product(id: $id) { id title handle descriptionHtml media(first: 5) { nodes { ... on MediaImage { image { url altText } } } } variants(first: 1) { nodes { price } } } }' --variables '{"id": "gid://shopify/Product/<id>"}'
```

Then insert this HTML block into the article body:

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

Pull real values from the Shopify MCP response: product title, first image URL, price, handle, and a short description (first sentence of the body, or the product type).

### Placement
- Place the card **after** the paragraph that naturally mentions the product, not before
- Add a short transition sentence before the card, or simply flow from the discussion into the card
- The card should feel like a helpful aside, not a sales pitch

---

## Content Quality Checks

Before presenting the article, verify:

1. **Word count**: 1,500-2,500 words (calibrated against top SERP results from Phase 2)
2. **Heading frequency**: roughly every 150-200 words
3. **Internal links**: 3-5, all pointing to real URLs (not placeholders)
4. **Primary keyword density**: appears naturally ~5-8 times total (not stuffed)
5. **No greenwashing**: every sustainability claim has evidence or is removed
6. **No competitor mentions**: we stay in our own lane
7. **No discount/urgency language**: fair prices, no countdown timers, no "limited time"
8. **Alt text prepared**: for the featured image

---

## Output Format

Present the article to the user as:

### 1. SEO Metadata
```
Title: [50-60 chars]
Meta Description: [150-160 chars]
URL Handle: [keyword-slug]
Image Alt Text: [under 125 chars]
Tags: [tag1, tag2, tag3]
```

### 2. Full Article (HTML)

Clean HTML with:
- Table of contents with anchor links
- All H2/H3/H4 headings with `id` attributes
- Resolved internal links (real store URLs)
- Short paragraphs, proper formatting
- Featured snippet answer blocks where planned

### 3. Word count and keyword summary

Brief summary showing: total word count, primary keyword occurrences, internal links placed.

Wait for user approval or change requests before proceeding to image generation.

---

## Common Pitfalls

- **Keyword stuffing**: if the primary keyword appears more than once per 200 words, it's too much
- **Generic intros**: don't start with "In today's world..." or "Have you ever wondered..." — start with something specific to the reader's situation
- **Wall of text**: break up any paragraph longer than 3 sentences
- **Orphan sections**: every H2 section should have at least 150 words of substance
- **Passive voice**: prefer active constructions. "We source our cotton from..." not "Our cotton is sourced from..."
- **AI-detectable patterns**: vary sentence length, use specific examples, include unique perspectives. Avoid formulaic structures (3 points per section, identical paragraph lengths)
