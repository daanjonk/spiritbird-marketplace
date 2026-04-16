# SpiritBird Marketplace for Claude Code

Expert Shopify automation plugins for Claude Code. AI-powered blog publishing, product image generation, and store intelligence — all connected to your Shopify store via native CLI.

**Created by [Daan Jonkman — SpiritBird](https://spiritbird.ai)**

---

## Installation

```bash
# Add marketplace
/plugin marketplace add daanjonk/spiritbird-marketplace

# Install all plugins
/plugin install shopify-brain@spiritbird-marketplace
/plugin install shopify-blog-publisher@spiritbird-marketplace
/plugin install ai-product-images@spiritbird-marketplace
/plugin install dataforseo@spiritbird-marketplace
/plugin install kie-ai@spiritbird-marketplace
```

Or from your terminal (single copy-paste):
```bash
claude plugin marketplace add daanjonk/spiritbird-marketplace && claude plugin install shopify-brain@spiritbird-marketplace && claude plugin install shopify-blog-publisher@spiritbird-marketplace && claude plugin install ai-product-images@spiritbird-marketplace && claude plugin install dataforseo@spiritbird-marketplace && claude plugin install kie-ai@spiritbird-marketplace
```

---

## Setup — After Installing

Copy this prompt into Claude Code and fill in your details:

```
Set up my SpiritBird marketplace. Here are my credentials:

1. Shopify store: YOUR-STORE.myshopify.com
2. DataForSEO login: YOUR-EMAIL
3. DataForSEO password: YOUR-API-PASSWORD
4. Kie AI API key: YOUR-API-KEY

Connect everything and tell me when you're done so I can spin up a new Claude session to verify it's working.
```

Claude will connect your Shopify store, set up the MCP servers, and confirm when everything is ready. You'll need to start a new Claude session after setup for the MCP connections to take effect.

**Where to get your credentials:**

| Credential | Where to get it |
|-----------|----------------|
| Shopify store domain | Your store URL (e.g. `my-brand.myshopify.com`) |
| DataForSEO login + password | [dataforseo.com](https://dataforseo.com) → Dashboard → API Access |
| Kie AI API key | [kie.ai/api-key](https://kie.ai/api-key) |

No technical setup needed — just provide your credentials and Claude handles the rest.

---

## Available Plugins

### Shopify Brain (2 skills)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| Setup | "build my vault", "setup" | Interactive onboarding — captures brand, customer, strategy into a structured vault |
| Assistant | "check in", "weekly review" | Daily driver — check-ins, experiment tracking, decision logging |

### Blog Publisher (1 skill, 6 phases)
| Phase | What it does |
|-------|-------------|
| Ideation | Get topic, set goal, choose autonomy level |
| Keyword Research | DataForSEO MCP — suggestions, difficulty, intent |
| SERP Analysis | Competitive content analysis + AI optimization |
| Outline | SEO-optimized heading structure with snippet targets |
| Writing | 1,500-2,500 word brand-aligned article |
| Image + Publish | Kie AI featured image → publish via Shopify CLI |

### AI Product Images (1 skill, 4 modes)
| Mode | Best for |
|------|----------|
| Mode A — Model + Product | Wearable products with model reference photos |
| Mode B — Image-to-image | Non-wearable products, background swap |
| Mode C — Text-to-image | New products with no existing photo (fallback) |
| Mode D — UGC Style | Social media, mirror selfies, lifestyle content |

### MCP Servers
| Plugin | What it provides |
|--------|-----------------|
| **dataforseo** | Keyword research, SERP data, backlinks, on-page analysis |
| **kie-ai** | AI image generation with 20+ models (Nano Banana Pro, Seedream 5, Flux 2, Imagen 4, etc.) |

---

## Required Connections by Plugin

| Plugin | Required | Get Access |
|--------|----------|------------|
| **shopify-brain** | Shopify CLI | [Shopify CLI](https://shopify.dev/docs/api/shopify-cli) |
| **shopify-blog-publisher** | Shopify CLI, DataForSEO MCP, Kie AI MCP | [DataForSEO](https://dataforseo.com), [Kie AI](https://kie.ai/api-key) |
| **ai-product-images** | Shopify CLI, Kie AI MCP | [Kie AI](https://kie.ai/api-key) |
| **dataforseo** | DataForSEO account | [DataForSEO](https://dataforseo.com) |
| **kie-ai** | Kie AI API key | [Kie AI](https://kie.ai/api-key) |

---

## Updating

```bash
/plugin update shopify-brain@spiritbird-marketplace
/plugin update shopify-blog-publisher@spiritbird-marketplace
/plugin update ai-product-images@spiritbird-marketplace
/plugin update dataforseo@spiritbird-marketplace
/plugin update kie-ai@spiritbird-marketplace
```

---

## Support

- Issues: [github.com/daanjonk/spiritbird-marketplace/issues](https://github.com/daanjonk/spiritbird-marketplace/issues)
- Website: [spiritbird.ai](https://spiritbird.ai)
- Email: daan@spiritbird.ai
