"""One-shot seeder: rebuild comps.json tech_comps/deals/cohorts from the v2
research drop (docs/research/). mega_ipos are preserved from the current file.

This is a curation tool, not part of the daily ETL - run manually when the
research dataset is re-issued.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPS = ROOT / "data" / "comps.json"
CSV = ROOT / "docs" / "research" / "comps.csv"
FINDINGS = "/docs/research/03-research-findings.md"
AS_OF = "2026-06-10"

EDGAR_424B4 = {
    "GOOGL": "https://www.sec.gov/Archives/edgar/data/1288776/000119312504143377/d424b4.htm",
    "META": "https://www.sec.gov/Archives/edgar/data/1326801/000119312512240111/d287954d424b4.htm",
    "BABA": "https://www.sec.gov/Archives/edgar/data/1577552/000119312514347620/d709111d424b4.htm",
    "V": "https://www.sec.gov/Archives/edgar/data/1403161/000119312508060989/d424b4.htm",
    "SNOW": "https://www.sec.gov/Archives/edgar/data/1640147/000162828020013667/snowflake424b4.htm",
    "COIN": "https://www.sec.gov/Archives/edgar/data/1679788/000162828021003168/coinbaseglobalincs-1.htm",
    "CRWV": "https://www.sec.gov/Archives/edgar/data/1769628/000119312525067651/d899798d424b4.htm",
}

CONFLICTS = {
    "CRWV": "(#1) IPO year: Mar 2025 (CNBC, authoritative) vs 'Mar 2026' in two 2026 articles (errors). "
            "+365d return: +93.7% (WP-4 CSV, price 77.47) vs +72.9% (yfinance close on/after 2026-03-28). "
            "Different date convention suspected. Not averaged; CSV figure shown.",
    "CBRS": "Offer price ~$155 is the midpoint of the $150-$160 range; exact final price pending 424B4 (findings v2 sec.7.4).",
    "BABA": "+365d return: -13.3% (WP-4 CSV, price 58.97) vs -6.0% (yfinance close on/after IPO+365d, 2015-09-21). "
            "Likely different anniversary-date convention. Not averaged; CSV figure shown.",
    "V": "+365d return: +45.5% (WP-4 CSV, price 16.00) vs +19.8% (yfinance split-adj close ~13.2 on 2009-03-19). "
         "CSV +365d price looks like a later-2009 date - probable WP-4 data error. Not averaged; CSV figure shown pending re-research.",
    "SNAP": "+365d return: -6.6% (WP-4 CSV, price 15.87) vs +5.9% (yfinance close ~18.01 on 2018-03-02). "
            "Different date convention suspected. Not averaged; CSV figure shown.",
    "COIN": "+365d return: -54.9% (WP-4 CSV, price 112.71) vs -41.1% (yfinance close ~147 on 2022-04-14). "
            "CSV price matches May-2022 crash levels, not the April anniversary - probable WP-4 data error. "
            "Not averaged; CSV figure shown pending re-research.",
}

FID = "https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf"
MORN = "https://global.morningstar.com/en-gb/stocks/financials-look-reckless-lifting-xais-hood-spacex-ipo"
RITTER = "https://site.warrington.ufl.edu/ritter/ipo-data/"
GRANITE = "https://graniteshares.com/research/everything-you-need-to-know-about-spacex/"
TECHTIMES = "https://www.techtimes.com/articles/318170/20260610/spacex-ipo-order-books-close-four-times-oversubscribed-gray-market-slide-signals-shrinking-premium.htm"


def analysis():
    """Question-oriented analysis layer. Every item carries a source; items
    marked derived are arithmetic on sourced figures, not new claims.
    NO buy/sell advice - these are observations and dates to watch."""
    return {
        "note": "Interpretive layer distilled from docs/research/03-research-findings.md. Flags are observations with sources, not recommendations.",
        "red_flags": [
            {"text": "xAI drag: $6.35B 2025 operating loss on $3.2B revenue (which bundles X/Twitter ads - Grok-only revenue is smaller). Pre-merger core SpaceX made ~$8B op profit; consolidated is a ~$4.9B net-loss company.", "source_url": MORN},
            {"text": "Starship: ~$3B/yr R&D with zero Starship revenue - the S-1's top risk factor.", "source_url": FINDINGS},
            {"text": "Both independent valuations are far below the ask: Morningstar $780B (-53%), Damodaran ~$1.30T (-26%). Nobody independent gets to $1.75T.", "source_url": "https://www.wsj.com/business/what-the-dean-of-valuation-thinks-elon-musks-spacex-is-really-worth-bfe8061c"},
            {"text": "~94x trailing sales while loss-making. Profitable mega-comps listed at far less: Facebook ~28x, Google ~16x, Alibaba ~19x. Aramco at the same $1.7T valuation earned ~$88B net income.", "source_url": FINDINGS},
            {"text": "Priced at ~2.2x the company's own December 2025 tender mark ($800B, $421/sh pre-split) six months earlier - and 40%+ above its Feb 2026 self-assessed $1.25T.", "source_url": "https://www.reuters.com/business/spacex-sets-800-billion-valuation-bloomberg-news-reports-2025-12-13/"},
            {"text": "Retail allocation ~30% (~$22.5B) is ~3x the mega-cap norm - heavy distribution to retail at the ask is historically a late-cycle pattern.", "source_url": "https://www.cnbc.com/2026/06/09/spacex-ipo-explained-stock-price-date.html"},
            {"text": "Gray-market premium is shrinking into the deal: Hyperliquid perps ~$216-230 mid-May down to ~$157 (+16%) by Jun 10.", "source_url": TECHTIMES},
            {"text": "Aggressive lockup: 20% of insider holdings unlock at the FIRST quarterly earnings (~Sep), +7% at 70/90/105/120/135 days; fully unlocked Sep-Dec 2026 vs the standard 180-day. Early, repeated supply waves.", "source_url": GRANITE},
            {"text": "Controlled company: Musk holds 82.4% of votes via 10-vote Class B. Public Class A has 1 vote/share and cannot influence the board.", "source_url": FID},
            {"text": "Balance sheet carries ~$30B debt / ~$14B net debt after a $20B bridge loan taken in Mar 2026 to retire xAI's debt stack.", "source_url": FINDINGS},
            {"text": "Demand signal is murky: Bloomberg TV says ~2x oversubscribed; Reuters/Eastern Herald say 3.5-4x. Conflict unresolved.", "source_url": FINDINGS},
        ],
        "counterpoints": [
            {"text": "Starlink is a real, growing, profitable business: $11.4B revenue (61% of total), $4.4B op profit in 2025.", "source_url": FINDINGS},
            {"text": "83% share of global mass-to-orbit (2025) - genuine monopoly economics in launch.", "source_url": "https://global.morningstar.com/en-ca/stocks/spacex-what-investors-need-know-about-its-enormous-upcoming-ipo"},
            {"text": "Contracted AI revenue exists: Anthropic leases Colossus 1 & 2 at $1.25B/month (~$15B/yr) through May 2029.", "source_url": "https://aswathdamodaran.substack.com/p/revisiting-the-spacex-valuation-a"},
            {"text": "Second anchor tenant (FWP, Jun 5): Google signed a Cloud Service Agreement paying SpaceX $920M/month from Oct 2026 through Jun 2029 (~110,000 NVIDIA GPUs). Caveats in the same filing: if SpaceX misses the Sep 30, 2026 GPU delivery deadline Google can terminate or take fewer at pro-rata fees, and after Dec 31, 2026 either party can terminate on 90 days' notice.", "source_url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026041150/spacexagreementfwp.htm"},
            {"text": "Size is on its side: IPOs with LTM sales >= $100M roughly match style benchmarks (+2.3% 3yr style-adj); long-run IPO underperformance concentrates in small caps.", "source_url": RITTER},
            {"text": "Damodaran's moonshot scenario values the AI segment alone at ~$1.3T standalone (7% probability per Morningstar's weighting) - the bull case is real, just low-probability-weighted.", "source_url": FINDINGS},
            {"text": "CoreWeave lesson: the last hated AI-infra IPO (priced below range, flat day-1) returned +139% to Jun 2026. Sentiment at listing is not destiny.", "source_url": FINDINGS},
        ],
        "timeline": [
            {"date": "2026-06-11", "event": "Pricing (after close). Watch: final price vs $135, greenshoe terms in 424B4, final Musk voting % (pin conflict #2).", "source_url": FINDINGS},
            {"date": "2026-06-12", "event": "First trade. Base rate: the day-1 pop is a weak, high-dispersion guide to the 1-yr outcome (Snap +44% day-1 then -68% long-run; Uber -7.6% day-1 then +52%; Figma +250% then below offer). Chasing the pop is the classic error.", "source_url": FINDINGS},
            {"date": "2026-07-07 to 2026-07-22", "event": "Quiet period ends ~25-40 days post-IPO: Goldman/Morgan Stanley initiations land. Underwriter targets are structurally biased high.", "source_url": FINDINGS, "derived": True},
            {"date": "~2026-08-21 to 2026-10-25", "event": "Staggered unlocks: +7% of holdings at 70/90/105/120/135 days (Aug 21, Sep 10, Sep 25, Oct 10, Oct 25 - derived from Jun 12). Repeated supply waves; Facebook 2012 bottomed amid its lockup expiries, ~-50% from offer, 4 months in.", "source_url": GRANITE, "derived": True},
            {"date": "~2026-09", "event": "First quarterly earnings = first 20% unlock AND first real look at post-IPO xAI burn. Largest single supply + information event of year one.", "source_url": GRANITE},
            {"date": "~2026-10 / Q4 2026", "event": "Anthropic (~Oct) and OpenAI (~Q4) IPO windows: two more mega-AI listings competing for the same institutional dollars. Supply of 'AI mega-cap exposure' stops being scarce.", "source_url": "https://www.cnbc.com/2026/06/08/openai-confidentially-files-for-ipo-prepping-wall-street-for-ai-debut.html"},
            {"date": "2027-06-13", "event": "Musk's 366-day hold ends. Also the +365d mark where this dashboard's comp table says the average recent mega-IPO verdict is in.", "source_url": FINDINGS, "derived": True},
        ],
        "base_rates": [
            {"stat": "56.1%", "text": "of ALL IPOs (1975-2021) traded below offer price 3 years later. For large IPOs (sales >= $100M): 44.5%. Patience has usually been paid.", "source_url": RITTER},
            {"stat": "r=0.46", "text": "Pearson correlation of day-1 pop vs +365d return in this 15-name comp set (computed) - positive but not reliable enough to chase: Snap +44% to -6.6%, Figma +250% to below offer, Uber -7.6% to +52%. At cohort level the hottest pop years (1999-2000, 64.6% mean) produced the worst 3-yr returns in the dataset.", "source_url": FINDINGS, "derived": True},
            {"stat": "6/8", "text": "of profitable-at-IPO comps are positive vs offer to Jun 2026; the 9 unprofitable ones split into big winners (Snowflake, Airbnb) and -80% wrecks (Lyft, Rivian). SpaceX lists unprofitable.", "source_url": FINDINGS},
            {"stat": "-53.1%", "text": "average 3-yr buy-and-hold of the 1999-2000 bubble cohort (856 IPOs, 64.6% mean day-1 pop). Pops were broad then; 2025-26 pops are concentrated - a real difference.", "source_url": RITTER},
            {"stat": "-3.6%/yr", "text": "average IPO underperformance vs same-size firms for 5 years post-listing (Ritter) - concentrated in small caps; large IPOs roughly match benchmarks.", "source_url": RITTER},
            {"stat": "-49.4%", "text": "average 1-yr market-adjusted return of deSPACs 2012-2022 - the base rate for the LAST hype-wave's vehicle of choice. (SPCX is a traditional IPO; this is the cautionary anchor.)", "source_url": "https://site.warrington.ufl.edu/ritter/files/IPOs-SPACs.pdf"},
        ],
    }


# +365d figures where WP-4 CSV and yfinance disagree >20% (see CONFLICTS):
# the seed value is kept and the daily ETL must not overwrite or re-trip on it.
QUARANTINED_1YR = {"BABA", "V", "SNAP", "COIN", "CRWV"}


def f(v):
    v = (v or "").strip()
    if v in ("", "<365d"):
        return None
    return float(v)


def tech_comps():
    out = []
    for r in csv.DictReader(open(CSV, encoding="utf-8-sig")):
        tk = r["ticker"]
        mktcap = f(r["implied_mktcap_at_ipo_b"])
        rev = f(r["ttm_revenue_at_ipo_b"])
        one_yr = f(r["return_plus365d"])
        rec = {
            "company": r["company"],
            "ticker": tk,
            "ipo_date": r["ipo_date"],
            "offer_price_usd": f(r["offer_price"]),
            "day1_close_usd": f(r["day1_close"]),
            "ipo_valuation_usd": mktcap * 1e9 if mktcap else None,
            "raise_usd": f(r["raise_b"]) * 1e9 if f(r["raise_b"]) is not None else None,
            "revenue_at_ipo_usd": rev * 1e9 if rev is not None else None,
            "profitable_at_ipo": {"YES": True, "NO": False}.get(r["gaap_profitable_at_ipo"]),
            "ps_multiple": round(mktcap / rev, 1) if (mktcap and rev) else None,
            "ps_multiple_note": "derived: implied mktcap at IPO / TTM revenue (WP-4 CSV basis)" if (mktcap and rev) else ("n/m (~zero revenue)" if rev == 0 else None),
            "day1_return_pct": round(f(r["day1_return"]) * 100, 1),
            "one_yr_return_pct": round(one_yr * 100, 1) if one_yr is not None else None,
            "return_basis": "vs offer price (split-adjusted); Coinbase vs Nasdaq reference price (DPO)",
            "verified": True,
            "note": r["notes"] or None,
            "source_url": EDGAR_424B4.get(tk, FINDINGS),
            "conflict_note": CONFLICTS.get(tk),
            "as_of": AS_OF,
        }
        if tk in QUARANTINED_1YR:
            rec["one_yr_quarantined"] = True
        out.append(rec)
    return out


def deals():
    return [
        {
            "company": "SpaceX", "ticker": "SPCX", "exchange": "Nasdaq (and Nasdaq Texas)",
            "status": "S-1 public May 20 (conf. Apr 1); S-1/A#2 Jun 3 set $135; prices 2026-06-11, trades 2026-06-12",
            "ipo_date": "2026-06-12",
            "offer_price_usd": 135.0,
            "shares_offered": 555555555,
            "greenshoe_shares": 83333333,
            "target_valuation_usd": 1750000000000,
            "valuation_note": "$1.75T and $1.77T both correct per S-1: pre- vs post-pending-acquisition (EchoStar spectrum, Cursor) share counts (findings v2 sec.1.2)",
            "raise_usd": 75000000000,
            "raise_with_greenshoe_usd": 85700000000,
            "revenue_usd": 18670000000, "revenue_period": "FY2025 (+33% YoY, post-xAI consolidation)",
            "net_income_usd": -4940000000, "net_income_note": "2025 net loss -$4.94B; Q1 2026 -$4.28B; accumulated deficit -$41.3B; 2025 EBITDA $6.58B",
            "profitable": False,
            "ps_multiple": 94, "ps_multiple_note": "derived ~94-107x 2025 revenue at offer",
            "segment_detail": "Starlink $11.4B rev (61%); xAI rev $3.20B 2025, op loss -$6.35B (verified vs S-1; $6.4B = media rounding), xAI capex $12.7B (~61% of SpaceX total); pre-merger core generated ~$8B op profit",
            "governance": "Musk voting power 82.4% base / 82.3% post-greenshoe (S-1/A#2 primary); Class B 10 votes/sh; controlled company under Nasdaq rules",
            "lockup": "Staggered: 20% unlocks at first quarterly earnings, +7% at 70/90/105/120/135 days; Musk 366-day hold",
            "order_book": "~$250B total demand, 3.5-4x oversubscribed (Reuters/Eastern Herald); Bloomberg TV cited ~2x - conflict noted; retail ~30% (~$22.5B)",
            "valuation_anchors": [
                {"analyst": "Morningstar (Owens)", "value_usd": 780000000000, "per_share": 63, "vs_ipo": "-53%", "method": "DCF + probability-weighted AI scenarios", "date": "2026-06-08"},
                {"analyst": "Damodaran (post-prospectus)", "value_usd": 1300000000000, "per_share": 100, "vs_ipo": "-26%", "method": "SOTP DCF, $1.25-1.35T range", "date": "2026-06-04"},
                {"analyst": "IPO pricing", "value_usd": 1770000000000, "per_share": 135, "vs_ipo": "-", "method": "bookbuild", "date": "2026-06-11"}
            ],
            "private_ladder": "$400B/$212 (Jul 2025 tender) -> $800B/$421 pre-split (Dec 2025 tender; resolved - X post claiming $135/$250B is erroneous) -> $1.25T (Feb 2026 xAI merger) -> ~$1.5T (Apr 2026) -> $1.75-1.77T IPO",
            "gray_market": "Hyperliquid perp ~$157 (~+16% vs offer) Jun 10, off May peak $216-230; Polymarket consensus first close ~$175 (~$2.3T), 75% prob close >$135",
            "contracted_ai_revenue": "Anthropic Colossus lease $1.25B/mo to May 2029 (S-1); Google Cloud Service Agreement $920M/mo Oct 2026-Jun 2029, ~110k NVIDIA GPUs (FWP Jun 5) - terminable by either party on 90 days' notice after Dec 31 2026, and by Google if the Sep 30 2026 GPU delivery deadline is missed",
            "cik": "1181412",
            "day1_return_pct": None, "one_yr_return_pct": None, "return_to_date_pct": None,
            "verified": False,
            "source_url": "https://www.fidelity.com/bin-public/600_Fidelity_Institutional/fidelityinstitutional/Application/AP154833/documents/clients/SPCXLV/SPCXLVred.pdf",
            "conflict_note": "(#2 RESOLVED) Musk voting = 82.4% per S-1/A#2; '79%' unsourced, BitMEX '85%' uncorroborated. (#3 RESOLVED) Dec 2025 tender = $421/sh at ~$800B (Reuters/Bloomberg/Fortune). (#4) Starlink $4.4B op profit vs $7.2B segment EBITDA are different metrics - do not conflate. (OPEN) Order book: ~2x (Bloomberg TV) vs 3.5-4x (Reuters) oversubscription.",
            "as_of": AS_OF,
        },
        {
            "company": "Anthropic", "ticker": None, "exchange": None,
            "status": "confidential S-1 filed 2026-06-01 (Anthropic PBC); public S-1 ~Summer-Fall; target window ~Oct 2026",
            "ipo_date": None, "offer_price_usd": None,
            "target_valuation_usd": 965000000000,
            "valuation_basis": "Series H $65B at $965B post-money, May 28 2026 (Altimeter, Dragoneer, Greenoaks, Sequoia; $15B of $65B previously committed hyperscaler money)",
            "raise_usd": None, "raise_note": "TBD; FutureSearch median post-IPO mktcap $1.05T (p10 $750B / p90 $1.6T)",
            "revenue_usd": 47000000000, "revenue_period": "ARR May 2026 ($14B Feb 2026, ~$30B Apr 2026; Q1 2026 GAAP quarterly $4.8B; Claude Code ~$8B ARR)",
            "profitable": None,
            "profitability_note": "first operating profit ~$559M projected Q2 2026 (operating, not GAAP net, excl. frontier training capex); 2026 FY cash flow ~-$11B to -$14B; break-even ~2028",
            "ps_multiple": 20.5, "ps_multiple_note": "derived ~21x ARR (FutureSearch: ~10x median 2027 ARR of $93B)",
            "governance": "Delaware PBC + Long-Term Benefit Trust: Class T stock held by independent trust elects board majority by ~2027; public shareholders will NOT control the board; underwriters Morgan Stanley, Goldman Sachs, JPMorgan",
            "compute_commitments": "~$382B+ disclosed (AWS >$100B/10yr, Google ~$200B/5yr, Azure $30B, SpaceX Colossus $1.25B/mo to May 2029, Fluidstack $50B, Akamai $1.8B)",
            "valuation_ladder": "$61.5B (Mar 2025, Series E) -> $183B (Sep 2025, F) -> $380B (Feb 2026, G) -> $965B (May 2026, H) = ~15.7x in ~14 months",
            "day1_return_pct": None, "one_yr_return_pct": None, "return_to_date_pct": None,
            "verified": False,
            "source_url": "https://www.anthropic.com/news/confidential-draft-s1-sec",
            "conflict_note": "(NEW, v2 sec.2.3) 2025 annual revenue disputed: ~$4.5B (The Information) vs >$5B-to-date (CFO sworn declaration Mar 2026) vs ~$10B (CNBC) - different methodologies (GAAP vs ARR vs cumulative); public S-1 will settle. ARR figures are forward run-rates, not TTM GAAP; gross-vs-net treatment of hyperscaler compute credits unresolved.",
            "as_of": AS_OF,
        },
        {
            "company": "OpenAI", "ticker": None, "exchange": "Nasdaq or NYSE expected",
            "status": "confidential S-1 filed 2026-06-08 (OpenAI Group PBC); target ~Q4 2026; 'may be a while' - Altman/Friar at odds on timing",
            "ipo_date": None, "offer_price_usd": None,
            "target_valuation_usd": 852000000000,
            "valuation_basis": "$122B round closed Mar 31 2026 (largest private fundraise ever; Amazon $50B, Nvidia $30B, SoftBank $30B); pre-IPO consensus target $730-850B",
            "raise_usd": None, "raise_note": "TBD",
            "revenue_usd": 25000000000, "revenue_period": "ARR Feb 2026 (~$24B ~May 2026; 2025 annual $13B CFO-stated; Q1 2026 GAAP quarterly $5.7B; 2026 target ~$30B)",
            "profitable": False,
            "profitability_note": "Q1 2026 non-GAAP operating margin -122% (-$6.95B loss on $5.7B rev); cash-flow positive ~2029-2030; ~900M weekly ChatGPT users, ~50M paying subscribers",
            "ps_multiple": 34, "ps_multiple_note": "derived ~34x ARR at $852B (~24-28x on 2026 target)",
            "governance": "OpenAI Foundation (nonprofit) holds 26% and appoints ALL board members; Microsoft ~27% fully diluted + 20% of revenue until AGI certified + IP access to 2032; Altman ~7%; profit caps removed; underwriters Goldman Sachs, Morgan Stanley",
            "compute_commitments": "~$1.4T over 8 years (Azure primary, Oracle, Amazon, NVIDIA); HSBC projects $207B funding shortfall by 2030 even if revenue targets hit",
            "valuation_ladder": "$157B (Oct 2024) -> $300B (Mar 2025) -> ~$500B (Oct 2025, PBC conversion) -> $852B (Mar 2026)",
            "day1_return_pct": None, "one_yr_return_pct": None, "return_to_date_pct": None,
            "verified": False,
            "source_url": "https://openai.com/index/openai-submits-confidential-s-1/",
            "conflict_note": "(#6 RESOLVED) Round closed Mar 31 2026 per OpenAI.com/Bloomberg. (#8, expanded v2 sec.3.4) Loss figures are THREE distinct metrics conflated in media: ~$14B 2026 non-GAAP vs $25-26B GAAP est.; cumulative '$44B' (2023-28, excl. stock comp, older docs) vs '$115B' (cash burn thru 2029, The Information) vs '$143B' (negative FCF 2024-29 incl. capex, Deutsche Bank). 2028 op loss: WSJ $74B vs TechCrunch $85B - both cited, not averaged.",
            "as_of": AS_OF,
        },
    ]


def cohorts():
    return [
        {
            "cohort": "Dot-com bubble (1999-2000)",
            "n_ipos": 856, "mean_day1_return_pct": 64.6,
            "n_ipos_1999": 476, "mean_day1_1999_pct": 71.2, "mean_day1_2000_pct": 56.4,
            "avg_day1_1990_98_pct": 14.8,
            "avg_1yr_return_pct": -11.2,
            "avg_3yr_bhr_from_close_pct": -53.1, "three_yr_mkt_adj_pct": -31.8,
            "implied_3yr_bhr_from_offer": "1999: -10.3% / 2000: -37.6% (computed: (1+FDR)x(1+BHR)-1)",
            "pct_below_offer_at_3yr": "56.1% - 1975-2021 AGGREGATE (Ritter Table 16e), not year-specific; 44.5% for large IPOs (sales >= $100M); 57.0% at +5yr. Year-specific 1999-2000 figure requires IPOALL.xlsx and is likely well above 56%",
            "money_left_on_table_usd": 66790000000,
            "note": "1999-2000 market-adjusted -31.8% is the single worst cohort sub-period in the 44-year dataset. Ex-bubble, tech IPOs BEAT style benchmarks (+46.0% 3yr style-adj 1980-2023) - the bubble reverses the sign.",
            "source_url": "https://site.warrington.ufl.edu/ritter/ipo-data/",
            "conflict_note": "(#7) 1999 IPO count: 476 (Ritter) vs 457 (definitional).",
            "as_of": AS_OF,
        },
        {
            "cohort": "2020-21 IPO/SPAC wave",
            "spac_ipos_2021": 613, "spac_proceeds_2021_usd": 144500000000,
            "operating_ipos_2021": 311, "mean_day1_2021_pct": 32.1,
            "despac_avg_1yr_mkt_adj_pct": -49.4, "despac_avg_3yr_mkt_adj_pct": -74.7,
            "despac_2021_cohort": "N=198: 1yr -64.2%, 3yr -73.0%",
            "redemption_rate": "68.4% avg 2017-2025 (rose from 11.3% Q1-2021 to ~93-97% by 2023)",
            "pct_above_offer_by_mar_2023": 5,
            "pct_above_offer_note": "approximate (~5%) of the 2020-21 IPO/SPAC class (v1 finding; Ritter deSPAC stats above are the primary numbers)",
            "source_url": "https://site.warrington.ufl.edu/ritter/files/IPOs-SPACs.pdf",
            "conflict_note": None,
            "as_of": AS_OF,
        },
        {
            "cohort": "2025-26 AI cohort",
            "n_ipos_2025": 90, "mean_day1_2025_pct": 29.3,
            "avg_day1_2025_ex_figma_circle_pct": 8,
            "money_left_on_table_2025_usd": 13110000000,
            "note": "Pops concentrated, not broad - unlike 1999. CoreWeave priced below range, flat day-1, +139% to Jun 2026 (-55% off peak; founders sold $2.3B). Figma +250% day-1 then -40% below offer. Cerebras +100.7% day-1 at ~65x sales, 86% UAE revenue concentration. Databricks ~$134B listing pending.",
            "source_url": "/docs/research/03-research-findings.md",
            "conflict_note": "Mean 2025 day-1: 29.3% (Ritter, N=90) vs 24% (ION, v1 doc) - different samples/definitions; Ritter shown as primary.",
            "as_of": AS_OF,
        },
    ]


def main():
    comps = json.loads(COMPS.read_text(encoding="utf-8"))
    comps["deals"] = deals()
    comps["tech_comps"] = tech_comps()
    comps["cohorts"] = cohorts()
    comps["analysis"] = analysis()
    # normalize any local doc link to the v2 findings (v1 docs are superseded)
    def normalize(node):
        if isinstance(node, dict):
            u = node.get("source_url")
            if isinstance(u, str) and u.startswith("/docs/") and u != FINDINGS:
                node["source_url"] = FINDINGS
            for v in node.values():
                normalize(v)
        elif isinstance(node, list):
            for v in node:
                normalize(v)
    normalize(comps)
    comps["_meta"]["status"] = "SEEDED from docs/research/ v2 drop (2026-06-10)"
    comps["_meta"]["note"] = ("Historical seed from docs/research/03-research-findings.md (v2) and comps.csv "
                              "(WP-4, EDGAR 424B4-derived, offer-price return basis). Conflicts #2, #3, #6 resolved in v2; "
                              "resolutions recorded in conflict_note fields. ETL never modifies seed fields; it only fills "
                              "etl_writable_fields. tech_comps day-1/+365d returns are vs offer price (verified, WP-4). "
                              "v1 valuations used a different share-count basis for some names (e.g. Airbnb $47B vs $86.5B "
                              "implied mktcap) - v2 CSV figures govern.")
    comps["_meta"]["conflict_9_table_note"] = ("Conflict #9 RESOLVED in v2: tech_comps day-1 and +365d returns are now "
                                                "offer-price-based from WP-4 (EDGAR 424B4 + finance data), verified. "
                                                "etl/refresh_prices.py recomputes vs-offer returns daily as a cross-check.")
    COMPS.write_text(json.dumps(comps, indent=2), encoding="utf-8")
    print(f"seeded: {len(comps['deals'])} deals, {len(comps['mega_ipos'])} mega, "
          f"{len(comps['tech_comps'])} tech comps, {len(comps['cohorts'])} cohorts")


if __name__ == "__main__":
    main()
