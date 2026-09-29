import os
import re
import pandas as pd
import emoji
from fastapi import HTTPException

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cache dataframes to avoid reading multiple times per request
_DATA = {}

def get_merged_data():
    if "merged" in _DATA:
        return _DATA["merged"]
        
    # 1. Main Data (Emotions & Text)
    main_path = os.path.join(PROJECT_ROOT, "data", "results", "indobert_9_emosi_fixed.csv")
    df_main = pd.read_csv(main_path)
    
    # 2. Sarcasm Data
    sarcasm_path = os.path.join(PROJECT_ROOT, "data", "sarcasm", "dataset_sindiran_valid.csv")
    if os.path.exists(sarcasm_path):
        df_sarcasm = pd.read_csv(sarcasm_path)
        # Ensure ID format matches
        df_sarcasm['id'] = df_sarcasm['id'].astype(str)
        df_main['id'] = df_main['id'].astype(str)
        df_sarcasm['is_sarcasm'] = df_sarcasm['sindiran'].astype(str).str.lower().isin(['true', '1', 'ya'])
        # Merge Sarcasm
        df_merged = pd.merge(df_main, df_sarcasm[['id', 'is_sarcasm']], on='id', how='left')
    else:
        df_merged = df_main.copy()
        df_merged['is_sarcasm'] = False
        
    # 3. Community Data (Nodes)
    nodes_path = os.path.join(PROJECT_ROOT, "data", "results", "mbg_network_nodes_final.csv")
    if os.path.exists(nodes_path):
        df_nodes = pd.read_csv(nodes_path)
        df_nodes['Id'] = df_nodes['Id'].astype(str)
        df_merged['author_username'] = df_merged['author_username'].astype(str)
        # Rename Id to author_username for merge
        df_nodes = df_nodes.rename(columns={'Id': 'author_username'})
        df_merged = pd.merge(df_merged, df_nodes[['author_username', 'Community']], on='author_username', how='left')
    else:
        df_merged['Community'] = -1

    # Fill NaN for boolean/int
    df_merged['is_sarcasm'] = df_merged['is_sarcasm'].fillna(False)
    
    _DATA["merged"] = df_merged
    return df_merged

def aggregate_stats(filtered_df):
    total = len(filtered_df)
    
    # Emotion
    emotion_counts = filtered_df['predicted_emotion'].value_counts().reset_index()
    emotion_counts.columns = ['label', 'count']
    emotions = emotion_counts.to_dict(orient='records')
    
    # Sarcasm
    sarcasm_counts = filtered_df['is_sarcasm'].value_counts().to_dict()
    sarcasm_true = sarcasm_counts.get(True, 0)
    sarcasm_false = sarcasm_counts.get(False, 0)
    
    # Communities
    community_counts = filtered_df['Community'].value_counts().reset_index()
    community_counts.columns = ['community', 'count']
    # Filter out missing communities (NaN or -1) if needed, but keeping is fine
    communities = community_counts.head(10).to_dict(orient='records')
    
    # Top Actors
    actor_counts = filtered_df['author_username'].value_counts().reset_index()
    actor_counts.columns = ['actor', 'count']
    top_actors = actor_counts.head(10).to_dict(orient='records')
    
    return {
        "total_tweets": total,
        "emotions": emotions,
        "sarcasm": {
            "sarkasme": sarcasm_true,
            "non_sarkasme": sarcasm_false
        },
        "communities": communities,
        "top_actors": top_actors
    }

def explore_hashtag(hashtag: str):
    try:
        df = get_merged_data()
        
        # Exact match for hashtag (case insensitive)
        query = f"#{hashtag.lower()}"
        
        def has_hashtag(text):
            if pd.isna(text): return False
            # extract all hashtags
            tags = re.findall(r'#\w+', str(text).lower())
            return query in tags
            
        mask = df['text'].apply(has_hashtag)
        filtered = df[mask]
        
        res = aggregate_stats(filtered)
        res["keyword"] = f"#{hashtag}"
        return res
    except Exception as e:
        return {"error": str(e)}

def explore_emoji(emoji_char: str):
    try:
        df = get_merged_data()
        
        def has_emoji(text):
            if pd.isna(text): return False
            return emoji_char in str(text)
            
        mask = df['text'].apply(has_emoji)
        filtered = df[mask]
        
        res = aggregate_stats(filtered)
        res["keyword"] = emoji_char
        return res
    except Exception as e:
        return {"error": str(e)}
