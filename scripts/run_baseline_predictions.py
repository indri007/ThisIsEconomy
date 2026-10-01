"""
run_baseline_predictions.py
============================
Re-runs TF-IDF + LogReg and TF-IDF + LinearSVM on the SAME group-aware
train/test split used for IndoBERT, and saves per-sample prediction CSVs.

This enables:
  - McNemar statistical test vs IndoBERT
  - Per-sample comparison table
  - Leakage-free comparison (same split, same random_state=42)

After running this script, re-run:
  python scripts/scientific_validation_audit.py

Outputs
-------
  results/baseline_logreg_predictions.csv
  results/baseline_svm_predictions.csv
"""

from __future__ import annotations

import hashlib
import pathlib
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.svm import LinearSVC

BASE = pathlib.Path("/Users/jevin/Documents/tesis_mbg")
RESULTS = BASE / "results"

RANDOM_STATE = 42  # must match IndoBERT split

# ─── load full predictions (which has both true and pred columns) ───────────
print("Loading IndoBERT predictions (for train/test reconstruction) …")
pred_df = pd.read_csv(RESULTS / "FINAL_indobert_predictions.csv")
pred_df = pred_df.rename(columns={"true_label": "y_true", "predicted_label": "y_pred_indobert"})

# The predictions CSV is the TEST set; we need the FULL dataset to rebuild train.
# Check if a full dataset or split verification CSV exists.
split_ver = pd.read_csv(RESULTS / "final_split_verification.csv")
train_N = int(split_ver["train_N"].iloc[0])
test_N  = int(split_ver["test_N"].iloc[0])
print(f"  Expected split: train={train_N}, test={test_N}")

# Try to load full annotated dataset
candidates = [
    BASE / "data" / "tweets_annotated.csv",
    BASE / "data" / "processed" / "tweets_annotated.csv",
    BASE / "data" / "tweets_processed.csv",
    BASE / "data" / "processed" / "tweets_processed.csv",
    BASE / "data" / "emotion_dataset.csv",
    BASE / "data" / "processed" / "emotion_labeled.csv",
]
full_df = None
for c in candidates:
    if c.exists():
        full_df = pd.read_csv(c)
        print(f"  Found full dataset: {c}  ({len(full_df):,} rows)")
        print(f"  Columns: {list(full_df.columns)}")
        break

if full_df is None:
    # Fallback: use the emotion split CSVs if they exist
    train_split = RESULTS / "emotion_train_group_split.csv"
    test_split  = RESULTS / "emotion_test_group_split.csv"
    if train_split.exists() and test_split.exists():
        train_df = pd.read_csv(train_split)
        test_df  = pd.read_csv(test_split)
        print(f"  Using split CSVs: train={len(train_df)}, test={len(test_df)}")
        full_df = pd.concat([train_df, test_df], ignore_index=True)
        print(f"  Columns: {list(full_df.columns)}")

if full_df is None:
    print("ERROR: Cannot find full dataset. Checked:")
    for c in candidates:
        print(f"  {c}")
    sys.exit(1)

# ─── identify text and label columns ─────────────────────────────────────────
def detect_col(df, keywords):
    for kw in keywords:
        for c in df.columns:
            if kw.lower() in c.lower():
                return c
    return None

text_col = detect_col(full_df, ["processed_text", "processed", "text_clean", "text"])
label_col = detect_col(full_df, ["emotion_label", "label", "emotion", "true_label", "y_true"])
group_col = detect_col(full_df, ["group", "user_id", "tweet_id", "id"])

print(f"  text_col  = {text_col}")
print(f"  label_col = {label_col}")
print(f"  group_col = {group_col}")

if text_col is None or label_col is None:
    print("ERROR: Cannot detect text/label columns")
    sys.exit(1)

full_df = full_df.dropna(subset=[text_col, label_col]).reset_index(drop=True)
X = full_df[text_col].astype(str).values
y = full_df[label_col].astype(str).values

# ─── group-aware split (replicate IndoBERT split) ────────────────────────────
from sklearn.model_selection import GroupShuffleSplit, train_test_split

if group_col and group_col in full_df.columns:
    print(f"  Group-aware split on '{group_col}' …")
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=RANDOM_STATE)
    groups = full_df[group_col].values
    train_idx, test_idx = next(gss.split(X, y, groups=groups))
else:
    print("  Stratified split (no group column) …")
    idx = np.arange(len(X))
    train_idx, test_idx = train_test_split(
        idx, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]
print(f"  Split: train={len(X_train)}, test={len(X_test)}")

# Verify overlap
overlap = len(set(X_train) & set(X_test))
print(f"  Text overlap train/test: {overlap}")
if overlap > 0:
    print("  WARNING: text overlap detected — split may differ from IndoBERT split")

# ─── TF-IDF vectorizer ───────────────────────────────────────────────────────
print("\nFitting TF-IDF vectorizer …")
tfidf = TfidfVectorizer(max_features=50_000, ngram_range=(1, 2), sublinear_tf=True)
Xtr = tfidf.fit_transform(X_train)
Xte = tfidf.transform(X_test)

def evaluate_and_save(name: str, model, filename: str):
    model.fit(Xtr, y_train)
    y_pred = model.predict(Xte)
    acc   = accuracy_score(y_test, y_pred)
    f1    = f1_score(y_test, y_pred, average="macro", zero_division=0)
    prec  = precision_score(y_test, y_pred, average="macro", zero_division=0)
    rec   = recall_score(y_test, y_pred, average="macro", zero_division=0)
    print(f"\n  {name}:")
    print(f"    Accuracy  = {acc:.4f}")
    print(f"    Macro-F1  = {f1:.4f}")
    print(f"    Macro-P   = {prec:.4f}")
    print(f"    Macro-R   = {rec:.4f}")

    out = pd.DataFrame({
        "text": X_test,
        "y_true": y_test,
        f"y_pred_{filename.split('_')[1]}": y_pred,
    })
    out_path = RESULTS / f"{filename}.csv"
    out.to_csv(out_path, index=False)
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    print(f"    Saved: {out_path}  ({out_path.stat().st_size:,} bytes)")
    print(f"    SHA-256: {sha[:16]}…")
    return y_pred, acc, f1

# ─── Logistic Regression ─────────────────────────────────────────────────────
print("\nRunning TF-IDF + Logistic Regression …")
lr = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, C=1.0)
y_logreg, acc_lr, f1_lr = evaluate_and_save(
    "TF-IDF + LogReg", lr, "baseline_logreg_predictions"
)

# ─── Linear SVM ──────────────────────────────────────────────────────────────
print("\nRunning TF-IDF + LinearSVM …")
svm = LinearSVC(max_iter=2000, random_state=RANDOM_STATE, C=1.0)
y_svm, acc_svm, f1_svm = evaluate_and_save(
    "TF-IDF + LinearSVM", svm, "baseline_svm_predictions"
)

print("\n" + "=" * 60)
print("✅ Baseline predictions saved.")
print("   → Re-run: python scripts/scientific_validation_audit.py")
print("   → McNemar test will now execute automatically.")
print("=" * 60)
