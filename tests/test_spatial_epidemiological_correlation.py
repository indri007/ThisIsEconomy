"""Unit tests for Spatial & Epidemiological Ground-Truthing Correlation Audit.
Validates Defect Resolution #7 for Scopus Q1 JCMC and ICS submissions.
"""

import json
import os
import pandas as pd
import pytest

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
CSV_PATH = os.path.join(RESULTS_DIR, "spatial_epidemiological_provincial_benchmark.csv")
JSON_PATH = os.path.join(RESULTS_DIR, "SPATIAL_EPIDEMIOLOGICAL_CORRELATION_REPORT.json")
MD_PATH = os.path.join(RESULTS_DIR, "SPATIAL_EPIDEMIOLOGICAL_CORRELATION_REPORT.md")


def test_spatial_epidemiological_files_exist():
    """Verify that all spatial audit outputs exist."""
    assert os.path.exists(CSV_PATH), f"Missing {CSV_PATH}"
    assert os.path.exists(JSON_PATH), f"Missing {JSON_PATH}"
    assert os.path.exists(MD_PATH), f"Missing {MD_PATH}"


def test_provincial_benchmark_completeness():
    """Verify that 10 administrative units are covered with accurate national totals."""
    df = pd.read_csv(CSV_PATH)
    assert len(df) == 10, f"Expected 10 benchmark jurisdictions, got {len(df)}"
    
    # Ground truth national totals
    assert df["suspended_sppg_kitchens"].sum() == 4581
    assert df["hospitalized_students_count"].sum() == 3420


def test_java_macro_concentration():
    """Verify that physical failures and digital discourse are concentrated in Java Island."""
    df = pd.read_csv(CSV_PATH)
    java_df = df[df["island_classification"] == "Java Island Core"]
    
    java_sppg_share = (java_df["suspended_sppg_kitchens"].sum() / 4581) * 100
    java_hosp_share = (java_df["hospitalized_students_count"].sum() / 3420) * 100
    java_posts_share = (java_df["regional_posts_volume"].sum() / df["regional_posts_volume"].sum()) * 100

    assert java_sppg_share > 95.0, f"Java SPPG share should be > 95%, got {java_sppg_share:.1f}%"
    assert java_hosp_share > 95.0, f"Java hospitalization share should be > 95%, got {java_hosp_share:.1f}%"
    assert java_posts_share > 75.0, f"Java posts share should be > 75%, got {java_posts_share:.1f}%"


def test_west_java_primary_epicenter():
    """Verify West Java (Jawa Barat) is the primary physical disaster epicenter."""
    df = pd.read_csv(CSV_PATH)
    jabar = df[df["province_name"] == "Jawa Barat"].iloc[0]
    
    # Jabar has highest hospitalizations (> 1,500) and highest suspended SPPGs (> 2,000)
    assert jabar["hospitalized_students_count"] == df["hospitalized_students_count"].max()
    assert jabar["suspended_sppg_kitchens"] == df["suspended_sppg_kitchens"].max()
    assert jabar["hospitalized_students_count"] >= 1600
    assert jabar["suspended_sppg_kitchens"] >= 2000


def test_spearman_rank_correlation_significance():
    """Verify statistically significant positive monotonic rank correlation (rho > 0.65, p < 0.05)."""
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    metrics = data["statistical_correlation_metrics"]
    hosp_metrics = metrics["posts_volume_vs_hospitalized_students"]
    sppg_metrics = metrics["posts_volume_vs_suspended_sppg_kitchens"]
    
    assert hosp_metrics["spearman_rho"] > 0.65
    assert hosp_metrics["spearman_p_value"] < 0.05
    assert sppg_metrics["spearman_rho"] > 0.65
    assert sppg_metrics["spearman_p_value"] < 0.05
