# PEER-REVIEW METHODOLOGICAL RECONCILIATION REPORT
## Tanggapan Metodologis & Rekonsiliasi Saintifik atas Evaluasi Model, Label Data, Partisi Latih-Uji, dan Dinamika Longitudinal

**Status Repositori:** `https://github.com/indri007/ThisIsEconomy`  
**Protokol Evaluasi:** Protocol v2 Group-Aware Zero-Leakage Split (`GroupShuffleSplit`, `seed=42`)  
**Tanggal Rekonsiliasi:** 11 Oktober 2026  
**Peran Auditor:** Senior ML Engineer, Computational Communication Researcher, & Scopus Q1 Reviewer  

---

### RINGKASAN EKSEKUTIF REKONSILIASI

Laporan ini menyajikan pembuktian matematis, penyesuaian kode sumber (*source code refactoring*), dan rekonsiliasi dokumentasi untuk menjawab secara tuntas 4 butir telaah kritis (*peer-review critique*):

| No | Butir Telaah Kritis | Temuan Akar Masalah (*Root Cause*) | Resolusi & Bukti Empiris | Status |
|:---:|:---|:---|:---|:---:|
| **A** | **Model sembilan emosi belum terbukti sebagai model sembilan kelas valid** | Taksonomi awal dirancang untuk 9 emosi Plutchik, tetapi korpus empiris $N = 5.263$ hanya memuat **6 kelas aktif**. Kelas *Joy* dan *Surprise* bernilai 0 sampel, dan *Fear* hanya 2 sampel. | Seluruh klaim divalidasi ulang: dideklarasikan secara eksplisit sebagai **model 6-kelas aktif dengan ketimpangan kelas alami**, bukan model 9-kelas penuh. Metrik resmi dilaporkan jujur: Macro-F1 = **0,4535**, Weighted-F1 = **0,7434**, Akurasi = **75,99%**. | **RESOLVED** ✅ |
| **B** | **README menyebut hasil sebagai "ground truth"** | Label korpus $N = 5.263$ diekstraksi melalui pipeline otomatis (Gemini LLM + aturan leksikal). Istilah *ground truth* berisiko menyesatkan jika diartikan sebagai anotasi manusia. | Terminologi diseragamkan menjadi **silver-standard reference labels**. Istilah *human gold standard / ground truth* secara ketat dibatasi hanya untuk sub-sampel validasi pakar manusia ($n = 100$ cuitan teranotasi ganda, $\kappa = 0{,}9135$). | **RESOLVED** ✅ |
| **C** | **Protokol pemisahan data belum konsisten (`train_test_split` vs `GroupShuffleSplit`)** | Skrip `scripts/train.py` dan `scripts/train_indobert.py` masih memakai `sklearn.model_selection.train_test_split` acak, bertolak belakang dengan protokol zero-leakage `GroupShuffleSplit` di dokumen audit. | Seluruh skrip pelatihan dan evaluasi (`scripts/train.py`, `scripts/train_indobert.py`, `scripts/evaluate.py`) telah di-refactor menggunakan **`GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)`** berbasis `processed_text` dengan asersi programatik **Zero Lexical Overlap** (`overlap = 0`). | **RESOLVED** ✅ |
| **D** | **Angka longitudinal perlu direkonsiliasi ($9.365$ vs $9.360$)** | Tabel ringkasan longitudinal menuliskan akumulasi Cinta (*Love*) sebesar 167 ($1{,}78\%$). Penjumlahan baris bulanan: $9.189 + 167 + 9 = 9.365$, menimbulkan selisih 5 data terhadap total cuitan $9.360$. | Penjumlahan riil kolom bulanan Cinta: $0+0+5+16+93+3+2+2+39+2 = \mathbf{162}$ cuitan ($1{,}73\%$). Rekonsiliasi matematis: **$9.189 + 162 + 9 = 9.360$** ($98{,}17\% + 1{,}73\% + 0{,}10\% = 100{,}00\%$). Selisih 5 data terbukti sebagai salah ketik pada baris ringkasan dan kini telah diperbaiki di seluruh berkas. | **RESOLVED** ✅ |

---

### BUTIR A: PEMBUKTIAN EMPIRIS DISTRIBUSI EMOSI & METRIK 6-KELAS AKTIF

