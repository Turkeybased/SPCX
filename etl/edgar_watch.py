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
     "confidential_filed": "2026-06-01", "cik": 2130357},
    {"name": "OpenAI", "query": '"OpenAI"', "forms": "S-1,S-1/A",
     "confidential_filed": "2026-06-08"},
]
SPACEX_CIK = 1181412


def fts_search(query, forms):
    resp = get_with_retry(FTS_URL, params={"q": query, "forms": forms},
                          headers=HEADERS, timeout=30)
    return resp.json()


def issuer_filings(cik):
    """Use the issuer CIK once known; a full-text mention is not a filing."""
    resp = get_with_retry(SUBMISSIONS_URL.format(cik=cik),
                          headers=HEADERS, timeout=30)
    data = resp.json()
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accs = recent.get("accessionNumber", [])
    docs = recent.get("primaryDocument", [])
    hits = []
    for form, dt, acc, doc in zip(forms, dates, accs, docs):
        if form in ("424B4", "S-1", "S-1/A"):
            acc_nodash = acc.replace("-", "")
            hits.append({
                "form": form, "filing_date": dt,
                "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}/{doc}",
            })
    return sorted(hits, key=lambda f: f["filing_date"], reverse=True)


def main():
    status = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "companies": []}
    errors = 0
    total_watches = len(WATCHES) + 1  # +1 for the SpaceX submissions check
    # A transient outage must not erase a previously observed public filing.
    previous = json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}
    cached = {c["name"]: c for c in previous.get("companies", [])}

    for w in WATCHES:
        entry = {"name": w["name"], "confidential_s1_filed": w["confidential_filed"],
                 "public_s1": None, "status": "confidential (not in full-text search)"}
        try:
            if w.get("cik"):
                entry["cik"] = str(w["cik"])
                matches = issuer_filings(w["cik"])
                entry["filings"] = matches
            else:
                matches = search_issuer_filings(w)
            if matches:
                entry["public_s1"] = matches[0]
                entry["status"] = "424B4 FILED (priced)" if any(f["form"] == "424B4" for f in matches) else "PUBLIC S-1 ON EDGAR"
            else:
                entry["status"] = "No public S-1 found; confidential submission previously reported"
            entry["checked_at"] = status["generated_at"]
        except Exception as exc:
            entry = dict(cached.get(w["name"], entry))
            entry["refresh_error"] = str(exc)
            errors += 1
        status["companies"].append(entry)
        time.sleep(0.2)

    spacex = {"name": "SpaceX", "cik": str(SPACEX_CIK),
              "filings": [], "status": "no S-1/424B4 on EDGAR yet"}
    try:
        filings = issuer_filings(SPACEX_CIK)
        spacex["filings"] = filings
        if any(f["form"] == "424B4" for f in filings):
            spacex["status"] = "424B4 FILED (priced)"
        elif filings:
            spacex["status"] = "S-1 on EDGAR"
        spacex["checked_at"] = status["generated_at"]
    except Exception as exc:
        spacex = dict(cached.get("SpaceX", spacex))
        spacex["refresh_error"] = str(exc)
        errors += 1
    status["companies"].append(spacex)

    tmp = OUT_PATH.with_suffix(OUT_PATH.suffix + ".tmp")
    tmp.write_text(json.dumps(status, indent=2), encoding="utf-8")
    tmp.replace(OUT_PATH)
    print(f"wrote {OUT_PATH}")
    if errors:
        print(f"WARNING: {errors}/{total_watches} EDGAR watch(es) failed; prior observations retained.", file=sys.stderr)
    return 1 if errors >= total_watches else 0


def search_issuer_filings(w):
    """Fallback for issuers whose CIK has not yet been identified."""
    data = fts_search(w["query"], w["forms"])
    hits = data.get("hits", {}).get("hits", [])
    matches = []
    for hit in hits:
        src = hit.get("_source", {})
        names = src.get("display_names", [])
        # Ignore funds whose names merely contain the watched company.
        if any(n.split(" (CIK")[0].strip().lower() in
               {w["name"].lower(), w["name"].lower() + " group pbc", w["name"].lower() + ", pbc"}
               for n in names):
            acc = src.get("adsh", "")
            ciks = src.get("ciks", [])
            document = hit.get("_id", "").split(":", 1)[-1]
            if not acc or not ciks or not document:
                continue
            matches.append({"form": src.get("file_type"), "filing_date": src.get("file_date"),
                            "entity": " ".join(names),
                            "url": f"https://www.sec.gov/Archives/edgar/data/{int(ciks[0])}/{acc.replace('-', '')}/{document}"})
    return sorted(matches, key=lambda f: f["filing_date"] or "", reverse=True)


if __name__ == "__main__":
    sys.exit(main())
