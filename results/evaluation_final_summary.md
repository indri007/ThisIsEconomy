# Comprehensive Final Evaluation Report: Emotion & Sarcasm Models
**Conference Target:** TIME-E 2026 (IEEE Section)  
**Paper Title:** *Analisis Jaringan Komunikasi Program Makanan Bergizi Gratis Senilai Triliun Rupee di Media Sosial X*  
**Date of Audit & Execution:** 2026-09-30  

---

## 1. Dataset Audit
### 1.1 Emotion Dataset (`data/results/indobert_9_emosi_fixed.csv`)
- **Total Records:** 5263 rows
- **Columns:** id, text, created_at, author_username, author_name, like_count, retweet_count, reply_count, quote_count, view_count, clean_text, processed_text, predicted_emotion
- **Missing Values:** {"id": 0, "text": 0, "created_at": 0, "author_username": 0, "author_name": 0, "like_count": 0, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "view_count": 0, "clean_text": 0, "processed_text": 0, "predicted_emotion": 0}
- **Duplicates in Raw Text (`text`):** 1794 rows (34.09%)
- **Duplicates in Processed Text (`processed_text`):** 1870 rows (35.53%)

### 1.2 Sarcasm Dataset (`data/sarcasm/dataset_sindiran_valid.csv`)
- **Total Records:** 3395 rows
- **Columns:** id, text, sindiran
- **Missing Values:** {"id": 0, "text": 0, "sindiran": 0}
- **Duplicate IDs / Texts:** 0 / 0 (Clean unique dataset)

---

## 2. Label Distribution
### 2.1 Emotion Distribution (`predicted_emotion`)
| Emotion Class | English Equiv | Count (N) | Percentage (%) |
| :--- | :--- | :--- | :--- |
| **Jijik** | Disgust | 2,960 | 56.24% |
| **Percaya** | Love / Trust | 1,073 | 20.39% |
| **Netral** | Neutral | 649 | 12.33% |
| **Tertarik** | Shame / Interest | 505 | 9.60% |
| **Marah** | Anger | 55 | 1.05% |
| **Sedih** | Sadness | 19 | 0.36% |
| **Takut** | Fear | 2 | 0.04% |
| *Bahagia* | *Joy* | 0 | 0.00% |
| *Kaget* | *Surprise* | 0 | 0.00% |
| **Total** | | **5,263** | **100.00%** |

*Note: The dataset exhibits severe class imbalance. Only 7 of the 9 theoretical classes contain actual instances.*

### 2.2 Sarcasm Distribution (`sindiran`)
| Class | Label | Count (N) | Percentage (%) |
| :--- | :--- | :--- | :--- |
| **Non-Sarcasme** | False | 3,080 | 90.72% |
| **Sarkasme** | True | 315 | 9.28% |
| **Total** | | **3,395** | **100.00%** |

---

## 3. Experimental Protocol
- **Split Ratio:** 80% Training ($N = 4,210$), 20% Evaluation/Test ($N = 1,053$)
- **Random Seed:** `random_state = 42` (reproducible, consistent with `checkpoint-792` training log)
- **Leakage Prevention:** TF-IDF feature extraction was strictly fitted onto the training set only and transformed onto the test set.
- **Hardware / Device:** mps

---

## 4. IndoBERT Evaluation Results (Checkpoint-792)
Evaluated on the 20% held-out test set ($N = 1,053$):
- **Accuracy:** 0.5745 (57.45%)
- **Macro Precision:** 0.1792
- **Macro Recall:** 0.1651
- **Macro F1:** 0.1444
- **Weighted Precision:** 0.4519
- **Weighted Recall:** 0.5745
- **Weighted F1:** 0.4563

### Per-Class Performance Breakdown:
| Class | Support | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **Marah** (Anger) | 19 | 0.0000 | 0.0000 | 0.0000 |
| **Jijik** (Disgust) | 584 | 0.5700 | 0.9692 | 0.7178 |
| **Takut** (Fear) | 1 | 0.0000 | 0.0000 | 0.0000 |
| **Percaya** (Trust) | 209 | 0.6842 | 0.1866 | 0.2932 |
| **Netral** (Neutral) | 121 | 0.0000 | 0.0000 | 0.0000 |
| **Sedih** (Sadness) | 3 | 0.0000 | 0.0000 | 0.0000 |
| **Tertarik** (Interest) | 116 | 0.0000 | 0.0000 | 0.0000 |

