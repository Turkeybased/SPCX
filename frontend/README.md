# SPCX in Context — Launch Trajectory dashboard (frontend)

A self-contained static front-end for the IPO Context Dashboard. It reads the
JSON in `data/` and renders the full dashboard: the price-vs-fair-value gauge,
thrust/drag ledger, mission-clock timeline, base-rate cards, the
"ignition ≠ orbit" scatter, the 45-year Ritter chart, and the two interactive
box-and-whisker plots (with per-company colour legend + click-to-isolate).

## Folder structure

```
frontend/
├── index.html      # the dashboard (open this)
├── support.js      # rendering runtime (bundled; includes React — no CDN needed)
└── data/
    ├── comps.json            # frozen historical seed (deals, comps, cohorts, analysis)
    ├── prices.json           # live layer — daily closes / returns
    ├── filing_status.json    # live layer — EDGAR S-1 watch
    └── ritter_cohorts.json   # Ritter 1980–2025 first-day-return series
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
the masthead ("TELEMETRY").

### The LIVE · TELEMETRY section (SPCX price line)

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
- `index.html` is an exported snapshot from the design project. If you re-export
  a new version, replace `index.html` (keep `support.js` and `data/` as they are).
- No backend, no auth, no tracking. Returns are vs. (split-adjusted) offer price;
  mega-IPO returns are first-close-based. Not investment advice.
