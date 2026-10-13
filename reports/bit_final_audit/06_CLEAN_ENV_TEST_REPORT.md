# BIT AUDIT PHASE 6: REPRODUCIBILITY AND TEST SUITE REPORT

**Audit Date:** 2026-10-13T18:13:46+07:00  
**Test Command:** `/opt/miniconda3/bin/python3 -m pytest tests/ -v --tb=short`  
**Test Suite Status:** **101 PASSED (100% Success Rate, 0 Failed)**  
**Duration:** 12.69 seconds  
**Execution Log File:** `reports/bit_final_audit/06_TEST_EXECUTION.log`  
**Environment Metadata:** `reports/bit_final_audit/06_ENVIRONMENT.json`  

---

## 1. Test Suite Architecture & Categorization

The repository's test suite contains 101 tests categorized across four distinct scientific layers:

| Layer | Test Files | Total Tests | Focus Area & Verified Properties |
| :--- | :--- | :---: | :--- |
| **Scientific Validation** | `tests/test_scientific_validation.py`<br>`tests/test_minority_class_audit.py` | 10 | Model performance recomputation, 9-class split integrity, zero leakage, class imbalance audit. |
| **Data Integrity & Lineage** | `tests/test_data_integrity.py`<br>`tests/test_operational_and_pipeline_audit.py` | 9 | Multi-corpus lineage reconciliation ($5,272 = 4,208 + 1,064$), 30M manifest integrity. |
| **Communication Networks (CNA) & Forensics** | `tests/test_canonical_sna_recalculation.py`<br>`tests/test_dynamic_temporal_network.py`<br>`tests/test_spatial_epidemiological_correlation.py`<br>`tests/test_astroturfing_bot_audit.py`<br>`tests/test_absa_acsa_validation.py` | 23 | Directed graph topology ($|V|=971, |E|=666, Q=0.9837$), 4 temporal crisis phases, Spearman rank correlation ($\rho=0.7212$), circadian distributions. |
| **System Reliability & EWS** | `tests/test_ews_engine.py`<br>`tests/test_telegram_ews.py`<br>`tests/test_zenodo_replication_package.py`<br>`tests/test_audit_master_suite.py` | 59 | Early Warning System relevance-gating, HTML anti-injection, retry/backoff, Zenodo package integrity. |

---

## 2. Separation of Distinct Model Evaluations

A major audit finding resolved in this phase is the explicit separation between:
1. **Historical Baseline v1/v2 (6 Classes, $n = 1,058$):**
   - Method: `test_reproduce_indobert_historical_six_class_baseline_metrics`
   - Verified: Accuracy 79.40%, Macro Precision 0.6726, Macro Recall 0.4977, Macro-F1 0.5160, Weighted-F1 0.7851.
2. **Master Current Model (9 Classes, $N = 1,064$):**
   - Method: `test_reproduce_indobert_master_nine_class_evaluation_metrics`
   - Verified: Accuracy 79.14%, Macro Precision 0.5069, Macro Recall 0.4846, Macro-F1 0.4810, Weighted-F1 0.7889.
3. **Hierarchical Stance Super-Class ($N = 1,064$):**
   - Method: `test_hierarchical_super_class_valence_evaluation`
   - Verified: Accuracy 81.67%, Macro-F1 81.73%, Weighted-F1 81.88%.

---

## 3. Environment & Execution Integrity
- **Python Version:** 3.13.11 | Clang 20.1.8 | macOS Darwin 24.3.0
- **Pytest Version:** 9.1.0
- **Integrity Guarantee:** Zero test assertions were relaxed, mock-bypassed, or suppressed. Every metric is computed dynamically from real underlying predictions and ground-truth references.
