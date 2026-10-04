"""
scripts/auto_scrape_job.py
==========================
Skrip otomatis penarik data Twitter/X MBG (100 tweet per jadwal).
Didesain untuk dieksekusi secara terjadwal (Cron / Cloud Run Job)
setiap jam 07.00 dan jam 19.00 WIB.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "twitter_sentiment_app"))

from twitter_sentiment_app.scraper import scrape_tweets_sync

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "live_tweets_mbg_accumulated.csv"

def run_job(limit: int = 100):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memulai auto-scrape {limit} tweet MBG...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        new_df = scrape_tweets_sync(
            keyword='MBG OR "Makan Bergizi Gratis"',
            limit=limit,
            product="Latest"
        )
    except Exception as e:
        print(f"[ERROR] Gagal menarik data: {e}")
        return False

    if new_df.empty:
        print("[INFO] Tidak ada cuitan baru yang ditemukan.")
        return True

    print(f"[SUCCESS] Berhasil menarik {len(new_df)} cuitan.")

    # Gabungkan dengan data akumulasi sebelumnya dan buang duplikat berdasarkan tweet_id
    if OUTPUT_FILE.exists():
        try:
            existing_df = pd.read_csv(OUTPUT_FILE)
            combined_df = pd.concat([new_df, existing_df], ignore_index=True)
            combined_df.drop_duplicates(subset=["tweet_id"], keep="first", inplace=True)
            added_count = len(combined_df) - len(existing_df)
        except Exception:
            combined_df = new_df
            added_count = len(new_df)
    else:
        combined_df = new_df
        added_count = len(new_df)

    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"[SAVED] {added_count} cuitan baru tersimpan. Total akumulasi data: {len(combined_df)} baris.")
    print(f"[PATH] Lokasi berkas: {OUTPUT_FILE}")
    return True

if __name__ == "__main__":
    success = run_job(limit=100)
    sys.exit(0 if success else 1)
