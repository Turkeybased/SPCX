"""Refresh daily closes and computed returns for all listed comp tickers + SPCX.

Reads tickers from data/comps.json (mega_ipos, tech_comps, deals), pulls daily
closes from yfinance, computes day-1 return, +365d return, and return-to-date
per ticker, and writes data/prices.json.

It then overwrites ONLY the ETL-writable return fields in comps.json
(day1_return_pct, one_yr_return_pct, return_to_date_pct, verified, last_price,
last_price_as_of). Historical seed fields are never touched. If a computed
figure differs from a non-null seed figure by >20%, the script aborts with a
report instead of writing (likely a data bug, not news).
"""

import json
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
COMPS_PATH = ROOT / "data" / "comps.json"
PRICES_PATH = ROOT / "data" / "prices.json"

ETL_WRITABLE = {"day1_return_pct", "one_yr_return_pct", "return_to_date_pct",
                "verified", "last_price", "last_price_as_of"}
DIVERGENCE_LIMIT = 0.20  # abort if computed differs from seed by >20%

RETRY_ATTEMPTS = 3
RETRY_BACKOFF = (1, 2, 4)  # seconds before each retry; Yahoo is flakiest for
                          # newly-listed names (SPCX first trade 2026-06-12)


def history_with_retry(ticker, **kwargs):
    """yf.Ticker(ticker).history(**kwargs) with up to RETRY_ATTEMPTS tries and
    exponential backoff. Absorbs transient yfinance/Yahoo blips; the final
    failure propagates to the caller's per-ticker handling."""
    last_exc = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            return yf.Ticker(ticker).history(**kwargs)
        except Exception as exc:
            last_exc = exc
            if attempt < RETRY_ATTEMPTS - 1:
                wait = RETRY_BACKOFF[attempt]
                print(f"  {ticker}: history() failed ({exc}); retrying in {wait}s "
                      f"({attempt + 1}/{RETRY_ATTEMPTS})", file=sys.stderr)
                time.sleep(wait)
    raise last_exc


