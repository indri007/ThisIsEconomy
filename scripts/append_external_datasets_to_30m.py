#!/usr/bin/env python3
"""
append_external_datasets_to_30m.py
==================================
Menggabungkan 4 sumber data eksternal:
  1. dataset_mbg.csv (25.000 baris)
  2. tweets__makanan_bergizi_gratis_OR_mbg_20251104_231922.csv (1.220 baris)
  3. tweets_Makan_Bergizi_Gratis_20251104_224406.csv (440 baris)
  4. Public Opinion Dataset on MBG Program.csv dari file ZIP (7.462 baris)

Harmonisasi ke skema target:
  [id, created_at, author_username, author_id, text, like_count, retweet_count, reply_count, quote_count, source]

Deduplikasi berdasarkan 'id', lalu di-append langsung ke:
  data/processed/tweet_mbg_1juta.csv (Korpus 30 Juta).
"""

import os
import zipfile
import pandas as pd

def main():
    target_path = "/Users/jevin/Documents/tesis_mbg/data/processed/tweet_mbg_1juta.csv"
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"File target 30M tidak ditemukan: {target_path}")

    p_csv1 = '/Users/jevin/Downloads/dataset_mbg.csv'
    p_csv2 = '/Users/jevin/Downloads/tweets__makanan_bergizi_gratis_OR_mbg_20251104_231922.csv'
    p_csv3 = '/Users/jevin/Downloads/tweets_Makan_Bergizi_Gratis_20251104_224406.csv'
    p_zip = '/Users/jevin/Downloads/Public Opinion Dataset on X Social Media Regarding.zip'

    print("=" * 70)
    print("APPEND DATASET EKSTERNAL KE KORPUS 30 JUTA")
    print("=" * 70)

    rows = []

    # 1. dataset_mbg.csv
    print(f"[1] Membaca {p_csv1}...")
    df1 = pd.read_csv(p_csv1)
    for _, r in df1.iterrows():
        rows.append({
            'id': str(r.get('id', '')),
            'created_at': str(r.get('created_at', '')),
            'author_username': str(r.get('author_username', '')),
            'author_id': str(r.get('author_id', '')),
            'text': str(r.get('text', '')),
            'like_count': int(r.get('like_count', 0) if pd.notna(r.get('like_count')) else 0),
            'retweet_count': int(r.get('retweet_count', 0) if pd.notna(r.get('retweet_count')) else 0),
            'reply_count': int(r.get('reply_count', 0) if pd.notna(r.get('reply_count')) else 0),
            'quote_count': int(r.get('quote_count', 0) if pd.notna(r.get('quote_count')) else 0),
            'source': str(r.get('source', 'dataset_mbg'))
        })

    # 2. tweets__makanan...231922.csv
    print(f"[2] Membaca {p_csv2}...")
    df2 = pd.read_csv(p_csv2)
    for _, r in df2.iterrows():
        rows.append({
            'id': str(r.get('id', '')),
            'created_at': str(r.get('created_at', '')),
            'author_username': str(r.get('username', '')),
            'author_id': '',
            'text': str(r.get('text', '')),
            'like_count': int(r.get('favorite_count', 0) if pd.notna(r.get('favorite_count')) else 0),
            'retweet_count': int(r.get('retweet_count', 0) if pd.notna(r.get('retweet_count')) else 0),
            'reply_count': int(r.get('reply_count', 0) if pd.notna(r.get('reply_count')) else 0),
            'quote_count': int(r.get('quote_count', 0) if pd.notna(r.get('quote_count')) else 0),
            'source': 'Scraped MBG 231922'
        })

    # 3. tweets_Makan...224406.csv
    print(f"[3] Membaca {p_csv3}...")
    df3 = pd.read_csv(p_csv3)
    for _, r in df3.iterrows():
        rows.append({
            'id': str(r.get('id', '')),
            'created_at': str(r.get('created_at', '')),
            'author_username': str(r.get('username', '')),
            'author_id': '',
            'text': str(r.get('text', '')),
            'like_count': int(r.get('favorite_count', 0) if pd.notna(r.get('favorite_count')) else 0),
            'retweet_count': int(r.get('retweet_count', 0) if pd.notna(r.get('retweet_count')) else 0),
            'reply_count': int(r.get('reply_count', 0) if pd.notna(r.get('reply_count')) else 0),
            'quote_count': int(r.get('quote_count', 0) if pd.notna(r.get('quote_count')) else 0),
            'source': 'Scraped MBG 224406'
        })

    # 4. ZIP CSV
    print(f"[4] Membaca file CSV dari ZIP: {p_zip}...")
    with zipfile.ZipFile(p_zip) as z:
        for name in z.namelist():
            if name.endswith('.csv'):
                with z.open(name) as f:
                    df4 = pd.read_csv(f)
                    for _, r in df4.iterrows():
                        rows.append({
                            'id': str(r.get('id_str', r.get('conversation_id_str', ''))),
                            'created_at': str(r.get('created_at', '')),
                            'author_username': str(r.get('username', '')),
                            'author_id': str(r.get('user_id_str', '')),
                            'text': str(r.get('full_text', '')),
                            'like_count': int(r.get('favorite_count', 0) if pd.notna(r.get('favorite_count')) else 0),
                            'retweet_count': int(r.get('retweet_count', 0) if pd.notna(r.get('retweet_count')) else 0),
                            'reply_count': int(r.get('reply_count', 0) if pd.notna(r.get('reply_count')) else 0),
                            'quote_count': int(r.get('quote_count', 0) if pd.notna(r.get('quote_count')) else 0),
                            'source': 'Public Opinion Dataset ZIP'
                        })

    df_combined = pd.DataFrame(rows)
    print(f"Total baris terkumpul mentah: {len(df_combined)}")

    # Deduplikasi berdasarkan ID
    df_combined = df_combined.drop_duplicates(subset=['id']).reset_index(drop=True)
    print(f"Total baris unik setelah deduplikasi ID: {len(df_combined)}")

    # Urutkan kolom sesuai skema 30M
    cols = ['id', 'created_at', 'author_username', 'author_id', 'text', 'like_count', 'retweet_count', 'reply_count', 'quote_count', 'source']
    df_combined = df_combined[cols]

    # Append ke file 30M
    print(f"\n[*] Melakukan append {len(df_combined)} baris ke {target_path}...")
    df_combined.to_csv(target_path, mode='a', header=False, index=False)
    print("[*] Selesai! Seluruh data baru telah berhasil digabungkan ke korpus 30 juta.")

if __name__ == '__main__':
    main()
