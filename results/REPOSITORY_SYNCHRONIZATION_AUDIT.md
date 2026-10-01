# REPOSITORY SYNCHRONIZATION AUDIT REPORT
**Timestamp:** 2026-09-30 15:50:00 WIB  
**Status:** PASS (All components synchronized to Source of Truth)

---

## 1. Files Modified

| No | File Path | Scope of Modification |
| :---: | :--- | :--- |
| 1 | `README.md` | Replaced legacy 83% claims and checkpoint-792 ($n=1.053$) with the verified group-aware multi-model evaluation table ($n=1.058$, checkpoint-264). Added `## Final Machine Learning Evaluation` section. |
| 2 | `mbg-sna-github/README.md` | Synchronized identical changes to the package repository documentation. |
| 3 | `dashboard/app.py` | Integrated `load_final_evaluation()` to dynamically pull metrics from CSVs in `results/`. Replaced hardcoded legacy metrics with dynamic metric cards, dynamic multi-model comparison table (Tabel 4.4a), dynamic per-class evaluation table (Tabel 4.4b), and 300 DPI confusion matrix toggle (Counts / Normalized). |
| 4 | `mbg-sna-github/dashboard/app.py` | Synchronized identical dynamic evaluation implementation and path resolution for package deployment. |
| 5 | `mbg-sna-github/results/*` | Synced final CSV and image assets (`FINAL_MODEL_COMPARISON.csv`, `FINAL_PER_CLASS_ANALYSIS.csv`, `FINAL_CLASS_DISTRIBUTION.csv`, `FINAL_indobert_metrics.csv`, `final_split_verification.csv`, `TABLE_FINAL_RESULTS.csv`, `FINAL_indobert_confusion_matrix.png`, `FINAL_indobert_confusion_matrix_normalized.png`). |

---

## 2. Old Metrics Removed & Recontextualized

- **Akurasi 83.00% & Macro F1 0.8122:** Replaced from active claim status in Bab II benchmark tables. Recontextualized clearly as an exploratory developmental run that was superseded by strict zero-leakage group-aware holdout protocols.
- **Checkpoint-792 & $n=1.053$:** Removed from all active evaluation sections in README and both dashboards. Replaced with `checkpoint-264` evaluated on the independent holdout partition ($n=1.058$).
- **Akurasi 57.45%, Weighted F1 0.4563, Macro F1 0.1444:** Completely removed from `dashboard/app.py` and `mbg-sna-github/dashboard/app.py`. All metric cards now load dynamically from verified evaluation CSVs.

---

## 3. Final Metrics Loaded from Source-of-Truth

All metrics directly reflect the verified files `results/FINAL_MODEL_COMPARISON.csv` and `results/FINAL_PER_CLASS_ANALYSIS.csv`:

### Multi-Model Comparison ($n=1,058$ Test Holdout, Zero Leakage)
- **TF-IDF + Logistic Regression:** Accuracy = `0.6947`, Macro-F1 = `0.3429`, Weighted-F1 = `0.6457`
- **TF-IDF + Linear SVM:** Accuracy = `0.6720`, Macro-F1 = `0.4095`, Weighted-F1 = `0.6558`
- **IndoBERT Group-Aware (checkpoint-264):** Accuracy = `0.7940` (79.40%), Macro-F1 = `0.5160`, Weighted-F1 = `0.7851`
- **Macro Precision:** `0.6726`, **Macro Recall:** `0.4977`

### Per-Class Support & F1 ($N=1,058$ Total Support)
- **Disgust (Jijik):** Support = `606` (57.28%), Precision = `0.8176`, Recall = `0.8729`, F1 = `0.8444`
- **Trust (Percaya):** Support = `220` (20.79%), Precision = `0.7511`, Recall = `0.7545`, F1 = `0.7528`
- **Neutral (Netral):** Support = `124` (11.72%), Precision = `0.8347`, Recall = `0.8145`, F1 = `0.8245`
- **Interest (Tertarik):** Support = `91` (8.60%), Precision = `0.6324`, Recall = `0.4725`, F1 = `0.5409`
- **Anger (Marah):** Support = `14` (1.32%), Precision = `1.0000`, Recall = `0.0714`, F1 = `0.1333`
- **Sadness (Sedih):** Support = `3` (0.28%), Precision = `0.0000`, Recall = `0.0000`, F1 = `0.0000`

---

## 4. Dashboard Data Sources

The function `load_final_evaluation()` implements dynamic multi-path fallback searching `base_dir / "results"`, `base_dir.parent / "results"`, and `cwd / "results"`.
Data frames are read directly from:
- `results/FINAL_MODEL_COMPARISON.csv`
- `results/FINAL_PER_CLASS_ANALYSIS.csv`
- `results/FINAL_CLASS_DISTRIBUTION.csv`
- `results/FINAL_indobert_metrics.csv`
- `results/FINAL_indobert_confusion_matrix.png`
- `results/FINAL_indobert_confusion_matrix_normalized.png`

Zero hardcoded metric arrays exist in Section 4.5.

---

## 5. Syntax Check

Executed via Python standard library:
```bash
python -m py_compile dashboard/app.py
python -m py_compile mbg-sna-github/dashboard/app.py
```
**Result:** Both dashboard applications compile with **ZERO errors** (`SYNTAX OK`).

---

## 6. README Consistency

Both `README.md` (root) and `mbg-sna-github/README.md` contain:
- Unified `## Final Machine Learning Evaluation` section.
- Multi-model comparative table (TF-IDF LR, Linear SVM, IndoBERT).
- Per-class breakdown table with support summing exactly to 1,058.
- Explicit statements on `GroupShuffleSplit`, `random_state=42`, zero lexical overlap, and silver-standard reference labels.
- Sarcasm documented as rule-based linguistic incongruence detection ($N=3,395$, 315 true instances), avoiding false machine learning classifier claims.

---

## 7. Dashboard Consistency

Both `dashboard/app.py` and `mbg-sna-github/dashboard/app.py`:
- Contain identical `load_final_evaluation()` routines.
- Present 4 metric cards dynamically displaying Test N (1,058), IndoBERT Accuracy (79.40%), Macro F1 (0.5160), and Weighted F1 (0.7851).
- Include interactive radio toggle between Raw Counts and Normalized Confusion Matrix plots.
- Include Table 4.4a (Multi-model comparative baselines) and Table 4.4b (Per-class support breakdown).
- Display standard methodological caption acknowledging silver-standard reference labels and zero-leakage group-aware partitioning.

---

## 8. Remaining Warnings & Scorecard

- **Critical Issues:** 0
- **Warnings:** 0
- **Final Status:** **PASS**
