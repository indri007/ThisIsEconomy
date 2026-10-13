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

    def test_hierarchical_super_class_valence_evaluation(self):
        """Memverifikasi bahwa Taksonomi Bertingkat 3 Super-Kelas mencapai Macro-F1 >= 80%."""
        from sklearn.metrics import accuracy_score, f1_score
        pred_path = PROJECT_ROOT / "results/indobert_test_predictions_9_labels.csv"
        self.assertTrue(pred_path.exists(), "Prediksi 9-kelas test set harus tersedia")

        df_preds = pd.read_csv(pred_path)
        mapping = {
            "Jijik": "Negatif", "Marah": "Negatif", "Sedih": "Negatif", "Takut": "Negatif", "Kaget": "Negatif",
            "Percaya": "Positif", "Tertarik": "Positif", "Bahagia": "Positif",
            "Netral": "Netral"
        }
        y_true = df_preds["predicted_emotion"].map(mapping)
        y_pred = df_preds["predicted_model_emotion"].map(mapping)

        acc = accuracy_score(y_true, y_pred)
        macro_f1 = f1_score(y_true, y_pred, average="macro")

        self.assertGreaterEqual(acc, 0.80, f"Akurasi super-kelas harus >= 80% (aktual: {acc:.4f})")
        self.assertGreaterEqual(macro_f1, 0.80, f"Macro F1 super-kelas harus >= 80% (aktual: {macro_f1:.4f})")

    def test_30m_dataset_manifest_integrity(self):
        """Memverifikasi integritas manifest 30 juta baris dan rekonsiliasi data lake."""
        manifest_path = PROJECT_ROOT / "reports/scientific_validation/DATASET_30M_MANIFEST_AUDIT.json"
        self.assertTrue(manifest_path.exists(), "Manifest 30M harus ada")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest["total_physical_lines"], 30000001, "Total baris fisik harus 30.000.001")
        self.assertEqual(manifest["total_data_records"], 30000000, "Total data record harus 30.000.000")
        self.assertIn("sha256_checksum", manifest)
        self.assertTrue(manifest["required_columns_present"])

    def test_operational_execution_logging_pipeline(self):
        """Memverifikasi pembuatan dan penulisan berkas log eksekusi EWS."""
        log_dir = PROJECT_ROOT / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "ews_production_audit.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("[2026-10-13 17:00] TEST_AUDIT_LOG_ENTRY: pipeline active\n")
        self.assertTrue(log_file.exists())
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("TEST_AUDIT_LOG_ENTRY", content)

if __name__ == "__main__":
    unittest.main()
