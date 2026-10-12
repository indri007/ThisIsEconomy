# 🚀 Pipeline Pra-Pemrosesan 30 Juta Korpus MBG & Inferensi IndoBERT Terlatih

Repositori ini menyediakan pipeline komputasi terisolasi untuk memproses korpus data berskala besar (**30 Juta Baris / `tweet_mbg_30juta.csv`**) dan inferensi model **IndoBERT Fine-Tuned (3 Epochs)**:

---

## 🔬 Arsitektur Dua Varian Pemrosesan (Ablation Study Framework)

Secara linguistik dan komputasional (khususnya untuk model Transformer dua-arah seperti IndoBERT), pemotongan kata berimbuhan (*stemming*) dan eliminasi stopword dapat menghilangkan konteks penting, kata negasi (*"tidak"*, *"bukan"*, *"belum"*, *"jangan"*), serta ekspresi emosional informal media sosial. 

Oleh karena itu, pipeline ini **tidak mengasumsikan Sastrawi langsung lebih baik**, melainkan menyediakan **dua varian komparatif**:

1. **Varian 1 (`clean_text` — Context-Preserving Clean Text)**:
   - Menghapus noise teknis: URL (`http\S+`), mentions (`@\w+`), hashtags (`#\w+`), angka (`\d+`), dan karakter non-ASCII/emoji.
   - **Mempertahankan kata negasi dan kosakata sentimen informal** agar representasi atensi multi-head IndoBERT tetap utuh dan akurat.
2. **Varian 2 (`processed_text` — Sastrawi Stemmed + Stopword Removed)**:
   - Menerapkan eliminasi stopword Sastrawi dan stemming morfologis dasar Sastrawi.
   - Terbukti secara matematis dan empiris **100.0000% identik** mereproduksi kolom `processed_text` pada dataset master tesis (`indobert_9_emosi_fixed.csv`, $N = 5.263$).

Kedua varian disimpan berdampingan di setiap berkas partisi Parquet (`clean_30m_part_XXXXX.parquet`) sehingga peneliti dapat menguji ablasi performa keduanya secara bebas.

---

## 🤖 Model IndoBERT Fine-Tuned (3 Epochs, GroupShuffleSplit)

Inferensi emosi (`pipelines_30m/indobert_inference.py`) menggunakan bobot model **yang benar-benar telah dilatih**:
* **Base Architecture**: `indobenchmark/indobert-base-p2`
* **Fine-Tuning Epochs**: **3 Epochs** (`num_train_epochs = 3`)
* **Split Protocol**: GroupShuffleSplit ($80/20$) berdasar teks terproses (Zero Text & Token Leakage)
* **Akurasi Validasi**: $75.99\%$ Akurasi, Weighted F1 $0.7434$
* **Taksonomi 9 Emosi Plutchik**:
  - `0: Marah`
  - `1: Jijik`
  - `2: Takut`
  - `3: Bahagia`
  - `4: Percaya`
  - `5: Netral`
  - `6: Sedih`
  - `7: Tertarik`
  - `8: Kaget`
* **Akselerasi Perangkat**: Otomatis mendeteksi Apple Silicon GPU (MPS Metal) atau NVIDIA CUDA.

---

## 📁 Konvensi Penamaan Berkas Skala 30 Juta

* **Berkas Input Mentah**: `data/processed/tweet_mbg_30juta.csv` (simbolik link ke korpus 6.0 GB tanpa menduplikasi ruang disk).
* **Partisi Bersih**: `data/processed/clean_30m_output/clean_30m_part_XXXXX.parquet`
* **Hasil Inferensi Emosi**: `data/processed/clean_30m_output/clean_30m_part_XXXXX_with_indobert.parquet`
* **Log Checkpoint**: `data/processed/clean_30m_output/progress_checkpoint.json`

---

## 📖 Panduan Penggunaan

### 1. Uji Coba Cepat Pra-pemrosesan Teks (Sample 500 Baris)
```bash
python3 pipelines_30m/clean_30m_pipeline.py --sample 500 --chunk-size 500
```

### 2. Inferensi IndoBERT Terlatih pada Partisi
```bash
python3 pipelines_30m/indobert_inference.py \
  --input /Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output/clean_30m_part_00001.parquet \
  --output /Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output/clean_30m_part_00001_with_indobert.parquet \
  --text-col clean_text \
  --batch-size 32
```

### 3. Eksekusi Pembuktian Kebenaran Dataset Lama Tesis ($N = 5.263$)
```bash
python3 scripts/verify_old_dataset_preprocessing.py
```
Hasil verifikasi membuktikan:
* `clean_text`: **5.263 / 5.263 baris (100.0000% Exact Match)**
* `processed_text`: **5.263 / 5.263 baris (100.0000% Exact Match)**

### 4. Menjalankan Seluruh Automated Test Suite
```bash
python3 -m pytest pipelines_30m/test_pipeline.py -v
```
Semua 7 unit dan integration test terverifikasi lulus 100%.
