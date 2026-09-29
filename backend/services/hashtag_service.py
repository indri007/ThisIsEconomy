import os
import re
import pandas as pd
import emoji
from collections import Counter
import itertools
import networkx as nx

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "results", "indobert_9_emosi_fixed.csv")

def extract_hashtags_and_emojis():
    df = pd.read_csv(DATA_PATH)
    hashtag_pattern = re.compile(r'#\w+')
    
    tweets_data = []
    for text in df['text'].dropna():
        text_str = str(text)
        tags = list(set(hashtag_pattern.findall(text_str.lower())))
        emojis = list(set([c for c in text_str if emoji.is_emoji(c)]))
        tweets_data.append({"tags": tags, "emojis": emojis})
        
    return tweets_data

def get_hashtag_summary():
    try:
        tweets_data = extract_hashtags_and_emojis()
        hashtag_counter = Counter()
        for t in tweets_data:
            hashtag_counter.update(t["tags"])
            
        top_hashtags = [{"tag": tag, "count": count} for tag, count in hashtag_counter.most_common(20)]
        
        # Calculate global nodes and edges for co-occurrence
        G = nx.Graph()
        for t in tweets_data:
            tags = t["tags"]
            for tag in tags:
                G.add_node(tag)
            for combo in itertools.combinations(tags, 2):
                if G.has_edge(combo[0], combo[1]):
                    G[combo[0]][combo[1]]['weight'] += 1
                else:
                    G.add_edge(combo[0], combo[1], weight=1)
                    
        return {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "top_hashtags": top_hashtags
        }
    except Exception as e:
        return {"error": str(e)}

def get_hashtag_network():
    try:
        tweets_data = extract_hashtags_and_emojis()
        hashtag_counter = Counter()
        for t in tweets_data:
            hashtag_counter.update(t["tags"])
            
        # Limit to top 50 hashtags to avoid browser crash
        top_tags = {tag for tag, _ in hashtag_counter.most_common(50)}
        
        G = nx.Graph()
        for t in tweets_data:
            tags = [tag for tag in t["tags"] if tag in top_tags]
            for tag in tags:
                if not G.has_node(tag):
                    G.add_node(tag, frequency=hashtag_counter[tag])
            for combo in itertools.combinations(tags, 2):
                if G.has_edge(combo[0], combo[1]):
                    G[combo[0]][combo[1]]['weight'] += 1
                else:
                    G.add_edge(combo[0], combo[1], weight=1)
                    
        nodes = [{"data": {"id": n, "label": n, "frequency": G.nodes[n]['frequency']}} for n in G.nodes()]
        edges = [{"data": {"source": u, "target": v, "weight": d['weight']}} for u, v, d in G.edges(data=True)]
        
        return {"elements": nodes + edges}
    except Exception as e:
        return {"error": str(e)}

def get_emoji_summary():
    try:
        tweets_data = extract_hashtags_and_emojis()
        emoji_counter = Counter()
        for t in tweets_data:
            emoji_counter.update(t["emojis"])
            
        top_emojis = [{"emoji": em, "count": count} for em, count in emoji_counter.most_common(20)]
        
        G = nx.Graph()
        for t in tweets_data:
            emojis = t["emojis"]
            for em in emojis:
                G.add_node(em)
            for combo in itertools.combinations(emojis, 2):
                if G.has_edge(combo[0], combo[1]):
                    G[combo[0]][combo[1]]['weight'] += 1
                else:
                    G.add_edge(combo[0], combo[1], weight=1)
                    
        return {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "top_emojis": top_emojis
        }
    except Exception as e:
        return {"error": str(e)}

def get_emoji_network():
    try:
        tweets_data = extract_hashtags_and_emojis()
        emoji_counter = Counter()
        for t in tweets_data:
            emoji_counter.update(t["emojis"])
            
        top_emojis = {em for em, _ in emoji_counter.most_common(50)}
        
        G = nx.Graph()
        for t in tweets_data:
            emojis = [em for em in t["emojis"] if em in top_emojis]
            for em in emojis:
                if not G.has_node(em):
                    G.add_node(em, frequency=emoji_counter[em])
            for combo in itertools.combinations(emojis, 2):
                if G.has_edge(combo[0], combo[1]):
                    G[combo[0]][combo[1]]['weight'] += 1
                else:
                    G.add_edge(combo[0], combo[1], weight=1)
                    
        nodes = [{"data": {"id": n, "label": n, "frequency": G.nodes[n]['frequency']}} for n in G.nodes()]
        edges = [{"data": {"source": u, "target": v, "weight": d['weight']}} for u, v, d in G.edges(data=True)]
        
        return {"elements": nodes + edges}
    except Exception as e:
        return {"error": str(e)}
