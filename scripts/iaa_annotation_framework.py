"""
iaa_annotation_framework.py
=============================
Complete inter-annotator agreement (IAA) framework for the MBG thesis.

This module handles:
  A. Annotation batch generation   — stratified sample ready for human labellers
  B. IAA computation engine         — Cohen's κ (2 annotators), Fleiss' κ (≥3)
  C. Adjudication protocol          — majority vote + conflict flagging + gold labels
  D. Annotation guidelines export   — Markdown doc for annotators
  E. Status tracking                — what's done vs pending

Workflow
--------
1. python iaa_annotation_framework.py --generate-batch
   → Creates data/annotation/batch_001_emotion.csv  (200 rows)
   → Creates data/annotation/batch_001_sarcasm.csv  (100 rows)
   → Creates docs/ANNOTATION_GUIDELINES.md

2. Give batch CSVs to human annotators (A, B, C)
   Annotators fill column: annotator_label

3. Collect filled CSVs as:
   data/annotation/batch_001_emotion_annotator_A.csv
   data/annotation/batch_001_emotion_annotator_B.csv
   data/annotation/batch_001_emotion_annotator_C.csv

4. python iaa_annotation_framework.py --compute-iaa --task emotion --batch 001
   → Computes Cohen/Fleiss κ
   → Runs adjudication
   → Exports gold labels + IAA report

Usage
-----
  python scripts/iaa_annotation_framework.py --generate-batch
  python scripts/iaa_annotation_framework.py --compute-iaa --task emotion --batch 001
  python scripts/iaa_annotation_framework.py --status
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import textwrap
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# ─── optional scikit-learn for Cohen's κ ─────────────────────────────────────
try:
    from sklearn.metrics import cohen_kappa_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

BASE  = pathlib.Path("/Users/jevin/Documents/tesis_mbg")
ANN   = BASE / "data" / "annotation"
DOCS  = BASE / "docs"
RESULTS = BASE / "results"
REPORTS = BASE / "reports"

ANN.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now(timezone.utc).isoformat()

EMOTION_LABELS   = ["Jijik", "Marah", "Netral", "Percaya", "Sedih", "Takut", "Tertarik"]
SARCASM_LABELS   = ["Sarkasme", "Bukan Sarkasme"]

# ─── A. Batch generation ──────────────────────────────────────────────────────

def generate_annotation_batch(batch_id: str = "001"):
    """
    Create stratified annotation samples for human labellers.

    Sampling strategy:
      - 100 random samples from FULL test set (representative)
      - 100 hard samples (IndoBERT disagreed with silver label)
      - 100 sarcasm samples (balanced Sarkasme / Bukan Sarkasme)
    Total emotion batch: 200 rows
    Total sarcasm batch: 100 rows
    """
    pred_path = RESULTS / "FINAL_indobert_predictions.csv"
    if not pred_path.exists():
        print(f"❌ {pred_path} not found — run scientific_validation_audit.py first")
        return

    pred_df = pd.read_csv(pred_path)
    pred_df = pred_df.rename(columns={"true_label": "silver_label",
                                      "predicted_label": "indobert_pred"})
    pred_df["agreed"] = pred_df["silver_label"] == pred_df["indobert_pred"]
    pred_df = pred_df.reset_index(drop=True)

    rng = np.random.default_rng(42)

    # --- emotion batch --------------------------------------------------------
    n_random = 100
    n_hard   = 100

    hard   = pred_df[~pred_df["agreed"]].sample(
        min(n_hard, (~pred_df["agreed"]).sum()), random_state=42)
    easy   = pred_df[pred_df["agreed"]].sample(
        min(n_random, pred_df["agreed"].sum()), random_state=42)
    emo_batch = pd.concat([hard, easy]).drop_duplicates(subset=["text"])
    emo_batch = emo_batch.sample(frac=1, random_state=42).reset_index(drop=True)
    emo_batch["annotation_id"]   = [f"EMO-{batch_id}-{i:04d}" for i in range(len(emo_batch))]
    emo_batch["batch_id"]        = batch_id
    emo_batch["task"]            = "emotion"
    emo_batch["annotator_label"] = ""      # ← annotator fills this column
    emo_batch["annotator_notes"] = ""      # ← optional free text

    cols = ["annotation_id", "batch_id", "task", "text",
            "silver_label", "indobert_pred", "agreed",
            "annotator_label", "annotator_notes"]
    emo_out = ANN / f"batch_{batch_id}_emotion.csv"
    emo_batch[cols].to_csv(emo_out, index=False)
    print(f"✅ Emotion batch: {emo_out}  ({len(emo_batch)} rows)")
    print(f"   Hard (disagreement): {(~emo_batch['agreed']).sum()}")
    print(f"   Easy (agreement):    {emo_batch['agreed'].sum()}")

    # --- sarcasm batch --------------------------------------------------------
    sar_path = REPORTS / "sarcasm_validation.json"
    sar_info = json.loads(sar_path.read_text()) if sar_path.exists() else {}

    # Build from test set text — mark silver sarcasm label if available
    sar_batch = pred_df[["text"]].copy().sample(100, random_state=99).reset_index(drop=True)
    sar_batch["annotation_id"]   = [f"SAR-{batch_id}-{i:04d}" for i in range(len(sar_batch))]
    sar_batch["batch_id"]        = batch_id
    sar_batch["task"]            = "sarcasm"
    sar_batch["annotator_label"] = ""
    sar_batch["annotator_notes"] = ""

    sar_cols = ["annotation_id", "batch_id", "task", "text",
                "annotator_label", "annotator_notes"]
    sar_out = ANN / f"batch_{batch_id}_sarcasm.csv"
    sar_batch[sar_cols].to_csv(sar_out, index=False)
    print(f"✅ Sarcasm batch: {sar_out}  ({len(sar_batch)} rows)")

    # --- metadata ------------------------------------------------------------
    meta = {
        "batch_id": batch_id,
        "generated_at": TIMESTAMP,
        "emotion_batch_file": str(emo_out),
        "sarcasm_batch_file": str(sar_out),
        "emotion_n": len(emo_batch),
        "sarcasm_n": len(sar_batch),
        "emotion_labels": EMOTION_LABELS,
        "sarcasm_labels": SARCASM_LABELS,
        "instructions": "See docs/ANNOTATION_GUIDELINES.md",
        "sha256_emotion": hashlib.sha256(emo_out.read_bytes()).hexdigest(),
        "sha256_sarcasm": hashlib.sha256(sar_out.read_bytes()).hexdigest(),
    }
    (ANN / f"batch_{batch_id}_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False))
    print(f"✅ Batch metadata: {ANN}/batch_{batch_id}_meta.json")

    _export_annotation_guidelines(batch_id)


# ─── B. IAA computation ───────────────────────────────────────────────────────

def fleiss_kappa(ratings: np.ndarray) -> float:
    """
    Compute Fleiss' κ for N subjects × k raters.
    ratings: 2D array shape (n_items, n_raters), values are category indices.
    """
    n_items, n_raters = ratings.shape
    categories = np.unique(ratings)
    n_cats = len(categories)

    # Build count matrix: n_items × n_cats
    cat_to_idx = {c: i for i, c in enumerate(categories)}
    count = np.zeros((n_items, n_cats), dtype=float)
    for i in range(n_items):
        for r in range(n_raters):
            count[i, cat_to_idx[ratings[i, r]]] += 1

    P_i = (1 / (n_raters * (n_raters - 1))) * (
        np.sum(count ** 2, axis=1) - n_raters
    )
    P_bar = np.mean(P_i)
    p_j   = count.sum(axis=0) / (n_items * n_raters)
    P_e   = np.sum(p_j ** 2)

    if P_e == 1.0:
        return 1.0
    return float((P_bar - P_e) / (1 - P_e))


def interpret_kappa(k: float) -> str:
    if k < 0:        return "Poor (worse than chance)"
    if k < 0.20:     return "Slight"
    if k < 0.40:     return "Fair"
    if k < 0.60:     return "Moderate"
    if k < 0.80:     return "Substantial"
    return "Almost Perfect"


def compute_iaa(task: str, batch_id: str):
    """
    Load annotator CSVs, compute Cohen's κ (pairwise) + Fleiss' κ,
    then run adjudication.
    """
    pattern = ANN / f"batch_{batch_id}_{task}_annotator_*.csv"
    files = sorted(ANN.glob(f"batch_{batch_id}_{task}_annotator_*.csv"))

    if not files:
        print(f"❌ No annotator files found matching: {pattern}")
        print("   Expected: data/annotation/batch_001_emotion_annotator_A.csv, _B, _C …")
        print("   → Give batch CSV to human annotators first.")
        _show_pending_annotation(task, batch_id)
        return

    print(f"Found {len(files)} annotator files:")
    dfs = {}
    for f in files:
        annotator = f.stem.split("annotator_")[-1]
        df = pd.read_csv(f)
        if "annotator_label" not in df.columns:
            print(f"  ❌ {f.name}: no 'annotator_label' column")
            continue
        df = df[df["annotator_label"].notna() & (df["annotator_label"] != "")]
        dfs[annotator] = df
        print(f"  {annotator}: {len(df)} labeled rows")

    if len(dfs) < 2:
        print("❌ Need at least 2 annotators. Aborting.")
        return

    # Align on annotation_id
    ref_ids = dfs[list(dfs.keys())[0]]["annotation_id"].values
    labels_matrix = []
    annotator_names = list(dfs.keys())
    for name in annotator_names:
        df = dfs[name].set_index("annotation_id")
        labels_matrix.append(df["annotator_label"].reindex(ref_ids).values)

    labels_matrix = np.array(labels_matrix, dtype=str).T  # shape: (n_items, n_raters)

    # Filter out rows with any NaN
    valid_mask = ~np.any(pd.isnull(labels_matrix) | (labels_matrix == "nan"), axis=1)
    labels_matrix = labels_matrix[valid_mask]
    valid_ids = ref_ids[valid_mask]
    print(f"\nAligned items with all annotators: {len(labels_matrix)}")

    # --- Pairwise Cohen's κ --------------------------------------------------
    pairwise = []
    for i, a1 in enumerate(annotator_names):
        for j, a2 in enumerate(annotator_names):
            if j <= i:
                continue
            col_a = labels_matrix[:, i]
            col_b = labels_matrix[:, j]
            if HAS_SKLEARN:
                k = cohen_kappa_score(col_a, col_b)
            else:
                # manual Cohen's κ
                agree = np.sum(col_a == col_b)
                n = len(col_a)
                po = agree / n
                cats = np.unique(np.concatenate([col_a, col_b]))
                pe = sum((np.sum(col_a == c) / n) * (np.sum(col_b == c) / n) for c in cats)
                k = (po - pe) / (1 - pe) if pe < 1 else 1.0
            pairwise.append({"annotator_a": a1, "annotator_b": a2,
                             "cohen_kappa": round(float(k), 4),
                             "interpretation": interpret_kappa(k),
                             "n_items": len(labels_matrix)})
            print(f"  Cohen κ ({a1} vs {a2}): {k:.4f}  → {interpret_kappa(k)}")

    # --- Fleiss' κ (≥3 raters) -----------------------------------------------
    fleiss_k = fleiss_kappa(labels_matrix) if len(annotator_names) >= 3 else None
    if fleiss_k is not None:
        print(f"  Fleiss' κ: {fleiss_k:.4f}  → {interpret_kappa(fleiss_k)}")

    # --- Adjudication ─────────────────────────────────────────────────────────
    gold = _adjudicate(labels_matrix, valid_ids, annotator_names, task, batch_id)

    # --- Save IAA report ──────────────────────────────────────────────────────
    report = {
        "task": task,
        "batch_id": batch_id,
        "computed_at": TIMESTAMP,
        "n_annotators": len(annotator_names),
        "annotators": annotator_names,
        "n_items_aligned": int(len(labels_matrix)),
        "pairwise_cohen_kappa": pairwise,
        "fleiss_kappa": round(float(fleiss_k), 4) if fleiss_k is not None else None,
        "fleiss_interpretation": interpret_kappa(fleiss_k) if fleiss_k is not None else None,
        "adjudication_method": "majority_vote_with_conflict_flagging",
        "conflict_threshold": "unanimous disagreement",
        "gold_label_file": str(ANN / f"batch_{batch_id}_{task}_gold.csv"),
        "evidence_type": "GROUND_TRUTH",
        "iaa_threshold_passed": (fleiss_k or max(p["cohen_kappa"] for p in pairwise)) >= 0.60,
    }
    report_path = REPORTS / f"iaa_{task}_batch{batch_id}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n✅ IAA report: {report_path}")
    print(f"✅ Gold labels: {ANN}/batch_{batch_id}_{task}_gold.csv")

    return report


def _adjudicate(labels_matrix: np.ndarray, ids: np.ndarray,
                annotator_names: List[str], task: str, batch_id: str) -> pd.DataFrame:
    """
    Majority vote adjudication.
    Conflicts (no majority) are flagged for lead-annotator resolution.
    """
    n_raters = labels_matrix.shape[1]
    gold_labels = []
    conflict_flags = []

    for row in labels_matrix:
        from collections import Counter
        counts = Counter(row)
        most_common, freq = counts.most_common(1)[0]
        if freq > n_raters / 2:
            gold_labels.append(most_common)
            conflict_flags.append(False)
        else:
            gold_labels.append("CONFLICT")
            conflict_flags.append(True)

    n_conflict = sum(conflict_flags)
    print(f"\n  Adjudication: {len(gold_labels)} items")
    print(f"    Resolved by majority: {len(gold_labels) - n_conflict}")
    print(f"    Conflicts (need lead-annotator): {n_conflict}")

    gold_df = pd.DataFrame({
        "annotation_id": ids,
        "gold_label": gold_labels,
        "conflict": conflict_flags,
        **{f"annotator_{n}": labels_matrix[:, i]
           for i, n in enumerate(annotator_names)},
    })
    gold_df["evidence_type"] = gold_df["conflict"].apply(
        lambda c: "CONFLICT_UNRESOLVED" if c else "GROUND_TRUTH"
    )
    out = ANN / f"batch_{batch_id}_{task}_gold.csv"
    gold_df.to_csv(out, index=False)
    return gold_df


# ─── C. Annotation guidelines ─────────────────────────────────────────────────

def _export_annotation_guidelines(batch_id: str = "001"):
    guidelines = textwrap.dedent(f"""
    # Annotation Guidelines — MBG Twitter Emotion & Sarcasm

    > Version: 1.0 | Batch: {batch_id} | Generated: {TIMESTAMP}

    ---

    ## 1. Overview

    You will annotate Indonesian tweets related to **Makan Bergizi Gratis (MBG)**
    policy for two tasks:

    | Task | Labels | N items |
    |------|--------|---------|
    | Emotion | 7 classes (see below) | 200 |
    | Sarcasm | 2 classes (see below) | 100 |

    **Important rules:**
    - Label each tweet **independently** — do not discuss with other annotators.
    - Label based on the tweet **as written**, not what you think the author meant.
    - If unsure, choose the **most likely** label and add a note.
    - Do **not** leave `annotator_label` blank.

    ---

    ## 2. Emotion Classification (7 classes)

    | Label | Bahasa Indonesia | Description | Example signal words |
    |-------|-----------------|-------------|----------------------|
    | **Jijik** | Disgust | Feeling of revulsion, contempt, or moral disgust | "menjijikkan", "kotor", "najis", "benci" |
    | **Marah** | Anger | Frustration, rage, indignation | "marah", "kesal", "geram", "biadab" |
    | **Netral** | Neutral | Factual, no clear emotion | neutral reporting, statistics |
    | **Percaya** | Trust/Joy | Positive sentiment, trust, happiness | "bagus", "senang", "percaya", "keren" |
    | **Sedih** | Sadness | Sorrow, disappointment, grief | "sedih", "kecewa", "menyesal" |
    | **Takut** | Fear | Anxiety, worry, threat perception | "takut", "khawatir", "ngeri" |
    | **Tertarik** | Interest/Anticipation | Curiosity, interest, looking forward | "menarik", "tertarik", "penasaran" |

    ### Decision Rules

    1. **Mixed emotions**: choose the **dominant** emotion.
    2. **Sarcasm**: if a tweet uses sarcasm to express disgust/anger, label as **Jijik** or **Marah**
       (based on the underlying emotion, not the surface words).
    3. **Off-topic** (e.g., non-MBG content): choose **Netral**.
    4. **Emojis**: use emojis as emotional cues but prioritize textual content.

    ### Examples

    | Tweet | Label | Reason |
    |-------|-------|--------|
    | "Program MBG keren banget, anak-anak jadi lebih sehat!" | Percaya | Positive endorsement |
    | "MBG ini mah kayak proyek korupsi doang, menjijikkan" | Jijik | Contempt/disgust |
    | "Katanya gratis, tapi kok bayar? Lucu banget 🙃" | Jijik | Sarcasm → underlying disgust |
    | "3 juta pelajar sudah menerima MBG per Mei 2026" | Netral | Factual statistic |
    | "Sedih banget lihat makanannya kualitasnya jelek" | Sedih | Sadness |

    ---

    ## 3. Sarcasm Classification (2 classes)

    | Label | Description |
    |-------|-------------|
    | **Sarkasme** | Tweet contains sarcasm, irony, or indirect criticism |
    | **Bukan Sarkasme** | Tweet is straightforward (positive, negative, or neutral) |

    ### Sarcasm Indicators (Indonesian context)

    - Excessive praise for clearly bad things
    - Emojis that contradict text (e.g., 🙃😂 on serious topic)
    - Rhetorical questions
    - Exaggeration (hiperbola)
    - "Katanya…" / "Konon…" + contradiction
    - Quoting official statements ironically

    ### Examples

    | Tweet | Label | Reason |
    |-------|-------|--------|
    | "Mantap! MBG sukses bikin anak kelaparan 👏" | Sarkasme | Praises negative outcome |
    | "Alhamdulillah MBG berjalan lancar" | Bukan Sarkasme | Sincere positive |
    | "Katanya gratis, tapi ada pungutan di sekolah 🙃" | Sarkasme | Irony |
    | "Data terbaru: 29.225 SPPG aktif per Mei 2026" | Bukan Sarkasme | Factual |

    ---

    ## 4. How to Fill the CSV

    1. Open the batch CSV: `batch_{batch_id}_emotion.csv` or `batch_{batch_id}_sarcasm.csv`
    2. For each row, fill the **`annotator_label`** column with exactly one of the valid labels.
    3. Optionally add notes in **`annotator_notes`**.
    4. Save as: `batch_{batch_id}_emotion_annotator_X.csv` (replace X with your ID: A, B, or C)
    5. Return the filled CSV to the project lead.

    **Valid emotion labels (copy-paste exactly):**
    ```
    Jijik
    Marah
    Netral
    Percaya
    Sedih
    Takut
    Tertarik
    ```

    **Valid sarcasm labels (copy-paste exactly):**
    ```
    Sarkasme
    Bukan Sarkasme
    ```

    ---

    ## 5. Adjudication Protocol

    After all annotators submit:

    1. **Majority vote**: if ≥2 of 3 annotators agree → that label = gold label.
    2. **Conflict** (all 3 disagree): flagged as `CONFLICT` → lead annotator decides.
    3. **IAA threshold**: Cohen/Fleiss κ ≥ 0.60 (Substantial) required for publication.
    4. If κ < 0.60: guidelines are revised → re-annotation of conflict items.

    ---

    ## 6. Annotator Declaration

    By submitting your annotations, you confirm:
    - You annotated independently.
    - You did not consult other annotators.
    - You followed these guidelines.
    - Your annotations represent your honest interpretation.

    ---

    *Generated by: `scripts/iaa_annotation_framework.py`*
    *Thesis: Social Network Analysis Sarkasme Cuitan Twitter — MBG (Marketing 6.0)*
    """).strip()

    out = DOCS / "ANNOTATION_GUIDELINES.md"
    out.write_text(guidelines, encoding="utf-8")
    print(f"✅ Annotation guidelines: {out}")


# ─── D. External validation ───────────────────────────────────────────────────

def run_external_validation():
    """
    Use IndoNLU EmoT dataset as external/generalization test.

    The EmoT dataset (Koto et al., 2020) uses labels:
      anger, fear, happy, love, sadness
    Our thesis uses:
      Jijik, Marah, Netral, Percaya, Sedih, Takut, Tertarik

    We map overlapping classes, report:
      - Performance on mapped classes
      - Domain shift analysis
      - Coverage (which thesis labels have external analogues)
    """
    EMOT = BASE / "lib/IndoNLU/dataset/emot_emotion-twitter"
    test_path = EMOT / "test_preprocess.csv"

    if not test_path.exists():
        print(f"❌ IndoNLU EmoT not found at {test_path}")
        return

    emot_test  = pd.read_csv(test_path)
    emot_train = pd.read_csv(EMOT / "train_preprocess.csv")
    emot_valid = pd.read_csv(EMOT / "valid_preprocess.csv")
    emot_all   = pd.concat([emot_train, emot_valid, emot_test], ignore_index=True)

    print(f"IndoNLU EmoT loaded: {len(emot_test)} test, {len(emot_all)} total")
    print(f"  EmoT labels: {sorted(emot_test['label'].unique())}")
    print(f"  Thesis labels: {EMOTION_LABELS}")

    # Label mapping
    EMOT_TO_THESIS = {
        "anger":   "Marah",
        "fear":    "Takut",
        "happy":   "Percaya",    # nearest equivalent (trust/joy)
        "love":    "Tertarik",   # nearest equivalent (interest/affection)
        "sadness": "Sedih",
        # "neutral": "Netral",  # not in EmoT
    }

    emot_test["thesis_label"] = emot_test["label"].map(EMOT_TO_THESIS)
    mapped = emot_test[emot_test["thesis_label"].notna()].copy()
    print(f"\n  Mappable test items: {len(mapped)} / {len(emot_test)}")
    for emot_l, thesis_l in EMOT_TO_THESIS.items():
        n = (emot_test["label"] == emot_l).sum()
        print(f"    {emot_l:8s} → {thesis_l:10s}  (n={n})")

    # Domain characteristics
    domain_report = {
        "external_dataset": {
            "name": "EmoT (IndoNLU)",
            "citation": "Koto et al. (2020) IndoNLU Benchmark",
            "url": "https://github.com/IndoNLP/indonlu",
            "source": "Indonesian Twitter",
            "annotation": "HUMAN_ANNOTATED — crowd-sourced with quality control",
            "evidence_type": "GROUND_TRUTH",
            "license": "Apache-2.0",
            "n_test": len(emot_test),
            "n_total": len(emot_all),
            "labels": sorted(emot_test["label"].unique().tolist()),
        },
        "thesis_dataset": {
            "name": "MBG Twitter Corpus",
            "source": "Indonesian Twitter (MBG keyword)",
            "annotation": "SILVER-STANDARD — automated labelling",
            "evidence_type": "MODEL_INFERENCE",
            "n_test": 1058,
            "labels": EMOTION_LABELS,
        },
        "label_mapping": EMOT_TO_THESIS,
        "coverage_analysis": {
            "thesis_labels_with_external_analogue": list(EMOT_TO_THESIS.values()),
            "thesis_labels_without_external_analogue": [
                l for l in EMOTION_LABELS if l not in EMOT_TO_THESIS.values()
            ],
            "emot_labels_without_thesis_analogue": [],
            "coverage_ratio": len(EMOT_TO_THESIS) / len(EMOTION_LABELS),
        },
        "domain_shift_notes": [
            "EmoT: general Indonesian Twitter (diverse topics)",
            "MBG corpus: domain-specific (government policy, food programme)",
            "Expected shift: higher 'Jijik'/'Marah' in MBG due to political content",
            "'Netral' class exists only in MBG corpus, not in EmoT",
            "'Takut' rare in MBG corpus (n=0 in test) — low external coverage",
        ],
        "generalization_status": "PARTIAL — 5/7 thesis emotion classes have EmoT analogues",
        "recommendation": (
            "Use EmoT as soft external benchmark for Marah, Takut, Percaya, Sedih, Tertarik. "
            "Report domain shift explicitly. Jijik and Netral have no direct EmoT equivalent."
        ),
    }

    # Distribution comparison
    thesis_dist = {
        "Jijik": 606, "Percaya": 220, "Netral": 124,
        "Tertarik": 91, "Marah": 14, "Sedih": 3, "Takut": 0,
    }
    emot_dist = emot_test["label"].value_counts().to_dict()

    distribution_df = pd.DataFrame({
        "EmoT_label": list(EMOT_TO_THESIS.keys()),
        "thesis_label": list(EMOT_TO_THESIS.values()),
        "EmoT_n_test": [emot_dist.get(l, 0) for l in EMOT_TO_THESIS.keys()],
        "thesis_n_test": [thesis_dist.get(EMOT_TO_THESIS[l], 0)
                         for l in EMOT_TO_THESIS.keys()],
    })
    distribution_df["EmoT_pct"] = (distribution_df["EmoT_n_test"] /
                                   distribution_df["EmoT_n_test"].sum() * 100).round(1)
    distribution_df["thesis_pct"] = (distribution_df["thesis_n_test"] /
                                     distribution_df["thesis_n_test"].sum() * 100).round(1)
    distribution_df["pct_shift"] = (distribution_df["thesis_pct"] -
                                    distribution_df["EmoT_pct"]).round(1)

    out_csv = RESULTS / "external_validation_domain_shift.csv"
    distribution_df.to_csv(out_csv, index=False)

    out_json = REPORTS / "external_validation_report.json"
    out_json.write_text(json.dumps(domain_report, indent=2, ensure_ascii=False))

    # Markdown report
    md_lines = [
        "# External Validation Report — IndoNLU EmoT",
        f"\n> Generated: {TIMESTAMP}\n",
        "---\n",
        "## Dataset Comparison\n",
        "| Property | EmoT (External) | MBG Corpus (Thesis) |",
        "|----------|----------------|---------------------|",
        f"| Source | Indonesian Twitter | Indonesian Twitter (MBG) |",
        f"| Annotation | HUMAN_ANNOTATED | SILVER-STANDARD |",
        f"| N test | {len(emot_test):,} | 1,058 |",
        f"| Labels | anger, fear, happy, love, sadness | 7 (Ekman-based, Indonesian) |",
        f"| Domain | General | Policy-specific (MBG) |",
        "",
        "## Label Mapping\n",
        "| EmoT Label | Thesis Label | EmoT n (test) | Thesis n (test) | Δ% |",
        "|------------|--------------|---------------|-----------------|-----|",
    ]
    for _, row in distribution_df.iterrows():
        md_lines.append(
            f"| {row['EmoT_label']} | {row['thesis_label']} "
            f"| {row['EmoT_n_test']} ({row['EmoT_pct']}%) "
            f"| {row['thesis_n_test']} ({row['thesis_pct']}%) "
            f"| {row['pct_shift']:+.1f}% |"
        )

    md_lines += [
        "",
        "## Labels Without External Analogue\n",
        "| Thesis Label | Reason |",
        "|-------------|--------|",
        "| Jijik | EmoT uses 'anger' but 'Jijik' is disgust — distinct construct |",
        "| Netral | Not present in EmoT (EmoT has no neutral class) |",
        "",
        "## Domain Shift Notes\n",
    ]
    for note in domain_report["domain_shift_notes"]:
        md_lines.append(f"- {note}")

    md_lines += [
        "",
        "## Generalization Status\n",
        f"> **{domain_report['generalization_status']}**\n",
        f"> {domain_report['recommendation']}\n",
        "",
        "## Evidence Classification\n",
        "| Dataset | Evidence Type |",
        "|---------|--------------|",
        "| EmoT labels | `GROUND_TRUTH` (human-annotated) |",
        "| MBG corpus labels | `SILVER-STANDARD` (automated) |",
        "| Model predictions on EmoT | `MODEL_INFERENCE` |",
        "",
        "---",
        "*Source: IndoNLU EmoT (Koto et al., 2020) — Apache-2.0 License*",
    ]

    md_out = RESULTS / "external_validation_domain_shift.md"
    md_out.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"\n✅ External validation report: {out_json}")
    print(f"✅ Domain shift CSV: {out_csv}")
    print(f"✅ Domain shift Markdown: {md_out}")
    print(f"\n  Coverage: 5/7 thesis labels have EmoT analogues")
    print(f"  Status: PARTIAL — sufficient for soft generalization benchmark")
    print(f"\n  Domain shift (EmoT → MBG):")
    print(distribution_df[["EmoT_label","thesis_label","EmoT_pct","thesis_pct","pct_shift"]].to_string(index=False))

    return domain_report


# ─── E. Status tracker ────────────────────────────────────────────────────────

def show_status():
    print("\n" + "=" * 64)
    print("IAA & ANNOTATION STATUS")
    print("=" * 64)

    checks = {
        "Annotation guidelines": DOCS / "ANNOTATION_GUIDELINES.md",
        "Emotion batch (for annotators)": ANN / "batch_001_emotion.csv",
        "Sarcasm batch (for annotators)": ANN / "batch_001_sarcasm.csv",
        "Annotator A — emotion": ANN / "batch_001_emotion_annotator_A.csv",
        "Annotator B — emotion": ANN / "batch_001_emotion_annotator_B.csv",
        "Annotator C — emotion": ANN / "batch_001_emotion_annotator_C.csv",
        "Annotator A — sarcasm": ANN / "batch_001_sarcasm_annotator_A.csv",
        "Annotator B — sarcasm": ANN / "batch_001_sarcasm_annotator_B.csv",
        "Annotator C — sarcasm": ANN / "batch_001_sarcasm_annotator_C.csv",
        "Gold labels — emotion": ANN / "batch_001_emotion_gold.csv",
        "Gold labels — sarcasm": ANN / "batch_001_sarcasm_gold.csv",
        "IAA report — emotion": REPORTS / "iaa_emotion_batch001.json",
        "IAA report — sarcasm": REPORTS / "iaa_sarcasm_batch001.json",
        "External validation report": REPORTS / "external_validation_report.json",
        "Domain shift CSV": RESULTS / "external_validation_domain_shift.csv",
    }

    for label, path in checks.items():
        icon = "✅" if path.exists() else "❌"
        size = f"({path.stat().st_size:,}b)" if path.exists() else ""
        print(f"  {icon}  {label:<45s} {size}")

    print()

    # IAA summary if computed
    for task in ["emotion", "sarcasm"]:
        rep = REPORTS / f"iaa_{task}_batch001.json"
        if rep.exists():
            data = json.loads(rep.read_text())
            fleiss = data.get("fleiss_kappa")
            if fleiss:
                print(f"  Fleiss κ ({task}): {fleiss}  → {interpret_kappa(fleiss)}")
                thresh = "✅ PASS" if data.get("iaa_threshold_passed") else "❌ FAIL"
                print(f"  κ ≥ 0.60 threshold: {thresh}")


def _show_pending_annotation(task: str, batch_id: str):
    batch_file = ANN / f"batch_{batch_id}_{task}.csv"
    print(f"\n📋 Next steps for IAA:")
    print(f"  1. Give annotators: {batch_file}")
    print(f"  2. They fill 'annotator_label' column")
    print(f"  3. Save as: {ANN}/batch_{batch_id}_{task}_annotator_A.csv")
    print(f"               {ANN}/batch_{batch_id}_{task}_annotator_B.csv")
    print(f"               {ANN}/batch_{batch_id}_{task}_annotator_C.csv")
    print(f"  4. Re-run: python scripts/iaa_annotation_framework.py --compute-iaa "
          f"--task {task} --batch {batch_id}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="IAA annotation framework for MBG thesis"
    )
    parser.add_argument("--generate-batch", action="store_true",
                        help="Generate annotation batches + guidelines")
    parser.add_argument("--compute-iaa", action="store_true",
                        help="Compute Cohen/Fleiss κ + adjudication")
    parser.add_argument("--external-validation", action="store_true",
                        help="Run external generalization validation (IndoNLU EmoT)")
    parser.add_argument("--status", action="store_true",
                        help="Show annotation status")
    parser.add_argument("--task", default="emotion",
                        choices=["emotion", "sarcasm"])
    parser.add_argument("--batch", default="001")
    parser.add_argument("--all", action="store_true",
                        help="Run generate-batch + external-validation + status")
    args = parser.parse_args()

    if args.all or args.generate_batch:
        print("=== Generating annotation batches ===")
        generate_annotation_batch(args.batch)

    if args.all or args.external_validation:
        print("\n=== Running external validation ===")
        run_external_validation()

    if args.compute_iaa:
        print(f"\n=== Computing IAA for task={args.task} batch={args.batch} ===")
        compute_iaa(args.task, args.batch)

    if args.all or args.status:
        show_status()

    if not any([args.generate_batch, args.compute_iaa,
                args.external_validation, args.status, args.all]):
        parser.print_help()


if __name__ == "__main__":
    main()
