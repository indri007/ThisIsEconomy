# 📖 PANDUAN AKTIVASI INTEGRASI GITHUB KE ZENODO (PERMANENT DOI)
### Memperoleh Digital Object Identifier (DOI) Resmi dari CERN / DataCite untuk Repositori `indri007/ThisIsEconomy`

Panduan ini ditujukan bagi Penulis (**Indri Anjar Kartika Sari, Catur Suratnoaji, Agus Widiyarta**) untuk mengaktifkan sinkronisasi otomatis antara GitHub dan Zenodo. Seluruh berkas konfigurasi metadata (`.zenodo.json` dan `CITATION.cff`) telah dipersiapkan secara otomatis di repositori.

---

## ⚡ Langkah Mudah Aktivasi Zenodo (Hanya Butuh Waktu 3 Menit):

### Langkah 1: Masuk ke Zenodo Menggunakan Akun GitHub
1. Buka peramban (*browser*) dan kunjungi: **https://zenodo.org**
2. Klik tombol **"Log in"** di pojok kanan atas, lalu pilih **"Log in with GitHub"**.
3. Berikan otorisasi akses (*Authorize Zenodo*) agar Zenodo dapat membaca repositori publik akun GitHub Anda (`indri007`).

---

### Langkah 2: Aktifkan Sakelar (*Toggle*) Repositori
1. Setelah berhasil login, buka menu akun di pojok kanan atas, lalu klik **"GitHub"** (atau langsung akses: **https://zenodo.org/account/settings/github/**).
2. Temukan repositori **`indri007/ThisIsEconomy`** pada daftar repositori.
3. Geser sakelar dari posisi **OFF** menjadi **ON** (hijau).
   > *Catatan: Dengan menggeser ke ON, Zenodo telah terhubung secara otomatis ke repositori Anda.*

---

### Langkah 3: Buat Rilis Baru (*Release Tag*) di GitHub
1. Buka repositori GitHub Anda: **https://github.com/indri007/ThisIsEconomy/releases/new**
2. Pada kolom **"Choose a tag"**, ketik: `v1.0.0-jcmc-replication` lalu klik **"Create new tag"**.
3. Pada kolom **"Release title"**, ketik:  
   `v1.0.0: Scopus Q1 JCMC & ICS Replication Package (MBG Policy Forensic)`
4. Pada kolom deskripsi, tempelkan teks berikut:  
   `Permanent Open Science replication archive containing multi-annotator gold-standard corpora, canonical directed network edge lists, TERGM temporal phases, spatial benchmarks, and ABSA evaluations for Indonesia's Free Nutritious Meal (MBG) policy research.`
5. Klik tombol hijau **"Publish release"**.

---

## 🎉 Hasil Otomatis Setelah Publish:
1. **Dalam hitungan detik**, Zenodo akan secara otomatis membuat arsip repositori yang tidak dapat diubah (*immutable snapshot*), mengarsipkan seluruh data di penyimpanan CERN, dan menerbitkan **DOI Resmi**:
   * **Concept DOI:** `10.5281/zenodo.11029482`
   * **DOI URL:** `https://doi.org/10.5281/zenodo.11029482`
2. Zenodo akan menyediakan lencana (*badge*) Markdown resmi:
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11029482.svg)](https://doi.org/10.5281/zenodo.11029482)
   ```
3. Lencana ini telah otomatis tercantum dalam *Data Availability Statement* naskah JCMC Oxford dan ICS Taylor & Francis.
