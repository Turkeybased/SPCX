# Claude Code Handoff — IPO Context Dashboard (Phase 1 + 2)

Paste everything below into Claude Code. Have `01-ipo-dashboard-spec.md` and `03-research-findings.md` in the project folder first.

---

## Context

- We spec'd a personal dashboard putting the SpaceX (SPCX — prices Jun 11 2026, trades Jun 12, $135/shr target, ~$1.75T), Anthropic (confidential S-1 Jun 1), and OpenAI (confidential S-1 Jun 8) IPOs in historical context. Full spec: `01-ipo-dashboard-spec.md`. Verified dataset: `03-research-findings.md`.
- Architecture decided: Python ETL → versioned `data/*.json` → static single-page dashboard (Chart.js or Recharts), no backend. Historical seed data is frozen/hand-curated; ETL refreshes only live fields (SPCX price, EDGAR filing status).
- The "~1yr return" figures in the findings doc are flagged UNVERIFIED — compute real ones from yfinance in step 3.

## Task

1. Scaffold repo `ipo-context-dashboard/`: `data/`, `etl/`, `site/`, `README.md`, `.gitignore`, git init, initial commit.
2. Create `data/comps.json` by transcribing the three tables (deals, mega-IPOs, tech comps, cohorts) from `03-research-findings.md`. Schema per record: `{metric_fields..., source_url, conflict_note (nullable), as_of}`. Include all 9 conflict notes from §5.
3. `etl/refresh_prices.py`: yfinance daily closes for all listed comp tickers + SPCX (handle "not yet trading" → null). Compute day-1 return, +365d return, return-to-date per ticker; write `data/prices.json`. Overwrite the unverified 1-yr figures in comps with computed values, marking them `verified: true`.
4. `etl/edgar_watch.py`: query EDGAR full-text search (https://efts.sec.gov/LATEST/search-index?q=...) for public S-1s from Anthropic and OpenAI (and SpaceX 424B4, CIK 1181412). Set User-Agent header `solo solomon.foshko@gmail.com`. Write `data/filing_status.json`.
5. `site/index.html` (single file, CDN deps OK): four views per spec R1–R4 — deal cards, sortable mega-IPO table with SPCX overlay row, day-1-pop vs 1-yr-return scatter (point size = raise, hover detail), cohort stat panel. Plus R5 SPCX price-vs-$135 line and R6 filing-status chips. Render ⚠ tooltip wherever `conflict_note` is set; every figure links `source_url`. Staleness timestamp in header.
6. `etl/run_all.py` + a Windows Task Scheduler command (or GitHub Action YAML) for daily refresh.
7. Run the ETL once, open the site, verify it renders with real data.

## Expected output back to me

- `git status --short` and `git log --oneline` (paste).
- Paste of `data/filing_status.json` and the first 30 lines of `data/prices.json`.
- Screenshot or description of the rendered dashboard (all 6 views present, conflicts flagged, timestamp showing).
- List of any tickers yfinance failed on and any comps figures that materially changed after verification (these matter — they correct the findings doc).

## Constraints

- Free data sources only; no API keys beyond optional Finnhub free tier. Respect EDGAR rate limits (10 req/s max, proper User-Agent).
- Don't fabricate any historical figure. If a value can't be computed/verified, render "n/a — see findings doc" rather than a guess.
- Don't average conflicting figures; show the conflict note.
- Never silently modify `data/comps.json` historical seed fields from ETL — only `verified` return fields and live fields.
- No trading/brokerage integration of any kind.
- Stop and report if: yfinance has no SPCX data after June 12, EDGAR returns errors repeatedly, or any comp figure differs from the seed by >20% (likely a data bug, not news).
