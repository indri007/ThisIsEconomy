"""
test_scopus_verifier.py
Unit tests for Scopus verification engine and credential resolution.
"""

import unittest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from scopus_verifier import load_env_credentials, verify_doi_via_elsevier

class TestScopusVerifier(unittest.TestCase):

    def test_load_env_credentials_structure(self):
        creds = load_env_credentials()
        self.assertIsInstance(creds, dict)
        self.assertIn("SCOPUS_API_KEY", creds)
        self.assertIn("SCOPUS_INST_TOKEN", creds)

    def test_verify_doi_missing_key_graceful(self):
        res = verify_doi_via_elsevier(doi="10.1016/j.chb.2025.108570", api_key="")
        self.assertIsNone(res, "Missing key should safely return None without throwing exception.")

    def test_verify_doi_empty_doi_graceful(self):
        res = verify_doi_via_elsevier(doi="", api_key="dummy_key")
        self.assertIsNone(res, "Empty DOI should safely return None without throwing exception.")

if __name__ == "__main__":
    unittest.main()
