import copy
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("spacex", Path(__file__).resolve().parents[1] / "etl/refresh_spacex_context.py")
spacex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spacex)


def sample():
    start = int(datetime(2026, 6, 12, 13, 30, tzinfo=timezone.utc).timestamp())
    monday = int(datetime(2026, 6, 15, 13, 30, tzinfo=timezone.utc).timestamp())
    return {"chart": {"result": [{"meta": {"symbol": "SPCX", "longName": "Space Exploration Technologies Corp.",
        "instrumentType": "EQUITY", "currentTradingPeriod": {"regular": {"start": monday, "end": monday + 23400}}},
        "timestamp": [start, monday], "indicators": {"quote": [{"open": [150, 160], "high": [163, 180],
        "low": [149, 159], "close": [161, 175], "volume": [100, 120]}]}}]}}


class SpaceXRefreshTests(unittest.TestCase):
    def test_current_open_session_is_excluded(self):
        data = spacex.parse_chart(sample(), "SPCX", datetime(2026, 6, 15, 19, tzinfo=timezone.utc))
        self.assertEqual([p["date"] for p in data["series"]], ["2026-06-12"])

    def test_completed_session_included_after_buffer(self):
        data = spacex.parse_chart(sample(), "SPCX", datetime(2026, 6, 15, 20, 20, tzinfo=timezone.utc))
        self.assertEqual(data["last_close"], 175)

    def test_wrong_issuer_and_invalid_bars_are_rejected(self):
        for change in ("issuer", "range", "split"):
            data = copy.deepcopy(sample())
            result = data["chart"]["result"][0]
            if change == "issuer":
                result["meta"].update(longName="The SPAC and New Issue ETF", instrumentType="ETF")
            elif change == "range":
                result["indicators"]["quote"][0]["low"][0] = 200
            else:
                result["events"] = {"splits": {"one": {"splitRatio": "2:1"}}}
            with self.subTest(change=change), self.assertRaises(ValueError):
                spacex.parse_chart(data, "SPCX", datetime(2026, 6, 15, 21, tzinfo=timezone.utc))

    def test_download_failure_does_not_replace_cache(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "data").mkdir()
            cache = root / "data/prices.json"
            cache.write_text(json.dumps({"old": "keep"}), encoding="utf-8")
            before = cache.read_bytes()
            with patch.object(spacex, "ROOT", root), patch.object(spacex, "fetch", side_effect=ValueError("unavailable")):
                with self.assertRaises(ValueError):
                    spacex.main()
            self.assertEqual(cache.read_bytes(), before)

    def test_pipeline_can_defer_frontend_publication(self):
        fixture = spacex.parse_chart(sample(), "SPCX", datetime(2026, 6, 15, 21, tzinfo=timezone.utc))
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "data").mkdir()
            (root / "frontend/data").mkdir(parents=True)
            (root / "data/prices.json").write_text(json.dumps({"prices": {"SPCX": {"series": []}}}), encoding="utf-8")
            (root / "data/comps.json").write_text(json.dumps({"deals": [{"ticker": "SPCX", "offer_price_usd": 135}]}), encoding="utf-8")
            served = root / "frontend/data/prices.json"
            served.write_text('{"previous":true}', encoding="utf-8")
            with patch.object(spacex, "ROOT", root), patch.object(spacex, "fetch", return_value=fixture):
                self.assertEqual(spacex.main(sync_frontend=False), 0)
            self.assertEqual(served.read_text(encoding="utf-8"), '{"previous":true}')
            self.assertTrue((root / "data/spacex_market.json").exists())


if __name__ == "__main__":
    unittest.main()
