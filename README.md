# SpiritBird Marketplace for Claude Code

A curated plugin marketplace for Shopify store owners using Claude Code. One command to add the marketplace, then install the plugins you need.

**Created by [Daan Jonkman — SpiritBird](https://spiritbird.ai)**

---

## Quick Start

### Step 1: Add the marketplace

```bash
/plugin marketplace add daanjonk/spiritbird-marketplace
```

### Step 2: Install the plugins you want

```bash
# The AI brain for your Shopify store
/plugin install shopify-brain@spiritbird-marketplace

# Publish SEO-optimized blog posts to Shopify
/plugin install shopify-blog-publisher@spiritbird-marketplace

# Generate AI product images for Shopify
/plugin install ai-product-images@spiritbird-marketplace

# Standalone MCP servers (also bundled with the plugins above)
/plugin install dataforseo@spiritbird-marketplace
/plugin install kie-ai@spiritbird-marketplace
```

### Step 3: Set your environment variables

The MCP servers need API credentials. Set these in your environment or `.env` file:

```bash
# DataForSEO (for keyword research & SEO data)
export DATAFORSEO_USERNAME="your_api_login"
export DATAFORSEO_PASSWORD="your_api_password"
# Get credentials at https://dataforseo.com → API Access tab

# Kie AI (for AI image generation)
export KIE_AI_API_KEY="your_api_key"
# Get your key at https://kie.ai/api-key
```

That's it. You're ready to go.

---

## What's Included

### Plugins (Skills)

| Plugin | What it does | Triggers |
|--------|-------------|----------|
| **shopify-brain** | Builds a personalized AI brain for your store. Interactive onboarding captures your brand, customer, and strategy. A daily assistant keeps it alive with check-ins, weekly reviews, and decision logging. | "setup", "build my vault", "check in", "weekly review" |
| **shopify-blog-publisher** | End-to-end blog publishing: keyword research (DataForSEO) → writing → image generation (Kie AI) → publish to Shopify. One flow. | "publish a blog", "new blog post", "write an article" |
| **ai-product-images** | Generate studio-style, UGC, or model+product AI images and upload them directly to your Shopify products. | "generate product images", "create product photos" |

### MCP Servers

| Server | What it provides | Required by |
|--------|-----------------|-------------|
| **dataforseo** | Real-time keyword research, SERP data, backlinks, on-page analysis, content analysis, and more. | shopify-blog-publisher |
| **kie-ai** | AI image generation and editing with 20+ models (Nano Banana Pro, Seedream 5 Lite, Flux 2 Pro, Imagen 4, Ideogram V3, etc.) | shopify-blog-publisher, ai-product-images |

MCP servers are auto-configured when you install a plugin that needs them. You can also install them standalone if you just want the raw MCP tools.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [Node.js](https://nodejs.org/) v18+ (for MCP servers via npx)
- A Shopify store (for the Shopify plugins)
- API credentials for the services you want to use (see Step 3 above)

---

## Plugin Details

### Shopify Brain

Two skills:
- **Setup** — One-time interactive onboarding. Builds an Obsidian-style vault with your brand voice, ICP, channels, competitors, and strategy. Three tiers: Foundation (5 min), Growth (12 min), Full Brain (18 min).
- **Assistant** — Daily driver. Check-ins, weekly reviews, experiment tracking, decision logging. Automatically loads your vault context every session.

### Shopify Blog Publisher

One skill, four phases:
1. **Keyword Research** — Uses DataForSEO to find the right topic and keywords
2. **Blog Writing** — Writes an SEO-optimized article
3. **Image Generation** — Creates a featured image via Kie AI
4. **Publish** — Pushes the article live on your Shopify store

Requires: Shopify Custom App with `write_content` scope, DataForSEO account, Kie AI API key.

### AI Product Images

One skill, four modes:
- **Mode A** — Model + Product (best quality, needs model reference photos)
- **Mode B** — Image-to-image (recreates existing product photos on white background)
- **Mode C** — Text-to-image (generates from product description only)
- **Mode D** — UGC Style (mirror selfies, lifestyle shots)

Requires: Shopify Custom App with `read_products`, `write_products`, `write_files` scopes, Kie AI API key.

---

## Updating

To get the latest versions:

```bash
/plugin update shopify-brain@spiritbird-marketplace
/plugin update shopify-blog-publisher@spiritbird-marketplace
/plugin update ai-product-images@spiritbird-marketplace
```

---

## Support

- Issues: [github.com/daanjonk/spiritbird-marketplace/issues](https://github.com/daanjonk/spiritbird-marketplace/issues)
- Website: [spiritbird.ai](https://spiritbird.ai)
- Email: daan@spiritbird.ai
