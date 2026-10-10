"""
scripts/auto_scrape_job.py
==========================
Skrip otomatis penarik data Twitter/X MBG (100 tweet per jadwal).
Didesain untuk dieksekusi secara terjadwal (Cron / Cloud Run Job)
setiap jam 07.00 dan jam 19.00 WIB.
Dilengkapi pengiriman laporan EWS otomatis via Bot Telegram.
"""

import os
import sys
import re
import time
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "twitter_sentiment_app"))

from twitter_sentiment_app.scraper import scrape_tweets_sync

OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "live_tweets_mbg_accumulated.csv"


def get_secret(key_name: str, default: str = None) -> str:
    """Membaca rahasia dari Streamlit Secrets, os.environ, atau file secrets.toml."""
    # 1. Streamlit Secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            return str(st.secrets[key_name]).strip()
    except Exception:
        pass

    # 2. Environment Variable
    val = os.getenv(key_name)
    if val:
        return val.strip()

    # 3. File .streamlit/secrets.toml manual parser
    secrets_path = PROJECT_ROOT / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{key_name} =") or line.startswith(f'{key_name}='):
                        raw_val = line.split("=", 1)[1].strip().strip('"\'')
                        if raw_val:
                            return raw_val
        except Exception:
            pass

    return default


import html

def send_telegram_ews_report(summary: dict) -> bool:
    """Mengirim ringkasan laporan EWS otomatis ke Telegram."""
    token = get_secret("TELEGRAM_BOT_TOKEN")
    chat_id = get_secret("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[TELEGRAM] Token atau Chat ID belum disetel, lewati pengiriman.")
        return False

    time_str = html.escape(str(summary.get("timestamp", "-")))
    added_str = html.escape(str(summary.get("added_count", 0)))
    total_str = f"{summary.get('total_records', 0):,}"
    risk_str = html.escape(str(summary.get("risk_level", "-")))
    keywords_str = html.escape(str(summary.get("top_keywords", "-")))
    sample_str = html.escape(str(summary.get("sample_tweet", "-")))
    action_str = html.escape(str(summary.get("action", "-")))

    message_text = (
        "🚨 <b>LAPORAN EWS MBG TERBARU</b>\n"
        f"⏰ <b>Waktu</b>: {time_str} WIB\n"
        "───────────────────────────────\n"
        f"📥 <b>Status Tarikan</b> : {added_str} Cuitan Baru\n"
        f"📊 <b>Total Database</b> : {total_str} Cuitan Akumulasi\n"
        f"⚠️ <b>Level Risiko EWS</b>: {risk_str}\n"
        f"🔥 <b>Kata Kunci Top</b> : {keywords_str}\n"
        "───────────────────────────────\n"
        f"💬 <b>Contoh Isu Warganet</b>:\n<i>{sample_str}</i>\n"
        "───────────────────────────────\n"
        f"💡 <b>Rekomendasi</b>: {action_str}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML"
    }

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                print(f"[TELEGRAM] ✅ Notifikasi laporan EWS berhasil dikirim ke Telegram! (percobaan {attempt})")
                return True
            elif resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
                print(f"[TELEGRAM] ⏳ Rate limited (HTTP 429). Menunggu {retry_after}s sebelum coba lagi...")
                time.sleep(retry_after)
            else:
                print(f"[TELEGRAM] ❌ Gagal mengirim (HTTP {resp.status_code}): {resp.text}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
        except Exception as e:
            print(f"[TELEGRAM] ⚠️ Error koneksi pada percobaan {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)

    return False


def analyze_new_batch(df: pd.DataFrame) -> dict:
    """Menganalisis batch cuitan baru untuk membuat ringkasan EWS."""
    crisis_vocab = [
        "keracunan", "mual", "muntah", "basi", "susu", "ulat", "lalat",
        "ompreng", "anggaran", "korupsi", "sppg", "diare", "gizi", "menu"
    ]
    
    keyword_counts = {}
    sample_text = "Tidak ada contoh cuitan."
    
    if not df.empty:
        # Cari cuitan yang relevan untuk contoh
        for t in df["text"].dropna():
            t_clean = str(t).strip().replace("\n", " ")
            if len(t_clean) > 30:
                sample_text = t_clean[:140] + ("..." if len(t_clean) > 140 else "")
                break

        # Hitung frekuensi kata kunci
        full_text = " ".join(df["text"].dropna().astype(str).str.lower())
        for kw in crisis_vocab:
            cnt = len(re.findall(r'\b' + re.escape(kw) + r'\b', full_text))
            if cnt > 0:
                keyword_counts[kw] = cnt

    # Urutkan top keywords
    sorted_kw = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:4]
    if sorted_kw:
        kw_str = ", ".join([f"{k} ({v}x)" for k, v in sorted_kw])
    else:
        kw_str = "Dinamika umum / netral"

    # Evaluasi level risiko sederhana
    has_medical = any(k in keyword_counts for k in ["keracunan", "muntah", "mual", "diare"])
    has_hygiene = any(k in keyword_counts for k in ["basi", "ulat", "lalat", "susu"])
    has_policy = any(k in keyword_counts for k in ["korupsi", "anggaran", "sppg", "ompreng"])

    if has_medical:
        risk_level = "🔴 KRITIS (Indikasi Isu Medis/Keracunan)"
        action = "Prioritaskan verifikasi kejadian medis di faskes setempat."
    elif has_hygiene:
        risk_level = "🟠 BAHAYA (Keluhan Higienitas Makanan)"
        action = "Lakukan audit standar pengolahan SPPG/katering terkait."
    elif has_policy:
        risk_level = "🟡 WASPADA (Diskusi Anggaran & Tata Kelola)"
        action = "Siapkan klarifikasi transparansi alokasi belanja program."
    else:
        risk_level = "🟢 KONDUSIF (Wacana Relatif Stabil)"
        action = "Lanjutkan pemantauan rutin pada jadwal berikutnya."

    return {
        "top_keywords": kw_str,
        "risk_level": risk_level,
        "action": action,
        "sample_tweet": sample_text
    }


def run_job(limit: int = 100):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[{now_str}] Memulai auto-scrape {limit} tweet MBG...")
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
        summary = {
            "timestamp": now_str,
            "added_count": 0,
            "total_records": 0,
            "risk_level": "🟢 AMAN (Nol Tarikan Baru)",
            "top_keywords": "Nihil",
            "sample_tweet": "Tidak ada cuitan baru saat tarikan terjadwal.",
            "action": "Tetap pantau pada jadwal penarikan selanjutnya."
        }
        send_telegram_ews_report(summary)
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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"[SAVED] {added_count} cuitan baru tersimpan. Total akumulasi: {len(combined_df)} baris.")

    # Analisis dan Kirim Laporan ke Bot Telegram
    analysis = analyze_new_batch(new_df)
    summary = {
        "timestamp": now_str,
        "added_count": added_count,
        "total_records": len(combined_df),
        "risk_level": analysis["risk_level"],
        "top_keywords": analysis["top_keywords"],
        "sample_tweet": analysis["sample_tweet"],
        "action": analysis["action"]
    }
    
    send_telegram_ews_report(summary)
    return True


if __name__ == "__main__":
    success = run_job(limit=100)
    sys.exit(0 if success else 1)
