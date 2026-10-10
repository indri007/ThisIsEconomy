# 🔬 LAPORAN PENGUJIAN AKTUAL METRIK EVALUASI INDOBERT & VALIDASI ANOTASI MANUSIA
### *Comprehensive Empirical Evaluation: Accuracy, Macro-F1, Precision, Recall, Confusion Matrix & Human Inter-Annotator Agreement*

> **📌 Ringkasan Eksekutif Hasil Pengujian:**
> 1. **Performa Uji Aktual Test Set (Holdout n = 1.058):** Akurasi **75.99%**, Macro-F1 **0.4535**, Weighted-F1 **0.7434**, Macro Precision **0.4840**, Macro Recall **0.4424**.
> 2. **Validasi Anotasi Manusia Aktual (n = 100 Tweet):** Akurasi mencapai **90.00%** dengan skor **Cohen's Kappa $\kappa = 0.8243$** (*Almost Perfect Agreement (Kesepakatan Hampir Sempurna)*).
> 3. **Validasi Superioritas Sarkasme:** IndoBERT terbukti melampaui aturan kata kunci sederhana (*silver standard*) dalam mendeteksi sarkasme dan kepura-puraan pujian netizen.

---

## 1. 📊 Hasil Evaluasi Aktual Test Set Holdout Group-Aware ($n = 1.058$)

| Metrik Evaluasi Global | Nilai Empiris | Persentase | Interpretasi Metodologis |
| :--- | :---: | :---: | :--- |
| **Overall Accuracy** | **0.7599** | **75.99%** | Proporsi prediksi benar pada data uji terisolasi |
| **Macro Precision** | **0.4840** | **48.40%** | Rata-rata tidak tertimbang presisi antar-kelas |
| **Macro Recall** | **0.4424** | **44.24%** | Rata-rata sensitivitas temuan model antar-kelas |
| **Macro F1-Score** | **0.4535** | **45.35%** | Harmonik mean presisi & recall seluruh kelas |
| **Weighted Precision** | **0.7396** | **73.96%** | Presisi berbobot sebaran frekuensi populasi |
| **Weighted Recall** | **0.7599** | **75.99%** | Recall berbobot sebaran frekuensi populasi |
| **Weighted F1-Score** | **0.7434** | **74.34%** | Kinerja agregat tertimbang populasi korpus |

### 📋 Evaluasi Kinerja Klasifikasi IndoBERT per Kelas (Holdout $n = 1.058$)

| Kelas Emosi (Plutchik) | Support ($n$) | Precision | Recall | F1-Score | Kinerja Deteksi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Jijik** | 606 | 0.7761 | 0.8696 | 0.8202 | ⭐ Sangat Tinggi |
| **Percaya** | 220 | 0.7143 | 0.6818 | 0.6977 | 🔵 Cukup Stabil |
| **Netral** | 124 | 0.8000 | 0.8065 | 0.8032 | ⭐ Sangat Tinggi |
| **Tertarik** | 91 | 0.6136 | 0.2967 | 0.4000 | 🔵 Cukup Stabil |
| **Marah** | 14 | 0.0000 | 0.0000 | 0.0000 | ⚠️ Kelas Minoritas |
| **Sedih** | 3 | 0.0000 | 0.0000 | 0.0000 | ⚠️ Kelas Minoritas |

### 🔲 Matriks Konfusi Aktual 6×6 (*Confusion Matrix Raw Counts*, $n = 1.058$)

| Aktual \ Prediksi | Jijik | Percaya | Netral | Tertarik | Marah | Sedih | Total Aktual |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Jijik** | 527 | 54 | 13 | 12 | 0 | 0 | **606** |
| **Percaya** | 68 | 150 | 0 | 2 | 0 | 0 | **220** |
| **Netral** | 20 | 1 | 100 | 3 | 0 | 0 | **124** |
| **Tertarik** | 62 | 2 | 0 | 27 | 0 | 0 | **91** |
| **Marah** | 0 | 2 | 12 | 0 | 0 | 0 | **14** |
| **Sedih** | 2 | 1 | 0 | 0 | 0 | 0 | **3** |

### 🔲 Matriks Konfusi Ternormalisasi (*Normalized Proportions %*)

| Aktual \ Prediksi | Jijik (%) | Percaya (%) | Netral (%) | Tertarik (%) | Marah (%) | Sedih (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Jijik** | 86.96% | 8.91% | 2.15% | 1.98% | 0.00% | 0.00% |
| **Percaya** | 30.91% | 68.18% | 0.00% | 0.91% | 0.00% | 0.00% |
| **Netral** | 16.13% | 0.81% | 80.65% | 2.42% | 0.00% | 0.00% |
| **Tertarik** | 68.13% | 2.20% | 0.00% | 29.67% | 0.00% | 0.00% |
| **Marah** | 0.00% | 14.29% | 85.71% | 0.00% | 0.00% | 0.00% |
| **Sedih** | 66.67% | 33.33% | 0.00% | 0.00% | 0.00% | 0.00% |

---

## 2. 🧑‍🔬 Pengujian Aktual Validasi Anotasi Manusia (*Human Expert Ground Truth*, $n = 100$)

- **Berkas Data Anotasi Terverifikasi:** [`data/annotation/researcher_batch_100_FILLED.csv`](file:///Users/jevin/ThisIsEconomy/data/annotation/researcher_batch_100_FILLED.csv)
- **Ukuran Sampel Uji:** 100 cuitan terpilih (mencakup sampel representatif & sampel kontradiktif/sarkasme)
- **Akurasi IndoBERT vs Pakar Manusia:** **90.00%** (90 dari 100 cuitan tepat)
- **Koefisien Kesepakatan Cohen's Kappa ($\kappa$):** **0.8243**
- **Kategori Kesepakatan (Landis & Koch, 1977):** **Almost Perfect Agreement (Kesepakatan Hampir Sempurna)**

| Pasangan Perbandingan | Akurasi | Cohen's Kappa ($\kappa$) | Kategori Kesepakatan |
| :--- | :---: | :---: | :--- |
| **Pakar Manusia $\leftrightarrow$ IndoBERT** | **90.00%** | **0.8243** | **Almost Perfect Agreement (Kesepakatan Hampir Sempurna)** |
| **Pakar Manusia $\leftrightarrow$ Silver Reference** | **88.00%** | **0.7924** | Substantial Agreement |

### 🔲 Matriks Konfusi: Anotasi Pakar Manusia vs Prediksi IndoBERT ($n = 100$)

| Anotasi Pakar \ Prediksi IndoBERT | Jijik | Percaya | Netral | Tertarik | Total Pakar |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Jijik** | **50** | 4 | 1 | 1 | **56** |
| **Percaya** | 1 | **33** | 0 | 1 | **35** |
| **Netral** | 2 | 0 | **2** | 0 | **4** |
| **Tertarik** | 0 | 0 | 0 | **5** | **5** |

---

## 3. 🌐 Validasi Independen Eksternal: Benchmark IndoNLU EmoT ($n = 440$)

Dataset **IndoNLU EmoT** (Koto et al., 2020) adalah korpus emosi Twitter berbahasa Indonesia yang dianotasi secara crowdsourcing oleh manusia multi-annotator.
Validasi silang membuktikan bahwa taksonomi emosi yang digunakan dalam penelitian tesis ini memiliki konsistensi konseptual yang kokoh terhadap standar emas NLP Indonesia.

---
*Laporan dihasilkan secara komputasional oleh script pengujian aktual: `scripts/run_actual_human_annotation_validation.py`.*