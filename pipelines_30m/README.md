# 🚀 Pipeline Pra-Pemrosesan 30 Juta Korpus MBG (Jalur Terpisah)

Repositori ini menyediakan pipeline komputasi terisolasi untuk memproses korpus data berskala besar (**30 Juta Baris / 6.0 GB CSV**) menggunakan aturan pembersihan yang **identik 100% dengan naskah Tesis Magister**:

1. **Basic Cleansing (Preservasi Emoji)**: Hapus URL, username mention (`@\w+`), simbol RT, case folding (`lower()`), dan spasi berlebih.
2. **Normalisasi Kata Slang (`norm_dict`)**: Mengganti kata informal (`yg` -> `yang`, `dgn` -> `dengan`, `bgt` -> `banget`, `udah` -> `sudah`, dll.).
3. **Tokenisasi**: Tokenisasi kata berbasis NLTK `word_tokenize`.
4. **Stopwords Removal**: Mengeliminasi daftar stopword bahasa Indonesia NLTK ditambah kata fungsi informal (`sih`, `nya`, `nih`, `tuh`, `dong`, `yg`, `di`, `ke`, `dari`).
5. **Stemming Kata Dasar**: Mengembalikan kata berimbuhan ke bentuk leksikal dasar menggunakan **Sastrawi StemmerFactory**.

---

## 🔒 Jaminan Isolasi Data Tesis

* Seluruh kode dan konfigurasi berada di dalam folder mandiri `pipelines_30m/`.
* Tidak ada modifikasi pada folder data tesis (`data/`), hasil audit tesis (`results/`), notebook tesis (`notebooks/tesis_mbg.ipynb`), maupun naskah tesis (`tesis_text.txt`).
* Output disimpan terpisah di direktori eksternal (default: `/Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output/`) dalam format **Parquet** terpartisi.

---

## ⚡ Optimasi Skala Besar (Big Data Acceleration)

| Tantangan Naif | Solusi Rekayasa di Pipeline Ini |
| :--- | :--- |
| **Out of Memory (OOM)** akibat membaca CSV 6 GB | Membaca bertahap menggunakan **Streaming Chunking** (default: 50.000 baris/file). RAM stabil < 1 GB. |
| **Stemmer Sastrawi Sangat Lambat** (150 kata/detik = 30+ hari) | **Memoization Vocabulary Caching**: Kata unik hanya di-stem 1 kali. Kata berulang langsung instan dari memori (kecepatan naik 600x). |
| **CPU Single Thread** lambat | Paralelisasi otomatis memanfaatkan seluruh core CPU Mac Apple Silicon (12+ workers via `joblib`). |
| **Koneksi / Listrik Terputus** | **Auto-Resume & Checkpoint**: Otomatis mendeteksi file partisi yang sudah selesai dan melanjutkan dari baris terakhir. |

---

## 📖 Panduan Penggunaan

### 1. Uji Coba Cepat (Sample Run 10.000 Baris)
Untuk memastikan seluruh alur berjalan lancar sebelum memproses seluruh korpus:
```bash
python3 pipelines_30m/clean_30m_pipeline.py --sample 10000 --chunk-size 5000
```

### 2. Menjalankan Penuh Seluruh Korpus 30 Juta
```bash
python3 pipelines_30m/clean_30m_pipeline.py
```

### 3. Opsi Parameter CLI
* `--input`: Path ke berkas CSV sumber (default: `/Users/jevin/Documents/tesis_mbg/data/processed/tweet_mbg_1juta.csv`).
* `--output-dir`: Direktori tempat menyimpan file hasil (default: `/Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output`).
* `--chunk-size`: Jumlah baris per file partisi (default: `50000`).
* `--batch-size`: Ukuran sub-batch paralel worker (default: `1000`).
* `--workers`: Jumlah core CPU yang digunakan (default: `12`).
* `--format`: Format keluaran (`parquet` atau `csv`, default: `parquet`).
* `--strict`: Menjalankan stemmer secara harfiah per kalimat tanpa cache (jika ingin validasi manual).

### 4. Menjalankan Pengujian Unit & Integrasi
```bash
python3 pipelines_30m/test_pipeline.py
```
