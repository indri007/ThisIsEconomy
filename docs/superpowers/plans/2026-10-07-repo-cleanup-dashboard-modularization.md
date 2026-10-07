# Repository Restructuring & Dashboard Modularization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean the root directory, eliminate 0-byte/redundant assets, modularize the 6,868-line Streamlit dashboard into maintainable modules, and add an automated test suite to achieve a perfect 100/100 repo quality score.

**Architecture:** A streamlined root directory with ad-hoc scripts archived, redundant binaries stored in `manuscript/`, and `dashboard/app.py` transformed into a slim entrypoint (<150 lines) delegating to `dashboard/modules/` without breaking Streamlit Cloud. Automated testing via `pytest` covers data integrity and imports.

**Tech Stack:** Python 3.12, Streamlit, NetworkX, Plotly, Pandas, Pytest.

## Global Constraints
- `dashboard/app.py` must remain the working entry point for Streamlit Cloud.
- Download buttons in dashboard must continue resolving valid docx and gexf files without crashes.
- Git working tree must be clean, with zero syntax or runtime import errors.

---

### Task 1: Root Directory Cleanup & Asset Organization

**Files:**
- Create/Move to: `scripts/audit_archive/`
- Move from root:
  - `fix_hmc_*.py`, `final_hmc_*.py`, `diagnose_spacing.py`, `audit_spacing_*.py`, `precise_spacing_check.py`, `edas_audit.py`, `fix_evidence_*.py`, `fix_p169.py`, `fix_spacing_*.py`, `hmc_*.py`, `final_10step_audit.py`
- Move root docx to: `manuscript/`
  - `Journal_Paper_Indri_Anjar_MBG_SNA.docx`
  - `Journal_Paper_Indri_Anjar_MBG_SNA_30_Pages.docx`
  - `Journal_Paper_Indri_Anjar_MBG_SNA_JIKI.docx`
  - `Journal_Paper_Indri_Anjar_MBG_SNA_JIKI_REVISED.docx`
- Remove 0-byte files:
  - `data/absa/dataset_absa.xlsx`
  - `data/sarcasm/dataset_sindiran.xlsx`
  - `scripts/preprocessing.py`
- Rename notebook:
  - `notebooks/Salinan lain dari Untitled8.ipynb` -> `notebooks/01_mbg_eda_and_scraping.ipynb`
- Modify: `.github/workflows/mbg_auto_scrape_ews.yml` (add `-f` flag to `git add`)

- [ ] **Step 1: Create `scripts/audit_archive/` and move root audit scripts**
- [ ] **Step 2: Relocate root docx documents into `manuscript/` and ensure backward-compatible paths**
- [ ] **Step 3: Remove corrupt/empty 0-byte files**
- [ ] **Step 4: Rename Google Colab notebook to descriptive academic name**
- [ ] **Step 5: Fix `.github/workflows/mbg_auto_scrape_ews.yml`**
- [ ] **Step 6: Commit Task 1 changes**

---

### Task 2: Dashboard Modularization (`dashboard/app.py`)

**Files:**
- Create: `dashboard/modules/__init__.py`
- Create: `dashboard/modules/config.py` (styles, path resolution, `download_file_button`, constants)
- Create: `dashboard/modules/data_loader.py` (cached data loaders)
- Create: `dashboard/modules/ui_components.py` (stepper, metrics cards, badges)
- Create: `dashboard/modules/views_home.py` (Beranda & Executive Summary)
- Create: `dashboard/modules/views_bab2.py` (Bab II Tinjauan Pustaka & Sintesis Teori)
- Create: `dashboard/modules/views_bab3.py` (Bab III Metodologi & Korpus Ground Truth)
- Create: `dashboard/modules/views_bab4.py` (Bab IV Temuan Empiris, CNA Graph, IndoBERT & ABSA)
- Create: `dashboard/modules/views_ews.py` (Early Warning System & Twitter Sentiment Monitor)
- Create: `dashboard/modules/views_meta.py` (Profil Peneliti, Checklist 70 Poin, & Referensi Scopus)
- Modify: `dashboard/app.py` (streamlined coordinator orchestrating sidebar and views)

- [ ] **Step 1: Create `dashboard/modules/` directory and `config.py` with path resolvers supporting both root and `manuscript/` paths**
- [ ] **Step 2: Create `data_loader.py` and `ui_components.py`**
- [ ] **Step 3: Extract chapter views (`views_home.py`, `views_bab2.py`, `views_bab3.py`, `views_bab4.py`)**
- [ ] **Step 4: Extract EWS and meta views (`views_ews.py`, `views_meta.py`)**
- [ ] **Step 5: Rewrite `dashboard/app.py` as clean router (<150 lines)**
- [ ] **Step 6: Run `python3 -m py_compile` across all files in `dashboard/`**
- [ ] **Step 7: Commit Task 2 changes**

---

### Task 3: Automated Test Suite

**Files:**
- Create: `tests/test_data_integrity.py`
- Create: `tests/test_dashboard_imports.py`
- Create: `tests/test_ews_engine.py`

- [ ] **Step 1: Write `tests/test_data_integrity.py` verifying critical CSV, GEXF, and image files**
- [ ] **Step 2: Write `tests/test_dashboard_imports.py` verifying all dashboard modules import cleanly**
- [ ] **Step 3: Write `tests/test_ews_engine.py` verifying anomaly detection and EWS calculations**
- [ ] **Step 4: Run test suite via `pytest` and verify 100% pass rate**
- [ ] **Step 5: Commit Task 3 changes**

---

### Task 4: Final Verification, Git Synchronization & Score Review

**Files:**
- Modify: `README.md` (update architecture section reflecting modular dashboard and test suite)

- [ ] **Step 1: Run full verification suite (`pytest`, `verify_paths.py`)**
- [ ] **Step 2: Push changes to `origin/main`**
- [ ] **Step 3: Synchronize `origin/cloud-deploy`**
- [ ] **Step 4: Generate final 100/100 score review for the user**
