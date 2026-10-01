# Legacy Checkpoint Audit Report

- **Checkpoint ID:** `results/indobert_finetuned_9_labels/checkpoint-792`
- **Original Split Protocol:** `train_test_split(df['processed_text'], test_size=0.2, random_state=42)`
- **Duplicate Overlap:** 533 unique text strings (0 instances) leaked between train and test sets.
- **Classification Status:** **LEGACY / DIAGNOSTIC ONLY**
- **Justification for Exclusion from Final Comparison:**
  The legacy checkpoint was evaluated on a non-group-aware split where exact duplicate texts appeared in both training and testing partitions, artificially inflating memorization and failing to provide an unbiased generalization estimate.
- **Resolution:** Retrained from scratch using `GroupShuffleSplit` on `processed_text` with verified zero leakage (`Text Overlap = 0`, `Processed Text Overlap = 0`).
