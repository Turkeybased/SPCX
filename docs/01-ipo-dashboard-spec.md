# Spec: IPO Context Dashboard — SpaceX / Anthropic / OpenAI vs. IPO History

**Version:** 1.0 · **Date:** 2026-06-10 · **Owner:** Solo · **Status:** Draft for build handoff

---

## 1. Problem Statement

Three of the largest IPOs ever attempted are landing within months of each other: SpaceX prices June 11, 2026 (targeting ~$75B raise at ~$1.75T — the largest IPO in history), and Anthropic (filed June 1) and OpenAI (filed June 8) have confidential S-1s pending. Coverage of each deal is siloed and narrative-driven; there is no single view that puts these deals in quantitative context against IPO history — raise size, valuation multiples, profitability at listing, and how comparable hype-cycle cohorts actually performed.

The user (a single individual making personal investing decisions) needs that context to decide whether and how to participate, and to keep tracking the deals as they evolve (SPCX starts trading June 12; the two AI S-1s will flip public later in 2026).

**Cost of not solving:** decisions anchored on headlines ("largest IPO ever") instead of base rates (e.g., only ~5% of the 2020–21 IPO class traded above offer price by March 2023; day-1 pops are uncorrelated with 1-year outcomes).

**Honest scoping note:** most of the *context* value is deliverable as a static dataset + report. The dashboard earns its keep only through the *live layer* — SPCX price tracking post-June 12 and EDGAR monitoring for the Anthropic/OpenAI S-1s. v1 is therefore: static, pre-verified comparables dataset + thin live layer. Resist building a general-purpose IPO analytics platform.

## 2. Goals

1. **Context at a glance:** user can answer "how does this deal compare historically?" for any of the three deals in under 30 seconds (raise, valuation, P/S multiple, profitability vs. comp sets).
2. **Base-rate visibility:** every view that shows a 2026 deal also shows the distribution of historical outcomes (day-1 pop vs 1-yr return scatter; cohort survival rates), not just single comps.
3. **Live tracking:** SPCX price vs. $135 offer updates at least daily; Anthropic/OpenAI filing status checked daily against EDGAR full-text search.
4. **Trustable numbers:** every figure traces to a source URL; known data conflicts (see Data Appendix §5) are flagged in the UI, never silently averaged.

## 3. Non-Goals

- **No trade execution or brokerage integration.** Context tool only; keeps scope and risk down.
- **No buy/sell recommendations or price predictions.** Show valuation anchors others published (Morningstar $780B, Damodaran ~$1.3T for SpaceX) as labeled third-party views.
- **No real-time tick data.** Daily close (intraday optional P2). Free-tier data sources only.
- **No multi-user/auth/sharing features.** Single user, local or simple static hosting.
- **No coverage of every 2026 IPO.** The three subject deals + fixed comp sets. Databricks/Cerebras appear only as cohort members.

## 4. User Stories (priority order)

1. As an individual investor, I want a single comparison table of SpaceX/Anthropic/OpenAI vs. historical mega-IPOs and tech IPOs, so that I can judge whether the pricing is historically extreme. *(It is: SpaceX at ~94x trailing sales vs. Facebook ~28x, Google ~16x, Aramco profitable at similar valuation.)*
2. As an individual investor, I want a scatter of day-1 pop vs. 1-year return for landmark tech IPOs, so that I don't over-read SPCX's first trading day.
3. As an individual investor, I want SPCX's daily price vs. its $135 offer price once it lists, so that I can track the deal against its own pricing.
4. As an individual investor, I want to be notified (dashboard flag is enough) when Anthropic's or OpenAI's S-1 becomes public on EDGAR, so that I can read primary financials the day they drop.
5. As an individual investor, I want cohort views (dot-com 1999–2000, 2020–21 SPAC wave, 2025–26 AI cohort), so that I can see how IPO waves resolved historically.
6. As a skeptical reader, I want every number linked to its source and conflicting figures flagged, so that I can verify before acting.

**Edge cases:** SPCX IPO delayed/repriced (dashboard must render with "pending" state); data source down (render last-cached data with staleness timestamp); Anthropic/OpenAI withdraw (status field supports it).

