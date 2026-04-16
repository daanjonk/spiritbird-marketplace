# Keyword Research — Phase 1

Detailed instructions for running keyword research via the DataForSEO MCP tools (always available, no auth needed). Defaults: location "United States", language "en".

---

## Step 1: Keyword Discovery

Cast a wide net with three parallel calls:

```
# Long-tail variations of the seed keyword
mcp__dataforseo__dataforseo_labs_google_keyword_suggestions(
    keyword="<seed_keyword>",
    limit=20,
    location_name="United States",
    language_code="en",
    order_by=["keyword_info.search_volume,desc"]
)

# Broader keyword ideas from the product/service category
mcp__dataforseo__dataforseo_labs_google_keyword_ideas(
    keywords=["<seed_keyword>"],
    limit=10,
    location_name="United States",
    language_code="en"
)

# "Related searches" keywords — what people also search for
mcp__dataforseo__dataforseo_labs_google_related_keywords(
    keyword="<seed_keyword>",
    limit=10,
    location_name="United States",
    language_code="en"
)
```

Each returns keyword data including search_volume, competition level, CPC. The `keyword_ideas` tool also returns search_intent info.

**Market override examples:**
- UK market: `location_name="United Kingdom"`
- Netherlands: `location_name="Netherlands"`, `language_code="nl"`
- Germany: `location_name="Germany"`, `language_code="de"`

---

## Step 2: Filter and Validate

Pick the 10-15 most promising keywords from Step 1 and check difficulty + intent:

```
# Keyword difficulty — 0-100 scale, lower = easier to rank
mcp__dataforseo__dataforseo_labs_bulk_keyword_difficulty(
    keywords=["<kw1>", "<kw2>", "<kw3>"],
    location_name="United States",
    language_code="en"
)

# Search intent — informational/commercial/transactional/navigational
mcp__dataforseo__dataforseo_labs_search_intent(
    keywords=["<kw1>", "<kw2>", "<kw3>"],
    language_code="en"
)
```

### Filtering by user's goal

| Goal | Prioritize | Avoid |
|------|-----------|-------|
| Traffic | High volume + difficulty under 40 | Transactional intent (too competitive) |
| Conversion | Commercial or transactional intent | Pure informational (won't convert) |
| Education | Informational intent + medium volume | Low-volume niche terms |
| Product launch | Keywords where the product is a natural answer | Generic terms unrelated to the product |

### Difficulty interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 0-20 | Very easy | Great for new stores with low domain authority |
| 21-40 | Easy-medium | Sweet spot for most Shopify blogs |
| 41-60 | Medium | Need strong content + some backlinks |
| 61-80 | Hard | Only if you have high domain authority |
| 80+ | Very hard | Skip unless you're a major player |

---

## Step 3: Detailed Overview

For the final 5-8 keyword picks, get full data:

```
# Volume, CPC, competition, monthly trends, and intent in one call
mcp__dataforseo__dataforseo_labs_google_keyword_overview(
    keywords=["<primary>", "<secondary1>", "<secondary2>"],
    location_name="United States",
    language_code="en"
)
```

This gives monthly search trends (useful for spotting seasonality) and confirms intent.

---

## Step 4: Present to User

Show a clean summary table:

| Keyword | Volume | Difficulty | Intent | CPC | Role |
|---------|--------|-----------|--------|-----|------|
| organic cotton kids clothes | 1,200 | 34 | informational | $0.85 | **Primary** |
| sustainable children clothing | 880 | 28 | informational | $0.72 | Secondary |
| eczema safe kids clothing | 320 | 15 | commercial | $1.20 | Secondary |
| ... | ... | ... | ... | ... | ... |

### Recommendation format

Explain your picks:
- **Primary keyword** — why (volume + difficulty balance, matches the goal)
- **Secondary keywords** — how they complement the primary (different angles, long-tail variations)
- **Keywords you dropped** — why (too competitive, wrong intent, low volume)

Wait for user confirmation before proceeding to Phase 2.

---

## Cost summary for Phase 1

| Call | Cost |
|------|------|
| suggestions | ~$0.01 |
| ideas | ~$0.01 |
| related | ~$0.01 |
| difficulty | ~$0.01 |
| intent | ~$0.001 |
| overview | ~$0.02 |
| **Total** | **~$0.06** |
