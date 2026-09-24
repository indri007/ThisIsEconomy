"""
ews/emotion_analyzer.py
=======================
Modul Analisis Emosi IndoBERT untuk Custom EWS v2.
Menganalisis distribusi 7 label emosi aktual dari hasil inferensi model
dan menghitung kontribusi risiko emosi terhadap skor peringatan dini.
"""

from __future__ import annotations
from typing import Dict, Any, Tuple
import pandas as pd
from ews.config import DATA_PATHS, INDOBERT_MODEL_METADATA, EWS_WEIGHTS


def load_emotion_data(filepath: str | None = None) -> pd.DataFrame:
    """
    Memuat dataset inferensi emosi IndoBERT.
    Default path: data/results/indobert_9_emosi_fixed.csv
    """
    path = filepath or DATA_PATHS["emotion"]
    try:
        df = pd.read_csv(path)
        return df
    except Exception as exc:
        raise RuntimeError(f"Gagal memuat dataset emosi dari {path}: {exc}")


def get_emotion_distribution(df: pd.DataFrame) -> Dict[str, int]:
    """
    Menghitung frekuensi kemunculan setiap kelas emosi aktual.
    """
    if "predicted_emotion" not in df.columns:
        raise ValueError("Kolom 'predicted_emotion' tidak ditemukan dalam DataFrame.")
    counts = df["predicted_emotion"].value_counts().to_dict()
    return counts


def get_emotion_percentages(df: pd.DataFrame) -> Dict[str, float]:
    """
    Menghitung persentase setiap kelas emosi aktual (dibulatkan 2 desimal).
    """
    total = len(df)
    if total == 0:
        return {}
    counts = get_emotion_distribution(df)
    return {k: round((v / total) * 100, 2) for k, v in counts.items()}


def get_dominant_emotion(df: pd.DataFrame) -> Tuple[str, int, float]:
    """
    Mengidentifikasi emosi yang paling dominan dalam korpus beserta frekuensi dan persentasenya.
    Contoh output: ('Jijik', 2960, 56.24)
    """
    counts = get_emotion_distribution(df)
    if not counts:
        return ("Unknown", 0, 0.0)
    dominant_label = max(counts, key=counts.get)
    dominant_count = counts[dominant_label]
    dominant_pct = round((dominant_count / len(df)) * 100, 2)
    return (dominant_label, dominant_count, dominant_pct)


def get_emotion_risk(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Menghitung kontribusi risiko emosi terhadap skor EWS (Maksimal 30 Poin).
    
    FORMULA TRANSPARAN:
    - Emosi Berisiko Tinggi (Negative Risk): 'Jijik', 'Marah', 'Takut', 'Sedih'
    - Emosi Konstruktif / Netral: 'Percaya', 'Netral', 'Tertarik'
    - Rasio Emosi Negatif (%) = sum(Negative Labels) / Total Tweets * 100
    - Skor Risiko Emosi = (Rasio Negatif / 100) * EWS_WEIGHTS['emotion_risk']
    """
    total = len(df)
    if total == 0:
        return {
            "score": 0.0,
            "max_score": EWS_WEIGHTS["emotion_risk"],
            "negative_count": 0,
            "negative_pct": 0.0,
            "dominant_emotion": "Unknown",
            "distribution": {},
            "percentages": {},
            "explanation": "Dataset kosong."
        }

    counts = get_emotion_distribution(df)
    percentages = get_emotion_percentages(df)
    dominant_label, dominant_count, dominant_pct = get_dominant_emotion(df)

    neg_labels = INDOBERT_MODEL_METADATA["negative_risk_labels"]
    negative_count = sum(counts.get(lbl, 0) for lbl in neg_labels)
    negative_pct = round((negative_count / total) * 100, 2)

    max_score = EWS_WEIGHTS["emotion_risk"]
    # Perhitungan skor risiko proporsional
    score = round((negative_pct / 100.0) * max_score, 1)

    explanation = (
        f"Emosi negatif mencapai {negative_pct}% ({negative_count:,} dari {total:,} cuitan), "
        f"didominasi oleh '{dominant_label}' ({dominant_pct}%). "
        f"Menyumbang {score}/{max_score} poin risiko EWS."
    )

    return {
        "score": score,
        "max_score": max_score,
        "negative_count": negative_count,
        "negative_pct": negative_pct,
        "dominant_emotion": dominant_label,
        "dominant_count": dominant_count,
        "dominant_pct": dominant_pct,
        "distribution": counts,
        "percentages": percentages,
        "actual_labels_count": len(counts),
        "explanation": explanation
    }
