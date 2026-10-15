# 📋 Comprehensive Python Repository Audit Report
**Target Repository**: `indri007/ThisIsEconomy` / `tesis_mbg`  
**Working Directory**: `/Users/jevin/Documents/tesis_mbg`  
**Audit Timestamp**: 2026-10-15T10:35:00+07:00  
**Audit Protocol**: Static AST Traversal, Dependency Graph Analysis, and Runtime Verification  
**Auditor**: Antigravity Autonomous Engineering Agent  

---

## 1. Executive Summary

This repository is a **Polyglot Research Monorepo** supporting the empirical Master's thesis of Indri Anjar Kartika Sari (UPN "Veteran" Jawa Timur), titled:
> *"Digital Sarcasm as a Signal of Policy Distrust: Social Network Analysis and Emotion Classification of Indonesia's Free Nutritious Meal Program Discourse on X (Twitter)"*

The monorepo unites empirical NLP (Fine-tuned IndoBERT 9-class), Social Network Analysis (971 nodes, 666 edges), Early Warning System (EWS) telemetry, and an interactive public web dashboard deployed on Streamlit Cloud (`https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/`).

### High-Level Metrics
| Metric | Value | Audit Finding |
| :--- | :---: | :--- |
| **Tracked Python Files** | **226 files** | Across `dashboard/`, `backend/`, `ews/`, `pipelines_30m/`, `scripts/`, `tests/`, `twitter_sentiment_app/` |
| **Total Python Lines of Code (LOC)** | **~74,200 LOC** | (Excluding git-ignored vendor clones `cloned_repos/`, `MiroFish/`, `lib/`) |
| **AST Parse Errors** | **0 errors (100% Valid)** | All 226 files parse without Python syntax defects |
| **Circular Imports** | **0 cycles** | Clean directed acyclic import graph in `dashboard` and `ews` |
| **Automated Test Suite** | **108 Passed (0 Failures)** | All tests passing across 23 test suites (`tests/`) |
| **Working Tree Status** | **2 preserved modifications** | `manuscript/JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx` and `.pdf` preserved |

---

## 2. Inventory of Tracked Python Subsystems

