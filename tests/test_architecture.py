import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestMonorepoArchitecture(unittest.TestCase):
    def test_architecture_doc_exists(self):
        arch_path = os.path.join(PROJECT_ROOT, "ARCHITECTURE.md")
        self.assertTrue(os.path.exists(arch_path), "Missing ARCHITECTURE.md specification")
        self.assertGreater(os.path.getsize(arch_path), 500, "ARCHITECTURE.md should be comprehensive")

    def test_all_tiers_directories_exist(self):
        tiers = {
            "Tier 1 (Dashboard)": os.path.join(PROJECT_ROOT, "dashboard"),
            "Tier 2 (Backend)": os.path.join(PROJECT_ROOT, "backend"),
            "Tier 3 (Frontend)": os.path.join(PROJECT_ROOT, "frontend"),
            "Tier 4 (Scraper)": os.path.join(PROJECT_ROOT, "twitter_sentiment_app"),
        }
        for tier_name, dir_path in tiers.items():
            with self.subTest(tier=tier_name):
                self.assertTrue(os.path.isdir(dir_path), f"Missing tier directory: {dir_path}")

    def test_frontend_has_custom_readme(self):
        f_readme = os.path.join(PROJECT_ROOT, "frontend", "README.md")
        self.assertTrue(os.path.exists(f_readme))
        with open(f_readme, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Cytoscape", content, "Frontend README should document Cytoscape Explorer")
        self.assertNotIn("bootstrapped with create-next-app", content, "Boilerplate should be replaced")


if __name__ == "__main__":
    unittest.main()
