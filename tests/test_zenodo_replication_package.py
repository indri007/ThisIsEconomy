"""
tests/test_zenodo_replication_package.py
================================================================================
Unit tests for Zenodo / OSF Permanent DOI Replication Package Integration:
Open Science FAIR data compliance, DataCite schema 4.4, CFF 1.2.0, and archive integrity.
================================================================================
"""

import os
import json
import zipfile
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZENODO_JSON_PATH = os.path.join(BASE_DIR, ".zenodo.json")
CITATION_CFF_PATH = os.path.join(BASE_DIR, "CITATION.cff")
REPLICATION_ZIP_PATH = os.path.join(BASE_DIR, "results", "ZENODO_REPLICATION_PACKAGE_DOI_MBG_2026.zip")
REPORT_JSON_PATH = os.path.join(BASE_DIR, "results", "ZENODO_PERMANENT_DOI_INTEGRATION_REPORT.json")
REPORT_MD_PATH = os.path.join(BASE_DIR, "results", "ZENODO_PERMANENT_DOI_INTEGRATION_REPORT.md")
GUIDE_MD_PATH = os.path.join(BASE_DIR, "docs", "ZENODO_GITHUB_INTEGRATION_GUIDE.md")
PAPER_MD_PATH = os.path.join(BASE_DIR, "journal_paper_mbg_sna.md")

DOI_TARGET = "10.5281/zenodo.11029482"
DOI_URL_TARGET = "https://doi.org/10.5281/zenodo.11029482"


def test_zenodo_metadata_json_schema():
    assert os.path.exists(ZENODO_JSON_PATH), f"Missing .zenodo.json: {ZENODO_JSON_PATH}"
    with open(ZENODO_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("upload_type") == "dataset"
    assert "Free Nutritious Meal (MBG)" in data.get("title", "")
    assert data.get("access_right") == "open"
    assert data.get("license") == "CC-BY-4.0"
    
    creators = data.get("creators", [])
    assert len(creators) == 3
    creator_names = [c["name"] for c in creators]
    assert any("Sari, Indri Anjar Kartika" in name for name in creator_names)
    assert any("Suratnoaji, Catur" in name for name in creator_names)
    assert any("Widiyarta, Agus" in name for name in creator_names)

    # Validate ORCIDs
    assert any(c.get("orcid") == "0009-0002-8419-7231" for c in creators)
    assert any(c.get("orcid") == "0000-0002-8596-3914" for c in creators)
    assert any(c.get("orcid") == "0000-0002-7104-5820" for c in creators)

    # Keywords & relations
    assert len(data.get("keywords", [])) >= 5
    related = data.get("related_identifiers", [])
    assert any("github.com/indri007/ThisIsEconomy" in r.get("identifier", "") for r in related)


def test_citation_cff_metadata():
    assert os.path.exists(CITATION_CFF_PATH), f"Missing CITATION.cff: {CITATION_CFF_PATH}"
    with open(CITATION_CFF_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert DOI_TARGET in content
    assert DOI_URL_TARGET in content
    assert "Indri Anjar Kartika" in content
    assert "Suratnoaji" in content
    assert "Widiyarta" in content
    assert "0009-0002-8419-7231" in content


def test_zenodo_replication_archive_integrity():
    assert os.path.exists(REPLICATION_ZIP_PATH), f"Missing zip archive: {REPLICATION_ZIP_PATH}"
    size_mb = os.path.getsize(REPLICATION_ZIP_PATH) / (1024 * 1024)
    assert size_mb > 1.0, f"Zip file size ({size_mb:.2f} MB) is smaller than expected 1 MB"

    with zipfile.ZipFile(REPLICATION_ZIP_PATH, "r") as z:
        file_list = z.namelist()
        assert len(file_list) >= 20, f"Archive has too few files: {len(file_list)}"

        # Check critical benchmark datasets
        assert any("multi_annotator_batch_100_GOLD.csv" in f for f in file_list)
        assert any("canonical_macro_topology_metrics.csv" in f for f in file_list)
        assert any("dynamic_temporal_network_phases.csv" in f for f in file_list)
        assert any("spatial_epidemiological_provincial_benchmark.csv" in f for f in file_list)
        assert any("absa_aspect_category_token_benchmark.csv" in f for f in file_list)

        # Check script & docs
        assert any("run_absa_acsa_span_audit.py" in f for f in file_list)
        assert any("run_spatial_epidemiological_audit.py" in f for f in file_list)
        assert any("README.md" in f for f in file_list)
        assert any(".zenodo.json" in f for f in file_list)
        assert any("CITATION.cff" in f for f in file_list)


def test_zenodo_integration_report_and_guide():
    assert os.path.exists(REPORT_JSON_PATH), f"Missing report JSON: {REPORT_JSON_PATH}"
    assert os.path.exists(REPORT_MD_PATH), f"Missing report MD: {REPORT_MD_PATH}"
    assert os.path.exists(GUIDE_MD_PATH), f"Missing guide: {GUIDE_MD_PATH}"

    with open(REPORT_JSON_PATH, "r", encoding="utf-8") as f:
        report = json.load(f)

    zenodo_meta = report.get("zenodo_integration", {})
    assert zenodo_meta.get("concept_doi") == DOI_TARGET
    assert zenodo_meta.get("doi_url") == DOI_URL_TARGET
    assert zenodo_meta.get("total_files", 0) >= 20

    compliance = zenodo_meta.get("compliance_standards", [])
    assert any("FAIR Data Principles" in c for c in compliance)
    assert any("DataCite Metadata Schema" in c for c in compliance)
    assert any("AoIR 3.0" in c for c in compliance)


def test_data_availability_statement_in_manuscript():
    with open(PAPER_MD_PATH, "r", encoding="utf-8") as f:
        paper_text = f.read()

    assert DOI_TARGET in paper_text
    assert DOI_URL_TARGET in paper_text
    assert "FAIR data principles" in paper_text
    assert "AoIR 3.0" in paper_text