```text
├── dashboard/ (13 files, ~4,800 LOC)
│   ├── app.py                      # Canonical Streamlit application entry point
│   ├── requirements.txt            # Streamlit Cloud isolated dependency manifest
│   └── modules/
│       ├── config.py               # Centralized path resolvers, theme styling, secret getters
│       ├── data_loader.py          # Cached data loading routines (emotion, network, evaluation)
│       ├── ui_components.py        # Stepper, 70-point checklist, biography, footer
│       ├── views_bab1.py           # Chapter I: Introduction & 6 Research Questions
│       ├── views_bab2.py           # Chapter II: Theoretical Framework & Sunburst taxonomy
│       ├── views_bab3.py           # Chapter III: Computational Methodology & Lineage
│       ├── views_bab4.py           # Chapter IV: Empirical Results, CNA, IndoBERT, & Bimodal Peaks
│       ├── views_bab5.py           # Chapter V: Conclusions & Policy Recommendations
│       ├── views_ews.py            # Early Warning System, Brand24, & Twitter AI console
│       ├── views_storytelling.py   # 10 Master Storytelling Visual Plots
│       └── views_audit.py          # Data Integrity Audit & Scopus APA 7th Taxonomy
│
├── ews/ (10 files, ~3,200 LOC)     # Custom Early Warning System (EWS) v2 Engine
│   ├── __init__.py                 # EWS package exports
│   ├── anomaly_detector.py         # Time-series statistical anomaly detection (z-score)
│   ├── config.py                   # Weight configurations, threshold parameters
│   ├── custom_dashboard.py         # Streamlit UI integration for Custom EWS v2
│   ├── emotion_analyzer.py         # IndoBERT affective risk scoring
│   ├── ews_engine.py               # Composite tri-level crisis risk formula (0-100)
│   ├── explainable_score.py        # Score breakdown and feature attribution
│   ├── fallback.py                 # Offline sample dataset failover
│   ├── keyword_analyzer.py         # Multi-tier crisis lexicon density counter
│   └── sna_analyzer.py             # Network centrality integration (DPPTI & polarization)
│
├── twitter_sentiment_app/ (3 files, ~850 LOC) # Tier 4 Scraper & Local Sentiment App
│   ├── app.py                      # Standalone Streamlit monitor app
│   ├── scraper.py                  # Twikit Twitter/X scraper with session cookie auth
│   └── analyzer.py                 # Google Gemini 2.5 Flash sentiment & sarcasm annotator
│
├── backend/ (21 files, ~3,400 LOC) # Tier 2 Headless REST API
│   ├── main.py                     # FastAPI server entry point (port 8000)
│   ├── requirements.txt            # FastAPI backend dependencies
│   └── services/                   # Modular data services (SNA, Emotion, Sarcasm, Communities)
│
├── pipelines_30m/ (6 files, ~2,100 LOC) # 30-Million National Data Lake Pipeline
│   ├── clean_30m_pipeline.py       # High-throughput data lake deduplicator
│   ├── sastrawi_to_indobert.py     # Indonesian morphology and token normalizer
│   ├── indobert_inference.py       # Chunked IndoBERT inference handler
│   └── test_pipeline.py            # Reproducibility unit tests
│
├── scripts/ (141 files, ~48,000 LOC) # Research tooling, evaluation, and document builders
│   ├── auto_scrape_job.py          # Scheduled ingestion & Telegram EWS push bot
│   ├── build_*_manuscript.py       # Automated docx/pdf manuscript compilers
│   ├── compute_*_metrics.py        # Network topology & centrality calculators
│   ├── run_*_audit.py              # Specialized audit scripts (AoIR, Bot, ABSA, Bias)
│   └── audit_archive/              # 30+ archived audit iterations
│
└── tests/ (23 files, ~11,800 LOC)  # Comprehensive pytest verification suite
```

---

## 3. Findings: Code Smells, Duplications, & Overlaps

### 3.1 Duplicate Helper Functions Across Subsystems
1. **Document Formatting Utilities (`set_cell_background` & `set_cell_margins`)**:
   - **Locations**: Found identically copy-pasted in 7 manuscript generation scripts:
     - `backend/generate_academic_bab2.py`
     - `scripts/build_full_30_pages_cloudrun_bit.py`
     - `scripts/build_ics_taylor_francis_manuscript.py`
     - `scripts/build_jcmc_oxford_manuscript.py`
     - `scripts/build_scopus_q1_latest_manuscript.py`
     - `scripts/format_mediator_submission.py`
     - `scripts/revise_jiki_docx.py`
   - **Recommendation**: Extract into a shared document utility module: `scripts/utils/docx_utils.py`.

2. **Secret & Environment Variable Resolvers (`get_secret`)**:
   - **Locations**: Implemented redundantly in:
     - `twitter_sentiment_app/scraper.py`
     - `twitter_sentiment_app/analyzer.py`
     - `scripts/auto_scrape_job.py`
     - `dashboard/modules/config.py`
   - **Recommendation**: Consolidate into `dashboard/modules/config.py::get_secret()` and import cleanly.

3. **Inter-Annotator Agreement Kappa Interpreter (`interpret_kappa`)**:
   - **Locations**: Redundantly defined in:
     - `scripts/iaa_annotation_framework.py`
     - `scripts/run_actual_human_annotation_validation.py`
     - `scripts/run_multi_annotator_agreement_validation.py`
   - **Recommendation**: Consolidate into `scripts/utils/metrics_utils.py`.

4. **Image Path Resolution (`get_image_path`)**:
   - **Locations**: Repeated across `dashboard/modules/config.py`, `dashboard/modules/views_storytelling.py`, and `scripts/build_ics_taylor_francis_manuscript.py`.
   - **Recommendation**: Canonicalize onto `dashboard.modules.config.resolve_image_path()`.

