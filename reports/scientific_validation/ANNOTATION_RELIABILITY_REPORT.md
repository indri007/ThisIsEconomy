# Annotation Reliability Report

## 1. Audit Nilai Kesepakatan Historis
- **Klaim Sebelumnya:**
  - Persentase Kesepakatan: 95.00%
  - Cohen's Kappa ($\kappa$): 0.9135 / 0.925
  - Tri-Rater Krippendorff's Alpha ($\alpha$): 0.8447 / 0.9252
- **Temuan Forensik:**
  - Kolom `annotator_2_notes` pada 95 entri bertuliskan teks template identik: *"Sepakat penuh dengan Penilai 1 (Konsensus)"*.
  - Ini membuktikan bahwa Penilai 2 **melihat** hasil penilaian Penilai 1 saat proses berlangsung, sehingga menghasilkan kesepakatan semu (*pseudo-agreement*) akibat efek jangkar (*anchoring bias*).
  - Dalam standar telaah sejawat Scopus Q1 (seperti JCMC Oxford), prosedur ini tidak dapat diterima sebagai reliabilitas antar-penilai independen (*inter-rater reliability*).

## 2. Status Reliabilitas Terkini
- **Status Operasional:** **`NOT_VERIFIED`** (Pending Independent Human Annotation).
- Dilarang keras mempertahankan angka 0.925 / 0.9135 di manuskrip sebagai bukti independen terverifikasi.

## 3. Infrastruktur Double-Blind yang Telah Disiapkan
Untuk memulihkan integritas metodologis, pipeline berikut telah dibuat dan aktif:
1. **Template Double-Blind Tanpa Kisi-Kisi Label:**
   - `data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1.csv`
   - `data/annotation/double_blind/DOUBLE_BLIND_TEMPLATE_ANNOTATOR_2.csv`
2. **Karakteristik Template:**
   - Kolom prediksi model IndoBERT dihapus 100%.
   - Label penilai lain disembunyikan secara penuh.
   - Kolom yang tersedia: `item_id`, `tweet_text`, `assigned_emotion`, `confidence_1to5`, `annotation_notes`, `annotator_pseudonym`, `timestamp_iso`.
3. **Pedoman Operasional:**
   - Tersedia di `data/annotation/double_blind/PEDOMAN_ANOTASI_9_EMOSI.md`.

## 4. Prosedur Perhitungan Ulang
Setelah kedua file template diisi oleh dua penilai manusia independen:
Jalankan skrip:
```bash
/Users/jevin/Documents/tesis_mbg/.venv/bin/python scripts/setup_double_blind_annotation.py
```
Statistik Cohen's Kappa dan Krippendorff's Alpha akan dihitung otomatis dari *raw labels* sebelum adjudikasi.
