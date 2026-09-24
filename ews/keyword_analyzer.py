"""
ews/keyword_analyzer.py
=======================
Modul Analisis Sinyal Kata Kunci Krisis, Emoji, & Tagar untuk Custom EWS v2.
Mendeteksi intensitas sinyal linguistik terkait diskursus risiko (Tier 1-3)
serta indikator pragmatik sarkasme.

BATASAN METODOLOGIS:
- Kemunculan kata kunci krisis adalah "Sinyal Deteksi Linguistik",
  BUKAN vonis otomatis krisis faktual.
- Diperlukan triangulasi antara teks, sentimen emosi, dan lonjakan volume.
"""

from __future__ import annotations
import re
from typing import Dict, Any, List, Tuple
from collections import Counter
import pandas as pd
from ews.config import CRISIS_KEYWORDS, SARCASM_EMOJIS, FAKE_POSITIVE_EMOJIS, EWS_WEIGHTS


def extract_crisis_keywords(texts: pd.Series) -> Dict[str, Dict[str, int]]:
    """
    Menghitung kemunculan kata kunci krisis per tier.
    - Tier 1: Isu Fisik & Medis Berat (keracunan, dirawat, ambulans, dll.)
    - Tier 2: Kualitas Higienis & Logistik (basi, busuk, kotor, sppg, dll.)
    - Tier 3: Kekecewaan Kebijakan & Keuangan (gagal, bohong, tidak layak, anggaran, dll.)
    """
    combined = " ".join(texts.fillna("").astype(str).str.lower().tolist())
    result = {"tier1": {}, "tier2": {}, "tier3": {}}

    for kw in CRISIS_KEYWORDS["tier1"]:
        # Match batas kata atau substring spesifik
        cnt = len(re.findall(re.escape(kw), combined))
        if cnt > 0:
            result["tier1"][kw] = cnt

    for kw in CRISIS_KEYWORDS["tier2"]:
        cnt = len(re.findall(re.escape(kw), combined))
        if cnt > 0:
            result["tier2"][kw] = cnt

    for kw in CRISIS_KEYWORDS["tier3"]:
        cnt = len(re.findall(re.escape(kw), combined))
        if cnt > 0:
            result["tier3"][kw] = cnt

    return result


def extract_emojis(texts: pd.Series) -> Dict[str, Dict[str, int]]:
    """
    Menghitung frekuensi emoji sarkasme dan emoji positif palsu (penanda ironi).
    """
    combined = " ".join(texts.fillna("").astype(str).tolist())
    sarcasm_counts = {}
    for emo in SARCASM_EMOJIS:
        cnt = combined.count(emo)
        if cnt > 0:
            sarcasm_counts[emo] = cnt

    fake_positive_counts = {}
    for emo in FAKE_POSITIVE_EMOJIS:
        cnt = combined.count(emo)
        if cnt > 0:
            fake_positive_counts[emo] = cnt

    return {
        "sarcasm_emojis": sarcasm_counts,
        "fake_positive_emojis": fake_positive_counts
    }


def extract_hashtags(texts: pd.Series, top_n: int = 15) -> List[Tuple[str, int]]:
    """
    Mengekstraksi tagar (#) terpopuler dalam korpus.
    """
    combined = " ".join(texts.fillna("").astype(str).str.lower().tolist())
    tags = re.findall(r"#\w+", combined)
    counts = Counter(tags).most_common(top_n)
    return counts


def get_keyword_risk(texts: pd.Series) -> Dict[str, Any]:
    """
    Menghitung skor risiko sinyal kata kunci krisis & emoji (Maksimal 20 Poin).
    
    FORMULA BOBOT EWS:
    - Tier 1 Bobot: x3
    - Tier 2 Bobot: x2
    - Tier 3 Bobot: x1
    - Emoji Sarkasme Bobot: x2
    - Emoji Positif Palsu: x1
    - Normalisasi per 1.000 tweet
    """
    total_tweets = max(len(texts), 1)
    kw_res = extract_crisis_keywords(texts)
    emo_res = extract_emojis(texts)

    t1_hits = sum(kw_res["tier1"].values())
    t2_hits = sum(kw_res["tier2"].values())
    t3_hits = sum(kw_res["tier3"].values())

    weighted_kw_score = (t1_hits * 3) + (t2_hits * 2) + (t3_hits * 1)
    
    sarcasm_emo_hits = sum(emo_res["sarcasm_emojis"].values())
    fake_pos_hits = sum(emo_res["fake_positive_emojis"].values())
    weighted_emo_score = (sarcasm_emo_hits * 2) + (fake_pos_hits * 1)

    # Total weighted intensity per tweet
    kw_intensity_per_100 = (weighted_kw_score / total_tweets) * 100
    emo_intensity_per_100 = (weighted_emo_score / total_tweets) * 100

    max_score = EWS_WEIGHTS["keyword_risk"] # 20 poin
    
    # 15% weighted intensity kata kunci memberi hingga 14 poin
    score_kw = min((kw_intensity_per_100 / 15.0) * 14.0, 14.0)
    # 20% intensity emoji memberi hingga 6 poin
    score_emo = min((emo_intensity_per_100 / 20.0) * 6.0, 6.0)
    
    total_keyword_score = round(score_kw + score_emo, 1)

    top_crisis_terms = sorted(
        [{"term": k, "hits": v, "tier": 1} for k, v in kw_res["tier1"].items()] +
        [{"term": k, "hits": v, "tier": 2} for k, v in kw_res["tier2"].items()] +
        [{"term": k, "hits": v, "tier": 3} for k, v in kw_res["tier3"].items()],
        key=lambda x: x["hits"],
        reverse=True
    )

    explanation = (
        f"Terdeteksi {t1_hits} sinyal Tier-1 (Medis), {t2_hits} sinyal Tier-2 (Higienis), "
        f"dan {t3_hits} sinyal Tier-3 (Kritik). Intensitas sinyal kata kunci: {kw_intensity_per_100:.1f}%. "
        f"Emoji sinis terdeteksi {sarcasm_emo_hits:,} kali. "
        f"Menyumbang {total_keyword_score}/{max_score} poin risiko EWS."
    )

    return {
        "score": total_keyword_score,
        "max_score": max_score,
        "tier1_hits": t1_hits,
        "tier2_hits": t2_hits,
        "tier3_hits": t3_hits,
        "top_crisis_terms": top_crisis_terms[:10],
        "keywords_detail": kw_res,
        "emojis_detail": emo_res,
        "hashtags": extract_hashtags(texts, 10),
        "explanation": explanation
    }
