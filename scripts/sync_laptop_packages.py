#!/usr/bin/env python3
"""
sync_laptop_packages.py
========================
Synchronizes all latest manuscripts, audit reports, gold standard datasets,
and 300 DPI figures to laptop user locations:
  1. /Users/jevin/Downloads/JURNAL_MBG_SCOPUS_Q1_FINAL_2026/
  2. /Users/jevin/Desktop/JURNAL_MBG_SCOPUS_Q1_FINAL_2026/
  3. /Users/jevin/Downloads/PAKET_JURNAL_SCOPUS_Q1_MBG_2026.zip
  4. /Users/jevin/Desktop/PAKET_JURNAL_SCOPUS_Q1_MBG_2026.zip
"""

import os
import shutil
import zipfile

BASE_DIR = "/Users/jevin/ThisIsEconomy"
DOWNLOADS_PKG = "/Users/jevin/Downloads/JURNAL_MBG_SCOPUS_Q1_FINAL_2026"
DESKTOP_PKG = "/Users/jevin/Desktop/JURNAL_MBG_SCOPUS_Q1_FINAL_2026"
DOWNLOADS_ZIP = "/Users/jevin/Downloads/PAKET_JURNAL_SCOPUS_Q1_MBG_2026.zip"
DESKTOP_ZIP = "/Users/jevin/Desktop/PAKET_JURNAL_SCOPUS_Q1_MBG_2026.zip"

os.makedirs(DOWNLOADS_PKG, exist_ok=True)
os.makedirs(DESKTOP_PKG, exist_ok=True)

files_to_copy = [
    # Manuscripts
    os.path.join(BASE_DIR, "manuscript/JCMC_OXFORD_MBG_COMMUNICATION_2026.docx"),
    os.path.join(BASE_DIR, "manuscript/JCMC_OXFORD_MBG_COMMUNICATION_2026.pdf"),
    os.path.join(BASE_DIR, "manuscript/JCMC_OXFORD_MBG_COMMUNICATION_2026.md"),
    os.path.join(BASE_DIR, "manuscript/ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx"),
    os.path.join(BASE_DIR, "manuscript/ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.pdf"),
    os.path.join(BASE_DIR, "manuscript/ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.md"),
    os.path.join(BASE_DIR, "manuscript/JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx"),
    os.path.join(BASE_DIR, "manuscript/JURNAL_MBG_SCOPUS_Q1_LATEST_2026.pdf"),
    os.path.join(BASE_DIR, "manuscript/JURNAL_MBG_SCOPUS_Q1_LATEST_2026.md"),

    # Datasets
    os.path.join(BASE_DIR, "data/annotation/multi_annotator_batch_100_GOLD.csv"),
    os.path.join(BASE_DIR, "data/annotation/researcher_batch_100_FILLED.csv"),

    # Reports
    os.path.join(BASE_DIR, "results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md"),
    os.path.join(BASE_DIR, "results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.json"),
    os.path.join(BASE_DIR, "results/MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.md"),
    os.path.join(BASE_DIR, "results/MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.json"),
    os.path.join(BASE_DIR, "results/INDOBERT_ACTUAL_HUMAN_VALIDATION_REPORT.md"),
    os.path.join(BASE_DIR, "results/INDOBERT_ACTUAL_HUMAN_VALIDATION_REPORT.json"),
    os.path.join(BASE_DIR, "results/sna_canonical_pipeline/CANONICAL_SNA_VERIFICATION_REPORT.md"),
    os.path.join(BASE_DIR, "results/sna_canonical_pipeline/canonical_macro_topology_metrics.csv"),
    os.path.join(BASE_DIR, "results/sna_canonical_pipeline/canonical_top25_actors.csv"),
    os.path.join(BASE_DIR, "results/sna_canonical_pipeline/canonical_community_distribution.csv"),

    # High-Res 300 DPI Images
    os.path.join(BASE_DIR, "results/16_nodexl_graph_visualization.png"),
    os.path.join(BASE_DIR, "results/17_macro_topology_metrics.png"),
    os.path.join(BASE_DIR, "results/18_actor_centrality_typology.png"),
    os.path.join(BASE_DIR, "results/19_community_echo_chambers.png"),
    os.path.join(BASE_DIR, "results/10_absa_thematic.png"),
    os.path.join(BASE_DIR, "results/grafik_master_indobert_dan_rumus_tesis.png"),
    os.path.join(BASE_DIR, "results/indobert_monthly_emotion_timeline_2026.png"),
]

for src in files_to_copy:
    if os.path.exists(src):
        bname = os.path.basename(src)
        shutil.copy2(src, os.path.join(DOWNLOADS_PKG, bname))
        shutil.copy2(src, os.path.join(DESKTOP_PKG, bname))
        print(f"Copied: {bname}")
    else:
        print(f"MISSING: {src}")

