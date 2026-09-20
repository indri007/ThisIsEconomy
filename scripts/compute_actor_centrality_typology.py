"""
Script: compute_actor_centrality_typology.py
Menjalankan Analisis Komprehensif Dimensi 2:
Sentralitas Aktor & Tipologi Peran Komunikasi (Micro-Level Centralities & Role Typologies)
Standar Resmi NodeXL Pro & NetworkX
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import networkx as nx

# Setup paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nodes_path = os.path.join(base_dir, "results", "mbg_network_nodes_final.csv")
edges_path = os.path.join(base_dir, "results", "mbg_network_edges_final.csv")

nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)

print("=" * 80)
print("ANALISIS DIMENSI 2: SENTRALITAS AKTOR & TIPOLOGI PERAN KOMUNIKASI")
print("STANDAR RESMI PUBLIKASI NODEXL PRO & NETWORKX")
print("=" * 80)

# Bangun Graf Berarah dan Tak Berarah
G_dir = nx.DiGraph()
G_undir = nx.Graph()

for _, r in nodes_df.iterrows():
    nid = str(r['Id'])
    G_dir.add_node(nid, label=str(r.get('Label', nid)), community=int(r.get('Community', 0)), emotion=str(r.get('Dominant_Emotion', 'neutral')))
    G_undir.add_node(nid, label=str(r.get('Label', nid)), community=int(r.get('Community', 0)), emotion=str(r.get('Dominant_Emotion', 'neutral')))

for _, r in edges_df.iterrows():
    u = str(r['Source'])
    v = str(r['Target'])
    G_dir.add_edge(u, v)
    G_undir.add_edge(u, v)

# 1. Komputasi Berbagai Metrik Sentralitas Matematis
in_deg = dict(G_dir.in_degree())
out_deg = dict(G_dir.out_degree())
tot_deg = dict(G_undir.degree())
deg_cent = nx.degree_centrality(G_undir)
bet_cent = nx.betweenness_centrality(G_undir, normalized=True)
closeness_cent = nx.closeness_centrality(G_undir)
pagerank_cent = nx.pagerank(G_dir, alpha=0.85)

# 2. Pemetaan Tipologi Peran Komunikasi (Communication Role Typology)
# 4 Tipologi Utama:
# 1. Target Sink (In-Degree Dominan, Out-Degree = 0, Otoritas Pemerintah Penerima Keluhan)
# 2. Algorithmic Oracle (Total Degree Ekstrem Tinggi, Bot AI Pusat Verifikasi Data Anggaran)
# 3. Opinion Broker / Bridge (Betweenness Centrality Tinggi, Menjembatani Klaster Wacana)
# 4. Opinion Leader / Agregator (Kombinasi In-Degree & Out-Degree Aktif)
# 5. Peripheral Citizen (Partisipan Biasa Derajat Rendah)

actors_data = []
for n in G_undir.nodes():
    lbl = G_undir.nodes[n].get('label', n)
    comm = G_undir.nodes[n].get('community', 0)
    emo = G_undir.nodes[n].get('emotion', 'neutral')
    ind = in_deg.get(n, 0)
    outd = out_deg.get(n, 0)
    tot = tot_deg.get(n, 0)
    bw = bet_cent.get(n, 0.0)
    pr = pagerank_cent.get(n, 0.0)
    cls_c = closeness_cent.get(n, 0.0)
    
    # Penentuan Peran Komunikasi
    if lbl.lower() == 'grok':
        role = "Algorithmic Oracle (AI Fact-Checker)"
    elif lbl.lower() in ['prabowo', 'gibran_tweet', 'kemensosri', 'jokowi']:
        role = "Target Sink (Otoritas Kebijakan)"
    elif bw >= 0.0015 or (tot >= 4 and bw >= 0.0005):
        role = "Opinion Broker (Jembatan Diskursus)"
    elif ind >= 3 and outd == 0:
        role = "Target Sink (Akun Rujukan Keluhan)"
    elif outd >= 3 and ind <= 1:
        role = "Information Broadcaster (Penyebar Wacana)"
    elif tot >= 2:
        role = "Secondary Influencer (Akun Penggerak)"
    else:
        role = "Peripheral Citizen (Warganet Biasa)"
        
    actors_data.append({
        'Id': n,
        'Label': '@' + lbl,
        'Community': comm,
        'Dominant_Emotion': emo,
        'In_Degree': ind,
        'Out_Degree': outd,
        'Total_Degree': tot,
        'Normalized_Degree': round(deg_cent.get(n, 0.0), 6),
        'Betweenness_Centrality': round(bw, 6),
        'PageRank': round(pr, 6),
        'Closeness_Centrality': round(cls_c, 6),
        'Communication_Role': role
    })

df_actors = pd.DataFrame(actors_data)

# Top Aktor
top_tot = df_actors.sort_values(by='Total_Degree', ascending=False).head(15)
top_bw = df_actors.sort_values(by='Betweenness_Centrality', ascending=False).head(15)
top_in = df_actors.sort_values(by='In_Degree', ascending=False).head(10)

print("\n--- TABEL 4.3: 15 AKTOR DENGAN DERAJAT TOTAL TERTINGGI (TOP INFLUENTIAL ACTORS) ---")
print(top_tot[['Label', 'Total_Degree', 'In_Degree', 'Out_Degree', 'Betweenness_Centrality', 'Communication_Role']].to_string(index=False))

print("\n--- 10 AKUN DENGAN BETWEENNESS CENTRALITY TERTINGGI (OPINION BROKERS) ---")
print(top_bw[['Label', 'Betweenness_Centrality', 'Total_Degree', 'Communication_Role']].head(10).to_string(index=False))

print("\n--- DISTRIBUSI TIPOLOGI PERAN KOMUNIKASI (POPULASI N=971) ---")
role_counts = df_actors['Communication_Role'].value_counts()
for r, c in role_counts.items():
    pct = (c / len(df_actors)) * 100
    print(f"  • {r:<42} : {c:>3} akun ({pct:5.2f}%)")

# Simpan CSV & JSON
out_csv = os.path.join(base_dir, "results", "actor_centrality_typology.csv")
out_json = os.path.join(base_dir, "results", "actor_centrality_top15.json")
df_actors.to_csv(out_csv, index=False)

top_summary = {
    "top_total_degree": top_tot.to_dict(orient='records'),
    "top_in_degree": top_in.to_dict(orient='records'),
    "top_betweenness": top_bw.to_dict(orient='records'),
    "role_counts": role_counts.to_dict()
}
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(top_summary, f, indent=2, ensure_ascii=False)

print(f"\nHasil kalkulasi Dimensi 2 berhasil disimpan:\n1. {out_csv}\n2. {out_json}")
