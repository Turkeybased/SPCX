# IPO Research Findings
**As-of date:** June 10, 2026 | **Research plan:** 02-research-plan-for-llms.md

---

## §0 Executive Summary

This document consolidates five completed work packages covering the SpaceX SPCX IPO, Anthropic and OpenAI S-1 watch, the 17-company comp set, valuation anchors, and the Jay Ritter historical IPO dataset. Collectively they represent the primary reference layer for the IPO dashboard project.

**State of research:** SpaceX (WP-2) is the most data-rich package: pricing terms, governance, and order-book figures are sourced from the S-1/A#2 primary filing with independent press corroboration. Day-1 trading data (June 12, 2026) remains the single largest outstanding gap — no actual SPCX open/close prices were available in any indexed source at research close. Both Anthropic and OpenAI (WP-3) have filed confidential S-1s but no public filings exist on EDGAR; all financials are derived from press reports, investor announcements, and sworn court statements rather than audited filings. The comp set (WP-4) is complete with 17 companies sourced primarily from SEC EDGAR 424B4s and live finance data. Valuation anchors (WP-5) resolve cleanly: Morningstar ($780B) and Damodaran ($1.25–1.35T) bracket the SpaceX IPO price (~$1.75–1.77T), and the xAI $6.35B operating loss figure is verified against the primary S-1. The Ritter dataset (WP-1) is fully extracted from primary PDFs updated through May 2026; bubble-era cohort statistics are clearly demarcated as direct figures (aggregate data) vs. ◆computed (year-specific inferencing).

**Key conflicts resolved:** (a) Musk voting power — resolved at 82.4% per S-1/A#2 primary, not 79% or 85%; (b) IPO valuation — both $1.75T and $1.77T are correct per different S-1 share-count scenarios; (c) December 2025 tender — $421/share/$800B confirmed via Reuters/Bloomberg/Fortune; X post claiming "$135/$250B" is erroneous; (d) xAI operating loss — $6.35B (Morningstar/S-1 table) vs. $6.4B (media rounding) — same source, different rounding; (e) Ritter bubble-era "% below offer" — the published 56.1% figure is the 1975–2021 aggregate; year-specific 1999–2000 distributions are ◆computed, not directly reported in any public table.

**WP-6 status:** Blocked — not started as of June 10, 2026.

### Package Status Table

