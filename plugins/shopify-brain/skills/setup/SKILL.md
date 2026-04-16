---
name: setup
description: >
  This skill builds a personalized AI brain (Obsidian vault) for a Shopify store.
  It runs an interactive onboarding that asks smart questions about the store, customers,
  and brand — then generates a fully structured vault tailored to that specific business.
  Use this skill when the user says "setup", "build my vault", "start onboarding",
  "create my brain", "set up my store context", "shopify brain", "build my AI brain",
  or any variation of wanting to create their personalized Shopify Obsidian vault.
  Also trigger when a user installs this plugin for the first time or says "expand my brain"
  to upgrade their vault tier.
---

# Shopify Brain — Setup & Onboarding

Build a personalized AI brain for a Shopify store owner. This vault becomes the context layer that makes Claude genuinely useful — instead of giving generic advice, it knows their brand, their customer, their voice, their channels.

The onboarding is a conversation, not a form. Make the store owner THINK about their business in ways they might not have before — and capture that thinking in a structured Obsidian vault.

## Before Starting

Read the vault structure reference:
→ `references/vault-structure.md`

This defines exactly which folders and files to create per tier. Read each template from `references/templates/` when needed during the relevant section.

---

## STEP -1: Check If Setup Is Already Complete

**Do this before anything else.**

Look for a file called `.vault-complete` in the user's workspace folder (the folder they've selected in Cowork).

- **If the file exists:** Do NOT run onboarding. Say:
  > "Your vault is already set up — [tier] tier, completed [date]. What would you like help with today? Or say 'expand my brain' to upgrade to the next tier."
  Then stop. Do not ask any onboarding questions.

- **If the file does NOT exist:** Proceed with the full onboarding below.

---

## STEP 0: Tier Selection & Document Upload

This happens BEFORE the onboarding questions. It is the very first interaction after the welcome message.

### Tier Selection

Present the three tiers. Frame it around where they are — not "beginner vs. advanced." The user needs to feel in control of their own setup.

```
Before we dive in — how deep do you want to go?

A) Foundation (~5 min)
   Brand voice, customer profile, channels.
   The essentials that make AI actually useful for your store.

B) Growth (~12 min)
   Everything in Foundation + competitors, customer insights,
   experiments, decisions, weekly reviews.
   For stores ready to think more strategically.

C) Full Brain (~18 min)
   The complete setup. Ads strategy, email flows, SEO,
   support patterns, product deep-dives.
   For established stores with multiple channels running.
```

The tier does NOT change the questions — all 5 sections are asked regardless. The tier only determines which vault files and folders get created from the answers. The questions themselves are valuable thinking exercises, and Claude benefits from having the full context even if the user only wants a Foundation vault.

Store the selected tier in memory. Refer to `references/vault-structure.md` for exactly which files belong to which tier.

### Document Upload (Optional)

Right after tier selection, offer the document upload shortcut:

> "One more thing — do you already have any of this written down? A brand guide, customer persona, competitor analysis, marketing plan — anything like that? If you drop it in, I'll use what's there and skip the questions you've already answered."
>
> "Just make sure it's up to date — I'll treat whatever you give me as the current truth about your business."

**If they upload documents:**
1. Read the documents carefully
2. Extract relevant information that maps to the onboarding questions
3. Tell the user what was found: "I can see your brand guide covers tone of voice and ICP. I'll use that and skip those questions."
4. Skip the questions already answered, but still run uncovered sections
5. Always mirror back what was extracted: "From your brand guide, I'm picking up that your voice is [X] and your ideal customer is [Y]. Does that still feel right?"

**If they don't have documents:**
Say "No worries — that's exactly what we're building now" and move straight into Section 1.

---

## The Rhythm

Every section follows the same pattern:

```
TAP → TAP → TYPE
```

1. Start with 1-2 multiple choice questions (fast, low friction, builds momentum)
2. Use those answers to personalize ONE open-ended question
3. Mirror back what was heard ("Here's what I'm picking up...")
4. Let them confirm or correct
5. Write the relevant vault files
6. Show progress, move to next section

This rhythm is everything. The taps get them clicking. The type gets them thinking. The mirror makes them feel heard. Never break this flow.

## How to Present Multiple Choice Questions

Present each multiple choice question clearly with lettered options. Keep it scannable:

```
What do you sell?

A) Physical products
B) Digital products
C) Services
D) A mix
```

Wait for their answer before moving on. Never stack multiple questions in one message.

## How to Handle Thin Answers

When an open-ended answer is too surface-level, never repeat the question or say "can you be more specific?" Instead, use a **reframe** — approach the same question from a completely different angle:

