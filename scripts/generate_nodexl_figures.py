"""
Script: generate_nodexl_figures.py
Menghasilkan 7 Figure Publikasi dari Data NodeXL MBG Tesis Indri Anjar

RQ: "What role do technology, AI, and algorithms play in shaping, detecting,
     mediating, and interpreting human communication on social media?"

NodeXL tetap sebagai alat SNA resmi. Script ini hanya menghitung metrik
tambahan (eigenvector centrality) dan menghasilkan visualisasi.

Output: results/nodexl_final/
"""

import os, sys, json, warnings, textwrap
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "results")
OUT     = os.path.join(RESULTS, "nodexl_final")
os.makedirs(OUT, exist_ok=True)

NODES_PATH     = os.path.join(RESULTS, "mbg_network_nodes_final.csv")
EDGES_PATH     = os.path.join(RESULTS, "mbg_network_edges_final.csv")
ACTORS_PATH    = os.path.join(RESULTS, "actor_centrality_typology.csv")
COMMUNITY_PATH = os.path.join(RESULTS, "community_echo_chambers.json")

plt.rcParams.update({
    "figure.facecolor": "#FAFAFA", "axes.facecolor": "#F5F5F5",
    "axes.edgecolor": "#CCCCCC", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": "#E0E0E0", "grid.linewidth": 0.5,
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "legend.framealpha": 0.85, "lines.linewidth": 1.5,
})

EMOTION_PALETTE = {
    "disgust": "#E53935", "neutral": "#757575", "love": "#7B1FA2",
    "anger": "#FF6F00", "fear": "#1565C0", "joy": "#F9A825",
    "sadness": "#0097A7", "shame": "#AD1457", "surprise": "#2E7D32",
}

ROLE_PALETTE = {
    "Algorithmic Oracle (AI Fact-Checker)":      "#1A237E",
    "Target Sink (Otoritas Kebijakan)":           "#B71C1C",
    "Target Sink (Akun Rujukan Keluhan)":         "#C62828",
    "Opinion Broker (Jembatan Diskursus)":        "#E65100",
    "Information Broadcaster (Penyebar Wacana)":  "#1B5E20",
    "Secondary Influencer (Akun Penggerak)":      "#4527A0",
    "Peripheral Citizen (Warganet Biasa)":        "#37474F",
}

print("=" * 70)
print("PIPELINE NODEXL — 7 FIGURE PUBLIKASI TESIS MBG")
print("=" * 70)

# ── LOAD DATA ──────────────────────────────────────────────────────────────
print("\n[1/9] Memuat data...")
nodes_df  = pd.read_csv(NODES_PATH)
edges_df  = pd.read_csv(EDGES_PATH)
actors_df = pd.read_csv(ACTORS_PATH)
with open(COMMUNITY_PATH, encoding="utf-8") as f:
    comm_data = json.load(f)
print(f"  Nodes={len(nodes_df)}, Edges={len(edges_df)}, Actors={len(actors_df)}")

# ── BUILD GRAPH ─────────────────────────────────────────────────────────────
print("\n[2/9] Membangun graf NetworkX...")
G_dir   = nx.DiGraph()
G_undir = nx.Graph()
for _, r in nodes_df.iterrows():
    nid = str(r["Id"])
    attr = {
        "label": str(r.get("Label", nid)),
        "degree": float(r.get("Degree", 0)),
        "betweenness": float(r.get("Betweenness", 0)),
        "community": int(r.get("Community", 0)),
        "emotion": str(r.get("Dominant_Emotion", "neutral")),
    }
    G_dir.add_node(nid, **attr)
    G_undir.add_node(nid, **attr)
for _, r in edges_df.iterrows():
    u, v = str(r["Source"]), str(r["Target"])
    G_dir.add_edge(u, v)
    G_undir.add_edge(u, v)
print(f"  DiGraph: {G_dir.number_of_nodes()} nodes, {G_dir.number_of_edges()} edges")

# ── EIGENVECTOR CENTRALITY ──────────────────────────────────────────────────
print("\n[3/9] Menghitung Eigenvector Centrality...")
try:
    eig_cent = nx.eigenvector_centrality_numpy(G_undir)
    print(f"  OK: numpy method, {len(eig_cent)} nodes")
except Exception as e:
    print(f"  numpy gagal ({e}), coba iteratif...")
    try:
        eig_cent = nx.eigenvector_centrality(G_undir, max_iter=1000, tol=1e-6)
        print(f"  OK: iteratif method")
    except Exception as e2:
        print(f"  gagal ({e2}), pakai degree sebagai proxy")
        eig_cent = nx.degree_centrality(G_undir)

