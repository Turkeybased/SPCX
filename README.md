# IPO Context Dashboard

Personal dashboard putting the SpaceX (SPCX), Anthropic, and OpenAI IPOs in
historical context. Python ETL → versioned `data/*.json` → static single-page
dashboard (`frontend/`, deployed by Vercel). No backend, no API keys.

## Status

**November 5 update:** the served dashboard now has **Overview**, **Anthropic**
and **SpaceX** views with shared historical charts. Anthropic research uses the
November 2 public S-1/A (CIK 2130357): quarterly reported financials, pending
offering terms, filing milestones and an illustrative valuation slider. Its
last private funding valuation is labeled separately from IPO pricing. See
`data/anthropic.json` for primary-source links and dates. SpaceX prices have been
refreshed through November 5 (102 completed sessions) with SPY/QQQ context and a
19-item source-linked event archive. Select a numbered marker to inspect returns,
volume and market comparisons around publication; use filters to explore deals,
reported acquisition talks, war/policy, earnings, launches and capital events.
The archive is curated and explicitly separates evidence from interpretation.

The following describes the original June research seed:

**Seeded and live.** `data/comps.json` is populated from the v2 research drop
(`docs/research/`, 2026-06-10): 3 deals, 10 mega-IPOs, 17 tech comps
(offer-price return basis, EDGAR 424B4-derived), Ritter cohort statistics,
and a sourced analysis layer (red flags / counterpoints / timeline / base
rates) rendered by the question-first dashboard. Conflicts #2 (Musk voting =
82.4%), #3 (Dec 2025 tender = $421/$800B), and #6 (OpenAI round close) are
resolved in v2; five WP-4 `+365d` figures are quarantined pending re-research
(see `docs/DATA.md`). The remaining gap is live SPCX trading data, which the
daily ETL picks up automatically once SPCX trades (expected 2026-06-12).

Full provenance map and integrity rules: [docs/DATA.md](docs/DATA.md).

## Layout

- `data/comps.json` — hand-curated historical seed. Record schema:
  `{ ...metric_fields, source_url, conflict_note (nullable), as_of }`.
  ETL only ever writes the fields listed in `_meta.etl_writable_fields`
  (computed returns, `verified`, last price); seed figures are never modified.
- `data/prices.json` — yfinance daily closes + computed day-1 / +365d /
  to-date returns per ticker. SPCX gets a full daily series for the R5 chart.
- `data/filing_status.json` — EDGAR watch output (public S-1s for
  Anthropic/OpenAI via full-text search; SpaceX S-1/424B4 via CIK 1181412).
- `etl/refresh_prices.py`, `etl/edgar_watch.py`, `etl/run_all.py`
- `site/index.html` — views R1–R6, conflict ⚠ tooltips, source links,
  staleness timestamp (legacy version).
- `frontend/index.html`, `ipo-watch.js`, `dashboard.css` — the served dashboard;
  `frontend/data/` mirrors the canonical JSON from `data/`.
- `data/anthropic.json` — reviewed quarterly results and offering milestones;
  research is manually refreshed, while the filing watcher runs separately.
- `data/spacex_market.json` — full completed-session SPCX OHLCV, plus SPY/QQQ.
- `data/spacex_events.json` — curated news and sources, public dates, timing
  confidence and potential business channels. Daily price refreshes do not add news.

## Run

```powershell
python -m pip install yfinance requests
python etl/run_all.py
# To refresh only SpaceX and its benchmarks, without re-pricing the old comps:
python etl/refresh_spacex_context.py
# serve repo root so the site can fetch ../data/*.json:
python -m http.server 8347
# open http://localhost:8347/frontend/
```

## Daily refresh

Windows Task Scheduler (run once, as your user):

```powershell
schtasks /Create /TN "IPO Dashboard Refresh" /SC DAILY /ST 17:30 `
  /TR "python C:\Users\solom\projects\ipo-context-dashboard\etl\run_all.py"
```

Or GitHub Actions: see `.github/workflows/refresh.yml`.

Run filing-watcher regression checks with `python -m unittest discover -s tests -v`.
Event-window and archive checks: `node tests/test_spacex_events.cjs`.

## Guardrails

- EDGAR: max 10 req/s, User-Agent `solo solomon.foshko@gmail.com`. We sleep
  between requests.
- No fabricated figures; conflicting sources are shown via `conflict_note`,
  never averaged.
- `refresh_prices.py` aborts the comps write-back if a computed figure
  diverges from a non-null seed figure by more than 20% (data bug, not news).
- Stop and report if yfinance has no SPCX data after 2026-06-12 or EDGAR
  errors repeatedly.
- No trading or brokerage integration.
