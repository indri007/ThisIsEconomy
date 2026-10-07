"""
scopus_verifier.py
Module for verifying papers against Scopus / Elsevier API and SCImago journal catalog.
Reads SCOPUS_API_KEY from .env or environment variable.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)

# Base directory & path to .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

def load_env_credentials():
    """Load SCOPUS_API_KEY and SCOPUS_INST_TOKEN from .env if present."""
    creds = {
        "SCOPUS_API_KEY": os.environ.get("SCOPUS_API_KEY", ""),
        "SCOPUS_INST_TOKEN": os.environ.get("SCOPUS_INST_TOKEN", "")
    }
    if ENV_FILE.exists():
        try:
            with open(ENV_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k in creds and not creds[k]:
                            creds[k] = v
        except Exception as e:
            logger.warning(f"Failed to read .env file: {e}")
    return creds


def verify_doi_via_elsevier(doi: str, api_key: str, inst_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Query Elsevier Scopus Search API for a specific DOI.
    Returns metadata dict if found, or None if not indexed.
    """
    if not api_key or not doi:
        return None
        
    clean_doi = doi.strip()
    if clean_doi.startswith("http"):
        clean_doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", clean_doi)

    url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }
    if inst_token:
        headers["X-ELS-Insttoken"] = inst_token

    params = {
        "query": f'DOI("{clean_doi}")',
        "count": 1
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            search_res = data.get("search-results", {})
            total_results = int(search_res.get("opensearch:totalResults", 0))
            if total_results > 0 and "entry" in search_res and len(search_res["entry"]) > 0:
                entry = search_res["entry"][0]
                if "error" not in entry:
                    return {
                        "scopus_verified": True,
                        "eid": entry.get("eid", ""),
                        "publication_name": entry.get("prism:publicationName", ""),
                        "issn": entry.get("prism:issn", ""),
                        "cited_by_count": entry.get("citedby-count", 0),
                        "cover_date": entry.get("prism:coverDate", "")
                    }
        elif resp.status_code == 401:
            logger.error("[Scopus API] 401 Unauthorized: Periksa SCOPUS_API_KEY Anda.")
        elif resp.status_code == 429:
            logger.warning("[Scopus API] 429 Quota Exceeded / Rate limit.")
    except Exception as e:
        logger.error(f"[Scopus API] Connection error for DOI {doi}: {e}")

    return None
