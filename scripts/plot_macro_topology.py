"""
Script: plot_macro_topology.py
Membuat visualisasi komprehensif Dimensi 1:
Struktur Makro Topologi Jaringan Komunikasi MBG (NodeXL & NetworkX Standards)
Menghasilkan 17_macro_topology_metrics.png (300 DPI)
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx

# Setup paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nodes_path = os.path.join(base_dir, "results", "mbg_network_nodes_final.csv")
edges_path = os.path.join(base_dir, "results", "mbg_network_edges_final.csv")

nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)

# Bangun graf
G_dir = nx.DiGraph()
for _, r in edges_df.iterrows():
    G_dir.add_edge(str(r['Source']), str(r['Target']))

in_deg = [d for n, d in G_dir.in_degree() if d > 0]
out_deg = [d for n, d in G_dir.out_degree() if d > 0]
all_deg = [d for n, d in G_dir.degree() if d > 0]

# Hitung komponen
wcc_sizes = sorted([len(c) for c in nx.weakly_connected_components(G_dir)], reverse=True)

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(18, 12), dpi=300)
gs = gridspec.GridSpec(2, 2, width_ratios=[1.2, 1.0], height_ratios=[1.0, 1.0], wspace=0.25, hspace=0.32)

# Color palette
c_blue = '#1E3A8A'
c_cyan = '#0284C7'
c_red = '#DC2626'
c_amber = '#D97706'
c_slate = '#334155'
c_card = '#F8FAFC'

# ─────────────────────────────────────────────────────────────
# PANEL 1: Degree Distribution (Descriptive Heavy-Tailed Structure)
# ─────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
from collections import Counter
deg_counts = Counter(all_deg)
x_vals = sorted(deg_counts.keys())
y_vals = [deg_counts[x] for x in x_vals]

ax1.scatter(x_vals, y_vals, color=c_blue, s=65, alpha=0.85, edgecolors='black', linewidth=0.8, label='Empirical Distribution P(k)')

# Descriptive scaling fit line
x_arr = np.linspace(min(x_vals), max(x_vals), 100)
# alpha = 2.168, P(k) ~ C * k^(-alpha)
C = y_vals[0] * (x_vals[0] ** 2.168)
y_fit = C * (x_arr ** (-2.168))
ax1.plot(x_arr, y_fit, color=c_red, linestyle='--', linewidth=2.0, label=r'Descriptive Scaling Fit: $P(k) \propto k^{-2.17}$')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_title('A. Distribusi Derajat Simpul (Heavy-Tailed Degree Distribution)', fontsize=13, fontweight='bold', pad=10, color=c_slate)
ax1.set_xlabel('Derajat Koneksi / Degree (k) [Log Scale]', fontsize=11, fontweight='semibold')
ax1.set_ylabel('Frekuensi Akun P(k) [Log Scale]', fontsize=11, fontweight='semibold')
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax1.annotate('Segelintir Hub Elit (@prabowo, @grok)\nmenguasai sentralitas informasi', 
             xy=(14, 2), xytext=(4, 25),
             arrowprops=dict(facecolor=c_slate, arrowstyle='->', lw=1.5),
             fontsize=9.5, fontweight='semibold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF3C7', edgecolor='#F59E0B'))
ax1.grid(True, which="both", ls="--", alpha=0.4)

# ─────────────────────────────────────────────────────────────
# PANEL 2: Component Size Distribution (Giant vs Fragmented)
# ─────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
top_wcc = wcc_sizes[:10]
comp_labels = [f"Comp {i+1}" if i > 0 else "Giant Component" for i in range(len(top_wcc))]
colors_wcc = [c_blue if i == 0 else c_cyan for i in range(len(top_wcc))]

bars = ax2.bar(range(len(top_wcc)), top_wcc, color=colors_wcc, edgecolor='black', linewidth=0.8, alpha=0.85)
ax2.set_xticks(range(len(top_wcc)))
ax2.set_xticklabels(comp_labels, rotation=35, ha='right', fontsize=9.5, fontweight='semibold')
ax2.set_title('B. Ukuran Komponen Terhubung (Weakly Connected Components)', fontsize=13, fontweight='bold', pad=10, color=c_slate)
ax2.set_ylabel('Jumlah Simpul Aktor (|V|)', fontsize=11, fontweight='semibold')

for bar in bars:
    h = bar.get_height()
    ax2.annotate(f'{h}', xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.annotate('Giant Component: 89 Aktor (9.17%)\n340 pulau kecil terisolasi (Echo Chambers)', 
             xy=(0, 89), xytext=(2, 65),
             arrowprops=dict(facecolor=c_blue, arrowstyle='->', lw=1.5),
             fontsize=9.5, fontweight='semibold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#E0F2FE', edgecolor='#38BDF8'))
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 3: Asymmetric Reciprocity Breakdown
# ─────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
# Edge categorization
total_edges = 692
unique_dir = 666
mutual_edges = 8  # 1.2%
self_loops = 17
asym_edges = unique_dir - mutual_edges

cats = ['Relasi Asimetris (Satu Arah)\n[Warganet -> Target Sink]', 'Self-Loops (Penyebutan Diri)', 'Relasi Resiprokal (Dua Arah)\n[Dialog Timbal-Balik]']
vals = [asym_edges, self_loops, mutual_edges]
colors_pie = ['#3B82F6', '#94A3B8', '#10B981']

bars3 = ax3.barh(cats, vals, color=colors_pie, edgecolor='black', linewidth=0.8, height=0.55)
ax3.set_title('C. Komposisi Arah Relasi & Resiprositas (Reciprocity Breakdown)', fontsize=13, fontweight='bold', pad=10, color=c_slate)
ax3.set_xlabel('Jumlah Relasi Tepi (|E|)', fontsize=11, fontweight='semibold')

for bar in bars3:
    w = bar.get_width()
    pct = (w / total_edges) * 100
    ax3.annotate(f'{w} ({pct:.1f}%)', xy=(w, bar.get_y() + bar.get_height() / 2),
                 xytext=(8, 0), textcoords="offset points",
                 ha='left', va='center', fontsize=9.5, fontweight='bold')

ax3.set_xlim(0, 750)
ax3.grid(axis='x', linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 4: NodeXL Official Overall Graph Metrics Scorecard
# ─────────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

# Render formal summary card
scorecard_text = """
===================================================================
   RINGKASAN PARAMETER STRUKTUR MAKRO TOPOLOGI JARINGAN (SNA)
                  STANDAR RESMI PUBLIKASI NODEXL PRO
