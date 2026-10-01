# 🔬 Scientific Validation Report — MBG Thesis

> Generated: 2026-10-01T16:19:56.286423+00:00

---

## ✅ Readiness Scorecard

**36 / 40 = 90%**

| Item | Weight | Status | Note |
|------|--------|--------|------|
| Ground-truth specification exists | 4% | ✅ | FINAL_MODEL_COMPARISON references SILVER-STANDARD label |
| Independent human annotation (IAA) documented | 4% | ❌ | No IAA score found; sarcasm/emotion labels are silver-standard, not human-adjudicated |
| Benchmark runner (leakage-safe split) | 4% | ✅ | NO_LEAKAGE confirmed: train=4205, test=1058 |
| Baseline comparison (≥2 baselines) | 4% | ✅ | TF-IDF LogReg + TF-IDF SVM vs IndoBERT |
| 95% Bootstrap CI computed | 4% | ✅ | Bootstrap (n=2000) for IndoBERT; Wilson/Wald for baselines |
| Effect size (Cohen's d / Δ) computed | 4% | ✅ | Delta accuracy/F1 + Cohen's d for all pairs |
| Statistical test (McNemar) computed | 4% | ✅ | McNemar requires per-sample baseline predictions (see mcnemar_results.csv) |
| Provenance / reproducibility metadata | 4% | ✅ | SHA-256 hashes recorded; git=b19a761d97a1 |
| Automated readiness scoring | 4% | ✅ | This scorecard — run scientific_validation_audit.py |
| E2E validation report generated | 4% | ✅ | SCIENTIFIC_VALIDATION_REPORT.json + .md |

---

## 📊 Bootstrap Confidence Intervals (95%)

| Model | Metric | Point | CI Lower | CI Upper | Method |
|-------|--------|-------|----------|----------|--------|
| IndoBERT Group-Aware | accuracy | 0.7940 | 0.7694 | 0.8176 | 2000 |
| IndoBERT Group-Aware | macro_f1 | 0.5160 | 0.4765 | 0.6070 | 2000 |
| TF-IDF + Logistic Regression | accuracy | 0.6947 | 0.6663 | 0.7217 | Wilson (n=1058) |
| TF-IDF + Logistic Regression | macro_f1 | 0.3429 | 0.3143 | 0.3715 | Wald (n=1058) |
| TF-IDF + Linear SVM | accuracy | 0.6720 | 0.6431 | 0.6996 | Wilson (n=1058) |
| TF-IDF + Linear SVM | macro_f1 | 0.4095 | 0.3799 | 0.4391 | Wald (n=1058) |

---

## 📐 Effect Sizes

| Comparison | Metric | IndoBERT | Baseline | Δ | Cohen's d | Interpretation |
|------------|--------|----------|----------|---|-----------|----------------|
| IndoBERT vs TF-IDF + Logistic Regression | accuracy | 0.7940 | 0.6947 | +0.0993 | 0.233 | small |
| IndoBERT vs TF-IDF + Logistic Regression | macro_f1 | 0.5160 | 0.3429 | +0.1731 | N/A (no per-sample F1) | see delta |
| IndoBERT vs TF-IDF + Linear SVM | accuracy | 0.7940 | 0.6720 | +0.1220 | 0.272 | small |
| IndoBERT vs TF-IDF + Linear SVM | macro_f1 | 0.5160 | 0.4095 | +0.1065 | N/A (no per-sample F1) | see delta |

---

## 🧪 McNemar Statistical Test

| Model A | Model B | b | c | χ² | p-value | p<0.05? | Note |
|---------|---------|---|---|-----|---------|---------|------|
| IndoBERT Group-Aware | TF-IDF + Logistic Regression | 194 | 64 | 64.5 | 9.992007221626409e-16 | True | baseline_logreg_predictions.csv |
| IndoBERT Group-Aware | TF-IDF + Linear SVM | 177 | 57 | 60.51709401709402 | 7.327471962526033e-15 | True | baseline_svm_predictions.csv |

---

## 🏷️ Evidence Claims

| Claim ID | Claim | Evidence Type | N | 95% CI | Note |
|----------|-------|---------------|---|--------|------|
| CLAIM-001 | IndoBERT accuracy = 0.794 on test set | `DERIVED_METRIC` | 1,058 | [0.7694, 0.8176] | Silver-standard labels; human IAA not documented |
| CLAIM-002 | IndoBERT Macro-F1 = 0.516 on test set | `DERIVED_METRIC` | 1,058 | [0.4765, 0.6070] | Silver-standard labels; human IAA not documented |
| CLAIM-003 | Sarcasm corpus N = 3,395 (315 sarcastic, 3080 non-sarcastic) | `OBSERVED_DATA` | 3,395 | N/A | Label source: automated; independent human verification not documented |
| CLAIM-004 | Emotion corpus N = 5,263 (7 classes) | `OBSERVED_DATA` | 5,263 | N/A | Label source: automated; independent human verification not documented |
| CLAIM-005 | No text leakage between train/test sets | `DERIVED_METRIC` | 1,058 | N/A | leakage_status=NO_LEAKAGE, text_overlap=0, random_state=42 |

---

## ⚠️ Open Gaps

| Gap ID | Description | Severity | Weight | Action Required |
|--------|-------------|----------|--------|-----------------|
| GAP-001 | Inter-annotator agreement (Cohen/Fleiss κ) not documented | HIGH | 4% | Recruit ≥2 independent annotators; compute κ; adjudicate; document procedure |
| GAP-002 | McNemar test requires per-sample baseline predictions | MEDIUM | 2% | Re-run TF-IDF LogReg and SVM with prediction CSV export; re-run this script |
| GAP-003 | Robustness / sensitivity analysis not implemented | MEDIUM | 2% | Add noise-injection test and hyperparameter sweep section |
| GAP-004 | External / generalization validation dataset missing | LOW | 1% | Collect or identify an out-of-distribution MBG Twitter sample |

---

## 🔑 Provenance

| Key | Value |
|-----|-------|
| Timestamp UTC | `2026-10-01T16:19:56.286423+00:00` |
| Python | `3.12.7` |
| Git commit | `b19a761d97a1` |
| SHA-256 `FINAL_indobert_predictions.csv` | `c65cb5e5e624bd0e…` |
| SHA-256 `FINAL_MODEL_COMPARISON.csv` | `74a32e29ee2f87f3…` |
| SHA-256 `final_split_verification.csv` | `2f00f5963a8ad0a8…` |
| SHA-256 `sarcasm_validation.json` | `92f45d2ac8022504…` |
| SHA-256 `emotion_validation.json` | `db0deec2436676b6…` |