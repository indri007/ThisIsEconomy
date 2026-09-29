#!/usr/bin/env python3
"""
build_master_dataset.py
-----------------------
Menggabungkan seluruh dataset crawling & scraping MBG (8.700 gabungan, 5.310 crawlingori,
3.700 mbg_tweets1, 1.829 apify baru, dan 5.263 indobert labeled) menjadi satu Master Dataset
bersih tanpa duplikat: data/processed/mbg_tweets_master_clean.csv & .parquet.
"""

import os
import re
import pandas as pd
import numpy as np

REPO_ROOT = "/Users/jevin/Documents/tesis_mbg"
RAW_DIR = os.path.join(REPO_ROOT, "data/raw/scrape_all")
OUTPUT_DIR = os.path.join(REPO_ROOT, "data/processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_tweet_text(text):
    if not isinstance(text, str):
        return ""
    # Hapus URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Hapus mention @user
    text = re.sub(r'@\w+', '', text)
    # Hapus whitespace berlebih dan newlines berulang
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_text_for_dedup(text):
    if not isinstance(text, str):
        return ""
    t = clean_tweet_text(text).lower()
    # Hapus tanda baca untuk pencocokan deduplikasi
    t = re.sub(r'[^\w\s]', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def main():
    print("="*60)
    print("🚀 MEMULAI PEMBUATAN MASTER DATASET MBG")
    print("="*60)

    # 1. Muat mapping label emosi dari indobert_9_emosi_fixed.csv
    emotion_map = {}
    indobert_file = os.path.join(RAW_DIR, "indobert_9_emosi_fixed.csv")
    if os.path.exists(indobert_file):
        df_indobert = pd.read_csv(indobert_file, low_memory=False)
        print(f"📖 Memuat {len(df_indobert)} data berlabel dari indobert_9_emosi_fixed.csv")
        for _, r in df_indobert.iterrows():
            txt = str(r.get('text', '')).strip()
            pred = r.get('predicted_emotion')
            if txt and pd.notna(pred):
                norm_key = normalize_text_for_dedup(txt)
                if norm_key:
                    emotion_map[norm_key] = str(pred).strip()
        print(f"✅ Berhasil memetakan {len(emotion_map)} teks unik berlabel emosi IndoBERT.")

    # 2. Daftar file prioritas
    source_configs = [
        ("mbg_tweets_gabungan.csv", "gabungan_8700"),
        ("crawlingori5310.csv", "crawling_5310"),
        ("mbg_tweets1.csv", "mbg_tweets_3700"),
        ("apify_x_scraper_2026-09-13.csv", "apify_2026_09_13"),
        ("indobert_9_emosi_fixed.csv", "indobert_labeled")
    ]

    all_records = []

    for fname, src_tag in source_configs:
        fpath = os.path.join(RAW_DIR, fname)
        if not os.path.exists(fpath):
            print(f"⚠️ Melewati {fname} (file tidak ditemukan)")
            continue

        print(f"\n📂 Memproses: {fname}...")
        df = pd.read_csv(fpath, low_memory=False)

        # Deteksi nama kolom secara dinamis
        id_col = next((c for c in ['id', 'tweet_id', 'id_str', 'id_tweet'] if c in df.columns), None)
        text_col = next((c for c in ['full_text', 'text', 'tweet'] if c in df.columns), None)
        created_col = next((c for c in ['created_at', 'createdAt', 'date', 'timestamp'] if c in df.columns), None)
        user_col = next((c for c in ['author_username', 'user/username', 'username', 'screen_name'] if c in df.columns), None)
        name_col = next((c for c in ['author_name', 'user/name', 'name'] if c in df.columns), None)

        like_col = next((c for c in ['like_count', 'favorite_count', 'likes'] if c in df.columns), None)
        rt_col = next((c for c in ['retweet_count', 'retweets'] if c in df.columns), None)
        reply_col = next((c for c in ['reply_count', 'replies'] if c in df.columns), None)
        quote_col = next((c for c in ['quote_count', 'quotes'] if c in df.columns), None)
        view_col = next((c for c in ['view_count', 'views'] if c in df.columns), None)

        for _, row in df.iterrows():
            txt = str(row[text_col]).strip() if text_col and pd.notna(row[text_col]) else ""
            if not txt or txt.lower() == "nan":
                continue

            tid = str(row[id_col]).strip() if id_col and pd.notna(row[id_col]) else ""
            created = str(row[created_col]).strip() if created_col and pd.notna(row[created_col]) else ""
            user = str(row[user_col]).strip() if user_col and pd.notna(row[user_col]) else ""
            name = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else ""

            likes = row[like_col] if like_col and pd.notna(row[like_col]) else 0
            rts = row[rt_col] if rt_col and pd.notna(row[rt_col]) else 0
            replies = row[reply_col] if reply_col and pd.notna(row[reply_col]) else 0
            quotes = row[quote_col] if quote_col and pd.notna(row[quote_col]) else 0
            views = row[view_col] if view_col and pd.notna(row[view_col]) else 0

            norm_t = normalize_text_for_dedup(txt)
            emo = emotion_map.get(norm_t, None)
            if emo is None and 'predicted_emotion' in row and pd.notna(row['predicted_emotion']):
                emo = str(row['predicted_emotion']).strip()

            all_records.append({
                'tweet_id': tid,
                'created_at': created,
                'author_username': user,
                'author_name': name,
                'text': txt,
                'clean_text': clean_tweet_text(txt),
                'like_count': int(pd.to_numeric(likes, errors='coerce') or 0),
                'retweet_count': int(pd.to_numeric(rts, errors='coerce') or 0),
                'reply_count': int(pd.to_numeric(replies, errors='coerce') or 0),
                'quote_count': int(pd.to_numeric(quotes, errors='coerce') or 0),
                'view_count': int(pd.to_numeric(views, errors='coerce') or 0),
                'predicted_emotion': emo,
                'source_dataset': src_tag,
                '_norm_text': norm_t
            })

    df_combined = pd.DataFrame(all_records)
    print(f"\n📊 Total baris gabungan terkumpul: {len(df_combined):,}")

    # 3. Deduplikasi berdasarkan teks ternormalisasi (prioritaskan baris yang memiliki predicted_emotion)
    df_combined['has_emotion'] = df_combined['predicted_emotion'].notna().astype(int)
    df_combined.sort_values(by=['has_emotion', 'like_count'], ascending=[False, False], inplace=True)
    df_master = df_combined.drop_duplicates(subset=['_norm_text']).copy()
    df_master.drop(columns=['_norm_text', 'has_emotion'], inplace=True)
    df_master.reset_index(drop=True, inplace=True)

    print(f"🎯 Total Baris Master UNIK: {len(df_master):,}")
    print(f"🏷️ Tweet dengan label emosi IndoBERT: {df_master['predicted_emotion'].notna().sum():,}")

    # Simpan file Master CSV & Parquet
    master_csv = os.path.join(OUTPUT_DIR, "mbg_tweets_master_clean.csv")
    master_parquet = os.path.join(OUTPUT_DIR, "mbg_tweets_master_clean.parquet")

    df_master.to_csv(master_csv, index=False)
    df_master.to_parquet(master_parquet, index=False)

    print(f"\n💾 Disimpan ke:")
    print(f"   -> CSV    : {master_csv} ({os.path.getsize(master_csv)/(1024*1024):.2f} MB)")
    print(f"   -> Parquet: {master_parquet} ({os.path.getsize(master_parquet)/(1024*1024):.2f} MB)")

    print("\n📈 Distribusi Emosi pada Master Dataset:")
    print(df_master['predicted_emotion'].value_counts(dropna=False))

    print("\n✅ SELESAI DENGAN SUKSES!")

if __name__ == "__main__":
    main()
