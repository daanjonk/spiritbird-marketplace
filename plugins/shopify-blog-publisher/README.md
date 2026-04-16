# Shopify Blog Publisher — Claude Code Plugin

An end-to-end blog publishing plugin for Claude Code. Takes a blog idea from keyword research through SEO-optimized writing, AI image generation, and publishing to Shopify — all in one conversational flow.

## What It Does

1. **Keyword Research** — Uses DataForSEO MCP for keyword discovery, difficulty, and intent analysis
2. **SERP & Competitive Analysis** — Analyzes top-ranking content for structure and gaps
3. **Outline & Structure** — Builds an SEO-optimized outline with featured snippet targets
4. **Blog Writing** — Writes a brand-aligned, SEO-optimized article (1,500-2,500 words)
5. **Image Generation** — Creates a featured image using Kie AI MCP
6. **Publish to Shopify** — Pushes the finished article to your Shopify blog via Shopify CLI

## Prerequisites

| Requirement | What For | Setup |
|-------------|----------|-------|
| **Shopify CLI** | Publishing blog articles, fetching store data | `shopify store auth --store <your-store>.myshopify.com --scopes write_content,read_content,read_products` |
| **DataForSEO MCP** | Keyword research, SERP analysis, AI optimization | Connect in Claude Code MCP settings |
| **Kie AI MCP** | Featured image generation | Connect in Claude Code MCP settings |

No custom apps, no API keys in config files, no environment variables needed. The Shopify CLI and MCP servers handle all authentication.

## Installation

```bash
# Add the marketplace (one time)
/plugin marketplace add daanjonk/spiritbird-marketplace

# Install this plugin
/plugin install shopify-blog-publisher@spiritbird-marketplace
```

## Usage

Once installed, just tell Claude:

- "Write a blog post about [topic]"
- "Publish a new blog article for my store"
- "Do keyword research for [topic] and write a blog"
- "New blog post"

Claude will walk you through each phase. You can choose your autonomy level:
1. **Full autopilot** — research, write, generate image, save as draft
2. **Outline check + final review** — pause at outline and final article
3. **Full control** — approve every step

## Customization

### Target a different market

The default market is US/English. Override per-request:

> "Write a blog post about sustainable fashion, target the German market"

Common markets: United Kingdom, Netherlands ("nl"), Germany ("de"), France ("fr"), Canada, Australia.

### Skip phases

- "Skip keyword research, I already know I want to target 'organic cotton t-shirts'"
- "Don't generate an image, I'll add one manually"
- "Just write the article, don't publish yet"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "shopify store execute" fails | Run `shopify store auth --store <store>.myshopify.com --scopes write_content,read_content,read_products` |
| Article creation fails with scope error | Ensure `write_content` scope is included in your auth |
| DataForSEO errors | Check that the DataForSEO MCP is connected and your account has API credits |
| Kie AI not working | Check that the Kie AI MCP is connected in Claude Code |

## Credits

Created by [Daan Jonkman — SpiritBird](https://spiritbird.ai)

## License

MIT