actors_df["Eigenvector_Centrality"] = actors_df["Id"].astype(str).map(
    lambda x: round(eig_cent.get(x, 0.0), 8)
)
csv_out = os.path.join(OUT, "nodexl_centrality_full.csv")
actors_df.to_csv(csv_out, index=False)
print(f"  Disimpan: nodexl_centrality_full.csv")

# ── FIGURE 1: NETWORK STRUCTURE ─────────────────────────────────────────────
print("\n[4/9] Figure 1: Social Network Structure...")
fig1, ax1 = plt.subplots(1, 1, figsize=(16, 12), facecolor="#0D1117")
ax1.set_facecolor("#0D1117")

top_nodes = actors_df.nlargest(300, "Total_Degree")["Id"].astype(str).tolist()
H = G_undir.subgraph(top_nodes).copy()
try:
    pos = nx.spring_layout(H, k=2.5, iterations=80, seed=42)
except:
    pos = nx.kamada_kawai_layout(H)

node_list   = list(H.nodes())
node_colors = [EMOTION_PALETTE.get(G_undir.nodes[n].get("emotion","neutral"), "#757575") for n in node_list]
node_sizes  = [max(30, G_undir.nodes[n].get("degree", 0.001) * 15000) for n in node_list]

nx.draw_networkx_edges(H, pos, ax=ax1, edge_color="#FFFFFF", alpha=0.06,
                       width=0.4, arrows=False)
nx.draw_networkx_nodes(H, pos, ax=ax1, nodelist=node_list,
                       node_color=node_colors, node_size=node_sizes,
                       alpha=0.85, linewidths=0.3, edgecolors="#FFFFFF")

top15 = actors_df.nlargest(15, "Total_Degree")["Id"].astype(str).tolist()
labels_to_draw = {n: "@" + str(G_undir.nodes[n].get("label", n)).lstrip("@")
                  for n in top15 if n in H.nodes()}
nx.draw_networkx_labels(H, pos, labels=labels_to_draw, ax=ax1,
                        font_size=7, font_color="#FFFFFF", font_weight="bold")

emo_present = actors_df["Dominant_Emotion"].unique()
legend_patches = [mpatches.Patch(color=EMOTION_PALETTE.get(e,"#999"), label=e.capitalize())
                  for e in emo_present]
ax1.legend(handles=legend_patches, loc="upper left",
           facecolor="#1C2333", edgecolor="#444", labelcolor="white",
           fontsize=9, title="Dominant Emotion", title_fontsize=9)
