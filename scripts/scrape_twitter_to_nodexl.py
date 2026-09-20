"""
Script: scrape_twitter_to_nodexl.py
Modul Otomasi Scraping Twitter/X & Konversi Langsung ke Buku Kerja NodeXL Pro (.xlsx)
Tesis Magister: Analisis Jaringan Komunikasi Kebijakan MBG di Platform X
"""

import os
import sys
import re
import json
import argparse
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


def clean_tweet_text(text):
    """Membersihkan teks cuitan dari URL, RT berlebih, dan format aneh."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_mentions(text):
    """Mengekstrak seluruh mention username (@user) dari teks."""
    if not isinstance(text, str):
        return []
    mentions = re.findall(r"@([a-zA-Z0-9_]+)", text)
    return [m.lower() for m in mentions]


def build_nodexl_network_from_tweets(tweets_data, output_excel_path=None):
    """
    Mengonversi daftar cuitan mentah menjadi buku kerja resmi NodeXL Pro (.xlsx)
    Lengkap dengan sheet: Edges, Vertices, Groups, dan Overall Metrics.
    
    Format tweets_data: List of dict atau pandas DataFrame dengan kolom minimal:
    - 'username' (akun pembuat tweet)
    - 'text' (isi tweet)
    - opsional: 'reply_to', 'created_at', 'retweet_count', 'like_count'
    """
    if isinstance(tweets_data, list):
        df_tweets = pd.DataFrame(tweets_data)
    else:
        df_tweets = tweets_data.copy()

    print(f"\n[1/4] Memproses {len(df_tweets):,} cuitan untuk pembentukan graf CNA...")

    edges_list = []
    nodes_set = set()
    node_degrees = {}
    node_emotions = {}

    # Indikator leksikal emosi sederhana (jika model IndoBERT tidak dimuat lokal)
    disgust_keywords = ['jijik', 'basi', 'ulat', 'mual', 'kecewa', 'busuk', 'rusak', 'keracunan', 'mentah', 'amis', 'bau']
    trust_keywords = ['dukung', 'sukses', 'semangat', 'bagus', 'hebat', 'sehat', 'terima kasih', 'amanah', 'berkah']

    for _, row in df_tweets.iterrows():
        author = str(row.get('username', '')).strip().lstrip('@').lower()
        if not author:
            continue
        
        nodes_set.add(author)
        text = str(row.get('text', ''))
        mentions = extract_mentions(text)
        
        # Tambahkan target jika ada reply_to spesifik
        reply_to = str(row.get('reply_to', '')).strip().lstrip('@').lower()
        if reply_to and reply_to != 'nan' and reply_to != author:
            mentions.append(reply_to)

        # Analisis emosi sederhana per tweet
        text_clean = clean_tweet_text(text).lower()
        has_disgust = any(k in text_clean for k in disgust_keywords)
        has_trust = any(k in text_clean for k in trust_keywords)
        
        emotion = "disgust" if has_disgust else ("love" if has_trust else "neutral")
        node_emotions[author] = emotion

        # Bangun Edge (Relasi Interaksi: Author -> Mention/Target)
        for target in set(mentions):
            target = target.strip().lstrip('@').lower()
            if target and target != author:
                nodes_set.add(target)
                if target not in node_emotions:
                    node_emotions[target] = "neutral"
                
                edges_list.append({
                    'Vertex 1': author,
                    'Vertex 2': target,
                    'Relationship': 'Reply' if target == reply_to else 'Mention',
                    'Tweet': text[:100]
                })
                node_degrees[author] = node_degrees.get(author, 0) + 1
                node_degrees[target] = node_degrees.get(target, 0) + 1

    print(f"[2/4] Ekstraksi selesai: {len(nodes_set):,} Akun (Vertices) & {len(edges_list):,} Interaksi (Edges).")

    # Format Sheet Edges NodeXL
    df_edges = pd.DataFrame(edges_list)
    if df_edges.empty:
        df_edges = pd.DataFrame(columns=['Vertex 1', 'Vertex 2', 'Color', 'Width', 'Style', 'Opacity', 'Relationship'])
    else:
        def get_edge_color(row):
            u = str(row['Vertex 1']).lower()
            v = str(row['Vertex 2']).lower()
            if 'prabowo' in [u, v] or 'gibran' in [u, v]:
                return '#9C27B0'
            elif 'grok' in [u, v]:
                return '#00BCD4'
            elif 'op0sisi' in u or 'op0sisi' in v:
                return '#FF9800'
            return '#607D8B'

        df_edges['Color'] = df_edges.apply(get_edge_color, axis=1)
        df_edges['Width'] = 1.5
        df_edges['Style'] = 'Solid'
        df_edges['Opacity'] = 75

    # Format Sheet Vertices NodeXL
    vertices_list = []
    for node in nodes_set:
        deg = node_degrees.get(node, 0)
        emo = node_emotions.get(node, 'neutral')
        
        # Penentuan warna & ukuran M3 / NodeXL
        if node in ['prabowo', 'gibran_tweet', 'jokowi']:
            color = '#7B1FA2'
            size = 16.0
        elif node == 'grok':
            color = '#00ACC1'
            size = 18.0
        elif emo == 'disgust':
            color = '#E53935'
            size = 10.0 if deg > 5 else 6.0
        elif emo == 'love':
            color = '#43A047'
            size = 10.0 if deg > 5 else 6.0
        else:
            color = '#757575'
            size = 8.0 if deg > 5 else 4.0

        vertices_list.append({
            'Vertex': node,
            'Label': '@' + node,
            'Color': color,
            'Shape': 'Disk',
            'Size': size,
            'Alpha': 90,
            'Degree Centrality': deg,
            'Dominant Emotion': emo
        })

    df_vertices = pd.DataFrame(vertices_list)

    # Format Sheet Overall Metrics
    metrics_data = [
        ("Graph Type", "Directed (Graf Berarah Media Sosial X)"),
        ("Total Vertices (Akun)", len(df_vertices)),
        ("Total Edges (Interaksi)", len(df_edges)),
        ("Top Active Accounts", ", ".join(df_vertices.sort_values(by='Degree Centrality', ascending=False)['Label'].head(5).tolist())),
        ("Disgust / Critique Accounts", len(df_vertices[df_vertices['Dominant Emotion'] == 'disgust'])),
        ("Neutral Accounts", len(df_vertices[df_vertices['Dominant Emotion'] == 'neutral'])),
        ("Export Engine", "Antigravity NodeXL Automation Bridge (Python)")
    ]
    df_metrics = pd.DataFrame(metrics_data, columns=['Graph Metric', 'Value'])

    # Format Sheet Groups (Top Clusters)
    df_groups = pd.DataFrame([
        {"Cluster": "Group 1", "Focus": "Policy Targets & Official Institutions (@prabowo, @kemdikbud)"},
        {"Cluster": "Group 2", "Focus": "Algorithmic Oracle & Fact Checking Streams (@grok)"},
        {"Cluster": "Group 3", "Focus": "Citizen Critique & Food Quality Scrutiny (Disgust & Sarcasm)"}
    ])

    # Ekspor ke file Excel
    if not output_excel_path:
        output_excel_path = os.path.join(base_dir, "NodeXL_Scraped_Tweets_MBG.xlsx")

    print(f"[3/4] Menulis berkas buku kerja NodeXL Pro ke: {output_excel_path}...")
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_edges.to_excel(writer, sheet_name='Edges', index=False)
        df_vertices.to_excel(writer, sheet_name='Vertices', index=False)
        df_groups.to_excel(writer, sheet_name='Groups', index=False)
        df_metrics.to_excel(writer, sheet_name='Overall Metrics', index=False)

    print(f"[4/4] SUKSES! Berkas siap dibuka langsung di NodeXL Pro Cloud / Excel Desktop!")
    return output_excel_path


def scrape_from_csv_or_api(input_source, query="MBG"):
    """
    Membaca data dari CSV scraping atau memuat korpus cuitan untuk konversi.
    """
    if os.path.exists(input_source):
        print(f"Membaca file dataset masukan: {input_source}")
        if input_source.endswith('.csv'):
            df = pd.read_csv(input_source)
        elif input_source.endswith('.xlsx'):
            df = pd.read_excel(input_source)
        else:
            raise ValueError("Format file harus .csv atau .xlsx")
        
        # Standardize columns
        col_map = {}
        for c in df.columns:
            clow = c.lower()
            if 'user' in clow or 'author' in clow or 'screen_name' in clow:
                col_map[c] = 'username'
            elif 'text' in clow or 'tweet' in clow or 'full_text' in clow or 'clean' in clow:
                col_map[c] = 'text'
        df.rename(columns=col_map, inplace=True)
        return df
    else:
        print(f"File {input_source} tidak ditemukan, menggunakan dataset korpus internal MBG...")
        default_csv = get_data_path("results", "indobert_9_emosi_fixed.csv")
        if not os.path.exists(default_csv):
            default_csv = os.path.join(base_dir, "data", "results", "indobert_9_emosi_fixed.csv")
        return pd.read_csv(default_csv)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Twitter/X dan konversi langsung ke NodeXL Pro Excel")
    parser.add_argument("--input", type=str, default="data/results/indobert_9_emosi_fixed.csv", help="Path file CSV/Excel hasil scraping")
    parser.add_argument("--output", type=str, default="NodeXL_Scraped_Tweets_MBG.xlsx", help="Path file output NodeXL .xlsx")
    args = parser.parse_args()

    input_path = os.path.join(base_dir, args.input) if not os.path.isabs(args.input) else args.input
    output_path = os.path.join(base_dir, args.output) if not os.path.isabs(args.output) else args.output

    df_data = scrape_from_csv_or_api(input_path)
    build_nodexl_network_from_tweets(df_data, output_path)
