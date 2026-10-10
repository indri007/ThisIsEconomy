"""
Unit Test: test_canonical_sna_recalculation.py
Memverifikasi bahwa rekalkulasi metrik SNA dari 1 edge list kanonis
berjalan pada jalur terisolasi tanpa merusak baseline tesis.
"""

import os
import json
import unittest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestCanonicalSNARecalculation(unittest.TestCase):
    def test_canonical_edge_list_integrity(self):
        edge_file = PROJECT_ROOT / "data" / "network_edges.csv"
        self.assertTrue(edge_file.exists(), "Berkas network_edges.csv harus ada")
        df = pd.read_csv(edge_file)
        self.assertEqual(len(df), 692, "Total baris interaksi mentah harus 692")
        unique_nodes = set(df['Source'].astype(str).str.strip()).union(set(df['Target'].astype(str).str.strip()))
        self.assertEqual(len(unique_nodes), 971, "Total simpul unik harus 971")
        unique_edges = len(df.drop_duplicates(subset=['Source', 'Target']))
        self.assertEqual(unique_edges, 666, "Total tepi berarah unik harus 666")

    def test_isolated_pipeline_outputs_exist_and_valid(self):
        out_dir = PROJECT_ROOT / "results" / "sna_canonical_pipeline"
        macro_json = out_dir / "canonical_macro_topology_metrics.json"
        macro_csv = out_dir / "canonical_macro_topology_metrics.csv"
        actors_csv = out_dir / "canonical_node_centralities.csv"
        report_md = out_dir / "CANONICAL_SNA_VERIFICATION_REPORT.md"

        self.assertTrue(macro_json.exists(), "canonical_macro_topology_metrics.json harus ada")
        self.assertTrue(macro_csv.exists(), "canonical_macro_topology_metrics.csv harus ada")
        self.assertTrue(actors_csv.exists(), "canonical_node_centralities.csv harus ada")
        self.assertTrue(report_md.exists(), "CANONICAL_SNA_VERIFICATION_REPORT.md harus ada")

        with open(macro_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        overview = data["network_overview"]
        self.assertEqual(overview["total_vertices_V"], 971)
        self.assertEqual(overview["total_raw_edges_E"], 692)
        self.assertEqual(overview["unique_directed_edges"], 666)

        dens = data["density_and_reciprocity"]
        self.assertAlmostEqual(dens["directed_density"], 0.000707, places=5)
        self.assertEqual(dens["reciprocity_percentage"], "1.20%")

        clust = data["clustering_and_structure"]
        self.assertAlmostEqual(clust["modularity_louvain_Q"], 0.9837, places=3)
        self.assertEqual(clust["total_louvain_communities"], 342)


if __name__ == "__main__":
    unittest.main()