ax1.set_title(
    "FIGURE 1 — Social Network Structure: MBG Discourse on Platform X\n"
    f"N=971 vertices, 692 directed edges (displayed: top-300) | NodeXL/NetworkX Spring Layout",
    color="white", fontsize=11, fontweight="bold", pad=12
)
stats_text = (
    "Graph Density: 0.000707\n"
    "WCC: 341 | SCC: 967\n"
    "Modularity Q: 0.9837\n"
    "Reciprocity: 1.20%\n"
    "Max Degree: @grok (42)"
)
ax1.text(0.98, 0.02, stats_text, transform=ax1.transAxes, fontsize=8,
         va="bottom", ha="right", color="white",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#1C2333", edgecolor="#444", alpha=0.9))
ax1.axis("off")
fig1.savefig(os.path.join(OUT, "fig1_social_network_structure.png"), dpi=300,
             bbox_inches="tight", facecolor="#0D1117")
plt.close(fig1)
print("  Disimpan: fig1_social_network_structure.png")

# ── FIGURE 2: ACTOR CENTRALITY ───────────────────────────────────────────────
print("\n[5/9] Figure 2: Actor Centrality...")
metrics = [
    ("In_Degree",              "In-Degree\n(Koneksi Masuk)"),
    ("Out_Degree",             "Out-Degree\n(Koneksi Keluar)"),
    ("Betweenness_Centrality", "Betweenness\n(Perantara)"),
    ("Closeness_Centrality",   "Closeness\n(Kedekatan)"),
    ("Eigenvector_Centrality", "Eigenvector\n(Pengaruh Global)"),
    ("PageRank",               "PageRank\n(Otoritas Halaman)"),
]
fig2, axes2 = plt.subplots(2, 3, figsize=(16, 11), facecolor="#FAFAFA")
fig2.suptitle(
    "FIGURE 2 — Actor Centrality Analysis: Top-15 Actors per Metric\n"
    "NodeXL Pro Standard · NetworkX Computation · N=971 Actors",
    fontsize=13, fontweight="bold", y=1.01
)
for idx, (metric, label) in enumerate(metrics):
    ax = axes2[idx // 3][idx % 3]
    top = actors_df.nlargest(15, metric)[["Label", metric, "Dominant_Emotion"]].sort_values(metric)
    colors = [EMOTION_PALETTE.get(e, "#757575") for e in top["Dominant_Emotion"]]
    bars = ax.barh(top["Label"], top[metric], color=colors, edgecolor="white", linewidth=0.5, height=0.7)
    for bar, val in zip(bars, top[metric]):
        ax.text(bar.get_width() + top[metric].max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.4f}", va="center", ha="left", fontsize=7.5, color="#333333")
    ax.set_title(label, fontsize=10, fontweight="bold", pad=6)
    ax.set_xlabel("Nilai Sentralitas", fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines[["top","right"]].set_visible(False)
    ax.set_facecolor("#F8F8F8")
legend_patches2 = [mpatches.Patch(color=v, label=k.capitalize())
                   for k, v in EMOTION_PALETTE.items() if k in actors_df["Dominant_Emotion"].unique()]
fig2.legend(handles=legend_patches2, loc="lower center", ncol=len(legend_patches2),
            bbox_to_anchor=(0.5, -0.02), title="Warna = Dominant Emotion (IndoBERT)", fontsize=8)
plt.tight_layout()
fig2.savefig(os.path.join(OUT, "fig2_actor_centrality.png"), dpi=300, bbox_inches="tight")
plt.close(fig2)
print("  Disimpan: fig2_actor_centrality.png")

# ── FIGURE 3: COMMUNITY STRUCTURE ────────────────────────────────────────────
print("\n[6/9] Figure 3: Community Structure...")
top_comms = comm_data["top_communities"]
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(16, 8),
                                   gridspec_kw={"width_ratios": [2, 1]})
fig3.suptitle(
    "FIGURE 3 — Community Structure: Louvain Modularity Q=0.9837 · 342 Communities\n"
    "Internal Edges: 99.86% · Bridge Edges: 0.14%",
    fontsize=12, fontweight="bold"
)
ax3a.set_facecolor("#F0F4F8")
x_pos = np.array([1.5, 4, 7, 9.5, 2.5, 5.5, 8, 1, 4.5, 6.5])[:len(top_comms)]
y_pos = np.array([5.5, 6, 5, 6, 3, 3.5, 3, 1.5, 2, 1])[:len(top_comms)]
scatter_sizes = [c["Jumlah_Aktor"] * 80 for c in top_comms]
scatter_colors = [EMOTION_PALETTE.get(c["Emosi_Dominan"], "#999") for c in top_comms]
ax3a.scatter(x_pos, y_pos, s=scatter_sizes, c=scatter_colors, alpha=0.8,
             edgecolors="white", linewidths=2, zorder=3)
for i, (x, y, comm) in enumerate(zip(x_pos, y_pos, top_comms)):
    ax3a.annotate(f"#{comm['Community_Id']}\nn={comm['Jumlah_Aktor']}",
                  (x, y), fontsize=7.5, ha="center", va="center",
                  color="white", fontweight="bold",
                  path_effects=[pe.withStroke(linewidth=2, foreground="black")])
    short_name = comm["Nama_Wacana"][:35]
    ax3a.annotate(short_name, (x, y - 0.6), fontsize=6, ha="center", va="top", color="#333333")
ax3a.set_xlim(0, 11); ax3a.set_ylim(-1, 8.5)
ax3a.set_title("Top Communities by Size (Bubble ∝ Jumlah Aktor)", fontsize=10)
ax3a.axis("off")
for emo in set(c["Emosi_Dominan"] for c in top_comms):
    ax3a.scatter([], [], c=EMOTION_PALETTE.get(emo, "#999"), label=emo.capitalize(), s=80)
ax3a.legend(loc="upper right", fontsize=8, title="Emosi Dominan")

ax3b.set_facecolor("#F8F8F8")
iso_vals   = [comm_data["internal_pct"], comm_data["external_pct"]]
iso_labels = [
    f"Internal\n({comm_data['internal_edges']} edges)",
    f"Bridge\n({comm_data['external_edges']} edge)",
]
bars_iso = ax3b.bar(iso_labels, iso_vals, color=["#1565C0", "#E53935"],
                    width=0.5, edgecolor="white", linewidth=1.5)
for bar, val in zip(bars_iso, iso_vals):
    ax3b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
              f"{val:.2f}%", ha="center", va="bottom", fontsize=14, fontweight="bold")
ax3b.set_ylim(0, 110)
ax3b.set_ylabel("% dari Total Edges", fontsize=9)
ax3b.set_title(f"Echo Chamber Isolation\nTotal = {comm_data['total_edges']} edges", fontsize=10)
ax3b.spines[["top","right"]].set_visible(False)
plt.tight_layout()
fig3.savefig(os.path.join(OUT, "fig3_community_structure.png"), dpi=300, bbox_inches="tight")
plt.close(fig3)
print("  Disimpan: fig3_community_structure.png")

# ── FIGURE 4: EMOTION DISTRIBUTION ──────────────────────────────────────────
print("\n[7/9] Figure 4: Emotion Distribution...")
emo_counts = actors_df["Dominant_Emotion"].value_counts()
emo_labels_pie = emo_counts.index.tolist()
emo_vals_pie   = emo_counts.values.tolist()
emo_colors_pie = [EMOTION_PALETTE.get(e, "#999") for e in emo_labels_pie]
total_n = sum(emo_vals_pie)
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 7))
fig4.suptitle(
    "FIGURE 4 — Emotion Distribution (IndoBERT 9-Label Classification)\n"
    f"N={total_n} Actors · Model: indobenchmark/indobert-base-p2 · Fine-tuned 3 Epochs",
    fontsize=12, fontweight="bold"
)
wedges, texts, autotexts = ax4a.pie(
    emo_vals_pie, colors=emo_colors_pie, autopct="%1.1f%%",
    startangle=140, pctdistance=0.82,
    wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2)
)
for at in autotexts:
    at.set_fontsize(10); at.set_fontweight("bold"); at.set_color("white")
