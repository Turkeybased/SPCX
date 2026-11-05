"""Refresh SpaceX OHLCV and SPY/QQQ context without re-pricing historical comps.

Uses Yahoo's chart endpoint directly (requests only). Validates issuer identity,
dates and bars before replacing cached data. Includes completed US sessions only.
News in spacex_events.json is a separately curated, source-checked archive.
"""
import argparse
import json
import math
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
START = "2026-06-12"
NY = ZoneInfo("America/New_York")
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"


def write_atomic(path, value):
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def percent(base, end):
    return round((end / base - 1) * 100, 4) if base else None


def parse_chart(payload, ticker, now):
    chart = payload.get("chart", {})
    if chart.get("error") or not chart.get("result"):
        raise ValueError(f"{ticker}: missing chart result")
    result = chart["result"][0]
    meta = result.get("meta", {})
    if meta.get("symbol") != ticker:
        raise ValueError("Provider returned a different symbol")
    if ticker == "SPCX" and (meta.get("instrumentType") != "EQUITY" or
                             "space exploration" not in meta.get("longName", "").lower()):
        raise ValueError("SPCX issuer identity mismatch; refusing to use legacy ETF data")
    if result.get("events", {}).get("splits"):
        raise ValueError(f"{ticker}: split detected; review price basis before refreshing")
    quotes = result.get("indicators", {}).get("quote", [{}])[0]
    rows = []
    for index, timestamp in enumerate(result.get("timestamp", [])):
        session = datetime.fromtimestamp(timestamp, NY)
        day = session.date().isoformat()
        # Daily bars for an open session are provisional. Do not call them closes.
        if day < START or session.date() > now.astimezone(NY).date():
            continue
        close_time = session.replace(hour=16, minute=15, second=0, microsecond=0)
        regular = meta.get("currentTradingPeriod", {}).get("regular", {})
        if regular.get("start") and datetime.fromtimestamp(regular["start"], NY).date() == session.date():
            close_time = datetime.fromtimestamp(regular["end"], NY)
            if now.timestamp() < regular["end"] + 900:
                continue
        elif now < close_time:
            continue
        bar = {key.lower(): quotes.get(key, [])[index] if index < len(quotes.get(key, [])) else None
               for key in ("open", "high", "low", "close", "volume")}
        if any(not isinstance(bar[k], (float, int)) or not math.isfinite(bar[k]) or bar[k] <= 0
               for k in ("open", "high", "low", "close")):
            continue
        if not isinstance(bar["volume"], (float, int)) or not math.isfinite(bar["volume"]) or bar["volume"] <= 0:
            continue
        if not (bar["low"] <= min(bar["open"], bar["close"]) <= max(bar["open"], bar["close"]) <= bar["high"]):
            raise ValueError(f"{ticker}: invalid OHLC range on {day}")
        rows.append({"date": day, **{k: int(v) if k == "volume" else round(float(v), 4) for k, v in bar.items()}})
    if not rows or rows[0]["date"] != START:
        raise ValueError(f"{ticker}: incomplete history; listing-day bar unavailable")
    dates = [r["date"] for r in rows]
    if dates != sorted(set(dates)):
        raise ValueError(f"{ticker}: duplicate or out-of-order sessions")
    if (now.astimezone(NY).date() - datetime.fromisoformat(dates[-1]).date()).days > 4:
        raise ValueError(f"{ticker}: provider history is stale ({dates[-1]})")
    return {"ticker": ticker, "issuer": meta.get("longName"), "currency": meta.get("currency", "USD"),
            "price_basis": "Unadjusted daily closes; price returns exclude dividends. No splits in retrieved period.",
            "source_url": f"https://finance.yahoo.com/quote/{ticker}/history/", "series": rows,
            "last_close": rows[-1]["close"], "last_close_date": rows[-1]["date"]}


