import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.data_utils import get_data_path, get_result_path

datasets_to_check = [
    ("IndoBERT Emotion (Processed/Fixed)", "indobert_9_emosi_fixed.csv", pd.read_csv),
    ("IndoBERT Emotion (Original)", "indobert_9_emosi.csv", pd.read_csv),
    ("Raw MBG Tweets Excel", "mbg_tweets_indobert_ready.xlsx", pd.read_excel),
    ("Sarcasm Dataset", "dataset_sindiran_valid.csv", pd.read_csv),
    ("SNA Network Edges", "network_edges.csv", pd.read_csv),
    ("SNA Degree Centrality", "sna_degree.csv", pd.read_csv),
    ("SNA Network Nodes Final", "mbg_network_nodes_final.csv", pd.read_csv),
    ("SNA Network Edges Final", "mbg_network_edges_final.csv", pd.read_csv),
    ("ABSA Results", "absa_results.csv", pd.read_csv),
]

print("=" * 60)
print("       LAPORAN AUDIT KETERSEDIAAN & AKSES DATASET")
print("=" * 60)

all_ok = True
for name, filename, loader in datasets_to_check:
    resolved_path = get_data_path(filename)
    exists = os.path.exists(resolved_path)
    if exists:
        try:
            df = loader(resolved_path)
            rows, cols = df.shape
            print(f"[OK] {name:<35} | Path: {os.path.relpath(resolved_path, PROJECT_ROOT):<35} | Baris: {rows:<6} | Kolom: {cols}")
        except Exception as e:
            all_ok = False
            print(f"[ERR] {name:<34} | Gagal dibaca: {e}")
    else:
        all_ok = False
        print(f"[FAIL] {name:<33} | File TIDAK DITEMUKAN di: {resolved_path}")

print("=" * 60)

results_to_check = [
    "network_graph.png",
    "integrated_sna_nlp.png",
    "confusion_matrix.png",
    "f1_scores.png",
    "emotion_distribution.png",
    "top_actors.png",
    "1_pipeline.png",
    "2_dataset_characteristics.png",
    "3_sarcasm.png",
    "6_global_network.png",
    "9_emotion_network.png",
    "10_absa_thematic.png",
    "keterbatasan_penelitian.png",
]

print("\n" + "=" * 60)
print("       LAPORAN AUDIT FILE VISUALISASI HASIL (RESULTS)")
print("=" * 60)
for r_file in results_to_check:
    p = get_result_path(r_file)
    if os.path.exists(p):
        size_kb = os.path.getsize(p) / 1024
        print(f"[OK] {r_file:<30} | {size_kb:>8.2f} KB | Path: {os.path.relpath(p, PROJECT_ROOT)}")
    else:
        all_ok = False
        print(f"[FAIL] {r_file:<28} | TIDAK DITEMUKAN")

print("=" * 60)
if all_ok:
    print("STATUS AKHIR: SEMUA DATASET DAN VISUALISASI SIAP DIAKSES 100%!")
else:
    print("STATUS AKHIR: ADA BEBERAPA FILE YANG PERLU DIPERIKSA.")
print("=" * 60)