def write_json_atomic(path, obj):
    """Write JSON via temp file + atomic replace so an interrupted run can
    never leave a truncated file behind (this happened 2026-06-12)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    tmp.replace(path)


def pct(a, b):
    if a is None or b is None or a == 0:
        return None
    return round((b - a) / a * 100, 2)


def compute_for_ticker(ticker, ipo_date_str):
    """Return dict of closes + returns, or None if yfinance has no data."""
    hist = history_with_retry(ticker, period="max", interval="1d", auto_adjust=False)
    if hist is None or hist.empty:
        return None
    # Drop leading zero-volume placeholder rows (e.g. SPCX shows a 2026-06-11
    # "pricing day" row at exactly $135 with no volume; first real session is
    # 06-12). Only leading rows are dropped so genuine zero-volume days later
    # in a series are untouched.
    if "Volume" in hist.columns:
        nonzero = hist["Volume"].fillna(0) > 0
        if nonzero.any():
            hist = hist.loc[nonzero.idxmax():]
    closes = hist["Close"].dropna()
    if closes.empty:
        return None

    first_close = float(closes.iloc[0])
    first_date = closes.index[0].date()
    last_close = float(closes.iloc[-1])
    last_date = closes.index[-1].date()

    # Day-1 return needs the offer price; without it fall back to null unless
    # an ipo open is available the same day.
    day1 = None
    opens = hist["Open"].dropna()
    if not opens.empty:
        first_open = float(opens.iloc[0])
        day1 = pct(first_open, first_close)

    # close nearest to first trading day + 365d (only if a full year elapsed)
    close_plus_365 = None
    one_yr = None
    target = first_date + timedelta(days=365)
    if last_date >= target:
        after = closes[closes.index.date >= target]
        if not after.empty:
            close_plus_365 = float(after.iloc[0])
            one_yr = pct(first_close, close_plus_365)

    to_date = pct(first_close, last_close)

    return {
        "ticker": ticker,
        "first_trade_date": first_date.isoformat(),
        "first_open": round(float(opens.iloc[0]), 4) if not opens.empty else None,
        "first_close": round(first_close, 4),
        "close_plus_365": round(close_plus_365, 4) if close_plus_365 else None,
        "last_close": round(last_close, 4),
        "last_close_date": last_date.isoformat(),
        "day1_return_pct": day1,
        "one_yr_return_pct": one_yr,
        "return_to_date_pct": to_date,
    }


def main():
    comps = json.loads(COMPS_PATH.read_text(encoding="utf-8"))

    records = []
    for table in ("deals", "mega_ipos", "tech_comps"):
        records.extend(comps.get(table, []))

    tickers = sorted({r["ticker"] for r in records if r.get("ticker")})
    if "SPCX" not in tickers:
        tickers.append("SPCX")

    prices = {}
    failed = []
    for tk in tickers:
        try:
            result = compute_for_ticker(tk, None)
        except Exception as exc:  # network / delisted / not yet trading
            result = None
            print(f"  {tk}: error: {exc}", file=sys.stderr)
        if result is None:
            prices[tk] = {"ticker": tk, "status": "no data (not yet trading or unknown ticker)",
                          "day1_return_pct": None, "one_yr_return_pct": None,
                          "return_to_date_pct": None, "last_close": None}
            failed.append(tk)
        else:
            result["status"] = "ok"
            if tk == "SPCX":
                # full daily series for the R5 price-vs-$135 line. Wrapped in
                # its own try/except: a yfinance error fetching the series must
                # NOT crash the whole refresh — we just skip the series and keep
                # the (already-computed) returns for SPCX.
                try:
                    full = history_with_retry(tk, period="max", interval="1d",
                                              auto_adjust=False)
                    # same leading zero-volume placeholder trim as compute_for_ticker
                    if "Volume" in full.columns:
                        nonzero = full["Volume"].fillna(0) > 0
                        if nonzero.any():
                            full = full.loc[nonzero.idxmax():]
                    hist = full["Close"].dropna()
                    result["series"] = [
                        {"date": d.date().isoformat(), "close": round(float(c), 4)}
                        for d, c in hist.items()
                    ]
                except Exception as exc:
                    print(f"  {tk}: series fetch failed, skipping series: {exc}",
                          file=sys.stderr)
            prices[tk] = result

    # SPCX not trading until 2026-06-12 — null is expected before then.
    if "SPCX" in failed and date.today() > date(2026, 6, 12):
        print("STOP: yfinance has no SPCX data after June 12 — report to user.",
              file=sys.stderr)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "yfinance (Yahoo Finance) daily closes",
        "tickers_requested": tickers,
        "tickers_failed": failed,
        "prices": prices,
    }
    write_json_atomic(PRICES_PATH, out)
    print(f"wrote {PRICES_PATH} ({len(tickers)} tickers, {len(failed)} failed)")

    # --- write back ONLY verified return fields into comps.json ---
    divergences = []
    changed = []
    for table in ("deals", "mega_ipos", "tech_comps"):
        for rec in comps.get(table, []):
            tk = rec.get("ticker")
            if not tk or tk not in prices or prices[tk].get("status") != "ok":
                continue
            p = prices[tk]
            # offer-based returns when the seed carries an offer price (the
            # WP-4 convention: split-adjusted offer; yfinance is split-adjusted
            # too, so the bases match). Fall back to first-close basis.
            offer = rec.get("offer_price_usd")
            if offer:
                comp_1yr = pct(offer, p["close_plus_365"]) if p.get("close_plus_365") else None
                comp_to_date = pct(offer, p["last_close"])
                comp_day1 = pct(offer, p["first_close"])
            else:
                comp_1yr = p["one_yr_return_pct"]
                comp_to_date = p["return_to_date_pct"]
                comp_day1 = p["day1_return_pct"]
            seed_1yr = rec.get("one_yr_return_pct")
            quarantined = rec.get("one_yr_quarantined")
            diverges = (seed_1yr is not None and comp_1yr is not None and seed_1yr != 0
                        and abs(comp_1yr - seed_1yr) / abs(seed_1yr) > DIVERGENCE_LIMIT)
            if diverges and rec.get("verified") and not quarantined:
                # already-verified figure moving >20% = data bug, not news
                divergences.append((tk, seed_1yr, comp_1yr))
                continue
            if not quarantined:
                # unverified seeds (findings-doc conflict #9) are approximations
                # meant to be replaced; overwrite, surfacing material changes
                if seed_1yr != comp_1yr:
                    changed.append((tk, seed_1yr, comp_1yr))
                if comp_1yr is not None or seed_1yr is None:
                    rec["one_yr_return_pct"] = comp_1yr if comp_1yr is not None else seed_1yr
            # quarantined +365d figures (documented WP-4/yfinance disagreements,
            # see conflict_note) keep the seed; live fields still refresh below
            if comp_day1 is not None and rec.get("day1_return_pct") is None:
                rec["day1_return_pct"] = comp_day1
            rec["return_to_date_pct"] = comp_to_date
            rec["last_price"] = p["last_close"]
            rec["last_price_as_of"] = p["last_close_date"]
            rec["verified"] = True

    if divergences:
        # abort WITHOUT writing comps.json - a verified figure moving >20%
        # means a data bug somewhere; nothing gets persisted until resolved
        print("STOP: computed figures diverge from verified seed by >20% — "
              "comps.json NOT written (likely a data bug, not news):", file=sys.stderr)
        for tk, seed, comp in divergences:
            print(f"  {tk}: seed 1yr {seed}% vs computed {comp}%", file=sys.stderr)
        return 1

    write_json_atomic(COMPS_PATH, comps)
    if changed:
        print("verified 1-yr figures that changed vs seed:")
        for tk, seed, comp in changed:
            print(f"  {tk}: {seed} -> {comp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
