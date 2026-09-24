import os
import sys

PROJECT_ROOT = "/Users/jevin/Documents/tesis_mbg"

def get_data_path(filename):
    candidates = [
        os.path.join(PROJECT_ROOT, "data", filename),
        os.path.join(PROJECT_ROOT, "data", "sna", filename),
        os.path.join(PROJECT_ROOT, "data", "emotion", filename),
        os.path.join(PROJECT_ROOT, "data", "sarcasm", filename),
        os.path.join(PROJECT_ROOT, "data", "results", filename),
        os.path.join(PROJECT_ROOT, "results", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def get_result_path(filename):
    candidates = [
        os.path.join(PROJECT_ROOT, "results", filename),
        os.path.join(PROJECT_ROOT, "results", "storytelling", filename),
        os.path.join(PROJECT_ROOT, "data", "results", filename), 
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

files_to_check = {
    "data": ["indobert_9_emosi_fixed.csv", "network_edges.csv", "dataset_sindiran_valid.csv", "mbg_tweets_indobert_ready.xlsx", "sna_degree.csv"],
    "results": ["mbg_network_nodes_final.csv", "absa_results.csv", "sna_degree.csv", "classification_report.csv", "integrated_sna_nlp.png", "wordcloud_mbg.png", "10_absa_thematic.png", "keterbatasan_penelitian.png"]
}

missing = []

for cat, files in files_to_check.items():
    print(f"\n--- Checking {cat.upper()} files ---")
    for f in files:
        if cat == "data":
            path = get_data_path(f)
        else:
            path = get_result_path(f)
            
        if path:
            print(f"[OK] {f} -> {path}")
        else:
            print(f"[MISSING] {f}")
            missing.append(f)

if missing:
    sys.exit(1)
