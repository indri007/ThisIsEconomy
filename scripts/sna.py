import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import networkx as nx
import community.community_louvain as community_louvain
import re
from tqdm import tqdm

# --- 1. SETUP ---
print("=== Memulai Pipeline Inferensi & SNA (End-to-End) ===")
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

FILE_PATH = get_data_path("mbg_tweets_indobert_ready.xlsx")
MODEL_PATH = get_result_path("indobert_finetuned_9_labels/checkpoint-792")
OUT_NODES = get_result_path("mbg_network_nodes_final.csv")
OUT_EDGES = get_result_path("mbg_network_edges_final.csv")

# Label Emosi 9 Kelas (Harus urut sesuai hasil fine-tuning)
emotion_labels = ['anger', 'disgust', 'fear', 'joy', 'love', 'neutral', 'sadness', 'shame', 'surprise']
id2label = {i: label for i, label in enumerate(emotion_labels)}

# Device Mac M4 (MPS)
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(f"Menggunakan device: {device}")

# --- 2. LOAD DATA & PREPROCESSING (SASTRAWI) ---
print("\n[Tahap 1] Memuat Data & Preprocessing dengan Sastrawi...")
df = pd.read_excel(FILE_PATH)
df = df.dropna(subset=['text']).reset_index(drop=True)

# Sastrawi Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Kita lakukan preprocessing ringan & stemming (memakan waktu beberapa saat)
tqdm.pandas(desc="Sastrawi Stemming")
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#', '', text)
    # Stemming
    return stemmer.stem(text)

# (Opsional) Jika dirasa lama, kita bisa lewati stemming penuh. 
# Di sini kita terapkan ke data.
print(f"Mulai stemming {len(df)} baris data...")
df['stemmed_text'] = df['text_clean'].fillna(df['text']).progress_apply(preprocess_text)

# --- 3. KLASIFIKASI EMOSI (INDOBERT) ---
print("\n[Tahap 2] Memuat Model IndoBERT & Memprediksi Emosi...")
tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

predicted_labels = []
batch_size = 32

for i in tqdm(range(0, len(df), batch_size), desc="Inferensi IndoBERT"):
    batch_texts = df['stemmed_text'].iloc[i:i+batch_size].tolist()
    inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1).cpu().numpy()
        predicted_labels.extend([id2label[p] for p in preds])

df['predicted_emotion'] = predicted_labels
print(f"Inferensi selesai! Distribusi Emosi:\n{df['predicted_emotion'].value_counts()}")

# --- 4. SOCIAL NETWORK ANALYSIS (NETWORKX & LOUVAIN) ---
print("\n[Tahap 3] Membangun Graf Jaringan Sosial (SNA)...")

def extract_mentions(text):
    return re.findall(r'@(\w+)', str(text))

edges_list = []
# Kita gunakan teks asli untuk mendeteksi mention yang akurat
for _, row in df.iterrows():
    source = row['author_username']
    mentions = extract_mentions(row['text'])
    for target in mentions:
        edges_list.append((source, target))

G = nx.Graph()
if edges_list:
    G.add_edges_from(edges_list)
else:
    G.add_edge('dummy_source', 'dummy_target')

print(f"Graf terbentuk: {G.number_of_nodes()} Nodes, {G.number_of_edges()} Edges.")

print("Menghitung Metrik Sentralitas...")
degree_cent = nx.degree_centrality(G)
betweenness_cent = nx.betweenness_centrality(G)

print("Mendeteksi Komunitas (Louvain Algorithm)...")
partition = community_louvain.best_partition(G)

# --- 5. EXPORT HASIL ---
print("\n[Tahap 4] Menyimpan Hasil Final...")

# Nodes DataFrame
# Kita gabungkan metrik SNA dengan informasi user & emosi paling sering muncul
emotion_grouped = df.groupby('author_username')['predicted_emotion'].agg(lambda x: x.mode()[0] if not x.empty else 'neutral')

nodes_data = []
for node in G.nodes():
    nodes_data.append({
        'Id': node,
        'Label': node,
        'Degree': degree_cent.get(node, 0),
        'Betweenness': betweenness_cent.get(node, 0),
        'Community': partition.get(node, -1),
        'Dominant_Emotion': emotion_grouped.get(node, 'neutral')
    })
nodes_df = pd.DataFrame(nodes_data)
nodes_df.to_csv(OUT_NODES, index=False)

# Edges DataFrame
edges_df = pd.DataFrame(edges_list, columns=['Source', 'Target'])
edges_df.to_csv(OUT_EDGES, index=False)

print("✅ SELESAI!")
print(f"-> Data Nodes tersimpan di: {OUT_NODES}")
print(f"-> Data Edges tersimpan di: {OUT_EDGES}")