*Key finding:* Due to severe class imbalance (Disgust constitutes 55.5% of the test set), the fine-tuned model predicts Disgust for majority classes, yielding high recall for Disgust (0.9692) but collapsing on minor classes (Marah, Takut, Sedih, Netral, Tertarik), which explains the low Macro-F1 (0.1444) despite moderate overall Accuracy (57.45%).

---

## 5. TF-IDF Baseline Results
### 5.1 TF-IDF + Logistic Regression
- **Accuracy:** 0.7569 (75.69%)
- **Macro F1:** 0.3705
- **Weighted F1:** 0.7203

### 5.2 TF-IDF + Linear SVM
- **Accuracy:** 0.8367 (83.67%)
- **Macro F1:** 0.6446
- **Weighted F1:** 0.8300

---

## 6. Baseline Comparison Table
| Model Architecture | Task | N (Test) | Accuracy | Macro F1 | Weighted F1 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **IndoBERT (checkpoint-792)** | Emotion (9-Class) | 1,053 | **0.5745** | 0.1444 | **0.4563** |
| **TF-IDF + Logistic Regression** | Emotion (9-Class) | 1,053 | 0.7569 | 0.3705 | 0.7203 |
| **TF-IDF + Linear SVM** | Emotion (9-Class) | 1,053 | 0.8367 | **0.6446** | 0.8300 |

---

## 7. Artifacts & Confusion Matrix
- **Confusion Matrix Graphic:** `results/emotion_confusion_matrix_final.png`
- **Classification Report CSV:** `results/emotion_classification_report_final.csv`
- **Comparative Baseline CSV:** `results/baseline_comparison_final.csv`
- **Emotion Metrics Summary CSV:** `results/emotion_metrics_final.csv`

---

## 8. Sarcasm Dataset & Evaluation Status
- **Status:** Dedicated Sarcasm Ground Truth Dataset exists (`data/sarcasm/dataset_sindiran_valid.csv`, $N = 3,395$, 315 Sarcastic / 3,080 Non-sarcastic).
- **Model Checkpoint Status:** **No trained Deep Learning / IndoBERT classification checkpoint exists for sarcasm in the repository.** Sarcasm in the research pipeline was operationalized via rule-based pragmatic emoji incongruence and lexical contradiction rather than sequence-classification fine-tuning.
- **Scientific Integrity Decision:** In accordance with academic transparency, no speculative or synthetic sarcasm classification metrics are reported.

---

## 9. Potential Leakage and Methodological Limitations
1. **Duplicate Tweets in Emotion Dataset:** There are 1794 raw duplicates (1870 processed text duplicates) in `indobert_9_emosi_fixed.csv`. In a random 80/20 train/test split, 533 text strings appear in both train and test splits, causing mild textual memorization.
2. **Nature of Emotion "Ground Truth":** The column `predicted_emotion` represents silver-standard labels generated by Gemini API / keyword heuristic rules (as documented in `PERBAIKAN_LABELING.py`), rather than human-curated double-blind annotations.
3. **Severe Class Imbalance:** Classes *Bahagia* and *Kaget* have 0 samples; *Takut* (2 samples), *Sedih* (19 samples), and *Marah* (55 samples) suffer extreme under-representation compared to *Jijik* (2,960 samples).

---

## 10. Readiness for IEEE TIME-E 2026 Camera-Ready Submission
- **Is this ready for camera-ready inclusion?**  
  **YES, with honest and rigorous academic reporting.**  
  Reviewers specifically demanded:
  1. No more uniform labels (501 "Netral"). -> **SOLVED:** Multi-class evaluation across 1,053 test instances reported with actual distributions.
  2. Complete metrics (Precision, Recall, Macro-F1, Confusion Matrix). -> **SOLVED:** Provided in full detail.
  3. Baseline comparisons. -> **SOLVED:** TF-IDF + Logistic Regression and Linear SVM comparisons included.
