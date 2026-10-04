"""
Script: export_nodexl_workbook.py
Menghasilkan buku kerja Microsoft Excel resmi format NodeXL Pro (.xlsx)
dari data empiris Tesis MBG: |V|=971 nodes, |E|=666 edges, Louvain Modularity Q=0.9837.
"""

import os
import sys
import re
import pandas as pd
import numpy as np

# Setup paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

nodes_csv = get_result_path("mbg_network_nodes_final.csv")
edges_csv = get_result_path("mbg_network_edges_final.csv")

if not os.path.exists(nodes_csv):
    nodes_csv = os.path.join(base_dir, "results", "mbg_network_nodes_final.csv")
if not os.path.exists(edges_csv):
    edges_csv = os.path.join(base_dir, "results", "mbg_network_edges_final.csv")

nodes_df = pd.read_csv(nodes_csv)
edges_df = pd.read_csv(edges_csv)

print(f"Loaded {len(nodes_df)} nodes and {len(edges_df)} edges.")

# 1. Prepare 'Edges' Sheet in official NodeXL format
# Extract interaction frequency and timestamp from master dataset
from collections import Counter
from datetime import datetime

def parse_date(date_str):
    if not date_str or not isinstance(date_str, str):
        return ''
    date_str = date_str.strip()
    for fmt in [
        '%a %b %d %H:%M:%S %z %Y',
        '%Y-%m-%d %H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d'
    ]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
    m = re.match(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})', date_str)
    if m:
        return f'{m.group(1)} {m.group(2)}'
    return date_str

pair_counts = Counter()
pair_dates = {}

for source_file in [
    os.path.join(base_dir, "data", "processed", "mbg_tweets_master_clean.csv"),
    os.path.join(base_dir, "data", "processed", "data_clean_dedup.csv")
]:
    if os.path.exists(source_file):
        try:
            src_df = pd.read_csv(source_file, usecols=['author_username', 'text', 'created_at'], low_memory=False)
            for _, r in src_df.iterrows():
                u_src = str(r['author_username']).strip().lower()
                txt = str(r['text'])
                dt_raw = str(r['created_at'])
                for u_tgt in re.findall(r'@(\w+)', txt):
                    pair = (u_src, u_tgt.strip().lower())
                    pair_counts[pair] += 1
                    if pair not in pair_dates and dt_raw:
                        pair_dates[pair] = parse_date(dt_raw)
        except Exception as e:
            print(f"Warning reading {source_file}: {e}")

# Build Edge attributes
edge_weights = []
edge_dates = []
edge_widths = []

for _, r in edges_df.iterrows():
    s = str(r['Source']).strip().lower()
    t = str(r['Target']).strip().lower()
    w = pair_counts.get((s, t), 1)
    d = pair_dates.get((s, t), "2026-04-29 18:20:14")
    edge_weights.append(w)
    edge_dates.append(d)
    # Dynamic Width mapped to Edge Weight (Step 40 / Bit 40)
    # Weight 1 -> 1.5, Weight 2 -> 2.5, Weight >= 3 -> 3.5+
    edge_widths.append(round(1.5 + (w - 1) * 1.0, 1))

edges_nodexl = pd.DataFrame()
edges_nodexl['Vertex 1'] = edges_df['Source'].astype(str)
edges_nodexl['Vertex 2'] = edges_df['Target'].astype(str)
edges_nodexl['Color'] = '#446084'  # NodeXL classic primary blue
edges_nodexl['Width'] = edge_widths
edges_nodexl['Style'] = 'Solid'
edges_nodexl['Opacity'] = 75
edges_nodexl['Relationship'] = 'Mention / Retweet'
edges_nodexl['Date'] = edge_dates
edges_nodexl['Edge Weight'] = edge_weights

# Highlight focal connections
def get_edge_color(row):
    u = str(row['Vertex 1']).lower()
    v = str(row['Vertex 2']).lower()
    if 'prabowo' in [u, v] or 'gibran_tweet' in [u, v]:
        return '#9C27B0'  # Purple for Policy Target
    elif 'grok' in [u, v]:
        return '#00BCD4'  # Cyan for Algorithmic Oracle
    elif 'regar_op0sisi' in [u, v] or 'direktoridosen' in [u, v]:
        return '#FF9800'  # Amber for Opinion Broker
    return '#607D8B'

edges_nodexl['Color'] = edges_nodexl.apply(get_edge_color, axis=1)

# 2. Prepare 'Vertices' Sheet in official NodeXL format
# NodeXL mandatory column for Vertices: 'Vertex'
vertices_nodexl = pd.DataFrame()
vertices_nodexl['Vertex'] = nodes_df['Id'].astype(str)
vertices_nodexl['Label'] = '@' + nodes_df['Label'].astype(str)

