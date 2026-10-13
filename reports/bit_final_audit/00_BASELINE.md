# BIT AUDIT PHASE 0: BASELINE AND REPOSITORY INVENTORY

**Timestamp:** 2026-10-13T18:08:00+07:00  
**Repository Path:** `/Users/jevin/Documents/tesis_mbg`  
**Active Branch:** `fix/scientific-validation` (synced with `main` at `fd229de`)  
**Commit SHA:** `fd229de3b80a8ced01ac8a2ab26001eeb3a8ce49`  
**Git Working Tree Status:** Clean  

---

## 1. System & Environment Specifications

- **Operating System:** macOS (Darwin 24.3.0 Darwin Kernel Version 24.3.0)
- **Python Version:** 3.13.11 (Anaconda, Inc.)
- **Key Python Dependencies:**
  - `scikit-learn`: 1.8.0
  - `pandas`: 2.3.3
  - `numpy`: 2.4.0
  - `torch`: 2.10.0
  - `transformers`: 5.8.1
  - `networkx`: 3.4.2
  - `pytest`: 9.1.0

---

## 2. Inventory of Analytical Artifacts & Ground Truth Data

| File Path | Type | Size / Format | Record Count | Description & Provenance |
| :--- | :---: | :---: | :---: | :--- |
| `data/results/indobert_9_emosi_fixed.csv` | File | 3.54 MB / CSV | **5,272** | Master 9-emotion corpus labeled with full taxonomy |
| `results/emotion_train_group_split.csv` | File | 2.87 MB / CSV | **4,208** | GroupShuffleSplit 80% train set (Zero Text Leakage) |
| `results/emotion_test_group_split.csv` | File | 670 KB / CSV | **1,064** | GroupShuffleSplit 20% holdout test set |
| `results/indobert_test_predictions_9_labels.csv` | File | 685 KB / CSV | **1,064** | Model predictions on 9-class holdout test set |
| `results/FINAL_indobert_predictions.csv` | File | 417 KB / CSV | **1,058** | Historical baseline model (Protocol v2, 6 classes) |
| `data/sarcasm/dataset_sindiran_valid.csv` | File | 900 KB / CSV | **3,395** | Sarcasm & interaction validated corpus (315 sarcastic) |
| `data/annotation/multi_annotator_batch_100_GOLD.csv` | File | 33.6 KB / CSV | **100** | Multi-annotator gold standard consensus benchmark |
| `data/annotation/researcher_batch_100_FILLED.csv` | File | 23.6 KB / CSV | **100** | Primary researcher manual annotation benchmark |
| `data/sna/network_edges.csv` | File | 15.6 KB / CSV | **692** (666 unique) | Canonical directed edge list (971 nodes, density 0.0011) |
| `data/network_edges.csv` | Symlink | -> `sna/network_edges.csv` | **692** | Convenience symlink to canonical network edges |
| `data/processed/tweet_mbg_30juta.csv` | File | 6.43 GB / CSV | **30,035,226** (30M) | Raw acquisition streaming lake (unprocessed storage) |
| `data/processed/tweet_mbg_1juta.csv` | Symlink | -> `tweet_mbg_30juta.csv` | **30,035,226** | Historical naming symlink resolving to 30M lake |
| `reports/scientific_validation/DATASET_30M_MANIFEST_AUDIT.json` | File | 1.7 KB / JSON | N/A | Manifest auditing 30M lake & 600 processed sample |
| `reports/scientific_validation/MODEL_EVALUATION_REPORT.md` | File | 3.5 KB / MD | N/A | Evaluation report for 9-class IndoBERT model |
| `results/ZENODO_REPLICATION_PACKAGE_DOI_MBG_2026.zip` | Archive | 5.23 MB / ZIP | 35 files | Standalone FAIR replication bundle (DOI: 10.5281/zenodo.11029482) |

---

## 3. Discrepancies and Clarifications to Reconcile

1. **30M Raw Footprint vs Active NLP Corpus:**
   - The 30M CSV contains raw uncurated tweets harvested via high-throughput streaming.
   - Only 600 samples were processed in the lake demonstration; 29,999,400 remain unprocessed (`BLOCKED` status).
   - Analytical NLP modeling was performed on carefully filtered, relevant cohorts: $N=9,360$ (longitudinal crisis), $N=5,272$ (master 9-emotion), $N=3,395$ (sarcasm/SNA), and $n=100$ (gold standard).
   - *Action:* Reconcile and formalize in `03_DATASET_RECONCILIATION.md` and `03_DATASET_MANIFEST.json`.

2. **9-Emotion Granular Evaluation vs 3-Super-Class Valence Taxonomy:**
   - Granular 9-emotion evaluation yields Accuracy 79.14%, Macro-F1 48.10%, Weighted-F1 78.89%.
   - Extreme minority classes (*Takut* $n=0$, *Sedih* $n=2$, *Kaget* $n=6$, *Bahagia* $n=14$) pull down Macro-F1 due to severe class imbalance (Moral Disgust = 590).
   - When mapped into 3 theoretical valence super-classes (Negative Dissent, Positive Support, Neutral Objective), Macro-F1 is 81.73% and Accuracy is 81.67%.
   - *Action:* Distinctly report and audit both granular and aggregated metrics without conflating them as direct model improvements.

3. **Separation of Evaluation Protocols:**
   - Historical Baseline v2: 6 active classes ($n=1,058$, Accuracy 75.99% / 79.40%, Macro-F1 0.4535 / 0.5160).
   - Master 9-Class Model: 9 classes ($N=1,064$, Accuracy 79.14%, Macro-F1 0.4810).
   - *Action:* Ensure all tests, reports, and code distinctly label these two separate evaluation checkpoints.

---

## 4. Execution Plan & Target Deliverables
The audit will proceed sequentially through Phases 1 to 11, outputting verified artifacts in `reports/bit_final_audit/` and maintaining strict documentation of empirical evidence.
