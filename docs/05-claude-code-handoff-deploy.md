# Claude Code Handoff — Publish dashboard to GitHub + Vercel

Paste everything below into Claude Code, run from `C:\Users\solom\Projects\ipo-context-dashboard`.

---

## Context

- Static dashboard lives in `frontend/` (index.html + support.js + data/*.json, all relative paths, no build step).
- Target repo exists: https://github.com/Turkeybased/SPCX — public, branch `main`, currently contains only `LICENSE` (HEAD `4644b09`).
- `vercel.json` already at project root with `"outputDirectory": "frontend"` so Vercel serves the dashboard with zero config.
- Cowork's GitHub connector is read-only (403 on writes), so the push happens here with my own credentials.

## Task

0. Sanity-check the ETL runs clean on this machine (it was edited from a sandbox; line endings may need normalizing): `pip install yfinance` if needed, then `python etl/refresh_prices.py`. Expect "24 tickers, 0 failed" and `data/prices.json` containing an SPCX `series` whose FIRST entry is dated `2026-06-12` (not 06-11 — that placeholder row is a bug the script now filters). If it errors or the series starts 06-11, stop and report.
   Then copy refreshed data into the served folder: `copy data\*.json frontend\data\` (Windows) before committing.
1. `git status` — check if this folder is already a git repo. If not: `git init -b main`.
2. Ensure `.gitignore` excludes `session-reports/` and `.claude/`. Add those lines if missing.
3. Stage and commit everything else (frontend/, data/, etl/, docs/, vercel.json, README.md, .github/workflows/refresh.yml). Message: `Add IPO context dashboard: frontend, data, ETL, docs`.
4. `git remote add origin https://github.com/Turkeybased/SPCX.git` (or set-url if origin exists).
5. `git pull origin main --rebase --allow-unrelated-histories` (the repo has a LICENSE commit we want to keep), then `git push -u origin main`.
6. Deploy: `npx vercel@latest deploy --prod` from project root. Log in as prompted (GitHub auth is fine). Accept defaults; project name `spcx-dashboard` or similar.
7. After deploy, also link the GitHub repo in Vercel for auto-redeploys: `npx vercel git connect` (or note that I can do it in the Vercel dashboard → Project → Settings → Git).

## Expected output back to me

- Paste `git log --oneline` and `git remote -v`.
- The production URL Vercel prints (https://….vercel.app).
- Whether `vercel git connect` succeeded (yes/no + any message).
- Confirm `.github/workflows/refresh.yml` made it to GitHub (it will, with local git — the connector limitation doesn't apply).
- Open the deployed URL and confirm the LIVE · TELEMETRY section shows an SPCX price (not "Awaiting live price feed") — that's the proof the new frontend + fresh data both shipped.

## Constraints

- Don't force-push; if `main` diverges beyond the LICENSE commit, stop and report.
- Don't commit `session-reports/` or `.claude/`.
- If Vercel CLI asks "which scope/team", pick the personal account.
- If the GitHub Action `refresh.yml` errors on its first scheduled run, just report it — don't modify the workflow in this session.
- Stop and report if: push is rejected for auth reasons (then we re-check GitHub credentials), or the deployed URL serves 404 (then check vercel.json output directory took effect).