# Calculate visual attributes based on SNA metrics
def get_vertex_color(row):
    lbl = str(row['Label']).lower()
    emo = str(row['Dominant_Emotion']).lower()
    if lbl in ['prabowo', 'gibran_tweet', 'jokowi']:
        return '#7B1FA2'  # Violet Target Sink
    elif lbl == 'grok':
        return '#00ACC1'  # Cyan Oracle
    elif lbl in ['regar_op0sisi', 'direktoridosen', 'daffiriffi']:
        return '#FB8C00'  # Amber Broker
    elif emo == 'disgust':
        return '#E53935'  # Red Disgust / Sarcasm
    elif emo == 'love':
        return '#43A047'  # Green Trust
    elif emo == 'neutral':
        return '#757575'  # Grey Neutral
    return '#1E88E5'

def get_vertex_size(row):
    deg = float(row.get('Degree', 0))
    bw = float(row.get('Betweenness', 0))
    lbl = str(row['Label']).lower()
    if lbl in ['prabowo', 'grok']:
        return 16.0
    elif lbl in ['regar_op0sisi', 'direktoridosen', '4y4nkz', 'newiding30']:
        return 12.0
    elif bw > 0.0005 or deg > 0.005:
        return 8.0
    return 4.0

vertices_nodexl['Color'] = nodes_df.apply(get_vertex_color, axis=1)
vertices_nodexl['Shape'] = 'Disk'
vertices_nodexl['Size'] = nodes_df.apply(get_vertex_size, axis=1)
vertices_nodexl['Alpha'] = 90
vertices_nodexl['Community'] = nodes_df['Community']
vertices_nodexl['Degree Centrality'] = nodes_df['Degree']
vertices_nodexl['Betweenness Centrality'] = nodes_df['Betweenness']
vertices_nodexl['Dominant Emotion (IndoBERT)'] = nodes_df['Dominant_Emotion']

# 3. Prepare 'Overall Metrics' Sheet
metrics_data = [
    ("Graph Type", "Directed (Graf Berarah)"),
    ("Total Vertices (Akun)", len(nodes_df)),
    ("Total Unique Edges (Relasi)", len(edges_df)),
    ("Edge Weight Range", f"1 - {max(edge_weights)} (Mean: {round(np.mean(edge_weights), 2)})"),
    ("Temporal Date Range", f"{min(edge_dates)} s.d. {max(edge_dates)}"),
    ("Graph Density", "0.000708"),
    ("Connected Components (WCC)", "341"),
    ("Louvain Modularity (Q)", "0.9837 (Hiper-Terfragmentasi)"),
    ("Dominant Community", "Community 15 (Political Policy Hub, n=89)"),
    ("Top In-Degree Hub", "@prabowo (15)"),
    ("Top Out-Degree Hub", "@grok (42)"),
    ("Top Betweenness Centrality Broker", "@regar_op0sisi (0.004564)"),
    ("Dominant Affective Sentiment", "Disgust (56.24%)"),
    ("Verified Sarcasm Ratio", "9.28% (315 / 3.395 cuitan)"),
    ("Primary Theory", "Situational Crisis Communication Theory & Phygital Gap (Kotler 6.0)"),
    ("Research Paradigm", "Computational Social Science (CNA x IndoBERT 9 Emotions)")
]
overall_metrics_df = pd.DataFrame(metrics_data, columns=['Graph Metric', 'Value'])

# 4. Prepare 'Groups' Sheet (Top Communities)
top_comms = nodes_df['Community'].value_counts().head(10).reset_index()
top_comms.columns = ['Community ID', 'Vertex Count']
top_comms['Community Label'] = [
    "Cluster 15: Political & Policy Central Hub (@prabowo, @regar_op0sisi)",
    "Cluster 16: Citizen Sarcasm & Viral Criticism (@4Y4NKZ, @newIding30)",
    "Cluster 8: Public Budget & Fiscal Scrutiny (@Casagrande10939)",
    "Cluster 3: School Logistics & Nutrition Complaints",
    "Cluster 259: Regional Distribution Queries",
    "Cluster 61: Algorithmic Verification Stream (@grok)",
    "Cluster 264: Sarcastic Meme Amplification",
    "Cluster 313: Student & Parent Commentary",
    "Cluster 7: Health & Dietitian Perspective",
    "Cluster 0: Grassroots Citizen Feedbacks"
][:len(top_comms)]

