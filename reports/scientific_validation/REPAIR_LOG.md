# Repair Log: Scientific Validation & Integrity Pipeline

**Date:** 2026-10-12  
**Target Branch:** `fix/scientific-validation`  

---

### Step 1: Baseline Security & Repository Isolation
- Memeriksa Git status repositori `tesis_mbg`.
- Membuat branch baru `fix/scientific-validation` untuk mengisolasi semua pekerjaan perbaikan dari `main`.
- Mengonfirmasi bahwa data mentah asli tidak ditimpa atau dihapus.

### Step 2: Purifikasi Korpus Benchmark 100 Sampel
- Mengidentifikasi 49 dari 100 cuitan di `multi_annotator_batch_100_GOLD.csv` yang terkontaminasi spam iklan voucher belanja (Halodoc), bahasa asing (Turki, Portugis), dan homonim slang MBG non-program ("Mas Bahlil Ganteng", "My Bini Gue").
- Menulis dan mengeksekusi skrip `scripts/purify_mbg_benchmark.py` dengan kriteria inklusi dan eksklusi eksplisit.
- Menghasilkan artefak bersih `data/annotation/purified_benchmark_batch_100_audit.csv`.

### Step 3: Implementasi Protokol Double-Blind Independen
- Menulis skrip `scripts/setup_double_blind_annotation.py` untuk memisahkan template anotasi ke dua file terpisah tanpa menyertakan label penilai lain maupun prediksi model:
  - `data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1.csv`
  - `data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_2.csv`
- Menyusun pedoman operasional lengkap `data/annotation/double_blind/PEDOMAN_ANOTASI_9_EMOSI.md`.
- Menandai status reliabilitas kesepakatan penilai sebagai `NOT_VERIFIED` hingga anotasi manusia independen selesai diisi.

### Step 4: Verifikasi Matematis Graf SNA Canonical
- Melakukan verifikasi ulang graf interaksi terarah dari `data/network_edges.csv`.
- Memvalidasi secara eksak:
  - Nodes $\|V\| = 971$
  - Edges $\|E\| = 666$
  - Reciprocity $r = 0.01201$ (1.20%)
  - In-degree tertinggi: `@prabowo` (15, out-degree 0)
  - Out-degree tertinggi: `@grok` (42)

### Step 5: Dataset Manifest & Checksum SHA-256
- Menghasilkan `reports/scientific_validation/DATASET_MANIFEST.json` berisi ukuran file, jumlah baris, dan hash SHA-256 untuk seluruh dataset inti guna menjamin reproduksibilitas ilmiah.

### Step 6: Automated Testing Suite
- Menulis dan menjalankan unit test di `tests/test_scientific_validation.py`.
- Seluruh 5 tes validasi (Benchmark Contamination, Zero Leakage Split, SNA Graph Metrics, Double Blind Isolation, Manifest Integrity) lulus 100% (`OK`).

### Step 7: Dokumentasi & Laporan Audit
- Menyusun 8 dokumen laporan lengkap di direktori `reports/scientific_validation/`.
