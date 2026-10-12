# Reproducibility & Computational Pipeline Report

## 1. Audit Keterlacakan Skala Data
- **Klaim Sebelumnya:** Pemrosesan 30 juta baris cuitan.
- **Temuan Fisik di Lingkungan Penyimpanan:**
  - File `data/processed/tweet_mbg_30juta.csv` (ukuran 6.422.076.063 bytes) secara fisik terkonfigurasi sebagai *symbolic link* ke `data/processed/tweet_mbg_1juta.csv`.
  - Output partisi Parquet pada `data/processed/clean_30m_output/` hanya memuat 2 partisi parsial (`clean_part_00001.parquet` dan `clean_30m_part_00002.parquet`).
  - **Kesimpulan Auditor:** Klaim pemrosesan 30 juta baris belum memiliki log eksekusi komputasi batch yang lengkap dan independen. Status klaim ini wajib diturunkan menjadi **`UNVERIFIED / BENCHMARK SIMULATION`** di manuskrip, dan tidak boleh dinyatakan sebagai data empiris yang telah selesai diproses penuh.

## 2. Dataset Manifest & Checksum (SHA-256)
Dataset inti yang digunakan dalam analisis telah dicatat dalam `reports/scientific_validation/DATASET_MANIFEST.json`:
- `data/network_edges.csv`: `a8a5cf475ade0734fbc07f80887b204039938789fc27d05e10bfdaffc6a86622` (693 baris)
- `data/results/indobert_9_emosi_fixed.csv`: `cc9432ccb3c26b13abd9d14380152521f16dbd7e72fd28241cb9291ba55fcec6` (5.263 cuitan)
- `results/FINAL_indobert_metrics.csv`: `a6bd4f086aa66cc935c49f8f0411bef28b483a6426cbae456ba4755cacccd5a7`
- `results/emotion_test_group_split.csv`: `e8bf8199cea6c98cc8b173fb454be804ef64c02ba520586bda63f52c8f7e6c06` (1.058 baris test)

## 3. Lingkungan Eksekusi & Ketergantungan
- **Sistem Operasi:** macOS Darwin 24.3.0
- **Python Runtime:** Python 3.11.15 (`.venv`)
- **Pustaka Utama:**
  - PyTorch: `torch` 2.2+
  - Transformers: `transformers` 4.38+
  - Network Analysis: `networkx` 3.2+
  - Scikit-Learn: `scikit-learn` 1.4+
  - Data Processing: `pandas` 2.2+, `pyarrow`

## 4. Penghapusan Hardcoded Paths
Sebanyak 44 skrip yang sebelumnya memuat path lokal absolut `/Users/jevin/` telah diidentifikasi. Skrip pipeline inti (`purify_mbg_benchmark.py`, `setup_double_blind_annotation.py`, `evaluate.py`, dan modul testing) telah direkayasa ulang menggunakan resolusi direktori relatif dinamis berbasis `os.path`.
