"""
Script: plot_community_echo_chambers.py
Visualisasi Komprehensif Dimensi 3:
Partisi Komunitas & Deteksi Ruang Gema (Clustering & Echo Chambers)
Menghasilkan 19_community_echo_chambers.png (300 DPI)
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
json_path = os.path.join(base_dir, "results", "community_echo_chambers.json")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(19, 13), dpi=300)
gs = gridspec.GridSpec(2, 2, width_ratios=[1.15, 1.0], height_ratios=[1.0, 1.0], wspace=0.25, hspace=0.32)

c_disgust = '#EF4444' # Red
c_neutral = '#3B82F6' # Blue
c_trust   = '#10B981' # Green
c_amber   = '#F59E0B' # Amber
c_purple  = '#8B5CF6' # Purple
c_slate   = '#334155' # Slate

# ─────────────────────────────────────────────────────────────
# PANEL 1: Ukuran Top Komunitas & Top Aktor
# ─────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])

top_comms = data['top_communities']
labels = [f"Klaster #{c['Community_Id']}\n{c['Nama_Wacana'][:28]}..." for c in reversed(top_comms)]
sizes = [c['Jumlah_Aktor'] for c in reversed(top_comms)]
bar_cols = [c_disgust if c['Emosi_Dominan'] == 'disgust' else c_neutral for c in reversed(top_comms)]

bars = ax1.barh(labels, sizes, color=bar_cols, edgecolor='black', linewidth=0.8, height=0.6)
ax1.set_title('A. Peringkat Komunitas Louvain Terbesar (Data Riil |V|=971)', fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('Jumlah Aktor / Pengguna (|V|)', fontsize=11, fontweight='semibold')

for bar in bars:
    w = bar.get_width()
    ax1.annotate(f'{int(w)} akun ({w/971*100:.1f}%)', xy=(w, bar.get_y() + bar.get_height() / 2),
                 xytext=(5, 0), textcoords="offset points",
                 ha='left', va='center', fontsize=9.5, fontweight='bold')

ax1.set_xlim(0, 56)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 2: Donut Chart Isolasi Ruang Gema (Echo Chamber Ratio)
# ─────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])

edge_counts = [data['internal_edges'], data['external_edges']]
pie_labels = [f"Tepi Internal (Echo Chamber)\n{data['internal_edges']} relasi ({data['internal_pct']:.2f}%)",
              f"Tepi Lintas-Batas (Bridge)\n{data['external_edges']} relasi ({data['external_pct']:.2f}%)"]
pie_colors = ['#EF4444', '#10B981']

wedges, texts = ax2.pie(edge_counts, labels=None, colors=pie_colors, startangle=270,
                        wedgeprops=dict(width=0.45, edgecolor='black', linewidth=1.2))

ax2.legend(wedges, pie_labels, loc='center', fontsize=10, frameon=True, facecolor='white', framealpha=0.95)
ax2.set_title(f'B. Tingkat Isolasi Ruang Gema Struktural: {data["internal_pct"]:.2f}% Kedap', fontsize=13, fontweight='bold', pad=10)

ax2.text(0, 0, f"Q = {data['modularity_q']:.4f}\nHyper-Segregated", ha='center', va='center', fontsize=11, fontweight='bold', color=c_slate)

# ─────────────────────────────────────────────────────────────
# PANEL 3: Distribusi Emosi IndoBERT di Komunitas Kunci
# ─────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])

c_names = [f"Klaster #{c['Community_Id']}" for c in top_comms]
emo_categories = ['disgust', 'neutral', 'love', 'anger']
emo_labels_clean = {'disgust': 'Disgust (Jijik / Sinis)', 'neutral': 'Neutral (Faktual)', 'love': 'Trust (Dukungan)', 'anger': 'Anger (Kemarahan)'}
emo_palette = {'disgust': c_disgust, 'neutral': c_neutral, 'love': c_trust, 'anger': '#DC2626'}

bottom_vals = np.zeros(len(top_comms))
for emo in emo_categories:
    vals = [c['Distribusi_Emosi'].get(emo, 0) for c in top_comms]
    ax3.bar(c_names, vals, bottom=bottom_vals, label=emo_labels_clean[emo], color=emo_palette[emo], edgecolor='black', linewidth=0.6, width=0.55)
    bottom_vals += np.array(vals)

ax3.set_title('C. Komposisi Sentimen Emosi IndoBERT per Komunitas Kunci', fontsize=13, fontweight='bold', pad=10)
ax3.set_ylabel('Jumlah Tweet / Kontribusi Aktor', fontsize=11, fontweight='semibold')
ax3.legend(loc='upper right', frameon=True, fontsize=9.5)
ax3.grid(axis='y', linestyle='--', alpha=0.5)

# ─────────────────────────────────────────────────────────────
# PANEL 4: Scorecard Diagnostik Ruang Gema & Modularity
# ─────────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

scorecard_text = f"""
===================================================================
    DIAGNOSTIK EMPIRIS RUANG GEMA (ECHO CHAMBERS & CLUSTERING)
               STANDAR RESMI PUBLIKASI NODEXL PRO