===================================================================
• Tipe Topologi Graf        : Directed Network (Asymmetric Mentions)
• Total Simpul (|V|)         : 971 Akun Pengguna Aktif
• Total Tepi Relasi (|E|)    : 692 Tepi Komunikasi (666 Directed Unik)
• Kepadatan Graf (Density)   : 0.000707 (Jejaring Sangat Renggang/Sparse)
• Resiprositas Interaksi     : 1.20% (Didominasi Komunikasi Monolog)
• Komponen Terhubung (WCC)   : 341 Pulau Diskursus Independen
• Komponen Raksasa (Giant)   : 89 Simpul (9.17% Inti Percakapan Utama)
• Diameter Jaringan          : 9 Langkah Maksimum
• Jarak Rerata Jalur Pendek  : 3.67 Langkah Transmisi Informasi
• Rerata Koefisien Klaster   : 0.0171 (Fragmentasi Segitiga Lemah)
• Modularitas Louvain (Q)    : 0.9837 (Polarisasi & Segregasi Ekstrem)
• Asortativitas Derajat (r)  : -0.0847 (Disassortative: Warga -> Elit)
• Eksponen Struktur Derajat : Alpha = 2.168
===================================================================
KESIMPULAN METODOLOGIS:
Struktur jaringan membuktikan wacana MBG bukan komunitas sosial organik,
melainkan arena polarisasi asimetris di mana ribuan warganet menembakkan
kritik fisik ke akun elit pemerintah (@prabowo) tanpa dialog timbal-balik.
===================================================================
"""

ax4.text(0.02, 0.98, scorecard_text, transform=ax4.transAxes,
         fontsize=9.2, fontfamily='monospace', verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#F1F5F9', edgecolor='#64748B', linewidth=1.5))

# Overall super title
fig.suptitle('ANALISIS DIMENSI 1: STRUKTUR MAKRO TOPOLOGI JARINGAN KOMUNIKASI MBG\nBuku Kerja NodeXL Pro & NetworkX Algorithmic Framework (|V|=971, |E|=666, Q=0.9837)', 
             fontsize=16, fontweight='heavy', y=0.99, color='#0F172A')

# Save outputs
out_png1 = os.path.join(base_dir, "results", "17_macro_topology_metrics.png")
out_png2 = os.path.join(base_dir, "docs", "assets", "macro_topology_metrics.png")

plt.savefig(out_png1, dpi=300, bbox_inches='tight')
plt.savefig(out_png2, dpi=300, bbox_inches='tight')
plt.close()

print(f"Visualisasi berhasil disimpan ke:\n1. {out_png1}\n2. {out_png2}")
