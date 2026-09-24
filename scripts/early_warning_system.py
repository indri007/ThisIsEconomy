"""
early_warning_system.py
=======================
Sistem Peringatan Dini (Early Warning System / EWS) Mandiri
untuk Pemantauan Wacana Program Makan Bergizi Gratis (MBG).

CARA PAKAI:
    python3 scripts/early_warning_system.py
    python3 scripts/early_warning_system.py --csv data/sarcasm/dataset_sindiran_valid.csv
    python3 scripts/early_warning_system.py --csv data/sarcasm/dataset_sindiran_valid.csv --json

FUNGSI:
    1. Memindai frekuensi kata kunci krisis (keracunan, basi, dll.)
    2. Mendeteksi lonjakan emoji sarkasme (🤡, 🙃, 🤮, dsb.)
    3. Menghitung distribusi sentimen & sarkasme dari data lokal
    4. Menghasilkan skor risiko EWS (0–100) + label status
    5. Mencetak laporan terstruktur ke terminal (+ opsi JSON)

PENULIS:
    Indri Anjar Kartika Sari — MBG SNA Research 2026
    Universitas Pembangunan Nasional "Veteran" Jawa Timur
"""

import os
import sys
import re
import json
import argparse
from collections import Counter
from datetime import datetime
from typing import Optional

import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI AMBANG BATAS (THRESHOLD)
# ─────────────────────────────────────────────────────────────────────────────

