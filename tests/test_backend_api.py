"""
test_backend_api.py
Unit tests verifying Tier 2 FastAPI Backend endpoints and service responses.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from main import app


class TestBackendAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_and_health_endpoints(self):
        res_root = self.client.get("/")
        self.assertEqual(res_root.status_code, 200)
        self.assertIn("message", res_root.json())

        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json().get("status"), "healthy")

    def test_sna_summary_endpoint(self):
        res = self.client.get("/api/sna/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        self.assertGreater(data["nodes"], 0)
        self.assertGreater(data["edges"], 0)

    def test_emotion_distribution_endpoint(self):
        res = self.client.get("/api/emotion-distribution")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("emotion", data[0])
        self.assertIn("count", data[0])

    def test_sarcasm_summary_endpoint(self):
        res = self.client.get("/api/sarcasm/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_tweets", data)
        self.assertIn("sarcastic_tweets", data)
        self.assertIn("sarcasm_percentage", data)
        self.assertGreater(data["total_tweets"], 0)

    def test_sna_communities_endpoint(self):
        res = self.client.get("/api/sna/communities")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_communities", data)
        self.assertIn("distribution", data)

    def test_absa_summary_endpoint(self):
        res = self.client.get("/api/absa/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("summary", data)
        self.assertIsInstance(data["summary"], list)
        self.assertGreater(len(data["summary"]), 0)

    def test_hashtag_and_emoji_summary(self):
        res_hash = self.client.get("/api/hashtag/summary")
        self.assertEqual(res_hash.status_code, 200)
        data_hash = res_hash.json()
        self.assertIn("top_hashtags", data_hash)

        res_emoji = self.client.get("/api/emoji/summary")
        self.assertEqual(res_emoji.status_code, 200)
        data_emoji = res_emoji.json()
        self.assertIn("top_emojis", data_emoji)


if __name__ == "__main__":
    unittest.main()
