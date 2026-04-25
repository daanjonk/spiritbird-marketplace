# Ad Playbook

> Load before writing any paid creative, Reels script, TikTok script, ambassador brief, or static ad. Pair with `customer-voice.md`, `icp.md`, `guardrails.md`, and `visual-identity.md`. **The `brand-ads-generate` skill reads the CTA tier examples and the words-to-avoid section directly.**

---

## The "good ad" rule

`<!-- TODO: one sentence. The single rule every ad lives or dies by. Mirror this into guardrails.md. -->`

*Example (Fox):* if it looks like an ad, it fails.
*Example (luxury beauty):* if it doesn't feel like a moment of self-care, it fails.
*Example (B2B SaaS):* if it doesn't make a busy buyer stop and think "wait, that's me", it fails.

---

## Why this format works (your evidence base)

`<!-- TODO: 2-4 bullets summarizing the data behind your creative thesis. Examples: "UGC outperforms polished 4× on CTR for our segment", "static carousels beat single-image by 2× for B2B SaaS top-of-funnel" -->`

- `<!-- TODO -->`
- `<!-- TODO -->`

Hook-rate targets:
- Meta Reels: `<!-- TODO: e.g. "30%+ healthy, 40%+ elite" -->`
- TikTok: `<!-- TODO -->`

---

## Hook frameworks (the first 3 seconds)

Test all in parallel — never pick one upfront. The four below are universally applicable; edit or replace with what works for your category.

### 1. Pattern Interrupt
A visual or audio shock that breaks the scroll rhythm.
- `<!-- TODO: 1-2 example opens specific to your brand -->`
- Why: stops the thumb because the brain didn't predict it

### 2. Social-Proof / Testimonial
Open with a relatable creator stating their experience as a peer.
- `<!-- TODO: example open. Pull verbatim from customer-voice.md if possible. -->`

### 3. Before / After (the *honest* version)
Open with the relatable struggle state, transition to the resolved state.
- `<!-- TODO: example. Forbidden framings for your category? -->`
- **Forbidden framing:** `<!-- TODO: any before/after framing that crosses your guardrails. e.g. for fitness: weight-loss / appearance transformation -->`

### 4. Curiosity Gap
Open with an incomplete statement that the viewer needs to finish.
- `<!-- TODO: example -->`

---

## Script structure (15–30s)

Generic 4-beat model. Override per-vertical if needed.

| Beat | Time | What happens |
|---|---|---|
| 1 — Hook | 0–3s | Pattern-interrupt / testimonial / before-after / curiosity-gap. **Brand accent should appear in frame within 2s.** |
| 2 — Problem | 3–8s | Creator names a pain point the viewer recognizes |
| 3 — Product | 8–15s | Natural product introduction. First-person benefit, not feature dump |
| 4 — CTA | 15–30s | Soft CTA — see tier table below |

---

## Words to USE

Pull from these. The closer to verbatim from `customer-voice.md`, the better.

`<!-- TODO: 5-10 buckets of language your customers actually use. Examples below — replace with yours. -->`

### Trust language
`<!-- TODO: e.g. "honestly, ngl, lowkey, real talk, actually, tbh, look, for real" — for casual / Gen Z. Or "in our experience, what we've found, the data shows" — for B2B. -->`

### First-person framing
`<!-- TODO: e.g. "I tried, I've been using, I switched from, this changed my, if you're like me" -->`

### Category vocab (use naturally — see `icp.md`)
`<!-- TODO: insider words your ICP uses among themselves -->`

### Benefit verbs (action, not adjective)
`<!-- TODO: e.g. "helped me, kept me, gave me, let me, got me through, held up" -->`

### Credible micro-data
`<!-- TODO: specific small numbers beat vague claims. e.g. "3 years still going, 5x a week no pilling, wore them for a 12-mile session" -->`

---

## Words to AVOID (★ read by `brand-ads-generate` for CTA validation)

These break the voice or trigger ad policy. Mirror the lists in `guardrails.md` — the skill checks both files.

### Corporate jargon (instant ad-detection)
`<!-- TODO: list. Universal-bad baseline: introducing, elevate, premium, discover, experience, unleash, transform, scientifically proven, clinically tested, proprietary, revolutionary, breakthrough, cutting-edge, world-class, best-in-class -->`

### Comparative claims (policy + credibility risk)
`<!-- TODO: e.g. "better than [competitor], X times more effective, the only product that, nothing else compares" -->`

### Body-shaming / appearance / medical (policy violation)
`<!-- TODO: only if your category touches these — fitness, beauty, supplements, health -->`

### CTA clichés that scream "ad"
`<!-- TODO: universal-bad baseline: shop now, buy today, limited time, click the link, limited stock, act fast, don't miss out, tap here, swipe up to save -->`

### Sentence patterns
- Anything over `<!-- TODO: char count, e.g. "12 words" -->` spoken in voiceover (creator speech is short)
- Multi-clause "however / moreover / furthermore" structures
- Exclamation overload (1 max per script)

---

## CTAs — Soft / Moderate / Direct (★ read by `brand-ads-generate` for auto-CTA generation)

The skill samples one or more rows from each tier when auto-generating ad variants. The closer your tier examples are to verbatim customer language, the better the auto-CTAs will be.