#### 1. Realitas Data Empiris ($N = 5.263$)
Secara teoretis, penelitian mengadopsi taksonomi 9 emosi Plutchik (`anger`, `disgust`, `fear`, `joy`, `love`, `neutral`, `sadness`, `shame`, `surprise`). Namun, hasil audit terhadap dataset berlabel `data/results/indobert_9_emosi_fixed.csv` membuktikan distribusi frekuensi aktual sebagai berikut:

```
Distribusi Empiris Kelas Emosi:
  1. Jijik (Disgust)         : 2.960 cuitan (56,24%) -> Kelas Mayoritas Dominan
  2. Percaya (Trust/Love)    : 1.073 cuitan (20,39%) -> Kelas Sekunder
  3. Netral (Neutral)        :   649 cuitan (12,33%) -> Kelas Faktual
  4. Tertarik (Anticipation) :   505 cuitan ( 9,60%) -> Kelas Penantian
  5. Marah (Anger)           :    55 cuitan ( 1,05%) -> Kelas Minoritas
  6. Sedih (Sadness)         :    19 cuitan ( 0,36%) -> Kelas Minoritas
  7. Takut (Fear)            :     2 cuitan ( 0,04%) -> Ekstrem Minoritas (0 di test set)
  8. Bahagia (Joy)           :     0 cuitan ( 0,00%) -> Tidak ada sampel
  9. Kaget (Surprise)        :     0 cuitan ( 0,00%) -> Tidak ada sampel
---------------------------------------------------------------------------------
TOTAL                       : 5.263 cuitan (100,00%)
```

#### 2. Keterbatasan Saintifik yang Harus Dinyatakan Terbuka
* **Bukan Model 9-Kelas Tervalidasi Penuh:** Karena *Joy* ($N=0$) dan *Surprise* ($N=0$) tidak memiliki sampel dalam korpus training/test, model **tidak dapat dan tidak boleh diklaim telah memvalidasi klasifikasi 9-kelas**.
* **Model 6-Kelas Aktif Berkeadaan Nyata:** Pada partisi uji *zero-leakage holdout* ($n = 1.058$), hanya terdapat 6 kelas yang terevaluasi:
  $$\text{Macro-F1} = \frac{0{,}8202 + 0{,}6977 + 0{,}8032 + 0{,}4000 + 0{,}0000 + 0{,}0000}{6} = \frac{2{,}7211}{6} = \mathbf{0{,}4535}$$
  - Weighted-F1: **0,7434** (tertimbang pada populasi kelas dominan)
  - Akurasi Keseluruhan: **75,99%** (804 cuitan tepat dari 1.058 cuitan)
* **Koreksi Angka Historis di README:** Nilai usang `Macro F1 = 0.8122` (yang berasal dari rata-rata 3 kelas mayoritas pada draf awal) dan `Recall 96,92%` (yang berasal dari model rusak checkpoint-792 yang mengalami *collapse* ke kelas Disgust) telah **dihapus dan digantikan secara konsisten** dengan metrik Protocol v2 di atas.

---

### BUTIR B: KLARIFIKASI STATUS LABEL DATA (SILVER-STANDARD VS HUMAN GOLD-STANDARD)

#### 1. Definisi Epistemologis Tata Kelola Data
Dalam kepustakaan computational linguistics dan NLP (misal: Ratner et al., *Snorkel*, 2017; Koto et al., *IndoLEM*, 2020), data pelatihan dan evaluasi dibedakan secara tegas ke dalam tier berikut:

1. **Tier 1 — Raw Scraped Data:** Teks mentah media sosial hasil crawling/streaming ($N = 9.310$).
2. **Tier 2 — Silver-Standard Reference Labels:** Anotasi yang dihasilkan melalui pipeline terotomatisasi (Gemini LLM prompt-engineering yang dipadukan dengan aturan ekspresi reguler dan leksikon sentimen). Dataset $N = 5.263$ (`indobert_9_emosi_fixed.csv`) dan holdout $n = 1.058$ berada pada **Tier 2 ini**.
3. **Tier 3 — Human-Adjudicated Gold Standard:** Anotasi manual independen oleh pakar manusia (*domain experts*) dengan protokol double-blind dan konsensus adjudikasi. Di dalam repositori ini, Tier 3 diwujudkan dalam berkas `data/annotation/researcher_batch_100_FILLED.csv` ($n = 100$ cuitan).

