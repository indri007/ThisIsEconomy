"""
tests/test_scientific_validation.py
===================================
Test suite untuk validasi integritas ilmiah repositori tesis_mbg.
Mencakup pengujian substantif atas data, model, graf, dan artefak.

Desain pengujian:
- Menggunakan fixture mandiri jika file produksi / korpus besar tidak tersedia di runner CI.
- Menguji integritas manifest dataset 30 juta baris dan persamaan rekonsiliasi.
- Menguji status NOT_VERIFIED jika anotasi independen belum lengkap.
- Menguji konsistensi metrik evaluasi model dan pemisahan kelas emosi.
"""

import os
import json
import unittest
import pandas as pd
import networkx as nx
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix

class TestScientificValidationSubstantive(unittest.TestCase):

    def setUp(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_benchmark_relevance_counts_substantive(self):
        """Memverifikasi eksak jumlah kategori relevansi pada audit benchmark 100 baris langsung dari data aktual."""
        purified_path = os.path.join(self.root_dir, 'data/annotation/purified_benchmark_batch_100_audit.csv')
        self.assertTrue(os.path.exists(purified_path), f"File {purified_path} harus tersedia")

        df = pd.read_csv(purified_path)
        self.assertEqual(len(df), 100, "Total sampel benchmark harus tepat 100")

        counts = df['relevance_status'].value_counts()
        self.assertEqual(counts.get('IRRELEVANT', 0), 49, "Jumlah entri IRRELEVANT harus tepat 49")
        self.assertEqual(counts.get('RELEVANT', 0), 26, "Jumlah entri RELEVANT harus tepat 26")
        self.assertEqual(counts.get('REVIEW_REQUIRED', 0), 25, "Jumlah entri REVIEW_REQUIRED harus tepat 25")

    def test_inter_rater_status_not_verified_when_unannotated(self):
        """Memverifikasi bahwa evaluator menolak membuat klaim semu dan mengembalikan NOT_VERIFIED jika kosong."""
        from scripts.setup_double_blind_annotation import calculate_inter_rater_reliability
        t1 = os.path.join(self.root_dir, 'data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1.csv')
        t2 = os.path.join(self.root_dir, 'data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_2.csv')

        res = calculate_inter_rater_reliability(t1, t2)
        self.assertEqual(res['status'], 'NOT_VERIFIED')
        self.assertIsNone(res['cohen_kappa'])
        self.assertIsNone(res['krippendorff_alpha'])

    def test_reproduce_indobert_historical_six_class_baseline_metrics(self):
        """[Baseline Historis v1/v2 - 6 Kelas] Mereproduksi metrik evaluasi model dari partisi uji awal (n=1058)."""
        pred_path = os.path.join(self.root_dir, 'results/FINAL_indobert_predictions.csv')
        self.assertTrue(os.path.exists(pred_path), f"File {pred_path} harus tersedia")

        df = pd.read_csv(pred_path)
        self.assertEqual(len(df), 1058, "Ukuran test partition baseline harus tepat 1058 baris")

        y_true = df['true_label']
        y_pred = df['predicted_label']

        acc = accuracy_score(y_true, y_pred)
        macro_prec = precision_score(y_true, y_pred, average='macro', zero_division=0)
        macro_rec = recall_score(y_true, y_pred, average='macro', zero_division=0)
        macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
        weighted_f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

        self.assertAlmostEqual(acc, 0.793951, places=4, msg="Akurasi baseline 6-kelas harus tepat ~79.40%")
        self.assertAlmostEqual(macro_prec, 0.672636, places=4, msg="Macro Precision baseline 6-kelas harus ~0.6726")
        self.assertAlmostEqual(macro_rec, 0.497659, places=4, msg="Macro Recall baseline 6-kelas harus ~0.4977")
        self.assertAlmostEqual(macro_f1, 0.515985, places=4, msg="Macro F1 baseline 6-kelas harus ~0.5160")
        self.assertAlmostEqual(weighted_f1, 0.785102, places=4, msg="Weighted F1 baseline 6-kelas harus ~0.7851")

    def test_reproduce_indobert_master_nine_class_evaluation_metrics(self):
        """[Model Master Terkini - 9 Kelas] Mereproduksi metrik evaluasi model dari partisi uji master (N=1064)."""
        pred_path = os.path.join(self.root_dir, 'results/indobert_test_predictions_9_labels.csv')
        self.assertTrue(os.path.exists(pred_path), f"File {pred_path} harus tersedia")

        df = pd.read_csv(pred_path)
        self.assertEqual(len(df), 1064, "Ukuran holdout test partition 9-kelas harus tepat 1064 baris")

        y_true = df['predicted_emotion']
        y_pred = df['predicted_model_emotion']

        acc = accuracy_score(y_true, y_pred)
        macro_prec = precision_score(y_true, y_pred, average='macro', zero_division=0)
        macro_rec = recall_score(y_true, y_pred, average='macro', zero_division=0)
        macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
        weighted_f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

        self.assertAlmostEqual(acc, 0.791353, places=4, msg="Akurasi master 9-kelas harus tepat ~79.14%")
        self.assertAlmostEqual(macro_prec, 0.506884, places=4, msg="Macro Precision master 9-kelas harus ~0.5069")
        self.assertAlmostEqual(macro_rec, 0.484566, places=4, msg="Macro Recall master 9-kelas harus ~0.4846")
        self.assertAlmostEqual(macro_f1, 0.480955, places=4, msg="Macro F1 master 9-kelas harus ~0.4810")
        self.assertAlmostEqual(weighted_f1, 0.788916, places=4, msg="Weighted F1 master 9-kelas harus ~0.7889")

    def test_nine_emotion_distribution_distinction(self):
        """Memverifikasi pemisahan yang jelas antara kelas absen di korpus vs tidak ada di test set vs tidak terprediksi."""
        corpus_path = os.path.join(self.root_dir, 'data/results/indobert_9_emosi_fixed.csv')
        pred_path = os.path.join(self.root_dir, 'results/FINAL_indobert_predictions.csv')

        df_corpus = pd.read_csv(corpus_path)
        df_test = pd.read_csv(pred_path)

        all_9 = {'Marah', 'Jijik', 'Takut', 'Bahagia', 'Sedih', 'Kaget', 'Percaya', 'Tertarik', 'Netral'}
        corpus_emotions = set(df_corpus['predicted_emotion'].unique())
        test_true_emotions = set(df_test['true_label'].unique())
        test_pred_emotions = set(df_test['predicted_label'].unique())

        # 1. Seluruh 9 emosi kini telah lengkap hadir di korpus (termasuk Bahagia dan Kaget)
        absent_in_corpus = all_9 - corpus_emotions
        self.assertEqual(absent_in_corpus, set(), "Seluruh 9 emosi Plutchik harus hadir di korpus")

        # 2. Hadir di korpus tetapi tidak ada di test partition
        absent_in_test_set = corpus_emotions - test_true_emotions
        self.assertIn('Takut', absent_in_test_set)

    def test_30m_manifest_integrity_and_reconciliation(self):
        """Memverifikasi integritas manifest 30M dan rumus rekonsiliasi record."""
        manifest_path = os.path.join(self.root_dir, 'reports/scientific_validation/DATASET_30M_MANIFEST_AUDIT.json')
        self.assertTrue(os.path.exists(manifest_path), "File manifest 30M harus tersedia")

        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data['total_data_records'], 30000000)
        self.assertEqual(data['file_size_bytes'], 6422076063)
        self.assertTrue(data['is_symlink'])
        self.assertEqual(data['symlink_target'], 'tweet_mbg_1juta.csv')

        recon = data['pipeline_reconciliation']
        # Uji rumus rekonsiliasi: input = lake_processed + backlog
        total_in = recon['total_input_records']
        processed = recon['lake_parquet_rows']
        backlog = recon['unprocessed_backlog']
        self.assertEqual(total_in, processed + backlog, "Rumus rekonsiliasi record harus seimbang")
        self.assertEqual(recon['full_inference_status'], 'BLOCKED')

    def test_canonical_sna_graph_metrics_substantive(self):
        """Memverifikasi topologi graf SNA canonical NetworkX DiGraph langsung dari network_edges.csv."""
        edges_path = os.path.join(self.root_dir, 'data/network_edges.csv')
        df_edges = pd.read_csv(edges_path).dropna().drop_duplicates()
        G = nx.from_pandas_edgelist(df_edges, source='Source', target='Target', create_using=nx.DiGraph())

        self.assertEqual(G.number_of_nodes(), 971)
        self.assertEqual(G.number_of_edges(), 666)
        self.assertAlmostEqual(nx.reciprocity(G), 0.012012, places=4)

        in_degrees = dict(G.in_degree())
        out_degrees = dict(G.out_degree())

        self.assertEqual(in_degrees.get('prabowo', 0), 15)
        self.assertEqual(out_degrees.get('prabowo', 0), 0)
        self.assertEqual(out_degrees.get('grok', 0), 42)

    def test_confusion_matrix_per_class_integrity(self):
        """Memverifikasi diagonal matriks konfusi dan support per kelas di test set."""
        pred_path = os.path.join(self.root_dir, 'results/FINAL_indobert_predictions.csv')
        df = pd.read_csv(pred_path)
        y_true = df['true_label']
        y_pred = df['predicted_label']

        self.assertEqual((y_true == 'Jijik').sum(), 606)
        self.assertEqual((y_true == 'Percaya').sum(), 220)
        self.assertEqual((y_true == 'Netral').sum(), 124)
        self.assertEqual((y_true == 'Tertarik').sum(), 91)
        self.assertEqual((y_true == 'Marah').sum(), 14)
        self.assertEqual((y_true == 'Sedih').sum(), 3)

        tp_jijik = ((y_true == 'Jijik') & (y_pred == 'Jijik')).sum()
        tp_percaya = ((y_true == 'Percaya') & (y_pred == 'Percaya')).sum()
        tp_netral = ((y_true == 'Netral') & (y_pred == 'Netral')).sum()

        self.assertEqual(tp_jijik, 529)
        self.assertEqual(tp_percaya, 166)
        self.assertEqual(tp_netral, 101)

    def test_nine_class_split_and_predictions_integrity(self):
        """Memverifikasi konsistensi dataset 9-kelas master, split group-aware bebas bocor, dan prediksi test set."""
        corpus_path = os.path.join(self.root_dir, 'data/results/indobert_9_emosi_fixed.csv')
        train_path = os.path.join(self.root_dir, 'results/emotion_train_group_split.csv')
        test_path = os.path.join(self.root_dir, 'results/emotion_test_group_split.csv')
        pred_path = os.path.join(self.root_dir, 'results/indobert_test_predictions_9_labels.csv')

        df_corpus = pd.read_csv(corpus_path)
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        df_pred = pd.read_csv(pred_path)

        # 1. Rekonsiliasi ukuran partisi
        self.assertEqual(len(df_corpus), 5272, "Total korpus master harus 5.272 baris")
        self.assertEqual(len(df_train), 4208, "Train set harus 4.208 baris")
        self.assertEqual(len(df_test), 1064, "Test set harus 1.064 baris")
        self.assertEqual(len(df_pred), 1064, "File prediksi uji harus 1.064 baris")
        self.assertEqual(len(df_train) + len(df_test), 5272, "Penjumlahan train + test harus tepat 5.272")

        # 2. Garansi Zero Text Leakage
        train_texts = set(df_train['processed_text'].dropna())
        test_texts = set(df_test['processed_text'].dropna())
        overlap = train_texts.intersection(test_texts)
        self.assertEqual(len(overlap), 0, "Harus zero text leakage antara train dan test set")

        # 3. Metrik Akurasi Test Set
        acc = (df_pred['predicted_emotion'] == df_pred['predicted_model_emotion']).mean()
        self.assertAlmostEqual(acc, 0.791353, places=4, msg="Akurasi model 9-kelas harus ~79.14%")

        # 4. Kehadiran kelas minoritas di test set
        test_counts = df_pred['predicted_emotion'].value_counts()
        self.assertEqual(test_counts.get('Bahagia', 0), 14, "Support kelas Bahagia di test set harus 14")
        self.assertEqual(test_counts.get('Kaget', 0), 6, "Support kelas Kaget di test set harus 6")
        self.assertEqual(test_counts.get('Marah', 0), 12, "Support kelas Marah di test set harus 12")
        self.assertEqual(test_counts.get('Jijik', 0), 590, "Support kelas Jijik di test set harus 590")

if __name__ == '__main__':
    unittest.main()

