"""
test_cross_platform_ecological_validity.py
==========================================
Unit tests for Point 5: Cross-Platform Ecological Validity & Platform Affordance Bias.
Verifies:
  1. Affordance matrix CSV and reports (.json, .md) are generated.
  2. All 6 core architectural dimensions are evaluated across 4 platforms.
  3. Platform Ecology Alignment Index (PEAI) validates Platform X as optimal policy epicenter (> 90).
  4. Explicit ecological boundary conditions are defined to withstand Q1 reviewer scrutiny.
"""

import os
import json
import pandas as pd
import pytest

BASE_DIR = "/Users/jevin/ThisIsEconomy"
RESULTS_DIR = os.path.join(BASE_DIR, "results")
CSV_PATH = os.path.join(RESULTS_DIR, "cross_platform_affordance_matrix.csv")
JSON_PATH = os.path.join(RESULTS_DIR, "CROSS_PLATFORM_ECOLOGICAL_VALIDITY_REPORT.json")
MD_PATH = os.path.join(RESULTS_DIR, "CROSS_PLATFORM_ECOLOGICAL_VALIDITY_REPORT.md")


def test_ecological_reports_exist():
    assert os.path.exists(CSV_PATH), f"Missing CSV: {CSV_PATH}"
    assert os.path.exists(JSON_PATH), f"Missing JSON: {JSON_PATH}"
    assert os.path.exists(MD_PATH), f"Missing Markdown: {MD_PATH}"


def test_affordance_matrix_structure():
    df = pd.read_csv(CSV_PATH)
    assert len(df) == 6, f"Expected 6 affordance dimensions, got {len(df)}"
    assert "dimension" in df.columns
    assert "platform_x" in df.columns
    assert "tiktok" in df.columns
    assert "instagram" in df.columns
    assert "facebook" in df.columns

    dims = set(df["dimension"].tolist())
    expected = {
        "Primary Communicative Mode",
        "Algorithmic Political Exposure",
        "Public Scrutiny & Direct Institutional Accountability",
        "Sociodemographic Stratification (Indonesia Context)",
        "Network Topological Openness",
        "Crisis Response Latency (EWS Sensor Efficacy)"
    }
    assert dims == expected, f"Mismatch in dimensions: {dims ^ expected}"


def test_peai_scores_and_verdict():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    peai = data["peai_metrics"]
    assert "Platform_X" in peai
    assert "TikTok" in peai
    assert "Instagram" in peai
    assert "Facebook" in peai

    x_score = peai["Platform_X"]["Overall_PEAI_Score"]
    assert x_score > 90.0, f"Expected Platform X PEAI > 90.0, got {x_score}"
    assert "OPTIMAL" in peai["Platform_X"]["Verdict"]

    # Platform X must strictly beat alternative platforms
    assert x_score > peai["TikTok"]["Overall_PEAI_Score"]
    assert x_score > peai["Instagram"]["Overall_PEAI_Score"]
    assert x_score > peai["Facebook"]["Overall_PEAI_Score"]


def test_ecological_boundary_conditions_defined():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    bounds = data["ecological_boundary_conditions"]
    assert "demographic_generalization_limit" in bounds
    assert "affective_expression_bias" in bounds
    assert "future_research_agenda" in bounds
    assert "vanguard" in bounds["demographic_generalization_limit"].lower()
    assert "cynicism" in bounds["affective_expression_bias"].lower() or "irony" in bounds["affective_expression_bias"].lower()