#### 2. Tindakan Penyelarasan Dokumen
* Seluruh rujukan dalam `README.md`, `dashboard/modules/views_bab1.py`, dan `dashboard/modules/views_bab4.py` yang sebelumnya berpotensi menafsirkan label $N = 5.263$ sebagai *ground truth* telah diperjelas menjadi:  
  **`silver-standard reference labels`** (*label acuan perak berbasis penyulingan semantik terotomatisasi*).
* Istilah **`ground truth` / `human gold standard`** secara ketat dicadangkan hanya untuk sub-sampel validasi manusia ($n = 100$) yang mencatatkan Cohen's Kappa $\kappa = 0{,}9135$ dan Tri-Rater Fleiss' Kappa $\kappa = 0{,}8442$.

---

### BUTIR C: KONSISTENSI PROTOKOL PEMISAHAN DATA (ELIMINASI `train_test_split`)

#### 1. Akar Masalah Ketidakkonsistenan Kode
Sebelumnya, terdapat dikotomi berbahaya dalam repositori:
* Dokumen audit (`MODEL_EVALUATION_REPORT.md` dan `REPRODUCIBILITY.md`) menetapkan protokol evaluasi yang aman terhadap duplikasi viral retweet via `GroupShuffleSplit`.
* Namun, skrip `scripts/train.py`, `scripts/train_indobert.py`, dan `scripts/evaluate.py` masih mengimpor dan memanggil:
  ```python
  from sklearn.model_selection import train_test_split
  train_texts, val_texts, train_labels, val_labels = train_test_split(..., test_size=0.2, random_state=42)
  ```
  Hal ini menyebabkan audit eksternal menemukan bahwa jika pengguna menjalankan skrip pelatihan bawaan, akan terjadi kebocoran 533 teks duplikat antara data latih dan data uji.

#### 2. Refactoring Kode Menjadi Zero-Leakage Group-Aware
Seluruh skrip pelatihan dan evaluasi telah diperbarui secara seragam:

```python
# Refactored in scripts/train.py, scripts/train_indobert.py, and scripts/evaluate.py:
from sklearn.model_selection import GroupShuffleSplit

# GroupShuffleSplit memastikan bahwa semua kemunculan processed_text yang identik
# (retweet, copypasta, atau kutipan viral) hanya masuk ke SATU partisi (train atau test).
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, val_idx = next(gss.split(df, groups=df['processed_text']))
train_df = df.iloc[train_idx]
val_df = df.iloc[val_idx]

train_texts = train_df['processed_text'].tolist()
val_texts = val_df['processed_text'].tolist()

# Asersi programatik wajib: Zero Text Overlap
overlap = set(train_texts).intersection(set(val_texts))
assert len(overlap) == 0, f"Critical Data Leakage: Terdeteksi {len(overlap)} teks duplikat!"
print(f"✓ Zero Leakage Terverifikasi: overlap = {len(overlap)} teks")
```

#### 3. Verifikasi Programatik
Menjalankan skrip yang telah diperbarui mengonfirmasi output terminal:
```bash
✓ Zero Leakage Terverifikasi: overlap = 0 teks (Train: 4205, Val/Test: 1058)
```
Dengan demikian, integritas pemisahan data telah 100% konsisten antara dokumentasi ilmiah dan kode implementasi.

---

### BUTIR D: REKONSILIASI MATEMATIS ANGKA KORPUS LONGITUDINAL ($N = 9.360$)

#### 1. Audit Rincian Bulanan (Januari – 10 Oktober 2026)
Tabel 1 pada Bab IV dan `README.md` memuat dekomposisi longitudinal bulanan sebagai berikut:

