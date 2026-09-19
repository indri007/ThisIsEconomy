"""
Script: plot_material3_network.py
Tesis Magister: Analisis Jaringan Komunikasi & Sentimen MBG di Platform X
Visualisasi Hubungan Komunikasi Antar-Akun Twitter/X dengan Google Material Design 3 (M3)
"""

import os
import sys
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

# Setup paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

# Load real empirical network data
nodes_path = get_result_path("mbg_network_nodes_final.csv")
edges_path = get_result_path("mbg_network_edges_final.csv")

if not os.path.exists(nodes_path) or not os.path.exists(edges_path):
    nodes_path = os.path.join(base_dir, "results", "mbg_network_nodes_final.csv")
    edges_path = os.path.join(base_dir, "results", "mbg_network_edges_final.csv")

nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)

# Build Directed Graph
G = nx.from_pandas_edgelist(edges_df, source='Source', target='Target', create_using=nx.DiGraph())

# Add node attributes
for _, row in nodes_df.iterrows():
    if row['Id'] in G:
        G.nodes[row['Id']]['label'] = str(row['Label'])
        G.nodes[row['Id']]['degree'] = float(row['Degree'])
        G.nodes[row['Id']]['betweenness'] = float(row['Betweenness'])
        G.nodes[row['Id']]['community'] = int(row['Community'])
        G.nodes[row['Id']]['emotion'] = str(row['Dominant_Emotion'])

# Filter subnetwork for high-clarity visualization:
# Keep Largest Connected Component + Top Centrality Nodes + Top Clusters
wcc = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
lcc_nodes = set(wcc[0])  # Component 15 (Political & Policy Discourse, ~89 nodes)
for comp in wcc[1:10]:   # Add top 9 smaller connected dialogue clusters
    lcc_nodes.update(comp)

# Also ensure top nodes by betweenness and degree are present
top_betweenness = set(nodes_df.sort_values(by='Betweenness', ascending=False)['Id'].head(25))
top_degree = set(nodes_df.sort_values(by='Degree', ascending=False)['Id'].head(25))
visual_nodes = lcc_nodes.union(top_betweenness).union(top_degree)

subG = G.subgraph(visual_nodes).copy()

# Color Palette: Material Design 3 Dark Theme Tonal System
M3_SURFACE = "#141218"           # Baseline Dark Surface
M3_SURFACE_CARD = "#211F26"      # Elevated Surface Container
M3_SURFACE_CARD_HIGH = "#2B2930" # Higher Elevation Card
M3_OUTLINE = "#49454F"           # Outline / Border
M3_TEXT_PRIMARY = "#E6E0E9"      # High Contrast On-Surface Text
M3_TEXT_MUTED = "#CAC4D0"        # On-Surface Variant (Secondary text)

# M3 Semantic Tonal Colors for Account Roles
COLOR_TARGET_SINK = "#D0BCFF"     # M3 Primary Tonal (Violet/Purple) - @prabowo, @gibran_tweet
COLOR_OPINION_BROKER = "#FFB74D"  # M3 Tertiary Amber - @regar_op0sisi, @direktoridosen
COLOR_ALGO_ORACLE = "#4DD0E1"     # M3 Cyan/Teal - @grok
COLOR_SARCASM_CITIZEN = "#FF8A80" # M3 Soft Coral/Red - Citizen Disgust / Sarcasm
COLOR_AMPLIFIER = "#80CBC4"       # M3 Secondary Mint - Retweeters / Neutral
COLOR_DEFAULT = "#938F99"         # M3 Muted Outline

