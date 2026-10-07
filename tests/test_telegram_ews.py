"""
test_telegram_ews.py
Unit tests for Telegram EWS risk analyzer and notification alerting engine.
"""

import unittest
import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from auto_scrape_job import analyze_new_batch, send_telegram_ews_report

class TestTelegramEWSSystem(unittest.TestCase):

    def test_send_telegram_missing_token_graceful(self):
        # Without setting environment variables, send should return False gracefully
        dummy_summary = {
            "timestamp": "2026-10-07 19:00",
            "added_count": 10,
            "total_records": 100,
            "risk_level": "🟢 KONDUSIF",
            "top_keywords": "menu",
            "sample_tweet": "Menu bergizi hari ini",
            "action": "Pantau rutin"
        }
        res = send_telegram_ews_report(dummy_summary)
        self.assertFalse(res, "Missing credentials should gracefully return False without exception")

    def test_analyze_new_batch_medical_kritis(self):
        df_crisis = pd.DataFrame({
            "text": ["Ada 50 siswa mual dan muntah parah setelah makan siang MBG di sekolah", "Keracunan massal terjadi"]
        })
        res = analyze_new_batch(df_crisis)
        self.assertIn("KRITIS", res["risk_level"])
        self.assertIn("medis", res["action"].lower())

    def test_analyze_new_batch_hygiene_bahaya(self):
        df_hygiene = pd.DataFrame({
            "text": ["Makanan katering MBG hari ini basi dan ada ulat di dalam sayur", "Susu basi"]
        })
        res = analyze_new_batch(df_hygiene)
        self.assertIn("BAHAYA", res["risk_level"])
        self.assertIn("Higienitas", res["risk_level"])
        self.assertIn("audit", res["action"].lower())

    def test_analyze_new_batch_normal_kondusif(self):
        df_normal = pd.DataFrame({
            "text": ["Anak-anak senang mendapatkan makanan sehat hari ini", "Program berjalan lancar di kelas"]
        })
        res = analyze_new_batch(df_normal)
        self.assertIn("KONDUSIF", res["risk_level"])

if __name__ == "__main__":
    unittest.main()