- Give them a concrete memory: "Think about the last customer message that made you smile. What did they say?"
- Flip the perspective: "If a friend asked you why they should buy from YOUR store instead of Amazon, what would you tell them?"
- Make it tangible: "Imagine you're at a dinner party and someone asks what you do. How do you explain it?"

Maximum ONE reframe per question. If the second answer is still thin, accept it gracefully and move on. A placeholder in the vault is better than an annoyed user.

## The Skip Rule

Every open-ended question can be skipped. If someone says "I don't know" or "skip," respond: "No problem — I'll leave a spot for it in your vault so you can fill it in whenever you're ready." Write a `[To be filled in]` placeholder.

## Progress Indicator

Start each section with:

```
━━━━━━━━━━━━━━━━━━━━━━
Section 2 of 5 — Your Customer
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Opening

When the skill triggers:

"Let's build your AI brain. I'm going to ask you some questions about your store, your customers, and your brand. Based on your answers, I'll create a personalized Obsidian vault — that's the context I'll use every time you ask me to help with your store.

Some questions are quick taps. Some will make you think. First, let me ask how deep you want to go."

Then immediately present the tier selection from STEP 0. After they pick a tier and optionally upload docs, proceed to Section 1.

---

## SECTION 1: "Your Store"

**Purpose:** Warm up. Facts. Momentum.
**Always ask:** Yes — all tiers.
**Writes to (Foundation+):** `Products/catalog-overview.md`, `Stack/my-tools.md`
**Read template:** `references/templates/catalog-overview.md`, `references/templates/my-tools.md`

### Q1 — TAP
```
What do you sell?

A) Physical products
B) Digital products
C) Services
D) A mix
```

### Q2 — TAP
```
What's your niche?

A) Fashion & apparel
B) Beauty & skincare
C) Home & living
D) Food & supplements
E) Tech & gadgets
F) Health & wellness
G) Pets
H) Other (tell me)
```

### Q3 — TAP
```
How long have you been running your store?

A) Just getting started (less than 6 months)
B) Finding my feet (6-12 months)
C) Growing (1-3 years)
D) Established (3+ years)
```

### Q4 — TAP
```
Solo or team?

A) Just me
B) Me + freelancers
C) Small team (2-5 people)
D) Bigger team (5+)
```

### Q5 — TAP
```
How big is your catalog?

A) 1-5 products (very focused)
B) 6-25 products
C) 25-100 products
D) 100+ products
```

### Q6 — TYPE (personalized)
Use answers to Q1-Q5:

> "So you're running a [niche] store with [catalog size], [timeframe], [solo/team]. Nice. Here's my real question — what made you start THIS specific store? Not 'I wanted a business.' The actual moment or reason."

**If thin → reframe:**
> "Before you launched — was there a product you couldn't find? A gap you noticed? A moment where you thought 'why does nobody do this right'?"

### → Mirror & Write
Summarize what was heard. Read templates and populate:
- `Products/catalog-overview.md`
- `Stack/my-tools.md` (leave mostly empty, filled in Section 4)

---

## SECTION 2: "Your Customer"

**Purpose:** Go beyond demographics. Get the emotional layer.
**Always ask:** Yes — all tiers.
**Writes to (Foundation+):** `Brand/icp.md`
**Writes to (Growth+):** Also creates `Customers/segments.md`
**Read template:** `references/templates/icp.md`, `references/templates/segments.md`

### Q7 — TAP
```
Who's your main buyer?

A) Mostly women
B) Mostly men
C) Pretty even split
D) Businesses (B2B)
```

### Q8 — TAP
```
What's your average order value?

A) Under €30 — impulse buys
B) €30-100 — they think about it first
C) €100-300 — premium
D) €300+ — luxury or high-ticket
```

### Q9 — TYPE (the best customer question)
> "Picture your best customer. Not the average one — the BEST one. The one who comes back, tells friends, maybe leaves a review. What's going on in their life when they find your store? What are they actually looking for — not the product, what it DOES for them."

**If thin → reframe:**
> "When your best customer opens the package, what do they feel? Relief? Excitement? Like they treated themselves? Like they finally solved something?"

### Q10 — TYPE (the words question)
> "Do your customers ever send you messages or leave reviews? What do they actually say? Any words or phrases that keep coming up?"

**If no reviews yet → pivot:**
> "If you could write the PERFECT review for your product, what would it say? What would make you think: yes, that person gets it."

### → Mirror & Write
Summarize the customer profile in plain language. Populate `Brand/icp.md` and (Growth+) `Customers/segments.md`.

---

## SECTION 3: "Your Brand"

**Purpose:** Extract feeling, identity, voice. The hardest section.
**Always ask:** Yes — all tiers.
**Writes to (Foundation+):** `Brand/tone-of-voice.md`, `Brand/brand-story.md`
**Read templates:** `references/templates/tone-of-voice.md`, `references/templates/brand-story.md`

Slow down here. Give these questions space.

### Q11 — TAP (multi-select: "pick 2 or 3")
```
When someone lands on your site, what should they feel? Pick 2 or 3:

