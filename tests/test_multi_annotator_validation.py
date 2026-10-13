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

    # Verifikasi status penarikan metrik scripted (Option A)
    assert data["status"] == "withdrawn"
    assert "withdrawn" in data["note"]
