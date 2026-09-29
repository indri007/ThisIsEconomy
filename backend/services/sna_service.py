import os
import pandas as pd
import networkx as nx

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_sna_summary():
    try:
        SNA_EDGES_PATH = os.path.join(PROJECT_ROOT, "data", "network_edges.csv")
        df_e = pd.read_csv(SNA_EDGES_PATH)
        G_d = nx.DiGraph()
        for _, row in df_e.iterrows():
            G_d.add_edge(row['Source'], row['Target'])
            
        nodes = G_d.number_of_nodes()
        edges = G_d.number_of_edges()
        
        # Hardcoded metrik global dari NodeXL
        communities = 342
        modularity = 0.9837
        
        return {
            "nodes": nodes,
            "edges": edges,
            "communities": communities,
            "modularity": modularity
        }
    except Exception as e:
        return {"error": str(e)}

def get_network_data():
    try:
        nodes_path = os.path.join(PROJECT_ROOT, "data", "results", "mbg_network_nodes_final.csv")
        edges_path = os.path.join(PROJECT_ROOT, "data", "results", "mbg_network_edges_final.csv")
        
        df_nodes = pd.read_csv(nodes_path)
        df_edges = pd.read_csv(edges_path)
        
        df_nodes = df_nodes.sort_values(by="Degree", ascending=False).head(300)
        valid_nodes = set(df_nodes['Id'].astype(str))
        
        nodes = []
        for _, row in df_nodes.iterrows():
            nodes.append({
                "data": {
                    "id": str(row['Id']),
                    "label": str(row['Label']),
                    "degree": float(row['Degree']),
                    "community": int(row['Community']) if not pd.isna(row['Community']) else 0,
                    "emotion": str(row.get('Dominant_Emotion', 'neutral'))
                }
            })
            
        edges = []
        for _, row in df_edges.iterrows():
            source = str(row['Source'])
            target = str(row['Target'])
            if source in valid_nodes and target in valid_nodes:
                edges.append({
                    "data": {
                        "source": source,
                        "target": target,
                        "weight": float(row.get('Weight', 1.0))
                    }
                })
                
        return {"elements": nodes + edges}
    except Exception as e:
        return {"error": str(e)}
