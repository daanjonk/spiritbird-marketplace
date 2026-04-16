---
name: shopify-blog-publisher
description: End-to-end Shopify blog article publisher. Handles keyword research (DataForSEO), blog writing, featured image generation (Kie AI), and publishing to Shopify — all in one flow. Use this skill whenever the user wants to publish a blog post to their Shopify store, write a blog article for Shopify, do keyword research for a blog, or says things like "publish a blog", "new blog post", "write an article for the shop", "blog for Shopify", "create a blog post", or any variation of wanting to research, write, and publish blog content to their Shopify webshop.
---

# Shopify Blog Publisher

Publishes a complete, SEO-optimized blog article to a Shopify store in one flow: keyword research, writing, image generation, and publishing.

## Prerequisites

Before using this skill, you need:

1. **Shopify store** with a Custom App that has `write_content` scope (see README.md)
2. **DataForSEO account** for keyword research (https://dataforseo.com)
3. **Kie AI MCP** installed in your Claude workspace for image generation

Set your credentials as environment variables — see the `.env.example` file included in this skill.

## The Flow

```
1. Keyword Research (DataForSEO)
   → Find the right topic angle and keywords
2. Blog Writing
   → Write the article optimized for the researched keywords
3. Image Generation (Kie AI)
   → Create a featured image for the post
4. Publish to Shopify
   → Push the finished article live on the store
```

Each phase builds on the previous one. Don't skip phases unless the user explicitly says to.

---

## Phase 1: Keyword Research (DataForSEO)

Use the `scripts/dataforseo.py` script for all DataForSEO API calls. The script handles auth and response parsing.

### Step 1: Get the seed keyword from the user

Ask the user for a topic or seed keyword. If they've already provided one, use it.

### Step 2: Run keyword suggestions

```bash
python3 <skill-path>/scripts/dataforseo.py suggestions "<seed_keyword>" --location <location_code> --language <language_code> --limit 20
```

This returns keyword suggestions with search volume, CPC, and competition.

Default: location 2840 (United States), language en (English). Override per request — e.g., Netherlands = 2528 / nl, UK = 2826 / en, Germany = 2276 / de.

### Step 3: Run search volume for promising keywords

Pick the 5-10 most relevant keywords from suggestions and get precise search volume:

```bash
python3 <skill-path>/scripts/dataforseo.py volume "<keyword1>,<keyword2>,<keyword3>" --location <location_code> --language <language_code>
```

### Step 4: Run related keywords for additional angles

```bash
python3 <skill-path>/scripts/dataforseo.py related "<seed_keyword>" --location <location_code> --language <language_code> --limit 10
```

### Step 5: Present findings to the user

Show a clean summary table:

| Keyword | Search Volume | Competition | CPC |
|---------|--------------|-------------|-----|

Recommend a primary keyword and 3-5 secondary keywords. Explain why — search volume, competition level, and relevance to their store. Let the user confirm or adjust before moving to writing.

---

## Phase 2: Blog Writing

Write the blog article optimized for the chosen keywords. The user may have specific blog preferences configured — check with them if this is the first run.

### Default blog structure (if no preferences set yet):

1. **Title** — Include primary keyword, keep under 70 characters
2. **Meta description** — 150-160 characters, includes primary keyword
3. **Introduction** — Hook the reader, introduce the topic, mention primary keyword naturally
4. **H2 sections** (3-5) — Each addresses a subtopic, weave in secondary keywords
5. **Conclusion** — Summarize key points, include a CTA
6. **Tags** — Relevant tags based on keywords and topic

### SEO guidelines:

- Primary keyword in title, first paragraph, and at least 2 H2 headings
- Secondary keywords distributed naturally throughout
- Use internal linking placeholders: `[INTERNAL LINK: related product/collection]`
- Keep paragraphs short (2-3 sentences)
- Include alt text suggestions for images
- Aim for 800-1500 words depending on topic complexity

### Output format:

Present the complete article to the user in a clean format. Include:
- Suggested title
- Meta description
- Full article body (HTML-ready)
- Suggested tags

Wait for the user to approve or request changes before proceeding.

---

## Phase 3: Image Generation (Kie AI)

Generate a featured image using the `mcp__kie-ai__generate_nano_banana` tool.

### Step 1: Craft the image prompt

Based on the blog topic and content, create a descriptive image prompt. Consider:
- The blog's main theme and mood
- Brand style (if defined — check with user)
- What would look good as a blog header/featured image

### Step 2: Generate the image

Use the MCP tool:
```
mcp__kie-ai__generate_nano_banana(prompt="<your detailed image prompt>")
```

This returns a task_id. Poll for completion:
```
mcp__kie-ai__get_task_status(task_id="<task_id>")
```

Poll every 5-10 seconds until the status is complete. The result will contain an image URL.

### Step 3: Present to user

Show the generated image and ask if they're happy with it. Offer to regenerate with a different prompt if needed.

---

## Phase 4: Publish to Shopify

Use the `scripts/shopify.py` script for Shopify API calls. It handles OAuth token exchange and article creation.

### Step 1: Get a fresh access token

```bash
python3 <skill-path>/scripts/shopify.py auth
```

Tokens expire every 24 hours, so always get a fresh one before publishing.

### Step 2: Create the article

```bash
python3 <skill-path>/scripts/shopify.py publish \
  --token "<access_token>" \
  --title "<article title>" \
  --body "<html body>" \
  --tags "<tag1,tag2,tag3>" \
  --image-url "<featured image url>" \
  --published true
```

Set `--published false` if the user wants to save as draft first.

### Step 3: Confirm publication

Show the user:
- Article URL on the store
- Title and status (published/draft)
- Offer to make it a draft if they published by accident

---

## Configuration

All configuration is done via environment variables. See `.env.example` for the full list.

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `SHOPIFY_STORE` | Your store domain (e.g., `your-store.myshopify.com`) |
| `SHOPIFY_BLOG_ID` | The blog ID to publish to (find in Shopify admin URL) |
| `SHOPIFY_CLIENT_ID` | Custom App client ID |
| `SHOPIFY_CLIENT_SECRET` | Custom App client secret |
| `DATAFORSEO_LOGIN` | Your DataForSEO login email |
| `DATAFORSEO_PASSWORD` | Your DataForSEO API password |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SHOPIFY_API_VERSION` | `2025-01` | Shopify Admin API version |
| `DATAFORSEO_AUTH_TOKEN` | — | Pre-encoded Base64 token (alternative to login+password) |

### Default Market

- **Location**: United States (code 2840)
- **Language**: English (code en)

The user can override these per-request (e.g., "target the Netherlands market" → location 2528, language nl).

### Common Location Codes

| Country | Code | Language |
|---------|------|----------|
| United States | 2840 | en |
| United Kingdom | 2826 | en |
| Netherlands | 2528 | nl |
| Germany | 2276 | de |
| France | 2250 | fr |
| Canada | 2124 | en / fr |
| Australia | 2036 | en |

---

## Error Handling

- **DataForSEO fails**: Check if the API returns status_code != 20000. Show the error to the user.
- **Shopify token expired**: Re-run `shopify.py auth` to get a fresh token.
- **Shopify publish fails**: Check the HTTP status and error message. Common issues: missing required fields, HTML validation errors.
- **Kie AI generation fails**: Retry with a simplified prompt. If persistent, let the user know and offer to publish without an image.
- **Missing credentials**: The scripts will tell you exactly which environment variables are missing.
- **Network errors**: Retry once, then inform the user.
