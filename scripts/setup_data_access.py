import os
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_link(src_rel, dest_rel):
    src = os.path.join(PROJECT_ROOT, src_rel)
    dest = os.path.join(PROJECT_ROOT, dest_rel)
    if not os.path.exists(src):
        print(f"[SKIP] Source not found: {src_rel}")
        return
    # If symlink already exists, remove it first so we can ensure it is a portable relative symlink
    if os.path.islink(dest):
        os.remove(dest)
    elif os.path.exists(dest):
        print(f"[EXISTS] {dest_rel}")
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    rel_src = os.path.relpath(src, os.path.dirname(dest))
    try:
        os.symlink(rel_src, dest)
        print(f"[SYMLINK] {dest_rel} -> {rel_src}")
    except OSError:
        shutil.copy2(src, dest)
        print(f"[COPY] {dest_rel} -> {rel_src}")

# 1. Alias mbg_tweets_indobert_ready.xlsx directly in data/
ensure_link("data/emotion/mbg_tweets_indobert_ready.xlsx", "data/mbg_tweets_indobert_ready.xlsx")

# 2. Alias dataset_sindiran_valid.csv directly in data/
ensure_link("data/sarcasm/dataset_sindiran_valid.csv", "data/dataset_sindiran_valid.csv")

# 3. Alias network_edges.csv directly in data/
ensure_link("data/sna/network_edges.csv", "data/network_edges.csv")

# 4. Alias indobert_9_emosi_fixed.csv directly in data/
ensure_link("data/results/indobert_9_emosi_fixed.csv", "data/indobert_9_emosi_fixed.csv")

# 5. Alias absa_results.csv in data/results/ and data/
ensure_link("results/absa_results.csv", "data/results/absa_results.csv")
ensure_link("results/absa_results.csv", "data/absa_results.csv")

# 6. Alias mbg_network_nodes_final.csv and edges in data/results/
ensure_link("results/mbg_network_nodes_final.csv", "data/results/mbg_network_nodes_final.csv")
ensure_link("results/mbg_network_edges_final.csv", "data/results/mbg_network_edges_final.csv")

# 7. Alias sna_degree.csv in results/
ensure_link("data/results/sna_degree.csv", "results/sna_degree.csv")

print("Data access aliases and links successfully established!")
