# SERP & Competitive Analysis — Phase 2 / 2b

Detailed instructions for analyzing what's currently ranking and identifying content gaps. Run after keyword selection is confirmed.

---

## Phase 2: SERP Analysis

### Step 1: Live SERP Results

```
# Get top 10 Google results + featured snippets + People Also Ask
mcp__dataforseo__serp_organic_live_advanced(
    keyword="<primary_keyword>",
    language_code="en",
    location_name="United States",
    depth=10,
    device="desktop"
)
```

Returns:
- **Organic results**: position, title, URL, domain, description
- **Featured snippets**: what format (paragraph, list, table), which URL owns it
- **People Also Ask**: the questions Google shows — these become H2 headings in your outline
- **Related searches**: additional keyword angles

**What to note:**
- What content format dominates? (listicles, how-to guides, comparisons, roundups)
- Is there a featured snippet? Can we take it with a better answer?
- What questions appear in People Also Ask? (use these as H2 headings)
- Are there gaps — topics the top results don't cover well?

### Step 2: Parse Top-Ranking Content

Pick the top 2-3 organic results and analyze their structure:

```
# Parse headings, word count, link counts
mcp__dataforseo__on_page_content_parsing(
    url="<url_of_rank_1>",
    enable_javascript=true
)

mcp__dataforseo__on_page_content_parsing(
    url="<url_of_rank_2>",
    enable_javascript=true
)
```

Returns: title, description, h1/h2/h3 headings, word count, internal/external link counts, image count.

**What to extract:**
- **Word count**: our article should match or exceed the average of top 3
- **Heading structure**: what H2/H3 topics do they cover? What's missing?
- **Link density**: how many internal links? (we should match or beat this)
- **Image count**: indicates expected visual richness

### Step 3: SERP Competitors

```
# Which domains compete for our keywords
mcp__dataforseo__dataforseo_labs_google_serp_competitors(
    keywords=["<primary_kw>", "<secondary_kw1>"],
    location_name="United States",
    language_code="en",
    limit=10
)
```

Returns: domain, average position, rating, estimated traffic, visibility.

**What to note:**
- Are we competing against high-authority domains (Amazon, Wikipedia)?
- Are there smaller/niche domains ranking? (better opportunity)
- What's the average position spread? (tight = competitive, spread = opportunity)

---

## Phase 2b: AI Optimization (Optional)

Only run if the user opted in during Phase 0. Adds ~$0.10 to total cost.

### Step 1: LLM Mentions

```
# What pages do ChatGPT/Google AI recommend for this topic
mcp__dataforseo__ai_opt_llm_ment_search(
    target=[{"keyword": "<primary_keyword>"}],
    location_name="United States",
    language_code="en",
    limit=10
)
```

Returns: URLs that AI systems mention, their domains, mention count, AI search volume, and platforms.

**How to use this:**
- Study the recommended pages — what depth and format do they use?
- Cover the same topics so AI is likely to include your article too
- Structure content for easy AI extraction: clear headings, direct answers, factual statements
- If a competitor page gets mentioned a lot, analyze what makes it AI-friendly

### Step 2: AI Search Volume

```
# How often does this keyword appear in AI conversations
mcp__dataforseo__ai_optimization_keyword_data_search_volume(
    keywords=["<primary_kw>", "<secondary_kw1>"],
    language_code="en",
    location_name="United States"
)
```

Returns `ai_search_volume` (current monthly rate) and `ai_monthly_searches` (12-month history). High AI search volume = this topic gets asked about in ChatGPT/Perplexity often. Worth optimizing for structured, extractable answers.

---

## Summary Output for Phase 2

After completing the analysis, compile a brief for Phase 3 (outline):

1. **Content format**: what works (guide, listicle, comparison, etc.)
2. **Target word count**: based on top-ranking articles
3. **Heading topics to cover**: from parsing top results
4. **Featured snippet opportunity**: type (paragraph/list) + target question
5. **People Also Ask questions**: direct H2 candidates
6. **Content gaps**: what competitors miss
7. **AI optimization notes** (if opted in): what AI recommends, structural patterns

This brief feeds directly into the outline in Phase 3.

---

## Cost summary for Phase 2

| Call | Cost | Required? |
|------|------|-----------|
| serp (live) | ~$0.001 | Yes |
| content-parse (×2-3) | ~$0.0003 | Yes |
| serp-competitors | ~$0.01 | Yes |
| ai-llm-mentions | ~$0.10 | Only if AI opted in |
| ai-search-volume | ~varies | Only if AI opted in |
| **Total (SEO only)** | **~$0.01** | |
| **Total (SEO + AI)** | **~$0.11** | |