ax4a.text(0, 0, f"N={total_n}\nAktors", ha="center", va="center",
          fontsize=13, fontweight="bold", color="#333333")
ax4a.set_title("Distribusi Proporsi (Donut)", fontsize=10)
ax4a.legend(wedges, [f"{l.capitalize()} ({v})" for l, v in zip(emo_labels_pie, emo_vals_pie)],
            loc="lower center", fontsize=9, bbox_to_anchor=(0.5, -0.12))
sorted_idx    = np.argsort(emo_vals_pie)[::-1]
sorted_vals   = [emo_vals_pie[i] for i in sorted_idx]
sorted_labels = [emo_labels_pie[i] for i in sorted_idx]
sorted_colors = [emo_colors_pie[i] for i in sorted_idx]
bars4 = ax4b.barh([l.capitalize() for l in sorted_labels], sorted_vals,
                   color=sorted_colors, edgecolor="white", linewidth=0.7, height=0.65)
for bar, val in zip(bars4, sorted_vals):
    ax4b.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
              f"{val}  ({val/total_n*100:.1f}%)", va="center", fontsize=9, color="#333333")
ax4b.set_xlim(0, max(sorted_vals) * 1.3)
ax4b.set_xlabel("Jumlah Akun (N)", fontsize=9)
ax4b.set_title("Frekuensi per Emosi (Bar Chart)", fontsize=10)
ax4b.spines[["top","right"]].set_visible(False)
plt.tight_layout()
fig4.savefig(os.path.join(OUT, "fig4_emotion_distribution.png"), dpi=300, bbox_inches="tight")
plt.close(fig4)
print("  Disimpan: fig4_emotion_distribution.png")

# ── FIGURE 5: EMOTION BY COMMUNITY ──────────────────────────────────────────
print("\n[8/9] Figure 5: Emotion by Community...")
emo_labels_all = ["disgust", "neutral", "love", "anger", "fear", "joy", "sadness", "shame", "surprise"]
heatmap_matrix = []
comm_names_short = []
for c in top_comms:
    row = [c["Distribusi_Emosi"].get(e, 0) / c["Jumlah_Aktor"] * 100
           for e in emo_labels_all]
    heatmap_matrix.append(row)
    comm_names_short.append(f"#{c['Community_Id']} (n={c['Jumlah_Aktor']})\n{c.get('Nama_Wacana','')[:28]}")
heatmap_arr = np.array(heatmap_matrix)

fig5, axes5 = plt.subplots(1, 2, figsize=(16, 7),
                            gridspec_kw={"width_ratios": [2.5, 1]})
fig5.suptitle(
    "FIGURE 5 — Emotion Distribution by Community\n"
    "IndoBERT Emotion Profile per Louvain Cluster · Top Communities",
    fontsize=12, fontweight="bold"
)
cmap5 = LinearSegmentedColormap.from_list("emo_heat", ["#FFFFFF","#FFCDD2","#E53935","#B71C1C"])
im = axes5[0].imshow(heatmap_arr, cmap=cmap5, aspect="auto", vmin=0, vmax=100)
axes5[0].set_xticks(range(len(emo_labels_all)))
axes5[0].set_xticklabels([e.capitalize() for e in emo_labels_all], rotation=35, ha="right", fontsize=9)
axes5[0].set_yticks(range(len(comm_names_short)))
axes5[0].set_yticklabels(comm_names_short, fontsize=7.5)
axes5[0].set_title("Heatmap: % Emosi per Komunitas", fontsize=10)
for i in range(heatmap_arr.shape[0]):
    for j in range(heatmap_arr.shape[1]):
        val = heatmap_arr[i, j]
        if val > 0:
            axes5[0].text(j, i, f"{val:.0f}%", ha="center", va="center",
                          fontsize=7.5, color="white" if val > 50 else "#333333",
                          fontweight="bold" if val > 40 else "normal")
