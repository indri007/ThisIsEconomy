import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_communities_summary():
    try:
        nodes_path = os.path.join(PROJECT_ROOT, "data", "results", "mbg_network_nodes_final.csv")
        df_nodes = pd.read_csv(nodes_path)
        
        community_counts = df_nodes['Community'].value_counts().reset_index()
        community_counts.columns = ['community', 'size']
        
        top_communities = community_counts.head(10).to_dict(orient='records')
        largest_community = top_communities[0] if len(top_communities) > 0 else {"community": 0, "size": 0}
        
        total_communities = 342
        modularity = 0.9837
        
        return {
            "total_communities": total_communities,
            "modularity": modularity,
            "largest_community": largest_community,
            "distribution": top_communities
        }
    except Exception as e:
        return {"error": str(e)}
