"""
scripts/test_custom_ews_v2.py
=============================
Skrip Pengujian Otomatis Komprehensif untuk Custom Early Warning System (EWS) v2.
Menguji 10 dimensi kepatuhan metodologis tesis dan integritas perangkat lunak.
"""

import sys
from pathlib import Path
import pandas as pd

# Pastikan root direktori ada di sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ews.config import DATA_PATHS, INDOBERT_MODEL_METADATA, EWS_WEIGHTS
from ews.emotion_analyzer import (
    load_emotion_data,
    get_emotion_distribution,
    get_dominant_emotion,
    get_emotion_risk,
)
from ews.sna_analyzer import (
    load_sna_data,
    get_top_degree,
    get_top_betweenness,
    get_communities,
    get_community_sizes,
)
from ews.anomaly_detector import (
    aggregate_daily_mentions,
    calculate_rolling_statistics,
    calculate_z_score,
    detect_spikes,
    get_anomaly_metrics,
)
from ews.keyword_analyzer import (
    extract_crisis_keywords,
    extract_emojis,
    get_keyword_risk,
)
from ews.ews_engine import (
    calculate_sarcasm_risk,
    compute_custom_ews_v2,
)
from ews.fallback import run_with_fallback, MonitoringResult


def run_comprehensive_tests():
    print("=" * 60)
    print("      CUSTOM EWS v2 — COMPREHENSIVE VERIFICATION")
    print("=" * 60)

    results = {}

    # [1] Dataset
    try:
        assert DATA_PATHS["emotion"].exists(), "Dataset emosi tidak ditemukan"
        assert DATA_PATHS["sna_nodes"].exists(), "Dataset SNA tidak ditemukan"
        assert DATA_PATHS["sarcasm"].exists(), "Dataset sarkasme tidak ditemukan"
        df_emo = pd.read_csv(DATA_PATHS["emotion"])
        df_sna = pd.read_csv(DATA_PATHS["sna_nodes"])
        df_sar = pd.read_csv(DATA_PATHS["sarcasm"])
        assert len(df_emo) == 5263, f"Jumlah baris emosi {len(df_emo)} != 5263"
        assert len(df_sna) == 971, f"Jumlah simpul SNA {len(df_sna)} != 971"
        assert len(df_sar) == 3395, f"Jumlah baris sarkasme {len(df_sar)} != 3395"
        results["[1] Dataset"] = "PASS"
    except Exception as e:
        results["[1] Dataset"] = f"FAIL ({e})"

    # [2] Emotion Analyzer
    try:
        dist = get_emotion_distribution(df_emo)
        assert len(dist) == 7, f"Jumlah label aktual {len(dist)} != 7"
        expected_labels = set(INDOBERT_MODEL_METADATA["actual_labels"])
        assert set(dist.keys()) == expected_labels, "Label tidak cocok dengan konfigurasi 7 emosi aktual"
        dom_label, dom_cnt, dom_pct = get_dominant_emotion(df_emo)
        assert dom_label == "Jijik" and dom_cnt == 2960, "Dominant emotion bukan Jijik (2960)"
        results["[2] Emotion Analyzer"] = "PASS"
    except Exception as e:
        results["[2] Emotion Analyzer"] = f"FAIL ({e})"

    # [3] Emotion -> EWS
    try:
        emo_risk = get_emotion_risk(df_emo)
        assert emo_risk["score"] > 0, "Skor risiko emosi tidak boleh 0"
        assert emo_risk["negative_pct"] > 55.0, "Rasio negatif harus mencerminkan data aktual (~57.7%)"
        results["[3] Emotion → EWS"] = "PASS"
    except Exception as e:
        results["[3] Emotion → EWS"] = f"FAIL ({e})"

    # [4] SNA Integration
    try:
        comm_stat = get_communities(df_sna)
        assert comm_stat["total_nodes"] == 971, "Total nodes SNA != 971"
        assert comm_stat["total_communities"] == 342, "Total komunitas != 342"
        top_deg = get_top_degree(df_sna, 5)
        top_bet = get_top_betweenness(df_sna, 5)
        assert top_deg[0]["Label"] == "grok", "Top degree actor bukan grok"
        results["[4] SNA Integration"] = "PASS"
    except Exception as e:
        results["[4] SNA Integration"] = f"FAIL ({e})"

    # [5] Anomaly Detection
    try:
        anom_res = get_anomaly_metrics(df_emo, threshold=2.0)
        assert anom_res["active_days"] == 83, f"Active days {anom_res['active_days']} != 83"
        assert anom_res["spikes_count"] == 4, f"Spikes count {anom_res['spikes_count']} != 4"
        assert anom_res["max_day_volume"] == 1022, "Puncak volume bukan 1022"
        results["[5] Anomaly Detection"] = "PASS"
    except Exception as e:
        results["[5] Anomaly Detection"] = f"FAIL ({e})"

    # [6] Keyword Analysis
    try:
        kw_risk = get_keyword_risk(df_emo["text"])
        assert kw_risk["score"] > 0, "Skor kata kunci harus > 0"
        assert kw_risk["tier1_hits"] > 0, "Harus ada Tier 1 hits"
        assert kw_risk["tier2_hits"] > 0, "Harus ada Tier 2 hits"
        results["[6] Keyword Analysis"] = "PASS"
    except Exception as e:
        results["[6] Keyword Analysis"] = f"FAIL ({e})"

    # [7] EWS Engine
    try:
        engine_res = compute_custom_ews_v2(df_emo, df_sna, df_sar)
        assert 0 <= engine_res["score"] <= 100, "Skor EWS harus antara 0 dan 100"
        assert engine_res["status"] in ["SAFE", "WARNING", "DANGER", "CRITICAL"], "Status EWS tidak valid"
        assert len(engine_res["components"]) == 5, "Harus ada 5 komponen bobot EWS"
        results["[7] EWS Engine"] = "PASS"
    except Exception as e:
        results["[7] EWS Engine"] = f"FAIL ({e})"

    # [8] Dashboard
    try:
        import dashboard.app as app_module
        assert hasattr(app_module, "CUSTOM_EWS_AVAILABLE") and app_module.CUSTOM_EWS_AVAILABLE, "CUSTOM_EWS_AVAILABLE harus True di app.py"
        from ews.custom_dashboard import render_custom_ews
        assert callable(render_custom_ews), "render_custom_ews harus callable"
        results["[8] Dashboard"] = "PASS"
    except Exception as e:
        results["[8] Dashboard"] = f"FAIL ({e})"

    # [9] Brand24 Fallback
    try:
        def mock_b24_fail():
            raise ConnectionError("API subscription inactive")
        def mock_custom_ok():
            return {"status": "ok", "source": "local"}
        fb_res = run_with_fallback(mock_b24_fail, mock_custom_ok)
        assert fb_res.source == "Custom EWS", "Fallback harus memilih Custom EWS saat Brand24 gagal"
        assert fb_res.success, "Fallback harus sukses"
        results["[9] Brand24 Fallback"] = "PASS"
    except Exception as e:
        results["[9] Brand24 Fallback"] = f"FAIL ({e})"

    # [10] Final Audit
    try:
        total_pass = sum(1 for v in results.values() if v == "PASS")
        assert total_pass == 9, "Semua 9 modul sebelumnya harus PASS"
        results["[10] Final Audit"] = "PASS"
    except Exception as e:
        results["[10] Final Audit"] = f"FAIL ({e})"

    print("\nHASIL PENGUJIAN 10 DIMENSI:")
    print("-" * 60)
    for k, v in results.items():
        icon = "✅" if v == "PASS" else "❌"
        print(f"{icon} {k:<25} : {v}")
    print("=" * 60)
    
    return all(v == "PASS" for v in results.values())


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
