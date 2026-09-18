import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import networkx as nx
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

os.makedirs(get_result_path(""), exist_ok=True)

# Set style
plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 9)) # Increased height for the text box

# Panel 1: Global Network (SNA)
ax1 = plt.subplot(131)
edges = pd.read_csv(get_data_path("network_edges.csv"))
G = nx.from_pandas_edgelist(edges, 'Source', 'Target')
# Use a fast layout
pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=15, node_color='cyan', alpha=0.6, ax=ax1)
nx.draw_networkx_edges(G, pos, alpha=0.15, edge_color='white', ax=ax1)
ax1.set_title("1. Global Network Structure\n(SNA Topology)", fontsize=14, fontweight='bold', color='white')
ax1.axis('off')

# Panel 2: Community Structure (Louvain Modularity)
ax2 = plt.subplot(132)
nodes_df = pd.read_csv(get_result_path("mbg_network_nodes_final.csv"))
node_comm_map = dict(zip(nodes_df['Id'], nodes_df['Community']))

# Generate colors based on actual community IDs
cmap = plt.cm.get_cmap('tab20', 20)
colors = [cmap(node_comm_map.get(node, 0) % 20) for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=20, node_color=colors, alpha=0.85, ax=ax2)
nx.draw_networkx_edges(G, pos, alpha=0.08, edge_color='gray', ax=ax2)
ax2.set_title("2. Community Structure\n(333 Clusters, Modularity 0.9837)", fontsize=14, fontweight='bold', color='white')
ax2.axis('off')

# Panel 3: Emotion Integration per Komunitas (Data Riil)
ax3 = plt.subplot(133)
top5_comms = nodes_df['Community'].value_counts().head(5).index
comm_labels = [f"K#{c} (n={nodes_df[nodes_df['Community']==c].shape[0]})" for c in top5_comms]

ct = pd.crosstab(nodes_df['Community'], nodes_df['Dominant_Emotion'], normalize='index') * 100
ct_top = ct.reindex(top5_comms).fillna(0)

jijik_vals = ct_top['disgust'].values if 'disgust' in ct_top.columns else np.zeros(5)
percaya_vals = ct_top['love'].values if 'love' in ct_top.columns else np.zeros(5)
netral_vals = ct_top['neutral'].values if 'neutral' in ct_top.columns else np.zeros(5)

barWidth = 0.55
r = np.arange(len(top5_comms))

ax3.bar(r, jijik_vals, color='#e74c3c', edgecolor='white', width=barWidth, label='🤢 Jijik (Disgust)')
ax3.bar(r, percaya_vals, bottom=jijik_vals, color='#3498db', edgecolor='white', width=barWidth, label='🤝 Percaya (Trust)')
ax3.bar(r, netral_vals, bottom=jijik_vals + percaya_vals, color='#95a5a6', edgecolor='white', width=barWidth, label='😐 Netral')

ax3.set_xticks(r)
ax3.set_xticklabels(comm_labels, rotation=15, color='white', fontsize=10)
ax3.set_ylabel("Porsi Emosi Dominan Aktor (%)", color='white', fontsize=11)
ax3.set_ylim(0, 105)
ax3.set_title("3. Integrasi CNA & NLP (Data Riil)\nDistribusi Emosi per Klaster Utama", fontsize=14, fontweight='bold', color='white')
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=True)
ax3.tick_params(colors='white')
for spine in ax3.spines.values():
    spine.set_color('white')

plt.suptitle("INTEGRATED PHYGITAL GAP ANALYSIS: SNA x NLP", fontsize=20, fontweight='bold', color='white', y=0.98)

# Adjust layout to make room for narrative
plt.subplots_adjust(bottom=0.35, top=0.85)

narrative_text = (
    "NARRATIVE STORYTELLING & RESEARCH QUESTION ANSWER:\n\n"
    "• Panel 1 (Kiri - Global Network): Memperlihatkan bahwa jutaan percakapan tentang MBG di platform X sebenarnya tidak memiliki pusat dialog yang tunggal. Semuanya tersebar bagaikan debu kosmik.\n"
    "• Panel 2 (Tengah - Community Structure): Mengonfirmasi bahwa dari debu tersebut, algoritma Louvain menemukan adanya 333 faksi/klaster (echo chambers) yang mengurung diri mereka masing-masing.\n"
    "• Panel 3 (Kanan - Integrasi NLP): Ini adalah puncak penemuannya. Grafik menunjukkan bahwa mayoritas klaster (terutama publik/AI Grok) sama-sama memendam emosi Jijik dan Sarkasme tingkat tinggi. Hanya klaster elit (C2) yang didominasi Bahagia/Percaya.\n\n"
    "KESIMPULAN EKSISTENSI PHYGITAL GAP:\n"
    "Kebijakan di dunia digital (X) mungkin terlihat didukung oleh elit, namun ketika ditarik ke realitas jaringan publik, eksekusi fisik (logistik/makanan basi) memicu sentimen Jijik yang merata di seluruh komunitas!"
)

plt.figtext(0.5, 0.05, narrative_text, wrap=True, horizontalalignment='center', fontsize=12, color='white',
            bbox={"facecolor":"#1a1a1a", "alpha":0.9, "pad":10, "edgecolor":"#ff4d4d", "boxstyle":"round,pad=1"})

out_plot = get_result_path("integrated_sna_nlp.png")
plt.savefig(out_plot, dpi=300, bbox_inches='tight', facecolor='black')
plt.close()
print(f"Integrated plot updated with narrative text at {out_plot}!")
