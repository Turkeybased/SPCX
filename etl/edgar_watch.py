"""Watch EDGAR for public S-1s from Anthropic and OpenAI and SpaceX's 424B4.

Confidential (draft) S-1 submissions are not in EDGAR full-text search; this
script detects the moment they flip public. SpaceX is also checked directly by
CIK via the submissions API.

Writes data/filing_status.json. Respects EDGAR limits: <10 req/s (we sleep
between calls) and a proper User-Agent.
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data" / "filing_status.json"

HEADERS = {"User-Agent": "solo solomon.foshko@gmail.com"}
FTS_URL = "https://efts.sec.gov/LATEST/search-index"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:0>10}.json"

RETRY_ATTEMPTS = 3
RETRY_BACKOFF = (1, 2, 4)  # seconds before each retry; SEC EDGAR 403/429/503s automated traffic


def get_with_retry(url, **kwargs):
    """GET with up to RETRY_ATTEMPTS tries and exponential backoff. Only the
    final failure propagates; transient SEC 403/429/503 blips are absorbed."""
    last_exc = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            resp = requests.get(url, **kwargs)
            resp.raise_for_status()
            return resp
        except Exception as exc:  # network error or non-2xx status
            last_exc = exc
            if attempt < RETRY_ATTEMPTS - 1:
                wait = RETRY_BACKOFF[attempt]
                print(f"  request to {url} failed ({exc}); retrying in {wait}s "
                      f"({attempt + 1}/{RETRY_ATTEMPTS})", file=sys.stderr)
                time.sleep(wait)
    raise last_exc

WATCHES = [
    {"name": "Anthropic", "query": '"Anthropic"', "forms": "S-1,S-1/A",
     "confidential_filed": "2026-06-01"},
    {"name": "OpenAI", "query": '"OpenAI"', "forms": "S-1,S-1/A",
     "confidential_filed": "2026-06-08"},
]
SPACEX_CIK = 1181412


def fts_search(query, forms):
    resp = get_with_retry(FTS_URL, params={"q": query, "forms": forms},
                          headers=HEADERS, timeout=30)
    return resp.json()


def spacex_filings():
    resp = get_with_retry(SUBMISSIONS_URL.format(cik=SPACEX_CIK),
                          headers=HEADERS, timeout=30)
    data = resp.json()
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accs = recent.get("accessionNumber", [])
    hits = []
    for form, dt, acc in zip(forms, dates, accs):
        if form in ("424B4", "S-1", "S-1/A"):
            acc_nodash = acc.replace("-", "")
            hits.append({
                "form": form, "filing_date": dt,
                "url": f"https://www.sec.gov/Archives/edgar/data/{SPACEX_CIK}/{acc_nodash}/{acc}-index.htm",
            })
    return hits


def main():
    status = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "companies": []}
    errors = 0
    total_watches = len(WATCHES) + 1  # +1 for the SpaceX submissions check

    for w in WATCHES:
        entry = {"name": w["name"], "confidential_s1_filed": w["confidential_filed"],
                 "public_s1": None, "status": "confidential (not in full-text search)"}
        try:
            data = fts_search(w["query"], w["forms"])
            hits = data.get("hits", {}).get("hits", [])
            # Filter to hits where the filer entity actually matches the name.
            matches = []
            for h in hits:
                src = h.get("_source", {})
                names = " ".join(src.get("display_names", []))
                if w["name"].lower() in names.lower():
                    matches.append({
                        "form": src.get("file_type"),
                        "filing_date": src.get("file_date"),
                        "entity": names,
                        "url": "https://www.sec.gov/Archives/edgar/data/"
                               + src.get("_id", "").replace(":", "/"),
                    })
            if matches:
                entry["public_s1"] = matches[0]
                entry["status"] = "PUBLIC S-1 ON EDGAR"
        except Exception as exc:
            entry["status"] = f"error: {exc}"
            errors += 1
        status["companies"].append(entry)
        time.sleep(0.2)  # stay far under 10 req/s

    spacex = {"name": "SpaceX", "cik": str(SPACEX_CIK),
              "filings": [], "status": "no S-1/424B4 on EDGAR yet"}
    try:
        filings = spacex_filings()
        spacex["filings"] = filings
        if any(f["form"] == "424B4" for f in filings):
            spacex["status"] = "424B4 FILED (priced)"
        elif filings:
            spacex["status"] = "S-1 on EDGAR"
    except Exception as exc:
        spacex["status"] = f"error: {exc}"
        errors += 1
    status["companies"].append(spacex)

    tmp = OUT_PATH.with_suffix(OUT_PATH.suffix + ".tmp")
    tmp.write_text(json.dumps(status, indent=2), encoding="utf-8")
    tmp.replace(OUT_PATH)  # atomic: no truncated JSON if the run is killed
    print(f"wrote {OUT_PATH}")
    if errors:
        print(f"WARNING: {errors}/{total_watches} EDGAR watch(es) failed after "
              "retries — if this repeats, stop and report.", file=sys.stderr)
    # Only fail the daily refresh if EVERY watch failed (likely SEC-wide
    # outage / block). A single failed watch is downgraded to a logged
    # warning + exit 0 so one EDGAR blip doesn't block the price refresh and
    # the day's data commit.
    if errors >= total_watches:
        print("ERROR: all EDGAR watches failed — failing the step.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
