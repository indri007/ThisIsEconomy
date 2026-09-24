"""
ews/ews_engine.py
=================
Engine Inti Custom Early Warning System (EWS) v2 untuk Riset Tesis MBG.
Menyatukan analisis NLP (IndoBERT 7-Emosi, Sindiran/Sarkasme, Kata Kunci Krisis),
Statistik Runtut Waktu (Deteksi Anomali Z-Score & Volume Spikes),
serta Metrik Struktural SNA (Sentralitas Aktor & Partisi Komunitas).

BATASAN METODOLOGIS UTAMA:
- Skor EWS (0-100) adalah INDIKATOR INTENSITAS RISIKO WACANA PUBLIK BERBASIS DATASET,
  BUKAN prediksi kausal atau ramalan peristiwa masa depan.
- Seluruh perhitungan bersifat transparan, dapat diaudit, dan explainable.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
import pandas as pd

from ews.config import (
    DATA_PATHS,
    EWS_SCORE_LEVELS,
    EWS_WEIGHTS,
    INDOBERT_MODEL_METADATA,
)
from ews.emotion_analyzer import load_emotion_data, get_emotion_risk
from ews.sna_analyzer import load_sna_data, get_sna_summary
from ews.anomaly_detector import get_anomaly_metrics
from ews.keyword_analyzer import get_keyword_risk


def calculate_sarcasm_risk(sarcasm_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Menghitung kontribusi risiko sarkasme / sindiran (Maksimal 20 Poin).
    Berdasarkan rasio label 'sindiran' == True pada dataset validasi.
    """
    max_score = EWS_WEIGHTS["sarcasm_risk"]

    if sarcasm_df is None or sarcasm_df.empty:
        try:
            sarcasm_df = pd.read_csv(DATA_PATHS["sarcasm"])
        except Exception:
            return {
                "score": 0.0,
                "max_score": max_score,
                "total_rows": 0,
                "sarcasm_count": 0,
                "sarcasm_pct": 0.0,
                "explanation": "Dataset sindiran/sarkasme tidak tersedia."
            }

    total_rows = len(sarcasm_df)
    if total_rows == 0:
        return {
            "score": 0.0,
            "max_score": max_score,
            "total_rows": 0,
            "sarcasm_count": 0,
            "sarcasm_pct": 0.0,
            "explanation": "Dataset sindiran kosong."
        }

    # Kolom sindiran bertipe boolean / binary
    if "sindiran" in sarcasm_df.columns:
        sarcasm_count = int((sarcasm_df["sindiran"] == True).sum() + (sarcasm_df["sindiran"].astype(str).str.lower().isin(["1", "true", "ya"])).sum())
        # Pastikan tidak double count jika bool
        if sarcasm_df["sindiran"].dtype == bool:
            sarcasm_count = int(sarcasm_df["sindiran"].sum())
    else:
        sarcasm_count = 0

    sarcasm_pct = round((sarcasm_count / total_rows) * 100, 2)
    # Pada dataset 3.395 baris, ada 315 tweet sindiran (9.28%)
    # Rasio sindiran 20% dianggap memberikan skor penuh 20 poin
    score = min(round((sarcasm_pct / 20.0) * max_score, 1), max_score)

    explanation = (
        f"Teridentifikasi {sarcasm_count:,} cuitan sindiran/sarkasme ({sarcasm_pct}%) "
        f"dari {total_rows:,} cuitan terverifikasi. "
        f"Menyumbang {score}/{max_score} poin risiko EWS."
    )

    return {
        "score": score,
        "max_score": max_score,
        "total_rows": total_rows,
        "sarcasm_count": sarcasm_count,
        "sarcasm_pct": sarcasm_pct,
        "explanation": explanation
    }