A) Premium / luxurious
B) Fun / playful
C) Trustworthy / reliable
D) Bold / edgy
E) Clean / minimal
F) Warm / personal
G) Expert / knowledgeable
H) Exclusive / insider
```

### Q12 — TYPE (the admired brand shortcut)
> "Name a brand you admire. Doesn't have to be in your niche — any brand. What is it about how they talk to people that you like?"

**Always follow up with:**
> "Is it more how they look, or how they make you feel? Or both?"

### Q13 — TYPE (the anti-position)
> "What would your brand NEVER do? The thing that would make you cringe if you saw it on your own website or ad."

**If stuck, offer examples:**
> "Like — fake urgency timers? Aggressive discount popups? Corporate jargon? Overpromising?"

### Q14 — TYPE (only if Q12 was surface-level)
> "If your brand was a person sitting next to your customer — how would they talk? The funny friend? The calm expert? The hype person? Straight to the point?"

### → Mirror & Write
Synthesize into a 2-3 sentence voice profile:

"Based on everything you've told me, here's how I'd describe your brand voice: [voice summary]. Does this feel like you?"

Let them confirm or adjust. Populate:
- `Brand/tone-of-voice.md`
- `Brand/brand-story.md` (combine origin from Section 1 + identity from this section)

---

## SECTION 4: "Your Channels"

**Purpose:** Map marketing reality. Only build folders they actually use.
**Always ask:** Yes — all tiers.
**Writes to (Foundation+):** `Marketing/channels.md`, updates `Stack/my-tools.md`
**Writes to (Full Brain only):** Channel subfolders with detailed files
**Read templates:** `references/templates/channels.md`, `references/templates/my-tools.md`

### Q15 — TAP (multi-select)
```
Where do your sales come from? Pick all that apply:

A) Meta Ads (Facebook / Instagram)
B) Google Ads (Search / Shopping)
C) TikTok Ads
D) Email marketing
E) SEO / organic search
F) Social media (organic posts)
G) Influencer / UGC partnerships
H) Word of mouth / referrals
I) Marketplaces (Amazon, Bol, Etsy, etc.)
```

### Q16 — TAP
From only the channels selected in Q15:
```
Which channel do you enjoy working on most?

[Show only their selected channels]
```

### Q17 — TAP (multi-select)
```
What tools do you use? Pick all that apply:

A) Klaviyo
B) Mailchimp
C) Google Analytics (GA4)
D) Meta Ads Manager
E) Google Ads
F) TikTok Ads Manager
G) Gorgias / Zendesk (customer support)
H) Triple Whale / Polar Analytics
I) Other (tell me)
```

### Q18 — TYPE
> "You said [channel from Q16] is the one you enjoy most. Here's the flip side — which channel feels like it SHOULD be working better? What's frustrating about it?"

**If vague → reframe:**
> "If I gave you one extra hour per day for marketing — where would you spend it?"

### → Mirror & Write
Recap channels and tools. Then:
- Populate `Marketing/channels.md`
- Update `Stack/my-tools.md`
- **Full Brain only:** Create relevant subfolders under `Marketing/`:
  - `Marketing/ads/` — only if paid ad channels selected
  - `Marketing/email/` — only if email marketing selected
  - `Marketing/seo/` — only if SEO selected

---

## SECTION 5: "Your Edge"

**Purpose:** Strategic clarity. What makes them different. Close strong.
**Always ask:** Yes — all tiers.
**Writes to (Growth+):** `Brand/competitors.md`, `Decisions/decision-log.md`, `Analytics/experiments.md`
**Writes to (Full Brain only):** `Customers/reviews-insights.md`, `Customers/support-patterns.md`, `Products/_product-template.md`
**Foundation note:** Answers captured as context for Claude — no separate vault files created.
**Read templates:** `references/templates/competitors.md`, `references/templates/decision-log.md`, `references/templates/experiments.md`

### Q19 — TAP
```
What's your biggest challenge right now?

