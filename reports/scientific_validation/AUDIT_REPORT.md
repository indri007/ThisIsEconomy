# Audit Report: Scientific Validation & Integrity (Updated)
**Repository:** `indri007/ThisIsEconomy` (tesis_mbg)  
**Root Directory:** `/Users/jevin/Documents/tesis_mbg`  
**Git Remote:** `origin https://github.com/indri007/ThisIsEconomy.git`  
**Active Branch:** `fix/scientific-validation`  
**Base Commit:** `7c70273`  
**Date:** 2026-10-12  
**Role:** Senior ML Research Engineer & Scientific Integrity Auditor  

---

## 1. Executive Summary & Status Integritas
Audit forensik dan verifikasi komputasi langsung pada file aktual repositori telah selesai dijalankan. Evaluasi membuktikan adanya pemisahan tegas antara temuan ilmiah yang telah tervalidasi secara matematis versus klaim yang wajib ditandai `PROVISIONAL` atau `UNVERIFIED`:

1. **Benchmark 100 Sampel:** Terverifikasi memuat **49 cuitan tidak relevan (49.00%)**, terdiri dari spam voucher komersial Halodoc, homonim MBG ("Mas Bahlil Ganteng", "My Bini Gue", "My Boyfriend Gua", dsb), dan tweet bahasa asing. Sebanyak **26 cuitan terbukti relevan secara eksplisit**, dan **25 cuitan memerlukan klarifikasi manual (*Review Required*)**.
2. **Inter-Rater Reliability:** Ditandai **`NOT_VERIFIED`**. Template double-blind anonim (`DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1/2.csv`) telah dibuat dengan menyembunyikan prediksi model dan respon penilai lain. Tidak ada label sintetis yang dibuat.
3. **Reproduksi Metrik Model (Holdout N = 1.058):** Berhasil direproduksi secara eksak dari `results/FINAL_indobert_predictions.csv`:
   - **Akurasi:** 79.3951% (~79.40%)
   - **Macro F1:** 0.515985 (~0.5160)
   - **Weighted F1:** 0.785102 (~0.7851)
4. **Taksonomi 9 Emosi Plutchik:**
   - **Absen di Korpus (0 dari 5.263 cuitan):** *Bahagia (Joy)* dan *Kaget (Surprise)*.
   - **Ada di Korpus tapi Absen di Test Set:** *Takut (Fear)* (hanya 2 sampel di korpus, keduanya jatuh di partisi latih).
   - **Ada di Test Set tapi Gagal Diprediksi:** *Sedih (Sadness)* (support = 3, recall = 0.00, F1 = 0.00).
   - **Kelas Aktif Teruji Efektif:** *Jijik (F1 0.8444)*, *Percaya (F1 0.7528)*, *Netral (F1 0.8245)*, *Tertarik (F1 0.5409)*, *Marah (F1 0.1333)*.
5. **Verifikasi Klaim 30 Juta Baris:**
   - File `data/processed/tweet_mbg_30juta.csv` adalah *symbolic link* ke `tweet_mbg_1juta.csv`.
   - Ukuran fisik: 6.422.076.063 bytes (5.98 GB) dengan tepat 30.000.001 baris teks.
   - Karena korpus inferensi tesis utama adalah $N=5.263$, klaim pemrosesan 30 juta baris ditandai **`UNVERIFIED / BENCHMARK SIMULATION`** untuk analisis sentimen, agar tidak menimbulkan misrepresentasi di artikel ilmiah.
6. **Topologi Jaringan SNA Canonical:**
   - Terverifikasi matematis via NetworkX: $|V| = 971$ node, $|E| = 666$ edge unik, reciprocity $r = 0.012012$ (1.20%), Louvain Modularity $Q = 0.9837$ (342 komunitas terdeteksi).

---

## 2. Status Masalah per Kategori

| Komponen | Status Aktual | Keterangan & Tindakan |
| :--- | :---: | :--- |
| **Purifikasi Benchmark MBG** | **`FIXED`** | Filter inklusi/eksklusi berhasil membedakan 49 Irrelevant, 26 Relevant, 25 Review Required. |
| **Anotasi Independen & Reliabilitas** | **`PENDING_EXTERNAL_INPUT`** | Lembar kerja double-blind anonim siap diisi 2 pakar; status evaluator `NOT_VERIFIED`. |
| **Evaluasi Model 9 Emosi** | **`PROVISIONAL`** | Berhasil direproduksi (Acc 79.40%, Macro F1 0.5160, Weighted F1 0.7851) dengan transparansi limitasi minoritas. |
| **Klaim 30 Juta Baris** | **`BLOCKED (FLAGGED)`** | File 30 juta baris terverifikasi ada secara fisik (5.98 GB), namun status inferensi analitisnya ditandai unverified. |
| **Analisis Graf SNA** | **`FIXED`** | Seluruh metrik struktural NetworkX terverifikasi 100% konsisten. |
| **Test Suite Regresi** | **`FIXED`** | 6 unit test substantif berhasil dijalankan (`OK`). |
