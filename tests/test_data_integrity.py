import os
import unittest
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestDataIntegrity(unittest.TestCase):
    def test_essential_data_files_exist_and_non_empty(self):
        essential_data = [
            os.path.join(PROJECT_ROOT, "data", "indobert_9_emosi_fixed.csv"),
            os.path.join(PROJECT_ROOT, "data", "network_edges.csv"),
            os.path.join(PROJECT_ROOT, "data", "dataset_sindiran_valid.csv"),
            os.path.join(PROJECT_ROOT, "data", "mbg_tweets_indobert_ready.xlsx"),
            os.path.join(PROJECT_ROOT, "results", "sna_degree.csv"),
        ]
        for fpath in essential_data:
            with self.subTest(file=fpath):
                self.assertTrue(os.path.exists(fpath), f"Missing data file: {fpath}")
                self.assertGreater(os.path.getsize(fpath), 0, f"Empty data file (0-byte): {fpath}")

    def test_essential_result_files_exist_and_non_empty(self):
        essential_results = [
            os.path.join(PROJECT_ROOT, "results", "mbg_network_nodes_final.csv"),
            os.path.join(PROJECT_ROOT, "results", "absa_results.csv"),
            os.path.join(PROJECT_ROOT, "results", "classification_report.csv"),
            os.path.join(PROJECT_ROOT, "results", "integrated_sna_nlp.png"),
            os.path.join(PROJECT_ROOT, "results", "wordcloud_mbg.png"),
            os.path.join(PROJECT_ROOT, "results", "10_absa_thematic.png"),
            os.path.join(PROJECT_ROOT, "results", "keterbatasan_penelitian.png"),
        ]
        for fpath in essential_results:
            with self.subTest(file=fpath):
                self.assertTrue(os.path.exists(fpath), f"Missing result file: {fpath}")
                self.assertGreater(os.path.getsize(fpath), 0, f"Empty result file (0-byte): {fpath}")

    def test_network_edges_valid_format(self):
        edge_path = os.path.join(PROJECT_ROOT, "data", "network_edges.csv")
        df = pd.read_csv(edge_path)
        self.assertGreater(len(df), 100, "Network edges dataframe should contain rows")
        cols = [c.lower() for c in df.columns]
        self.assertTrue(
            ("source" in cols and "target" in cols) or ("vertex 1" in cols and "vertex 2" in cols) or ("from" in cols and "to" in cols),
            f"Edge file missing source/target columns: {df.columns.tolist()}"
        )


if __name__ == "__main__":
    unittest.main()