def compute_custom_ews_v2(
    emotion_df: Optional[pd.DataFrame] = None,
    sna_df: Optional[pd.DataFrame] = None,
    sarcasm_df: Optional[pd.DataFrame] = None,
    anomaly_threshold: float = 2.0,
) -> Dict[str, Any]:
    """
    Menghitung skor EWS v2 secara holistik dan transparan.
    
    KOMPONEN BOBOT:
    1. Emotion Risk   : 0 - 30 Poin (Emosi Negatif IndoBERT)
    2. Sarcasm Risk   : 0 - 20 Poin (Rasio Sindiran/Sarkasme)
    3. Keyword Risk   : 0 - 20 Poin (Kata Kunci Krisis & Emoji Sinis)
    4. Volume Risk    : 0 - 15 Poin (Rasio Puncak Volume Harian)
    5. Anomaly Risk   : 0 - 15 Poin (Frekuensi Lonjakan Z-Score)
    ----------------------------------------------------------
    TOTAL             : 0 - 100 Poin
    """
    # 1. Muat dataset jika belum disediakan
    if emotion_df is None:
        emotion_df = load_emotion_data()
    if sna_df is None:
        sna_df = load_sna_data()

    # 2. Eksekusi Analisis Sub-Modul
    emotion_res = get_emotion_risk(emotion_df)
    sarcasm_res = calculate_sarcasm_risk(sarcasm_df)
    
    text_col = "text" if "text" in emotion_df.columns else "clean_text"
    texts = emotion_df[text_col] if text_col in emotion_df.columns else pd.Series()
    keyword_res = get_keyword_risk(texts)

    anomaly_res = get_anomaly_metrics(emotion_df, threshold=anomaly_threshold)
    sna_summary = get_sna_summary(sna_df)

    # 3. Agregasi Skor Terbobot
    score_emo = emotion_res["score"]
    score_sar = sarcasm_res["score"]
    score_kw = keyword_res["score"]
    score_vol = anomaly_res["volume_risk_score"]
    score_anom = anomaly_res["anomaly_risk_score"]

    raw_total = score_emo + score_sar + score_kw + score_vol + score_anom
    total_score = round(min(max(raw_total, 0.0), 100.0), 1)

    # 4. Tentukan Status & Level
    current_level = EWS_SCORE_LEVELS[0]
    for lvl in EWS_SCORE_LEVELS:
        low, high = lvl["range"]
        if low <= total_score <= high:
            current_level = lvl
            break

    # 5. Rekomendasi Aksi & Penjelasan Terperinci
    if total_score >= 75:
        action = "🔴 Tingkat Krisis Tinggi: Perlu respons strategis, klarifikasi terbuka, dan koordinasi cepat tim komunikasi publik."
    elif total_score >= 50:
        action = "🟠 Tingkat Bahaya Terdeteksi: Diperlukan klarifikasi proaktif atas keluhan fisik/higienis dan pelibatan figur terpercaya."
    elif total_score >= 25:
        action = "🟡 Tingkat Waspada: Pantau pergerakan isu, petakan simpul jembatan informasi, dan siapkan fakta komunikasi publik."
    else:
        action = "🟢 Tingkat Aman: Wacana publik dalam batas dinamika normal. Lanjutkan pemantauan berkala."

    explanation_points = [
        emotion_res["explanation"],
        sarcasm_res["explanation"],
        keyword_res["explanation"],
        anomaly_res["explanation"],
        (
            f"Jejaring SNA mencakup {sna_summary['communities_stat']['total_nodes']} simpul "
            f"dalam {sna_summary['communities_stat']['total_communities']} komunitas independen, "
            f"dengan akun sentralitas tertinggi seperti @{sna_summary['top_degree_actors'][0]['Label']}."
        )
    ]

    return {
        "score": total_score,
        "status": current_level["status"],
        "level_label": current_level["label"],
        "color": current_level["color"],
        "action_recommendation": action,
        "components": {
            "emotion_risk": {
                "score": score_emo,
                "max": EWS_WEIGHTS["emotion_risk"],
                "details": emotion_res
            },
            "sarcasm_risk": {
                "score": score_sar,
                "max": EWS_WEIGHTS["sarcasm_risk"],
                "details": sarcasm_res
            },
            "keyword_risk": {
                "score": score_kw,
                "max": EWS_WEIGHTS["keyword_risk"],
                "details": keyword_res
            },
            "volume_risk": {
                "score": score_vol,
                "max": EWS_WEIGHTS["volume_risk"],
                "details": anomaly_res
            },
            "anomaly_risk": {
                "score": score_anom,
                "max": EWS_WEIGHTS["anomaly_risk"],
                "details": anomaly_res
            }
        },
        "metrics": {
            "total_tweets": len(emotion_df),
            "dominant_emotion": emotion_res["dominant_emotion"],
            "dominant_pct": emotion_res["dominant_pct"],
            "negative_pct": emotion_res["negative_pct"],
            "sarcasm_rate_pct": sarcasm_res["sarcasm_pct"],
            "active_days": anomaly_res["active_days"],
            "spikes_count": anomaly_res["spikes_count"],
            "network_nodes": sna_summary["communities_stat"]["total_nodes"],
            "network_communities": sna_summary["communities_stat"]["total_communities"]
        },
        "sna_summary": sna_summary,
        "daily_anomaly_df": anomaly_res["daily_df"],
        "explanation": explanation_points,
        "note": "Indikator monitoring/risk signal berbasis dataset wacana MBG (analisis empiris)."
    }
