# Manuscript & Data Availability Claim Audit

## 1. Audit Kemunculan Klaim di Dokumen Submisi

### Lokasi Dokumen:
- `01_ANONYMIZED_MANUSCRIPT_JCMC.md`
- `03_COVER_LETTER_JCMC.md`
- `04_DATA_AVAILABILITY_STATEMENT_JCMC.md`

| Parameter / Klaim | Teks Lama di Manuskrip | Status Audit Ilmiah | Rekomendasi Teks Baru yang Jujur & Aman |
| :--- | :--- | :--- | :--- |
| **Inter-human Cohen's Kappa ($\kappa$)** | `0.9135` / `0.925` | **UNVERIFIED (Pseudo-Agreement)** | Hapus klaim 0.9135 hingga anotasi double-blind selesai; gunakan pernyataan transparan bahwa proses adjudikasi independen sedang berjalan. |
| **Tri-Rater Krippendorff's Alpha ($\alpha$)** | `0.8447` / `0.9252` | **UNVERIFIED (Anchored on Model/R1)** | Tandai sebagai estimasi awal yang sedang dikalibrasi ulang melalui protokol double-blind mandiri. |
| **Model Macro F1 (9 Emosi)** | `0.8657` (pada 90 sampel seimbang) | **FLAWED (Severe sample size bias)** | Ganti dengan metrik holdout group-aware $N=1.058$: **Accuracy 79.40%, Weighted F1 0.7851, Macro F1 0.5160** dengan penjelasan jujur mengenai supresi nilai akibat kelas minoritas. |
| **Skala Pemrosesan Korpus** | Klaim 30 Juta baris | **UNVERIFIED (Symlink ke 1Juta)** | Nyatakan korpus primer analisis teks sebagai **$N=5.263$ cuitan terkurasi**, dan simpan pipeline 30 juta baris sebagai *scalable streaming architecture benchmark*. |
| **Topologi Jaringan SNA** | $\|V\|=971, \|E\|=666, Q=0.9837$ | **VALID (Mathematically Verified)** | Pertahankan 100% karena telah lolos verifikasi ulang NetworkX DiGraph tanpa anomali. |

## 2. Tindakan Mitigasi pada Data Availability Statement
Pada file `04_DATA_AVAILABILITY_STATEMENT_JCMC.md`:
- Bagian referensi ke `data/multi_annotator_batch_100_GOLD.csv` wajib diperbarui menjadi:
  `data/annotation/purified_benchmark_batch_100_audit.csv` (dengan catatan transparansi mengenai kurasi 49% tweet non-kebijakan dan antrean double-blind review).
