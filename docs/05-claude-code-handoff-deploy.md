# Claude Code Handoff — Publish dashboard to GitHub + Vercel

Paste everything below into Claude Code, run from `C:\Users\solom\Projects\ipo-context-dashboard`.

---

## Context

- Static dashboard lives in `frontend/` (index.html + support.js + data/*.json, all relative paths, no build step).
- Target repo exists: https://github.com/Turkeybased/SPCX — public, branch `main`, currently contains only `LICENSE` (HEAD `4644b09`).
- `vercel.json` already at project root with `"outputDirectory": "frontend"` so Vercel serves the dashboard with zero config.
- Cowork's GitHub connector is read-only (403 on writes), so the push happens here with my own credentials.
- **Why an existing deploy looks stale:** a Vercel deployment freezes whatever `frontend/data/*.json` existed at deploy time. If SPCX was deployed before it began trading (or before the placeholder-row fix), the live deploy shows "Awaiting close price". The page does NOT fetch new prices on reload — only a redeploy with fresh data updates it. This handoff redeploys with current data and (step 7) wires the daily auto-refresh so it stays current at each market close.
- **Model is daily-at-close, not real-time.** The telemetry section is labeled "DAILY TELEMETRY · AT CLOSE". yfinance gives delayed/EOD quotes; the GitHub Action refreshes once per day. That is by design.

## Task

0. Sanity-check the ETL runs clean on this machine (it was edited from a sandbox; line endings may need normalizing): `pip install yfinance` if needed, then `python etl/refresh_prices.py`. Expect "24 tickers, 0 failed" and `data/prices.json` containing an SPCX `series` whose FIRST entry is dated `2026-06-12` (not 06-11 — that placeholder row is a bug the script now filters). If it errors or the series starts 06-11, stop and report.
   Then copy refreshed data into the served folder: `copy data\*.json frontend\data\` (Windows) before committing.
1. `git status` — check if this folder is already a git repo. If not: `git init -b main`.
2. Ensure `.gitignore` excludes `session-reports/` and `.claude/`. Add those lines if missing.
3. Stage and commit everything else (frontend/, data/, etl/, docs/, vercel.json, README.md, .github/workflows/refresh.yml). Message: `Add IPO context dashboard: frontend, data, ETL, docs`.
4. `git remote add origin https://github.com/Turkeybased/SPCX.git` (or set-url if origin exists).
5. `git pull origin main --rebase --allow-unrelated-histories` (the repo has a LICENSE commit we want to keep), then `git push -u origin main`.
6. Deploy: `npx vercel@latest deploy --prod` from project root. Log in as prompted (GitHub auth is fine). Accept defaults; project name `spcx-dashboard` or similar.
7. After deploy, link the GitHub repo in Vercel so each data commit auto-redeploys: `npx vercel git connect` (or Vercel dashboard → Project → Settings → Git). THIS IS WHAT KEEPS THE DEPLOYED PRICE CURRENT — without it, the daily Action commits new data to GitHub but Vercel never rebuilds, so the live site stays frozen.
8. Confirm the daily refresh works end-to-end: check `.github/workflows/refresh.yml` has a `schedule:` cron and that it commits changed `data/*.json` back to the repo (it should also `copy data/*.json frontend/data/`). Trigger it once manually (GitHub → Actions → Run workflow) and confirm it produces a commit and a Vercel redeploy. If the Action lacks permission to push commits, set repo Settings → Actions → Workflow permissions to "Read and write".

## Expected output back to me

- Paste `git log --oneline` and `git remote -v`.
- The production URL Vercel prints (https://….vercel.app).
- Whether `vercel git connect` succeeded (yes/no + any message).
- Confirm `.github/workflows/refresh.yml` made it to GitHub (it will, with local git — the connector limitation doesn't apply).
- Open the deployed URL and confirm the DAILY TELEMETRY · AT CLOSE section (now positioned directly under Q1 · ASCENT) shows an SPCX price (not "Awaiting close price") — that's the proof the new frontend + fresh data both shipped.
- Confirm the manual Action run produced a new commit and Vercel redeployed (paste the redeploy URL or note "git connect not done").

## Constraints

- Don't force-push; if `main` diverges beyond the LICENSE commit, stop and report.
- Don't commit `session-reports/` or `.claude/`.
- If Vercel CLI asks "which scope/team", pick the personal account.
- If the GitHub Action `refresh.yml` errors on its first scheduled run, just report it — don't modify the workflow in this session.
- Stop and report if: push is rejected for auth reasons (then we re-check GitHub credentials), or the deployed URL serves 404 (then check vercel.json output directory took effect).