===================================================================
• Algoritma Partisi      : Louvain Modularity (Blondel et al., 2008)
• Skor Modularitas (Q)   : {data['modularity_q']:.4f} (Ambang Newman Q > 0.3)
• Total Komunitas Riil   : {data['num_communities']} Kelompok Percakapan
• Total Relasi Interaksi : {data['total_edges']} Tepi Relasi
• Relasi Internal        : {data['internal_edges']} Tepi ({data['internal_pct']:.2f}% Percakapan Tertutup)
• Relasi Lintas-Batas    : {data['external_edges']} Tepi ({data['external_pct']:.2f}% Dialog Menyeberang)
• Rasio Isolasi Wacana   : 99.86% (Kondisi Hyper-Polarized Chamber)
===================================================================
PROFIL TEMA DISKURSUS UTAMA:
1. Klaster #15 (46 Akun): Polemik Kebijakan & Oposisi (@prabowo vs @regar_op0sisi)
   Emosi Dominan : DISGUST (Sentimen Jijik/Kritik Mendominasi 60%+)
2. Klaster #61 (43 Akun): AI Fact-Checking Oracle (@grok)
   Emosi Dominan : NEUTRAL (Penyelidikan Anggaran & Kalkulasi Gizi)
3. Klaster #16 (18 Akun): Percakapan Sindiran / Sarkasme Warganet
4. Klaster #259 (14 Akun): Tanggapan Spontan & Curhatan Lapangan
===================================================================
TEMUAN UTAMA:
Hampir 100% (99.86%) percakapan terkunci di dalam kelompoknya masing-masing.
Tidak terjadi pertukaran gagasan konstruktif antar-faksi warganet,
yang memvalidasi temuan Phygital Gap pada naskah tesis.
===================================================================
"""

ax4.text(0.02, 0.98, scorecard_text, transform=ax4.transAxes,
         fontsize=9.2, fontfamily='monospace', verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.5))

fig.suptitle('ANALISIS DIMENSI 3: PARTISI KOMUNITAS & DETEKSI RUANG GEMA (ECHO CHAMBERS)\nBuku Kerja NodeXL Pro & Algoritma Louvain: Pembuktian Isolasi 99.86% & Polarisasi Q=0.9837',
             fontsize=16, fontweight='heavy', y=0.99, color='#0F172A')

out_png1 = os.path.join(base_dir, "results", "19_community_echo_chambers.png")
out_png2 = os.path.join(base_dir, "docs", "assets", "community_echo_chambers.png")

plt.savefig(out_png1, dpi=300, bbox_inches='tight')
plt.savefig(out_png2, dpi=300, bbox_inches='tight')
plt.close()

print(f"Visualisasi Dimensi 3 berhasil disimpan:\n1. {out_png1}\n2. {out_png2}")
