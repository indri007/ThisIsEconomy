#!/usr/bin/env python3
"""
run_inference_5909.py
---------------------
Menjalankan inferensi IndoBERT (Fine-tuned 9 Emosi) pada seluruh sisa cuitan (5.909 baris)
di dalam data/processed/mbg_tweets_master_clean.csv sehingga 100% dari 9.310 cuitan
memiliki label prediksi emosi yang lengkap.
"""

import os
import sys
import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

REPO_ROOT = "/Users/jevin/Documents/tesis_mbg"
CSV_PATH = os.path.join(REPO_ROOT, "data/processed/mbg_tweets_master_clean.csv")
PARQUET_PATH = os.path.join(REPO_ROOT, "data/processed/mbg_tweets_master_clean.parquet")
MODEL_PATH = os.path.join(REPO_ROOT, "results/indobert_finetuned_9_labels/checkpoint-792")

# Mapping label IndoBERT -> Bahasa Indonesia baku tesis
ID2LABEL_ENG = {
    0: 'anger',
    1: 'disgust',
    2: 'fear',
    3: 'joy',
    4: 'love',
    5: 'neutral',
    6: 'sadness',
    7: 'shame',
    8: 'surprise'
}

ENG2IDN = {
    'anger': 'Marah',
    'disgust': 'Jijik',
    'fear': 'Takut',
    'sadness': 'Sedih',
    'joy': 'Percaya',      # Joy / Kepercayaan / Apresiasi publik
    'neutral': 'Netral',
    'surprise': 'Kaget',
    'love': 'Percaya',      # Sesuai konvensi mapping tesis
    'shame': 'Tertarik'     # Sesuai konvensi mapping tesis
}

def main():
    print("="*65)
    print("🤖 INFERENSI INDOBERT 9-EMOSI PADA SISA DATA MBG MASTER (5.909 ROWS)")
    print("="*65)

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: {CSV_PATH} tidak ditemukan!")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH, low_memory=False)
    print(f"📊 Total baris dalam master dataset: {len(df):,}")

    # Cari baris yang belum memiliki label emosi
    mask_missing = df['predicted_emotion'].isna() | (df['predicted_emotion'].astype(str).str.strip() == '') | (df['predicted_emotion'].astype(str).str.lower() == 'nan')
    missing_count = mask_missing.sum()
    print(f"⏳ Cuitan yang belum berlabel emosi: {missing_count:,}")

    if missing_count == 0:
        print("✅ Seluruh 9.310 cuitan sudah memiliki label IndoBERT! Tidak perlu inferensi ulang.")
        return

    # Pilih device komputasi (Apple Silicon MPS / CUDA / CPU)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("⚡ Menggunakan akselerasi hardware: Apple Silicon GPU (MPS)")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print("⚡ Menggunakan akselerasi hardware: NVIDIA CUDA")
    else:
        device = torch.device("cpu")
        print("ℹ️ Menggunakan CPU")

    print(f"🔄 Memuat tokenizer dan model dari: {MODEL_PATH}")
    tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.to(device)
    model.eval()

    missing_indices = df[mask_missing].index.tolist()
    # Gunakan clean_text jika ada, jika tidak gunakan text
    texts_to_predict = [
        str(df.loc[idx, 'clean_text'] if pd.notna(df.loc[idx, 'clean_text']) and str(df.loc[idx, 'clean_text']).strip() != '' else df.loc[idx, 'text'])
        for idx in missing_indices
    ]

    batch_size = 64
    predicted_labels = []

    print(f"🚀 Menjalankan inferensi batch (batch_size={batch_size}) pada {len(texts_to_predict):,} teks...")
    
    with torch.no_grad():
        for i in tqdm(range(0, len(texts_to_predict), batch_size), desc="Inferensi IndoBERT"):
            batch_texts = texts_to_predict[i:i + batch_size]
            inputs = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=128,
                return_tensors="pt"
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            outputs = model(**inputs)
            preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
            
            for p in preds:
                eng_label = ID2LABEL_ENG.get(int(p), 'neutral')
                idn_label = ENG2IDN.get(eng_label, 'Netral')
                predicted_labels.append(idn_label)

    # Masukkan hasil prediksi ke dataframe
    df.loc[missing_indices, 'predicted_emotion'] = predicted_labels

    # Simpan kembali ke CSV dan Parquet
    df.to_csv(CSV_PATH, index=False)
    df.to_parquet(PARQUET_PATH, index=False)

    print("\n" + "="*65)
    print("✅ INFERENSI SELESAI DAN BERHASIL 100%!")
    print("="*65)
    print(f"💾 File tersimpan di:")
    print(f"   -> CSV    : {CSV_PATH} ({os.path.getsize(CSV_PATH)/(1024*1024):.2f} MB)")
    print(f"   -> Parquet: {PARQUET_PATH} ({os.path.getsize(PARQUET_PATH)/(1024*1024):.2f} MB)")

    print("\n📊 DISTRIBUSI LENGKAP 9 EMOSI INDOBERT (TOTAL 9.310 CUITAN):")
    dist = df['predicted_emotion'].value_counts()
    for emo, cnt in dist.items():
        pct = (cnt / len(df)) * 100
        print(f"   • {emo:<15}: {cnt:>5,} cuitan ({pct:>5.1f}%)")

if __name__ == "__main__":
    main()
