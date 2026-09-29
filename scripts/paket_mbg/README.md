# Paket Perbaikan Paper MBG — Early Warning & Literatur Telegram

Isi paket:

```
paket_mbg/
├── 1_early_warning/
│   ├── ew_backtest.py          ← backtest sistem peringatan dini
│   ├── events_template.csv     ← template daftar kejadian resmi (isi sendiri)
│   └── buat_data_demo.py       ← data SINTETIS untuk mencoba skrip
└── 2_telegram_fix/
    ├── fix_telegram_pipeline.py        ← perbaikan pipeline literatur (siap jalan)
    └── patch_untuk_pipeline_asli.py    ← potongan kode pengganti untuk run_telegram_paper_pipeline.py
```

Kebutuhan: Python 3.10+, `pip install pandas numpy networkx matplotlib statsmodels`

---

## 1. Backtest Sistem Peringatan Dini

Tujuan: membuktikan (atau membantah) bahwa lonjakan rasa jijik/sarkasme **mendahului** kejadian resmi.
Hasilnya menggantikan klaim "jendela diagnostik 24–48 jam" di Bagian 5.3.2 yang saat ini belum berbukti.

### Langkah

1. **Coba dulu dengan data demo**
   ```bash
   cd 1_early_warning
   python buat_data_demo.py
   python ew_backtest.py --tweets demo_tweets.csv --events demo_events.csv --edges demo_edges.csv --out hasil_demo
   ```
2. **Siapkan data asli**
   - `tweets_classified.csv`: kolom `created_at, emotion, sarcasm` — hasil klasifikasi IndoBERT
     **setelah** set pengujian dilabel ulang (poin 1 perbaikan). Label boleh Inggris atau Indonesia.
   - `edges.csv` (opsional): `source, target, created_at` → mengaktifkan Q dan R per periode pada DPPTI.
   - `events.csv`: salin dari `events_template.csv`. Isi **waktu pertama kali kejadian diberitakan resmi**
     (ANTARA, Kompas, rilis BGN, dsb.) lengkap dengan `source_url`. Target minimal 10–15 kejadian.
3. **Jalankan**
   ```bash
   python ew_backtest.py --tweets tweets_classified.csv --events events.csv --edges edges.csv --out hasil
   ```
   Opsi penting: `--freq 12h` (resolusi 12 jam), `--threshold 1.5` (ambang z), `--window 72` (jendela jam).
   **Tetapkan parameter sebelum melihat hasil** dan laporkan apa adanya — jangan mencoba-coba ambang sampai hasilnya bagus.

### Membaca hasil (`RINGKASAN.md`)

| Metrik | Arti |
|---|---|
| Recall | % kejadian yang didahului alarm |
| Precision | % alarm yang benar-benar diikuti kejadian |
| Median lead time | berapa jam alarm mendahului kejadian |
| Uji permutasi (p) | apakah recall lebih baik daripada tanggal kejadian acak; **p < 0,05 syarat klaim prediktif** |
| Granger / korelasi silang | bukti tambahan arah waktu sinyal → kejadian |

Catatan: dengan ±37 cuitan/hari, sinyal harian masih tipis. Jika banyak periode bertanda volume rendah,
gunakan `--freq 1D` (bukan 12h) atau perbesar korpus.

---

## 2. Perbaikan Pipeline Literatur Telegram

Memperbaiki error pada `pipeline_errors.log`:

| Error | Penyebab | Perbaikan |
|---|---|---|
| `KeyError: 'publication_year'` di `cleaning()` | kolom tahun tidak ada / beda nama | tahun dicari dari kolom kandidat, lalu dari Crossref; yang kosong dipisah ke `unknown_year.csv` |
| `int('UNVERIFIED')` di `generate_review()` | nilai tahun berupa teks | fungsi `safe_year()` — tidak pernah crash |
| `int('UNVERIFIED')` di `generate_summary()` | sama | sama, plus skor non-angka ditampilkan "—" |
| Scopus/Q1 semua UNVERIFIED | tidak ada sumber verifikasi | pencocokan ISSN ke file SCImago (berbasis Scopus) |

### Langkah

1. Unduh file SCImago terbaru: https://www.scimagojr.com/journalrank.php → **Download data** (CSV).
2. Jalankan:
   ```bash
   cd 2_telegram_fix
   python fix_telegram_pipeline.py --master /Users/jevin/Documents/tesis_mbg/backend/telegram_literature_output/telegram_literature_master.csv \
       --out hasil_fix --crossref --email EMAIL_ANDA --scimago scimagojr_2025.csv
   ```
   Crossref butuh internet; hasil disimpan di `crossref_cache.json` agar tidak memanggil ulang.
3. Periksa `telegram_literature_summary.txt`, lalu `unknown_year.csv` (cek manual jika masih ada).
4. Perbarui angka di Bagian 3.7 dan Tabel 6 naskah sesuai hasil baru, dan hapus kalimat
   "filter tahun belum diterapkan" jika sudah berhasil.

Jika ingin memperbaiki pipeline asli, ikuti `patch_untuk_pipeline_asli.py` (4 langkah salin-tempel).

### Catatan integritas

- Kuartil hanya diisi dari SCImago (atau Scopus API). Yang tidak cocok tetap `UNVERIFIED`.
- SCImago memakai kuartil **terbaik** lintas kategori; sebutkan tahun SCImago yang dipakai di naskah.
- Prosiding (IEEE, Springer LNCS) sering tidak punya kuartil — itu normal, bukan error.
