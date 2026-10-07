import os
import sys
import unittest
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dashboard.modules.views_ews import compute_ews_local


class TestEWSEngine(unittest.TestCase):
    def test_compute_ews_local_empty_df(self):
        res = compute_ews_local(pd.DataFrame())
        self.assertEqual(res["score"], 0)
        self.assertIn("⚪", res["status"])

    def test_compute_ews_local_normal_data(self):
        df_normal = pd.DataFrame({
            "text": [
                "Program makan bergizi gratis ini sangat bagus dan bermanfaat untuk siswa",
                "Semoga program MBG berjalan lancar dan tepat sasaran",
                "Menu makan siang hari ini cukup baik dan sehat"
            ],
            "sentiment": ["positif", "positif", "netral"],
            "is_sarcasm": [False, False, False]
        })
        res = compute_ews_local(df_normal)
        self.assertIsInstance(res["score"], (int, float))
        self.assertLess(res["score"], 50)
        self.assertIn("color", res)
        self.assertIn("action", res)

    def test_compute_ews_local_crisis_data(self):
        df_crisis = pd.DataFrame({
            "text": [
                "Banyak anak keracunan dan dilarikan ke rumah sakit setelah makan siang MBG 🤮",
                "Makanan basi dan berbau busuk, anak-anak masuk RS darurat 🤡",
                "Korupsi anggaran SPPG menyebabkan makanan beracun dan siswa dirawat"
            ],
            "sentiment": ["negatif", "negatif", "negatif"],
            "is_sarcasm": [True, True, False]
        })
        res = compute_ews_local(df_crisis)
        self.assertGreaterEqual(res["score"], 50)
        self.assertIn("status", res)


if __name__ == "__main__":
    unittest.main()
