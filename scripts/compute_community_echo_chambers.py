"""
Script: compute_community_echo_chambers.py
Menjalankan Analisis Komprehensif Dimensi 3:
Partisi Komunitas & Deteksi Ruang Gema (Clustering & Echo Chambers Analysis)
Standar Resmi NodeXL Pro & NetworkX
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain

# Setup paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nodes_path = os.path.join(base_dir, "results", "mbg_network_nodes_final.csv")
edges_path = os.path.join(base_dir, "results", "mbg_network_edges_final.csv")

nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)

print("=" * 80)
print("ANALISIS DIMENSI 3: PARTISI KOMUNITAS & DETEKSI RUANG GEMA (ECHO CHAMBERS)")
print("STANDAR RESMI PUBLIKASI NODEXL PRO & NETWORKX")
print("=" * 80)

# Bangun graf tak berarah untuk partisi Louvain
G = nx.Graph()
for _, r in nodes_df.iterrows():
    nid = str(r['Id'])
    G.add_node(nid, label=str(r.get('Label', nid)), emotion=str(r.get('Dominant_Emotion', 'neutral')))

for _, r in edges_df.iterrows():
    G.add_edge(str(r['Source']), str(r['Target']))

# Partisi Louvain
partition = {str(r['Id']): int(r['Community']) for _, r in nodes_df.iterrows()}
modularity_q = community_louvain.modularity(partition, G)

# Ukuran Komunitas
comm_sizes = pd.Series(partition).value_counts()
num_communities = len(comm_sizes)

print(f"Total Komunitas Terdeteksi: {num_communities}")
print(f"Skor Modularitas Louvain (Q): {modularity_q:.4f} (Ambang Newman > 0.3)")

# Analisis Tepi Internal vs Eksternal (Segregasi Ruang Gema)
internal_edges = 0
external_edges = 0
edge_cross_details = []

for _, r in edges_df.iterrows():
    u = str(r['Source'])
    v = str(r['Target'])
    c_u = partition.get(u, -1)
    c_v = partition.get(v, -1)
    if c_u == c_v:
        internal_edges += 1
    else:
        external_edges += 1
        edge_cross_details.append((u, v, c_u, c_v))

total_edges = len(edges_df)
internal_pct = (internal_edges / total_edges) * 100
external_pct = (external_edges / total_edges) * 100

print(f"\n--- ANALISIS ISOLASI STRUKTURAL (ECHO CHAMBER METRICS) ---")
print(f"Total Tepi Interaksi            : {total_edges}")
print(f"Tepi Internal (Dalam Komunitas) : {internal_edges} ({internal_pct:.2f}%)")
print(f"Tepi Lintas-Batas (Bridge Edges): {external_edges} ({external_pct:.2f}%)")
print(f"Rasio Isolasi Komunitas         : {internal_pct:.2f}% (Tingkat Kedap Percakapan Ekstrem)")

# Analisis Komposisi Emosi di Top 6 Komunitas
fokus_map = {
    15: "Klaster Elit & Target Otoritas (@prabowo, @regar_op0sisi)",
    61: "Klaster AI Fact-Checking Oracle (@grok)",
    27: "Klaster Pengawasan Anggaran & Fiskal APBN",
    32: "Klaster Keluhan Logistik Fisik & Keracunan Menu",
    45: "Klaster Sosialisasi & Dukungan Kebijakan",
    12: "Klaster Perdebatan Implementasi Daerah"
}

top_comm_ids = comm_sizes.head(6).index.tolist()
comm_summary = []

for cid in top_comm_ids:
    c_nodes = [nid for nid, c in partition.items() if c == cid]
    c_df = nodes_df[nodes_df['Id'].astype(str).isin(c_nodes)]
    c_size = len(c_df)
    
    # Distribusi emosi
    emo_counts = c_df['Dominant_Emotion'].value_counts().to_dict()
    dominant_emo = c_df['Dominant_Emotion'].mode()[0] if not c_df.empty else 'neutral'
    
    # Top akun di klaster ini
    top_accs = c_df.sort_values(by='Degree', ascending=False)['Label'].head(3).tolist()
    top_accs_str = ", ".join(['@' + str(a) for a in top_accs])
    
    comm_summary.append({
        'Community_Id': int(cid),
        'Nama_Wacana': fokus_map.get(cid, f"Klaster Diskursus #{cid}"),
        'Jumlah_Aktor': int(c_size),
        'Persentase_Populasi': round((c_size / len(nodes_df)) * 100, 2),
        'Emosi_Dominan': dominant_emo,
        'Distribusi_Emosi': emo_counts,
        'Top_Aktor': top_accs_str
    })

print("\n--- RINGKASAN TOP KOMUNITAS WACANA MBG ---")
for cs in comm_summary:
    print(f"• Klaster #{cs['Community_Id']:>2} ({cs['Jumlah_Aktor']:>2} aktor, {cs['Persentase_Populasi']:>5.2f}%): {cs['Nama_Wacana']}")
    print(f"  Emosi Dominan : {cs['Emosi_Dominan'].upper()} | Top Aktor: {cs['Top_Aktor']}")

# Simpan CSV & JSON
out_json = os.path.join(base_dir, "results", "community_echo_chambers.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump({
        'modularity_q': modularity_q,
        'num_communities': num_communities,
        'total_edges': total_edges,
        'internal_edges': internal_edges,
        'internal_pct': internal_pct,
        'external_edges': external_edges,
        'external_pct': external_pct,
        'top_communities': comm_summary
    }, f, indent=2, ensure_ascii=False)

out_md = os.path.join(base_dir, "results", "community_echo_chambers_report.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# Laporan Analisis Dimensi 3: Partisi Komunitas & Deteksi Ruang Gema (SNA MBG)\n\n")
    f.write(f"- **Algoritma Klasterisasi:** Louvain Modularity Optimization (Blondel dkk., 2008)\n")
    f.write(f"- **Skor Modularitas ($Q$):** **{modularity_q:.4f}** (Ambang Batas Polarisasi $Q > 0,30$)\n")
    f.write(f"- **Total Komunitas Terbentuk:** {num_communities} kelompok wacana independen\n")
    f.write(f"- **Tepi Internal (Dalam Kelompok):** {internal_edges} ({internal_pct:.2f}%)\n")
    f.write(f"- **Tepi Eksternal (Lintas Kelompok):** {external_edges} ({external_pct:.2f}%)\n\n")
    f.write("### Tabel Ringkasan Komunitas Utama & Karakteristik Afektif\n\n")
    f.write("| Klaster | Label Tema Wacana | Aktor (|V|) | Emosi Dominan | Tokoh Kunci |\n")
    f.write("| :---: | :--- | :---: | :---: | :--- |\n")
    for cs in comm_summary:
        f.write(f"| **#{cs['Community_Id']}** | {cs['Nama_Wacana']} | {cs['Jumlah_Aktor']} ({cs['Persentase_Populasi']}%) | **{cs['Emosi_Dominan'].upper()}** | {cs['Top_Aktor']} |\n")

print(f"\nHasil Dimensi 3 tersimpan:\n1. {out_json}\n2. {out_md}")
