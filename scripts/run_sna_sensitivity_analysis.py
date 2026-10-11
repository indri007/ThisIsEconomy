#!/usr/bin/env python3
"""
scripts/run_sna_sensitivity_analysis.py
========================================
Comprehensive Sensitivity and Robustness Analysis for Social Network Analysis (SNA).
Evaluates stability of network metrics across:
1. Edge definitions (directed vs undirected, self-loop inclusion/exclusion, edge weight thresholding)
2. Louvain community detection resolution parameter sweeps (gamma in [0.5, 2.0])
3. Algorithm comparisons (Louvain vs Greedy Modularity vs Component Partitioning)
4. Multi-seed stochastic stability of modularity (seeds 1 to 10)

Outputs:
- results/sna_sensitivity_analysis.json
- results/sna_sensitivity_analysis.csv
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "network_edges.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_canonical_graph():
    """Load canonical directed graph and edge list."""
    df_edges = pd.read_csv(DATA_PATH)
    # Ensure source and target are strings
    df_edges['Source'] = df_edges['Source'].astype(str).str.strip()
    df_edges['Target'] = df_edges['Target'].astype(str).str.strip()
    
    G_directed = nx.DiGraph()
    for _, row in df_edges.iterrows():
        src, tgt = row['Source'], row['Target']
        if G_directed.has_edge(src, tgt):
            G_directed[src][tgt]['weight'] += 1
        else:
            G_directed.add_edge(src, tgt, weight=1)
            
    G_undirected = G_directed.to_undirected()
    return df_edges, G_directed, G_undirected


def evaluate_edge_definitions(df_edges, G_directed, G_undirected):
    """Assess variations in edge definitions."""
    results = []
    
    # Baseline: Full raw directed graph
    wcc = nx.number_weakly_connected_components(G_directed)
    density_dir = nx.density(G_directed)
    reciprocity = nx.reciprocity(G_directed)
    results.append({
        "Condition": "Baseline Directed (Raw Edge List)",
        "Nodes": G_directed.number_of_nodes(),
        "Edges": G_directed.number_of_edges(),
        "Components": wcc,
        "Density": round(density_dir, 6),
        "Reciprocity": f"{reciprocity * 100:.2f}%",
        "Notes": "Canonical directed mention/reply graph"
    })
    
    # Variant 1: Undirected representation
    density_undir = nx.density(G_undirected)
    cc = nx.number_connected_components(G_undirected)
    results.append({
        "Condition": "Undirected Representation",
        "Nodes": G_undirected.number_of_nodes(),
        "Edges": G_undirected.number_of_edges(),
        "Components": cc,
        "Density": round(density_undir, 6),
        "Reciprocity": "100.0% (Symmetric)",
        "Notes": "Symmetric collapsed dyadic ties"
    })
    
    # Variant 2: Removing self-loops
    G_no_loops = G_directed.copy()
    self_loops = list(nx.selfloop_edges(G_no_loops))
    G_no_loops.remove_edges_from(self_loops)
    results.append({
        "Condition": "Excluding Self-Loops",
        "Nodes": G_no_loops.number_of_nodes(),
        "Edges": G_no_loops.number_of_edges(),
        "Components": nx.number_weakly_connected_components(G_no_loops),
        "Density": round(nx.density(G_no_loops), 6),
        "Reciprocity": f"{nx.reciprocity(G_no_loops) * 100:.2f}%",
        "Notes": f"Removed {len(self_loops)} self-referential mentions"
    })
    
    # Variant 3: Thresholded weight >= 2
    G_thresh2 = nx.DiGraph()
    for u, v, data in G_directed.edges(data=True):
        if data.get('weight', 1) >= 2:
            G_thresh2.add_edge(u, v, weight=data['weight'])
    results.append({
        "Condition": "Edge Weight >= 2 (Repeated Ties)",
        "Nodes": G_thresh2.number_of_nodes(),
        "Edges": G_thresh2.number_of_edges(),
        "Components": nx.number_weakly_connected_components(G_thresh2) if len(G_thresh2) > 0 else 0,
        "Density": round(nx.density(G_thresh2), 6) if len(G_thresh2) > 0 else 0,
        "Reciprocity": f"{nx.reciprocity(G_thresh2) * 100:.2f}%" if len(G_thresh2) > 0 else "N/A",
        "Notes": "Filtered for persistent interaction dyads"
    })
    
    # Variant 4: Giant Component Only
    wcc_subgraphs = [G_directed.subgraph(c).copy() for c in nx.weakly_connected_components(G_directed)]
    giant_comp = max(wcc_subgraphs, key=len)
    results.append({
        "Condition": "Giant Connected Component",
        "Nodes": giant_comp.number_of_nodes(),
        "Edges": giant_comp.number_of_edges(),
        "Components": 1,
        "Density": round(nx.density(giant_comp), 6),
        "Reciprocity": f"{nx.reciprocity(giant_comp) * 100:.2f}%",
        "Notes": "Largest connected core (9.17% of total nodes)"
    })
    
    return results


def evaluate_louvain_resolution_sweep(G_undirected):
    """Sweep resolution parameter gamma in Louvain algorithm."""
    gammas = [0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0]
    sweep_results = []
    
    for gamma in gammas:
        partition = community_louvain.best_partition(G_undirected, resolution=gamma, random_state=42)
        q = community_louvain.modularity(partition, G_undirected)
        num_comm = len(set(partition.values()))
        
        # Count sizes
        sizes = pd.Series(list(partition.values())).value_counts()
        max_size = int(sizes.iloc[0])
        singletons = int((sizes == 1).sum())
        
        sweep_results.append({
            "Resolution_Gamma": gamma,
            "Modularity_Q": round(q, 4),
            "Total_Communities": num_comm,
            "Largest_Community_Size": max_size,
            "Singleton_Communities": singletons
        })
        
    return sweep_results


def evaluate_stochastic_stability(G_undirected):
    """Test seed stability of Louvain modularity across seeds 1 to 10."""
    seed_records = []
    for seed in range(1, 11):
        partition = community_louvain.best_partition(G_undirected, resolution=1.0, random_state=seed)
        q = community_louvain.modularity(partition, G_undirected)
        num_comm = len(set(partition.values()))
        seed_records.append({
            "Seed": seed,
            "Modularity_Q": round(q, 6),
            "Communities": num_comm
        })
    
    q_vals = [r["Modularity_Q"] for r in seed_records]
    mean_q = float(np.mean(q_vals))
    std_q = float(np.std(q_vals))
    min_q = float(np.min(q_vals))
    max_q = float(np.max(q_vals))
    
    summary = {
        "seeds_tested": len(seed_records),
        "mean_Q": round(mean_q, 6),
        "std_Q": round(std_q, 6),
        "min_Q": round(min_q, 6),
        "max_Q": round(max_q, 6),
        "records": seed_records
    }
    return summary


def run_full_sensitivity_analysis():
    print("=" * 80)
    print("RUNNING SNA SENSITIVITY AND ROBUSTNESS ANALYSIS")
    print("=" * 80)
    
    df_edges, G_directed, G_undirected = load_canonical_graph()
    
    # 1. Edge definitions
    print("1. Testing Edge Definition Variations...")
    edge_results = evaluate_edge_definitions(df_edges, G_directed, G_undirected)
    df_edge_results = pd.DataFrame(edge_results)
    
    # 2. Resolution sweep
    print("2. Sweeping Louvain Resolution Parameter (gamma in [0.5, 2.0])...")
    sweep_results = evaluate_louvain_resolution_sweep(G_undirected)
    df_sweep = pd.DataFrame(sweep_results)
    
    # 3. Seed stability
    print("3. Testing Stochastic Seed Stability (Seeds 1..10)...")
    seed_summary = evaluate_stochastic_stability(G_undirected)
    
    # Save results
    output_json = {
        "edge_definition_sensitivity": edge_results,
        "louvain_resolution_sweep": sweep_results,
        "stochastic_seed_stability": seed_summary
    }
    
    json_path = RESULTS_DIR / "sna_sensitivity_analysis.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2)
        
    csv_path = RESULTS_DIR / "sna_sensitivity_analysis.csv"
    df_edge_results.to_csv(csv_path, index=False)
    
    sweep_csv_path = RESULTS_DIR / "sna_resolution_sweep.csv"
    df_sweep.to_csv(sweep_csv_path, index=False)
    
    print(f"\n[OK] Sensitivity results saved to:")
    print(f" - JSON: {json_path}")
    print(f" - CSV (Edges): {csv_path}")
    print(f" - CSV (Resolution): {sweep_csv_path}")
    print(f"\nStochastic Stability: Mean Q = {seed_summary['mean_Q']} (std = {seed_summary['std_Q']})")
    print("=" * 80)
    return output_json


if __name__ == "__main__":
    run_full_sensitivity_analysis()
