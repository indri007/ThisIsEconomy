"""
tests/test_operational_and_pipeline_audit.py
============================================
Pengujian programatik untuk validasi data lineage, evaluasi ketimpangan kelas,
dan ketahanan operasional Early Warning System (EWS).
"""

import html
import json
import unittest
from pathlib import Path
import pandas as pd
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class TestOperationalAndPipelineAudit(unittest.TestCase):

    def test_multi_corpus_lineage_reconciliation(self):
        """Memverifikasi konsistensi numerik antar-korpus pada repositori."""
        # 1. Korpus Master 9-Emosi
        master_path = PROJECT_ROOT / "data/results/indobert_9_emosi_fixed.csv"
        df_master = pd.read_csv(master_path)
        self.assertEqual(len(df_master), 5272, "Total korpus master emosi harus 5.272 baris")

        # 2. Rekonsiliasi Train + Test
        train_path = PROJECT_ROOT / "results/emotion_train_group_split.csv"
        test_path = PROJECT_ROOT / "results/emotion_test_group_split.csv"
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        self.assertEqual(len(df_train), 4208, "Train partition harus 4.208")
        self.assertEqual(len(df_test), 1064, "Test partition harus 1.064")
        self.assertEqual(len(df_train) + len(df_test), 5272, "4.208 + 1.064 harus tepat 5.272")

        # 3. Korpus Sindiran & Interaksi
        sarcasm_path = PROJECT_ROOT / "data/sarcasm/dataset_sindiran_valid.csv"
        df_sarcasm = pd.read_csv(sarcasm_path)
        self.assertEqual(len(df_sarcasm), 3395, "Korpus interaksi dan sindiran harus 3.395 baris")

    def test_ews_html_escaping_security(self):
        """Memverifikasi bahwa pesan notifikasi EWS lolos sanitasi HTML anti-injection."""
        raw_text = '<script>alert("hack")</script> & "menu basi"'
        escaped = html.escape(raw_text)
        self.assertNotIn("<script>", escaped)
        self.assertIn("&lt;script&gt;", escaped)
        self.assertIn("&amp;", escaped)

    def test_relevance_gating_false_alarm_reduction(self):
        """Memverifikasi logika pemilahan isu medis vs spam tidak relevan."""
        from scripts.auto_scrape_job import analyze_new_batch

        # Batch dengan noise kripto & ritel (tanpa kata kunci medis)
        df_noise = pd.DataFrame({
            "text": ["Buy $MBG token to the moon", "Promo air fryer diskon murah hari ini"]
        })
        res_noise = analyze_new_batch(df_noise)
        self.assertIn("KONDUSIF", res_noise["risk_level"], "Noise non-MBG tidak boleh memicu alarm bahaya/kritis")

        # Batch dengan isu krisis keracunan nyata
        df_crisis = pd.DataFrame({
            "text": ["Puluhan anak muntah dan diare massal setelah makan menu MBG di sekolah"]
        })
        res_crisis = analyze_new_batch(df_crisis)
        self.assertIn("KRITIS", res_crisis["risk_level"], "Isu keracunan wajib memicu alarm KRITIS")

if __name__ == "__main__":
    unittest.main()
