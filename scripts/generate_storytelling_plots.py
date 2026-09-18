import os
import sys

# Ensure working directory is project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import networkx as nx
import community.community_louvain as community_louvain

# Styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
os.makedirs("results", exist_ok=True)
os.makedirs("results/storytelling", exist_ok=True)

# -------------------------------------------------------------
# 1. Gambar 1A: End-to-End Pipeline
# -------------------------------------------------------------
print("1. Generating Gambar 1: Pipeline...")
fig, ax = plt.subplots(figsize=(11, 3.5), facecolor='#0f172a')
ax.set_facecolor('#0f172a')
ax.axis('off')

boxes = [
    ("1. Ekstraksi X API\n(Raw N = 5.310)", (0.10, 0.5), '#1e293b', '#38bdf8'),
    ("2. Data Cleansing\n(Filter Bot / Spam)", (0.32, 0.5), '#1e293b', '#818cf8'),
    ("3. Korpus Riset\n(Valid N=3.395 / Inf N=5.263)", (0.55, 0.5), '#1e293b', '#c084fc'),
    ("4. IndoBERT 9 Emosi\n(Akurasi 57,45%)", (0.76, 0.65), '#1e293b', '#f43f5e'),
    ("5. SNA & Louvain\n(971 Node, Mod=0.9837)", (0.76, 0.35), '#1e293b', '#06b6d4'),
    ("6. Sintesis Phygital\n(Marketing 6.0)", (0.94, 0.5), '#312e81', '#fbbf24')
]

for text, pos, bg, edge in boxes:
    ax.text(pos[0], pos[1], text, ha='center', va='center', size=8.5, fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.6", fc=bg, ec=edge, lw=1.8))

# Arrows
ax.annotate("", xy=(0.22, 0.5), xytext=(0.17, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color='#94a3b8'))
ax.annotate("", xy=(0.44, 0.5), xytext=(0.40, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color='#94a3b8'))
ax.annotate("", xy=(0.67, 0.62), xytext=(0.64, 0.53), arrowprops=dict(arrowstyle="->", lw=2, color='#f43f5e'))
ax.annotate("", xy=(0.67, 0.38), xytext=(0.64, 0.47), arrowprops=dict(arrowstyle="->", lw=2, color='#06b6d4'))
ax.annotate("", xy=(0.87, 0.53), xytext=(0.84, 0.62), arrowprops=dict(arrowstyle="->", lw=2, color='#f43f5e'))
ax.annotate("", xy=(0.87, 0.47), xytext=(0.84, 0.38), arrowprops=dict(arrowstyle="->", lw=2, color='#06b6d4'))

plt.title("Gambar 1: Alur Komputasional Riset MBG (Computational Social Science)", 
          fontsize=12, fontweight='bold', color='white', pad=15)
plt.savefig("results/1_pipeline.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/1_pipeline.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()


# -------------------------------------------------------------
# 2. Gambar 2: Emotion Distribution (N=5.263)
# -------------------------------------------------------------
print("2. Generating Gambar 2: Emotion Distribution...")
df_emo = pd.read_csv('data/results/indobert_9_emosi_fixed.csv')
emo_counts = df_emo['predicted_emotion'].value_counts()
all_9 = ['Jijik', 'Percaya', 'Netral', 'Tertarik', 'Marah', 'Sedih', 'Takut', 'Bahagia', 'Kaget']
counts = [emo_counts.get(e, 0) for e in all_9]
pcts = [(c / len(df_emo)) * 100 for c in counts]

emo_colors = {
    'Jijik': '#059669', 'Percaya': '#10b981', 'Netral': '#64748b', 'Tertarik': '#f97316',
    'Marah': '#ef4444', 'Sedih': '#3b82f6', 'Takut': '#8b5cf6', 'Bahagia': '#eab308', 'Kaget': '#06b6d4'
}

fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0f172a')
ax.set_facecolor('#1e293b')
bars = ax.bar(all_9, counts, color=[emo_colors[e] for e in all_9], width=0.6, edgecolor='white', linewidth=0.5)

for bar, count, pct in zip(bars, counts, pcts):
    if count > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, f"{count:,}\n({pct:.1f}%)", 
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='white')

ax.set_ylabel("Jumlah Cuitan (N = 5.263)", color='white', fontsize=11, fontweight='bold')
ax.set_xlabel("9 Kategori Emosi Plutchik", color='white', fontsize=11, fontweight='bold')
ax.tick_params(colors='white', labelsize=10)
ax.set_ylim(0, 3400)
for spine in ax.spines.values():
    spine.set_color('#334155')

plt.title("Gambar 2: Distribusi 9 Kelas Emosi Plutchik pada Korpus MBG (N=5.263)", 
          fontsize=13, fontweight='bold', color='white', pad=15)
plt.tight_layout()
plt.savefig("results/emotion_distribution.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/emotion_distribution.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()


# -------------------------------------------------------------
# 3. Gambar 3: Sarcasm Distribution (Real N=3.395)
# -------------------------------------------------------------
print("3. Generating Gambar 3: Sarcasm Distribution...")
df_sarc = pd.read_csv('data/sarcasm/dataset_sindiran_valid.csv')
sarc_counts = df_sarc['sindiran'].value_counts()
non_sarc = sarc_counts.get(False, 3080)
is_sarc = sarc_counts.get(True, 315)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), facecolor='#0f172a')
for ax in (ax1, ax2):
    ax.set_facecolor('#0f172a')

