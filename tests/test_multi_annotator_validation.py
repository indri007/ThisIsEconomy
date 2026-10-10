"""
Unit test: test_multi_annotator_validation.py
Menguji keabsahan dan konsistensi matematis dari protokol Multi-Annotator Gold Standard Benchmark.
"""

import json
from pathlib import Path
import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
ANN_DIR = BASE_DIR / "data" / "annotation"
RESULTS_DIR = BASE_DIR / "results"

def test_gold_dataset_integrity():
    gold_csv = ANN_DIR / "multi_annotator_batch_100_GOLD.csv"
    assert gold_csv.exists(), "Berkas multi_annotator_batch_100_GOLD.csv harus tersedia"
    df = pd.read_csv(gold_csv)
    assert len(df) == 100, "Dataset emas harus memiliki tepat 100 baris sampel"
    required_cols = [
        "annotation_id", "text", "indobert_prediction", "silver_label",
        "annotator_1", "annotator_2", "consensus_gold", "adjudication_rationale"
    ]
    for col in required_cols:
        assert col in df.columns, f"Kolom {col} harus ada dalam dataset emas"

def test_multi_annotator_metrics_report():
    report_json = RESULTS_DIR / "MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.json"
    assert report_json.exists(), "Berkas MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.json harus tersedia"
    with open(report_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Cek Kesepakatan Antar-Manusia (H1 vs H2)
    h_rel = data["inter_human_reliability"]
    assert h_rel["accuracy"] >= 0.90, "Akurasi antar-manusia harus >= 90%"
    assert h_rel["cohen_kappa"] >= 0.81, "Cohen's Kappa antar-manusia harus >= 0.81 (Almost Perfect)"

    # 2. Cek Reliabilitas Multi-Penilai (Fleiss & Krippendorff)
    m_rel = data["multi_rater_reliability"]
    assert m_rel["fleiss_kappa"] >= 0.80, "Fleiss' Kappa 3 penilai harus >= 0.80"
    assert m_rel["krippendorff_alpha"] >= 0.80, "Krippendorff's Alpha harus >= 0.80"

    # 3. Cek Kinerja Model vs Konsensus Emas
    mod_gold = data["model_vs_gold_standard"]
    assert mod_gold["accuracy"] == 0.90, "Akurasi model vs konsensus emas harus 90%"
    assert mod_gold["cohen_kappa"] == 0.8243, "Cohen's Kappa model vs konsensus emas harus 0.8243"
    assert mod_gold["weighted_f1"] >= 0.85, "Weighted F1 model vs konsensus emas harus >= 0.85"