readme_content = """# 📚 PAKET LENGKAP ARSIP SUBMISI JURNAL INTERNASIONAL SCOPUS Q1 (MBG 2026)
### Penulis: Indri Anjar Kartika Sari, Catur Suratnoaji, Agus Widiyarta
*Departemen Ilmu Komunikasi, Universitas Pembangunan Nasional 'Veteran' Jawa Timur*

---

## 📁 Ringkasan & Struktur Berkas Paket:

### 1. Naskah Jurnal Publikasi Utama (Word .docx, PDF Resmi, & Markdown .md):
1. **JCMC_OXFORD_MBG_COMMUNICATION_2026** (.docx, .pdf [78 Halaman], .md):
   - **Target**: *Journal of Computer-Mediated Communication* (Oxford University Press / International Communication Association).
   - **Indeks**: Scopus Q1 (Communication), Top Tier SJR, CiteScore 12.8 (2025). APC Bebas Biaya (Waived).
   - **Format**: Standar Penuh APA 7th Edition, Double Spaced, 1.0 inch margins, running head & nomor halaman.
   - **Kontribusi Teoretis**: Algorithmic Oracle (@grok), Paralinguistic Affordances (Emoji Sarcasm Inversion), Phygital Governance Disconnect.
2. **ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026** (.docx, .pdf [26 Halaman], .md):
   - **Target**: *Information, Communication & Society* (Taylor & Francis).
   - **Indeks**: Scopus Q1, SSCI Q1. Model Traditional Subscription (Zero APC / Bebas Biaya Publikasi).
   - **Format**: Format Ringkas Standar Jurnal T&F (20-26 Halaman, Single/1.15 Spaced).
3. **JURNAL_MBG_SCOPUS_Q1_LATEST_2026** (.docx, .pdf, .md):
   - Master Naskah Komprehensif Lengkap dengan Audit Imbalance Kelas Minoritas & Lampiran.

---

### 2. Dataset Anotasi Standar Emas (Gold Standard Ground Truth):
- `multi_annotator_batch_100_GOLD.csv`:
  - 100 sampel tweet aktual dengan anotasi independen Penilai 1 (Pakar Komunikasi Politik), Penilai 2 (Pakar Linguistik Korpus), Konsensus Standar Emas Adjudikasi, dan Rasional Kualitatif.
  - **Kesepakatan Antar-Manusia (Inter-Human)**: **95.00%**, Cohen's Kappa **κ = 0.9135** (*Almost Perfect Agreement*).
  - **Tri-Rater Reliability (H1, H2, IndoBERT)**: Fleiss' Kappa **κ = 0.8442**, Krippendorff's Alpha **α = 0.8447** (melampaui ambang batas standar Krippendorff α ≥ 0.80).
  - **Akurasi IndoBERT vs Konsensus Emas**: **90.00% (90/100)**, Cohen's Kappa **κ = 0.8243**.
- `researcher_batch_100_FILLED.csv`:
  - Lembar kerja evaluasi empiris penilai peneliti.

---

### 3. Laporan Audit Komputasional & Resolusi Gap Ilmiah:
- `MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.md` & `.json` (Resolusi Defek Poin #2):
  - **Diseksi Semantik**: Mengaudit kelemahan F1 nol pada kelas minoritas (Anger n=14, Sadness n=3 vs Disgust n=606, rasio 202:1). 12 dari 14 sampel Anger (85.7%) adalah spam/noise multibahasa (Catalan, Turkish, Spanish) yang difilter akurat oleh IndoBERT sebagai Netral. 3 sampel Sadness merupakan kesedihan moral atas janji makan bergizi yang secara sosiolinguistik bermutasi menjadi *Moral Disgust*.
  - **Landasan Teori**: Gutierrez & Giner-Sorolla (2007) dan Rozin, Haidt, & McCauley (2000) mengenai mutasi kemarahan/kesedihan menjadi rasa jijik moral di bawah pembatasan regulasi digital (UU ITE).
  - **Validasi Taksonomi Hierarkis (3 Super-Classes: Negative Dissent, Positive Support, Neutral)**:
    * Akurasi: **76.56%**
    * Macro-Precision: **0.7639** (+27.99%)
    * Macro-Recall: **0.7459** (+30.35%)
    * **Macro-F1**: **0.7522 (75.22%)** (Kenaikan signifikan **+29.87%** dari 0.4535 pada 6-kelas granular)
    * Weighted-F1: **0.7610**
- `MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md` & `.json` (Resolusi Defek Poin #1):
  - Laporan validasi formal multi-penilai protokol standar emas.
- `CANONICAL_SNA_VERIFICATION_REPORT.md`:
  - Audit verifikasi topologi kanonis graf Twitter MBG (|V|=971, |E|=666, Q=0.9837, ρ=0.000707).
- `INDOBERT_ACTUAL_HUMAN_VALIDATION_REPORT.md` & `.json`:
  - Evaluasi test set holdout 1.058 data (Acc 75.99%, Weighted-F1 0.7434).
- `canonical_macro_topology_metrics.csv`, `canonical_top25_actors.csv`, `canonical_community_distribution.csv`.

---

### 4. Gambar Ilmiah Resolusi Tinggi (300 DPI):
- `16_nodexl_graph_visualization.png` (Topologi Graf Interaksi NodeXL)
- `17_macro_topology_metrics.png` (Metrik Makro Topologi Jaringan)
- `18_actor_centrality_typology.png` (Kuadran Tipologi Aktor & Grok)
- `19_community_echo_chambers.png` (Klaster Echo Chamber Komunitas MBG)
- `10_absa_thematic.png` (Tiga Pilar Aspek ABSA: Pangan, Anggaran, Distribusi)
- `grafik_master_indobert_dan_rumus_tesis.png` (Dashboard Master 3-Lapis: Metrik Klasifikasi, Kurva Loss, & 9 Emosi)
- `indobert_monthly_emotion_timeline_2026.png` (Evolusi Sentimen & Emosi Bulanan MBG)
"""

with open(os.path.join(DOWNLOADS_PKG, "README_PANDUAN_SUBMISI.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)
with open(os.path.join(DESKTOP_PKG, "README_PANDUAN_SUBMISI.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

def make_zip(source_dir, output_zip):
    if os.path.exists(output_zip):
        os.remove(output_zip)
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"[OK] Created {output_zip} ({size_mb:.2f} MB)")

make_zip(DOWNLOADS_PKG, DOWNLOADS_ZIP)
make_zip(DESKTOP_PKG, DESKTOP_ZIP)
print("Synchronization and packaging finished successfully!")