def fetch(ticker, now):
    for attempt in range(3):
        try:
            response = requests.get(URL.format(ticker=ticker), params={
                "period1": int(datetime.fromisoformat(START).replace(tzinfo=timezone.utc).timestamp()),
                "period2": int(now.timestamp()), "interval": "1d", "events": "div,splits"},
                headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            response.raise_for_status()
            return parse_chart(response.json(), ticker, now)
        except (requests.RequestException, ValueError, KeyError) as exc:
            if attempt == 2:
                raise
            print(f"{ticker}: retrying after {type(exc).__name__}", file=sys.stderr)
            time.sleep(attempt + 1)


def main(sync_frontend=True):
    now = datetime.now(timezone.utc)
    datasets = {ticker: fetch(ticker, now) for ticker in ("SPCX", "SPY", "QQQ")}
    stock = datasets["SPCX"]
    series = stock["series"]
    anniversary = datetime.fromisoformat(series[0]["date"]).date() + timedelta(days=365)
    year_bar = next((p for p in series if datetime.fromisoformat(p["date"]).date() >= anniversary), None)
    cache = json.loads((ROOT / "data/prices.json").read_text(encoding="utf-8"))
    previous_series = list(cache.get("prices", {}).get("SPCX", {}).get("series", []))
    prior_context_path = ROOT / "data/spacex_market.json"
    if prior_context_path.exists():
        previous_series += json.loads(prior_context_path.read_text(encoding="utf-8")).get("stock", {}).get("series", [])
    missing_dates = {p["date"] for p in previous_series} - {p["date"] for p in series}
    if missing_dates:
        raise ValueError(f"New history drops retained sessions: {sorted(missing_dates)}")
    if series[-1]["date"] < cache.get("prices", {}).get("SPCX", {}).get("last_close_date", ""):
        raise ValueError("New history ends before the retained cache")
    spcx = {"ticker": "SPCX", "status": "ok", "issuer": stock["issuer"], "source_url": stock["source_url"],
            "first_trade_date": series[0]["date"], "first_open": series[0]["open"], "first_close": series[0]["close"],
            "last_close": series[-1]["close"], "last_close_date": series[-1]["date"],
            "close_plus_365": year_bar["close"] if year_bar else None,
            "one_yr_return_pct": percent(series[0]["close"], year_bar["close"]) if year_bar else None,
            "day1_return_pct": percent(series[0]["open"], series[0]["close"]),
            "return_to_date_pct": percent(series[0]["close"], series[-1]["close"]),
            "refreshed_at": now.isoformat(timespec="seconds"), "series": series}
    cache["prices"]["SPCX"] = spcx
    cache["spacex_refreshed_at"] = spcx["refreshed_at"]
    cache["refresh_scope_note"] = "SPCX refreshed independently; other ticker snapshots retain their original dates."
    # Do not advance the global timestamp for the untouched historical comps.
    comps = json.loads((ROOT / "data/comps.json").read_text(encoding="utf-8"))
    deal = next(d for d in comps["deals"] if d.get("ticker") == "SPCX")
    offer = deal["offer_price_usd"]
    deal.update(last_price=spcx["last_close"], last_price_as_of=spcx["last_close_date"],
                day1_return_pct=percent(offer, spcx["first_close"]),
                return_to_date_pct=percent(offer, spcx["last_close"]))
    if year_bar:
        deal["one_yr_return_pct"] = percent(offer, year_bar["close"])
    context = {"generated_at": spcx["refreshed_at"], "as_of": stock["last_close_date"],
               "market_timezone": "America/New_York", "session_policy": "Completed sessions only; 15-minute publication buffer after close.",
               "offer_price_usd": offer, "source": "Yahoo Finance daily OHLCV chart API",
               "stock": stock, "benchmarks": {t: datasets[t] for t in ("SPY", "QQQ")}}
    for name, value in (("spacex_market.json", context), ("prices.json", cache), ("comps.json", comps)):
        write_atomic(ROOT / "data" / name, value)
    # This focused command also updates the copies actually served by Vercel.
    for name in ("spacex_market.json", "prices.json", "comps.json", "spacex_events.json") if sync_frontend else ():
        source = ROOT / "data" / name
        if source.exists():
            write_atomic(ROOT / "frontend/data" / name, json.loads(source.read_text(encoding="utf-8")))
    print(f"Refreshed SPCX: {len(series)} sessions, {series[0]['date']} to {stock['last_close_date']}; last close ${stock['last_close']:.2f}")
    return 0


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--no-sync", action="store_true", help="Let run_all.py publish all frontend snapshots only after every step succeeds")
        args = parser.parse_args()
        sys.exit(main(sync_frontend=not args.no_sync))
    except Exception as error:
        print(f"STOP: SpaceX refresh failed; prior caches retained: {error}", file=sys.stderr)
        sys.exit(1)