def classify_m3_role(node):
    node_lower = str(node).lower()
    if node_lower in ['prabowo', 'gibran_tweet', 'jokowi', 'kemdikbud']:
        return "Target Sink (Pemerintah)", COLOR_TARGET_SINK, 18
    elif node_lower == 'grok':
        return "Algorithmic Oracle (AI Bot)", COLOR_ALGO_ORACLE, 20
    elif node_lower in ['regar_op0sisi', 'direktoridosen', 'daffiriffi', 'punishe98373138']:
        return "Opinion Broker (Kritikus/Hub)", COLOR_OPINION_BROKER, 16
    elif node_lower in ['4y4nkz', 'newiding30', 'casagrande10939', 'dbdbidip', 'luvdysh_']:
        return "Sarcasm Hub (Citizen Viral)", COLOR_SARCASM_CITIZEN, 14
    else:
        # Check betweenness
        bw = subG.nodes[node].get('betweenness', 0)
        deg = subG.nodes[node].get('degree', 0)
        if bw > 0.0005:
            return "Secondary Broker", COLOR_OPINION_BROKER, 11
        elif deg > 0.005:
            return "Active Amplifier", COLOR_AMPLIFIER, 9
        else:
            return "Citizen Node", COLOR_DEFAULT, 6

# Compute positions using spring layout with tuned gravity and seed
pos = nx.spring_layout(subG, k=0.35, iterations=60, seed=42)

# Specific anchor adjustments for prominent focal nodes to prevent overlap and maximize clarity
if 'prabowo' in pos:
    pos['prabowo'] = np.array([0.05, 0.45])
if 'gibran_tweet' in pos:
    pos['gibran_tweet'] = np.array([-0.30, 0.35])
if 'regar_op0sisi' in pos:
    pos['regar_op0sisi'] = np.array([0.25, 0.05])
if 'direktoridosen' in pos:
    pos['direktoridosen'] = np.array([-0.15, -0.15])
if 'grok' in pos:
    pos['grok'] = np.array([0.55, -0.35])
if '4Y4NKZ' in pos:
    pos['4Y4NKZ'] = np.array([-0.65, -0.30])
if 'newIding30' in pos:
    pos['newIding30'] = np.array([-0.50, -0.55])

# Create Canvas
fig = plt.figure(figsize=(19, 10.8), facecolor=M3_SURFACE)
ax = fig.add_axes([0.02, 0.03, 0.96, 0.94], facecolor=M3_SURFACE)
ax.set_xlim(-1.15, 1.45)
ax.set_ylim(-1.05, 1.05)
ax.axis('off')

# 1. Material 3 Header Card
header_box = FancyBboxPatch((-1.10, 0.82), 2.50, 0.20,
                            boxstyle="round,pad=0.03,rounding_size=0.04",
                            facecolor=M3_SURFACE_CARD, edgecolor=M3_OUTLINE, linewidth=1.2, zorder=1)
ax.add_patch(header_box)

ax.text(-1.07, 0.96, "STRUKTUR KOMUNIKASI ANTAR-AKUN PLATFORM X (DISCOURSE MBG)", 
        fontsize=16, fontweight='bold', color=M3_TEXT_PRIMARY, zorder=2)
ax.text(-1.07, 0.89, "Pemetaan Relasi Interaksi, Target Sinks, Opinion Brokers, dan Algorithmic Oracle dalam Wacana Kebijakan", 
        fontsize=11, color=M3_TEXT_MUTED, zorder=2)

# M3 Pills in Header
pills = [
    ("● Target Sinks", COLOR_TARGET_SINK, -0.15),
    ("● Opinion Brokers", COLOR_OPINION_BROKER, 0.22),
    ("● Algorithmic Oracle", COLOR_ALGO_ORACLE, 0.65),
    ("● Sarcasm Clusters", COLOR_SARCASM_CITIZEN, 1.10),
]
for text, color, x_pos in pills:
    pill_patch = FancyBboxPatch((x_pos, 0.87), 0.32, 0.08,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor=M3_SURFACE_CARD_HIGH, edgecolor=color, linewidth=1.0, zorder=2)
    ax.add_patch(pill_patch)
    ax.text(x_pos + 0.16, 0.91, text, fontsize=9.5, fontweight='bold', color=color, ha='center', va='center', zorder=3)

# 2. Material 3 Left KPI Card (Metrics)
kpi_box = FancyBboxPatch((-1.10, -0.05), 0.36, 0.80,
                         boxstyle="round,pad=0.03,rounding_size=0.04",
                         facecolor=M3_SURFACE_CARD, edgecolor=M3_OUTLINE, linewidth=1.2, zorder=1)
ax.add_patch(kpi_box)

