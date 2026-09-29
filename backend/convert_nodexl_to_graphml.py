from pathlib import Path
import pandas as pd
import networkx as nx

# ============================================================
# PATH
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

XLSX = ROOT / "NodeXL_MBG_Tesis_Indri_Anjar.xlsx"
OUT_DIR = ROOT / "data" / "processed"

GRAPHML = OUT_DIR / "nodexl_graph.graphml"
METRICS = OUT_DIR / "network_metrics.csv"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOAD NODEXL WORKBOOK
# ============================================================

print("=" * 60)
print("NODEXL → GRAPHML CONVERTER")
print("=" * 60)

print(f"Input : {XLSX}")

if not XLSX.exists():
    raise FileNotFoundError(
        f"File NodeXL tidak ditemukan:\n{XLSX}"
    )

edges = pd.read_excel(
    XLSX,
    sheet_name="Edges"
)

vertices = pd.read_excel(
    XLSX,
    sheet_name="Vertices"
)

print(f"Edges    : {len(edges):,}")
print(f"Vertices : {len(vertices):,}")

# ============================================================
# VALIDATE COLUMNS
# ============================================================

required_edges = [
    "Vertex 1",
    "Vertex 2",
]

required_vertices = [
    "Vertex",
]

for column in required_edges:
    if column not in edges.columns:
        raise ValueError(
            f"Kolom Edges tidak ditemukan: {column}"
        )

for column in required_vertices:
    if column not in vertices.columns:
        raise ValueError(
            f"Kolom Vertices tidak ditemukan: {column}"
        )

# ============================================================
# CREATE DIRECTED GRAPH
# ============================================================

G = nx.DiGraph()

# ============================================================
# ADD VERTICES + NODEXL ATTRIBUTES
# ============================================================

vertex_columns = [
    "Label",
    "Color",
    "Shape",
    "Size",
    "Alpha",
    "Community",
    "Degree Centrality",
    "Betweenness Centrality",
    "Dominant Emotion (IndoBERT)",
]

for _, row in vertices.iterrows():

    vertex = row["Vertex"]

    if pd.isna(vertex):
        continue

    vertex = str(vertex)

    attributes = {}

    for column in vertex_columns:
        if column not in vertices.columns:
            continue
        value = row[column]
        if pd.isna(value):
            continue
        if isinstance(value, (float, int)):
            attributes[column] = float(value)
        else:
            attributes[column] = str(value)
    G.add_node(vertex, **attributes)

# ============================================================
# ADD EDGES
# ============================================================

edge_columns = [
    "Color",
    "Width",
    "Style",
    "Opacity",
    "Relationship",
]

for _, row in edges.iterrows():
    source = row["Vertex 1"]
    target = row["Vertex 2"]
    if pd.isna(source) or pd.isna(target):
        continue
    source = str(source)
    target = str(target)
    attributes = {}
    for column in edge_columns:
        if column not in edges.columns:
            continue
        value = row[column]
        if pd.isna(value):
            continue
        if isinstance(value, (float, int)):
            attributes[column] = float(value)
        else:
            attributes[column] = str(value)
    G.add_edge(source, target, **attributes)

# ============================================================
# SAVE GRAPHML
# ============================================================

nx.write_graphml(G, GRAPHML)

# ============================================================
# CREATE METRICS CSV
# ============================================================

metrics = []
for node, attrs in G.nodes(data=True):
    metrics.append({
        "node": node,
        "label": attrs.get("Label"),
        "community": attrs.get("Community"),
        "degree_centrality": attrs.get("Degree Centrality"),
        "betweenness_centrality": attrs.get("Betweenness Centrality"),
        "dominant_emotion": attrs.get("Dominant Emotion (IndoBERT)"),
    })

metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv(METRICS, index=False)

# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("CONVERSION SELESAI")
print("=" * 60)
print(f"Nodes    : {G.number_of_nodes():,}")
print(f"Edges    : {G.number_of_edges():,}")
print(f"GraphML  : {GRAPHML}")
print(f"Metrics  : {METRICS}")
print("=" * 60)
