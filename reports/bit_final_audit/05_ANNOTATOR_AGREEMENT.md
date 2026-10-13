# BIT AUDIT PHASE 5: ANNOTATOR AGREEMENT AND RELIABILITY AUDIT REPORT

**Audit Date:** 2026-10-13T18:12:05+07:00  
**Gold Benchmark File:** `data/annotation/multi_annotator_batch_100_GOLD.csv` ($n = 100$)  
**Researcher Reference File:** `data/annotation/researcher_batch_100_FILLED.csv` ($n = 100$)  
**Future Protocol Templates:** `data/annotation/double_blind/` (Status: `NOT_VERIFIED` when unannotated)  

---

## 1. Empirical Agreement Metrics Across Independent Annotators

| Annotator Pair / Composition | Metric | Empirical Value | Landis & Koch (1977) Interpretation |
| :--- | :---: | :---: | :--- |
| **Annotator 1 $\leftrightarrow$ Annotator 2 (Human-Human)** | **Raw Agreement** | **95.00%** (95/100) | Consensual understanding of crisis affective discourse |
| **Annotator 1 $\leftrightarrow$ Annotator 2 (Human-Human)** | **Cohen's Kappa ($\kappa$)** | **0.9135** | **Almost Perfect Agreement** |
| **Tri-Rater (Annotator 1, Annotator 2, IndoBERT)** | **Fleiss' Kappa ($\kappa_{Fleiss}$)** | **0.8442** | **Almost Perfect Agreement** |
| **Tri-Rater (Annotator 1, Annotator 2, IndoBERT)** | **Krippendorff's Alpha ($\alpha$)** | **0.8447** | **Almost Perfect Reliability** |
| **IndoBERT $\leftrightarrow$ Consensus Gold ($n=100$)** | **Accuracy** | **90.00%** (90/100) | Robust zero-shot transfer onto curated benchmark |
| **IndoBERT $\leftrightarrow$ Consensus Gold ($n=100$)** | **Cohen's Kappa ($\kappa$)** | **0.8243** | **Almost Perfect Agreement** |
| **IndoBERT $\leftrightarrow$ Consensus Gold ($n=100$)** | **Macro F1-Score** | **0.8097** | Balanced across present classes |
| **IndoBERT $\leftrightarrow$ Consensus Gold ($n=100$)** | **Weighted F1-Score** | **0.8991** | Weighted class harmony |

---

## 2. Class Distribution Across Human Annotators ($n = 100$)

| Emotion Category | Annotator 1 ($n$) | Annotator 2 ($n$) | Adjudicated Consensus Gold ($n$) |
| :--- | :---: | :---: | :---: |
| **Jijik (Disgust)** | 56 | 53 | 56 |
| **Percaya (Trust)** | 35 | 34 | 35 |
| **Tertarik (Interest)** | 5 | 7 | 5 |
| **Netral (Neutral)** | 4 | 6 | 4 |
| **Total** | **100** | **100** | **100** |

---

## 3. Hermeneutic Adjudication of Discrepancies (5 Cases)

Disagreements occurred in exactly 5 posts ($5.0\%$) and were resolved through hermeneutic contextual adjudication:
1. **RES-0002:** Administrative press release (*BGN serap 1,28 juta tenaga kerja...*). Annotator 1: Netral, Annotator 2: Tertarik. Adjudicated to **Netral** (factual information without emotional markers).
2. **RES-0013:** Sarcastic post on poison immunity (*Uji coba lagi biar kebal racun...*). Annotator 1: Jijik, Annotator 2: Tertarik. Adjudicated to **Jijik** (cynical mockery of food safety).
3. **RES-0046:** Derisive laughter on spoilt food (*hahahah anjir...*). Annotator 1: Jijik, Annotator 2: Netral. Adjudicated to **Jijik** (mocking derision).
4. **RES-0071:** Inversion praise of insect-infested meal. Annotator 1: Jijik, Annotator 2: Tertarik. Adjudicated to **Jijik** (paralinguistic sarcasm inversion).
5. **RES-0089:** Inquisitive critique on supplier selection. Annotator 1: Netral, Annotator 2: Percaya. Adjudicated to **Netral** (balanced inquiry).

---

## 4. Verification of Unannotated Templates
- The reserve templates `data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1.csv` and `2.csv` contain empty labels.
- Running `scripts/setup_double_blind_annotation.py` programmatically returns **`NOT_VERIFIED`** (`cohen_kappa: None`), proving the evaluation harness guards against synthetic assertions.

---

## 5. Audit Status
* **Annotator Agreement Status:** **`PASS`** (Empirical raw Cohen's Kappa = 0.9135 on $n=100$ gold benchmark).
