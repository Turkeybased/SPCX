# IPO Context Dashboard

Personal dashboard putting the SpaceX (SPCX), Anthropic, and OpenAI IPOs in
historical context. Python ETL → versioned `data/*.json` → static single-page
dashboard (`site/index.html`, Chart.js via CDN). No backend, no API keys.

## Status

⚠ **Historical seed incomplete.** `data/comps.json` must be populated from
`03-research-findings.md` (the four tables — deals, mega-IPOs, tech comps,
cohorts — plus the 9 conflict notes from §5). That file was not present when
this repo was scaffolded, and per project constraints no historical figure is
fabricated. The dashboard renders "n/a — see findings doc" wherever data is
missing. Drop the findings doc into the repo root and transcribe the tables
into `comps.json` (schema below) to light up views R2–R4.

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
  staleness timestamp.

## Run

```powershell
python -m pip install yfinance requests
python etl/run_all.py
# serve repo root so the site can fetch ../data/*.json:
python -m http.server 8347
# open http://localhost:8347/site/
```

## Daily refresh

Windows Task Scheduler (run once, as your user):

```powershell
schtasks /Create /TN "IPO Dashboard Refresh" /SC DAILY /ST 17:30 `
  /TR "python C:\Users\solom\projects\ipo-context-dashboard\etl\run_all.py"
```

Or GitHub Actions: see `.github/workflows/refresh.yml`.

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