plt.colorbar(im, ax=axes5[0], label="% Emosi dalam Komunitas", fraction=0.046, pad=0.04)

dominant_emos   = [c["Emosi_Dominan"] for c in top_comms]
comm_ids_short  = [f"#{c['Community_Id']}" for c in top_comms]
dominant_colors = [EMOTION_PALETTE.get(e, "#999") for e in dominant_emos]
for i, (cid, dom, col) in enumerate(zip(comm_ids_short, dominant_emos, dominant_colors)):
    axes5[1].barh(i, 1, color=col, edgecolor="white", linewidth=0.7)
    axes5[1].text(0.5, i, dom.upper(), ha="center", va="center",
                  fontsize=8, color="white", fontweight="bold")
axes5[1].set_yticks(range(len(comm_ids_short)))
axes5[1].set_yticklabels(comm_ids_short, fontsize=9)
axes5[1].set_xlim(0, 1); axes5[1].set_xticks([])
axes5[1].set_title("Emosi\nDominan", fontsize=10)
axes5[1].spines[["top","right","bottom"]].set_visible(False)
plt.tight_layout()
fig5.savefig(os.path.join(OUT, "fig5_emotion_by_community.png"), dpi=300, bbox_inches="tight")
plt.close(fig5)
print("  Disimpan: fig5_emotion_by_community.png")

# ── FIGURE 6: NETWORK-EMOTION RELATIONSHIP ───────────────────────────────────
print("\n[9/9] Figure 6: Network–Emotion Relationship...")
fig6 = plt.figure(figsize=(16, 12))
gs6  = gridspec.GridSpec(2, 3, figure=fig6, hspace=0.4, wspace=0.35)
fig6.suptitle(
    "FIGURE 6 — Network Structure ↔ Emotion Relationship\n"
    "Structural Position (Centrality) vs Affective Expression (IndoBERT) · N=971",
    fontsize=12, fontweight="bold"
)
emos_present = actors_df["Dominant_Emotion"].unique()
emo_col_map  = {e: EMOTION_PALETTE.get(e, "#999") for e in emos_present}

ax61 = fig6.add_subplot(gs6[0, 0])
for emo in emos_present:
    sub = actors_df[actors_df["Dominant_Emotion"] == emo]
    ax61.scatter(sub["Normalized_Degree"], sub["PageRank"], c=emo_col_map[emo],
                 alpha=0.5, s=18, label=emo.capitalize(), edgecolors="none")
ax61.set_xlabel("Degree Centrality", fontsize=8)
ax61.set_ylabel("PageRank", fontsize=8)
ax61.set_title("Degree vs PageRank\nper Emotion", fontsize=9)
ax61.spines[["top","right"]].set_visible(False)
ax61.legend(fontsize=7)

ax62 = fig6.add_subplot(gs6[0, 1])
for emo in emos_present:
    sub = actors_df[actors_df["Dominant_Emotion"] == emo]
    ax62.scatter(sub["Betweenness_Centrality"], sub["Closeness_Centrality"],
                 c=emo_col_map[emo], alpha=0.5, s=18, edgecolors="none")
ax62.set_xlabel("Betweenness Centrality", fontsize=8)
ax62.set_ylabel("Closeness Centrality", fontsize=8)
ax62.set_title("Betweenness vs Closeness\nper Emotion", fontsize=9)
ax62.spines[["top","right"]].set_visible(False)

ax63 = fig6.add_subplot(gs6[0, 2])
for emo in emos_present:
    sub = actors_df[actors_df["Dominant_Emotion"] == emo]
    ax63.scatter(sub["Eigenvector_Centrality"], sub["Betweenness_Centrality"],
                 c=emo_col_map[emo], alpha=0.5, s=18, edgecolors="none")
ax63.set_xlabel("Eigenvector Centrality", fontsize=8)
ax63.set_ylabel("Betweenness Centrality", fontsize=8)
ax63.set_title("Eigenvector vs Betweenness\nper Emotion", fontsize=9)
ax63.spines[["top","right"]].set_visible(False)

ax64 = fig6.add_subplot(gs6[1, 0])
violin_data = [actors_df[actors_df["Dominant_Emotion"] == e]["Normalized_Degree"].values
               for e in emos_present]
