# Content Structure & Outline — Phase 3

How to build a detailed, SEO-optimized outline before writing. The outline is presented to the user for approval — no writing happens until it's confirmed.

---

## Heading Hierarchy

Shopify uses the article title as the H1. Never add another H1 in the body.

| Level | Purpose | Frequency |
|-------|---------|-----------|
| H1 | Article title (set by Shopify) | Exactly 1, never in body |
| H2 | Main sections | 4-6 per article |
| H3 | Subsections within an H2 | 2-3 per H2 as needed |
| H4 | Specific detail within H3 | Sparingly, only when needed |

Place a heading every 150-200 words. This improves both readability and crawlability.

---

## Featured Snippet Targets

Featured snippets appear at position zero in Google — they get ~8% of all clicks.

### How to target them

1. Turn 2-3 of your H2 headings into **questions** (from People Also Ask data in Phase 2)
2. Immediately below each question heading, write a **40-60 word direct answer**
3. This answer paragraph should fully resolve the question — Google extracts exactly this
4. Then expand with deeper detail in the following paragraphs

### Example

```html
<h2>Is organic cotton really better for kids with eczema?</h2>
<p>Yes — organic cotton is grown without synthetic pesticides or chemical treatments that can irritate sensitive skin. Unlike conventional cotton blends that may contain elastane or polyester, 100% organic cotton is breathable, hypoallergenic, and free from residual chemicals. For children with eczema, this means fewer flare-ups and more comfortable wear.</p>
<p>Here's what makes the difference in more detail...</p>
```

The first paragraph (53 words) is the snippet target. Clean, direct, factual.

---

## Table of Contents

Include a clickable table of contents for articles over 1,500 words. It improves UX, crawlability, and can generate jump-link rich snippets in search results.

### HTML format

```html
<div class="table-of-contents">
  <h2>What's in this guide</h2>
  <ul>
    <li><a href="#section-handle">Section Title</a></li>
    <li><a href="#section-handle-2">Section Title 2</a></li>
    <!-- one li per H2 section -->
  </ul>
</div>
```

Each H2 in the body gets a matching `id` attribute:
```html
<h2 id="section-handle">Section Title</h2>
```

---

## Internal Linking Plan

Internal links are critical for Shopify SEO — they pass authority from blog content to product and collection pages, and help Google crawl deeper into the store.

### Rules

- Include **3-5 internal links** per article
- Place them in **early-to-mid body paragraphs** (not just the conclusion)
- Link to **collections** for broad topics, **products** for specific mentions
- **Vary anchor text**: use product names, natural phrases, branded terms — avoid repeating the same keyword anchor

### Fetching real URLs

Before building the outline, fetch the store's actual URLs using the **Shopify CLI**:

```bash
shopify store execute --store <store>.myshopify.com --query 'query { products(first: 20) { edges { node { id title handle } } } }'
shopify store execute --store <store>.myshopify.com --query 'query { collections(first: 20) { edges { node { id title handle } } } }'
```

Map each planned internal link to a real URL. Never use placeholder links — every link in the final article must be a working URL.

### Where to place links

| Content context | Link to |
|----------------|---------|
| Mentioning a product category | Collection page |
| Recommending a specific item | Product page |
| Referencing a related guide | Another blog article |
| Mentioning brand values/mission | About page or brand story |

---

## CTA Placement

- **Soft CTA** after the 2nd or 3rd H2: mention a relevant product or collection naturally within the content flow. Not a sales pitch — a helpful suggestion. Example: "If you're looking for eczema-safe options, our [organic cotton collection](/collections/organic-cotton) is a good place to start."
- **Strong CTA** in the conclusion: direct link with clear action. Example: "Browse our full range of [organic kids' clothing](/collections/all) — free 30-day returns, 2-day delivery."

---

## SEO Metadata

Prepare these during the outline phase (finalize during writing):

### Title tag (50-60 characters)
- Include primary keyword near the start
- Use action-oriented language when possible
- Example: "Organic Cotton Kids Clothes: A Parent's Complete Guide"

### Meta description (150-160 characters)
- Include primary keyword
- Action-oriented: "Discover", "Learn", "Find out"
- Include a value prop or hook
- Example: "Discover why organic cotton is safer for kids with sensitive skin. Our guide covers materials, certifications, and what to look for — backed by real parent reviews."

### URL handle
- Short, keyword-rich, hyphens only
- Under 60 characters
- Strip filler words (a, the, and, of)
- Example: `organic-cotton-kids-clothes-guide`

---

## Outline Template

Present this to the user for approval:

```
TITLE: [50-60 chars, primary keyword near start]
META DESCRIPTION: [150-160 chars]
URL HANDLE: [short-keyword-slug]

TABLE OF CONTENTS
├── [H2 Section 1 title]
├── [H2 Section 2 title — question format for snippet]
├── [H2 Section 3 title]
│   ├── [H3 Subsection]
│   └── [H3 Subsection]
├── [H2 Section 4 title — question format for snippet]
├── [H2 Section 5 title]
└── [H2 Conclusion with CTA]

INTERNAL LINKS PLANNED:
- [anchor text] → [actual URL] (in Section X)
- [anchor text] → [actual URL] (in Section Y)
- ...

TARGET WORD COUNT: [based on SERP analysis]
FEATURED SNIPPET TARGETS: [which H2s, what format]
```

Wait for user approval. Adjust if they want to add, remove, or reorder sections.
