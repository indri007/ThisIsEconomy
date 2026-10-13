"""
Unit Test: test_human_annotation_validation.py
Memverifikasi validitas pengujian aktual anotasi manusia dan performa IndoBERT.
"""

import json
import unittest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestHumanAnnotationValidation(unittest.TestCase):
    def test_filled_human_annotation_file_exists_and_complete(self):
        filled_file = PROJECT_ROOT / "data" / "annotation" / "researcher_batch_100_FILLED.csv"
        self.assertTrue(filled_file.exists(), "Berkas researcher_batch_100_FILLED.csv harus ada")
        df = pd.read_csv(filled_file)
        self.assertEqual(len(df), 100, "Harus berisi tepat 100 sampel tweet beranotasi")
        self.assertEqual(df["researcher_label"].isnull().sum(), 0, "Semua baris harus memiliki label pakar manusia")
        self.assertEqual(df["confidence_1to5"].isnull().sum(), 0, "Semua baris harus memiliki skor keyakinan")

    def test_actual_human_validation_report_metrics(self):
        rep_json = PROJECT_ROOT / "results" / "INDOBERT_ACTUAL_HUMAN_VALIDATION_REPORT.json"
        self.assertTrue(rep_json.exists(), "INDOBERT_ACTUAL_HUMAN_VALIDATION_REPORT.json harus ada")
        with open(rep_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Cek evaluasi holdout test set (n=1.058)
        test_eval = data["holdout_v2_vs_silver"]
        self.assertEqual(test_eval["n"], 1058)
        self.assertAlmostEqual(test_eval["accuracy"], 0.7599, places=3)
        self.assertAlmostEqual(test_eval["macro_f1"], 0.4535, places=3)
        self.assertAlmostEqual(test_eval["weighted_f1"], 0.7434, places=3)

        # Cek status penarikan klaim anotasi manusia (Option A)
        human_status = data["human_annotation"]
        self.assertEqual(human_status["status"], "not_available")
        self.assertIn("withdrawn", human_status["note"])


if __name__ == "__main__":
    unittest.main()