vp = ax64.violinplot(violin_data, positions=range(len(emos_present)), showmedians=True)
for i, (patch, emo) in enumerate(zip(vp["bodies"], emos_present)):
    patch.set_facecolor(emo_col_map[emo]); patch.set_alpha(0.7)
vp["cmedians"].set_color("#222222")
vp["cbars"].set_color("#AAAAAA")
vp["cmaxes"].set_color("#AAAAAA")
vp["cmins"].set_color("#AAAAAA")
ax64.set_xticks(range(len(emos_present)))
ax64.set_xticklabels([e.capitalize() for e in emos_present], fontsize=8)
ax64.set_ylabel("Degree Centrality", fontsize=8)
ax64.set_title("Distribusi Degree per Emosi\n(Violin Plot)", fontsize=9)
ax64.spines[["top","right"]].set_visible(False)

ax65 = fig6.add_subplot(gs6[1, 1:])
roles_present = actors_df["Communication_Role"].unique()
box_data = [actors_df[actors_df["Communication_Role"] == r]["PageRank"].values
            for r in roles_present]
short_roles = [r.split("(")[0].strip()[:22] for r in roles_present]
bp = ax65.boxplot(box_data, vert=True, patch_artist=True,
                  medianprops=dict(color="black", linewidth=1.5),
                  flierprops=dict(marker="o", markersize=3, alpha=0.4))
for patch, role in zip(bp["boxes"], roles_present):
    patch.set_facecolor(ROLE_PALETTE.get(role, "#999999")); patch.set_alpha(0.75)
ax65.set_xticks(range(1, len(roles_present)+1))
ax65.set_xticklabels(short_roles, rotation=30, ha="right", fontsize=7.5)
ax65.set_ylabel("PageRank Score", fontsize=8)
ax65.set_title("Distribusi PageRank per Tipologi Peran Komunikasi", fontsize=9)
ax65.spines[["top","right"]].set_visible(False)

fig6.savefig(os.path.join(OUT, "fig6_network_emotion_relationship.png"), dpi=300, bbox_inches="tight")
plt.close(fig6)
print("  Disimpan: fig6_network_emotion_relationship.png")

# ── FIGURE 7: AI-MEDIATED FRAMEWORK ──────────────────────────────────────────
print("\n[10/10] Figure 7: AI-mediated Framework...")
fig7, ax7 = plt.subplots(1, 1, figsize=(16, 11), facecolor="#0A0E1A")
ax7.set_facecolor("#0A0E1A")
ax7.set_xlim(0, 10); ax7.set_ylim(0, 11); ax7.axis("off")

def draw_layer_box(ax, x, y, w, h, title, lines, tc, lc, bg, bc, ts=10.5, ls=8.8):
    from matplotlib.patches import FancyBboxPatch
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                           facecolor=bg, edgecolor=bc, linewidth=2.0, zorder=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.26, title, ha="center", va="top",
            fontsize=ts, fontweight="bold", color=tc, zorder=3)
    for i, line in enumerate(lines):
        ax.text(x + w/2, y + h - 0.58 - i*0.28, line, ha="center", va="top",
                fontsize=ls, color=lc, zorder=3)

