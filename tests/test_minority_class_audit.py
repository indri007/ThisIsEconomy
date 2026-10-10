"""
Unit test: test_minority_class_audit.py
Menguji keabsahan matematis audit ketimpangan kelas minoritas dan taksonomi bertingkat.
"""

import json
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

def test_minority_audit_json_integrity():
    report_json = RESULTS_DIR / "MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.json"
    assert report_json.exists(), "Berkas MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.json harus tersedia"
    with open(report_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Validasi Metrik Granular 6-Kelas
    gran = data["evaluation_comparison"]["granular_6_class"]
    assert gran["accuracy"] == 0.7599
    assert gran["macro_f1"] == 0.4535
    assert gran["weighted_f1"] == 0.7434

    # 2. Validasi Metrik Taksonomi Bertingkat 3-Super-Kelas
    super_cls = data["evaluation_comparison"]["hierarchical_3_super_class"]
    assert super_cls["accuracy"] >= 0.76
    assert super_cls["macro_f1"] >= 0.75, "Macro-F1 3-super-class harus mencapai >= 75%"
    assert super_cls["weighted_f1"] >= 0.76

    # 3. Validasi Diseksi Minoritas
    dissect = data["minority_dissection"]
    assert dissect["marah_sample_count"] == 14
    assert dissect["sedih_sample_count"] == 3
