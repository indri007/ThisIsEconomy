# Design Specification: Repository Restructuring & Dashboard Modularization

**Repository**: `indri007/ThisIsEconomy`  
**Date**: 2026-10-07  
**Objective**: Elevate codebase hygiene, architecture, and maintainability from 88/100 to 100/100 while maintaining 100% backward-compatibility for Streamlit Cloud deployment (`https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/`).

---

## 1. Problem Statement & Scope

### Current Deficiencies (88/100):
1. **Root Directory Clutter**: ~25 ad-hoc utility/audit Python scripts (`fix_hmc_v*.py`, `final_hmc_audit_*.py`, `diagnose_spacing.py`) in root.
2. **Binary Bloat & Docx Redundancy in Root**: 4 Word documents (~9 MB each) stored in root totaling ~35 MB.
3. **Empty / Corrupt 0-Byte Files**: `data/absa/dataset_absa.xlsx`, `data/sarcasm/dataset_sindiran.xlsx`, `scripts/preprocessing.py`, and `backend/services/__init__.py`.
4. **Monolithic Dashboard**: `dashboard/app.py` is 443 KB (6,868 lines) in a single file, mixing UI styling, data loading, route handling, PyVis network rendering, EWS, and thesis chapters.
5. **Unpolished Notebook Naming**: `notebooks/Salinan lain dari Untitled8.ipynb` (3.2 MB) retains Google Colab default name and embedded outputs.
6. **No Automated Testing Suite**: Absence of a `tests/` directory with automated assertions.
7. **GitHub Actions CI Path Conflict**: `.github/workflows/mbg_auto_scrape_ews.yml` tries to `git add` an ignored path (`data/raw/`).

---

## 2. Target Architecture

### 2.1. Root Directory Cleanup
- Move all `fix_hmc_v*.py`, `final_hmc_audit_*.py`, `diagnose_spacing.py`, `audit_spacing_*.py`, `precise_spacing_check.py`, `edas_audit.py`, `fix_evidence_*.py`, `fix_p169.py`, `fix_spacing_*.py`, `hmc_*.py` into `scripts/audit_archive/`.
- Move the 4 root docx files (`Journal_Paper_Indri_Anjar_MBG_SNA*.docx`) to `manuscript/` and create symbolic links or safe resolution in `dashboard/app.py` so download buttons in the dashboard still resolve.
- Remove 0-byte corrupt files (`data/absa/dataset_absa.xlsx`, `data/sarcasm/dataset_sindiran.xlsx`, `scripts/preprocessing.py`). Keep valid CSV datasets intact.
- Rename `notebooks/Salinan lain dari Untitled8.ipynb` to `notebooks/01_mbg_eda_and_scraping.ipynb`.
- Fix `.github/workflows/mbg_auto_scrape_ews.yml` to use `git add -f data/raw/live_tweets_mbg_accumulated.csv`.

### 2.2. Dashboard Modularization (Option A - Modular Views Pattern)
Keep `dashboard/app.py` as the lightweight entry point (<150 lines) recognized by Streamlit Cloud, while factoring out modules into `dashboard/modules/`:
1. `dashboard/modules/config.py`: Theme, constants, page configuration, and helper functions (including `download_file_button` and path resolvers).
2. `dashboard/modules/data_loader.py`: Cached dataset loaders (`load_final_evaluation`, network loaders, emotion distribution loaders).
3. `dashboard/modules/ui_components.py`: Shared UI widgets (thesis stepper, summary cards, custom CSS styling, download buttons).
4. `dashboard/modules/views_home.py`: Hero section, research snapshot, and executive summary.
5. `dashboard/modules/views_bab2.py`: Chapter II theoretical framework and literature synthesis.
6. `dashboard/modules/views_bab3.py`: Chapter III methodology, corpus breakdown, and ground-truth validation protocol.
7. `dashboard/modules/views_bab4.py`: Chapter IV empirical findings, PyVis interactive graph, 9-emotion distribution, ABSA thematic analysis, and model comparison.
8. `dashboard/modules/views_ews.py`: Early Warning System (EWS v2), Twitter sentiment monitoring, and alert triggers.
9. `dashboard/modules/views_meta.py`: Author biography, checklist, and Scopus reference audits.

### 2.3. Automated Testing Suite (`tests/`)
Introduce `pytest` test suite:
- `tests/test_data_integrity.py`: Verifies all critical corpus files, node/edge files, and metrics CSVs exist and are non-empty.
- `tests/test_dashboard_imports.py`: Verifies that `dashboard/app.py` and all modules import cleanly without runtime syntax or import errors.
- `tests/test_ews_engine.py`: Tests EWS calculation functions.

---

## 3. Backward Compatibility & Risk Mitigation
- **Streamlit Cloud Zero-Downtime**: `dashboard/app.py` remains in its exact location and entrypoint path.
- **Download Buttons Safety**: The `download_file_button` function already checks file existence safely; pointing to both `manuscript/` and fallback paths ensures no broken downloads.
- **Git State**: All changes will be verified with `pytest` and `py_compile` before committing to `main` and syncing to `cloud-deploy`.
