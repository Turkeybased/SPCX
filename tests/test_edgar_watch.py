"""Regression checks for issuer identity, filing URLs and outage behavior."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location("edgar", Path(__file__).resolve().parents[1] / "etl/edgar_watch.py")
edgar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edgar)


class EdgarWatchTests(unittest.TestCase):
    def test_cik_filings_sort_newest_and_link_primary_document(self):
        response = Mock()
        response.json.return_value = {"filings": {"recent": {
            "form": ["S-1", "S-1/A", "4"],
            "filingDate": ["2026-10-26", "2026-11-02", "2026-11-03"],
            "accessionNumber": ["0001628280-26-067168", "0001628280-26-068676", "0000000000-26-000000"],
            "primaryDocument": ["anthropicpbc-sx1.htm", "anthropicpbc-sx1ax1.htm", "form4.xml"],
        }}}
        with patch.object(edgar, "get_with_retry", return_value=response):
            results = edgar.issuer_filings(2130357)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["form"], "S-1/A")
        self.assertEqual(results[0]["url"], "https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm")

    def test_search_ignores_funds_and_uses_hit_id_for_document(self):
        def hit(name, cik):
            return {"_id": "0001628280-26-068676:prospectus.htm", "_source": {
                "display_names": [name], "ciks": [cik], "adsh": "0001628280-26-068676",
                "file_type": "S-1/A", "file_date": "2026-11-02"}}
        hits = [hit("OpenAI Investment Fund (CIK 0000000001)", "1"),
                hit("OpenAI Group PBC (CIK 0000000002)", "2")]
        with patch.object(edgar, "fts_search", return_value={"hits": {"hits": hits}}):
            results = edgar.search_issuer_filings({"name": "OpenAI", "query": '"OpenAI"', "forms": "S-1,S-1/A"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "https://www.sec.gov/Archives/edgar/data/2/000162828026068676/prospectus.htm")

    def test_outage_keeps_last_successful_public_observation(self):
        cached = {"generated_at": "2026-11-04", "companies": [{"name": "Anthropic",
            "status": "PUBLIC S-1 ON EDGAR", "public_s1": {"form": "S-1/A", "url": "https://example.org/filing"},
            "checked_at": "2026-11-04"}]}
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "filing_status.json"
            output.write_text(json.dumps(cached), encoding="utf-8")
            with patch.object(edgar, "OUT_PATH", output), \
                 patch.object(edgar, "issuer_filings", side_effect=RuntimeError("SEC unavailable")), \
                 patch.object(edgar, "search_issuer_filings", side_effect=RuntimeError("SEC unavailable")), \
                 patch.object(edgar.time, "sleep"):
                self.assertEqual(edgar.main(), 1)
            result = json.loads(output.read_text(encoding="utf-8"))["companies"][0]
        self.assertEqual(result["status"], "PUBLIC S-1 ON EDGAR")
        self.assertEqual(result["checked_at"], "2026-11-04")
        self.assertEqual(result["public_s1"], cached["companies"][0]["public_s1"])
        self.assertIn("refresh_error", result)


if __name__ == "__main__":
    unittest.main()
