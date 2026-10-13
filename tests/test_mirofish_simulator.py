#!/usr/bin/env python3
"""
test_mirofish_simulator.py
==========================
Unit test untuk MiroFish-Lite Swarm Simulator.
Memverifikasi struktur persona, pemanggilan API/fallback, dan sintesis laporan.
"""

import unittest
from unittest.mock import patch
from scripts.mirofish_simulator.mirofish_engine import (
    MiroFishSwarmSimulator,
    AGENT_PERSONAS,
    check_ollama_status
)

class TestMiroFishSimulator(unittest.TestCase):
    def test_personas_structure_and_coverage(self):
        """Memverifikasi bahwa seluruh persona terdefinisi lengkap dengan emosi dan peran."""
        self.assertGreaterEqual(len(AGENT_PERSONAS), 5)
        clusters = set(p["base_emotion"] for p in AGENT_PERSONAS)
        self.assertIn("Disgust", clusters)
        self.assertIn("Trust", clusters)
        self.assertIn("Neutral", clusters)

        for p in AGENT_PERSONAS:
            self.assertTrue(p["handle"].startswith("@"))
            self.assertIn("cluster", p)
            self.assertIn("role_desc", p)

    @patch("scripts.mirofish_simulator.mirofish_engine.query_ollama")
    def test_simulation_pipeline_execution(self, mock_query):
        """Menguji eksekusi pipeline simulasi multi-round secara deterministik."""
        mock_query.return_value = '{"predicted_public_sentiment": "Positif", "dominant_projected_emotion": "Trust", "crisis_risk_level": "LOW", "key_friction_point": "Kesiapan logistik", "strategic_policy_recommendation": "Sosialisasi masif"}'
        
        sim = MiroFishSwarmSimulator(model="test-model")
        scenario = "Uji coba skenario tes simulasi"
        res = sim.run_simulation(scenario)

        self.assertEqual(res["scenario"], scenario)
        self.assertEqual(len(res["round_1_initial_reactions"]), len(AGENT_PERSONAS))
        self.assertGreaterEqual(len(res["round_2_interactions"]), 3)
        self.assertIn("synthesis_report", res)
        self.assertEqual(res["synthesis_report"]["crisis_risk_level"], "LOW")

if __name__ == "__main__":
    unittest.main()