| Package | Topic | Status | Key Output | Data Quality |
|---------|-------|--------|-----------|--------------|
| WP-1 | Ritter IPO Dataset | **Complete** | Full 1980–2025 first-day/long-run/SPAC tables | Primary (Ritter PDFs, updated May 2026) |
| WP-2 | SpaceX SPCX Pricing | **Complete (pre-Day-1)** | Full deal card; governance; order book | Primary (S-1/A#2) + Secondary press |
| WP-3 | Anthropic / OpenAI S-1 | **Complete (pre-public S-1)** | Filing status; all available financials | Secondary (press, investor announcements, court filings) |
| WP-4 | 17-company Comp Set | **Complete** | Summary return table; day-1 and +365d data | Primary (SEC EDGAR 424B4) + Finance data |
| WP-5 | Valuation Anchors | **Complete** | Morningstar / Damodaran vs. IPO price; xAI verification | Primary (S-1) + Independent analyst |
| WP-6 | [Blocked] | **Not started** | — | — |

---

## §1 SpaceX (SPCX) Deal Card [WP-2]

**As-of date:** June 10–11, 2026 (pre-Day-1; June 12 trading data not yet available)

### 1.1 Full Deal Card

| Parameter | Value | Source |
|-----------|-------|--------|
| Issuer | Space Exploration Technologies Corp. | [Fidelity S-1/A#2 PDF](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf) |
| Ticker / Exchange | SPCX / Nasdaq (and Nasdaq Texas) | [CNBC](https://www.cnbc.com/2026/06/03/spacex-ipo-stock-price-roadshow-musk.html) |
| **Offer price** | **$135.00** (fixed; no range) | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf); [CNBC Jun 3](https://www.cnbc.com/2026/06/03/spacex-ipo-stock-price-roadshow-musk.html); [IPO Scoop](https://www.iposcoop.com/the-ipo-buzz-spacex-spcx-proposed-sets-135-share-ipo-price-to-raise-75-billion/) |
| **Shares offered** | 555,555,555 Class A shares (exact) | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf) |
| **Gross proceeds (base)** | ~$75.0B ◆ ($135 × 555,555,555) | [CNBC](https://www.cnbc.com/2026/06/03/spacex-ipo-stock-price-roadshow-musk.html); [NY Times](https://www.nytimes.com/2026/06/03/technology/spacex-ipo-pricing.html) |
| Offering type | All-primary (proceeds to company) | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf) |
| Share class sold | Class A (1 vote/share) | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf) |
| **Greenshoe shares** | Up to 83,333,333 Class A shares | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf); [GraniteShares](https://graniteshares.com/research/everything-you-need-to-know-about-spacex/) |
| Greenshoe window | 30 days after prospectus date | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf) |
| Greenshoe value | ~$11.2B ◆ ($135 × 83,333,333) | [SPCX.capital](https://spcx.capital/spcx-stock-price) |
| **Total raise (greenshoe exercised)** | ~$85.7B ◆ | [Fortune Jun 7](https://fortune.com/2026/06/07/spacex-ipo-selling-price-dislocations-spcx-stock-passive-index-flows-retail-investors/) |
| **Pricing date** | June 11, 2026 (after market close) | [Binance Square](https://www.binance.com/en/square/post/332126333971505) |
| **First trading date** | June 12, 2026 | [NY Times](https://www.nytimes.com/2026/06/10/business/spacex-ipo-what-to-know.html) |
| **Implied market cap (base)** | ~$1.75T / ~$1.77T ◆ | Both figures from S-1 under different share-count scenarios — see §1.2 |
| Directed Share Program | Up to 5% of shares for employees | [Fidelity S-1/A#2](https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf) |
| Retail allocation (target) | ~30% (~$22.5B) | [CNBC Jun 9](https://www.cnbc.com/2026/06/09/spacex-ipo-explained-stock-price-date.html) |
| UK retail allocation | ~£1.5B (~$1.9B) | [BBC](https://www.bbc.com/news/articles/cy8d9e4lzv1o) |
| Retail platforms | Fidelity, Schwab, Robinhood, SoFi, E-Trade (Morgan Stanley) | [CNBC](https://www.cnbc.com/2026/06/09/spacex-ipo-explained-stock-price-date.html) |
| Lead underwriters | Goldman Sachs (lead-left), Morgan Stanley; 21 banks total | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide); [Tech Times](https://www.techtimes.com/articles/318170/20260610/spacex-ipo-order-books-close-four-times-oversubscribed-gray-market-slide-signals-shrinking-premium.htm) |
| 5-for-1 stock split | May 4, 2026 | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide) |

**Filing history:**
- Confidential S-1 filed: April 1, 2026 ([Capital.com](https://capital.com/en-eu/learn/ipo/spacex-ipo))
- Public S-1 filed: May 20, 2026 ([CNBC live updates](https://www.cnbc.com/2026/05/20/spacex-ipo-live-updates.html))
- S-1/A Amendment 1: June 1, 2026 ([ChartDojo](https://blog.chartdojo.io/spacex-ipo-1-75-trillion-spcx-nasdaq-june-4-2026/))
- S-1/A Amendment 2 (terms, $135 price): June 3, 2026 ([IPO Scoop](https://www.iposcoop.com/the-ipo-buzz-spacex-spcx-proposed-sets-135-share-ipo-price-to-raise-75-billion/))
- 424B4 final prospectus: ❌ Not yet confirmed filed as of research close (blocked by EDGAR robots.txt; would be filed post June 11 pricing)

**Key financial metrics (from S-1):**

| Metric | Value | Source |
|--------|-------|--------|
| 2025 Revenue (consolidated, post-xAI) | $18.67B (+33% YoY) | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide); [WSJ May 20](https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-05-20-2026/card/spacex-and-xai-made-18-7-billion-in-2025-ZRZoT7TJaiy4cIV3wEYv) |
| 2025 Starlink revenue | $11.4B (61% of total) | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide) |
| 2025 EBITDA | $6.58B | [Morningstar S-1 charts](https://www.morningstar.com/stocks/6-charts-spacexs-s-1-financials) |
| 2025 Net loss (consolidated) | -$4.94B | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide) |
| Q1 2026 Net loss | -$4.28B | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide) |
| Accumulated deficit | -$41.3B | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide) |
| Q1 2026 financial position | ~$30B debt, $16B cash, net debt ~$14B | [Morningstar](https://global.morningstar.com/en-ca/stocks/spacex-what-investors-need-know-about-its-enormous-upcoming-ipo) |
| P/S ratio at offer price ◆ | ~94–107× 2025 revenue | [abhs.in](https://www.abhs.in/blog/spacex-ipo-135-fixed-price-roadshow-june-4-75-billion-spcx-2026) |
| SpaceX market share in mass-to-orbit (2025) | 83% | [Morningstar](https://global.morningstar.com/en-ca/stocks/spacex-what-investors-need-know-about-its-enormous-upcoming-ipo) |

### 1.2 Valuation — $1.75T vs. $1.77T (Conflict Resolved)

Both figures appear in the S-1/A filing. The difference reflects whether the pending EchoStar spectrum acquisition and Cursor transaction are included in the share-count denominator. Neither figure is erroneous; both are reported from different S-1 scenarios.

| Source | Valuation | Notes |
|--------|-----------|-------|
| Bloomberg, abhs.in, BitMEX | ~$1.75T | Pre-transaction scenario |
| CNBC, GraniteShares, IPO Scoop, NY Times | ~$1.77T | With pending acquisitions included |
| NY Times notes | 40%+ premium to Feb 2026 self-assessed $1.25T value | [NY Times](https://www.nytimes.com/2026/06/03/technology/spacex-ipo-pricing.html) |

### 1.3 Voting Power — Conflict #2 Resolved

**Resolution: S-1/A#2 primary filing governs. Musk voting power = 82.4% (base) / 82.3% (post-greenshoe).**

| Source | Voting % | Notes |
|--------|----------|-------|
| **Fidelity S-1/A#2 (primary)** | **82.4%** (82.3% if greenshoe fully exercised) | 81.1% via Class B alone; authoritative |
| CNBC Jun 3 | >82% | Consistent with S-1 |
| GraniteShares | >82% | Consistent with S-1 |
| BitMEX | 85% | Not corroborated; likely includes post-close adjustments or rounding error |
| "79%" (stale pre-filing estimate) | — | **Not sourced in any primary document** |

**Governance structure:**
- Class A shares: 1 vote/share (public float)
- Class B shares: 10 votes/share (Musk-held exclusively; 5,602M shares)
- Class A shares outstanding: 6,932M
- SpaceX classified as a **"controlled company"** under Nasdaq rules; Class B shareholders elect board majority

### 1.4 December 2025 Tender Offer Context (Conflict #3 Resolved)

**Resolution: $421/share, $800B valuation is the authoritative pre-IPO tender price.**

| Item | Value | Source |
|------|-------|--------|
| Date | December 12, 2025 (CFO letter date) | [Reuters Dec 13 2025](https://www.reuters.com/business/spacex-sets-800-billion-valuation-bloomberg-news-reports-2025-12-13/) |
| Valuation | ~$800B | [Reuters](https://www.reuters.com/business/spacex-sets-800-billion-valuation-bloomberg-news-reports-2025-12-13/); [Bloomberg Dec 13 2025](https://www.bloomberg.com/news/articles/2025-12-13/spacex-sets-insider-share-deal-at-about-800-billion-valuation); [Fortune Dec 13 2025](https://fortune.com/2025/12/13/spacex-ipo-plan-2026-secondary-offering-insider-share-sale-800-billion-valuation/) |
| Price per share (pre-split) | $421/share | [Reuters](https://www.reuters.com/business/spacex-sets-800-billion-valuation-bloomberg-news-reports-2025-12-13/) |
| Price per share (split-adjusted, 5-for-1) | ~$84.20 ◆ ($421 ÷ 5) | ◆ Computed |
| Total authorized deal | Up to $2.56B in shares | [Reuters](https://www.reuters.com/business/spacex-sets-800-billion-valuation-bloomberg-news-reports-2025-12-13/) |
| Prior tender (July 2025) | ~$400B at $212/share | [Fortune](https://fortune.com/2025/12/13/spacex-ipo-plan-2026-secondary-offering-insider-share-sale-800-billion-valuation/) |
| Implied premium of IPO over Dec tender ◆ | ~61% (split-adjusted $84.20 → $135 IPO) | ◆ Computed |

**Erroneous figure flagged:** An X post (@marketsday, Jun 3) claimed "$135/share, ~$250B valuation" for the December 2025 tender. This is **inconsistent** with Reuters, Bloomberg, and Fortune primary reporting. The $421/share, $800B figures are used throughout.

### 1.5 Order Book & Demand

| Metric | Figure | Source |
|--------|--------|--------|
| Total investor demand (final) | ~$250B | [Eastern Herald / Reuters](https://easternherald.com/2026/06/10/spacex-ipo-oversubscribed-record-250-billion-demand/) |
| Institutional order book | ~$150B | [FinanceFeeds](https://financefeeds.com/spacex-valuation-after-ipo-spcx-year-one/) |
| Oversubscription (Bloomberg TV) | ~2× the $75B offering | [Bloomberg TV Jun 9](https://www.youtube.com/watch?v=yGtUFGjq-5o) |
| Oversubscription (Reuters/Eastern Herald) | 3.5–4× (~$250–300B) | [Eastern Herald](https://easternherald.com/2026/06/10/spacex-ipo-oversubscribed-record-250-billion-demand/) |
| Single institutional orders | $10B+ each from multiple firms | [Bloomberg / Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/spacex-ipo-said-well-oversubscribed-154906500.html) |

**Conflict noted:** Bloomberg TV cites ~2× (~$150B); Eastern Herald/Reuters cites 3.5–4× (~$250–300B). The $250B figure is more widely cited in post-Jun 9 reporting.

### 1.6 Lock-Up Structure

| Feature | Detail | Source |
|---------|--------|--------|
| Structure | Staggered (not standard 180-day) | [GraniteShares](https://graniteshares.com/research/everything-you-need-to-know-about-spacex/) |
| First unlock | 20% of holdings at first quarterly earnings post-IPO | [GraniteShares](https://graniteshares.com/research/everything-you-need-to-know-about-spacex/) |
| Subsequent unlocks | +7% at 70, 90, 105, 120, and 135 days post-IPO | [GraniteShares](https://graniteshares.com/research/everything-you-need-to-know-about-spacex/) |
| Elon Musk | 366-day holding requirement | [abhs.in](https://www.abhs.in/blog/spacex-ipo-135-fixed-price-roadshow-june-4-75-billion-spcx-2026) |
| Full lockup expiration (estimated) | September–December 2026 | [BitMEX](https://www.bitmex.com/blog/spacex-ipo-guide) |

### 1.7 Day-1 Trading: Status as of June 10, 2026

**Day-1 trading data (June 12, 2026) is NOT YET AVAILABLE in any indexed source at research close.**

| Indicator | Price / Valuation | As-of | Source |
|-----------|-------------------|-------|--------|
| Hyperliquid perpetual futures (gray market) | ~$157/share (~$2.07T implied) | Jun 10, 2026 | [Tech Times](https://www.techtimes.com/articles/318170/20260610/spacex-ipo-order-books-close-four-times-oversubscribed-gray-market-slide-signals-shrinking-premium.htm) |
| Hyperliquid peak (mid-May) | ~$216–230/share | ~May 15–20 | [Tech Times](https://www.techtimes.com/articles/318170/20260610/spacex-ipo-order-books-close-four-times-oversubscribed-gray-market-slide-signals-shrinking-premium.htm) |
| Implied first-day premium (gray market, Jun 10) | ~16% above $135 offer | Jun 10, 2026 | [Tech Times](https://www.techtimes.com/articles/318170/20260610/spacex-ipo-order-books-close-four-times-oversubscribed-gray-market-slide-signals-shrinking-premium.htm) |
| Polymarket (first close consensus) | ~$2.3T (~$175/share ◆) | Pre-Jun 11 | [FinanceFeeds](https://financefeeds.com/spacex-valuation-after-ipo-spcx-year-one/) |
| Polymarket: probability SPCX closes above $135 | 75% | Pre-Jun 11 | [FinanceFeeds](https://financefeeds.com/spacex-valuation-after-ipo-spcx-year-one/) |

> **Note:** The gray market is not actual trading. All day-1 figures above are pre-market indicators only.

---

## §2 Anthropic S-1 Watch [WP-3]

**As-of date:** June 10, 2026

### 2.1 Filing Status

| Item | Detail | Source |
|------|--------|--------|
| Confidential S-1 filed | **Yes** — June 1, 2026 | [Anthropic.com](https://www.anthropic.com/news/confidential-draft-s1-sec) |
| Filing entity | Anthropic, PBC | [Anthropic.com](https://www.anthropic.com/news/confidential-draft-s1-sec) |
| Public S-1 on EDGAR | **No** — under confidential SEC review | [CNBC Jun 1](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html) |
| Number of shares / IPO price | Not yet set | [Anthropic.com](https://www.anthropic.com/news/confidential-draft-s1-sec) |
| Estimated public S-1 timing | ~Summer–Fall 2026 | [Zacks Jun 10](https://www.zacks.com/featured-articles/761/anthropic-ipo) |
| Target IPO window | ~October 2026 | [Yahoo Finance May 16](https://finance.yahoo.com/markets/article/spacex-openai-and-anthropic-here-are-the-most-anticipated-ipos-in-2026-114439441.html) |
| Ticker / Exchange | Not announced | [Zacks Jun 10](https://www.zacks.com/featured-articles/761/anthropic-ipo) |
| Lead underwriters | Morgan Stanley, Goldman Sachs, JPMorgan | [Bloomberg via Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/anthropic-said-pick-morgan-stanley-175802678.html) |

**Anthropic's verbatim statement:** *"This gives us the option to go public after the SEC completes its review. The proposed initial public offering will depend on market conditions and other factors."*

### 2.2 Fundraising History & Valuation Trajectory

| Round | Date | Amount | Post-Money Valuation | Lead Investors | Source |
|-------|------|--------|---------------------|----------------|--------|
| Series E | Mar 3, 2025 | $3.5B | $61.5B | Lightspeed VP | [Anthropic.com](https://www.anthropic.com/news/anthropic-raises-series-e-at-usd61-5b-post-money-valuation) |
| Series F | ~Sep 2025 | $13B | $183B | Iconiq Capital | [NYT Sep 2 2025](https://www.nytimes.com/2025/09/02/technology/anthropic-funding-ai.html) |
| (informal) | ~Nov 2025 | — | ~$350B | Microsoft/Nvidia partnerships | [CNBC Nov 18 2025](https://www.cnbc.com/2025/11/18/anthropic-ai-azure-microsoft-nvidia.html) |
| Series G | Feb 12, 2026 | $30B | **$380B** | GIC, Coatue | [Anthropic.com](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) |
| Series H | May 28, 2026 | **$65B** | **$965B** | Altimeter, Dragoneer, Greenoaks, Sequoia | [Anthropic.com](https://www.anthropic.com/news/series-h); [TechCrunch May 28](https://techcrunch.com/2026/05/28/anthropic-raises-65-billion-nears-1t-valuation-ahead-of-ipo/) |

◆ **Valuation re-rating:** $61.5B (March 2025) → $965B (May 2026) = ~15.7× in approximately 14 months.

**Series H co-investors:** Capital Group, Coatue, D1 Capital Partners, GIC, ICONIQ, XN, AMP PBC, Baillie Gifford, Blackstone, Brookfield, D.E. Shaw, DST Global, Fidelity, General Catalyst, Insight Partners, Jane Street, Lightspeed, MGX, NTTVC, T. Rowe Price, Temasek, Samsung, SK Hynix, Micron. Note: $15B of the $65B represents previously committed hyperscaler investments (including $5B from Amazon).

**Hyperscaler strategic stakes:**
- **Amazon:** Previously invested $8B; additional $5B Series H; committed $100B+ in AWS compute over 10 years; potential additional $20B
- **Google:** Committed up to $40B (with milestones); $10B immediate; $200B cloud spend over 5 years; 5 GW next-gen TPU capacity
- **Microsoft:** $10B investment; $30B Azure compute commitment; up to 1 GW additional capacity
- **NVIDIA:** $5B investment

### 2.3 Revenue Timeline

| Period | Revenue / Run Rate | Source | Notes |
|--------|--------------------|--------|-------|
| Dec 2024 | ~$1B ARR | [CNBC May 30 2025](https://www.cnbc.com/2025/05/30/anthropic-hits-3-billion-in-annualized-revenue-on-business-demand-for-ai.html) | |
| May 30, 2025 | ~$3B ARR | [CNBC May 30 2025](https://www.cnbc.com/2025/05/30/anthropic-hits-3-billion-in-annualized-revenue-on-business-demand-for-ai.html); [Reuters](https://www.reuters.com/business/anthropic-hits-3-billion-annualized-revenue-business-demand-ai-2025-05-30/) | Two sources confirm |
| Q4 2025 (end) | ~$9B ARR | [SaaStr Feb 15 2026](https://www.saastr.com/anthropic-just-hit-14-billion-in-arr-up-from-1-billion-just-14-months-ago/) | |
| Feb 12, 2026 | **$14B ARR** | [Anthropic Series G](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation); [SaaStr Feb 15 2026](https://www.saastr.com/anthropic-just-hit-14-billion-in-arr-up-from-1-billion-just-14-months-ago/) | Two sources confirm |
| Q1 2026 (GAAP quarterly) | **$4.8B** | [CNBC May 20 2026](https://www.cnbc.com/2026/05/20/anthropic-revenue-explosive-growth-ipo-profitable-quarter.html) | |
| Apr 2026 | ~$30B ARR | [Zacks Jun 10](https://www.zacks.com/featured-articles/761/anthropic-ipo) | |
| May 2026 | **$47B ARR** | [Anthropic Series H](https://www.anthropic.com/news/series-h); [CNBC May 28 2026](https://www.cnbc.com/2026/05/28/anthropic-open-ai-startup-value.html) | Two sources confirm |

**⚠️ Revenue figure disagreement on 2025 annual:** Three conflicting figures — (1) The Information: ~$4.5B ("nearly 12× last year's total"); (2) CFO Krishna Rao sworn court declaration (Mar 9, 2026): ">$5B to date"; (3) CNBC (May 28, 2026): ~$10B. Likely reflect different methodologies (recognized GAAP vs. ARR vs. cumulative). Public S-1 will be authoritative.

**Additional metrics:** Claude Code run-rate (May 2026): ~$8B ARR (from ~$500M ARR in Sep 2025); >500 customers spending $1M+ annually; 8 of Fortune 10 are Claude customers.

### 2.4 Path to Profitability

| Period | Figure | Source |
|--------|--------|--------|
| 2024 EBITDA loss | ~-$6B cash flow | [Reddit/analyst](https://www.reddit.com/r/Anthropic/comments/1s8bltu/how_much_money_is_anthropic_really_losing/) |
| 2025 EBITDA loss | ~-$4B to -$5.2B | [LinkedIn/The Information](https://www.linkedin.com/posts/gennarocuofano_anthropic-lowers-gross-margin-projection-activity-7419976159246979072-AEZp) |
| 2025 gross margin | ~40% (vs. 50% prior projection; vs. -94% in 2024) | [LinkedIn/analyst](https://www.linkedin.com/posts/gennarocuofano_anthropic-lowers-gross-margin-projection-activity-7419976159246979072-AEZp) |
| Q2 2026 (projected) | **First ever operating profit: ~$559M** (on $10.9B projected revenue) | [CNBC May 20 2026](https://www.cnbc.com/2026/05/20/anthropic-revenue-explosive-growth-ipo-profitable-quarter.html) — investor materials |
| 2026 full year | ~-$14B cash flow (loss persists despite Q2 operating profit) | [Digital Applied May 30 2026](https://www.digitalapplied.com/blog/anthropic-65b-series-h-965b-valuation-frontier-market-2026) |
| 2026 projected loss | ~-$11B cash flow | [Reddit discussion](https://www.reddit.com/r/Anthropic/comments/1s8bltu/how_much_money_is_anthropic_really_losing/) |
| 2028 | **Break-even / first annual profitability** | [WSJ Nov 10 2025](https://www.wsj.com/tech/ai/openai-anthropic-profitability-e9f5bcd6) |
| 2028 gross margin projection | 77% | [Yahoo Finance / The Information](https://finance.yahoo.com/news/anthropic-projects-70b-revenue-2028-164854310.html) |
| 2028 revenue projection | ~$70B | [Yahoo Finance Nov 4 2025](https://finance.yahoo.com/news/anthropic-projects-70b-revenue-2028-164854310.html) |

**Caveat:** The Q2 2026 operating profit projection is an *operating* figure, not GAAP net income, and excludes frontier model training capex.

Anthropic cash burn vs. OpenAI (per Fortune): 2026 Anthropic burns ~one-third of revenue vs. OpenAI ~57%; 2027 ~9% vs. ~57%; OpenAI expected to burn cumulatively ~14× as much cash as Anthropic before profitability. ([Fortune Nov 12 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/))

### 2.5 Governance Structure: PBC + LTBT

**Corporate form:** Delaware Public Benefit Corporation (PBC)
**Public benefit purpose (charter):** "The responsible development and maintenance of advanced AI for the long-term benefit of humanity"

**Long-Term Benefit Trust (LTBT):**

| Feature | Detail | Source |
|---------|--------|--------|
| What it is | Independent purpose trust of 5 financially disinterested trustees | [Anthropic.com Sep 2023](https://www.anthropic.com/news/the-long-term-benefit-trust) |
| Special share class | **Class T Common Stock** — held exclusively by the Trust | [Anthropic.com](https://www.anthropic.com/news/the-long-term-benefit-trust) |
| Board election power | Elects growing share of Anthropic board; ultimately majority (3 of 5+ seats) | [Harvard Law Oct 2023](https://corpgov.law.harvard.edu/2023/10/28/anthropic-long-term-benefit-trust/) |
| Phase-in milestone | LTBT elects majority within ~4 years of Series C (~2027) | [Anthropic.com](https://www.anthropic.com/news/the-long-term-benefit-trust) |
| Current trustees | Neil Buddy Shah (Chair), Richard Fontaine, Mariano-Florentino Cuéllar | [LuminixAI Jun 2026](https://www.useluminix.com/reports/company-overviews/what-do-we-know-about-the-anthropic-ipo/source/4) |
| Current board | Dario Amodei, Daniela Amodei, Yasmin Razavi, Reed Hastings, Chris Liddell, Vas Narasimhan | [LuminixAI Jun 2026](https://www.useluminix.com/reports/company-overviews/what-do-we-know-about-the-anthropic-ipo/source/4) |
| Trustee independence | Trustees hold no equity in Anthropic | [Anthropic.com](https://www.anthropic.com/news/the-long-term-benefit-trust) |
| Failsafe override | Supermajority of stockholders can amend Trust (threshold increases over time) | [Anthropic.com](https://www.anthropic.com/news/the-long-term-benefit-trust) |

**Key governance point for IPO investors:** Public IPO shares would likely be standard common stock — public investors would NOT control a board majority. Amazon and Google (equity investors) hold no voting shares. The LTBT structure is functionally distinct from founder-supervoting dual-class: an independent third-party trust (not founders) elects the majority board. ([Harvard Law](https://corpgov.law.harvard.edu/2023/10/28/anthropic-long-term-benefit-trust/))

### 2.6 Compute Commitments

| Partner | Commitment | Capacity | Timeline | Source |
|---------|-----------|----------|----------|--------|
| Amazon AWS | >$100B over 10 years | Up to 5 GW new capacity | 10-year deal signed Apr 20, 2026 | [TechInformed May 2026](https://techinformed.com/anthropic-turns-to-spacex-for-claude-capacity/) |
| Google Cloud / Broadcom | ~$200B over 5 years | 5 GW next-gen TPU | From 2027 | [Yahoo Finance May 5 2026](https://finance.yahoo.com/sectors/technology/articles/anthropic-commits-spending-200-billion-204952501.html) |
| Microsoft Azure | $30B committed + up to 1 GW | Up to 1 GW | Nov 2025 deal | [Reuters Nov 18 2025](https://www.reuters.com/technology/anthropic-commits-30-billion-microsoft-azure-compute-2025-11-18/) |
| SpaceX Colossus 1 & 2 | $1.25B/month (~$15B/yr); contract to May 2029 | >300 MW; >220,000 Nvidia GPUs | Signed ~May 2026 | [CNBC Jun 1 2026](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html); [Damodaran post-prospectus](https://aswathdamodaran.substack.com/p/revisiting-the-spacex-valuation-a) |
| Akamai | $1.8B | Additional capacity | Recent | [Brownstone Research](https://www.brownstoneresearch.com/bleeding-edge/anthropic-or-misanthropic/) |
| Fluidstack (TX/NY data centers) | $50B | New Anthropic-dedicated sites | Through 2026 | [Reddit/analyst](https://www.reddit.com/r/ClaudeAI/comments/1thzy0a/anthropic_announced_vs_current_compute_capacity/) |

**◆ Total disclosed compute commitments: ~$382B+** (Amazon $100B + Google/Broadcom ~$200B + Microsoft $30B + Akamai $1.8B + Fluidstack $50B). Note: the Google $200B figure is from Brownstone Research analysis of their deal, not a company-stated figure.

### 2.7 Key Uncertainties

1. **Compute obligation risk** — $382B+ in committed cloud/compute spend; revenue stall creates existential cash pressure
2. **Revenue credibility** — ARR vs. GAAP vs. cumulative figures conflict in public statements; gross vs. net accounting treatment for hyperscaler compute credits unresolved
3. **LTBT governance** — public shareholders will not control board; limits activist rights
4. **Hyperscaler concentration & conflict** — AWS is primary cloud AND equity investor; Google same
5. **Unauthorized SPV trading** — Anthropic issued enforcement notices against 8 firms; cap-table complexity
6. **Valuation risk** — $965B implies one of the largest IPOs in history with no comps at similar loss/scale profiles

---

## §3 OpenAI S-1 Watch [WP-3]

**As-of date:** June 10, 2026

### 3.1 Filing Status

| Item | Detail | Source |
|------|--------|--------|
| Confidential S-1 filed | **Yes** — June 8, 2026 | [CNBC Jun 8](https://www.cnbc.com/2026/06/08/openai-confidentially-files-for-ipo-prepping-wall-street-for-ai-debut.html) |
| Filing entity | OpenAI Group PBC | [OpenAI.com](https://openai.com/index/built-to-benefit-everyone/) |
| Public S-1 on EDGAR | **No** | [Zacks Jun 9](https://www.zacks.com/featured-articles/781/openai-ipo) |
| Target IPO window | ~Q4 2026 ("fall 2026") | [CNBC Jun 8](https://www.cnbc.com/2026/06/08/openai-confidentially-files-for-ipo-prepping-wall-street-for-ai-debut.html) |
| Ticker / Exchange | Not announced (Nasdaq or NYSE expected) | [Zacks Jun 9](https://www.zacks.com/featured-articles/781/openai-ipo) |
| Lead underwriters | Goldman Sachs, Morgan Stanley | [CNBC Jun 8](https://www.cnbc.com/2026/06/08/openai-confidentially-files-for-ipo-prepping-wall-street-for-ai-debut.html); [Yahoo Finance/Quartz](https://finance.yahoo.com/markets/stocks/articles/openai-confidentially-files-ipo-sec-223341186.html) |
| Internal disagreement on timing | Yes — CEO Altman vs. CFO Friar at odds | [YouTube Jun 9 2026](https://www.youtube.com/watch?v=y10KKLzqdH8) |
| FutureSearch central IPO estimate | ~November 2026 | [FutureSearch](https://futuresearch.ai/openai-financial-forecast/) |

**OpenAI's statement:** *"We have not decided on timing yet. It may be a while because there are things we want to do that are likely easier as a private company."*

### 3.2 PBC Conversion Status & Governance

**Conversion completed October 28, 2025.**

| Item | Detail | Source |
|------|--------|--------|
| New entity name | **OpenAI Group PBC** (Delaware PBC) | [OpenAI.com Oct 28 2025](https://openai.com/index/built-to-benefit-everyone/) |
| Nonprofit entity | **OpenAI Foundation** (formerly OpenAI Inc.) | [OpenAI.com](https://openai.com/index/built-to-benefit-everyone/) |
| Foundation equity stake | **26%** of OpenAI Group PBC | [CNBC Oct 28 2025](https://www.cnbc.com/2025/10/28/open-ai-for-profit-microsoft.html) |
| Foundation control | Foundation retains power to appoint **all** board members; safety committee can veto model releases | [OpenAI.com](https://openai.com/index/built-to-benefit-everyone/) |
| Profit caps | **Removed** — investors now entitled to uncapped returns | [Skycrumbs Jun 2 2026](https://skycrumbs.com/blog/openai-restructuring-for-profit-2026) |
| Microsoft stake | ~27% of OpenAI Group PBC (fully diluted; ~$135B at conversion) | [CNBC Oct 28 2025](https://www.cnbc.com/2025/10/28/open-ai-for-profit-microsoft.html) |
| Sam Altman equity | ~7% (expected) | [YouTube analysis](https://www.youtube.com/watch?v=tvGD2Sntkb4) |
| Microsoft revenue arrangement | 20% of OpenAI revenue until AGI certified by independent expert panel | [EA Forum Nov 17 2025](https://forum.effectivealtruism.org/posts/Tcy5HAg3d9LXDRGfq/the-openai-governance-transition-the-history-what-it-is-and-1) |
| Microsoft IP access | Extended to 2032, including post-AGI models | [EA Forum Nov 17 2025](https://forum.effectivealtruism.org/posts/Tcy5HAg3d9LXDRGfq/the-openai-governance-transition-the-history-what-it-is-and-1) |
| Regulatory approvals | California and Delaware AGs did not oppose | [thegeniusfactory.net Jun 7 2026](https://thegeniusfactory.net/ai-governance/the-conversion-what-turning-the-largest-nonprofit-into-a-company-did-to-charity/) |

**Ownership table (at conversion, October 2025):**

| Stakeholder | Stake | Value at Close (~$500B) |
|-------------|------:|------------------------|
| OpenAI Foundation (nonprofit) | 26% | ~$130B |
| Microsoft | ~27% (fully diluted) | ~$135B |
| Employees + other investors | ~47% | — |
| Sam Altman (CEO) | ~7% (expected) | ~$11B+ |

**Critics' note:** Zvi Mowshowitz called this "potentially the largest theft in history" given Foundation's pre-conversion claim on the bulk of profit interests. ([Substack Nov 2025](https://thezvi.substack.com/p/openai-moves-to-complete-potentially))

### 3.3 Revenue Figures

| Period | Revenue / ARR | Source | Notes |
|--------|--------------|--------|-------|
| 2023 | ~$1B | [FutureSearch](https://futuresearch.ai/openai-revenue-forecast/) | |
| 2024 (annual) | ~$3.7B–$4B | [Reuters/CFO Friar](https://www.reuters.com/business/openai-cfo-says-annualized-revenue-crosses-20-billion-2025-2026-01-19/) | Multiple sources consistent |
| 2025 (annual) | **$13B** (CFO-stated) | [CFO Friar at Goldman Sachs Sep 2025](https://finance.yahoo.com/news/openai-cfo-we-will-more-than-triple-our-revenue-this-year-213816957.html); [Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) | Two sources confirm |
| Jan 2026 ARR | **>$20B** | [Reuters Jan 19 2026](https://www.reuters.com/business/openai-cfo-says-annualized-revenue-crosses-20-billion-2025-2026-01-19/) | CFO-stated |
| Feb 2026 ARR | ~$25B | [Yahoo Finance via Sacra Mar 2026](https://finance.yahoo.com/news/openai-tops-25-billion-annualized-033836274.html) | |
| Q1 2026 (quarterly GAAP) | **$5.7B** | [The Information via Ed Zitron May 2026](https://www.wheresyoured.at/news-openai-had-a-negative-122-operating-margin-in-q1-2026-and-chatgpt-growth-has-stalled/) | |
| 2026 full year (target) | ~$30B | [Ed Zitron May 2026](https://www.wheresyoured.at/news-openai-had-a-negative-122-operating-margin-in-q1-2026-and-chatgpt-growth-has-stalled/) | "On track" per reports |
| 2027 (internal projection) | ~$59.8B | [Epoch AI Nov 2025](https://epochai.substack.com/p/openai-is-projecting-unprecedented) | |
| 2028 (internal projection) | ~$100B | [Epoch AI Nov 2025](https://epochai.substack.com/p/openai-is-projecting-unprecedented) | |
| 2030 (internal projection) | ~$200B | [Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) | |

**Key user metric:** ~900 million weekly active ChatGPT users; ~50 million paying consumer subscribers; ~$2B/month revenue. ([CNBC Jun 8 2026](https://www.cnbc.com/2026/06/08/openai-confidentially-files-for-ipo-prepping-wall-street-for-ai-debut.html))

**Gross margin (Sacra estimate):** 33% in 2025, constrained by $8.4B in inference costs. ([Sacra](https://sacra.com/c/openai/))

### 3.4 Loss Projections Table

| Year | Net / Operating Loss | Source | Notes |
|------|---------------------|--------|-------|
| 2025 | ~$9B net loss (on $13B revenue; spending ~$22B) | [Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) | $1.69 spent per $1 earned |
| Q1 2026 | ~$6.95B non-GAAP operating loss (on $5.7B revenue); **-122% non-GAAP operating margin** | [The Information via Ed Zitron May 22 2026](https://www.wheresyoured.at/news-openai-had-a-negative-122-operating-margin-in-q1-2026-and-chatgpt-growth-has-stalled/) | |
| 2026 (non-GAAP internal) | ~$14B | [Yahoo Finance Jan 2026](https://finance.yahoo.com/news/openais-own-forecast-predicts-14-150445813.html) | Multiple sources |
| 2026 (GAAP estimate) | ~$25–26B | [FutureSearch May 2026](https://futuresearch.ai/openai-financial-forecast/) | Adds ~$7–10B stock comp |
| 2028 | ~$74B–$85B operating loss | [Fortune/WSJ Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) | **Conflict: WSJ $74B vs. TechCrunch/AI Weekly $85B — both cited, not averaged** |
| Cumulative 2023–2028 (excl. stock comp) | ~$44B | [Foundation Capital Oct 2024](https://foundationcapital.com/ideas/why-openai-s-157b-valuation-misreads-ai-s-future) | Older internal document |
| **Cumulative through 2029 (cash burn, current) ** | **~$115B** | [The Information via Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) | More current; more authoritative |
| Cumulative negative FCF 2024–2029 | **~$143B** | [Deutsche Bank via eMarketer Dec 2025](https://www.emarketer.com/content/openai-forecast-143-billion-loss-raises-stakes-ai-monetization) | **Different metric**: includes capex |
| Profitability target | ~2029–2030 | [Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) | Cash-flow positive 2029/2030; meaningful profit 2030 |

**⚠️ Key conflict on cumulative losses:** "$44B total losses" (2023–2028, excl. stock comp; older internal docs) vs. "$115B cumulative cash burn" (through 2029; current The Information/Fortune) vs. "$143B cumulative negative FCF" (2024–2029; Deutsche Bank including capex). These are three distinct metrics, frequently conflated in media.

**2029 timeline conflict:** Some sources imply profitability in 2028 vs. Fortune/WSJ primary sources placing it in 2029–2030. The 2029–2030 figure from Fortune (citing financial documents) is treated as more authoritative.

**Microsoft equity-method corroboration:** Microsoft Q1 FY26 10-Q disclosed $3.1B quarterly decrease in net income from its OpenAI equity investment (27% diluted stake). ◆ Implied OpenAI quarterly loss ~$11.5B ($3.1B ÷ 0.27), or ~$46B annualized. ([Shanaka Anslem Perera Feb 10 2026](https://shanakaanslemperera.substack.com/p/the-thermodynamic-reckoning-openai))

### 3.5 Compute Commitments

| Item | Amount | Source |
|------|--------|--------|
| Compute/cloud deal commitments (8 years) | **~$1.4 trillion** | [Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) |
| Backup data-center capacity commitment | ~$100B | [Fortune Nov 2025](https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/) |
| Aggregate AI infrastructure (OpenAI + partners through 2030) | Could exceed $600B | [Zacks Jun 9](https://www.zacks.com/featured-articles/781/openai-ipo) |
| 2025 inference costs | $8.4B | [Sacra](https://sacra.com/c/openai/) |
| 2026 inference costs (projected) | $14.1B | [Sacra](https://sacra.com/c/openai/) |

**Key compute partners:** Microsoft Azure (primary), Oracle, Amazon, NVIDIA. HSBC projects a $207B funding shortfall by 2030 even if revenue meets targets. ([Yahoo Finance](https://finance.yahoo.com/news/openai-is-the-2025-yahoo-finance-company-of-the-year-120054312.html))

### 3.6 Side-by-Side Anthropic vs. OpenAI

| Dimension | Anthropic | OpenAI |
|-----------|-----------|--------|
| Confidential S-1 filed | Yes (Jun 1, 2026) | Yes (Jun 8, 2026) |
| Public S-1 on EDGAR | No | No |
| Target IPO window | ~Oct 2026 | ~Q4 2026 (Fall) |
| Corporate form | Delaware PBC | Delaware PBC (OpenAI Group PBC) |
| Governance overlay | LTBT — Class T shares, independent trustees elect majority board | OpenAI Foundation controls for-profit; 26% equity, all board appointments |
| Latest private valuation | **$965B** (May 28, 2026) | **$852B** (March 2026) |
| Most recent revenue run rate | ~$47B ARR (May 2026) | ~$24B ARR (~May 2026) |
| Q1 2026 quarterly revenue | $4.8B | $5.7B |
| 2025 annual revenue | ~$4.5B–$10B (disputed) | ~$13B (CFO-confirmed) |
| Q1 2026 operating margin | First operating profit projected Q2 2026 (~$559M) | **-122% non-GAAP** |
| 2025 gross margin | ~40% | ~33% |
| 2028 loss projection | Break-even / first profit | ~$74–85B operating loss |
| Cumulative losses (to 2029) | Not publicly disclosed | **~$115B** (The Information) |
| Lead underwriters | Morgan Stanley, Goldman Sachs, JPMorgan | Goldman Sachs, Morgan Stanley |
| Compute commitments | >$382B+ | ~$1.4T over 8 years |
| Major strategic investors | Amazon, Google, Microsoft, NVIDIA | Microsoft (~27%), SoftBank, Amazon, NVIDIA |

---

## §4 Valuation Anchors & Bear Cases [WP-5]

**As-of date:** June 9, 2026

### 4.1 SpaceX: Three-Analyst Summary

| Analyst/Firm | Date | Methodology | Equity Value | Per Share | vs. $135 IPO |
|-------------|------|------------|-------------|-----------|--------------|
| **Morningstar** (Nicolas Owens) | Jun 5–8, 2026 | DCF + probability-weighted AI scenarios | **$780B EV** | **~$63/sh** ◆ | −53% discount |
| **Damodaran** (NYU Stern) — pre-prospectus | Apr 23, 2026 | SOTP DCF (3 segments + options) | $1.22T (base); $1.29T (sim. median) | — | ~−35% |
| **Damodaran** — post-prospectus | Jun 4, 2026 | Updated SOTP with S-1 data | **$1.25–1.35T (~$1.30T midpoint)** | **~$100/sh** | ~−26% |
| **IPO market** | Jun 11, 2026 | Bookbuild pricing | **~$1.75–1.77T** | $135 | — |

**Morningstar segment breakdown:**

| Segment | Enterprise Value | Notes |
|---------|-----------------|-------|
| Space launch + connectivity | $611B | Starlink slower-growth post-2028 could reduce by $65B |
| AI segment (probability-weighted) | $170B | Blended: MVP 50% probability / Moonshot 7% / No-Go 43% |
| **Total** | **$780B** | |

**Morningstar AI scenario analysis:**

| Scenario | Probability | Standalone Value | Weighted |
|----------|------------|-----------------|---------|
| MVP (4% of global AI compute) | 50% | $230B | $114B |
| Moonshot (~1/5 of global AI compute) | 7% | ~$1.3T | $93B |
| No Go (orbital AI fails) | 43% | >$81B destruction | −$35B |

**Damodaran post-prospectus key changes from S-1 data:**

| Item | Pre-Prospectus | Post-Prospectus |
|------|----------------|-----------------|
| 2025 operating loss | ~$2B (est.) | $2.57B (S-1 reported) |
| Net cash position | Unknown | $1.9B net cash ($24.7B cash, $22.9B debt incl. leases) |
| Book value of equity | ~$20B (est.) | $41.3B (xAI acquisition) |
| Basic share count | ~2,467M | 12,535M reported |
| AI margin target | 45% | **25%** (reduced for competition) |
| AI revenue target | $80B | **$160B** (doubled for larger TAM) |
| Colossus lease | — | $1.25B/month to Anthropic |
| Discount rate | 8.00% | 8.37% (higher Treasury rates) |

**Sources:** [Morningstar initiation](https://global.morningstar.com/en-ca/stocks/spacex-what-investors-need-know-about-its-enormous-upcoming-ipo); [Damodaran Substack Apr 23 2026](https://aswathdamodaran.substack.com/p/to-trillions-and-beyond-a-spacex); [Damodaran Substack Jun 4 2026](https://aswathdamodaran.substack.com/p/revisiting-the-spacex-valuation-a); [CNBC Jun 3](https://www.cnbc.com/2026/06/03/morningstar-spacex-ipo-target-price-nasdaq.html); [Yahoo Finance Jun 2](https://finance.yahoo.com/markets/article/spacex-valued-at-just-780-billion-by-morningstar-less-than-half-its-ipo-target-174617034.html); [WSJ Jun 7 2026](https://www.wsj.com/business/what-the-dean-of-valuation-thinks-elon-musks-spacex-is-really-worth-bfe8061c)

### 4.2 xAI Bear Case: $6.35B Operating Loss Verified

**VERIFIED — PRIMARY SOURCE: SpaceX S-1 filed May 20, 2026.**

| Metric | 2024 | 2025 | Q1 2026 |
|--------|------|------|---------|
| xAI revenue | $2.62B | $3.20B | $818M |
| **xAI operating loss** | -$1.56B | **-$6.35B** | -$2.47B |
| xAI capex | — | $12.7B | $7.7B |
| SpaceX total capex | — | $20.74B | — |
| ◆ xAI share of SpaceX total capex | — | ~61% | — |

**Context:** Before the xAI merger (closed February 2026), SpaceX core business generated ~$8B in operating profit. After absorbing xAI, the consolidated entity became a ~$5B net-loss company. xAI revenue of $3.2B bundles X/Twitter advertising revenue with Grok AI product revenue; actual Grok-specific revenue is a smaller fraction. In March 2026, SpaceX took a $20B bridge loan and paid off xAI's $16B 2025 debt stack.

**Discrepancy note:** Morningstar S-1 analysis states **$6.35B**; TechCrunch and Yahoo Finance state **$6.4B** (rounded). Same S-1 source; consistent with $6,350M–$6,360M range. Both figures reported above.

**Sources:** [Morningstar "Financials Look Reckless"](https://global.morningstar.com/en-gb/stocks/financials-look-reckless-lifting-xais-hood-spacex-ipo); [TechCrunch May 20 2026](https://techcrunch.com/2026/05/20/xai-burned-6-4b-last-year-spacexs-ipo-filing-shows-why-the-spending-is-far-from-over/)

### 4.3 SpaceX Private Market Valuation History

| Date | Valuation | Price/Share | Event | Source |
|------|-----------|------------|-------|--------|
| July 2025 | ~$400B | ~$212 | Internal tender | [Fortune Dec 13 2025](https://fortune.com/2025/12/13/spacex-ipo-plan-2026-secondary-offering-insider-share-sale-800-billion-valuation/) |
| December 2025 | ~$800B | ~$421 (pre-split) | Secondary tender | [Reuters Dec 13 2025](https://www.reuters.com/business/spacex-sets-800-billion-valuation-bloomberg-news-reports-2025-12-13/) |
| February 2026 | ~$1.25T | — | xAI merger ($1T SpaceX + $250B xAI) | Multiple sources per S-1 |
| April 2026 | ~$1.5T | — | Last private reference pre-IPO | [Morningstar initiation](https://global.morningstar.com/en-ca/stocks/spacex-what-investors-need-know-about-its-enormous-upcoming-ipo) |
| May 26, 2026 | — | ~$125 | Nasdaq Private Market | [Nasdaq Private Market](https://www.nasdaqprivatemarket.com/company/spacex/) |
| June 11, 2026 | **~$1.77–1.80T** | **$135** | IPO pricing | [CNBC](https://www.cnbc.com/2026/06/03/morningstar-spacex-ipo-target-price-nasdaq.html) |

### 4.4 Anthropic: Funding Round Valuation Trajectory

| Round | Date | Amount | Valuation | Source |
|-------|------|--------|-----------|--------|
| Series E | Mar 3, 2025 | $3.5B | $61.5B | [Anthropic.com](https://www.anthropic.com/news/anthropic-raises-series-e-at-usd61-5b-post-money-valuation) |
| Series F | ~Sep 2025 | $13B | $183B | [NYT Sep 2 2025](https://www.nytimes.com/2025/09/02/technology/anthropic-funding-ai.html) |
| Series G | Feb 12, 2026 | $30B | $380B | [Anthropic.com](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) |
| Series H | May 28, 2026 | $65B | **$965B** | [Anthropic.com](https://www.anthropic.com/news/series-h) |

**FutureSearch IPO forecast:** Median post-IPO market cap $1.05T (p10: $750B; p90: $1.6T); $965B = ~21× current ARR; ~10× median 2027 ARR of $93B. ([FutureSearch May 28 2026](https://futuresearch.ai/anthropic-financial-forecast/))

**Margin warning (Shanaka Anslem Perera, Mar 12 2026):** Current 40% gross margin vs. ~77% needed; implied ARR multiple of 27× at Series G (Feb 2026 data) embeds "one of the most aggressive margin expansion assumptions in private tech." ([Substack Mar 12 2026](https://shanakaanslemperera.substack.com/p/the-growth-miracle-and-the-six-fractures))

### 4.5 OpenAI: Valuation Progression Through $852B

| Date | Valuation | Amount Raised | Key Details | Source |
|------|-----------|--------------|------------|--------|
| Oct 2024 | $157B | ~$6.6B | SoftBank, Thrive, Microsoft | [WSJ Oct 2 2024](https://www.wsj.com/tech/ai/openai-nearly-doubles-valuation-to-157-billion-in-funding-round-ee220607) |
| Mar 31, 2025 | $300B | $40B | SoftBank-led; conditional on PBC conversion | [OpenAI.com Mar 31 2025](https://openai.com/index/march-funding-updates/) |
| ~Aug 2025 | ~$500B | — | Secondary stock sales | [SaaStr Aug 20 2025](https://www.saastr.com/openai-crosses-12-billion-arr-the-3-year-sprint-that-redefined-whats-possible-in-scaling-software/) |
| Oct 28, 2025 | ~$500B | — | PBC conversion; Foundation 26% stake valued ~$130B | [OpenAI.com Oct 28 2025](https://openai.com/index/built-to-benefit-everyone/) |
| Mar 31, 2026 | **$852B** | **$122B** | Largest private fundraise in history; Amazon $50B, Nvidia $30B, SoftBank $30B | [OpenAI.com Mar 31 2026](https://openai.com/index/accelerating-the-next-phase-ai/); [Bloomberg Mar 31 2026](https://www.bloomberg.com/news/articles/2026-03-31/openai-valued-at-852-billion-after-completing-122-billion-round) |

**Note:** Anthropic's $965B valuation (May 2026) exceeds OpenAI's most recent $852B (March 2026). ([CNBC May 28 2026](https://www.cnbc.com/2026/05/28/anthropic-open-ai-startup-value.html))

### 4.6 Comparative Valuation Summary

| Company | Valuation | Date | Analyst/Basis | Revenue Basis | Multiple ◆ |
|---------|-----------|------|--------------|--------------|-----------|
| SpaceX | $780B (fair value) | Jun 5–8, 2026 | Morningstar DCF | $18.67B 2025 rev. | ~42× ◆ |
| SpaceX | $1.25–1.35T (equity) | Jun 4, 2026 | Damodaran SOTP | $18.67B 2025 rev. | ~67–72× ◆ |
| SpaceX | ~$1.77–1.80T (IPO) | Jun 11, 2026 | Market pricing | $18.67B 2025 rev. | ~94–96× ◆ |
| Anthropic | $965B | May 28, 2026 | Series H VC pricing | $47B ARR | ~21× ARR ◆ |
| Anthropic | $1.05T (median forecast) | May 28, 2026 | FutureSearch model | $47B ARR | ~22× ARR ◆ |
| OpenAI | $852B | Mar 31, 2026 | VC round pricing | >$25B ARR | ~34× ARR ◆ |
| OpenAI | $730B–$850B (IPO target) | Jun 8, 2026 | Pre-IPO consensus | $30B 2026 target | ~24–28× ◆ |

---

## §5 Comp Set Summary [WP-4]

**As-of date:** June 10, 2026. All returns ◆ computed from offer price (or Nasdaq reference price for Coinbase direct listing). Split-adjusted where noted.

### 5.1 Summary Return Table — All 17 Companies

| # | Company | Ticker | IPO Date | Offer Price | Day-1 Ret ◆ | +365d Ret ◆ | Return vs. Offer (Jun 10, 2026) ◆ | GAAP Profitable at IPO |
|---|---------|--------|----------|------------|------------|------------|----------------------------------|----------------------|
| 1 | Google | GOOGL | 2004-08-19 | $2.125 ◆ | +18.0% | +236.9% | **+16,671%** | YES |
| 2 | Facebook/Meta | META | 2012-05-18 | $38.00 | +0.6% | -35.9% | **+1,403%** | YES |
| 3 | Alibaba | BABA | 2014-09-19 | $68.00 | +38.1% | -13.3% | **+69.7%** | YES |
| 4 | Visa | V | 2008-03-19 | $11.00 ◆ | +28.4% | +45.5% | **+2,836%** | YES |
| 5 | Snap | SNAP | 2017-03-02 | $17.00 | +44.0% | -6.6% | **-68.4%** | NO |
| 6 | Lyft | LYFT | 2019-03-29 | $72.00 | +8.7% | -62.7% | **-81.4%** | NO |
| 7 | Uber | UBER | 2019-05-10 | $45.00 | -7.6% | -26.6% | **+52.5%** | NO |
| 8 | Snowflake | SNOW | 2020-09-16 | $120.00 | +111.6% | +152.0% | **+99.9%** | NO |
| 9 | Airbnb | ABNB | 2020-12-10 | $68.00 | +112.8% | +144.8% | **+89.9%** | NO |
| 10 | Coinbase † | COIN | 2021-04-14 | $250.00 | +31.3% | -54.9% | **-38.4%** | YES |
| 11 | Rivian | RIVN | 2021-11-10 | $78.00 | +29.1% | -58.9% | **-81.1%** | NO |
| 12 | Arm | ARM | 2023-09-14 | $51.00 | +24.7% | +180.4% | **+502.8%** | YES |
| 13 | Reddit | RDDT | 2024-03-21 | $34.00 | +48.4% | +208.5% | **+406.5%** | NO |
| 14 | CoreWeave | CRWV | 2025-03-28 | $40.00 | +0.0% | +93.7% | **+139.0%** | NO |
| 15 | Circle | CRCL | 2025-06-05 | $31.00 | +168.5% | +154.6% ‡ | **+154.6%** | YES |
| 16 | Figma | FIG | 2025-07-31 | $33.00 | +250.0% | N/A (<365d) | **-40.0%** | YES |
| 17 | Cerebras | CBRS | 2026-05-14 | ~$155.00 ~ | +100.7% | N/A (<365d) | **+53.1%** | NO |

> † Coinbase: direct listing; $250 is Nasdaq reference price, no new shares issued.
> ‡ Circle: IPO anniversary Jun 5, 2026 (5 days before snapshot). Jun 10 close used as proxy.
> Google offer price and day-1 close are split-adjusted (40:1 cumulative). Visa is split-adjusted (4:1).
> Cerebras offer price is ~ (estimate from final $150–$160 range; exact 424B4 pending).

**Primary sources — EDGAR 424B4 filings:**
- Google: https://www.sec.gov/Archives/edgar/data/1288776/000119312504143377/d424b4.htm
- Facebook: https://www.sec.gov/Archives/edgar/data/1326801/000119312512240111/d287954d424b4.htm
- Alibaba: https://www.sec.gov/Archives/edgar/data/1577552/000119312514347620/d709111d424b4.htm
- Visa: https://www.sec.gov/Archives/edgar/data/1403161/000119312508060989/d424b4.htm
- Snowflake: https://www.sec.gov/Archives/edgar/data/1640147/000162828020013667/snowflake424b4.htm
- Coinbase: https://www.sec.gov/Archives/edgar/data/1679788/000162828021003168/coinbaseglobalincs-1.htm
- CoreWeave: https://www.sec.gov/Archives/edgar/data/1769628/000119312525067651/d899798d424b4.htm

### 5.2 Key Observations

1. **Best performers (total return to Jun 10, 2026):** Google (+16,671%), Visa (+2,836%), Meta (+1,403%), Arm (+502.8%), Reddit (+406.5%). The first three demonstrate extraordinary multi-decade compounding; Arm and Reddit are the standout recent IPOs.

2. **Worst performers:** Lyft (−81.4%), Rivian (−81.1%), Snap (−68.4%), Coinbase (−38.4%), Figma (−40.0%). Lyft and Rivian both heavily loss-making at IPO and have never demonstrated durable profitability.

3. **Day-1 pop leaders:** Figma (+250%), Airbnb (+112.8%), Snowflake (+111.6%), Circle (+168.5%), Cerebras (+100.7%). Uber was the only company with a negative day-1 return (−7.6%).

4. **Profitable-at-IPO cohort pattern:** Google, Facebook (2012), Alibaba, Visa, Coinbase (2021), Arm (2023), Circle (2025), Figma (2025) — all 8 were GAAP profitable at IPO. Of the 8 profitable-at-IPO names, 6 showed positive long-run returns from offer price to Jun 10, 2026 (Alibaba +69.7% and Coinbase −38.4% are the exceptions). The 9 unprofitable-at-IPO names show far more dispersion: Snowflake (+99.9%) and Airbnb (+89.9%) are strong; Lyft, Rivian, and Snap are deep long-run losers.

5. **+365d deterioration pattern:** Facebook (−35.9%), Lyft (−62.7%), Coinbase (−54.9%), Rivian (−58.9%), and Snap (−6.6%) had negative 1-year returns. The 2021 vintage (Rivian, Coinbase) reflects peak-cycle pricing. Arm (+180.4%) and Reddit (+208.5%) are the standout strong 1-year performers among recent names.

6. **Structural note:** CoreWeave (priced $40 at the bottom of range, flat day-1) subsequently gained +139% to Jun 10, 2026 — illustrating that below-range pricings of AI infrastructure names can still generate strong returns for patient IPO buyers.

---

## §6 Ritter Dataset — Key Statistics [WP-1]

**Source:** Jay R. Ritter, University of Florida IPO Data
**Primary URL:** https://site.warrington.ufl.edu/ritter/ipo-data/
**Data last updated:** May 18, 2026 (IPO-Statistics.pdf); April 7, 2026 (long-run returns); April 14, 2026 (SPACs)

### 6.1 Bubble-Era Cohort (1999–2001) Summary

| Cohort | N_IPOs | Mean FDR | % Negative FDR | Avg 1yr Return | Avg 3yr BHR (from close) | 3yr Mkt-Adj | ◆ Implied 3yr BHR from Offer |
|--------|--------|----------|----------------|----------------|--------------------------|-------------|------------------------------|
| 1999 | 476 | **71.2%** | 11.8% | 22.1% | -47.6% | -32.5% | ◆ -10.3% |
| 2000 | 380 | **56.4%** | 11.8% | -52.9% | -60.1% | -30.9% | ◆ -37.6% |
| 2001 | 80 | 14.0% | 12.5% | -14.3% | +18.0% | +14.6% | ◆ +5.5% |
| **1999–2000 combined** | **856** | **64.6%** | **11.8%** | **-11.2%** | **-53.1%** | **-31.8%** | ◆ **-22.8%** |

**◆ Computation note for implied BHR from offer price:** BHR_offer = (1 + FDR) × (1 + BHR_close) − 1. E.g., 1999: (1.712) × (1 − 0.476) − 1 = −10.3%. These are cohort means, not % below offer price on individual IPOs.

**1999–2000 combined market-adjusted underperformance of −31.8% vs. CRSP is the single worst cohort sub-period in the 44-year dataset (1980–2025).**

### 6.2 % Below Offer Price Statistics

| Metric | Figure | Source / Notes |
|--------|--------|----------------|
| All IPOs 1975–2021 at +3 years, below offer price | **56.1%** ◆ | Ritter Table 16e; ◆ Computed: 3,215 + 1,939 = 5,154 / 9,195 |
| Large IPOs (Sales ≥ $100mm) at +3 years, below offer | **44.5%** ◆ | Ritter Table 16e Panel B; ◆ Computed |
| All IPOs 1975–2021 at +5 years, below offer price | **57.0%** ◆ | Ritter Table 16e Panel C; ◆ 3,646 + 1,598 = 5,244 / 9,195 |
| Large IPOs at +5 years, below offer | **~44%** ◆ | Ritter Table 16e Panel D (estimated from distribution) |

**Critical caveat:** Ritter does NOT publish year-by-year distributions. The 56.1%/57.0% figures are the **1975–2021 aggregate** only. For the 1999–2000 cohort specifically, the ◆computed implied 3-year BHR from offer of −10.3% (1999) and −37.6% (2000) suggests the fraction below offer was well above 56% for those years — but the exact year-specific percentage requires the IPOALL.xlsx file.

### 6.3 Overall IPO Statistics, 1980–2025

| Period | N_IPOs | Mean FDR (EW) | % Neg. FDR | Agg. Left on Table | Agg. Proceeds |
|--------|--------|---------------|------------|-------------------|---------------|
| 1980–1989 | 2,047 | 7.2% | 21.2% | — | — |
| 1990–1998 | 3,616 | 14.8% | 9.3% | — | — |
| **1999–2000** | **856** | **64.6%** | **11.8%** | **$66.79B** | **$129.47B** |
| 2001–2025 | 2,825 | 19.1% | 23.9% | — | — |
| **1980–2025 All** | **9,343** | **19.0%** | **16.5%** | **$250.1B** | **$1,200B** |

**Recent notable years:**
- 2025: 90 IPOs, 29.3% mean FDR, $13.11B left on table, $38.97B proceeds
- 2021 (peak): 311 IPOs, 32.1% mean FDR, $28.65B left on table, $119.36B proceeds
- 2008 (trough): 21 IPOs, 5.7% mean FDR, $5.63B left on table, 61.9% negative FDR (highest in dataset)

Source: [IPO-Statistics.pdf](https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf), Tables 1 and 4h (updated March 16, 2026 and December 30, 2025)

### 6.4 Long-Run Performance Summary

| Period | N_IPOs | Avg FDR | Avg 1yr | Avg 3yr BHR | 3yr Mkt-Adj | 3yr Style-Adj |
|--------|--------|---------|---------|-------------|-------------|---------------|
| 1980–1989 | 2,047 | 7.2% | 3.4% | 22.5% | -22.6% | +2.2% |
| 1990–1998 | 3,616 | 14.8% | 14.0% | 39.7% | -21.0% | -0.1% |
| **1999–2000** | **856** | **64.6%** | **-11.2%** | **-53.1%** | **-31.8%** | **-58.9%** |
| 2001–2010 | 1,010 | 11.6% | 6.7% | 17.1% | +2.2% | -7.6% |
| 2011–2024 | 1,724 | 23.0% | -1.7% | 9.1% | -24.7% | -16.4% |
| **1980–2024 All** | **9,253** | **18.9%** | **5.6%** | **19.1%** | **-20.5%** | **-8.9%** |

**Ritter's summary finding:** "IPOs have underperformed other firms of the same size by an average of 3.6%/yr during the five years after issuing, not including the first-day return." ([IPOs-long-run-returns-on-IPOs.pdf](https://site.warrington.ufl.edu/ritter/files/IPOs-long-run-returns-on-IPOs.pdf), Table 20)

**Large IPO exception:** IPOs with LTM sales ≥ $100mm essentially match style-matched benchmarks (+2.3% style-adjusted over 3 years). The underperformance is concentrated in sub-$100mm LTM sales companies (−17.9% style-adjusted 3yr).

Source: [IPOs-long-run-returns-on-IPOs.pdf](https://site.warrington.ufl.edu/ritter/files/IPOs-long-run-returns-on-IPOs.pdf), Table 16 (updated February 16, 2026)

### 6.5 SPAC Performance Statistics

**SPAC IPO volume:**
- 2020: 248 SPACs, $75.3B proceeds vs. 165 operating company IPOs, $61.9B — **first year SPACs exceeded operating companies in both count and proceeds**
- 2021 (peak): 613 SPACs, $144.5B proceeds vs. 311 operating company IPOs, $119.4B
- 2025: 144 SPACs (second highest ever), $26.9B; 90 operating company IPOs, $39.0B
- 1990–2025 total: 1,587 SPACs, $333.8B proceeds; mean first-day return = **1.2%** (near-zero by design; trust structure)

**deSPAC post-merger returns (2012–2022, N=451):**
- Average 1-year market-adjusted return: **−49.4%**
- Average 3-year market-adjusted return: **−74.7%**
- 2021 cohort (N=198): avg 1-year return −64.2%; avg 3-year return −73.0%
- 2023–2025 partial data: avg 1-year return −57.1% to −63.8%

**deSPAC redemption rates (trend):**
- 2021 Q1: 11.3% → 2021 Q4: 62% → 2022: ~85% → 2023: ~93–97% → 2024: ~92–98%
- Total 2017–2025: **68.4%** average redemption rate

Source: [IPOs-SPACs.pdf](https://site.warrington.ufl.edu/ritter/files/IPOs-SPACs.pdf), Tables 15b and 15c (updated April 14, 2026 and December 31, 2025); based on Gahng, Ritter & Zhang (2023, *Review of Financial Studies*)

### 6.6 Tech vs. Non-Tech Long-Run Returns

**Including bubble (1980–2024, from first close):**
- Tech (N=3,334): Mean FDR 31.2%; 3yr BHR +21.8%; 3yr Mkt-Adj **−12.7%**
- Non-Tech (N=5,919): Mean FDR 12.0%; 3yr BHR +17.6%; 3yr Mkt-Adj **−24.9%**

**Excluding bubble (1980–2023, from offer price, Table 16c):**
- Tech (N=2,689): Mean FDR 19.8%; 3yr BHR +73.3%; 3yr Style-Adj **+46.0%** (positive!)
- Non-Tech (N=5,636): Mean FDR 11.6%; 3yr BHR +30.3%; 3yr Style-Adj **−1.6%**
- Interpretation: Outside the bubble, tech IPOs substantially outperformed style-matched benchmarks. The bubble distortion (1999–2000 tech FDR ~78% average) reverses tech's market-adjusted 3-year return when included.

Source: [IPOs-Tech.pdf](https://site.warrington.ufl.edu/ritter/files/IPOs-Tech.pdf) and [IPOs-long-run-returns-on-IPOs.pdf](https://site.warrington.ufl.edu/ritter/files/IPOs-long-run-returns-on-IPOs.pdf), Tables 16c, 16d, 18b

### 6.7 Direct Download URLs for Excel Data Files

| File | Description | URL |
|------|-------------|-----|
| IPOALL.xlsx | Individual IPO data (full sample) | https://site.warrington.ufl.edu/ritter/files/IPOALL.xlsx |
| IPO-age.xlsx | Age of IPO firms | https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx |
| Underwriter-Rank.xls | Underwriter reputation rankings 1980–2025 | https://site.warrington.ufl.edu/ritter/files/Underwriter-Rank.xls |
| IPO-Allocation-2012-08-28.xls | Allocation data for 11 book-building IPOs 1997–2000 | https://site.warrington.ufl.edu/ritter/files/2016/01/IPO-Allocation-2012-08-28.xls |
| IPO-Analyst-Data-Online-1993-2009.xls | All-star analyst coverage and spinning data | https://site.warrington.ufl.edu/ritter/files/2015/06/IPO-Analyst-Data-Online-1993-2009-2011-04-01.xls |
| Fama-French-1973-2003.xls | Fama-French factor returns | https://site.warrington.ufl.edu/ritter/files/2016/01/Purged-and-unpurged-Fama-French-1973-2003.xls |

Additional: IPOScoop.com Excel file of U.S. IPOs 2000–present via "Track Record" at https://www.iposcoop.com

---

## §7 Open Items & Data Gaps

**As-of date:** June 10, 2026

### 7.1 Items Requiring Post-June 12 Data Collection

| Item | Why Needed | When Available |
|------|-----------|----------------|
| **SPCX Day-1 trading data** (open, close, high, low, volume) | Core dashboard metric | After June 12 market close |
| **SPCX 424B4 final prospectus** | Confirm final share count, exact terms, lock-up text | Filed on/after June 11; available on EDGAR after robots.txt check |
| **SPCX final retail allocation** | Actual allocation vs. 30% target | Post-IPO broker disclosures |
| **SPCX first quarterly earnings** | First lock-up unlock trigger (20% of holdings) | ~90 days after IPO |

### 7.2 S-1 Filings — Not Yet Public

| Company | Status | Expected Public S-1 | Impact |
|---------|--------|--------------------|----|
| **Anthropic** | Confidential SEC review | ~Summer–Fall 2026 | No audited financials; all revenue figures are secondary/press-sourced |
| **OpenAI** | Confidential SEC review | ~Fall 2026 | No audited financials; cumulative loss figures are internal projections |

Until public S-1s are filed: (a) all Anthropic/OpenAI financials carry secondary-source data quality ratings; (b) ARR figures may not match GAAP revenue in eventual audited statements; (c) governance structures (exact share classes, voting rights) are inferred from public statements, not prospectus text.

### 7.3 WP-6 — Blocked

WP-6 has not been started as of June 10, 2026. No findings to report.

### 7.4 Persistent Data Quality Caveats

| Item | Issue |
|------|-------|
| Ritter 1999–2000 year-specific "% below offer price" | Distribution table 16e is aggregate 1975–2021 only; year-specific figures require IPOALL.xlsx |
| OpenAI "$44B cumulative losses" vs. "$115B cash burn" | These are different metrics; "$44B" excludes stock comp and covers 2023–2028; "$115B" covers through 2029; "$143B FCF" includes capex — all three cited in media as "OpenAI's losses" |
| Anthropic ARR vs. GAAP revenue | $47B ARR is a forward run-rate, not TTM GAAP; open accounting question on gross vs. net for hyperscaler compute credits |
| xAI revenue "$3.2B" | Bundles X/Twitter advertising revenue with Grok-specific revenue; actual Grok-only revenue not separately disclosed |
| Cerebras CBRS offer price | Reported as ~$155 (midpoint of $150–$160 range); exact final price pending 424B4 |
| Figma current price (-40%) | Trading well below IPO price as of Jun 10, 2026 despite +250% day-1 pop; warrants monitoring |

### 7.5 Cadence Reminders (Per Research Plan)

- **Daily** (while SPCX active): Collect opening/closing price, volume, after-hours data for SPCX beginning June 12
- **On EDGAR publish:** Run EDGAR full-text search for 424B4 (SpaceX CIK 1181412), Anthropic S-1, OpenAI S-1 — alert when each goes public
- **+25–40 days post-June 12:** Collect sell-side initiation reports from Goldman Sachs, Morgan Stanley, and other underwriters as quiet period expires
- **On Anthropic/OpenAI S-1 public filing:** Re-run WP-3 with primary EDGAR sources to replace all secondary-source figures
- **Quarterly:** Update comp set prices and Ritter dataset as new PDFs publish

---

*Document compiled from WP1–WP5 source files. All ◆ marks indicate computed/derived figures; all ~ marks indicate estimates. Every claim carries at least one URL. As-of dates specific to each work package are noted in section headers. This is the primary reference document for the IPO dashboard project as of June 10, 2026.*
