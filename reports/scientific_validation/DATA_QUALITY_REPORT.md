# Data Quality & Benchmark Purification Report

## 1. Provenance Benchmark Awal
- **File Sumber:** `data/multi_annotator_batch_100_GOLD.csv` (berasal dari batch audit n = 100).
- **Tujuan Awal:** Digunakan sebagai "Gold Standard" multi-penilai untuk membuktikan keandalan klasifikasi model IndoBERT.

## 2. Temuan Audit Kualitas Data
Dari 100 baris cuitan yang diaudit menggunakan kriteria inklusi & eksklusi eksplisit (`scripts/purify_mbg_benchmark.py`):
- **RELEVANT:** 26 entri (26.00%) — Secara eksplisit membahas Program MBG, BGN, SPPG, menu makanan, susu, keracunan, atau anggaran.
- **REVIEW_REQUIRED:** 25 entri (25.00%) — Memuat akronim "MBG" dalam konteks ambigu yang memerlukan tinjauan pakar manusia.
- **IRRELEVANT:** 49 entri (49.00%) — **Spam, homonim non-kebijakan, dan bahasa asing yang salah terjaring:**
  1. *Spam Promosi Komersial:* Voucher diskon Halodoc (misal `RES-0010`, `RES-0012` dsb) terjaring hanya karena memuat kata "gizi".
  2. *Homonim MBG Fandom / Slang:* Akronim "MBG" digunakan warganet untuk "Mas Bahlil Ganteng", "My Bini Gue", "My Boyfriend Gua", "Goyang MBG", anime "Dorohedoro", kpop group "Boynextdoor".
  3. *Bahasa Asing:* Tweet berbahasa Turki (`RES-0008`: *"Bana gurban ol dedim olmadın..."*) dan Portugis (`RES-0083`: *"VAI FICAR PARECENDO UM MILK SHAKE..."*).

## 3. Bahaya Ilmiah Jika Tidak Dipurifikasi
Memberi label emosi "Jijik" atau "Percaya" pada tweet spam voucher Halodoc atau lagu lelucon "Mas Bahlil Ganteng" merusak validitas konstruk penelitian komunikasi kebijakan publik. Evaluasi model yang menyertakan data ini tidak mengukur pemahaman model terhadap resistensi publik MBG, melainkan menangkap artefak kebisingan data (*data noise artifact*).

## 4. Hasil Tindakan Kurasi
1. Seluruh 49 entri tidak relevan telah ditandai `IRRELEVANT` pada `data/annotation/purified_benchmark_batch_100_audit.csv`.
2. Dibuat antrean tinjauan 51 kandidat cuitan (`RELEVANT` + `REVIEW_REQUIRED`) ke dalam template double-blind independen.
3. Rekomendasi kurasi korpus: Penambahan sampel baru yang terverifikasi membahas entitas MBG diperlukan untuk mencapai $N \ge 200$ yang memadai secara statistik.