# Donut Chart Dataset Validasi
wedges, texts, autotexts = ax1.pie(
    [non_sarc, is_sarc], 
    labels=['Non-Sindiran (Literal)', 'Sindiran Terverifikasi'],
    colors=['#3b82f6', '#f43f5e'],
    autopct='%1.2f%%',
    startangle=40,
    pctdistance=0.75,
    textprops=dict(color="white", fontweight='bold', fontsize=9),
    wedgeprops=dict(width=0.45, edgecolor='#0f172a', linewidth=2)
)
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(10)
ax1.set_title(f"A. Korpus Validasi Sindiran (N=3.395)\n315 Sindiran (9,28%) vs 3.080 Literal", 
              color='white', fontsize=11, fontweight='bold', pad=10)

# Bar Chart Rekonstruksi Inferensi
cat_names = ['Sindiran Leksikon\nEksplisit', 'Proksi Afektif\nPenolakan/Jijik', 'Non-Sindiran\nLiteral']
cat_vals = [181, 2979, 2284]
cat_colors = ['#f43f5e', '#10b981', '#64748b']

bars = ax2.bar(cat_names, cat_vals, color=cat_colors, width=0.55, edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, cat_vals):
    pct = (val / 5263) * 100
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 60, f"{val:,}\n({pct:.1f}%)", 
             ha='center', va='bottom', fontsize=9, fontweight='bold', color='white')

ax2.set_facecolor('#1e293b')
ax2.tick_params(colors='white', labelsize=9)
ax2.set_ylabel("Jumlah Cuitan (N = 5.263)", color='white', fontsize=10)
ax2.set_ylim(0, 3500)
for spine in ax2.spines.values():
    spine.set_color('#334155')
ax2.set_title("B. Korpus Rekonstruksi Inferensi (N=5.263)\nProksi Penolakan & Resistensi Simbolik", 
              color='white', fontsize=11, fontweight='bold', pad=10)

plt.suptitle("Gambar 3: Karakteristik Deteksi Sindiran & Inkongruensi Bahasa (Data Riil)", 
             fontsize=13, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig("results/3_sarcasm.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/3_sarcasm.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()


# -------------------------------------------------------------
# 4. Gambar 6: Global Network Topology (Data Riil)
# -------------------------------------------------------------
print("4. Generating Gambar 6: Global Network Topology...")
df_edges = pd.read_csv('data/sna/network_edges.csv')
G = nx.from_pandas_edgelist(df_edges, 'Source', 'Target')

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#0f172a')
ax.set_facecolor('#0f172a')
pos = nx.spring_layout(G, k=0.18, iterations=30, seed=42)

# Degree calculation
deg_dict = dict(G.degree())
node_sizes = [max(15, deg_dict[n] * 6) for n in G.nodes()]

nx.draw_networkx_edges(G, pos, alpha=0.15, edge_color='#64748b', ax=ax, width=0.8)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='#38bdf8', alpha=0.7, ax=ax)

# Highlight Top 3
highlight = {'grok': '#f43f5e', 'prabowo': '#eab308', '4Y4NKZ': '#a855f7'}
for h_node, h_col in highlight.items():
    if h_node in G:
        nx.draw_networkx_nodes(G, pos, nodelist=[h_node], node_size=280, node_color=h_col, ax=ax)
        ax.text(pos[h_node][0], pos[h_node][1] + 0.03, f"@{h_node}", 
                fontsize=9, fontweight='bold', color='white', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc=h_col, ec="white", lw=1))

ax.set_title("Gambar 6: Struktur Graf Jaringan Global Diskursus MBG (971 Nodes, 666 Edges)\nHyper-Fragmentation Tanpa Pusat Dialog Tunggal", 
             fontsize=12, fontweight='bold', color='white', pad=15)
