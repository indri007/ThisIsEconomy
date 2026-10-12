#!/usr/bin/env python3
"""
Script: run_multi_annotator_agreement_validation.py
===================================================
Menghitung reliabilitas antarpenilai (inter-rater reliability) HANYA dari
berkas anotasi manusia yang benar-benar diisi secara independen.

Versi sebelumnya membuat label "Penilai 2" dengan menyalin label Penilai 1 dan
menuliskan 5 ketidaksepakatan langsung di dalam kode. Angka yang dihasilkan
(kappa 0.9135, Fleiss 0.8442, Krippendorff 0.8447) karena itu TIDAK berasal dari
penilai manusia dan tidak boleh dikutip. Versi ini menolak berjalan bila berkas
anotasi nyata belum tersedia.

Masukan (wajib, diisi manusia secara terpisah dan buta terhadap label model/silver):
  data/annotation/annotator_1.csv   kolom: annotation_id, label
  data/annotation/annotator_2.csv   kolom: annotation_id, label
Masukan opsional:
  data/annotation/adjudicated_gold.csv  kolom: annotation_id, label
      (hasil diskusi/adjudikasi kedua penilai untuk kasus yang tidak sepakat)
  data/annotation/researcher_batch_100.csv  (berisi indobert_prediction & silver_label)

Templat kosong untuk penilai: data/annotation/annotator_template.csv
(hanya annotation_id + text; tanpa label model maupun silver).

Keluaran:
  results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.json
  results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score

BASE_DIR = Path(__file__).resolve().parent.parent
ANN_DIR = BASE_DIR / "data" / "annotation"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

VALID_LABELS = {"Bahagia", "Sedih", "Percaya", "Jijik", "Takut", "Marah",
                "Kaget", "Tertarik", "Netral"}


def load_annotator(path: Path, name: str) -> pd.Series:
    if not path.exists():
        sys.exit(
            f"[STOP] {path.relative_to(BASE_DIR)} belum ada.\n"
            f"       {name} harus mengisi data/annotation/annotator_template.csv secara mandiri,\n"
            f"       lalu menyimpannya dengan nama tersebut. Reliabilitas tidak dihitung."
        )
    df = pd.read_csv(path, dtype=str)
    missing = {"annotation_id", "label"} - set(df.columns)
    if missing:
        sys.exit(f"[STOP] {path.name} tidak memiliki kolom {sorted(missing)}.")
    df["label"] = df["label"].fillna("").str.strip()
    empty = (df["label"] == "").sum()
    if empty:
        sys.exit(f"[STOP] {path.name}: {empty} baris belum dilabeli.")
    bad = sorted(set(df["label"]) - VALID_LABELS)
    if bad:
        sys.exit(f"[STOP] {path.name}: label tidak dikenal {bad}. Gunakan: {sorted(VALID_LABELS)}")
    if df["annotation_id"].duplicated().any():
        sys.exit(f"[STOP] {path.name}: annotation_id duplikat.")
    return df.set_index("annotation_id")["label"]


def krippendorff_alpha_nominal(matrix: np.ndarray) -> float:
    """matrix: units x raters (object array, None = missing). Nominal alpha."""
    values = sorted({v for row in matrix for v in row if v is not None})
    idx = {v: i for i, v in enumerate(values)}
    k = len(values)
    o = np.zeros((k, k))
    for row in matrix:
        vals = [v for v in row if v is not None]
        m = len(vals)
        if m < 2:
            continue
        for a in range(m):
            for b in range(m):
                if a != b:
                    o[idx[vals[a]], idx[vals[b]]] += 1.0 / (m - 1)
    n_c = o.sum(axis=1)
    n = n_c.sum()
    if n <= 1:
        return float("nan")
    d_o = (o.sum() - np.trace(o)) / n
    d_e = (n * n - (n_c ** 2).sum()) / (n * (n - 1))
    return float(1 - d_o / d_e) if d_e > 0 else float("nan")


def main():
    a1 = load_annotator(ANN_DIR / "annotator_1.csv", "Penilai 1")
    a2 = load_annotator(ANN_DIR / "annotator_2.csv", "Penilai 2")
    common = a1.index.intersection(a2.index)
    if len(common) < len(a1) or len(common) < len(a2):
        print(f"[!] Hanya {len(common)} annotation_id yang sama di kedua berkas; analisis memakai irisan ini.")
    a1, a2 = a1.loc[common], a2.loc[common]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "computed_from_independent_human_annotation_files",
        "n_units": int(len(common)),
        "inputs": ["data/annotation/annotator_1.csv", "data/annotation/annotator_2.csv"],
        "inter_rater": {
            "raw_agreement": round(float(accuracy_score(a1, a2)), 4),
            "cohen_kappa": round(float(cohen_kappa_score(a1, a2)), 4),
            "krippendorff_alpha_nominal": round(
                krippendorff_alpha_nominal(np.array([[x, y] for x, y in zip(a1, a2)], dtype=object)), 4),
            "n_disagreements": int((a1 != a2).sum()),
        },
    }

    gold_path = ANN_DIR / "adjudicated_gold.csv"
    batch_path = ANN_DIR / "researcher_batch_100.csv"
    if gold_path.exists() and batch_path.exists():
        gold = load_annotator(gold_path, "Adjudikasi")
        batch = pd.read_csv(batch_path, dtype=str).set_index("annotation_id")
        ids = gold.index.intersection(batch.index)
        g = gold.loc[ids]
        for col, key in (("indobert_prediction", "indobert_vs_gold"), ("silver_label", "silver_vs_gold")):
            if col in batch.columns:
                p = batch.loc[ids, col].fillna("").str.strip()
                report[key] = {
                    "n": int(len(ids)),
                    "accuracy": round(float(accuracy_score(g, p)), 4),
                    "cohen_kappa": round(float(cohen_kappa_score(g, p)), 4),
                    "macro_f1": round(float(f1_score(g, p, average="macro", zero_division=0)), 4),
                    "weighted_f1": round(float(f1_score(g, p, average="weighted", zero_division=0)), 4),
                }
    else:
        report["indobert_vs_gold"] = "not computed: adjudicated_gold.csv not provided"

    out_json = RESULTS_DIR / "MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    ir = report["inter_rater"]
    md = [
        "# Laporan Reliabilitas Antarpenilai (dihitung dari berkas anotasi manusia)",
        "",
        f"- Dibuat: {report['generated_at']}",
        f"- Jumlah unit: {report['n_units']}",
        f"- Kesepakatan mentah: {ir['raw_agreement']:.2%}",
        f"- Cohen's kappa: {ir['cohen_kappa']}",
        f"- Krippendorff's alpha (nominal): {ir['krippendorff_alpha_nominal']}",
        f"- Jumlah ketidaksepakatan: {ir['n_disagreements']}",
        "",
    ]
    if isinstance(report.get("indobert_vs_gold"), dict):
        m = report["indobert_vs_gold"]
        md += ["## IndoBERT vs gold hasil adjudikasi", "",
               f"- Akurasi: {m['accuracy']:.2%} | kappa: {m['cohen_kappa']} | macro-F1: {m['macro_f1']} | weighted-F1: {m['weighted_f1']}", ""]
    (RESULTS_DIR / "MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
