# Vault Structure Reference

The vault structure depends on which tier the user selected. Each tier builds on the previous one. Only create files for the selected tier — nothing more.

## Tier Overview

| | Foundation | Growth | Full Brain |
|---|---|---|---|
| Time | ~5 min | ~12 min | ~18 min |
| Files created | 8 | 15 | 21+ |
| Folders | 5 | 8 | 9+ |

## Foundation (Tier A)

```
[store-name]-brain/
├── Brand/
│   ├── tone-of-voice.md
│   ├── icp.md
│   └── brand-story.md
├── Products/
│   └── catalog-overview.md
├── Marketing/
│   └── channels.md
├── Stack/
│   └── my-tools.md
├── Daily/
│   └── [YYYY-MM-DD].md          ← first daily note (setup summary)
└── README.md
```

## Growth (Tier B)

Everything in Foundation PLUS:

```
Brand/
  └── competitors.md             ← NEW
Customers/
  └── segments.md                ← NEW
Analytics/
  ├── weekly-review.md           ← NEW (template for recurring use)
  └── experiments.md             ← NEW
Decisions/
  └── decision-log.md            ← NEW
```

## Full Brain (Tier C)

Everything in Growth PLUS:

```
Products/
  └── _product-template.md       ← NEW
Marketing/
  ├── ads/ad-strategy.md         ← NEW (only if paid ads)
  ├── email/flows-overview.md    ← NEW (only if email marketing)
  └── seo/keyword-strategy.md    ← NEW (only if SEO)
Customers/
  ├── reviews-insights.md        ← NEW
  └── support-patterns.md        ← NEW
```

## System Files (All Tiers)

```
.vault-complete                   ← created after setup finishes
```

## Conditional Channel Folders (Full Brain only)

| Channel selected | Creates |
|---|---|
| Meta/Google/TikTok Ads | `Marketing/ads/ad-strategy.md` |
| Email marketing | `Marketing/email/flows-overview.md` |
| SEO / organic search | `Marketing/seo/keyword-strategy.md` |

## The Daily/ Folder

Every tier gets a `Daily/` folder. The first daily note is created during setup with a summary of what was built. After setup, the assistant skill manages daily notes.

Daily notes follow this naming convention: `Daily/YYYY-MM-DD.md`

The assistant skill's `references/template-daily-note.md` defines the daily note structure.

## The "Expand My Brain" Upgrade Path

**Foundation → Growth:** Add competitors, segments, weekly-review, experiments, decision-log. Do NOT overwrite existing files.

**Growth → Full Brain:** Add product-template, reviews-insights, support-patterns, and relevant channel subfolders. Do NOT overwrite existing files.

Always read existing vault files before expanding.
