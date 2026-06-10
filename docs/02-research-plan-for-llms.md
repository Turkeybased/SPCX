# Research & Discovery Plan — IPO Context (for use with other LLMs)

**Purpose:** divide remaining research into self-contained work packages you can hand to any capable LLM (Claude, GPT, Gemini). Each package has a prompt, expected output, and verification rules. Initial discovery is already done (see `03-research-findings.md`) — these packages fill gaps and keep data current.

## Ground rules (paste into every LLM session)

1. Two independent sources per figure; if they disagree, report both — never average.
2. Prefer primary sources: SEC EDGAR filings > exchange/company PR > financial press > aggregator blogs.
3. Every claim gets a URL. Output tables as markdown with a `source` column.
4. Mark estimates with `~` and computed/derived figures with `◆`.
5. As-of date on everything; prices move daily.

---

## WP-1: Ritter dataset extraction (highest value, do first)

**Why:** the academic gold standard for cohort base rates; fills the flagged gap ("% of 1999–2000 IPOs below offer by 2002" has no verified number yet).

**Prompt:**
> Download Jay Ritter's IPO data files from https://site.warrington.ufl.edu/ritter/ipo-data/ (IPO-Statistics.pdf, IPOs-long-run-returns-on-IPOs.pdf, IPOs-SPACs.pdf, and the underlying Excel files where available). Extract: (a) IPO counts and mean first-day returns by year 1980–2025; (b) 3-year buy-and-hold returns vs market for IPO cohorts, especially 1999–2001; (c) tech vs non-tech splits; (d) SPAC issuance and return stats. Output as CSV-ready markdown tables. Compute, if the data allows: % of 1999–2000 IPOs trading below offer price at +3 years. Show your method.

**Output:** `data/ritter_cohorts.csv` candidate + method notes.
**Verify:** spot-check 3 years against the PDF directly.

## WP-2: SpaceX final-pricing update (run June 12, then weekly)

**Prompt:**
> SpaceX (SPCX) priced its IPO on June 11, 2026. Find: final offer price and share count, total raised incl. greenshoe, final valuation, day-1 open/close, retail vs institutional allocation, and the final prospectus (424B4) on EDGAR. Resolve from the 424B4: Musk's exact post-IPO voting power (sources previously conflicted: 79% vs >82%) and the December 2025 tender valuation. Sources: SEC EDGAR (CIK 1181412), CNBC, Reuters.

**Output:** updated deal card fields + resolved conflicts #2 and #3 from findings doc §5.

## WP-3: Anthropic / OpenAI S-1 watch (recurring until public)

**Prompt:**
> Check SEC EDGAR full-text search (https://efts.sec.gov/LATEST/search-index?q=%22Anthropic%22&dateRange=custom...) and news for: (a) public S-1 flips by Anthropic or OpenAI; (b) updated revenue/loss figures; (c) announced ranges, exchanges, tickers, lead underwriters; (d) withdrawal or delay signals. If an S-1 is public, extract: revenue by year, net loss, cash position, compute spend commitments, governance structure (Anthropic LTBT; OpenAI nonprofit/PBC structure), top 5 risk factors, and dual-class/voting details.

**Output:** status + structured financials when available. This is the single most important future event for the dashboard — primary financials replace all current estimates.

## WP-4: Comp-set hardening (one-time)

**Prompt:**
> For these 17 IPOs [Google, Facebook, Alibaba, Snap, Lyft, Uber, Snowflake, Airbnb, Coinbase, Rivian, Arm, Reddit, CoreWeave, Circle, Figma, Cerebras, Visa], verify from prospectuses (424B4 on EDGAR) and exchange data: offer price, shares offered, raise, implied valuation, TTM revenue at IPO, GAAP profitability at IPO, day-1 close. Then pull daily closes (Yahoo Finance/Macrotrends) to compute: return at +365 calendar days and return through [today]. Note: the existing dataset's 1-yr-out figures are UNVERIFIED approximations — replace them all. Flag any number that differs from the attached findings doc.

**Output:** `data/comps.json` candidate — this becomes the dashboard's frozen seed data.

## WP-5: Valuation anchors & bear cases (one-time, refresh monthly)

**Prompt:**
> Collect published third-party valuation work on SpaceX, Anthropic, and OpenAI: Morningstar (SpaceX FV $780B), Damodaran (~$1.3T), plus any sell-side initiation reports post-IPO, and serious bear cases (e.g., xAI's $6.35B operating loss inside SpaceX; OpenAI's projected cumulative losses to 2029; Anthropic's claim of near-term quarterly profit). For each: author, date, method (DCF/multiples/SOTP), headline number, key assumptions. Do not produce your own price target.

**Output:** "third-party views" panel data.

## WP-6: intelligence-hatchery repo review (blocked)

Repo `github.com/mikeruthruff/intelligence-hatchery` is 404 to the connected GitHub account and the username doesn't resolve in search — private or mistyped. Once accessible:

**Prompt:**
> Review this repo's agents and agent skills for financial institutions. Inventory: what agents exist, what data sources/APIs they wrap, what skills could serve (a) the ETL layer (prices, filings), (b) the research layer (S-1 analysis), or (c) the dashboard itself. Map each useful component to a requirement in the spec (R1–R7) and state what it replaces or augments. Flag licensing and any credentials it expects.

## Cadence summary

| Package | When |
|---|---|
| WP-1 Ritter | Once, now |
| WP-2 SPCX pricing | June 12, then weekly |
| WP-3 S-1 watch | Daily-ish until both public, then deep-read once |
| WP-4 Comp hardening | Once, before build |
| WP-5 Valuation anchors | Once, refresh monthly |
| WP-6 Repo review | When access resolved |
