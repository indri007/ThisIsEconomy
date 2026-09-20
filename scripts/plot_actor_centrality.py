"""
Script: plot_actor_centrality.py
Visualisasi Komprehensif Dimensi 2:
Sentralitas Aktor & Tipologi Peran Komunikasi (NodeXL & NetworkX Standards)
Menghasilkan 18_actor_centrality_typology.png (300 DPI)
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Setup paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "results", "actor_centrality_typology.csv")
df = pd.read_csv(csv_path)

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(19, 13), dpi=300)
gs = gridspec.GridSpec(2, 2, width_ratios=[1.15, 1.0], height_ratios=[1.0, 1.0], wspace=0.25, hspace=0.32)

c_oracle = '#00BCD4'    # Cyan
c_sink = '#7B1FA2'      # Purple
c_broker = '#FF9800'    # Amber
c_broadcast = '#2563EB' # Blue
c_citizen = '#94A3B8'   # Grey Slate
c_influencer = '#10B981'# Emerald

role_color_map = {
    'Algorithmic Oracle (AI Fact-Checker)': c_oracle,
    'Target Sink (Otoritas Kebijakan)': c_sink,
    'Target Sink (Akun Rujukan Keluhan)': '#9333EA',
    'Opinion Broker (Jembatan Diskursus)': c_broker,
    'Information Broadcaster (Penyebar Wacana)': c_broadcast,
    'Secondary Influencer (Akun Penggerak)': c_influencer,
    'Peripheral Citizen (Warganet Biasa)': c_citizen
}

# ─────────────────────────────────────────────────────────────
# PANEL 1: In-Degree vs Out-Degree (Target Sink vs Broadcaster)
# ─────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])

for role, color in role_color_map.items():
    sub = df[df['Communication_Role'] == role]
    s_size = 140 if 'Oracle' in role or 'Otoritas' in role or 'Broker' in role else 45
    ax1.scatter(sub['Out_Degree'], sub['In_Degree'], label=role, color=color, s=s_size, alpha=0.85, edgecolors='black', linewidth=0.6)

# Anotasi aktor penting
def annotate_node(ax, label, x, y, ox, oy, bg):
    ax.annotate(label, xy=(x, y), xytext=(x + ox, y + oy),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=9.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=bg, edgecolor='black', alpha=0.9))

annotate_node(ax1, '@prabowo\n(Target Sink)', 0, 15, 2.5, -2.5, '#F3E8FF')
annotate_node(ax1, '@grok\n(AI Oracle)', 42, 0, -10, 3.5, '#E0F7FA')
annotate_node(ax1, '@regar_op0sisi\n(Broker)', 2, 5, 2.5, 2.0, '#FEF3C7')
annotate_node(ax1, '@newIding30\n(Broadcaster)', 15, 1, 2.0, 2.0, '#DBEAFE')

ax1.set_title('A. Matriks Arah Komunikasi: In-Degree vs Out-Degree (N=971)', fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('Out-Degree (Jumlah Menyebut Akun Lain / Broadcaster)', fontsize=11, fontweight='semibold')
ax1.set_ylabel('In-Degree (Jumlah Disebut / Target Sink)', fontsize=11, fontweight='semibold')
ax1.axhline(0, color='grey', linestyle=':', alpha=0.6)
ax1.axvline(0, color='grey', linestyle=':', alpha=0.6)
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=8.5, frameon=True)
ax1.grid(True, linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 2: Betweenness Centrality vs Total Degree (Brokerage Matrix)
# ─────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])

ax2.scatter(df['Total_Degree'], df['Betweenness_Centrality'], c=df['Communication_Role'].map(role_color_map), s=65, alpha=0.85, edgecolors='black', linewidth=0.6)

annotate_node(ax2, '@grok\n(Betweenness: 0.00594)', 42, 0.00594, -14, -0.0012, '#E0F7FA')
annotate_node(ax2, '@prabowo\n(Betweenness: 0.00541)', 15, 0.00541, 2.5, -0.0008, '#F3E8FF')
annotate_node(ax2, '@regar_op0sisi\n(Betweenness: 0.00456)', 7, 0.00456, 3.0, 0.0005, '#FEF3C7')
annotate_node(ax2, '@direktoridosen\n(Betweenness: 0.00124)', 4, 0.00124, 3.0, 0.0008, '#FEF3C7')

ax2.set_title('B. Matriks Pengaruh Struktural: Betweenness vs Derajat Total', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Total Degree Centrality (Banyak Koneksi)', fontsize=11, fontweight='semibold')
ax2.set_ylabel('Betweenness Centrality (Kapasitas Menjembatani)', fontsize=11, fontweight='semibold')
ax2.grid(True, linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 3: Top 15 Influential Actors Bar Chart
# ─────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
top15 = df.sort_values(by='Total_Degree', ascending=True).tail(15)

bar_colors = [role_color_map.get(r, c_citizen) for r in top15['Communication_Role']]
bars = ax3.barh(top15['Label'], top15['Total_Degree'], color=bar_colors, edgecolor='black', linewidth=0.8, height=0.65)

ax3.set_title('C. Lima Belas Aktor Sentralitas Derajat Tertinggi (Tabel 4.3)', fontsize=13, fontweight='bold', pad=10)
ax3.set_xlabel('Jumlah Derajat Koneksi (Total Degree)', fontsize=11, fontweight='semibold')

for bar in bars:
    w = bar.get_width()
    ax3.annotate(f'{int(w)}', xy=(w, bar.get_y() + bar.get_height() / 2),
                 xytext=(5, 0), textcoords="offset points",
                 ha='left', va='center', fontsize=9.5, fontweight='bold')

ax3.set_xlim(0, 48)
ax3.grid(axis='x', linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 4: Communication Role Composition Donut Chart
# ─────────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
role_counts = df['Communication_Role'].value_counts()
labels = [f"{k}\n({v} akun, {v/len(df)*100:.1f}%)" for k, v in role_counts.items()]
pie_colors = [role_color_map.get(k, c_citizen) for k in role_counts.index]

wedges, texts = ax4.pie(role_counts, labels=None, colors=pie_colors, startangle=140,
                        wedgeprops=dict(width=0.45, edgecolor='black', linewidth=0.8))

ax4.legend(wedges, labels, loc='center left', bbox_to_anchor=(0.9, 0.5), fontsize=8.8, frameon=True)
ax4.set_title('D. Proporsi Tipologi Peran Komunikasi (Populasi N=971 Akun)', fontsize=13, fontweight='bold', pad=10)

# Super title
fig.suptitle('ANALISIS DIMENSI 2: SENTRALITAS AKTOR & TIPOLOGI PERAN KOMUNIKASI (SNA)\nBuku Kerja NodeXL Pro & NetworkX: Tipologi Asimetris Target Sink, AI Oracle, & Opinion Broker',
             fontsize=16, fontweight='heavy', y=0.99, color='#0F172A')

out_png1 = os.path.join(base_dir, "results", "18_actor_centrality_typology.png")
out_png2 = os.path.join(base_dir, "docs", "assets", "actor_centrality_typology.png")

plt.savefig(out_png1, dpi=300, bbox_inches='tight')
plt.savefig(out_png2, dpi=300, bbox_inches='tight')
plt.close()

print(f"Visualisasi Dimensi 2 berhasil disimpan:\n1. {out_png1}\n2. {out_png2}")
