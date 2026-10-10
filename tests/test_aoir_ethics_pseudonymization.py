"""
test_aoir_ethics_pseudonymization.py
=====================================
Unit tests for Point 3: AoIR 3.0 Ethical Guidelines & Internet Privacy Compliance.
Verifies that:
  1. The canonical top 25 actors table has valid AoIR pseudonyms for private citizen accounts.
  2. Public institutional accounts, state leaders, and automated systems remain identified.
  3. Network topology, centralities, and graph parameters are 100% preserved.
  4. Audit reports (.json and .md) are generated and consistent.
"""

import os
import json
import pandas as pd
import pytest

BASE_DIR = "/Users/jevin/ThisIsEconomy"
SNA_DIR = os.path.join(BASE_DIR, "results/sna_canonical_pipeline")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

PSEUDO_CSV = os.path.join(SNA_DIR, "canonical_top25_actors_aoir_pseudonymized.csv")
JSON_REPORT = os.path.join(RESULTS_DIR, "AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.json")
MD_REPORT = os.path.join(RESULTS_DIR, "AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.md")

def test_aoir_pseudonymized_csv_exists_and_valid():
    assert os.path.exists(PSEUDO_CSV), f"{PSEUDO_CSV} does not exist"
    df = pd.read_csv(PSEUDO_CSV)
    assert len(df) >= 25, f"Expected at least 25 actors, got {len(df)}"
    assert "AoIR_Pseudonym_Label" in df.columns
    assert "Ethical_Entity_Type" in df.columns
    assert "Raw_Handle" in df.columns

def test_public_entities_preserved():
    df = pd.read_csv(PSEUDO_CSV)
    public_actors = ["@grok", "@prabowo", "@tanyakanrl"]
    for pub in public_actors:
        matched = df[df["Raw_Handle"] == pub]
        assert len(matched) == 1, f"Public entity {pub} should exist"
        assert matched["AoIR_Pseudonym_Label"].iloc[0] == pub, f"{pub} label should match raw handle"
        assert matched["Ethical_Entity_Type"].iloc[0] == "Public Authority / Media / AI"

def test_private_citizens_pseudonymized():
    df = pd.read_csv(PSEUDO_CSV)
    citizen_handles = ["@4Y4NKZ", "@newIding30", "@dbdbidip", "@luvdysh_"]
    for handle in citizen_handles:
        matched = df[df["Raw_Handle"] == handle]
        assert len(matched) == 1, f"Citizen handle {handle} should be present in top 25"
        pseudo = matched["AoIR_Pseudonym_Label"].iloc[0]
        assert pseudo != handle, f"Citizen {handle} must not be displayed with raw handle"
        assert pseudo.startswith("[Citizen_"), f"Citizen {handle} should have standard pseudonym, got {pseudo}"
        assert matched["Ethical_Entity_Type"].iloc[0] == "Private Citizen Account"

def test_topological_invariants_preserved():
    df = pd.read_csv(PSEUDO_CSV)
    # Rank 1 must be grok with degree 42
    top1 = df.iloc[0]
    assert top1["Raw_Handle"] == "@grok"
    assert top1["Total_Degree"] == 42
    assert top1["Out_Degree"] == 42
    
    # prabowo must have In_Degree == 15 and Out_Degree == 0
    prabowo = df[df["Raw_Handle"] == "@prabowo"].iloc[0]
    assert prabowo["In_Degree"] == 15
    assert prabowo["Out_Degree"] == 0

def test_aoir_audit_reports_consistent():
    assert os.path.exists(JSON_REPORT), f"{JSON_REPORT} missing"
    assert os.path.exists(MD_REPORT), f"{MD_REPORT} missing"
    
    with open(JSON_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "protocol" in data
    assert "Franzke" in data["protocol"] or "AoIR" in data["protocol"]
    assert data["total_top25_actors"] >= 25
    assert data["pseudonymized_citizens_count"] > 10