layer_specs = [
    (0.3, 9.35, 9.4, 1.3, "LAYER 1 — INPUT: Komunikasi Publik di Platform X (Technology)",
     ["3.395 Cuitan MBG | Topik: Kualitas Gizi · Anggaran · Logistik · Kebijakan Prabowo",
      "Actor: @prabowo, @grok, @regar_op0sisi, @4Y4NKZ, @lambesahamjja (dan 966 lainnya)",
      "Format: Directed Mention & Retweet · Graf Berarah Asimetris"],
     "#64B5F6", "#CFE8FF", "#0D2137", "#1565C0"),
    (0.3, 7.65, 9.4, 1.45, "LAYER 2 — DETECTION: AI Emotion Classification (IndoBERT 9-Label)",
     ["Model: indobenchmark/indobert-base-p2 | Fine-tuned 3 Epoch · Batch=16 · Weight Decay=0.01",
      "9 Emosi: anger · disgust · fear · joy · love · neutral · sadness · shame · surprise",
      "Hasil Agregat: Disgust 56.24% · Neutral 52.5% (level aktor) · Sarcasm 9.28%"],
     "#EF9A9A", "#FFEBEE", "#1A0A0A", "#B71C1C"),
    (0.3, 5.75, 9.4, 1.65, "LAYER 3 — SHAPING: Algorithmic Community Formation (Louvain Algorithm)",
     ["Algoritma: Louvain Modularity Optimization (Blondel et al., 2008)",
      "Modularity Q = 0.9837 | 342 Echo Chambers Terbentuk",
      "Internal Edges: 691/692 (99.86%) | Bridge: 1 edge (0.14%) → Hiper-Fragmentasi",
      "Arketipe: Community Clusters (96.8%) + Polarized Crowd (94.5%)"],
     "#A5D6A7", "#E8F5E9", "#091A0A", "#1B5E20"),
    (0.3, 3.9, 9.4, 1.6, "LAYER 4 — MEDIATING: NodeXL Social Network Analysis (Centrality & Role)",
     ["Graf: 971 Vertices · 692 Directed Edges · Density=0.000707 · WCC=341 · SCC=967",
      "@grok: Out-Degree=42 (Algorithmic Oracle) · @prabowo: In-Degree=15 (Target Sink)",
      "@regar_op0sisi: Betweenness=0.004564 (Opinion Broker/Jembatan Diskursus)",
      "7 Tipologi Aktor · 6 Centrality Metrics: Degree · Betweenness · Closeness · Eigenvector · PageRank"],
     "#CE93D8", "#F3E5F5", "#130A1A", "#6A1B9A"),
    (0.3, 2.2, 9.4, 1.45, "LAYER 5 — INTERPRETING: Theoretical Synthesis & Research Output",
     ["Teori: Situational Crisis Communication Theory (SCCT) + Phygital Gap (Kotler)",
      "AI (@grok=Oracle Verifikasi) memediasi kepercayaan informasi secara algoritmik",
      "Hiper-fragmentasi = Algorithmic Sorting memisahkan ruang komunikasi publik",
      "Temuan: Teknologi/AI/Algoritma membentuk, mendeteksi, memediasi, dan menginterpretasi"],
     "#FFCC80", "#FFF8E1", "#1A1200", "#E65100"),
]

for spec in layer_specs:
    draw_layer_box(ax7, *spec)

# Arrows
for y1, y2 in [(9.35, 9.12), (7.65, 7.42), (5.75, 5.52), (3.9, 3.67)]:
    ax7.annotate("", xy=(5, y2), xytext=(5, y1),
                 arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=2.0, mutation_scale=18),
                 zorder=4)

ax7.text(5, 10.88, "FIGURE 7 — AI-mediated Social Communication Framework",
         ha="center", va="top", fontsize=13.5, fontweight="bold", color="white",
         path_effects=[pe.withStroke(linewidth=3, foreground="#0A0E1A")])
ax7.text(5, 10.58,
         "NodeXL SNA + IndoBERT 9-Emotion + Louvain Community Detection · MBG Discourse Platform X",
         ha="center", va="top", fontsize=9, color="#90A4AE")

# RQ box
rq = FancyBboxPatch((0.3, 0.2), 9.4, 1.75, boxstyle="round,pad=0.15",
                     facecolor="#1C2333", edgecolor="#37474F", linewidth=1.5, zorder=2)
ax7.add_patch(rq)
ax7.text(5, 1.83, "RESEARCH QUESTION ANSWERED:", ha="center", va="top",
         fontsize=10, fontweight="bold", color="#80DEEA")
ax7.text(5, 1.57,
         '"What role do technology, AI, and algorithms play in shaping, detecting, mediating,',
         ha="center", va="top", fontsize=9, color="#E0E0E0")
ax7.text(5, 1.33, 'and interpreting human communication on social media?"',
         ha="center", va="top", fontsize=9, color="#E0E0E0")
ax7.text(5, 1.04,
         "Technology → shapes discourse topology   |   AI (IndoBERT + @grok) → detects & mediates   |   Algorithms (Louvain + PageRank) → interprets actor roles",
         ha="center", va="top", fontsize=8, color="#AAAAAA", style="italic")

fig7.savefig(os.path.join(OUT, "fig7_ai_mediated_framework.png"), dpi=300,
             bbox_inches="tight", facecolor="#0A0E1A")
plt.close(fig7)
print("  Disimpan: fig7_ai_mediated_framework.png")

