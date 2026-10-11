# 📝 LOG PERUBAHAN RISET & DOKUMENTASI TEKNIS
### *Research Changelog, Code Modifications, and Scientific Audit Trail*

**Cabang Git (*Branch*):** `fix/scientific-technical-validation`  
**Basis Cabang (*Base Branch*):** `main`  
**Tanggal Eksekusi:** 11 Oktober 2026  
**Auditor / Perevisi:** Senior ML Engineer, Computational Communication Researcher, & Reviewer Scopus Q1

---

## 1. IKHTISAR PERUBAHAN (*EXECUTIVE SUMMARY*)

Perubahan dilakukan dengan mematuhi secara ketat 8 Aturan Wajib:
- **Nol Penghapusan Data/Fitur:** Tidak ada dataset, checkpoint, atau fitur aplikasi yang dihapus.
- **Nol Halusinasi Metrik:** Seluruh metrik diturunkan langsung dari eksekusi kode terhadap data riil.
- **Branch Terisolasi:** Perbaikan dikerjakan pada branch `fix/scientific-technical-validation`, tidak langsung di-push ke `main`.
- **Pengujian Regresi Penuh:** Rangkaian automated test suite meningkat dari 83 menjadi **85 tes**, dengan tingkat kelulusan **100%**.

---

## 2. MODIFIKASI FILE SUMBER KODE (*CODE MODIFICATIONS*)

### 2.1 `dashboard/app.py`
* **Lokasi Baris:** Baris 20–35
* **Kategori:** *Bugfix / Asynchronous Event Loop Isolation*
* **Rasional Ilmiah & Teknis:**  
  Sebelumnya terdapat monkeypatch tanpa syarat pada `sniffio.current_async_library()` yang selalu mengembalikan `"asyncio"` ketika fungsi standar melempar `AsyncLibraryNotFoundError`. Hal ini menyebabkan AnyIO blocking portal pada `starlette.testclient.TestClient` mendeteksi adanya event loop aktif palsu dalam synchronous test thread, menggagalkan 7 pengujian backend API.
* **Perubahan Kode:**  
  Menambahkan pengecekan eksplisit `asyncio.get_running_loop() is not None` sebelum mengembalikan `"asyncio"`. Jika tidak ada loop yang berjalan, exception dilempar secara normal sehingga Starlette TestClient dapat menginisialisasi AnyIO thread portal tanpa error.

---

### 2.2 `backend/services/sna_service.py`
* **Lokasi Baris:** Baris 18–38
* **Kategori:** *Code Integrity / Penghapusan Hardcoded Research Metrics*
* **Rasional Ilmiah & Teknis:**  
  Fungsi `get_sna_summary()` sebelumnya memuat konstanta statis `communities = 342` dan `modularity = 0.9837` yang di-hardcode. Hal ini melanggar prinsip transparansi komputasi di mana layanan API harus mencerminkan hasil perhitungan riil.
* **Perubahan Kode:**  
  Mengganti nilai hardcoded dengan pembacaan dinamis:
  - Jumlah komunitas dihitung dari `df_nodes['Community'].nunique()` pada `mbg_network_nodes_final.csv`.
  - Skor modularitas dimuat secara terversi dari `results/macro_topology_metrics.json`.

---

### 2.3 `backend/services/community_service.py`
* **Lokasi Baris:** Baris 14–33
* **Kategori:** *Code Integrity / Penghapusan Hardcoded Research Metrics*
* **Rasional Ilmiah & Teknis:**  
  Fungsi `get_communities_summary()` sebelumnya memuat konstanta statis `total_communities = 342`.
* **Perubahan Kode:**  
  Menghitung `total_communities = len(community_counts)` secara dinamis dari tabel simpul yang dimuat, serta mengambil nilai modularitas dari artefak JSON makro-topologi.

---

### 2.4 `scripts/rename_emotions.py`
* **Lokasi Baris:** Baris 20–35
* **Kategori:** *Documentation Integrity & Theoretical Guardrail*
* **Rasional Ilmiah & Teknis:**  
  Menambahkan blok dokumentasi peringatan ilmiah tingkat Scopus Q1 mengenai batasan translasi ad-hoc `love -> Percaya` dan `shame -> Tertarik`. Menegaskan bahwa dalam publikasi formal, label-label ini tidak boleh diklaim sebagai ekuivalen teoritis murni tanpa pengungkapan keterbatasan leksikal silver standard.

---

## 3. BERKAS BARU YANG DIBANGUN (*NEW FILES CREATED*)

### 3.1 Skrip Komputasi & Pengujian Otomatis
1. **`scripts/run_sna_sensitivity_analysis.py`:**  
   Skrip komputasi mandiri untuk mengevaluasi ketahanan topologi graf terhadap variasi definisi tepi (berarah vs tak berarah vs tanpa self-loops vs ambang bobot $w \ge 2$), sapuan parameter resolusi Louvain ($\gamma \in [0.5, 2.0]$), dan uji stabilitas stokastik modularitas pada 10 random seed.
2. **`tests/test_sna_sensitivity_analysis.py`:**  
   Unit test otomatis untuk memvalidasi keberadaan, struktur data, dan kepatuhan rentang matematis seluruh artefak uji sensitivitas SNA.

### 3.2 Berkas Data & Artefak Hasil Komputasi
1. **`results/sna_sensitivity_analysis.json`:**  
   Artefak JSON terstruktur memuat hasil dekomposisi sensitivitas definisi tepi, sapuan parameter resolusi Louvain, dan ringkasan stabilitas multi-seed.
2. **`results/sna_sensitivity_analysis.csv`:**  
   Tabel perbandingan variasi definisi sisi (Nodes, Edges, Components, Density, Reciprocity).
3. **`results/sna_resolution_sweep.csv`:**  
   Tabel hasil sapuan parameter resolusi $\gamma$ terhadap nilai modularitas $Q$ dan jumlah klaster komunitas.

### 3.3 Berkas Dokumentasi Ilmiah Mandatori
1. **`AUDIT_REPORT.md`:** Laporan temuan komprehensif, tingkat risiko (Critical/High/Medium/Low), bukti file/baris kode, dan solusi.
2. **`DATA_DICTIONARY.md`:** Spesifikasi skema kolom, tipe data, sumber data, dan analisis taksonomi 9 emosi Plutchik vs empiris.
3. **`REPRODUCIBILITY.md`:** Panduan replikasi end-to-end dari penyiapan dependensi hingga eksekusi regresi otomatis.
4. **`MODEL_EVALUATION_REPORT.md`:** Rekonsiliasi tiga nilai Macro-F1, laporan evaluasi resmi Protokol v2, perbandingan baseline linier, diseksi kelas minoritas, dan pengungkapan model 9-emosi.
5. **`SNA_VALIDATION_REPORT.md`:** Definisi graf formal, dekomposisi matematis modularitas $Q = 0.9837$, pembuktian *atomized grievance archipelago*, hasil uji sensitivitas, dan tipologi peran aktor.
6. **`TEST_REPORT.md`:** Laporan eksekusi 85 unit test otomatis dengan tingkat kelulusan 100%, investigasi kegagalan masa lalu, dan diagnostik lingkungan.
7. **`CHANGELOG_RESEARCH.md`:** Log lengkap perubahan file dan justifikasi ilmiah (dokumen ini).
8. **`RESEARCH_GAP_AND_NOVELTY.md`:** Analisis kontribusi keilmuan, formalisasi 5 proposisi teoretis *Phygital Gap*, pemisahan TRL software vs sains, dan agenda riset doktoral S3.