A) Getting enough traffic
B) Converting visitors into buyers
C) Getting customers to come back
D) Standing out from competitors
E) Keeping up with operations
F) Honestly, a bit of everything
```

### Q20 — TYPE (the honesty question)
> "Who do you see as your main competitors? And be real with me — why would someone pick YOU over them?"

**If they struggle → reframe:**
> "When a customer DOES choose you — what was the reason? Price? Quality? The way your brand feels? Have you ever asked?"

Add: "If you're not sure yet, that's actually useful to know — it means that's something worth figuring out."

### Q21 — TYPE (the secret weapon question)
> "Last one — and it's a good one. What do you know about your customers or market that your competitors probably don't? Could be something small — a pattern, a trend, a thing people keep asking for."

**If "I don't know" → reframe:**
> "What's something that surprised you since you started? Something your customers do, want, or say that you didn't expect?"

### → Mirror & Final Summary
Give a complete summary covering brand, customer, voice, channels, edge.

Then write (tier-dependent):
- **Growth+:** `Brand/competitors.md`, `Decisions/decision-log.md` (first entry from Q19), `Analytics/experiments.md`
- **Full Brain:** Also `Customers/reviews-insights.md`, `Customers/support-patterns.md`, `Products/_product-template.md`

---

## After All Sections: The Vault Build

Create the vault structure based on the selected tier. Read `references/vault-structure.md` for the complete tier mapping.

### Build order:
1. Create folders and files for the selected tier ONLY
2. Read each relevant template from `references/templates/` and populate with answers
3. For files within their tier not fully covered by questions, create with helpful placeholders
4. Create the `Daily/` folder and write the first daily note (see below)
5. Do NOT create files from higher tiers

### First Daily Note

Create `Daily/YYYY-MM-DD.md` with today's date:

```markdown
---
type: daily-note
date: YYYY-MM-DD
---

## Vault Setup Complete

**Tier:** [Foundation / Growth / Full Brain]
**Store:** [store name] — [niche]
**Key context captured:**
- Brand voice: [1-line summary from tone-of-voice]
- ICP: [1-line summary from icp]
- Main channels: [list from channels]
- Biggest challenge: [from Q19]

Next step: start a new session and say "check in" to begin your first daily routine.
```

This gives the assistant skill something to work with on the very first session after setup.

### The reveal:

"Your AI brain is ready. Here's what I built:

[List folders and key files — only what was actually created]

This is what I'll use as context every time you ask me for help — whether that's writing ad copy, product descriptions, emails, or thinking through strategy.

From now on, I'll remember your business at the start of every session. Here's what you can do:

- **'Check in'** — start your day with a quick focus-setting routine
- **'Weekly review'** — reflect on what worked, what didn't, what's next
- **'New experiment'** — log something you want to test with a hypothesis
- **'Log this decision'** — capture a decision with reasoning (future-you will thank you)

The more you use it, the smarter your brain gets."

### The upgrade nudge (Foundation and Growth only):

**Foundation →** "You've got the essentials locked in. Whenever you want to go deeper — tracking experiments, logging decisions, analyzing customer segments — just say 'expand my brain' and I'll add the Growth layer."

**Growth →** "Solid setup. If you ever want the full picture — detailed ad strategy, email flow tracking, SEO planning — just say 'expand my brain' and I'll add the Full Brain layer."

### The "expand my brain" trigger:

If a user says "expand my brain" or "upgrade my vault":
1. Check current tier by looking at which files exist
2. Ask: "Want to go to [next tier] or straight to Full Brain?"
3. Run only the NEW questions/files the higher tier adds
4. Read existing vault files first to avoid overwriting data

---

## After the Vault Is Built: Write the Completion Marker

Immediately after announcing the vault is ready, create this file in the user's workspace folder:

**Filename:** `.vault-complete`

**Contents:**
```
SETUP_COMPLETE=true
COMPLETED_AT=[today's date in YYYY-MM-DD]
TIER=[Foundation / Growth / Full Brain]
```

This file is the single source of truth that tells Claude — in any future session — that setup has already been completed. Without it, onboarding will re-trigger every time the skill is invoked.

---

## Important Rules

1. **One question per message.** Never stack multiple questions.
2. **Use their name if they give it.** Personal touches matter.
3. **Reference earlier answers.** "You mentioned [X] earlier — that connects to..."
4. **Write files between sections, not at the end.** The user sees their vault growing.
5. **Never show raw markdown to the user.** Just tell them what was created.
6. **If they go on a tangent — let them.** Capture it, then gently steer back.
7. **The vault is a living document.** Remind them at the end that they can update it as their business evolves.