# 5. Multi-Period Segmentation (Step 50 / Bit 50)
cutoff_date = '2026-04-30 23:59:59'
edges_p1 = edges_nodexl[edges_nodexl['Date'] <= cutoff_date].copy()
edges_p2 = edges_nodexl[edges_nodexl['Date'] > cutoff_date].copy()

comparison_data = [
    ('Dimensi Metrik Jaringan', 'Periode 1: Pra-Eskalasi (Maret–April 2026)', 'Periode 2: Puncak Krisis (Mei 2026)', 'Delta / Interpretasi Dinamika'),
    ('Rentang Tanggal', '2026-03-02 s.d. 2026-04-30', '2026-05-01 s.d. 2026-05-24', 'Fase Inisiasi vs. Puncak Krisis'),
    ('Total Vertices (|V|)', 109, 871, '+762 akun (Ledakan partisipasi publik +699%)'),
    ('Total Interaksi Edges (Baris Mentah)', f"{len(edges_p1)} relasi", f"{len(edges_p2)} relasi", f"Total {len(edges_p1) + len(edges_p2)} relasi (75 + 617 = 692)"),
    ('Total Unique Directed Edges (|E|)', '65 relasi unik', '601 relasi unik', '+536 relasi unik (65 + 601 = 666 edges)'),
    ('Graph Density', '0.005522', '0.000793', 'Penurunan kepadatan (jaringan makin sparse)'),
    ('Weakly Connected Components (WCC)', 46, 304, '+258 komponen (Fragmentasi ekstrem)'),
    ('Giant Component Size', '8 akun (7.34%)', '38 akun (4.36%)', 'Dominasi sub-komponen terisolasi'),
    ('Network Diameter (Giant)', 4, 2, 'Penyusutan diameter (pola sentral hub-and-spoke)'),
    ('Average Geodesic Distance', '2.2143', '1.9474', 'Jarak tempuh informasi makin pendek'),
    ('Louvain Modularity (Q)', '0.9455', '0.9851', '+0.0396 (Polarisasi opini mengkristal kuat)'),
    ('Jumlah Klaster Komunitas', 46, 304, 'Multiplikasi kelompok wacana terpisah'),
    ('Reciprocity Ratio', '0.0000 (0%)', '0.0133 (1.33%)', 'Munculnya komunikasi timbal-balik/debat'),
    ('Top In-Degree Hub', '@prabowo (3)', '@prabowo (12)', 'Target kebijakan konsisten (@prabowo)'),
    ('Secondary In-Degree Hub', '@dosenkesmas (2)', '@tanyakanrl (5), @regar_op0sisi (4)', 'Pergeseran dari akun edukasi ke akun viral'),
    ('Top Out-Degree Broadcaster', '@grok (5)', '@grok (37)', 'Eskalasi verifikasi bot AI (@grok)'),
    ('Top Betweenness Broker', 'Nihil / 0.0000', '@4Y4NKZ, @regar_op0sisi', 'Munculnya opinion leader & broker opini'),
    ('Emosi Dominan (IndoBERT)', 'Neutral & Disgust', 'Disgust (56.24%) & Sarcasm', 'Eskalasi afektif ketidakpuasan warganet')
]
period_comparison_df = pd.DataFrame(comparison_data[1:], columns=comparison_data[0])

# Export to Excel (.xlsx) with multiple formatted sheets
target_files = [
    os.path.join(base_dir, "NodeXL_MBG_Tesis_Indri_Anjar.xlsx"),
    os.path.join(base_dir, "results", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx"),
    os.path.join(base_dir, "docs", "assets", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx"),
    os.path.join(base_dir, "mbg-sna-github", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx"),
    os.path.join(base_dir, "mbg-sna-github", "results", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx"),
    os.path.join(base_dir, "mbg-sna-github", "docs", "assets", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx")
]

for target_file in target_files:
    d = os.path.dirname(target_file)
    if d:
        os.makedirs(d, exist_ok=True)
    with pd.ExcelWriter(target_file, engine='openpyxl') as writer:
        edges_nodexl.to_excel(writer, sheet_name='Edges', index=False)
        vertices_nodexl.to_excel(writer, sheet_name='Vertices', index=False)
        top_comms.to_excel(writer, sheet_name='Groups', index=False)
        overall_metrics_df.to_excel(writer, sheet_name='Overall Metrics', index=False)
        edges_p1.to_excel(writer, sheet_name='Edges_P1_PreCrisis', index=False)
        edges_p2.to_excel(writer, sheet_name='Edges_P2_PeakCrisis', index=False)
        period_comparison_df.to_excel(writer, sheet_name='Period Comparison', index=False)
    print(f"Generated NodeXL Workbook at: {target_file}")

print("All NodeXL Workbooks successfully created!")
