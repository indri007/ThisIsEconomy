"""
Script: export_nodexl_workbook.py
Menghasilkan buku kerja Microsoft Excel resmi format NodeXL Pro (.xlsx)
dari data empiris Tesis MBG: |V|=971 nodes, |E|=666 edges, Louvain Modularity Q=0.9837.
"""

import os
import sys
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
# NodeXL mandatory columns for Edges: 'Vertex 1', 'Vertex 2'
edges_nodexl = pd.DataFrame()
edges_nodexl['Vertex 1'] = edges_df['Source'].astype(str)
edges_nodexl['Vertex 2'] = edges_df['Target'].astype(str)
edges_nodexl['Color'] = '#446084'  # NodeXL classic primary blue
edges_nodexl['Width'] = 1.5
edges_nodexl['Style'] = 'Solid'
edges_nodexl['Opacity'] = 75
edges_nodexl['Relationship'] = 'Mention / Retweet'

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

# Export to Excel (.xlsx) with multiple formatted sheets
output_root = os.path.join(base_dir, "NodeXL_MBG_Tesis_Indri_Anjar.xlsx")
output_results = os.path.join(base_dir, "results", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx")
output_assets = os.path.join(base_dir, "docs", "assets", "NodeXL_MBG_Tesis_Indri_Anjar.xlsx")

for target_file in [output_root, output_results, output_assets]:
    with pd.ExcelWriter(target_file, engine='openpyxl') as writer:
        edges_nodexl.to_excel(writer, sheet_name='Edges', index=False)
        vertices_nodexl.to_excel(writer, sheet_name='Vertices', index=False)
        top_comms.to_excel(writer, sheet_name='Groups', index=False)
        overall_metrics_df.to_excel(writer, sheet_name='Overall Metrics', index=False)
    print(f"Generated NodeXL Workbook at: {target_file}")

print("All NodeXL Workbooks successfully created!")
