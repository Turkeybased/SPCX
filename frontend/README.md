# IPO Context — SpaceX, Anthropic and OpenAI

A self-contained static front-end for the IPO Context Dashboard. It reads the
JSON in `data/` and renders the full dashboard: the price-vs-fair-value gauge,
thrust/drag ledger, mission-clock timeline, base-rate cards, the
"ignition ≠ orbit" scatter, the 45-year Ritter chart, and the two interactive
box-and-whisker plots (with per-company colour legend + click-to-isolate).

The top navigation now offers **Overview**, **Anthropic**, and **SpaceX**.
Direct links use `#overview`, `#anthropic`, and `#spacex`; historical charts
remain available beneath each view. The Anthropic view adds quarterly reported
revenue, GAAP/adjusted results, pending IPO terms, an illustrative valuation
slider and a source-linked filing timeline. The research was checked November 5,
2026 against the November 2 S-1/A. Private funding marks are not IPO prices.

The visual treatment adapts Magic UI's DotPattern and BorderBeam effects to the
existing runtime, with SVG and CSS replacing its Motion/Tailwind dependencies.
The header coverage illustration is conceptual; company positions encode no
financial measures. See `THIRD-PARTY-NOTICES.txt` for sources and the MIT license.
The valuation comparison bars update with the scenario slider. Reduced-motion
preferences disable decorative animation and transitions.

The intended decision is whether to participate at the available entry price,
wait for more evidence or different terms, or pass. The decision strip frames
those choices; it does not issue an automatic investment rating. The current
research supports valuation context and identifies missing information. It does
not yet model future returns, growth/margin requirements or portfolio sizing.

## Folder structure

```
frontend/
├── index.html      # the dashboard (open this)
├── support.js      # rendering runtime (loads React from unpkg)
├── ipo-watch.js    # overview, Anthropic financials and valuation scenarios
├── spacex-context.js # linked price/news chart, event windows and filters
├── visual-effects.js # adapted Magic UI effects and conceptual coverage art
├── dashboard.css   # responsive styles for the company views
└── data/
    ├── comps.json            # frozen historical seed (deals, comps, cohorts, analysis)
    ├── prices.json           # live layer — daily closes / returns
    ├── filing_status.json    # live layer — EDGAR S-1 watch
    ├── ritter_cohorts.json   # Ritter 1980–2025 first-day-return series
    ├── anthropic.json        # November 2026 primary-source research snapshot
    ├── spacex_market.json    # completed SPCX / SPY / QQQ price sessions
    └── spacex_events.json    # curated dated news with sources and timing
```

## Run it locally

`index.html` fetches the files in `data/`, so it must be served over **HTTP** —
opening it directly from the filesystem (`file://`) will fail on those fetches.

```bash
cd frontend
python3 -m http.server 8000
# then open http://localhost:8000/
```

Any static server works (`npx serve`, nginx, etc.).

## Deploy

It's a plain static site — host the contents of `frontend/` anywhere:

- **GitHub Pages**: commit this folder and point Pages at it (or move the three
  items to the repo root / `docs/`). No build step.
- **Vercel / Netlify / S3**: drop the folder in as static output.

## Updating the data (live layer)

`comps.json` is a frozen, source-cited seed — leave it alone except for verified
revisions. The live layer is `prices.json` and `filing_status.json`; regenerate
them with the repo's `etl/` scripts (e.g. `python etl/run_all.py`) and overwrite
the files here. The UI re-reads them on load and shows the refresh timestamp in
the masthead and each research view. JSON requests revalidate the browser cache.
`anthropic.json` contains manually reviewed research, not automatically extracted
financials; scheduled ETL copies it to the frontend without rewriting it.

### SpaceX price and news compendium

The SpaceX view now joins full daily OHLCV history with the curated
`spacex_events.json` archive. The November 5 refresh contains 102 completed
sessions and 19 sourced entries. Controls select the date range, price versus
relative-return view, SPY or QQQ benchmark, category, search and confirmed-only
coverage. Numbered markers and archive cards select the same event window.

Daily close-to-close windows run from the prior close through the first, third
or fifth mapped trading session. Verified after-close reports map to the next
available session. Unknown publication timing is flagged; the window may include
trading before the story. Future endpoints, missing benchmark data and missing
prior public closes remain unavailable. Differences from benchmarks are measured
in percentage points, not causal attribution or risk-adjusted abnormal returns.
The largest-session list includes days with no matching researched event.

`python etl/refresh_spacex_context.py` refreshes prices and mirrors the relevant
JSON to the frontend. It uses requests directly, validates SpaceX's issuer
identity (SPCX was formerly an ETF symbol), rejects splits for manual basis review,
and includes completed sessions with a 15-minute post-close buffer. The daily
pipeline runs it with `--no-sync` so frontend publication still waits for every
step to succeed. The news archive requires source review and is not a live feed.

June analyst marks, risk commentary and timeline are preserved under the
collapsed **Original IPO research** section. Other companies' price snapshots
retain their own dates. The independently refreshed SPCX price does not advance
the global timestamp for untouched historical comps.

The telemetry panel reads `prices.SPCX.series` (the daily `[{date, close}]`
array that `refresh_prices.py` emits for SPCX). Behaviour is automatic:

- **No series yet** (SPCX not in the feed) → an "Awaiting live price feed" panel
  that names the last refresh date and the command to run. This is the shipped
  state until SPCX actually trades and the ETL ingests it.
- **Series present** → a stat strip (last close, vs-$135, day-1 vs offer,
  return-to-date, as-of, session count) above a price line charted against the
  dashed **$135 escape line** — green above the offer, red below.

So to light it up: re-run the ETL so `prices.json` carries `SPCX.series`, and the
panel switches to the live chart on next load. No code change needed. (If
yfinance returns nothing for `SPCX`, the listing ticker may differ — point
`refresh_prices.py` at the real symbol.)

## Notes

- **Fonts**: Space Grotesk + JetBrains Mono load from Google Fonts (needs
  internet). To go fully offline, self-host the fonts and swap the `<link>` tags
  in `index.html`.
- `index.html` originated as a design export and now includes the company-view
  integration. Preserve that integration when incorporating a new design export.
- No backend, no auth, no tracking. Returns are vs. (split-adjusted) offer price;
  mega-IPO returns are first-close-based. Not investment advice.
