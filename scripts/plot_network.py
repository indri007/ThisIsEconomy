import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

print("Generating SNA visual...")
edges_df = pd.read_csv(get_result_path('mbg_network_edges_final.csv'))
nodes_df = pd.read_csv(get_result_path('mbg_network_nodes_final.csv'))

G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target', create_using=nx.DiGraph())

degrees = dict(G.degree())

plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)

node_sizes = [v * 10 for v in degrees.values()]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)
nx.draw_networkx_edges(G, pos, alpha=0.2, arrows=False)

plt.title('MBG Network Fragmentation on X (Mar-May 2026)', fontsize=16)
plt.axis('off')
plt.tight_layout()

out_path = get_result_path("network_graph.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Saved SNA visual to {out_path}")
