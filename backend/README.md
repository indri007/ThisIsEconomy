# 🔬 Telegram Literature Research Intelligence Platform

> An end-to-end Python research intelligence pipeline for literature discovery,
> verification, full-text analysis, methodology extraction, research-gap discovery,
> thesis alignment, academic reporting, and reproducible research.

[![Roadmap](https://img.shields.io/badge/Roadmap-392%20Tasks-blue)](ROADMAP.md)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange)]()
[![Research](https://img.shields.io/badge/Research-Academic-purple)]()
[![Reproducible](https://img.shields.io/badge/Reproducible-Yes-green)]()

---

## 🎯 Vision

Build a reproducible research intelligence platform that transforms:

**Literature Discovery → Verification → Full-Text Intelligence → Research Synthesis → Thesis Alignment → Academic Output**

The system is designed to support research involving:

- Telegram / Telegram Bots
- AI / LLM / NLP
- Social Network Analysis
- Emotion Analysis & Sarcasm Detection
- ABSA / Emoji / Hashtag
- Community Detection / Topic Modeling
- Policy Communication / Marketing 6.0
- MBG / Makan Bergizi Gratis

---

## 🗺️ Development Roadmap

### Progress

```text
Phase 1  Data Foundation          ░░░░░░░░░░  0%
Phase 2  Verification             ░░░░░░░░░░  0%
Phase 3  Full-Text Intelligence   ░░░░░░░░░░  0%
Phase 4  Research Synthesis       ░░░░░░░░░░  0%
Phase 5  Thesis Alignment         ░░░░░░░░░░  0%
Phase 6  Academic Output          ░░░░░░░░░░  0%
Phase 7  Reproducibility          ░░░░░░░░░░  0%
Phase 8  Research Platform        ░░░░░░░░░░  0%

Total roadmap: 392 tasks | Completed: 0 | Remaining: 392
```

→ See full task list with IDs: [ROADMAP.md](ROADMAP.md)

---

## 🚀 Pipeline Overview

```
┌──────────────────────┐
│   Literature Search  │  Phase 1
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Data Normalization   │  Phase 1
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ DOI / Metadata Audit │  Phase 2
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Scopus / Q1 Verify   │  Phase 2
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Full Text Analysis   │  Phase 3
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Methodology Mining   │  Phase 3
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Research Gap Engine  │  Phase 4
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Thesis Alignment     │  Phase 5
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Academic Outputs     │  Phase 6
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Reproducible System  │  Phase 7–8
└──────────────────────┘
```

---

## 🎓 Thesis Alignment

| Component            | Status |
|----------------------|--------|
| Telegram             | ⬜     |
| Twitter/X            | ⬜     |
| Social Network Analysis | ⬜  |
| IndoBERT             | ⬜     |
| Emotion              | ⬜     |
| Sarcasm              | ⬜     |
| ABSA                 | ⬜     |
| Emoji                | ⬜     |
| Hashtag              | ⬜     |
| Community Detection  | ⬜     |
| Topic Modeling       | ⬜     |
| Marketing 6.0        | ⬜     |
| Phygital             | ⬜     |
| Policy Communication | ⬜     |
| MBG                  | ⬜     |

---

## 🔬 Scientific Validation Gap (82 → 100)

Current pipeline maturity: **82 / 100**

| # | Gap Area                                                       | Weight | Status |
|---|----------------------------------------------------------------|--------|--------|
| 1 | Independent ground-truth validation (emotion/sarcasm labels)   | 4%     | ⬜     |
| 2 | Inter-annotator agreement (Cohen/Fleiss κ) + adjudication      | 2%     | ⬜     |
| 3 | Out-of-sample IndoBERT benchmark (leakage-safe)                | 2%     | ⬜     |
| 4 | Baseline model comparison (consistent)                         | 2%     | ⬜     |
| 5 | Statistical uncertainty: 95% CI + effect size + sig. test      | 2%     | ⬜     |
| 6 | Robustness / sensitivity analysis                              | 2%     | ⬜     |
| 7 | Reproducibility audit end-to-end                               | 1%     | ⬜     |
| 8 | Claim–evidence audit (every claim traceable to evidence)       | 1%     | ⬜     |
| 9 | External / generalization validation                           | 1%     | ⬜     |
|10 | Final manuscript consistency + replication package             | 1%     | ⬜     |

### Evidence Type Taxonomy

```text
OBSERVED_DATA       — raw dataset metrics (nodes, edges, corpus size)
GROUND_TRUTH        — labels with documented annotation procedure
HUMAN_ANNOTATED     — human-labelled data (must include IAA score)
MODEL_INFERENCE     — output from a trained model
DERIVED_METRIC      — computed from above (accuracy, F1, centrality, etc.)
LITERATURE_EVIDENCE — citation-backed claim
INTERPRETATION      — author's analytical inference
```

> ⚠️ **"ground truth"** must only be applied to data with a documented
> annotation procedure, annotator credentials, IAA score, and adjudication protocol.

### Minimum Benchmark Template

```text
TRAIN  →  VALIDATION  →  UNSEEN TEST
                               ↓
               IndoBERT  vs  Baseline A  vs  Baseline B
                               ↓
            Accuracy / Macro-F1 / Precision / Recall
                               ↓
                    95% Bootstrap CI
                    Effect Size (Cohen's d / Δ)
                    Statistical Test (McNemar / Wilcoxon)
                    N | Dataset Hash | Model Version
```

---

## 🔐 Research Integrity Rules

- No fabricated DOI.
- No fabricated Scopus status.
- No fabricated Q1 status.
- No fabricated methodology.
- No fabricated research gap.
- When evidence is unavailable: **`UNVERIFIED`**
- Candidate status must **never** be presented as verified status.

---

## 🧪 Current Dataset Baseline

```text
Records                  : 322
Columns                  : 46
Valid DOI syntax         : 308
Missing DOI              : 14
Invalid DOI syntax       : 0
Scopus                   : UNVERIFIED
Q1 / Quartile            : UNVERIFIED
```

---

## 🛣️ Version Roadmap

| Version | Milestone                       |
|---------|---------------------------------|
| v0.1    | Discovery Engine                |
| v0.2    | Data Quality Engine             |
| v0.3    | DOI & Metadata Verification     |
| v0.4    | Scopus / Quartile Verification  |
| v0.5    | Full-Text Intelligence          |
| v0.6    | Methodology Intelligence        |
| v0.7    | Research Gap Engine             |
| v0.8    | Thesis Alignment Engine         |
| v0.9    | Academic Export                 |
| v1.0    | Reproducible Research Platform  |

---

## 📊 Roadmap Status

```
0 / 392 tasks completed
[░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## 📚 Documentation

- [ROADMAP.md](ROADMAP.md) — Full 392-task development roadmap with IDs
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — System architecture
- [docs/DATA_MODEL.md](docs/DATA_MODEL.md) — Data schema & model
- [docs/EVIDENCE_MODEL.md](docs/EVIDENCE_MODEL.md) — Evidence taxonomy & traceability

---

## 🗂️ Repository Structure

```
.
├── README.md                  ← Landing page (this file)
├── ROADMAP.md                 ← 392-task backlog with IDs
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── src/                       ← Source modules
├── tests/                     ← Unit / integration tests
├── docs/                      ← Architecture & data model docs
└── .github/
    └── workflows/             ← CI/CD pipelines
```

---

## 🤝 Development

Every new feature must include:

1. Implementation
2. Validation
3. Test
4. Documentation
5. Provenance
6. Reproducibility information

---

*Built to support thesis research on Social Network Analysis, Sarcasm Detection on Twitter/X,
and policy communication around Makan Bergizi Gratis (MBG).*
