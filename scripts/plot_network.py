import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

print("Generating SNA visual...")
edges_df = pd.read_csv('/Users/jevin/Documents/tesis_mbg/results/mbg_network_edges_final.csv')
nodes_df = pd.read_csv('/Users/jevin/Documents/tesis_mbg/results/mbg_network_nodes_final.csv')

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

out_path = "/Users/jevin/.gemini/antigravity-ide/brain/2e99ce0b-957c-493e-b5b4-d776646dfc7a/network_graph.png"
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Saved SNA visual to {out_path}")