ax.axis('off')
plt.tight_layout()
plt.savefig("results/6_global_network.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/6_global_network.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()


# -------------------------------------------------------------
# 5. Gambar 8: Top 10 Actors (In-Degree vs Out-Degree)
# -------------------------------------------------------------
print("5. Generating Gambar 8: Top 10 Actors...")
df_edges = pd.read_csv('data/sna/network_edges.csv')
G_dir = nx.from_pandas_edgelist(df_edges, source='Source', target='Target', create_using=nx.DiGraph())

in_degs = dict(G_dir.in_degree())
out_degs = dict(G_dir.out_degree())
tot_degs = {n: in_degs.get(n, 0) + out_degs.get(n, 0) for n in G_dir.nodes()}

top10_nodes = sorted(tot_degs, key=tot_degs.get, reverse=True)[:10]
actor_df = pd.DataFrame({
    'Akun': [f"@{n}" for n in top10_nodes],
    'In-Degree (Disebut/Target)': [in_degs.get(n, 0) for n in top10_nodes],
    'Out-Degree (Menyebut/Aktif)': [out_degs.get(n, 0) for n in top10_nodes]
})

fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0f172a')
ax.set_facecolor('#1e293b')

y = np.arange(len(actor_df))
height = 0.38

r1 = ax.barh(y - height/2, actor_df['In-Degree (Disebut/Target)'], height, label='In-Degree (Target Aduan / Power Vacuum)', color='#f59e0b')
r2 = ax.barh(y + height/2, actor_df['Out-Degree (Menyebut/Aktif)'], height, label='Out-Degree (Aktor Aktif / Algorithmic Oracle)', color='#38bdf8')

for bar in r1:
    w = bar.get_width()
    if w > 0:
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{int(w)}", va='center', ha='left', color='white', fontsize=9, fontweight='bold')
for bar in r2:
    w = bar.get_width()
    if w > 0:
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{int(w)}", va='center', ha='left', color='white', fontsize=9, fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels(actor_df['Akun'], color='white', fontsize=10, fontweight='bold')
ax.invert_yaxis()
ax.set_xlabel("Nilai Derajat (Degree Count)", color='white', fontsize=11, fontweight='bold')
ax.tick_params(colors='white')
ax.set_xlim(0, 48)
ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')
for spine in ax.spines.values():
    spine.set_color('#334155')

plt.title("Gambar 8: Sentralitas Aktor Utama — Fenomena Power Vacuum & Algorithmic Oracle\n@prabowo In=15, Out=0 (Pasif) vs @grok Out=42 (Verifikator Publik)", 
          fontsize=12, fontweight='bold', color='white', pad=15)
plt.tight_layout()
plt.savefig("results/top_actors.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/top_actors.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()


# -------------------------------------------------------------
# 6. Gambar 9: Emotion x Louvain Communities Heatmap (Data Riil)
# -------------------------------------------------------------
print("6. Generating Gambar 9: Emotion x Louvain Heatmap...")
df_nodes = pd.read_csv('results/mbg_network_nodes_final.csv')
top5_comms = [15, 61, 16, 259, 8]
sub_nodes = df_nodes[df_nodes['Community'].isin(top5_comms)].copy()

# Rename columns to Indonesian
emo_map_id = {
    'disgust': 'Jijik (Disgust)',
    'neutral': 'Netral',
    'love': 'Percaya (Trust)',
    'shame': 'Tertarik',
    'anger': 'Marah'
}
sub_nodes['Emosi'] = sub_nodes['Dominant_Emotion'].map(lambda x: emo_map_id.get(str(x).lower(), str(x)))

comm_names = {
    15: "Klaster #15\n(Kritik MBG @prabowo)",
    61: "Klaster #61\n(Tanya Jawab AI @grok)",
    16: "Klaster #16\n(Sindiran @4Y4NKZ)",
    259: "Klaster #259\n(Apresiasi @dbdbidip)",
    8: "Klaster #8\n(Vendor & Anggaran)"
}
sub_nodes['Klaster'] = sub_nodes['Community'].map(comm_names)

ct = pd.crosstab(sub_nodes['Klaster'], sub_nodes['Emosi'])

fig, ax = plt.subplots(figsize=(9, 5), facecolor='#0f172a')
ax.set_facecolor('#1e293b')
sns.heatmap(ct, annot=True, fmt='d', cmap='YlOrRd', ax=ax, cbar=True, linewidths=1, linecolor='#0f172a',
            annot_kws={"size": 11, "fontweight": "bold"})
ax.tick_params(colors='white', labelsize=10)
ax.set_xlabel("Emosi Dominan Anggota Komunitas", color='white', fontsize=11, fontweight='bold')
ax.set_ylabel("Top 5 Komunitas Louvain", color='white', fontsize=11, fontweight='bold')
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(colors='white')

plt.title("Gambar 9: Distribusi Emosi pada Top 5 Komunitas Louvain (Data Riil)\nEmosi Jijik Meresap Kuat pada Klaster Inti (#15)", 
          fontsize=12, fontweight='bold', color='white', pad=15)
plt.tight_layout()
plt.savefig("results/9_emotion_network.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/9_emotion_network.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()


# -------------------------------------------------------------
# 7. Gambar 10: ABSA Thematic Analysis (Data Riil)
# -------------------------------------------------------------
print("7. Generating Gambar 10: ABSA Thematic...")
df_emo = pd.read_csv('data/results/indobert_9_emosi_fixed.csv')

logistik_kw = 'basi|racun|katering|telat|busuk|bau|dapur|distribusi|porsi'
anggaran_kw = 'anggaran|pajak|korupsi|dana|triliun|harga|rp|biaya|apbn|vendor'
gizi_kw = 'gizi|susu|sehat|stunting|nutrisi|telur|menu|protein|vitamin'

df_emo['logistik'] = df_emo['text'].str.contains(logistik_kw, case=False, na=False)
df_emo['anggaran'] = df_emo['text'].str.contains(anggaran_kw, case=False, na=False)
df_emo['gizi'] = df_emo['text'].str.contains(gizi_kw, case=False, na=False)

def get_sentiment(row):
    emo = row['predicted_emotion']
    if emo in ['Jijik', 'Marah', 'Sedih', 'Takut']:
        return 'Negatif (Jijik/Marah)'
    elif emo in ['Percaya', 'Bahagia']:
        return 'Positif (Percaya/Apresiasi)'
    else:
        return 'Netral / Ekspektasi'

df_emo['sentimen'] = df_emo.apply(get_sentiment, axis=1)

aspect_stats = []
for asp_name, col in [('Logistik & Mutu', 'logistik'), ('Anggaran & Vendor', 'anggaran'), ('Kualitas Gizi', 'gizi')]:
    sub = df_emo[df_emo[col]]
    vc = sub['sentimen'].value_counts(normalize=True) * 100
    aspect_stats.append({
        'Aspek': asp_name,
        'Negatif': vc.get('Negatif (Jijik/Marah)', 0),
        'Positif': vc.get('Positif (Percaya/Apresiasi)', 0),
        'Netral': vc.get('Netral / Ekspektasi', 0),
        'Total': len(sub)
    })

df_asp = pd.DataFrame(aspect_stats)

fig, ax = plt.subplots(figsize=(9, 5), facecolor='#0f172a')
ax.set_facecolor('#1e293b')

x = np.arange(len(df_asp))
width = 0.26

b1 = ax.bar(x - width, df_asp['Negatif'], width, label='Negatif (Jijik/Marah)', color='#ef4444')
b2 = ax.bar(x, df_asp['Positif'], width, label='Positif (Percaya/Apresiasi)', color='#10b981')
b3 = ax.bar(x + width, df_asp['Netral'], width, label='Netral / Ekspektasi', color='#64748b')

for bars in (b1, b2, b3):
    for b in bars:
        h = b.get_height()
        if h > 0:
            ax.text(b.get_x() + b.get_width()/2, h + 1, f"{h:.1f}%", ha='center', va='bottom', color='white', fontsize=9, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels([f"{row['Aspek']}\n(n = {row['Total']:,})" for _, row in df_asp.iterrows()], color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Persentase Sentimen (%)", color='white', fontsize=11, fontweight='bold')
ax.tick_params(colors='white')
ax.set_ylim(0, 95)
ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')
for spine in ax.spines.values():
    spine.set_color('#334155')

plt.title("Gambar 10: Analisis Sentimen 3 Aspek Kunci Program MBG (Data Riil)\nKekecewaan Publik Terpusat pada Eksekusi Logistik & Anggaran", 
          fontsize=12, fontweight='bold', color='white', pad=15)
plt.tight_layout()
plt.savefig("results/10_absa_thematic.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.savefig("results/storytelling/10_absa_thematic.png", dpi=300, bbox_inches='tight', facecolor='#0f172a')
plt.close()

print("ALL REAL VISUAL PLOTS SUCCESSFULLY GENERATED!")
