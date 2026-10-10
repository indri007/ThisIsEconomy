"""Unit tests for Dynamic Temporal Network Evolution, TERGM, and SAOM/SIENA modeling.
Validates Defect Resolution #6 for Scopus Q1 JCMC and ICS submissions.
"""

import json
import os
import pandas as pd
import pytest

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
CSV_PATH = os.path.join(RESULTS_DIR, "dynamic_temporal_network_phases.csv")
JSON_PATH = os.path.join(RESULTS_DIR, "DYNAMIC_TEMPORAL_NETWORK_REPORT.json")
MD_PATH = os.path.join(RESULTS_DIR, "DYNAMIC_TEMPORAL_NETWORK_REPORT.md")


def test_dynamic_temporal_files_exist():
    """Verify that all required dynamic network outputs are generated."""
    assert os.path.exists(CSV_PATH), f"Missing {CSV_PATH}"
    assert os.path.exists(JSON_PATH), f"Missing {JSON_PATH}"
    assert os.path.exists(MD_PATH), f"Missing {MD_PATH}"


def test_four_empirical_phases():
    """Verify that all 4 empirical phases of 2026 are modeled with correct ordering and volumes."""
    df = pd.read_csv(CSV_PATH)
    assert len(df) == 4, f"Expected 4 longitudinal phases, got {len(df)}"
    assert list(df["phase_id"]) == [1, 2, 3, 4]
    
    # Check post volume bounds and positive node counts
    assert df.loc[df["phase_id"] == 1, "posts_volume"].iloc[0] == 299
    assert df.loc[df["phase_id"] == 2, "posts_volume"].iloc[0] == 3379
    assert df.loc[df["phase_id"] == 3, "posts_volume"].iloc[0] == 619
    assert df.loc[df["phase_id"] == 4, "posts_volume"].iloc[0] == 4397


def test_phase_network_topology_metrics():
    """Verify topological integrity, sparsity, and community modularity across phases."""
    df = pd.read_csv(CSV_PATH)
    
    for _, row in df.iterrows():
        # Nodes and edges must be non-negative
        assert row["nodes_v"] > 0
        assert row["edges_e"] > 0
        # Directed density must be within (0, 1)
        assert 0 < row["network_density"] < 1.0
        # Reciprocity must be minimal (confirming deliberative deficit <= 2%)
        assert row["reciprocity_rate"] <= 0.02

    # Phase 2 (Peak I) must reflect canonical crisis fragmentation (Modularity Q ~ 0.97)
    p2 = df[df["phase_id"] == 2].iloc[0]
    assert p2["louvain_modularity_q"] > 0.95
    assert p2["nodes_v"] >= 950
    assert p2["edges_e"] >= 650


def test_hub_centrality_and_algorithmic_oracle():
    """Verify preferential attachment of state authority and emergence of algorithmic oracle."""
    df = pd.read_csv(CSV_PATH)
    p2 = df[df["phase_id"] == 2].iloc[0]
    
    # @prabowo in-degree reflects primary grievance sink
    assert p2["prabowo_in_degree"] >= 10
    # @grok out-degree reflects autonomous conversational arbitration
    assert p2["grok_out_degree"] >= 35


def test_tergm_and_saom_specifications():
    """Verify statistical parameters and substantive interpretations in JSON report."""
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "tergm_model" in data
    assert "saom_model" in data
    
    tergm = data["tergm_model"]
    params = {p["parameter"]: p for p in tergm["parameter_estimates"]}
    
    # Check essential parameter names
    assert any("Edge Density" in k for k in params)
    assert any("Dyadic Reciprocity" in k for k in params)
    assert any("In-Degree" in k for k in params)
    assert any("Algorithmic Oracle" in k for k in params)

    # Theoretical directions: Density negative (sparse), Popularity positive, Oracle activity positive
    density_param = next(p for k, p in params.items() if "Edge Density" in k)
    popularity_param = next(p for k, p in params.items() if "In-Degree" in k)
    oracle_param = next(p for k, p in params.items() if "Algorithmic Oracle" in k)
    recip_param = next(p for k, p in params.items() if "Dyadic Reciprocity" in k)

    assert density_param["estimate"] < 0
    assert popularity_param["estimate"] > 0
    assert oracle_param["estimate"] > 0
    assert "Not Significant" in recip_param["p_value"]
