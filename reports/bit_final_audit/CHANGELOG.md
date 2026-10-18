# BIT AUDIT CHANGELOG

## [Audit Session: 2026-10-13T18:19:00+07:00]
**Commit SHA:** `fd229de3b80a8ced01ac8a2ab26001eeb3a8ce49`  
**Auditor:** BIT Automated Forensic Engine  

### Added:
- `config/valence_super_class_mapping.json`: Deterministic 3-super-class valence mapping configuration.
- `reports/bit_final_audit/00_BASELINE.md`: Comprehensive repository inventory and baseline specifications.
- `reports/bit_final_audit/01_NINE_CLASS_VALIDATION.md`: Full empirical validation of IndoBERT 9-emotion model with zero leakage.
- `reports/bit_final_audit/01_NINE_CLASS_METRICS.csv`: Precision, recall, F1, and support per class.
- `reports/bit_final_audit/01_CONFUSION_MATRIX.csv`: Complete 9×9 empirical confusion matrix.
- `reports/bit_final_audit/01_SAMPLE_LEVEL_PREDICTIONS.csv`: Sample-level true vs predicted labels on test set ($N=1,064$).
- `reports/bit_final_audit/02_VALENCE_MAPPING.md`: Theoretical justification and recomputed metrics for 3-tier stance taxonomy.
- `reports/bit_final_audit/02_VALENCE_METRICS.csv`: Super-class metrics (Negative F1 83.90%, Neutral F1 84.08%, Positive F1 77.20%).
- `reports/bit_final_audit/02_VALENCE_CONFUSION_MATRIX.csv`: 3×3 super-class confusion matrix.
- `reports/bit_final_audit/03_DATASET_RECONCILIATION.md`: Rigorous separation of raw data lake footprint (30M) vs active analytical cohorts.
- `reports/bit_final_audit/03_DATASET_MANIFEST.json`: Machine-readable manifest tracking all dataset layers and backlog status.
- `reports/bit_final_audit/03_RECORD_ACCOUNTING.csv`: Exact record-level accounting across all analytical layers.
- `reports/bit_final_audit/04_TAXONOMY_RECONCILIATION.md`: Provenance analysis of the longitudinal 9,360 corpus and the "Love" label.
- `reports/bit_final_audit/05_ANNOTATOR_AGREEMENT.md`: Inter-rater agreement audit (Cohen's Kappa $\kappa = 0.9135$, Fleiss' Kappa = 0.8442).
- `reports/bit_final_audit/06_CLEAN_ENV_TEST_REPORT.md`: Test suite architecture and execution report (101/101 passed).
- `reports/bit_final_audit/06_TEST_EXECUTION.log`: Raw stdout and stderr log of clean environment test run.
- `reports/bit_final_audit/06_ENVIRONMENT.json`: Environment and execution metadata.
- `reports/bit_final_audit/07_SNA_SARCASM_ABSA_EWS.md`: Forensic audit of SNA graph ($|V|=971, |E|=666$), sarcasm, ACSA, and EWS resilience.
- `reports/bit_final_audit/08_CLAIM_EVIDENCE_MATRIX.csv`: Traceability matrix matching 7 primary quantitative claims to empirical datasets.
- `reports/bit_final_audit/08_MANUSCRIPT_CONSISTENCY.md`: Cross-validation report of manuscript numbers against audit results.
- `reports/bit_final_audit/SCIENTIFIC_GROUND_TRUTH.json`: Unified master source of truth for all scientific parameters.
- `reports/bit_final_audit/REMAINING_BLOCKERS.md`: Complete register of resolved issues and non-blocking limitations.
- `scripts/generate_claim_matrix.py`: Standalone reproducible script generating the claim-evidence matrix.

### Modified:
- `tests/test_scientific_validation.py`: Renamed historical 6-class baseline test and added explicit master 9-class model assertion method (`test_reproduce_indobert_master_nine_class_evaluation_metrics`).
- `results/ZENODO_REPLICATION_PACKAGE_DOI_MBG_2026.zip`: Rebuilt and mirrored to include latest 9-class minority reports.
- `README_PANDUAN_SUBMISI.md` & `03_COVER_LETTER_JCMC.md`: Synchronized metrics with 9-class master model and 3-super-class valence taxonomy.