## 5. Requirements

### P0 — Must have
| # | Requirement | Acceptance criteria |
|---|---|---|
| R1 | **Headline view**: 3 deal cards (SpaceX/Anthropic/OpenAI) with status, valuation, raise, revenue, P/S, profitability | Given the data file, when the page loads, then all three cards render with last-updated timestamp; pending deals show "confidential S-1" state |
| R2 | **Mega-IPO league table**: top ~12 raises ever + SpaceX overlay | Sortable by raise/valuation/year; SpaceX row visually distinct; all rows have source links |
| R3 | **Tech IPO comp table + scatter**: ~17 landmark IPOs; scatter of day-1 pop (x) vs 1-yr return (y), point size = raise | Hover shows company detail; quadrant labels make non-correlation visible |
| R4 | **Cohort panel**: dot-com, SPAC wave, AI-2026 cohort summary stats | Each cohort shows: avg day-1 return, % above offer at +1yr (or best available proxy), N; missing stats shown as "not yet computed" not fabricated |
| R5 | **SPCX live tracker**: daily close vs $135 offer line | Updates via scheduled job (daily); renders "not yet trading" before June 12 |
| R6 | **EDGAR S-1 watch**: daily check for public Anthropic/OpenAI S-1 | Status chip flips from "confidential" to "public" with link to filing |
| R7 | **Data integrity**: every metric has `source_url`; conflicts carry a `conflict_note` rendered as ⚠ tooltip | No figure in UI without a source in the data file; the 9 known conflicts (Data Appendix §5) all render flags |

### P1 — Nice to have
- Per-comp price chart since IPO (yfinance daily closes).
- "Multiple compression" view: P/S at IPO vs P/S today for surviving comps.
- Ritter-derived stat: % of 1999–2000 IPOs below offer by 2002 (compute from his long-run returns file — currently a flagged gap; do not cite until computed).
- Export current view as PNG/CSV.

### P2 — Future
- Anthropic/OpenAI S-1 auto-summary when public (LLM pipeline).
- Intraday SPCX during week 1.
- Lockup-expiry calendar for the three deals.

## 6. Architecture (recommended, not mandated)

- **ETL:** Python scripts (yfinance, requests for EDGAR FTS + Nasdaq IPO API, one-time Ritter file ingestion) → writes versioned `data/*.json`. Run daily via cron/Task Scheduler/GitHub Action.
- **Frontend:** single-page static app (vanilla or React + Chart.js/Recharts) reading the JSON. No backend server; host locally or GitHub Pages.
- **Hand-curated seed data:** the verified comparables dataset (Data Appendix file) is committed as `data/comps.json` — the ETL only refreshes *live* fields (prices, filing status), never the historical seed.
- Rationale: separating frozen-historical from live data is what makes "trustable numbers" cheap to maintain.

## 7. Success Metrics (lightweight — personal tool)

- Dashboard answers the user's "should I look deeper?" question without opening >2 other tabs (self-assessed after SPCX week 1).
- Live layer stays current: data staleness < 36h on any trading day, measured by the rendered timestamp.
- Zero unsourced figures in UI (spot-check 10 random metrics).

## 8. Open Questions

| Q | Owner | Blocking? |
|---|---|---|
| Final SPCX pricing/allocation (June 11) — seed data updates needed day 1 | ETL job | No (designed for) |
| What does `intelligence-hatchery` repo provide (agents/skills for financial institutions)? Could replace/augment the ETL or research layer | Solo — repo currently inaccessible (404 to connected account) | No — slot in later |
| Musk voting control: 79% vs >82% — pin from final prospectus | Research pass after pricing | No |
| Where to host (local vs GitHub Pages vs Vercel)? | Solo | Before build handoff |

## 9. Timeline Considerations

- **June 11–12, 2026:** SPCX prices and trades — live tracker is the only date-sensitive piece. Everything else has no deadline.
- Phasing: **Phase 1** (static views R1–R4, seeded data) → **Phase 2** (live layer R5–R6) → **Phase 3** (P1 items). Phase 1+2 are one Claude Code session each, roughly.