| Periode / Bulan | Total Cuitan | 🤢 Jijik (*Disgust*) | ❤️ Cinta (*Love*) | 😐 Netral (*Neutral*) | Proporsi Jijik (%) | Catatan Peristiwa |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Januari 2026** | 42 | 42 | 0 | 0 | 100,00% | Peluncuran percontohan awal |
| **Februari 2026** | 55 | 55 | 0 | 0 | 100,00% | Perluasan uji coba regional |
| **Maret 2026** | 189 | 184 | 5 | 0 | 97,35% | Penyesuaian jadwal Ramadan |
| **April 2026** | 515 | 499 | 16 | 0 | 96,89% | Kontroversi nampan plastik ompreng |
| **Mei 2026 (Puncak I)** | **3.157** | **3.060** | **93** | **4** | **96,93%** | Suspensi 4.581 SPPG oleh BGN |
| **Juni 2026** | 228 | 225 | 3 | 0 | 98,68% | Libur sekolah & dengar pendapat DPR |
| **Juli 2026** | 184 | 182 | 2 | 0 | 98,91% | Tahun ajaran baru sekolah |
| **Agustus 2026** | 209 | 205 | 2 | 2 | 98,09% | Nota Keuangan RAPBN 2026 (Rp 268T) |
| **September 2026 (Puncak II)** | **4.661** | **4.619** | **39** | **3** | **99,10%** | Insiden keracunan massal siswa nasional |
| **Oktober 2026 (s.d. 10 Okt)** | 120 | 118 | 2 | 0 | 98,33% | Pengawasan aktif bot Telegram EWS |

#### 2. Pembuktian Penjumlahan Kolom
Mari kita jumlahkan nilai setiap kolom secara eksak:

1. **Kolom Total Cuitan:**
   $$42 + 55 + 189 + 515 + 3.157 + 228 + 184 + 209 + 4.661 + 120 = \mathbf{9.360}$$
2. **Kolom Jijik (*Disgust*):**
   $$42 + 55 + 184 + 499 + 3.060 + 225 + 182 + 205 + 4.619 + 118 = \mathbf{9.189} \quad (98{,}17\%)$$
3. **Kolom Netral (*Neutral*):**
   $$0 + 0 + 0 + 0 + 4 + 0 + 0 + 2 + 3 + 0 = \mathbf{9} \quad (0{,}10\%)$$
4. **Kolom Cinta (*Love*):**
   $$0 + 0 + 5 + 16 + 93 + 3 + 2 + 2 + 39 + 2 = \mathbf{162} \quad (1{,}73\%)$$

#### 3. Rekonsiliasi Terhadap Selisih 5 Data
* **Sebelum Rekonsiliasi:** Baris ringkasan di draf sebelumnya mencantumkan angka Cinta sebesar **167** ($1{,}78\%$). Akibatnya:
  $$9.189 + 167 + 9 = 9.365 \quad (\text{selisih } +5 \text{ terhadap total } 9.360)$$
* **Sesudah Rekonsiliasi:** Angka pada baris ringkasan dikoreksi menjadi nilai penjumlahan kolom yang sebenarnya, yaitu **162** ($1{,}73\%$). Dengan demikian:
  $$9.189 + 162 + 9 = \mathbf{9.360} \quad (98{,}17\% + 1{,}73\% + 0{,}10\% = 100{,}00\%)$$
  Persamaan ini seimbang sempurna dengan **selisih 0 data (zero discrepancy)**.

Koreksi ini telah disinkronkan ke seluruh file terkait:
* `README.md` (Tabel 1 dan Tabel 2 baris ke-8)
* `dashboard/modules/views_bab1.py` (DataFrame `df_monthly_timeline` & `df_taxonomy_9`)
* `dashboard/modules/views_bab4.py` (DataFrame `df_tax_b4`)
* `manuscript/JURNAL_MBG_SCOPUS_Q1_LATEST_2026.md` (Table 7)
* `manuscript/ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.md` (Table 5)
* `journal_paper_mbg_sna.md` (Table 7)

---

### STATUS VERIFIKASI AKHIR

1. **Python Syntax Compilation:** Seluruh berkas Python lulus uji kompilasi sintaks `python3 -m py_compile` (0 error).
2. **Master Automated Test Suite:** `85 passed` dari 85 unit test pada `pytest` (100% kelulusan).
3. **Git Branching Integrity:** Seluruh perubahan dikerjakan pada branch perbaikan terpisah `fix/peer-review-reconciliation` sesuai kaidah software engineering dan scientific computing.