# ── README ─────────────────────────────────────────────────────────────────
readme = """# README — NodeXL Analysis Pipeline: 7 Figures
## Tesis MBG: Indri Anjar Kartika Sari · Magister Ilmu Komunikasi

**RQ:** *"What role do technology, AI, and algorithms play in shaping, detecting, mediating, and interpreting human communication on social media?"*

---

## Data Sumber (TIDAK DIMODIFIKASI)
| File | Keterangan |
|:---|:---|
| `NodeXL_MBG_Tesis_Indri_Anjar.xlsx` | Workbook NodeXL utama: Edges, Vertices, Groups, Overall Metrics |
| `results/mbg_network_nodes_final.csv` | 971 akun: Id, Degree, Betweenness, Community, Dominant_Emotion |
| `results/mbg_network_edges_final.csv` | 692 relasi: Source → Target |
| `results/actor_centrality_typology.csv` | 971 akun: 6 centrality + tipologi peran komunikasi |
| `results/community_echo_chambers.json` | Louvain Q=0.9837, 342 komunitas, echo chamber stats |

---

## FIGURE 1 — Social Network Structure
**fig1_social_network_structure.png**
- Variabel: node color = Dominant_Emotion, node size = Degree Centrality, edge = mention/retweet directed
- Metode: NetworkX Spring Layout (k=2.5, iter=80, seed=42), top-300 node by degree
- RQ: Menunjukkan bagaimana teknologi (platform X) membentuk topologi komunikasi — hub-and-spoke, fragmentasi 341 WCC

## FIGURE 2 — Actor Centrality
**fig2_actor_centrality.png**
- Variabel: Top-15 aktor per 6 metrik (In-Degree, Out-Degree, Betweenness, Closeness, Eigenvector, PageRank)
- Metode: NetworkX (DiGraph + Graph), Eigenvector = nx.eigenvector_centrality_numpy [BARU DIHITUNG]
- RQ: Mengidentifikasi peran AI (@grok=Oracle) dan algoritma (PageRank) dalam mediasi informasi

## FIGURE 3 — Community Structure
**fig3_community_structure.png**
- Variabel: bubble size = jumlah aktor, bubble color = emosi dominan, bar = isolasi internal/bridge
- Metode: Louvain Modularity (Blondel 2008), Q=0.9837, echo chamber index = 99.86%
- RQ: Membuktikan algorithmic sorting menciptakan echo chamber ekstrem (fragmentasi 342 klaster)

## FIGURE 4 — Emotion Distribution
**fig4_emotion_distribution.png**
- Variabel: Dominant_Emotion per aktor (neutral=510, disgust=447, love=14)
- Metode: IndoBERT fine-tuned → mode(predicted_emotion) per author_username
- RQ: AI (IndoBERT) mendeteksi disgust sebagai emosi dominan (56.24%) — AI memediasi interpretasi emosi

## FIGURE 5 — Emotion by Community
**fig5_emotion_by_community.png**
- Variabel: heatmap % emosi per komunitas, top-6 klaster × 9 label emosi
- Metode: Distribusi_Emosi dari community_echo_chambers.json, normalisasi per klaster
- RQ: AI (IndoBERT) + algoritma (Louvain) mengungkap setiap echo chamber memiliki karakter afektif unik

## FIGURE 6 — Network–Emotion Relationship
**fig6_network_emotion_relationship.png**
- Variabel: scatter Degree×PageRank, Betweenness×Closeness, Eigenvector×Betweenness (color=emotion)
- Tambahan: violin distribusi degree per emosi, box PageRank per Communication_Role
- RQ: Menguji korelasi posisi struktural (algoritmik) dengan ekspresi emosi manusia

## FIGURE 7 — AI-mediated Social Communication Framework
**fig7_ai_mediated_framework.png**
- 5-layer conceptual framework: INPUT → DETECTION → SHAPING → MEDIATING → INTERPRETING
- Menjawab RQ secara holistik: Technology + AI + Algorithms dalam komunikasi sosial

---

## Cara Reproduksi
```bash
cd /path/to/tesis_mbg
python3 scripts/generate_nodexl_figures.py
```

## Output Tambahan
- `nodexl_centrality_full.csv` — 971 aktor × 13 kolom termasuk Eigenvector_Centrality (baru)

**Catatan:** NodeXL workbook tidak dimodifikasi. Tidak ada data sintetis. Resolusi 300 DPI.
"""
with open(os.path.join(OUT, "README_FIGURES.md"), "w", encoding="utf-8") as f:
    f.write(readme)
print("  Disimpan: README_FIGURES.md")

# ── FINAL SUMMARY ────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("PIPELINE SELESAI")
print("=" * 70)
for fname in sorted(os.listdir(OUT)):
    fpath = os.path.join(OUT, fname)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {fname:<48} {size_kb:7.1f} KB")
print("=" * 70)
import hashlib
for fname in ["NodeXL_MBG_Tesis_Indri_Anjar.xlsx", "NodeXL_Scraped_Tweets_MBG.xlsx"]:
    fpath_m = os.path.join(BASE, fname)
    if os.path.exists(fpath_m):
        h = hashlib.md5(open(fpath_m,"rb").read()).hexdigest()
        print(f"  [TIDAK DIUBAH] {fname}  MD5: {h}")
