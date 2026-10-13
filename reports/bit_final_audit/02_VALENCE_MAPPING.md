# BIT AUDIT PHASE 2: HIERARCHICAL VALENCE SUPER-CLASS MAPPING REPORT

**Audit Date:** 2026-10-13T18:09:14+07:00  
**Mapping Configuration File:** `config/valence_super_class_mapping.json`  
**Test Set Size:** $N = 1,064$ holdout samples (`results/emotion_test_group_split.csv`)  
**Theoretical Framework:** Circumplex Model of Affect (Russell, 1980) & Situational Crisis Communication Stance (Coombs, 2007)  

---

## 1. Explicit Taxonomy Mapping & Theoretical Grounding

The 9 granular Plutchik emotions are mapped into 3 functional communication postures (Super-Classes):

| Granular Emotion (Plutchik) | Super-Class (Valence Stance) | Theoretical Justification |
| :--- | :---: | :--- |
| **Marah (Anger)** | **Negatif** (Dissent) | Explicit public outrage and institutional reproach. |
| **Jijik (Disgust)** | **Negatif** (Dissent) | Visceral moral revulsion against spoilt food, unhygienic menus, and food poisoning. |
| **Takut (Fear)** | **Negatif** (Dissent) | Apprehension and anxiety regarding public health and child safety. |
| **Sedih (Sadness)** | **Negatif** (Dissent) | Sympathy and sorrow for affected school children. |
| **Kaget (Surprise)** | **Negatif** (Dissent) | In the MBG crisis context, surprise manifests as shock at budgetary irregularities or poor food quality. |
| **Percaya (Trust)** | **Positif** (Support) | Affirmative civic trust and governmental program endorsement. |
| **Tertarik (Interest)** | **Positif** (Support) | Anticipation, hopeful questions, and constructive participation in program rollout. |
| **Bahagia (Joy)** | **Positif** (Support) | Gratitude, delight, and celebration of meal provision. |
| **Netral (Neutral)** | **Netral** (Objective) | Journalistic factual reporting, logistical schedules, and balanced commentary. |

> **⚠️ Critical Epistemological Note:**  
> The shift from Granular Macro-F1 (48.10%) to Valence Macro-F1 (81.73%) **is NOT an algorithmic improvement of the model**.  
> Rather, it evaluates the model under a **different task granularity** (3-class stance detection vs. 9-class discrete affective classification). Both metrics are reported side-by-side to maintain full scientific transparency.

---

## 2. Empirical Performance Metrics ($N = 1,064$)

| Evaluation Metric | Granular 9-Emotion Task | 3-Tier Valence Super-Class Task | Nature of Difference |
| :--- | :---: | :---: | :--- |
| **Accuracy** | **79.14%** (0.791353) | **81.67%** (0.816729) | +2.53% (cross-class within valence resolved) |
| **Macro Precision** | **50.69%** (0.506884) | **82.46%** (0.824587) | +31.77% |
| **Macro Recall** | **48.46%** (0.484566) | **81.70%** (0.816986) | +33.24% |
| **Macro F1-Score** | **48.10%** (0.480955) | **81.73%** (0.817295) | +33.63% (mitigates minority penalty) |
| **Weighted F1-Score** | **78.89%** (0.788916) | **81.88%** (0.818787) | +2.99% |

---

## 3. Per-Super-Class Detail ($N = 1,064$)

| Super-Class | Test Support ($n$) | Precision | Recall | F1-Score | Substantive Meaning |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Negatif (Dissent)** | 610 | 0.8781 | 0.8033 | **0.8390** | Highly robust identification of crisis dissent. |
| **Positif (Support)** | 325 | 0.7077 | 0.8492 | **0.7720** | Effective identification of policy support and positive engagement. |
| **Netral (Objective)** | 129 | 0.8879 | 0.7984 | **0.8408** | Sharp discrimination of factual news from opinionated discourse. |

---

## 4. Super-Class Confusion Matrix (3×3)

| True \ Predicted | Negatif | Positif | Netral | Total True |
| :--- | :---: | :---: | :---: | :---: |
| **Negatif** | **490** | 109 | 11 | **610** |
| **Positif** | 47 | **276** | 2 | **325** |
| **Netral** | 21 | 5 | **103** | **129** |
| **Total Predicted** | **558** | **390** | **116** | **1,064** |

---

## 5. Artifact Reference
- Configuration File: `config/valence_super_class_mapping.json`
- Metrics CSV: `reports/bit_final_audit/02_VALENCE_METRICS.csv`
- Confusion Matrix CSV: `reports/bit_final_audit/02_VALENCE_CONFUSION_MATRIX.csv`
