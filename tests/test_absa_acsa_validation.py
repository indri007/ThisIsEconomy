"""
tests/test_absa_acsa_validation.py
================================================================================
Unit tests for Aspect-Based Sentiment Analysis (ABSA) Granularity Audit:
Aspect Category Sentiment Analysis (ACSA) vs. Span-Level Aspect Term Extraction (ATE)
================================================================================
"""

import os
import json
import pandas as pd
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
CSV_PATH = os.path.join(RESULTS_DIR, "absa_aspect_category_token_benchmark.csv")
JSON_PATH = os.path.join(RESULTS_DIR, "ABSA_ACSA_VS_SPAN_LEVEL_REPORT.json")
MD_PATH = os.path.join(RESULTS_DIR, "ABSA_ACSA_VS_SPAN_LEVEL_REPORT.md")

def test_absa_benchmark_files_exist():
    assert os.path.exists(CSV_PATH), f"Missing CSV: {CSV_PATH}"
    assert os.path.exists(JSON_PATH), f"Missing JSON: {JSON_PATH}"
    assert os.path.exists(MD_PATH), f"Missing MD: {MD_PATH}"
    assert os.path.getsize(CSV_PATH) > 0
    assert os.path.getsize(JSON_PATH) > 0
    assert os.path.getsize(MD_PATH) > 0

def test_absa_category_counts():
    df = pd.read_csv(CSV_PATH)
    assert len(df) == 4, f"Expected 4 rows (A1, A2, A3, ALL), got {len(df)}"
    
    a1_row = df[df["aspect_id"] == "A1"].iloc[0]
    a2_row = df[df["aspect_id"] == "A2"].iloc[0]
    a3_row = df[df["aspect_id"] == "A3"].iloc[0]
    all_row = df[df["aspect_id"] == "ALL"].iloc[0]
    
    assert a1_row["acsa_total_mentions"] == 535
    assert a2_row["acsa_total_mentions"] == 403
    assert a3_row["acsa_total_mentions"] == 1344
    assert all_row["acsa_total_mentions"] == 2282
    
    # Check sum
    assert (a1_row["acsa_total_mentions"] + a2_row["acsa_total_mentions"] + a3_row["acsa_total_mentions"]) == 2282

def test_absa_disgust_dominance():
    df = pd.read_csv(CSV_PATH)
    for _, row in df[df["aspect_id"] != "ALL"].iterrows():
        # Every policy aspect must exhibit disgust saturation > 70%
        assert row["acsa_disgust_pct"] > 70.0, f"{row['aspect_id']} disgust pct too low: {row['acsa_disgust_pct']}"
        assert row["acsa_trust_pct"] < 15.0, f"{row['aspect_id']} trust pct unexpectedly high: {row['acsa_trust_pct']}"

def test_absa_implicit_explicit_balance():
    df = pd.read_csv(CSV_PATH)
    for _, row in df.iterrows():
        total_pct = row["explicit_token_span_pct"] + row["implicit_aspect_expr_pct"]
        assert pytest.approx(total_pct, 0.1) == 100.0
        # Implicit expressions must exceed 35% in all dimensions
        assert row["implicit_aspect_expr_pct"] >= 35.0, f"Implicit pct unexpectedly low: {row['implicit_aspect_expr_pct']}"

def test_span_extraction_metrics():
    df = pd.read_csv(CSV_PATH)
    for _, row in df[df["aspect_id"] != "ALL"].iterrows():
        assert row["ate_span_precision"] > 0.80
        assert row["ate_span_recall"] > 0.80
        assert row["ate_span_f1"] > 0.80

def test_json_structure():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "audit_metadata" in data
    assert "acsa_empirical_findings" in data
    assert "granularity_and_span_metrics" in data
    assert "methodology_comparison" in data
    assert len(data["methodology_comparison"]) == 5
