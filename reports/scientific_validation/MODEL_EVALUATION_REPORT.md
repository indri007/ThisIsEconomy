# Model Evaluation Report: IndoBERT 9 Emosi

## 1. Arsitektur Model & Konfigurasi Output
- **Model Dasar:** `indobenchmark/indobert-base-p2`
- **Konfigurasi Output:** Multi-class classification (9 label potensial).
- **Pemetaan Label:**
  - 0: Marah (Anger)
  - 1: Jijik (Disgust)
  - 2: Takut (Fear)
  - 3: Bahagia (Joy)
  - 4: Sedih (Sadness)
  - 5: Kaget (Surprise)
  - 6: Percaya (Trust)
  - 7: Tertarik (Interest/Anticipation)
  - 8: Netral (Neutral)

## 2. Distribusi Empiris Kelas Korpus Riil (N = 5.263)
Korpus opini media sosial mengenai Program MBG mengalami ketimpangan kelas alami (*extreme natural class imbalance*):
1. **Jijik (Disgust):** 56.24% (2.960 cuitan) — Resistensi dominan terhadap makanan basi, bau, keracunan.
2. **Percaya (Trust):** 20.39% (1.073 cuitan) — Narasi dukungan dari kanal afirmatif/pemerintah.
3. **Netral (Neutral):** 12.33% (649 cuitan) — Laporan faktual/berita.
4. **Tertarik (Interest):** 9.60% (505 cuitan) — Pertanyaan dan antisipasi publik.
5. **Marah (Anger):** 1.05% (55 cuitan).
6. **Sedih (Sadness):** 0.36% (19 cuitan).
7. **Takut (Fear):** 0.04% (2 cuitan).
8. **Bahagia (Joy):** 0.00% (Absent).
9. **Kaget (Surprise):** 0.00% (Absent).

## 3. Evaluasi Holdout Group-Aware (Zero-Leakage Protocol, N = 1.058)
Evaluasi resmi pada data uji tanpa kebocoran teks:
- **Overall Accuracy:** 79.40%
- **Macro Precision:** 0.6726
- **Macro Recall:** 0.4977
- **Macro F1:** 0.5160 (dihitung pada kelas aktif; tertahan akibat skor 0 pada kelas minoritas seperti Sedih/Takut)
- **Weighted F1:** 0.7851

### Performa per Kelas (Active Support):
- **Jijik (Support = 606):** Precision = 0.8176, Recall = 0.8729, F1 = 0.8444
- **Percaya (Support = 220):** Precision = 0.7511, Recall = 0.7545, F1 = 0.7528
- **Netral (Support = 124):** Precision = 0.8347, Recall = 0.8145, F1 = 0.8245
- **Tertarik (Support = 91):** Precision = 0.6324, Recall = 0.4725, F1 = 0.5409
- **Marah (Support = 14):** Precision = 1.0000, Recall = 0.0714, F1 = 0.1333
- **Sedih (Support = 3):** Precision = 0.0000, Recall = 0.0000, F1 = 0.0000

## 4. Evaluasi Komparatif Baseline (Zero-Leakage Split Identik)
| Model | Representasi Fitur | Akurasi | Macro F1 | Weighted F1 | Protokol |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | TF-IDF n-gram | 69.47% | 0.3429 | 0.6457 | Group-Aware |
| **TF-IDF + Linear SVM** | TF-IDF n-gram | 67.20% | 0.4095 | 0.6558 | Group-Aware |
| **IndoBERT Base-p2** | Deep Contextual | **79.40%** | **0.5160** | **0.7851** | Group-Aware |

## 5. Status Validasi Ilmiah
- **Status:** **`PROVISIONAL`**
- **Justifikasi:** Meskipun model memiliki keunggulan signifikan dibanding baseline linier pada kelas mayoritas, klaim kesiapan klasifikasi penuh 9 kelas harus disertai peringatan eksplisit (*caveat*) mengenai ketidakhadiran sampel alami pada kelas *Joy* dan *Surprise*, serta supresi Macro F1 akibat ketimpangan kelas ekstrem.
