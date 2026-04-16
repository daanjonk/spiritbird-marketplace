# Shopify Blog Publisher — Claude Skill

An end-to-end blog publishing skill for Claude (Cowork / Claude Code). Takes a blog idea from keyword research through SEO-optimized writing, AI image generation, and publishing to Shopify — all in one conversational flow.

## What It Does

1. **Keyword Research** — Uses DataForSEO to find high-opportunity keywords for your blog topic
2. **Blog Writing** — Writes an SEO-optimized article based on the research
3. **Image Generation** — Creates a featured image using Kie AI
4. **Publish to Shopify** — Pushes the finished article to your Shopify blog

## Requirements

You'll need accounts with these services:

| Service | What For | Sign Up |
|---------|----------|---------|
| **Shopify** | Publishing blog articles | You probably already have this |
| **DataForSEO** | Keyword research & search volume data | https://dataforseo.com |
| **Kie AI** | Featured image generation (MCP) | Install via Claude MCP marketplace |

## Setup

### Step 1: Install the skill

Copy the `shopify-blog-publisher/` folder into your Claude workspace:

```
.claude/skills/shopify-blog-publisher/
├── SKILL.md
├── README.md
├── .env.example
└── scripts/
    ├── shopify.py
    └── dataforseo.py
```

### Step 2: Create a Shopify Custom App

1. Go to your Shopify admin → **Settings** → **Apps and sales channels** → **Develop apps**
2. Click **Create an app**, give it a name (e.g., "Blog Publisher")
3. Under **Configuration**, add the following API scopes:
   - `write_content` (required — for creating blog articles)
   - `read_content` (required — for listing articles)
4. Click **Install app**
5. Note down your **Client ID** and **Client Secret** from the API credentials page

### Step 3: Find your Blog ID

1. In Shopify admin, go to **Online Store** → **Blog posts**
2. Click on the blog name (e.g., "News") in the sidebar
3. Look at the URL — it'll be something like: `https://your-store.myshopify.com/admin/blogs/123456789`
4. The number at the end (`123456789`) is your Blog ID

### Step 4: Get DataForSEO credentials

1. Sign up at https://dataforseo.com
2. Go to your dashboard → **API Access**
3. Note your **login email** and **API password**

### Step 5: Set environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Then edit `.env` with your credentials. How you load these depends on your setup:

**Option A: Export in your shell profile** (`.bashrc`, `.zshrc`):
```bash
export SHOPIFY_STORE="your-store.myshopify.com"
export SHOPIFY_BLOG_ID="123456789"
export SHOPIFY_CLIENT_ID="your-client-id"
export SHOPIFY_CLIENT_SECRET="your-client-secret"
export DATAFORSEO_LOGIN="your@email.com"
export DATAFORSEO_PASSWORD="your-api-password"
```

**Option B: Use a `.env` file** with a tool that loads it (e.g., `direnv`, `dotenv`).

### Step 6: Install Kie AI MCP

Install the Kie AI MCP connector in your Claude workspace. This provides the image generation tools used in Phase 3 of the skill.

## Usage

Once set up, just tell Claude:

- "Write a blog post about [topic]"
- "Publish a new blog article for my store"
- "Do keyword research for [topic] and write a blog"
- "New blog post"

Claude will walk you through each phase, asking for approval before publishing.

## Customization

### Target a different market

The default market is US/English. Override per-request:

> "Write a blog post about sustainable fashion, target the German market"

Or change the defaults in the script arguments. Common location codes:

| Country | Code | Language |
|---------|------|----------|
| United States | 2840 | en |
| United Kingdom | 2826 | en |
| Netherlands | 2528 | nl |
| Germany | 2276 | de |
| France | 2250 | fr |
| Canada | 2124 | en / fr |
| Australia | 2036 | en |

### Change blog structure

The default structure is defined in SKILL.md under Phase 2. You can edit it to match your brand's style guide, preferred word count, tone, etc.

### Skip phases

You can tell Claude to skip any phase:

- "Skip keyword research, I already know I want to target 'organic cotton t-shirts'"
- "Don't generate an image, I'll add one manually"
- "Just write the article, don't publish yet"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing required environment variables" | Check that all env vars from `.env.example` are set and exported |
| Shopify 401 error | Your client credentials may be wrong, or the app isn't installed |
| Shopify 403 error | Your Custom App is missing the `write_content` scope |
| DataForSEO errors | Check your login/password, and that your account has API credits |
| Kie AI not working | Make sure the Kie AI MCP is installed in your Claude workspace |

## License

MIT — use it however you want.