| Tier | Example | When to use |
|---|---|---|
| Soft | `<!-- TODO: e.g. "link's in my bio", "I'll drop the link", "this is what I'm wearing" -->` | Default — top of funnel, brand-aware audiences, broad cold |
| Soft | `<!-- TODO: 1-2 more soft examples — pull verbatim from customer-voice.md if possible -->` | |
| Soft | `<!-- TODO -->` | |
| Moderate | `<!-- TODO: e.g. "if you want to try them, link below", "100% recommend grabbing a pair" -->` | Mid-funnel, retargeting warm audiences |
| Moderate | `<!-- TODO -->` | |
| Direct | `<!-- TODO: e.g. "use code [CREATOR] for 15% off" -->` | Bottom-funnel only, abandoned cart, bestseller drops |

**Default for this brand:** `<!-- TODO: pick one — Soft / Moderate / Direct -->`. Direct CTAs with codes break the UGC illusion fastest. Use codes only with creators where the personal-discount-code is part of their normal content.

CTA placement: end of script. **Never** open with a CTA. Lead with the hook.

---

## Format-specific rules

### Meta Reels (IG + FB)
- 9:16 vertical, full screen
- 30–45s sweet spot for algorithmic distribution
- Sound-on assumption
- Native captions recommended (1–2 lines max)
- Cuts every 1–2s
- First 3 seconds critical; <20% hook rate = de-prioritized

### TikTok native + Spark Ads
- 9:16 vertical
- 15–34s sweet spot (algorithm rewards completion)
- Trending audio when authentically usable; original audio otherwise
- First 1–2 seconds critical (faster scroll than Meta)
- Comments + shares weighted heavily — script for engagement

### Static image ads (the format `brand-ads-generate` produces)
- 9:16, 4:5, or 1:1
- Native-feed appearance: looks like a real post, not an ad
- Text-on-image: native font (TikTok caption / IG sticker style), not corporate Helvetica perfection
- See `visual-identity.md` for typeface + accent rules

### Carousel ads
- Slide 1 = the hook
- Slides 2–5 = beat-by-beat narrative arc
- Last slide = soft CTA

---

## Visual & framing rules (UGC-native)

`<!-- TODO: 4-6 bullets specific to your brand. Below is the universal UGC baseline — keep, edit, or replace. -->`

- **Camera:** phone footage, handheld, slight shake, natural framing. No gimbals, no drones, no studio lighting.
- **Lighting:** Natural — `<!-- TODO: where your customer actually is. Gym lights, kitchen window, office desk, bathroom mirror. -->`. No ring lights for talking heads (too obvious).
- **Eye contact** for testimonial framings. Mid-action for movement framings.
- **Background:** Real environment — `<!-- TODO -->`. Never sterile white studio.
- **Color:** Natural color temperature. **No heavy filters** (that's for brand-tier content, not UGC-tier ads).

### The brand visual signature in every ad

**Every ad must show the brand accent at least once.** See `visual-identity.md` for the full rules — the `brand-ads-generate` skill validates this on every render.

---

## Policy guardrails (Meta + TikTok)

Compliance checklist — every creative passes through this before going live:

- [ ] No comparative claims to named competitors
- [ ] No body-shaming or appearance-based transformation framing (if applicable to your category)
- [ ] No weight-loss / fat-loss language (if applicable)
- [ ] No medical / health claims without disclaimer (if applicable)
- [ ] No unsubstantiated efficacy claims ("guaranteed", "proven")
- [ ] No fake user testimonials or AI-voiced creators presented as real people
- [ ] If using a creator: real person, real handle, paid disclosure visible if required
- [ ] First-person language preferred (reduces brand-liability)

---

## Test cadence

Phased testing. Rapid iteration beats perfection.

### Budget per variation
- `<!-- TODO: e.g. "$100-150 minimum per creative" -->`
- 3–5 day window for statistical significance on hook + CTR
- Pause on day 2 if CTR drops >40% below average

### Phase 1 — Hook test (Week 1)
- Hold script, visual, CTA constant; test all 4 hook frameworks
- Metric: hook rate

### Phase 2 — Script test (Week 2)
- Use winning hook; test 3–4 script variations
- Metric: CTR

### Phase 3 — Creator test (Week 3)
- Use winning hook + script; test with 3–4 different creators
- Metric: conversion rate + ROAS

### Phase 4 — CTA test (ongoing)
- Use winning combo; test soft / moderate / direct CTA tiers
- Metric: CTR → landing page → conversion

### Refresh cadence
- New creator briefs every `<!-- TODO: 2-4 weeks typical -->`
- Refresh winning hooks with new creators to extend lifespan

---

## Creator brief template (copy-paste block)

```
Brand: <!-- TODO: brand name -->
Campaign: [name + month]
Format: [9:16 vertical / 15s TikTok / 30s Reel]
Goal: [specific PDP / always-on / drop launch / community challenge]

Hook framework: [pattern interrupt / testimonial / before-after / curiosity gap]
Script structure: 4-beat (Hook 0-3s → Problem 3-8s → Product 8-15s → CTA 15-30s)

Required:
- Brand accent visible at least once (see visual-identity.md for what counts)
- Soft CTA: "<!-- TODO: your default soft CTA -->" or your natural equivalent
- First-person voice — talk like yourself, not like an ad

Free to riff on:
- Hook line (idea provided, but your version always beats ours)
- Music, edit, location, framing
- Whether to disclose as #ad or partner — your call

Off-limits (full list in our internal ad-playbook):
- Words: <!-- TODO: top 5 forbidden words from your guardrails -->
- Framings: <!-- TODO -->
- Visuals: studio lighting, ring lights, motion graphics, lens flares

Deliverables:
- [count + format]
- Raw files for paid usage rights ([term])

Timeline: [draft → revisions → final]
Compensation: [retainer / product / commission]
```

---

*Last updated: `<!-- TODO: date -->`*