THRESHOLDS = {
    # Kata kunci krisis Tier-1 (berat, bobot x3)
    "tier1_keywords": [
        "keracunan", "dirawat", "pingsan", "masuk rs", "mati", "meninggal",
        "ambulans", "rumah sakit", "opname", "gawat darurat",
    ],
    # Kata kunci krisis Tier-2 (sedang, bobot x2)
    "tier2_keywords": [
        "basi", "busuk", "belatung", "ulat", "kotor", "menjijikkan", "korupsi",
        "fiktif", "vendor bodong", "vendor fiktif", "dihentikan", "ditutup",
        "dibekukan", "ditangguhkan", "sppg",
    ],
    # Kata kunci krisis Tier-3 (ringan, bobot x1)
    "tier3_keywords": [
        "kecewa", "malu", "gagal", "bohong", "janji", "tidak sesuai", "kurang",
        "tidak layak", "tidak bergizi", "tidak enak", "hambar", "tipuan",
        "kebohongan", "omong kosong", "harapan palsu",
    ],
    # Emoji sarkasme (bobot x2 masing-masing)
    "sarcasm_emojis": [
        "🤡", "🙃", "🤮", "🤢", "😒", "😑", "😤", "🤬",
        "💀", "☠️", "🗑️", "🚮", "👎", "🤦", "😅", "🙄",
    ],
    # Emoji positif palsu (indikator sarkasme pragmatik, bobot x1.5)
    "fake_positive_emojis": [
        "😍", "🥰", "👍", "🎉", "✨", "🌟", "❤️", "🥺", "😊",
    ],
    # Ambang batas volume (per 100 tweet)
    "crisis_keyword_rate_danger":  5.0,   # % → BAHAYA
    "crisis_keyword_rate_warning": 2.0,   # % → WASPADA
    "sarcasm_emoji_rate_danger":  10.0,   # % → BAHAYA
    "sarcasm_emoji_rate_warning":  4.0,   # % → WASPADA
    "neg_sentiment_pct_danger":   70.0,   # % → BAHAYA
    "neg_sentiment_pct_warning":  50.0,   # % → WASPADA
    "sarcasm_pct_danger":         60.0,   # % → BAHAYA
    "sarcasm_pct_warning":        40.0,   # % → WASPADA
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Deteksi path file CSV
# ─────────────────────────────────────────────────────────────────────────────

def find_csv(custom_path: Optional[str] = None) -> Optional[str]:
    """Cari file CSV terbaik yang tersedia di direktori proyek."""
    if custom_path and os.path.exists(custom_path):
        return custom_path

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(project_root, "data", "results", "indobert_9_emosi_fixed.csv"),
        os.path.join(project_root, "data", "sarcasm", "dataset_sindiran_valid.csv"),
        os.path.join(project_root, "data", "indobert_9_emosi_fixed.csv"),
        os.path.join(project_root, "data", "emotion", "mbg_tweets_indobert_ready.csv"),
        os.path.join(project_root, "results", "indobert_9_emosi_fixed.csv"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def load_dataframe(csv_path: str) -> pd.DataFrame:
    """Muat CSV dengan encoding fallback."""
    for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            return df
        except (UnicodeDecodeError, Exception):
            continue
    raise ValueError(f"Tidak dapat membaca file: {csv_path}")


def detect_text_column(df: pd.DataFrame) -> Optional[str]:
    """Deteksi otomatis kolom teks tweet."""
    for col in ["text", "tweet", "konten", "content", "tweet_text",
                "full_text", "clean_text", "processed_text"]:
        if col in df.columns:
            return col
    # Pilih kolom string terpanjang
    str_cols = [c for c in df.columns if df[c].dtype == object]
    if str_cols:
        return max(str_cols, key=lambda c: df[c].str.len().mean() if df[c].str.len().mean() > 0 else 0)
    return None


def detect_sentiment_column(df: pd.DataFrame) -> Optional[str]:
    for col in ["sentiment", "sentimen", "label_sentimen", "emotion", "label",
                "predicted_emotion", "emosi", "emotion_label"]:
        if col in df.columns:
            return col
    return None


def detect_sarcasm_column(df: pd.DataFrame) -> Optional[str]:
    for col in ["sarcasm", "sarkasme", "label_sarkasme", "is_sarcasm",
                "sarcasm_label", "sindiran", "label_sindiran"]:
        if col in df.columns:
            return col
    return None


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI ANALISIS
# ─────────────────────────────────────────────────────────────────────────────

def count_crisis_keywords(texts: pd.Series) -> dict:
    """Hitung frekuensi kata kunci krisis per tier."""
    combined = " ".join(texts.fillna("").astype(str).str.lower().tolist())
    result = {"tier1": {}, "tier2": {}, "tier3": {}}
    for kw in THRESHOLDS["tier1_keywords"]:
        cnt = combined.count(kw)
        if cnt > 0:
            result["tier1"][kw] = cnt
    for kw in THRESHOLDS["tier2_keywords"]:
        cnt = combined.count(kw)
        if cnt > 0:
            result["tier2"][kw] = cnt
    for kw in THRESHOLDS["tier3_keywords"]:
        cnt = combined.count(kw)
        if cnt > 0:
            result["tier3"][kw] = cnt
    return result


def count_sarcasm_emojis(texts: pd.Series) -> dict:
    """Hitung frekuensi emoji sarkasme dan emoji positif palsu."""
    all_text = " ".join(texts.fillna("").astype(str).tolist())
    sarcasm_counts = {}
    for emoji in THRESHOLDS["sarcasm_emojis"]:
        cnt = all_text.count(emoji)
        if cnt > 0:
            sarcasm_counts[emoji] = cnt
    fake_pos_counts = {}
    for emoji in THRESHOLDS["fake_positive_emojis"]:
        cnt = all_text.count(emoji)
        if cnt > 0:
            fake_pos_counts[emoji] = cnt
    return {"sarcasm": sarcasm_counts, "fake_positive": fake_pos_counts}


def analyze_sentiment(df: pd.DataFrame, col: Optional[str]) -> dict:
    """Hitung distribusi sentimen."""
    if col is None or col not in df.columns:
        return {"available": False}
    vc = df[col].fillna("unknown").astype(str).str.lower().value_counts()
    total = len(df)
    neg_labels = ["negatif", "negative", "disgust", "anger", "fear", "sadness", "jijik", "marah", "takut", "sedih"]
    pos_labels = ["positif", "positive", "joy", "surprise", "senang", "gembira", "terkejut"]
    neg = sum(vc.get(l, 0) for l in neg_labels)
    pos = sum(vc.get(l, 0) for l in pos_labels)
    neu = total - neg - pos
    return {
        "available": True,
        "total": total,
        "negative": neg,
        "positive": pos,
        "neutral": max(neu, 0),
        "neg_pct": round(neg / total * 100, 1) if total else 0,
        "pos_pct": round(pos / total * 100, 1) if total else 0,
        "top_labels": vc.head(10).to_dict(),
    }


def analyze_sarcasm(df: pd.DataFrame, col: Optional[str]) -> dict:
    """Hitung distribusi label sarkasme."""
    if col is None or col not in df.columns:
        return {"available": False}
    vc = df[col].fillna("unknown").astype(str).str.lower().value_counts()
    total = len(df)
    sarcasm_labels = ["sarcasm", "sarkas", "sindiran", "sarkasme", "1", "true", "ya", "yes"]
    sarcasm_cnt = sum(vc.get(l, 0) for l in sarcasm_labels)
    sarcasm_pct = round(sarcasm_cnt / total * 100, 1) if total else 0
    return {
        "available": True,
        "total": total,
        "sarcasm_count": sarcasm_cnt,
        "sarcasm_pct": sarcasm_pct,
        "top_labels": vc.head(5).to_dict(),
    }


def compute_ews_score(
    total_tweets: int,
    kw_counts: dict,
    emoji_counts: dict,
    sentiment: dict,
    sarcasm: dict,
) -> dict:
    """
    Hitung EWS Score (0–100) dari 4 komponen:
      - Komponen A: Kata kunci krisis      (0–30 poin)
      - Komponen B: Emoji sarkasme        (0–20 poin)
      - Komponen C: Rasio sentimen negatif (0–30 poin)
      - Komponen D: Rasio sarkasme        (0–20 poin)
    """
    N = max(total_tweets, 1)

    # Komponen A: Kata kunci krisis (bobot per tier)
    kw_weighted = (
        sum(kw_counts["tier1"].values()) * 3 +
        sum(kw_counts["tier2"].values()) * 2 +
        sum(kw_counts["tier3"].values()) * 1
    )
    kw_rate = kw_weighted / N * 100   # weighted hits per tweet (%)
    score_a = min(kw_rate / 15 * 30, 30)  # cap 15% weighted rate → 30 poin

    # Komponen B: Emoji sarkasme
    emoji_total = sum(emoji_counts["sarcasm"].values()) * 2 + sum(emoji_counts["fake_positive"].values())
    emoji_rate  = emoji_total / N * 100
    score_b = min(emoji_rate / 20 * 20, 20)

    # Komponen C: Sentimen negatif (berbasis emosi negatif aktual IndoBERT)
    if sentiment.get("available"):
        neg_pct = sentiment.get("neg_pct", 0.0)
    else:
        try:
            from ews.emotion_analyzer import load_emotion_data, get_emotion_risk
            emo_df = load_emotion_data()
            neg_pct = get_emotion_risk(emo_df)["negative_pct"]
        except Exception:
            neg_pct = 0.0
    score_c = min(neg_pct / 100 * 30, 30)

    # Komponen D: Sarkasme
    sar_pct = sarcasm.get("sarcasm_pct", 0) if sarcasm.get("available") else 0.0
    score_d = min(sar_pct / 100 * 20, 20)

    total_score = score_a + score_b + score_c + score_d

    if total_score >= 75:
        status = "🔴 KRITIS — AMBIL TINDAKAN SEGERA"
        action = "Aktifkan protokol krisis. Koordinasikan Humas BGN + Kemenkes dalam 24 jam."
    elif total_score >= 50:
        status = "🟠 BAHAYA — RESPONS CEPAT DIPERLUKAN"
        action = "Siapkan pernyataan resmi. Pantau perkembangan setiap 6 jam."
    elif total_score >= 25:
        status = "🟡 WASPADA — PEMANTAUAN INTENSIF"
        action = "Tingkatkan frekuensi pemantauan. Siapkan draf klarifikasi."
    else:
        status = "🟢 AMAN — SITUASI TERKENDALI"
        action = "Pemantauan rutin harian sudah cukup."

    return {
        "score": round(total_score, 1),
        "status": status,
        "action": action,
        "breakdown": {
            "A_crisis_keywords": round(score_a, 1),
            "B_sarcasm_emojis":  round(score_b, 1),
            "C_neg_sentiment":   round(score_c, 1),
            "D_sarcasm_rate":    round(score_d, 1),
        },
        "rates": {
            "kw_weighted_rate_pct": round(kw_rate, 2),
            "emoji_rate_pct":       round(emoji_rate, 2),
            "neg_sentiment_pct":    neg_pct,
            "sarcasm_pct":          sar_pct,
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# LAPORAN OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

BORDER = "═" * 70

def print_report(csv_path, df, kw_counts, emoji_counts, sentiment, sarcasm, ews):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
    print(f"\n{BORDER}")
    print(f"  📡 LAPORAN EARLY WARNING SYSTEM (EWS) — PROGRAM MBG")
    print(f"  Timestamp : {ts}")
    print(f"  Sumber    : {os.path.basename(csv_path)}")
    print(f"  Total Data: {len(df):,} tweet / entri")
    print(BORDER)

    # EWS Score
    print(f"\n  🚨 SKOR PERINGATAN DINI : {ews['score']}/100")
    print(f"  STATUS                  : {ews['status']}")
    print(f"  REKOMENDASI TINDAKAN    : {ews['action']}")
    print(f"\n  Breakdown Skor:")
    bd = ews['breakdown']
    rates = ews['rates']
    print(f"    A. Kata Kunci Krisis   : {bd['A_crisis_keywords']:>5.1f}/30  "
          f"(rate terbobot: {rates['kw_weighted_rate_pct']}%)")
    print(f"    B. Emoji Sarkasme      : {bd['B_sarcasm_emojis']:>5.1f}/20  "
          f"(rate: {rates['emoji_rate_pct']}%)")
    print(f"    C. Sentimen Negatif    : {bd['C_neg_sentiment']:>5.1f}/30  "
          f"({rates['neg_sentiment_pct']}% negatif)")
    print(f"    D. Rasio Sarkasme      : {bd['D_sarcasm_rate']:>5.1f}/20  "
          f"({rates['sarcasm_pct']}% sarkasme)")

    # Kata kunci
    print(f"\n{BORDER}")
    print("  ⚠️  DETEKSI KATA KUNCI KRISIS")
    print(BORDER)

    def _print_kw(tier_name, tier_key, weight):
        items = kw_counts[tier_key]
        total_hits = sum(items.values())
        icon = "🔴" if tier_key == "tier1" else ("🟠" if tier_key == "tier2" else "🟡")
        print(f"\n  {icon} {tier_name} (bobot ×{weight}) — {len(items)} kata terdeteksi, "
              f"{total_hits} total kemunculan:")
        if items:
            for kw, cnt in sorted(items.items(), key=lambda x: -x[1])[:10]:
                bar = "█" * min(cnt, 40)
                print(f"     {kw:<25} {cnt:>4}× | {bar}")
        else:
            print("     (tidak ada kata kunci krisis yang terdeteksi)")

    _print_kw("Tier 1 — KRITIS", "tier1", 3)
    _print_kw("Tier 2 — SERIUS", "tier2", 2)
    _print_kw("Tier 3 — RINGAN", "tier3", 1)

    # Emoji
    print(f"\n{BORDER}")
    print("  🎭 DETEKSI EMOJI SARKASME & SINYAL PRAGMATIK")
    print(BORDER)
    sar_emojis = emoji_counts["sarcasm"]
    print(f"\n  😡 Emoji Sarkasme Langsung ({sum(sar_emojis.values())} total):")
    if sar_emojis:
        for em, cnt in sorted(sar_emojis.items(), key=lambda x: -x[1]):
            print(f"     {em}  {cnt:>4}× kemunculan")
    else:
        print("     (tidak terdeteksi)")

    fk_emojis = emoji_counts["fake_positive"]
    print(f"\n  🎭 Emoji Positif Palsu / Sarkasme Implisit ({sum(fk_emojis.values())} total):")
    if fk_emojis:
        for em, cnt in sorted(fk_emojis.items(), key=lambda x: -x[1]):
            print(f"     {em}  {cnt:>4}× kemunculan")
    else:
        print("     (tidak terdeteksi)")

    # Sentimen
    print(f"\n{BORDER}")
    print("  💬 ANALISIS DISTRIBUSI SENTIMEN")
    print(BORDER)
    if sentiment.get("available"):
        tot = sentiment["total"]
        print(f"\n  Total entri : {tot:,}")
        print(f"  😡 Negatif  : {sentiment['negative']:>5,}  ({sentiment['neg_pct']}%)")
        print(f"  😊 Positif  : {sentiment['positive']:>5,}  ({sentiment['pos_pct']}%)")
        neu_pct = round(sentiment['neutral'] / tot * 100, 1) if tot else 0
        print(f"  😐 Netral   : {sentiment['neutral']:>5,}  ({neu_pct}%)")
        print(f"\n  Label terbanyak (Top 10):")
        for lbl, cnt in list(sentiment["top_labels"].items())[:10]:
            print(f"     {lbl:<30} {cnt:>5,}")
    else:
        print("  ⚠️  Kolom sentimen tidak ditemukan dalam dataset.")

    # Sarkasme
    print(f"\n{BORDER}")
    print("  🤡 ANALISIS DETEKSI SARKASME")
    print(BORDER)
    if sarcasm.get("available"):
        print(f"\n  Total entri    : {sarcasm['total']:,}")
        print(f"  Label Sarkasme : {sarcasm['sarcasm_count']:,}  ({sarcasm['sarcasm_pct']}%)")
        print(f"\n  Distribusi label sarkasme:")
        for lbl, cnt in sarcasm["top_labels"].items():
            print(f"     {lbl:<30} {cnt:>5,}")
    else:
        print("  ⚠️  Kolom sarkasme tidak ditemukan dalam dataset.")

    print(f"\n{BORDER}")
    print(f"  ✅ Laporan selesai dibuat — {ts}")
    print(f"{BORDER}\n")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Early Warning System (EWS) — Pemantauan Wacana MBG"
    )
    parser.add_argument("--csv",  type=str, default=None,
                        help="Path ke file CSV dataset tweet MBG")
    parser.add_argument("--json", action="store_true",
                        help="Ekspor hasil juga ke format JSON")
    parser.add_argument("--out",  type=str, default=None,
                        help="Path output JSON (default: results/ews_report.json)")
    args = parser.parse_args()

    # 1. Temukan file CSV
    csv_path = find_csv(args.csv)
    if csv_path is None:
        print("❌ File CSV dataset tidak ditemukan.")
        print("   Gunakan: python3 scripts/early_warning_system.py --csv <path/ke/file.csv>")
        sys.exit(1)

    print(f"\n📂 Memuat dataset: {csv_path}")
    df = load_dataframe(csv_path)
    print(f"✅ Dataset dimuat: {len(df):,} baris × {len(df.columns)} kolom")

    # 2. Deteksi kolom
    text_col  = detect_text_column(df)
    sent_col  = detect_sentiment_column(df)
    sarc_col  = detect_sarcasm_column(df)

    print(f"   Kolom teks      : {text_col or '(tidak ditemukan)'}")
    print(f"   Kolom sentimen  : {sent_col or '(tidak ditemukan)'}")
    print(f"   Kolom sarkasme  : {sarc_col or '(tidak ditemukan)'}")

    if text_col is None:
        print("❌ Kolom teks tidak ditemukan. Tidak dapat melanjutkan analisis.")
        sys.exit(1)

    texts = df[text_col]

    # 3. Analisis
    print("\n🔍 Memindai kata kunci krisis...")
    kw_counts    = count_crisis_keywords(texts)

    print("🎭 Mendeteksi emoji sarkasme...")
    emoji_counts = count_sarcasm_emojis(texts)

    print("💬 Menganalisis distribusi sentimen...")
    sentiment    = analyze_sentiment(df, sent_col)

    print("🤡 Menganalisis distribusi sarkasme...")
    sarcasm      = analyze_sarcasm(df, sarc_col)

    # 4. Hitung EWS
    print("🧮 Menghitung EWS Score...")
    ews = compute_ews_score(len(df), kw_counts, emoji_counts, sentiment, sarcasm)

    # 5. Cetak laporan
    print_report(csv_path, df, kw_counts, emoji_counts, sentiment, sarcasm, ews)

    # 6. Ekspor JSON (opsional)
    if args.json:
        out_path = args.out
        if out_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            out_path = os.path.join(project_root, "results", "ews_report.json")

        report = {
            "timestamp": datetime.now().isoformat(),
            "source_file": csv_path,
            "total_tweets": len(df),
            "ews": ews,
            "crisis_keywords": kw_counts,
            "emoji_analysis": emoji_counts,
            "sentiment": sentiment,
            "sarcasm": sarcasm,
        }
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
        print(f"📄 Laporan JSON disimpan ke: {out_path}")


if __name__ == "__main__":
    main()
