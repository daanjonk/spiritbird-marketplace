---
name: brand-ads-generate
description: Generate on-brand paid-ad creative variations from your reference images plus cross-industry inspiration, with on-image CTA text rendered inline by an image-to-image model. Reads a brand vault under ./Brand/ for voice, visual identity, and guardrails so output is on-brand without manual prompt engineering. On first run in a fresh workspace, walks the user through ~7 onboarding questions and scaffolds the vault. Trigger when the user says "generate ads", "create ad variations", "make me 5 static ads", "test new ad creative", "static ad with CTA", or any variation of producing paid-media static creative for their brand. Do NOT trigger for video/Reels/TikTok scripts, ad performance audits, organic UGC briefs, or new product photography from scratch.
---

# brand-ads-generate — Universal Static Ad Creative + On-Image CTA

Turn your brand's image stack (reference + lifestyle anchors) plus cross-industry inspiration into testable static ad variations. Renders the on-image CTA text inline via the user's chosen image-to-image model — no Photoshop, no Figma, no After Effects. Every variation is logged to a per-run `BRIEF.md` so the next test cycle can iterate.

The skill reads brand context from a workspace-local `Brand/` folder. On first run in a fresh workspace, it conversationally onboards the user and writes the vault stubs itself. The companion methodology is documented in `Ad-Generation-Method.md` (in this skill's repo, also [available here](Ad-Generation-Method.md) — read it once for the why).

The single rule (load the user's "good ad" rule from `Brand/ad-playbook.md` and pressure-test against it before every render).

---

## When to use

- "generate ads", "create ad variations", "make me 5 ads"
- "test a new CTA on the [scene] shot"
- "static ad with [CTA] on top"
- Any time the user wants paid-media static images for their brand

## When NOT to use

- Video / Reels / TikTok scripts → use the user's `Brand/ad-playbook.md` directly, no skill needed
- Ad performance audits → out of scope
- New product photography from scratch → use a product-image generator
- Anything that crosses brand boundaries (this skill is one-workspace-one-brand by design)

---

## Step 0 — Pre-flight

### 0a. Verify the Kie AI MCP is available

Check that `mcp__kie-ai__kie_generate_image` and `mcp__kie-ai__kie_get_task_status` are callable in this session. If either is missing, halt with:

> **This skill needs the Kie AI MCP server.** It's not currently available in this session. The easiest way to install it is via the SpiritBird marketplace (which is also where this skill came from):
>
> ```
> /plugin install kie-ai@spiritbird-marketplace
> ```
>
> You'll be prompted for a Kie AI API key — get one at https://kie.ai/api-key. Restart your Claude session after install so the MCP connection initializes, then re-run this skill.
>
> If you're not using the SpiritBird marketplace, see https://docs.kie.ai/mcp for manual MCP setup.

Do not attempt to substitute a different image-generation tool — the prompt template, polling pattern, and aspect-ratio handling are all written for Kie AI's API.

### 0b. Discover the brand vault

Look for a `Brand/` folder under the current working directory. Two outcomes:

- **Vault exists** (`./Brand/` is a directory containing at least `visual-identity.md`, `customer-voice.md`, `ad-playbook.md`, and `guardrails.md`) → skip to Step 0c.
- **Vault missing or incomplete** → run **Onboarding** (see below) before proceeding.

### 0c. Load brand context

Read these four files in order; they are the load-bearing context for every render:

1. `./Brand/ad-playbook.md` — CTA tiers, the "good ad" rule, words-to-avoid, char-limit guidance
2. `./Brand/customer-voice.md` — verbatim quote block (used for auto-CTA)
3. `./Brand/guardrails.md` — non-negotiable "never do" rules
4. `./Brand/visual-identity.md` — accent hex, on-image typeface, do/don't list

Also read (compressed into the BRAND paragraph in PART 1 of the prompt):
- `./Brand/icp.md`
- `./Brand/tone-of-voice.md`
- `./Brand/positioning.md` (optional — only if it exists)

If any **required** file (the four above) is missing or has an empty required section, warn the user, name the missing piece, and offer to scaffold it via Onboarding. Don't silently proceed with degraded context.

### 0d. Parse the hosted-URL table

Read `./Images/hosted-urls.md` and build an in-memory map of `local_path → cdn_url`. This is the single source of truth — never re-upload a file that already has a row. If the file doesn't exist or is empty, halt with:

> No hosted images found at `./Images/hosted-urls.md`. Add at least one reference-pack image and one inspiration image to your CDN, register them in `hosted-urls.md`, then re-run.

The skill itself never uploads. Hosting is hosting-agnostic — Shopify Files, Cloudinary, S3, imgur, anything that gives a public URL.

---

## Onboarding (first run only — when vault is missing)

Walk the user through 7 questions via `AskUserQuestion`. After all answers, write the vault to `./Brand/` and the scaffolding to `./Images/` based on the brand-vault-template structure. Then loop back into the main flow with a short "Vault scaffolded. Drop reference + inspiration images into `./Images/reference-pack/` and `./Images/Creative ideas/`, host them on your CDN, register them in `./Images/hosted-urls.md`, then re-run me."

The 7 questions:

1. **Brand name and one-liner.** Free text. Example: *"Fox · athletic apparel for the gym-as-identity generation, ages 18–35"*.
2. **Visual signature — accent color, typeface, accent rule.** Three sub-fields:
   - Accent hex (default: `#000000` = no signature accent)
   - On-image typeface (default: `Inter`, suggest `Bebas Neue` for athletic / streetwear, `Helvetica Neue` for clean DTC, `Playfair Display` for editorial / beauty)
   - One-line accent rule (default: *"the accent appears in every frame as a small signal — never as a body fill, background, or color wash"*)
3. **Ideal customer (ICP).** Free text, 2–3 sentences. Who actually buys?
4. **Voice in one line.** Free text. Example: *"the friend at the gym three years deeper than you — cuts the BS, hypes you up without preaching"*.
5. **5–10 verbatim customer quotes.** Free text, paste-able block. Prompt: *"Real lines from reviews, Reddit, YouTube comments, support tickets, sales calls. The more verbatim, the better. Quote them as written, typos and all — that's the voice that converts."*
6. **3–5 forbidden words/phrases.** Free text, comma-separated. Default-prefilled with the universally-bad CTA set: *introducing, elevate, premium, discover, experience, unleash, transform, revolutionary, shop now, limited time, click the link, don't miss out, swipe up*. The user can extend, replace, or accept.
7. **The "good ad" rule.** Free text, one sentence. Prompt: *"What's the one rule that, if broken, means the ad failed regardless of metrics? For Fox it's 'if it looks like an ad, it fails'. For your brand it might be different."*

After collecting answers, write these files (use the templates under `brand-vault-template/` next to this SKILL.md as the structural base — when this skill is installed via the SpiritBird marketplace, the templates are at `${CLAUDE_PLUGIN_ROOT}/skills/brand-ads-generate/brand-vault-template/`; substitute the user's answers into the appropriate sections):

```
./CLAUDE.md                          ← routing index (template, with brand name + one-liner substituted)
./Brand/tone-of-voice.md             ← voice one-liner from Q4 + style defaults stub
./Brand/customer-voice.md            ← verbatim block from Q6 in the "Verbatim Hook Material" section
./Brand/visual-identity.md           ← accent hex + typeface + accent rule from Q2 + do/don't stub
./Brand/guardrails.md                ← forbidden words from Q6 + good-ad rule from Q7 + 3-5 placeholder rules to fill in
./Brand/ad-playbook.md               ← good-ad rule + Soft/Moderate/Direct CTA tier examples sourced from Q5 quotes
./Brand/icp.md                       ← ICP from Q3
./Brand/positioning.md               ← stub with prompts for the user to fill in later
./Images/CLAUDE.md                   ← from template, hosting-agnostic conventions
./Images/hosted-urls.md              ← from template, empty tables + upload procedure
./Images/reference-pack/.gitkeep
./Images/Creative ideas/.gitkeep
./Images/ads/.gitkeep
```

After writing, surface a one-liner of next steps (drop images, host them, register, re-run).

---

## Step 1 — Ask: source image(s)

Use `AskUserQuestion`. Build options dynamically from the `hosted-urls.md` map:

- If the table has a `reference-pack/` section, offer "Reference-pack image(s)" with the first 1-2 listed as default suggestions
- If the table has a `lifestyle-pack/` section (or any post-reference-pack section the user has added), offer "Lifestyle-pack image(s)" with the first 2 listed
- Always offer the third option "Both — lifestyle for scene, reference as character anchor"

Map every selected file through the `hosted-urls.md` table to its public URL.

**If a chosen file isn't in the table:** halt the skill and tell the user: *"`<filename>` isn't registered in `Images/hosted-urls.md`. Upload it to your CDN using whatever uploader you have (Shopify CLI, Cloudinary, S3, etc.), add the row to the table, then re-run."* Do not call any upload flow inline.

---

## Step 2 — Ask: CTA copy mode

Use `AskUserQuestion` with two options:

### Option A — Auto-generate (5–8 variants)

Draft variants by sampling across the three tiers from the user's `ad-playbook.md` (Soft / Moderate / Direct) and the verbatim quote block from `customer-voice.md`. Suggested mix per run:

- **3 Soft** (default for cold/top-of-funnel): drawn from the `ad-playbook.md` Soft tier examples + verbatim quotes from `customer-voice.md` that fit Soft framing (peer testimonial, "I tried…", "100% recommend…")
- **2 Moderate** (warm/retargeting): drawn from the Moderate tier examples
- **1 Direct** (bottom-funnel only, off-default): from the Direct tier — flag this one explicitly so the user can drop it if they're cold-targeting

For each variant, output a row:

```
| # | Tier     | Source                                                    | CTA on image                                  | Char count |
|---|----------|-----------------------------------------------------------|-----------------------------------------------|------------|
| 1 | Soft     | customer-voice.md "Finally fits my shoulders..."          | FINALLY FITS MY SHOULDERS                     | 25         |
| 2 | Soft     | ad-playbook.md soft tier "link's in my bio"               | LINK'S IN MY BIO                              | 17         |
| ... |        |                                                           |                                               |            |
```

Show the table to the user; let them edit, drop rows, or add their own before generation.

### Option B — User-supplied

User gives one CTA line. Skill renders N variants of the same CTA in different placements (top-third / bottom-third / mid-overlay) and styles per the user's `visual-identity.md` accent rules (e.g. white type with accent underline / black type on accent swatch).

### Validate every CTA against the forbidden-words list

Read the "Words to AVOID" block from `./Brand/ad-playbook.md` plus any additional bans in `./Brand/guardrails.md`. Reject (or warn + ask before proceeding) any CTA containing those words.

If the user's vault has no explicit list, fall back to this universally-bad baseline:

**Corporate jargon:** introducing, elevate, premium, discover, experience, unleash, transform your, scientifically proven, clinically tested, proprietary, revolutionary, breakthrough, cutting-edge, world-class, best-in-class

**CTA clichés:** shop now, buy today, limited time, click the link, limited stock, act fast, don't miss out, tap here, swipe up to save

**Comparative claims:** better than [competitor], X times more effective, the only product that, nothing else compares

**Body-shaming / appearance / medical:** any weight-loss, fat-loss, slimming framing; cures / treats / prevents / heals / detoxifies

**Length limits** (applied to on-image text length):
- Headline-style on-image text: **≤40 chars** hard cap (legibility on 9:16)
- Long overlay (bottom-third caption): **≤125 chars**

If a user-supplied CTA fails validation, name the violated rule and the source line in `ad-playbook.md` (or note that it came from the universal baseline if the user's playbook didn't specify).

---

## Step 3 — Ask: aspect ratios

Use `AskUserQuestion`, multi-select, options: `9:16`, `4:5`, `1:1`.

Default suggestion: **`9:16`** — matches Meta Reels + TikTok + Stories, the highest-volume paid surfaces in 2025–26.

---

## Step 3.5 — Ask: image model

Use `AskUserQuestion`, single-select, exactly three options in this order:

1. **GPT Image 2 image-to-image** (`gpt-image-2-image-to-image`) — *Recommended.* OpenAI GPT Image 2; strongest on-image text rendering, holds up well at 29–30 char CTAs, clean kerning. Good default for any brand where the CTA text is the headline.
2. **Nano Banana Pro** (`nano-banana-pro`) — Google DeepMind. Sharper 2K/4K output, supports up to 8 reference images. Higher cost (~$0.09–$0.12). Pick when you want the highest-fidelity render or need to pass extra anchor references.
3. **Seedream 5 Lite image-to-image** (`seedream/5-lite-image-to-image`) — ByteDance. Most photorealistic UGC scene mood, but weaker on longer text. Pick only when CTAs are ≤25 chars and the scene needs to feel hyper-natural.

Do **not** silently default to one of these — always ask. Do **not** offer a fourth model.

---

## Step 3.6 — Cost gate

Calculate generation count:

```
calls = len(source_images) × len(approved_ctas) × len(ratios)
```

If `calls > 12`, **confirm with the user before proceeding.** Show: number of calls, the source-image / CTA / ratio matrix, the chosen model, an explicit "OK to proceed?" prompt.

---

## Step 4 — Generate

For each `(source_url, cta_text, ratio)` triple, use the model the user picked in Step 3.5. No silent fallback to a different model — if the chosen model produces garbled text on the first render, surface the issue to the user and ask whether to re-render with a different model rather than swapping silently.

### Build the Kie AI prompt

Three-part structure, in this order. Substitute the bracketed placeholders from the brand vault.

```
PART 1 — preserve the source scene
"Preserve the {scene_descriptor} composition from the reference image:
the model's pose, framing, lighting, {brand_mark} placement, and the
existing {accent_color_name} ({accent_hex}) accent on the {accent_location}.
Do not re-style the person, do not change wardrobe color, do not crop the face."

PART 2 — add the on-image CTA
"Render the text '{CTA_TEXT}' as a native UGC text overlay in the
{placement_zone} (top-third / bottom-third / mid). Use {on_image_typeface}
all-caps with tight tracking (-25 to -50). White type. Add a single
{accent_color_name} accent ({accent_hex}) underline beneath ONE word — pick
the verb or the most emotional noun. TikTok-caption / Instagram-sticker
style — never a corporate brand graphic. No drop shadows, no boxes, no glow,
no motion-graphic effects, no kerning artifacts."

PART 3 — visual identity guardrails (read from visual-identity.md)
"{accent_color_name} accent rules from visual-identity.md:
- The accent MUST appear in the frame at least once (logo accent, trim,
  or the CTA underline counts)
- The accent is NEVER {forbidden_accent_uses — e.g. 'a body fabric color,
  a hero background, a color grade, a gradient, or a wash on the photo'}
- Color grade: {photography_mood — e.g. 'cool, desaturated, lifted blacks,
  crushed shadows'}
- Match the photography mood of the source image — if the source is a
  natural-light gym mirror selfie, keep it natural-light, not studio."
```

Placeholder sourcing:

| Placeholder | Source |
|---|---|
| `{scene_descriptor}` | Derived from the source filename (e.g. `07-gym-locker-mirror` → "gym locker mirror selfie") |
| `{brand_mark}` | "Logo" + brand name from `Brand/visual-identity.md` (e.g. "F7 Fox logo") |
| `{accent_hex}`, `{accent_color_name}`, `{accent_location}` | From `Brand/visual-identity.md` Color System section |
| `{on_image_typeface}` | From `Brand/visual-identity.md` Typography → Display |
| `{forbidden_accent_uses}` | From `Brand/visual-identity.md` "Where the accent does NOT live" section |
| `{photography_mood}` | From `Brand/visual-identity.md` Photography → Mood |
| `{placement_zone}` | For Option A auto-CTAs, cycle through top-third / bottom-third / mid-overlay across variants so the user sees placement diversity |

If any of the visual-identity sections are missing, fall back to a sensible neutral default (white type, no accent underline, photography mood "natural-light, true-color, no heavy grade") and warn in the BRIEF that the visual-identity section needs filling in.

### Call Kie AI

Use `mcp__kie-ai__kie_generate_image`:

```json
{
  "model": "<model picked in Step 3.5 — e.g. gpt-image-2-image-to-image>",
  "prompt": "<the three-part prompt from above>",
  "image_urls": ["<source_cdn_url>", "<optional_reference_anchor_url>"],
  "aspect_ratio": "9:16"
}
```

Model-specific knobs:
- `gpt-image-2-image-to-image` — no extra params; `aspect_ratio` controls output ratio.
- `nano-banana-pro` — add `"resolution": "2K"` (or `"4K"` if the user explicitly wants the cost bump).
- `seedream/5-lite-image-to-image` — add `"quality": "high"` for 4K output.

### Poll for the result

Use `mcp__kie-ai__kie_get_task_status` every **30 seconds**, with exponential backoff after 3 consecutive failures (60s → 120s → 240s, then surface the error). Typical completion is 150–250s.

### Save the output

Path convention:

```
./Images/ads/
└── <YYYY-MM-DD-HHMM>/                ← run timestamp
    ├── BRIEF.md                       ← one per run, written in Step 5
    └── <concept-slug>/                ← e.g. "gym-locker-mirror"
        └── <ratio-slug>/              ← "9-16", "4-5", "1-1"
            ├── soft-1.png
            ├── soft-2.png
            ├── moderate-1.png
            └── direct-1.png
```

`<cta-tier>` values: `soft`, `moderate`, `direct`, or `custom` (Option B user-supplied).

---

## Step 5 — Write the run BRIEF.md

After all generations finish, write `./Images/ads/<run-timestamp>/BRIEF.md`:

```markdown
# Run BRIEF — <YYYY-MM-DD-HHMM>

## Source images
| Local file | CDN URL | Pack |
|---|---|---|
| Images/lifestyle-pack/<file>.jpeg | https://<cdn>/.../<file>.jpg | lifestyle |

## CTA variants tested
| Variant | Tier | Source | Char count | Output file |
|---|---|---|---|---|
| 1 | Soft | customer-voice.md verbatim line "..." | 25 | <concept>/9-16/soft-1.png |
| ... | | | | |

## Generation parameters
- Model: <chosen model>
- Aspect ratios: <chosen ratios>
- Total Kie AI calls: <N>
- Three-part prompt template version: v1 (brand-ads-generate skill)
- Brand vault snapshot: <git rev or vault-mtime>

## Test plan
Generic phased test plan (override with what your `ad-playbook.md` specifies if it has its own):

- Upload variants to Meta Ads Manager + TikTok Ads Manager as separate ad sets
- Hold targeting, budget, and bid strategy constant
- Budget: $100–150 per variation, 3–5 day window
- Pause on day 2 if CTR drops >40% below average
- Primary metric: hook rate (target: 30%+ Meta, 25%+ TikTok)
- Secondary: CTR (target 3–5% for DTC)
- Winner advances to script test per your ad-playbook.md
```

---

## Step 6 — Optional follow-up (offer, don't auto-run)

After the BRIEF is written, end the run by offering:

1. **Promote winners to your reference pool.** "If any of these test well, want me to walk you through hosting them and adding rows to `./Images/hosted-urls.md` under a new `ads-pack/` table so you can use them as anchor references in future runs?" — surface this as a manual step (you need their hosting tool); don't try to upload anything yourself.

2. **Schedule a performance check.** "Want me to /schedule an agent in 14 days to check Meta + TikTok performance on this run and recommend a script test?" — uses the `schedule` skill, one-time, not recurring.

Don't run either automatically. Ask once, drop it if the user says no.

---

## Reuse, don't reinvent

This skill is deliberately thin — it composes existing tools rather than re-implementing them:

- **Kie AI MCP** for image generation + async polling — not bundled, expects user to have it configured.
- **Hosted-URL bookkeeping** is read-only via `./Images/hosted-urls.md`. New uploads are the user's responsibility — Shopify CLI, Cloudinary, S3, anything that gives a public URL.
- **Brand context** comes from the workspace-local `./Brand/` vault, populated either by the onboarding flow or by hand from the `brand-vault-template/` reference (next to this SKILL.md when installed as a plugin).

---

## Per-run verification checklist

Before reporting a run as done:

- [ ] Every output PNG exists at the expected path
- [ ] `BRIEF.md` was written and lists every variant
- [ ] No source image was re-uploaded (the skill never uploads — but cross-check that no upload tool was invoked accidentally)
- [ ] Spot-check at least one rendered image: brand accent visible per `visual-identity.md`, not used in a forbidden way; CTA text in the configured typeface and case; scene composition preserved from source
- [ ] No forbidden word leaked into any rendered CTA (re-read the CTAs from the BRIEF table)
- [ ] The "good ad" rule from `ad-playbook.md` was honored — at least one variant clearly passes it

---

## Companion methodology

The methodology this skill operationalizes is documented in [`Ad-Generation-Method.md`](Ad-Generation-Method.md) (in this skill's repo). When the user is debugging poor output, the most common fix is: improve the brand-context prompt (which means: improve the `Brand/` vault files), not change the skill. Read that doc once if you haven't.
