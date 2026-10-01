# Final Evaluation Report

## 1. Dataset
- **Total Samples:** 5263 tweets
- **Unique Raw Texts:** 3469
- **Train Partition Size:** 4205 (79.90%)
- **Test Partition Size:** 1058 (20.10%)

## 2. Reference Label Provenance
The reference labels originate from the `predicted_emotion` column. Traced through `scripts/PERBAIKAN_LABELING.py` and `tesis_text.txt` line 310, these are **silver-standard reference labels** produced via an automated pipeline (Gemini API + rule-based heuristic keyword filters). They must strictly be acknowledged as **SILVER-STANDARD** and not human-annotated gold standard.

## 3. Class Distribution
The dataset exhibits severe class imbalance:
- **Jijik (Disgust):** 56.24%
- **Percaya (Trust):** 20.39%
- **Netral (Neutral):** 12.33%
- **Tertarik (Interest):** 9.60%
- **Marah (Anger):** 1.05%
- **Sedih (Sadness):** 0.36%
- **Takut (Fear):** 0.04%
- **Bahagia & Kaget:** 0.00% (Absent)

## 4. Duplicate and Conflict Audit
- **Total Duplicate Text Groups:** 1494
- **Conflicting Labels Across Duplicates:** 0 (All identical text occurrences share identical labels)

## 5. Leakage Audit
- **Original Checkpoint (checkpoint-792):** Leakage detected (533 overlapping texts).
- **Group-Aware Split:** Leakage strictly eliminated.
  - Raw Text Overlap: 0
  - Processed Text Overlap: 0

## 6. Group-Aware Split
Generated via `GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)` grouped by `processed_text`.

## 7. IndoBERT Training
- **Base Architecture:** `indobenchmark/indobert-base-p2`
- **Trained on:** 4205 group-aware train instances (3 epochs, batch size 32, seed 42)
- **Checkpoint Selected:** `checkpoint-264` (eval_loss: 0.5677, lowest validation loss)

## 8. IndoBERT Final Results
Evaluated exclusively on the unseen group-aware test set ($N = 1058$):
- **Accuracy:** 0.7940
- **Macro Precision:** 0.6726
- **Macro Recall:** 0.4977
- **Macro F1:** 0.5160
- **Weighted Precision:** 0.7900
- **Weighted Recall:** 0.7940
- **Weighted F1:** 0.7851

## 9. TF-IDF Logistic Regression Results
- **Accuracy:** 0.6947
- **Macro F1:** 0.3429
- **Weighted F1:** 0.6457

## 10. TF-IDF Linear SVM Results
- **Accuracy:** 0.6720
- **Macro F1:** 0.4095
- **Weighted F1:** 0.6558

## 11. Model Comparison
| Model | Protocol | Accuracy | Macro-F1 | Weighted-F1 | Valid For Comparison |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | GROUP-AWARE | 0.6947 | 0.3429 | 0.6457 | YES |
| **TF-IDF + Linear SVM** | GROUP-AWARE | 0.6720 | 0.4095 | 0.6558 | YES |
| **IndoBERT Group-Aware** | GROUP-AWARE | 0.7940 | 0.5160 | 0.7851 | YES |

## 12. Per-Class Performance
- Disgust constitutes 57.28% of the test set, where IndoBERT achieved Recall = 0.8729 and F1 = 0.8444.
- Severe imbalance heavily suppresses unweighted Macro-F1 across minority categories (Marah, Sedih, Takut).

## 13. Confusion Matrix
Rendered at 300 DPI:
- Count matrix: `results/FINAL_indobert_confusion_matrix.png`
- Normalized matrix: `results/FINAL_indobert_confusion_matrix_normalized.png`

## 14. Limitations
1. **Silver-Standard Labels:** Reference annotations were model/heuristic generated, not multi-annotator consensus.
2. **Extreme Imbalance:** 7 active classes, with 2 classes absent and 3 classes below 1.5% representation.
3. **No Deep Learning Sarcasm Model:** Sarcasm was extracted via rule-based lexicon and emoji incongruence rather than neural classification.

## 15. Reproducibility
- **Python Environment:** `/Users/jevin/Documents/tesis_mbg/.venv/bin/python`
- **Random Seed:** 42
- **Model Checkpoint:** `results/indobert_group_aware_final/checkpoint-264`

## 16. Final Status
- **Reference labels:** SILVER-STANDARD
- **Test leakage:** NO
- **Group-aware split:** YES
- **Final comparison:** VALID
- **Status:** **VALID_FOR_PAPER**
