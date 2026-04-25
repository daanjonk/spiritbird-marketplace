# Guardrails — What This Brand Would Never Do

The non-negotiables. When in doubt, this file is the tiebreaker. Each rule includes the *why* so future-you (or an AI agent) can judge edge cases instead of blindly following.

> **The "good ad" rule** (highest-priority — read by the `brand-ads-generate` skill before every render):
>
> *<!-- TODO: one sentence. The one rule that, if broken, means the ad failed regardless of metrics. e.g. "If it looks like an ad, it fails." -->*

---

### 1. `<!-- TODO: rule headline — e.g. "Never compromise [core value] for [easier alternative]" -->`
**Why:** `<!-- TODO: 1-2 sentences. The reason this rule exists. Often a past incident, a strong segment preference, or a positioning constraint. -->`
**How to apply:** `<!-- TODO: 1-2 sentences. When/where this kicks in, and what to do instead. -->`

### 2. `<!-- TODO: rule headline — e.g. "Never price like luxury" -->`
**Why:** `<!-- TODO -->`
**How to apply:** `<!-- TODO -->`

### 3. `<!-- TODO: rule headline -->`
**Why:** `<!-- TODO -->`
**How to apply:** `<!-- TODO -->`

### 4. `<!-- TODO: rule headline -->`
**Why:** `<!-- TODO -->`
**How to apply:** `<!-- TODO -->`

### 5. `<!-- TODO: rule headline -->`
**Why:** `<!-- TODO -->`
**How to apply:** `<!-- TODO -->`

`<!-- Add more rules as the brand develops. 5-10 is the sweet spot — too few and edge cases aren't covered, too many and the file stops being scannable. -->`

---

## Words to AVOID (read by `brand-ads-generate` for CTA validation)

The skill rejects any CTA containing these words. Add or remove based on what would feel off-brand for your customer.

### Corporate jargon
`<!-- TODO: comma-separated. The universal-bad baseline is: introducing, elevate, premium, discover, experience, unleash, transform, scientifically proven, clinically tested, proprietary, revolutionary, breakthrough, cutting-edge, world-class, best-in-class. Keep, edit, or replace. -->`

### CTA clichés
`<!-- TODO: comma-separated. Universal-bad baseline: shop now, buy today, limited time, click the link, limited stock, act fast, don't miss out, tap here, swipe up to save -->`

### Comparative claims (policy + credibility risk)
`<!-- TODO: e.g. "better than [competitor], X times more effective, the only product that, nothing else compares" -->`

### Category-specific reject (fill in based on your vertical)
`<!-- TODO: e.g. for fitness: "lose belly fat, fat-loss, slimming, before-after weight". For supplements: "cures, treats, prevents, heals, detoxifies". For B2B: "synergy, leverage, ecosystem, paradigm" -->`

---

## How to use this file

- Load it any time a decision feels close to a brand line.
- Cross-referenced from `tone-of-voice.md`, `ad-playbook.md`, and `CLAUDE.md`.
- If a new rule needs to be added, write it with a *why* and a *how to apply* — never a one-liner without context.

*Last updated: `<!-- TODO: date -->`*