ax.text(-1.06, 0.69, "METRIK JARINGAN", fontsize=11, fontweight='bold', color=COLOR_TARGET_SINK, zorder=2)
metrics = [
    ("Total Nodes (|V|)", "971", "Akun Terlibat"),
    ("Total Edges (|E|)", "666", "Interaksi Direksi"),
    ("Modularity (Q)", "0.9837", "Hiper-Terfragmentasi"),
    ("Louvain Clusters", "341", "Komunitas Wacana"),
    ("Avg. In-Degree", "0.686", "Tingkat Respons"),
    ("Graph Density", "0.0007", "Struktur Sangat Longgar")
]
y_start = 0.59
for title, val, note in metrics:
    ax.text(-1.06, y_start, title, fontsize=9, color=M3_TEXT_MUTED, zorder=2)
    ax.text(-1.06, y_start - 0.045, val, fontsize=15, fontweight='bold', color=M3_TEXT_PRIMARY, zorder=2)
    ax.text(-1.06, y_start - 0.075, note, fontsize=8, color="#938F99", zorder=2)
    y_start -= 0.105

# 3. Material 3 Right Card (Role Insights & Communication Flow)
insight_box = FancyBboxPatch((1.05, -0.95), 0.38, 1.70,
                             boxstyle="round,pad=0.03,rounding_size=0.04",
                             facecolor=M3_SURFACE_CARD, edgecolor=M3_OUTLINE, linewidth=1.2, zorder=1)
ax.add_patch(insight_box)

ax.text(1.08, 0.68, "POLA INTERAKSI KUNCI", fontsize=11, fontweight='bold', color=COLOR_TARGET_SINK, zorder=2)

insights = [
    ("1. Target Sinks (@prabowo)", COLOR_TARGET_SINK, 
     "Menerima in-degree tinggi (15+ mention) namun 0 out-degree. Menjadi muara keluhan/tuntutan sepihak tanpa dialog interaktif balik dari akun resmi."),
    
    ("2. Opinion Brokers (@regar_op0sisi)", COLOR_OPINION_BROKER, 
     "Betweenness tertinggi (0.00456). Bertindak sebagai gatekeeper penghubung antara kritik warganet dengan wacana politik nasional."),
    
    ("3. Algorithmic Oracle (@grok)", COLOR_ALGO_ORACLE, 
     "Out-degree 42 respon. AI di-mention secara masif oleh warganet sebagai wasit pencari fakta transparansi anggaran dan gizi simulasi."),
    
    ("4. Sarcasm Echo-Chamber", COLOR_SARCASM_CITIZEN, 
     "Klaster warganet (@4Y4NKZ, @newIding30) menunjukkan modularitas ekstrem (Q=0.9837). Warganet saling me-retweet sindiran tanpa interaksi konstruktif.")
]

y_ins = 0.58
for head, col, desc in insights:
    card_mini = FancyBboxPatch((1.07, y_ins - 0.22), 0.34, 0.27,
                               boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor=M3_SURFACE_CARD_HIGH, edgecolor=col, linewidth=0.8, zorder=2)
    ax.add_patch(card_mini)
    ax.text(1.09, y_ins + 0.01, head, fontsize=9.5, fontweight='bold', color=col, zorder=3)
    # Simple word wrap for text
    words = desc.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 32:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))
    
    y_text = y_ins - 0.04
    for line in lines[:5]:
        ax.text(1.09, y_text, line, fontsize=7.8, color=M3_TEXT_MUTED, zorder=3)
        y_text -= 0.036
    y_ins -= 0.32

# 4. Draw Graph Canvas Background Card
graph_box = FancyBboxPatch((-0.70, -0.95), 1.70, 1.70,
                           boxstyle="round,pad=0.03,rounding_size=0.04",
                           facecolor="#1B1920", edgecolor=M3_OUTLINE, linewidth=1.2, zorder=1)
ax.add_patch(graph_box)

# Draw subtle concentric radial grid inside graph card for radar/network depth
for r in [0.3, 0.6, 0.9]:
    c = Circle((0.15, -0.10), r, color="#2B2930", fill=False, linestyle="--", linewidth=0.6, alpha=0.5, zorder=2)
    ax.add_patch(c)

