# Visual Identity

> **Required for any visual brief.** The `brand-ads-generate` skill reads this file's Color System, Typography, and Photography sections directly into the Kie AI prompt. Sections marked **★** are load-bearing — fill them in completely or the generated ads will fall back to neutral defaults.

---

## The one rule

`<!-- TODO: one sentence — the single rule that governs your whole visual system. e.g. "Black and white are the structure. Light blue is the signal. Never confuse them." -->`

---

## Color System ★

### Primary anchors

| Role | Color | Hex | Use |
|---|---|---|---|
| Structural primary | `<!-- TODO -->` | `<!-- TODO: e.g. #000000 -->` | Body text, hero backgrounds, packaging |
| Structural secondary | `<!-- TODO -->` | `<!-- TODO: e.g. #FFFFFF -->` | Reverse text, breathing space |
| Mid-tones | `<!-- TODO -->` | `<!-- TODO: e.g. #1A1A1A / #F5F5F5 -->` | Section backgrounds, soft contrast |

### Signature accent (your edge) ★

| Role | Color name | Hex | Notes |
|---|---|---|---|
| **Accent / signature** | `<!-- TODO: e.g. "powder blue" -->` | `<!-- TODO: hex — required by the ads skill -->` | The differentiator. Used sparingly. |

### Where the accent lives (allowed)

`<!-- TODO: list 4-6 specific places. The ads skill uses this list to validate generated images. -->`

- Logo accent (`<!-- TODO: which element -->`)
- Primary CTA buttons
- Hover and focus states
- Packaging interior (the unboxing reveal moment)
- Product trim
- On-screen text overlay accents

### Where the accent does NOT live (forbidden) ★

`<!-- TODO: list 4-6 forbidden uses. The ads skill bakes these into PART 3 of the prompt as explicit "never do" rules. -->`

- As a body-fabric / surface color (no full accent-color tees, hoodies, packaging exteriors)
- As a color grade on photography or video
- As a hero background on landing pages, ads, or PDPs
- As a gradient
- In illustrations or decorative graphics
- Mixed with any other accent color

### Why the rules

`<!-- TODO: 1-2 sentences explaining why the accent is rare. The "rarity = signal" argument. -->`

---

## Typography ★

### Display
- **`<!-- TODO: typeface name — used as {on_image_typeface} in the ads skill -->`** (e.g. Bebas Neue, Inter Display, Playfair Display)
- Casing: `<!-- TODO: all-caps / title case / sentence case -->`
- Tracking: `<!-- TODO: e.g. -25 to -50 for tight condensed, 0 for neutral -->`
- Used for: hero headlines, drop names, on-product graphic text, video supers, **on-image ad CTAs**

### Body
- **`<!-- TODO: typeface name -->`** (e.g. Inter, Helvetica Neue, Söhne)
- Casing: sentence case
- Used for: body copy, PDP descriptions, email body

### Forbidden
`<!-- TODO: list 2-3 typeface categories you never use. Common: serifs, decorative scripts, brushed -->`

- `<!-- TODO -->`

---

## Logo System

### Components
- **Wordmark:** `<!-- TODO: describe — e.g. "BRAND set in Bebas Neue, all-caps, with an accent underline on one letter" -->`
- **Icon:** `<!-- TODO -->`
- **Lockups:** `<!-- TODO: which lockups exist — wordmark alone, icon alone, horizontal, stacked -->`

### Logo placement in ads (used by the ads skill as `{brand_mark}`)

`<!-- TODO: 1 sentence — where does your logo appear in a typical ad shot? Apparel chest, packaging, product label, etc. -->`

### Logo never
- Rotated, skewed, distorted, stretched
- Recolored beyond approved combos
- Outlined (always solid fill)
- `<!-- TODO: any brand-specific never-rules -->`

---

## Photography ★

### Mood (used by the ads skill as `{photography_mood}`)

`<!-- TODO: 1-2 sentences — the cinematic feel. e.g. "Cool, desaturated, lifted blacks, crushed shadows. Sweat-and-effort over polish." -->`

### Lighting
- `<!-- TODO: directional / soft / natural / studio — pick a direction and commit -->`

### Subject framing
- Subject fills `<!-- TODO: e.g. "60-80%" -->` of frame
- `<!-- TODO: mid-action vs. static / eye-contact preferences -->`

### Backgrounds
- `<!-- TODO -->`

### The accent in photography
- **Allowed:** `<!-- TODO: e.g. "small color pop from apparel detail caught in frame" -->`
- **Never:** `<!-- TODO: e.g. "entire image color-graded in the accent" -->`

---

## Video / Motion

### Edit
- `<!-- TODO: cut pacing — e.g. "fast cuts, every 0.5-1.5s" -->`
- `<!-- TODO: transition rules -->`

### Color grade
- Matches photography section above

### Sound
- `<!-- TODO: genre direction — e.g. "trap, electronic, cinematic instrumentals" -->`

### Text overlay
- Same typeface as Display section above
- Placement: `<!-- TODO -->`

---

## Visual do's and don'ts (consolidated)

### Do
- `<!-- TODO: 4-6 affirmative rules -->`

### Don't
- `<!-- TODO: 4-6 forbidden patterns. Mirror the "forbidden accent uses" above plus typography / photography rules. -->`

---

## Why the accent (the brand argument)

`<!-- TODO: 2-3 sentences on why this specific accent is right for your brand. The competitive whitespace argument: what does your accent own that no competitor does? -->`

---

*Last updated: `<!-- TODO: date -->`*
