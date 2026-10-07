"""
test_frontend_integrity.py
Unit tests verifying Frontend Next.js / React / Cytoscape configuration and assets.
"""

import unittest
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

class TestFrontendIntegrity(unittest.TestCase):

    def test_frontend_package_json_valid(self):
        pkg_file = FRONTEND_DIR / "package.json"
        self.assertTrue(pkg_file.exists(), "frontend/package.json must exist")
        with open(pkg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data.get("name"), "frontend")
        scripts = data.get("scripts", {})
        self.assertIn("build", scripts)
        self.assertIn("dev", scripts)

    def test_frontend_cytoscape_dependencies(self):
        pkg_file = FRONTEND_DIR / "package.json"
        with open(pkg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        deps = data.get("dependencies", {})
        self.assertIn("cytoscape", deps, "Cytoscape must be declared in frontend dependencies")
        self.assertIn("react-cytoscapejs", deps, "react-cytoscapejs must be declared")
        self.assertIn("next", deps, "Next.js must be declared")

    def test_frontend_tsconfig_valid(self):
        tsconfig_file = FRONTEND_DIR / "tsconfig.json"
        self.assertTrue(tsconfig_file.exists(), "tsconfig.json must exist")
        with open(tsconfig_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("compilerOptions", data)

if __name__ == "__main__":
    unittest.main()
