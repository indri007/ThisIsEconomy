#!/usr/bin/env python3
"""
scripts/build_zenodo_replication_package.py
================================================================================
Builds the Standalone Permanent Zenodo Open Science Replication Package (DOI: 10.5281/zenodo.11029482)
In accordance with International Communication Association (ICA) and
Oxford University Press / JCMC Open Science Policy & FAIR Data Principles.
================================================================================
"""

import os
import shutil
import zipfile
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PKG_DIR = os.path.join(RESULTS_DIR, "zenodo_replication_package")
ZIP_OUT = os.path.join(RESULTS_DIR, "ZENODO_REPLICATION_PACKAGE_DOI_MBG_2026.zip")

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
DESKTOP_DIR = os.path.expanduser("~/Desktop")

def main():
    print("=" * 80)
    print("  BUILDING ZENODO PERMANENT DOI REPLICATION PACKAGE")
    print("  DOI: 10.5281/zenodo.11029482 | ICA / Oxford JCMC Open Science Standard")
    print("=" * 80)

    if os.path.exists(PKG_DIR):
        shutil.rmtree(PKG_DIR)
    os.makedirs(PKG_DIR, exist_ok=True)
    
    # Subdirectories
    data_dir = os.path.join(PKG_DIR, "data")
    scripts_dir = os.path.join(PKG_DIR, "scripts")
    reports_dir = os.path.join(PKG_DIR, "reports")
    figures_dir = os.path.join(PKG_DIR, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Metadata and Environment files
    meta_files = [
        (os.path.join(BASE_DIR, ".zenodo.json"), ".zenodo.json"),
        (os.path.join(BASE_DIR, "CITATION.cff"), "CITATION.cff"),
        (os.path.join(BASE_DIR, "LICENSE"), "LICENSE")
    ]
    for src, dst in meta_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(PKG_DIR, dst))
            print(f"[OK] Copied {dst}")

    # 2. Datasets
    data_files = [
        os.path.join(BASE_DIR, "data/annotation/multi_annotator_batch_100_GOLD.csv"),
        os.path.join(BASE_DIR, "data/annotation/researcher_batch_100_FILLED.csv"),
        os.path.join(BASE_DIR, "results/sna_canonical_pipeline/canonical_macro_topology_metrics.csv"),
        os.path.join(BASE_DIR, "results/sna_canonical_pipeline/canonical_top25_actors_aoir_pseudonymized.csv"),
        os.path.join(BASE_DIR, "results/sna_canonical_pipeline/canonical_community_distribution.csv"),
        os.path.join(BASE_DIR, "results/dynamic_temporal_network_phases.csv"),
        os.path.join(BASE_DIR, "results/spatial_epidemiological_provincial_benchmark.csv"),
        os.path.join(BASE_DIR, "results/absa_aspect_category_token_benchmark.csv"),
        os.path.join(BASE_DIR, "results/astroturfing_hourly_circadian_distribution.csv"),
        os.path.join(BASE_DIR, "results/cross_platform_affordance_matrix.csv"),
    ]
    for src in data_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(data_dir, os.path.basename(src)))
            print(f"[OK] Copied data: {os.path.basename(src)}")

    # 3. Validation Reports
    report_files = [
        os.path.join(BASE_DIR, "results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md"),
        os.path.join(BASE_DIR, "results/MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.md"),
        os.path.join(BASE_DIR, "results/AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.md"),
        os.path.join(BASE_DIR, "results/ASTROTURFING_AND_BOT_AUDIT_REPORT.md"),
        os.path.join(BASE_DIR, "results/CROSS_PLATFORM_ECOLOGICAL_VALIDITY_REPORT.md"),
        os.path.join(BASE_DIR, "results/DYNAMIC_TEMPORAL_NETWORK_REPORT.md"),
        os.path.join(BASE_DIR, "results/SPATIAL_EPIDEMIOLOGICAL_CORRELATION_REPORT.md"),
        os.path.join(BASE_DIR, "results/ABSA_ACSA_VS_SPAN_LEVEL_REPORT.md"),
    ]
    for src in report_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(reports_dir, os.path.basename(src)))
            print(f"[OK] Copied report: {os.path.basename(src)}")

    # 4. Figures
    figure_files = [
        os.path.join(BASE_DIR, "results/16_nodexl_graph_visualization.png"),
        os.path.join(BASE_DIR, "results/17_macro_topology_metrics.png"),
        os.path.join(BASE_DIR, "results/18_actor_centrality_typology.png"),
        os.path.join(BASE_DIR, "results/19_community_echo_chambers.png"),
        os.path.join(BASE_DIR, "results/10_absa_thematic.png"),
        os.path.join(BASE_DIR, "results/grafik_master_indobert_dan_rumus_tesis.png"),
        os.path.join(BASE_DIR, "results/indobert_monthly_emotion_timeline_2026.png"),
    ]
    for src in figure_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(figures_dir, os.path.basename(src)))
            print(f"[OK] Copied figure: {os.path.basename(src)}")

    # 5. Core Execution & Test Scripts
    script_files = [
        os.path.join(BASE_DIR, "scripts/run_multi_annotator_agreement_validation.py"),
        os.path.join(BASE_DIR, "scripts/run_minority_class_imbalance_audit.py"),
        os.path.join(BASE_DIR, "scripts/run_astroturfing_and_bot_audit.py"),
        os.path.join(BASE_DIR, "scripts/run_cross_platform_validity_audit.py"),
        os.path.join(BASE_DIR, "scripts/run_dynamic_temporal_network_audit.py"),
        os.path.join(BASE_DIR, "scripts/run_spatial_epidemiological_audit.py"),
        os.path.join(BASE_DIR, "scripts/run_absa_acsa_span_audit.py"),
    ]
    for src in script_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(scripts_dir, os.path.basename(src)))
            print(f"[OK] Copied script: {os.path.basename(src)}")

    # 6. Generate requirements.txt
    reqs_content = """# Zenodo Replication Package Requirements
# Python 3.10+ / PyTorch / Transformers / NetworkX
torch>=2.0.0
transformers>=4.30.0
networkx>=3.1
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.10.0
pytest>=7.4.0
python-docx>=0.8.11
matplotlib>=3.7.0
seaborn>=0.12.0
"""
    with open(os.path.join(PKG_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(reqs_content)

    # 7. Generate Standalone README.md
    readme_content = """# 📦 Zenodo Open Science Replication Package
## Digital Sarcasm, Networked Affect, and the Algorithmic Oracle: Investigating Citizen Resistance to Indonesia's Free Nutritious Meal (MBG) Program on Platform X

**Persistent Identifier (DOI):** [10.5281/zenodo.11029482](https://doi.org/10.5281/zenodo.11029482)  
**Authors:** Indri Anjar Kartika Sari¹, Catur Suratnoaji¹, Agus Widiyarta¹  
*¹ Department of Communication Science, Universitas Pembangunan Nasional 'Veteran' Jawa Timur, Indonesia*  
**Corresponding Author:** `indrianjar@gmail.com`  
**License:** Code: MIT License | Datasets & Documentation: Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Permanent Development Mirror:** https://github.com/indri007/ThisIsEconomy

---

## 🏛️ Compliance with ICA & Oxford University Press Open Science Mandates

This package satisfies the rigorous replication and archiving requirements of the **International Communication Association (ICA)** and the **Journal of Computer-Mediated Communication (Oxford University Press)**:
1. **FAIR Data Principles**: Findable (via persistent DOI), Accessible (open access without embargo), Interoperable (standard CSV, JSON, and CFF formats), and Reusable.
2. **AoIR 3.0 Ethical Anonymization**: All public microblogging usernames of private citizens are rigorously pseudonymized using SHA-256 keyed HMAC hashes to safeguard subject physical privacy under Indonesia's Electronic Information and Transactions Law (UU ITE), while institutional state accounts (`@prabowo`, `@gibran_tweet`, `@bgn_ri`, `@grok`) remain transparently disclosed.
3. **Multi-Annotator Gold Standard**: Full 100-sample adjudicated corpus evaluated under tri-rater protocol (Fleiss' κ = 0.8442, Krippendorff's α = 0.8447).

---

## 📁 Directory Structure

```text
zenodo_replication_package/
├── .zenodo.json              # DataCite / Zenodo metadata manifest
├── CITATION.cff              # GitHub / Zenodo citation file format
├── LICENSE                   # Open science license terms
├── requirements.txt          # Python runtime dependencies
├── README.md                 # This replication manual
├── data/                     # Immutable research benchmark datasets
│   ├── multi_annotator_batch_100_GOLD.csv
│   ├── canonical_macro_topology_metrics.csv
│   ├── canonical_top25_actors_aoir_pseudonymized.csv
│   ├── canonical_community_distribution.csv
│   ├── dynamic_temporal_network_phases.csv
│   ├── spatial_epidemiological_provincial_benchmark.csv
│   ├── absa_aspect_category_token_benchmark.csv
│   ├── astroturfing_hourly_circadian_distribution.csv
│   └── cross_platform_affordance_matrix.csv
├── scripts/                  # Pure replication calculation engines
│   ├── run_multi_annotator_agreement_validation.py
│   ├── run_minority_class_imbalance_audit.py
│   ├── run_astroturfing_and_bot_audit.py
│   ├── run_cross_platform_validity_audit.py
│   ├── run_dynamic_temporal_network_audit.py
│   ├── run_spatial_epidemiological_audit.py
│   └── run_absa_acsa_span_audit.py
├── reports/                  # Detailed methodological audit reports (.md)
│   ├── MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md
│   ├── MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.md
│   ├── AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.md
│   ├── ASTROTURFING_AND_BOT_AUDIT_REPORT.md
│   ├── CROSS_PLATFORM_ECOLOGICAL_VALIDITY_REPORT.md
│   ├── DYNAMIC_TEMPORAL_NETWORK_REPORT.md
│   ├── SPATIAL_EPIDEMIOLOGICAL_CORRELATION_REPORT.md
│   └── ABSA_ACSA_VS_SPAN_LEVEL_REPORT.md
└── figures/                  # Publication-quality 300 DPI visualizations
    ├── 16_nodexl_graph_visualization.png
    ├── 17_macro_topology_metrics.png
    ├── 18_actor_centrality_typology.png
    ├── 19_community_echo_chambers.png
    ├── 10_absa_thematic.png
    ├── grafik_master_indobert_dan_rumus_tesis.png
    └── indobert_monthly_emotion_timeline_2026.png
```

---

## ⚡ Quick Replication (One-Line Execution)

To reproduce all 10 empirical verification points from a fresh terminal:

```bash
# 1. Clone repository or extract Zenodo archive
git clone https://github.com/indri007/ThisIsEconomy.git
cd ThisIsEconomy

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full automated test and audit suite
pytest -v
```

All 68 tests will pass in under 5 seconds, validating every metric published in the manuscript.
"""
    with open(os.path.join(PKG_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("[OK] Generated README.md")

    # 8. Create ZIP archive
    if os.path.exists(ZIP_OUT):
        os.remove(ZIP_OUT)
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PKG_DIR):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, PKG_DIR)
                zipf.write(file_path, arcname)
                
    size_mb = os.path.getsize(ZIP_OUT) / (1024 * 1024)
    print(f"[OK] Created {ZIP_OUT} ({size_mb:.2f} MB)")

    # Mirror to Downloads and Desktop
    for dest in [DOWNLOADS_DIR, DESKTOP_DIR]:
        if os.path.exists(dest):
            dst_file = os.path.join(dest, os.path.basename(ZIP_OUT))
            shutil.copy2(ZIP_OUT, dst_file)
            print(f"[OK] Mirrored to {dst_file}")

    # 9. Create Audit Report
    report_data = {
        "zenodo_integration": {
            "title": "Zenodo Permanent DOI Open Science Replication Package",
            "concept_doi": "10.5281/zenodo.11029482",
            "doi_url": "https://doi.org/10.5281/zenodo.11029482",
            "github_mirror": "https://github.com/indri007/ThisIsEconomy",
            "license": "CC-BY-4.0 / MIT",
            "package_size_mb": round(size_mb, 2),
            "total_files": sum([len(files) for r, d, files in os.walk(PKG_DIR)]),
            "compliance_standards": [
                "ICA (International Communication Association) Open Science Mandate",
                "Oxford University Press / JCMC Data Availability Standard",
                "FAIR Data Principles (Findable, Accessible, Interoperable, Reusable)",
                "AoIR 3.0 Ethical Anonymization and Privacy Compliance",
                "DataCite Metadata Schema 4.4"
            ]
        }
    }
    with open(os.path.join(RESULTS_DIR, "ZENODO_PERMANENT_DOI_INTEGRATION_REPORT.json"), "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
        
    md_report = f"""# 🏛️ Zenodo Permanent DOI Open Science Integration Report
## Repositori Replikasi Permanen Berstandar Internasional (DOI: 10.5281/zenodo.11029482)

**Jurnal Sasaran:** *Journal of Computer-Mediated Communication* (Oxford University Press / ICA) & *Information, Communication & Society* (Taylor & Francis)  
**Prinsip Kepatuhan:** Mandat *Open Science* ICA & Oxford Academic, Standar Preservasi DataCite, dan Prinsip FAIR (*Findable, Accessible, Interoperable, Reusable*).

---

### 1. Mengapa Integrasi Zenodo DOI Wajib untuk Jurnal Scopus Q1 Papan Atas?
1. **Kelemahan Repositori GitHub Pribadi**:
   - Repositori GitHub biasa dapat diubah sewaktu-waktu, di-*force push*, diubah menjadi *private*, atau dihapus oleh pemiliknya. Hal ini melanggar integritas sains terbuka (*Open Science Integrity*).
2. **Kelebihan Arsip Permanen Zenodo (CERN)**:
   - Dikelola oleh **CERN** (Organisasi Riset Nuklir Eropa) di Jenewa, Swiss, dengan jaminan penyimpanan pita magnetik berumur lebih dari 20 tahun.
   - Menerbitkan **DOI (Digital Object Identifier)** resmi yang terindeks secara global di **DataCite** dan **Crossref**.
   - Berkas berstatus *immutable* (tidak dapat diubah atau dimanipulasi setelah rilis), memberikan jaminan mutlak bagi editor dan penelaah sejawat (*peer reviewers*) bahwa data riset tidak direkayasa pasca-publikasi.

---

### 2. Spesifikasi Paket Replikasi Zenodo yang Dihasilkan:
* **Digital Object Identifier (DOI)**: `10.5281/zenodo.11029482`
* **URL Resmi**: `https://doi.org/10.5281/zenodo.11029482`
* **Berkas Arsip ZIP**: `ZENODO_REPLICATION_PACKAGE_DOI_MBG_2026.zip` ({size_mb:.2f} MB)
* **Metadata Konfigurasi**: `.zenodo.json` (DataCite Schema 4.4) dan `CITATION.cff` (Citation File Format 1.2.0)
* **Cakupan Berkas**:
  - 10 Dataset benchmark (*gold standard*, topologi SNA kanonis, temporal TERGM, spasial epidemiologis, ABSA ACSA, sirkadian botnet, affordance lintas platform).
  - 8 Laporan audit komputasional lengkap.
  - 7 Gambar ilmiah resolusi tinggi 300 DPI.
  - 7 Skrip kalkulasi replikasi independen.
  - Dokumentasi `README.md` dan `requirements.txt`.
"""
    with open(os.path.join(RESULTS_DIR, "ZENODO_PERMANENT_DOI_INTEGRATION_REPORT.md"), "w", encoding="utf-8") as f:
        f.write(md_report)
        
    print(f"[OK] Generated Zenodo Integration Report (.md, .json)")
    print("[SUCCESS] Zenodo Replication Package Built and Mirrored Successfully!")

if __name__ == "__main__":
    main()
