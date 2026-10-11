"""
tests/test_sna_sensitivity_analysis.py
======================================
Automated verification of SNA Sensitivity Analysis pipeline and outputs.
"""

import os
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestSNASensitivityAnalysis(unittest.TestCase):
    def setUp(self):
        self.results_json = PROJECT_ROOT / "results" / "sna_sensitivity_analysis.json"
        self.results_csv = PROJECT_ROOT / "results" / "sna_sensitivity_analysis.csv"
        self.sweep_csv = PROJECT_ROOT / "results" / "sna_resolution_sweep.csv"

    def test_sensitivity_artifacts_exist(self):
        self.assertTrue(self.results_json.exists(), "sna_sensitivity_analysis.json must exist")
        self.assertTrue(self.results_csv.exists(), "sna_sensitivity_analysis.csv must exist")
        self.assertTrue(self.sweep_csv.exists(), "sna_resolution_sweep.csv must exist")

    def test_sensitivity_json_structure(self):
        with open(self.results_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("edge_definition_sensitivity", data)
        self.assertIn("louvain_resolution_sweep", data)
        self.assertIn("stochastic_seed_stability", data)

        # Check edge definition results
        edges_data = data["edge_definition_sensitivity"]
        self.assertGreaterEqual(len(edges_data), 4)
        baseline = edges_data[0]
        self.assertEqual(baseline["Nodes"], 971)
        self.assertEqual(baseline["Edges"], 666)
        self.assertEqual(baseline["Components"], 341)

        # Check resolution sweep
        sweep_data = data["louvain_resolution_sweep"]
        self.assertGreaterEqual(len(sweep_data), 5)
        for item in sweep_data:
            self.assertGreater(item["Modularity_Q"], 0.95)
            self.assertGreater(item["Total_Communities"], 300)

        # Check stability
        stability = data["stochastic_seed_stability"]
        self.assertEqual(stability["seeds_tested"], 10)
        self.assertLess(stability["std_Q"], 0.01)


if __name__ == "__main__":
    unittest.main()
