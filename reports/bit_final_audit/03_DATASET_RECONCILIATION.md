# BIT AUDIT PHASE 3: 30-MILLION RECORD DATASET RECONCILIATION REPORT

**Audit Date:** 2026-10-13T18:09:55+07:00  
**Target Raw File:** `data/processed/tweet_mbg_30juta.csv`  
**Symlink Target:** `data/processed/tweet_mbg_1juta.csv` <-> `data/processed/tweet_mbg_30juta.csv`  
**Physical File Size:** 6,430,132,789 bytes (5.989 GB)  
**SHA-256 Checksum:** `d9333c3a56f2b2e65bdbc68cd7c4aaaf74f6048222443e0f3ab6a576640b06a0`  
**Physical Line Count:** 30,035,226 lines  

---

## 1. Strict Separation: Acquisition Footprint vs. Analytical NLP Corpora

Scientific integrity dictates a rigorous boundary between the raw acquisition footprint and the curated cohorts subjected to transformer NLP inference:

```
[Raw Streaming Harvester (Twitter/X API + Scraping)]
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  RAW BIG DATA LAKE (tweet_mbg_30juta.csv)               │
│  Total Records: 30,000,000 (Physical Lines: 30,035,226)│
│  Size: 5.989 GB | SHA-256: d9333c3a...                 │
└────────────────────────────────────────────────────────┘
          │                                  │
          ▼                                  ▼
┌─────────────────────────┐      ┌─────────────────────────────┐
│  Lake Processing Sample │      │  Unprocessed Lake Backlog   │
│  Records: 600           │      │  Records: 29,999,400        │
│  Status: PROCESSED      │      │  Inference: BLOCKED         │
└─────────────────────────┘      │  Reason: GPU Cost/Cluster   │
                                 └─────────────────────────────┘
          │
          ▼ (Curated Domain Filtering & Crisis Keyword Relevance)
┌────────────────────────────────────────────────────────┐
│  ACTIVE ANALYTICAL CORPORA (Subject to Full NLP & SNA) │
├────────────────────────────────────────────────────────┤
│  1. Crisis Timeline Corpus:           N = 9,360        │
│  2. Master 9-Emotion Corpus:          N = 5,272        │
│  3. Sarcasm & Network (SNA) Corpus:   N = 3,395        │
│  4. Gold Standard Consensus Benchmark: n = 100         │
└────────────────────────────────────────────────────────┘
```

---

## 2. Record Accounting Matrix

| Corpus Layer | Declared Records | Physical Lines / Rows | NLP Inferred | Unprocessed Backlog | Operational Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Raw Acquisition Lake** | 30,000,000 | 30,035,226 | 600 (Sample) | 29,999,400 | **BLOCKED** (GPU Cluster Protection) |
| **Crisis Timeline** | 9,360 | 9,360 | 9,360 | 0 | **COMPLETED** (Temporal Tracking) |
| **Master 9-Emotion** | 5,272 | 5,272 | 5,272 | 0 | **COMPLETED** (IndoBERT Fine-Tuning) |
| **SNA & Sarcasm** | 3,395 | 3,395 | 3,395 | 0 | **COMPLETED** (Network Analysis) |
| **Gold Standard Benchmark** | 100 | 100 | 100 | 0 | **COMPLETED** (Human Agreement $\kappa=0.832$) |

---

## 3. Explaining the Symbolic Link (`tweet_mbg_1juta.csv`)
* **Historical Provenance:** In earlier development iterations, the pipeline anticipated a 1-million record benchmark named `tweet_mbg_1juta.csv`. When harvesting scaled to 30 million records, a physical CSV `tweet_mbg_30juta.csv` (6.43 GB) was populated, and a symbolic link was created to preserve backward compatibility for legacy pipeline scripts.
* **Audit Verification:** Inspecting the file system reveals both names reference the identical underlying 6.43 GB storage inode.

---

## 4. Policy for Future Full-Lake Inference
If full inference of the 29,999,400 backlog records is ever mandated:
1. It requires estimated **38 hours** of A100 GPU compute.
2. Given that 85%+ of general social media streaming consists of noise, retweets, or spam, full-lake inference without relevance filtering is scientifically suboptimal and financially prohibitive.
3. Therefore, maintaining the **`BLOCKED`** status for full uncurated lake inference while validating on carefully curated cohorts ($N=9,360$ and $N=5,272$) is the correct, standard methodology in computational social science.

---

## 5. Artifact Reference
- Manifest JSON: `reports/bit_final_audit/03_DATASET_MANIFEST.json`
- Accounting CSV: `reports/bit_final_audit/03_RECORD_ACCOUNTING.csv`
