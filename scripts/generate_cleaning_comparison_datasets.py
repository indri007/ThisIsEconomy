"""Script to extract, format, and generate side-by-side datasets:
Raw Uncleaned Data (~5,000 items) vs Cleaned Data (~5,000 items).
"""

from __future__ import annotations

import csv
import json
import os
import re
import sqlite3
from pathlib import Path

ROOT_DIR = Path("/Users/jevin/Documents/tesis_mbg")
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "database" / "published_journals.db"

SOURCE_CSV = DATA_DIR / "indobert_9_emosi_fixed.csv"
OUT_RAW_CSV = DATA_DIR / "data_mentah_belum_dicleaning_5272.csv"
OUT_CLEAN_CSV = DATA_DIR / "data_bersih_sudah_dicleaning_5272.csv"
OUT_COMPARE_CSV = DATA_DIR / "komparasi_sebelum_vs_sesudah_cleaning_5272.csv"
OUT_STATS_JSON = DATA_DIR / "statistik_cleaning_5272.json"

URL_REGEX = re.compile(r"https?://\S+|www\.\S+")
MENTION_REGEX = re.compile(r"@\w+")
HASHTAG_REGEX = re.compile(r"#\w+")
EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]",
    flags=re.UNICODE,
)


def main():
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Source file {SOURCE_CSV} does not exist.")

    raw_rows = []
    clean_rows = []
    compare_rows = []

    count_with_url = 0
    count_with_mention = 0
    count_with_emoji = 0
    count_with_hashtag = 0

    total_len_raw = 0
    total_len_clean = 0

    with open(SOURCE_CSV, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            tweet_id = row.get("id", "")
            raw_text = row.get("text", "")
            clean_text = row.get("clean_text", "")
            processed_text = row.get("processed_text", "")
            created_at = row.get("created_at", "")
            author_user = row.get("author_username", "")
            author_name = row.get("author_name", "")
            likes = row.get("like_count", "0")
            retweets = row.get("retweet_count", "0")
            replies = row.get("reply_count", "0")
            quotes = row.get("quote_count", "0")
            views = row.get("view_count", "0")
            emotion = row.get("predicted_emotion", "")

            # Diagnostics on raw text
            has_url = bool(URL_REGEX.search(raw_text))
            has_mention = bool(MENTION_REGEX.search(raw_text))
            has_hashtag = bool(HASHTAG_REGEX.search(raw_text))
            has_emoji = bool(EMOJI_REGEX.search(raw_text))

            if has_url:
                count_with_url += 1
            if has_mention:
                count_with_mention += 1
            if has_hashtag:
                count_with_hashtag += 1
            if has_emoji:
                count_with_emoji += 1

            len_raw = len(raw_text)
            len_clean = len(clean_text)
            diff_chars = len_raw - len_clean
            pct_reduction = (diff_chars / len_raw * 100) if len_raw > 0 else 0.0

            total_len_raw += len_raw
            total_len_clean += len_clean

            # 1. Raw item
            raw_rows.append(
                {
                    "no": idx,
                    "id": tweet_id,
                    "created_at": created_at,
                    "author_username": author_user,
                    "author_name": author_name,
                    "teks_mentah_belum_dicleaning": raw_text,
                    "like_count": likes,
                    "retweet_count": retweets,
                    "reply_count": replies,
                    "quote_count": quotes,
                    "view_count": views,
                }
            )

            # 2. Clean item
            clean_rows.append(
                {
                    "no": idx,
                    "id": tweet_id,
                    "created_at": created_at,
                    "author_username": author_user,
                    "teks_bersih_clean": clean_text,
                    "teks_normalisasi_indobert": processed_text,
                    "predicted_emotion": emotion,
                    "like_count": likes,
                    "retweet_count": retweets,
                }
            )

            # 3. Comparative side-by-side item
            compare_rows.append(
                {
                    "no": idx,
                    "id": tweet_id,
                    "created_at": created_at,
                    "author_username": author_user,
                    "teks_sebelum_cleaning": raw_text,
                    "teks_sesudah_cleaning": clean_text,
                    "teks_normalisasi_indobert": processed_text,
                    "panjang_sebelum": len_raw,
                    "panjang_sesudah": len_clean,
                    "karakter_dihapus": diff_chars,
                    "persentase_reduksi": f"{pct_reduction:.1f}%",
                    "memuat_url": "Ya" if has_url else "Tidak",
                    "memuat_mention": "Ya" if has_mention else "Tidak",
                    "memuat_emoji": "Ya" if has_emoji else "Tidak",
                    "memuat_hashtag": "Ya" if has_hashtag else "Tidak",
                    "predicted_emotion": emotion,
                }
            )

    total_records = len(raw_rows)

    # Write CSVs
    with open(OUT_RAW_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(raw_rows[0].keys()))
        writer.writeheader()
        writer.writerows(raw_rows)

    with open(OUT_CLEAN_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(clean_rows[0].keys()))
        writer.writeheader()
        writer.writerows(clean_rows)

    with open(OUT_COMPARE_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(compare_rows[0].keys()))
        writer.writeheader()
        writer.writerows(compare_rows)

    stats = {
        "total_records": total_records,
        "rata_rata_panjang_karakter_sebelum": round(total_len_raw / total_records, 2),
        "rata_rata_panjang_karakter_sesudah": round(total_len_clean / total_records, 2),
        "rata_rata_reduksi_karakter": round((total_len_raw - total_len_clean) / total_records, 2),
        "persentase_reduksi_total": f"{((total_len_raw - total_len_clean) / total_len_raw * 100):.2f}%",
        "jumlah_tweet_memuat_url": count_with_url,
        "persen_tweet_memuat_url": f"{(count_with_url / total_records * 100):.2f}%",
        "jumlah_tweet_memuat_mention": count_with_mention,
        "persen_tweet_memuat_mention": f"{(count_with_mention / total_records * 100):.2f}%",
        "jumlah_tweet_memuat_emoji": count_with_emoji,
        "persen_tweet_memuat_emoji": f"{(count_with_emoji / total_records * 100):.2f}%",
        "jumlah_tweet_memuat_hashtag": count_with_hashtag,
        "persen_tweet_memuat_hashtag": f"{(count_with_hashtag / total_records * 100):.2f}%",
    }

    with open(OUT_STATS_JSON, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # Insert into SQLite Database
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS mbg_tweets_cleaning_comparison (
            no INTEGER PRIMARY KEY,
            tweet_id TEXT NOT NULL,
            created_at TIMESTAMP,
            author_username TEXT,
            teks_sebelum_cleaning TEXT NOT NULL,
            teks_sesudah_cleaning TEXT NOT NULL,
            teks_normalisasi_indobert TEXT NOT NULL,
            panjang_sebelum INTEGER,
            panjang_sesudah INTEGER,
            karakter_dihapus INTEGER,
            persentase_reduksi TEXT,
            memuat_url TEXT,
            memuat_mention TEXT,
            memuat_emoji TEXT,
            memuat_hashtag TEXT,
            predicted_emotion TEXT
        );
        """
        )

        cur.execute("DELETE FROM mbg_tweets_cleaning_comparison;")

        cur.executemany(
            """
        INSERT INTO mbg_tweets_cleaning_comparison VALUES (
            :no, :id, :created_at, :author_username, :teks_sebelum_cleaning,
            :teks_sesudah_cleaning, :teks_normalisasi_indobert, :panjang_sebelum,
            :panjang_sesudah, :karakter_dihapus, :persentase_reduksi,
            :memuat_url, :memuat_mention, :memuat_emoji, :memuat_hashtag, :predicted_emotion
        )
        """,
            compare_rows,
        )

        conn.commit()
        conn.close()
        print(f"Stored {len(compare_rows)} rows into SQLite table mbg_tweets_cleaning_comparison.")

    print(f"Generated {OUT_RAW_CSV.name} ({total_records} rows)")
    print(f"Generated {OUT_CLEAN_CSV.name} ({total_records} rows)")
    print(f"Generated {OUT_COMPARE_CSV.name} ({total_records} rows)")
    print(f"Generated {OUT_STATS_JSON.name}")


if __name__ == "__main__":
    main()
