# BIT AUDIT PHASE 1: NINE-CLASS INDOBERT EMPIRICAL VALIDATION REPORT

**Audit Date:** 2026-10-13T18:08:38+07:00  
**Target Test Set:** `results/emotion_test_group_split.csv` ($N = 1,064$)  
**Prediction Source:** `results/indobert_test_predictions_9_labels.csv` ($N = 1,064$)  
**Model Architecture:** `indobenchmark/indobert-base-p2` with Class-Weighted Cross-Entropy Loss  
**Evaluation Protocol:** Group-aware text normalization split (`GroupShuffleSplit`, zero text leakage)  

---

## 1. Summary of Macro & Global Metrics

| Metric | Empirical Value | Percentage | Note / Convention |
| :--- | :---: | :---: | :--- |
| **Global Accuracy** | **0.791353** | **79.14%** | 842 correctly predicted out of 1,064 test samples |
| **Macro Precision** | **0.506884** | **50.69%** | `zero_division=0` |
| **Macro Recall** | **0.484566** | **48.46%** | `zero_division=0` |
| **Macro F1-Score** | **0.480955** | **48.10%** | Unweighted average across all 9 Plutchik classes |
| **Weighted F1-Score** | **0.788916** | **78.89%** | Sample-weighted average based on class support |
| **Train/Test Leakage** | **0** | **0.00%** | Exact text overlap between train and test partitions |

---

## 2. Granular Per-Class Performance Breakdown

| Emotion Class | Support ($n$) | Precision | Recall | F1-Score | Empirical Status & Qualitative Error Behavior |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Marah (Anger)** | 12 | 0.7000 | 0.5833 | **0.6364** | **VERIFIED**: 7/12 predicted correctly. 5/12 predicted as Netral (flat critique without aggressive tokens). |
| **Jijik (Disgust)** | 590 | 0.8668 | 0.8051 | **0.8348** | **VERIFIED**: Dominant majority class (visceral reaction to spoilt food, maggot-infested meals, food poisoning). |
| **Takut (Fear)** | 0 | 0.0000 | 0.0000 | **0.0000** | **LIMITATION (NOT_EVALUATED)**: Extreme natural minority in corpus ($n=2$ in train, $n=0$ in test set). Cannot evaluate fear detection on this test set. |
| **Bahagia (Joy)** | 14 | 0.3333 | 0.0714 | **0.1176** | **ACTIVE**: 1 correctly predicted as Joy; 6 absorbed into Disgust (sarcastic mock praise), 6 into Tertarik, 1 into Percaya. |
| **Sedih (Sadness)** | 2 | 0.0000 | 0.0000 | **0.0000** | **SEMANTIC ABSORPTION**: Both 2 samples predicted as Jijik (*Moral Disgust* over child illness). |
| **Kaget (Surprise)** | 6 | 0.0000 | 0.0000 | **0.0000** | **SEMANTIC ABSORPTION**: All 6 samples predicted as Jijik (outrage at menu discrepancy). |
| **Percaya (Trust)** | 218 | 0.7216 | 0.8440 | **0.7780** | **VERIFIED**: Strong affirmative institutional communication. |
| **Tertarik (Interest)** | 93 | 0.5455 | 0.7742 | **0.6400** | **VERIFIED**: Public inquiries and anticipation. |
| **Netral (Neutral)** | 129 | 0.8879 | 0.7984 | **0.8408** | **VERIFIED**: Factual journalistic reports and budget summaries. |

---

## 3. Full 9×9 Empirical Confusion Matrix ($N = 1,064$)

| True Class \ Pred | Marah | Jijik | Takut | Bahagia | Sedih | Kaget | Percaya | Tertarik | Netral | Total True |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Marah** | **7** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | **12** |
| **Jijik** | 0 | **475** | 0 | 1 | 0 | 0 | 64 | 44 | 6 | **590** |
| **Takut** | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **Bahagia** | 0 | 6 | 0 | **1** | 0 | 0 | 1 | 6 | 0 | **14** |
| **Sedih** | 0 | 2 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | **2** |
| **Kaget** | 0 | 6 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | **6** |
| **Percaya** | 1 | 26 | 0 | 0 | 0 | 0 | **184** | 6 | 1 | **218** |
| **Tertarik** | 0 | 14 | 0 | 0 | 0 | 0 | 6 | **72** | 1 | **93** |
| **Netral** | 2 | 19 | 0 | 1 | 0 | 0 | 0 | 4 | **103** | **129** |
| **Total Pred** | **10** | **542** | **0** | **3** | **0** | **0** | **255** | **132** | **122** | **1,064** |

---

## 4. Key Scientific Findings & Limitations

1. **Extreme Imbalance Ratio:** Disgust ($n=590$) vs Sadness ($n=2$) is a 295:1 imbalance. In real-world disaster/crisis public health discourses, citizens overwhelmingly manifest moral disgust rather than nuanced personal sadness.
2. **Honest Accounting of Zero Support:** Fear (*Takut*) has 0 instances in the holdout test set. Therefore, the scientific claim cannot state that fear classification is validated; it must state that fear is unrepresented in the test partition.
3. **Reproducibility Files:**
   - Metrics CSV: `reports/bit_final_audit/01_NINE_CLASS_METRICS.csv`
   - Confusion Matrix CSV: `reports/bit_final_audit/01_CONFUSION_MATRIX.csv`
   - Sample-Level Mapping: `reports/bit_final_audit/01_SAMPLE_LEVEL_PREDICTIONS.csv`
