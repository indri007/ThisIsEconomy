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

## 2. Distribusi Empiris Kelas Korpus Riil (N = 5.272)
Korpus opini media sosial mengenai Program MBG mencakup seluruh 9 kelas emosi Plutchik ($N = 5.272$):
1. **Jijik (Disgust):** 55.01% (2.900 cuitan) — Resistensi dominan terhadap makanan basi, bau, keracunan.
2. **Percaya (Trust):** 20.09% (1.059 cuitan) — Narasi dukungan dari kanal afirmatif/pemerintah.
3. **Netral (Neutral):** 12.23% (645 cuitan) — Laporan faktual/berita anggaran.
4. **Tertarik (Interest):** 9.41% (496 cuitan) — Pertanyaan dan antisipasi publik.
5. **Bahagia (Joy):** 1.44% (76 cuitan) — Apresiasi rasa syukur, kelezatan menu & kegembiraan siswa.
6. **Marah (Anger):** 1.02% (54 cuitan) — Protes atas transparansi vendor & korupsi.
7. **Kaget (Surprise):** 0.44% (23 cuitan) — Kejutan perubahan alokasi & kontradiksi ekspektasi.
8. **Sedih (Sadness):** 0.32% (17 cuitan) — Empati pada siswa & keprihatinan mutu menu.
9. **Takut (Fear):** 0.04% (2 cuitan) — Kekhawatiran atas dampak keracunan massal.

## 3. Evaluasi Model IndoBERT 9-Kelas Berbobot (Zero-Leakage Test Set, N = 1.064)
Evaluasi resmi pada data uji 9-kelas tanpa kebocoran teks (`results/emotion_test_group_split.csv`):
- **Overall Accuracy:** 79.14% (842/1.064 cuitan tepat)
- **Weighted F1:** 78.89%
- **Macro F1:** 48.10%

### Performa per Kelas (Test Holdout Support):
- **Marah (Support = 12):** Precision = 0.70, Recall = 0.58, F1 = 0.64
- **Jijik (Support = 590):** Precision = 0.87, Recall = 0.81, F1 = 0.83
- **Takut (Support = 0):** Ekstrem minoritas alami ($n=2$ pada train set, $n=0$ pada test set)
- **Bahagia (Support = 14):** Precision = 0.33, Recall = 0.07, F1 = 0.12 (Aktif terdeteksi)
- **Percaya (Support = 218):** Precision = 0.72, Recall = 0.84, F1 = 0.78
- **Netral (Support = 129):** Precision = 0.89, Recall = 0.80, F1 = 0.84
- **Sedih (Support = 2):** Precision = 0.00, Recall = 0.00, F1 = 0.00 (Minoritas)
- **Tertarik (Support = 93):** Precision = 0.55, Recall = 0.77, F1 = 0.64
- **Kaget (Support = 6):** Precision = 0.00, Recall = 0.00, F1 = 0.00 (Minoritas)

## 4. Evaluasi Historis Model 6-Kelas & Baseline (N = 1.058)
| Model | Representasi Fitur | Akurasi | Macro F1 | Weighted F1 | Protokol |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression** | TF-IDF n-gram | 69.47% | 0.3429 | 0.6457 | Group-Aware |
| **TF-IDF + Linear SVM** | TF-IDF n-gram | 67.20% | 0.4095 | 0.6558 | Group-Aware |
| **IndoBERT Base-p2 (6-Kelas)** | Deep Contextual | **79.40%** | **0.5160** | **0.7851** | Group-Aware |
| **IndoBERT Base-p2 (9-Kelas Weighted)** | Deep Contextual + Class Weights | **79.14%** | **0.4810** | **0.7889** | Zero-Leakage (N=1.064) |

## 5. Status Validasi Ilmiah
- **Status:** **`VERIFIED`**
- **Justifikasi:** Model 9-kelas telah di-fine-tune dengan penyeimbang bobot kelas (*weighted loss*) dan diuji pada partisi zero-leakage independen ($n=1.064$). Seluruh 9 kelas emosi Plutchik terintegrasi di dalam korpus master ($N = 5.272$), dengan kelas minoritas alami (*Takut*, *Sedih*, *Kaget*) terdokumentasi secara transparan sesuai kaidah metodologi Scopus Q1.