### 3.2 Overlapping Modules & Multi-Engine Divergence
1. **EWS Calculation Dual Implementations**:
   - `ews/ews_engine.py` (Custom EWS v2, normalized 0-100 score).
   - `scripts/early_warning_system.py` (Legacy v1 EWS).
   - `twitter_sentiment_app/app.py` (`compute_ews` helper).
   - `scripts/auto_scrape_job.py` (`analyze_new_batch` lexicon matching).
   - *Assessment*: `ews/` is the canonical, modularized version. The others should reference `ews` instead of maintaining separate threshold dictionaries.

2. **Namespace & Missing Package Boundary**:
   - `twitter_sentiment_app/` lacks `__init__.py`. In `dashboard/modules/views_ews.py`, `sys.path.insert(0, TWITTER_APP_DIR)` is used to import `scraper` and `analyzer` as top-level modules.
   - *Fix*: Add `__init__.py` to `twitter_sentiment_app` and allow both `from twitter_sentiment_app.scraper import scrape_tweets_sync` and local fallback.

---

## 4. Dependency & Configuration Audit

### 4.1 Dependency Manifest Synchronization
* Root `requirements.txt` and `dashboard/requirements.txt` are strictly enforced by `tests/test_audit_master_suite.py::test_08_streamlit_app_startup`. Any edits must be mirrored exactly.
* **Missing Declaration**:
  - `python-docx` (`docx`): Imported in 198 files across document builders and backend modules, but currently absent from `requirements.txt`. While installed in the local environment, fresh Docker or cloud environments will fail if executing manuscript builders without `python-docx`.
* **Deprecation Warnings**:
  - `Sastrawi/Stemmer/Context/Visitor/RemoveInflectionalParticle.py`: Deprecation warning for passing `count` as positional argument in `re.sub()`. (Handled by upstream vendor).

### 4.2 Cloud Deployment Readiness (Streamlit Cloud)
* **Entry Point**: `dashboard/app.py`.
* **Configuration**: `.streamlit/config.toml` specifies:
  ```toml
  [server]
  address = "0.0.0.0"
  headless = true

  [browser]
  gatherUsageStats = false
  ```
* **Asset Resilience**: All image calls routed through `_crash_proof_st_image` to prevent unhandled `MediaFileStorageError` or 404s on Streamlit Cloud.
* **Event Loop Stability**: Polyfill in `dashboard/app.py` mitigates `AnyIO`/`sniffio` `NoEventLoopError` on Python 3.12+.

---

## 5. Security & Sensitive Data Audit
1. `.env.example` is tracked, containing placeholder keys only.
2. `.env` is properly ignored in `.gitignore`, with zero committed API keys.
3. Telegram bot credentials (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) and Twitter tokens are fetched dynamically via `st.secrets` or environment variables with graceful no-op fallbacks when unset.
4. AoIR 3.0 Compliance: Citizen handles in datasets are pseudonymized using SHA-256 HMAC cryptographic hashing.

---

## 6. Baseline Test Status
* Executed: `pytest` in `/Users/jevin/Documents/tesis_mbg`.
* Result: **108 passed, 0 failures, 16 subtests passed**.
* Coverage:
  - Data lineage and 30M manifest integrity.
  - Multi-annotator validation & Option A withdrawal compliance.
  - Hierarchical 3-super-class valence mapping ($Macro\text{-}F1 \ge 0.80$).
  - EWS HTML sanitization & false alarm suppression.
  - Streamlit headless app startup and routing via `AppTest`.

---

## 7. Audit Conclusion & Phase Gate
**Status: PASSED WITH RECOMMENDATIONS**  
The repository is in a stable, well-tested baseline state. No blocking bugs or syntax errors exist. Refactoring can proceed safely by consolidating duplicated utilities, introducing package boundary markers, and syncing dependencies without breaking tests or user changes.