# Draw Edges (Curved directed arcs)
for u, v in subG.edges():
    if u in pos and v in pos:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        
        # Determine edge highlight
        is_focal_edge = (u.lower() in ['prabowo', 'gibran_tweet', 'regar_op0sisi', 'grok'] or 
                         v.lower() in ['prabowo', 'gibran_tweet', 'regar_op0sisi', 'grok'])
        
        edge_col = "#6750A4" if is_focal_edge else "#49454F"
        edge_alpha = 0.55 if is_focal_edge else 0.20
        edge_width = 1.3 if is_focal_edge else 0.6
        
        ax.annotate("",
                    xy=(x2, y2), xycoords='data',
                    xytext=(x1, y1), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color=edge_col,
                                    shrinkA=8, shrinkB=8,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=0.08",
                                    alpha=edge_alpha, lw=edge_width),
                    zorder=3)

# Draw Nodes with Material 3 Glowing Halos
for node in subG.nodes():
    if node in pos:
        x, y = pos[node]
        role, color, base_size = classify_m3_role(node)
        
        # Outer soft glow halo for focal nodes
        if base_size >= 14:
            for halo_r, halo_alpha in [(base_size * 2.8, 0.08), (base_size * 1.8, 0.18)]:
                ax.plot(x, y, 'o', markersize=halo_r, color=color, alpha=halo_alpha, zorder=4)
        
        # Inner filled node
        ax.plot(x, y, 'o', markersize=base_size, color=color, markeredgecolor="#FFFFFF", markeredgewidth=1.2, zorder=5)
        
        # Labels for prominent nodes
        node_str = str(node)
        is_highlight_label = base_size >= 14 or node_str.lower() in ['prabowo', 'gibran_tweet', 'regar_op0sisi', 'grok', 'direktoridosen', '4y4nkz', 'newiding30', 'casagrande10939']
        
        if is_highlight_label:
            lbl = f"@{node_str}"
            ax.text(x, y + (0.045 if y > 0 else -0.055), lbl, 
                    fontsize=9.5, fontweight='bold', color="#FFFFFF", 
                    ha='center', va='center', zorder=6,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=M3_SURFACE_CARD, edgecolor=color, lw=0.8, alpha=0.92))

# 5. Bottom Narrative Card on Left
bot_card = FancyBboxPatch((-1.10, -0.95), 0.36, 0.85,
                          boxstyle="round,pad=0.03,rounding_size=0.04",
                          facecolor=M3_SURFACE_CARD, edgecolor=M3_OUTLINE, linewidth=1.2, zorder=1)
ax.add_patch(bot_card)

ax.text(-1.06, -0.15, "TEMUAN UTAMA SNA", fontsize=11, fontweight='bold', color=COLOR_TARGET_SINK, zorder=2)
bullets = [
    "• Relasi Komunikasi Asimetris: Target kebijakan tidak berdialog balik di media sosial.",
    "• Polaritas Fragmentasi: Q=0.9837 membuktikan wacana terpecah ke 341 sub-klaster tertutup.",
    "• Peran Algoritma: @grok berfungsi mengklarifikasi data gizi & alokasi anggaran Rp 71T.",
    "• Sarcasm Shielding: Warganet menggunakan sindiran halus untuk menghindari represi digital."
]
y_b = -0.25
for b in bullets:
    words = b.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 28:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))
    for l in lines:
        ax.text(-1.06, y_b, l, fontsize=7.8, color=M3_TEXT_MUTED, zorder=2)
        y_b -= 0.042
    y_b -= 0.02

# Save output high resolution
output_dir = os.path.join(base_dir, "results")
os.makedirs(output_dir, exist_ok=True)
save_path_results = os.path.join(output_dir, "15_material3_network_interaction.png")
save_path_assets = os.path.join(base_dir, "docs", "assets", "material3_network_interaction.png")

plt.savefig(save_path_results, dpi=300, facecolor=M3_SURFACE, bbox_inches='tight')
plt.savefig(save_path_assets, dpi=300, facecolor=M3_SURFACE, bbox_inches='tight')
plt.close()

print(f"Material 3 Network Plot saved successfully to:\n1. {save_path_results}\n2. {save_path_assets}")
