# 03 Group-Aware Split Audit Report

## 1. Protocol Specifications
- **Split Method:** `GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)`
- **Grouping Entity:** `processed_text` (prevents representation & token-level leakage)
- **Train Records:** 4205 (79.90%)
- **Test Records:** 1058 (20.10%)

## 2. Programmatic Verification
- **Exact Raw Text Overlap (`text`):** 0 (PASSED: Exactly 0)
- **Exact Processed Text Overlap (`processed_text`):** 0 (PASSED: Exactly 0)
- **OVERLAP TEXT = 0**: VERIFIED

## 3. Label Distribution Across Splits
| Emotion Class | Train Count (N) | Train Pct (%) | Test Count (N) | Test Pct (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Jijik** | 2354 | 55.98% | 606 | 57.28% |
| **Percaya** | 853 | 20.29% | 220 | 20.79% |
| **Netral** | 525 | 12.49% | 124 | 11.72% |
| **Tertarik** | 414 | 9.85% | 91 | 8.60% |
| **Marah** | 41 | 0.98% | 14 | 1.32% |
| **Sedih** | 16 | 0.38% | 3 | 0.28% |
| **Takut** | 2 | 0.05% | 0 | 0.00% |
