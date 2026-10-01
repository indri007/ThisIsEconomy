# 🗺️ ROADMAP — Telegram Literature Research Intelligence Platform

> 392 tasks organised across 8 phases.  
> Each task has a unique ID that can be linked to a GitHub Issue/Project card.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ⬜     | Not started |
| 🔄     | In progress |
| ✅     | Completed |

---

## PHASE 1 — DATA FOUNDATION

### Core Pipeline & Data Engine

- [ ] **DATA-001** Discovery literature
- [ ] **DATA-002** Multi-query search
- [ ] **DATA-003** Query registry
- [ ] **DATA-004** Search provenance
- [ ] **DATA-005** Retrieval timestamp
- [ ] **DATA-006** Persistent record ID
- [ ] **DATA-007** Schema normalization
- [ ] **DATA-008** Publication-year normalization
- [ ] **DATA-009** Missing-value normalization
- [ ] **DATA-010** Type normalization
- [ ] **DATA-011** Deduplication by DOI
- [ ] **DATA-012** Deduplication by title
- [ ] **DATA-013** Semantic duplicate detection
- [ ] **DATA-014** Preprint → journal matching
- [ ] **DATA-015** Conference → journal matching
- [ ] **DATA-016** Record lineage
- [ ] **DATA-017** Data lineage
- [ ] **DATA-018** Inclusion/exclusion rules
- [ ] **DATA-019** Inclusion/exclusion reason
- [ ] **DATA-020** Manual-review queue
- [ ] **DATA-021** Conflict detection
- [ ] **DATA-022** Data-quality score
- [ ] **DATA-023** Evidence-level tagging
- [ ] **DATA-024** Audit trail JSON
- [ ] **DATA-025** Configuration YAML/JSON
- [ ] **DATA-026** Checkpoint/resume
- [ ] **DATA-027** API caching
- [ ] **DATA-028** Retry mechanism
- [ ] **DATA-029** Rate-limit handling
- [ ] **DATA-030** Exception handling

---

## PHASE 2 — BIBLIOGRAPHIC & JOURNAL VERIFICATION

### DOI & Bibliographic Verification

- [ ] **VER-001** DOI syntax check
- [ ] **VER-002** DOI normalization
- [ ] **VER-003** DOI duplicate check
- [ ] **VER-004** DOI resolver check
- [ ] **VER-005** DOI-title consistency
- [ ] **VER-006** DOI-author consistency
- [ ] **VER-007** DOI-journal consistency
- [ ] **VER-008** DOI-year consistency
- [ ] **VER-009** DOI source attribution
- [ ] **VER-010** DOI resolution status
- [ ] **VER-011** Missing DOI report
- [ ] **VER-012** Broken DOI report
- [ ] **VER-013** Publisher metadata cross-check
- [ ] **VER-014** Crossref cross-check
- [ ] **VER-015** OpenAlex cross-check
- [ ] **VER-016** Bibliographic conflict report

### Scopus & Journal Quality

- [ ] **VER-017** Journal identification
- [ ] **VER-018** ISSN extraction
- [ ] **VER-019** ISSN-L normalization
- [ ] **VER-020** Publisher identification
- [ ] **VER-021** Journal subject/category
- [ ] **VER-022** Scopus indexed status
- [ ] **VER-023** Scopus source verification
- [ ] **VER-024** Scopus coverage year
- [ ] **VER-025** Scopus source title
- [ ] **VER-026** CiteScore data
- [ ] **VER-027** SJR data
- [ ] **VER-028** SNIP data
- [ ] **VER-029** Quartile verification
- [ ] **VER-030** Q1/Q2/Q3/Q4 tagging
- [ ] **VER-031** Quartile year
- [ ] **VER-032** Quartile source
- [ ] **VER-033** Historical quartile
- [ ] **VER-034** Candidate ≠ verified logic
- [ ] **VER-035** UNVERIFIED preservation
- [ ] **VER-036** Journal status audit

### Publication Integrity

- [ ] **VER-037** Retraction check
- [ ] **VER-038** Retraction date
- [ ] **VER-039** Retraction reason/source
- [ ] **VER-040** Correction check
- [ ] **VER-041** Expression-of-concern check
- [ ] **VER-042** Erratum check
- [ ] **VER-043** Article version matching
- [ ] **VER-044** Publication integrity flag

---

## PHASE 3 — FULL-TEXT INTELLIGENCE

### Full-Text Retrieval

- [ ] **FTX-001** Full-text availability
- [ ] **FTX-002** Open-access status
- [ ] **FTX-003** Legal full-text source
- [ ] **FTX-004** PDF URL
- [ ] **FTX-005** PDF download
- [ ] **FTX-006** PDF integrity check
- [ ] **FTX-007** Text extraction
- [ ] **FTX-008** OCR fallback
- [ ] **FTX-009** Extraction quality score
- [ ] **FTX-010** Page detection
- [ ] **FTX-011** Section detection
- [ ] **FTX-012** References extraction
- [ ] **FTX-013** Tables detection
- [ ] **FTX-014** Figures detection

### Abstract & Text Processing

- [ ] **FTX-015** Abstract extraction
- [ ] **FTX-016** OpenAlex inverted-index reconstruction
- [ ] **FTX-017** Abstract cleaning
- [ ] **FTX-018** Language detection
- [ ] **FTX-019** Translation layer
- [ ] **FTX-020** Text normalization
- [ ] **FTX-021** Sentence segmentation
- [ ] **FTX-022** Section-aware extraction

### Methodology Extraction

- [ ] **FTX-023** Methodology detection
- [ ] **FTX-024** Full-text methodology detection
- [ ] **FTX-025** Research design
- [ ] **FTX-026** Research question extraction
- [ ] **FTX-027** Hypothesis extraction
- [ ] **FTX-028** Dataset extraction
- [ ] **FTX-029** Sample-size extraction
- [ ] **FTX-030** Platform extraction
- [ ] **FTX-031** Data collection method
- [ ] **FTX-032** API usage detection
- [ ] **FTX-033** Sampling method
- [ ] **FTX-034** Model extraction
- [ ] **FTX-035** Algorithm extraction
- [ ] **FTX-036** Feature extraction
- [ ] **FTX-037** Evaluation metric extraction
- [ ] **FTX-038** Baseline extraction
- [ ] **FTX-039** Hyperparameter extraction
- [ ] **FTX-040** Train/validation/test split
- [ ] **FTX-041** Statistical test extraction
- [ ] **FTX-042** Limitation extraction
- [ ] **FTX-043** Future-work extraction
- [ ] **FTX-044** Theory extraction
- [ ] **FTX-045** Variable/construct extraction

---

## PHASE 4 — RESEARCH SYNTHESIS

### Relevance Engine

- [ ] **SYN-001** Telegram relevance
- [ ] **SYN-002** Bot relevance
- [ ] **SYN-003** Telegram Bot API relevance
- [ ] **SYN-004** AI/LLM relevance
- [ ] **SYN-005** NLP relevance
- [ ] **SYN-006** SNA relevance
- [ ] **SYN-007** Misinformation relevance
- [ ] **SYN-008** Disinformation relevance
- [ ] **SYN-009** Sentiment relevance
- [ ] **SYN-010** Emotion relevance
- [ ] **SYN-011** Sarcasm relevance
- [ ] **SYN-012** ABSA relevance
- [ ] **SYN-013** Emoji relevance
- [ ] **SYN-014** Policy communication relevance
- [ ] **SYN-015** Marketing 6.0 relevance
- [ ] **SYN-016** MBG relevance
- [ ] **SYN-017** Search-score explanation
- [ ] **SYN-018** Relevance reason

### Research Gap Engine

- [ ] **SYN-019** Topic gap
- [ ] **SYN-020** Platform gap
- [ ] **SYN-021** Dataset gap
- [ ] **SYN-022** Population gap
- [ ] **SYN-023** Geographic gap
- [ ] **SYN-024** Temporal gap
- [ ] **SYN-025** Methodological gap
- [ ] **SYN-026** Theoretical gap
- [ ] **SYN-027** Measurement gap
- [ ] **SYN-028** Context gap
- [ ] **SYN-029** Application gap
- [ ] **SYN-030** Evidence gap
- [ ] **SYN-031** Full-text gap
- [ ] **SYN-032** Limitation-derived gap
- [ ] **SYN-033** Future-work-derived gap
- [ ] **SYN-034** Thesis novelty mapping
- [ ] **SYN-035** Gap confidence
- [ ] **SYN-036** Evidence supporting gap

### Quality Assessment

- [ ] **SYN-037** Research question quality
- [ ] **SYN-038** Dataset transparency
- [ ] **SYN-039** Sample transparency
- [ ] **SYN-040** Method reproducibility
- [ ] **SYN-041** Evaluation transparency
- [ ] **SYN-042** Statistical transparency
- [ ] **SYN-043** Limitations disclosed
- [ ] **SYN-044** Full-text availability
- [ ] **SYN-045** DOI available
- [ ] **SYN-046** Metadata completeness
- [ ] **SYN-047** Citation traceability
- [ ] **SYN-048** Reproducibility checklist
- [ ] **SYN-049** Evidence completeness score

### PRISMA / Systematic Review

- [ ] **SYN-050** Identification count
- [ ] **SYN-051** Duplicate removal
- [ ] **SYN-052** Screening count
- [ ] **SYN-053** Exclusion count
- [ ] **SYN-054** Exclusion reasons
- [ ] **SYN-055** Full-text assessment
- [ ] **SYN-056** Full-text exclusion
- [ ] **SYN-057** Final included studies
- [ ] **SYN-058** PRISMA flow numbers
- [ ] **SYN-059** PRISMA diagram
- [ ] **SYN-060** Search strategy documentation
- [ ] **SYN-061** Inclusion criteria
- [ ] **SYN-062** Exclusion criteria

---

## PHASE 5 — THESIS ALIGNMENT & ADVANCED RESEARCH

### Thesis-Specific Mapping

- [ ] **THESIS-001** SNA detection
- [ ] **THESIS-002** IndoBERT detection
- [ ] **THESIS-003** BERT-family detection
- [ ] **THESIS-004** Emotion detection
- [ ] **THESIS-005** Sarcasm detection
- [ ] **THESIS-006** ABSA detection
- [ ] **THESIS-007** Emoji analysis
- [ ] **THESIS-008** Hashtag analysis
- [ ] **THESIS-009** Community detection
- [ ] **THESIS-010** Louvain detection
- [ ] **THESIS-011** Centrality detection
- [ ] **THESIS-012** Topic modeling
- [ ] **THESIS-013** Sentiment analysis
- [ ] **THESIS-014** Marketing 6.0
- [ ] **THESIS-015** Phygital
- [ ] **THESIS-016** Metamarketing
- [ ] **THESIS-017** Policy communication
- [ ] **THESIS-018** Public communication
- [ ] **THESIS-019** MBG context
- [ ] **THESIS-020** Twitter/X comparison
- [ ] **THESIS-021** Telegram-vs-X comparison
- [ ] **THESIS-022** Thesis alignment score
- [ ] **THESIS-023** Thesis component coverage

### Scientific Validation (82 → 100)

- [ ] **THESIS-024** Independent ground-truth validation protocol
- [ ] **THESIS-025** Annotator recruitment & credentials
- [ ] **THESIS-026** Annotation guidelines document
- [ ] **THESIS-027** Annotator A labels
- [ ] **THESIS-028** Annotator B labels
- [ ] **THESIS-029** Annotator C labels
- [ ] **THESIS-030** Cohen's κ / Fleiss' κ computation
- [ ] **THESIS-031** Adjudication protocol
- [ ] **THESIS-032** Final adjudicated ground truth
- [ ] **THESIS-033** Leakage-safe train/val/test split
- [ ] **THESIS-034** IndoBERT benchmark on unseen test set
- [ ] **THESIS-035** Baseline A (e.g. SVM + TF-IDF)
- [ ] **THESIS-036** Baseline B (e.g. LSTM)
- [ ] **THESIS-037** Consistent preprocessing across all models
- [ ] **THESIS-038** 95% Bootstrap CI computation
- [ ] **THESIS-039** Effect size (Cohen's d / Δ)
- [ ] **THESIS-040** Statistical test (McNemar / Wilcoxon)
- [ ] **THESIS-041** Robustness analysis (noise injection)
- [ ] **THESIS-042** Sensitivity analysis (hyperparameter sweep)
- [ ] **THESIS-043** Claim–evidence audit table
- [ ] **THESIS-044** Evidence type tagging for every claim
- [ ] **THESIS-045** External validation dataset

### Topic / NLP Analysis

- [ ] **THESIS-046** Keyword extraction
- [ ] **THESIS-047** Keyword normalization
- [ ] **THESIS-048** Keyword co-occurrence
- [ ] **THESIS-049** Topic modeling
- [ ] **THESIS-050** BERTopic
- [ ] **THESIS-051** LDA
- [ ] **THESIS-052** Semantic clustering
- [ ] **THESIS-053** Embedding generation
- [ ] **THESIS-054** Thesis-paper similarity
- [ ] **THESIS-055** Duplicate semantic similarity
- [ ] **THESIS-056** Topic evolution 2024→2026

### Author / Institution / Country

- [ ] **THESIS-057** Author extraction
- [ ] **THESIS-058** Author normalization
- [ ] **THESIS-059** Institution extraction
- [ ] **THESIS-060** Institution normalization
- [ ] **THESIS-061** Country extraction
- [ ] **THESIS-062** Country normalization
- [ ] **THESIS-063** Author frequency
- [ ] **THESIS-064** Institution frequency
- [ ] **THESIS-065** Country frequency
- [ ] **THESIS-066** Co-author network

### Citation Analysis

- [ ] **THESIS-067** Citation count
- [ ] **THESIS-068** Citation source
- [ ] **THESIS-069** Citation retrieval date
- [ ] **THESIS-070** Citation trend
- [ ] **THESIS-071** Citation network
- [ ] **THESIS-072** Co-citation analysis
- [ ] **THESIS-073** Bibliographic coupling
- [ ] **THESIS-074** Reference network

---

## PHASE 6 — ACADEMIC OUTPUT

### Bibliography

- [ ] **OUT-001** APA 7 generation
- [ ] **OUT-002** APA 7 validation
- [ ] **OUT-003** BibTeX export
- [ ] **OUT-004** RIS export
- [ ] **OUT-005** EndNote-compatible export
- [ ] **OUT-006** Zotero-compatible export
- [ ] **OUT-007** Mendeley-compatible export
- [ ] **OUT-008** Duplicate bibliography check
- [ ] **OUT-009** Missing author detection
- [ ] **OUT-010** Missing year detection
- [ ] **OUT-011** Missing journal detection
- [ ] **OUT-012** Broken DOI detection

### Thesis Writing Assistance

- [ ] **OUT-013** Bab II literature table
- [ ] **OUT-014** State-of-the-art table
- [ ] **OUT-015** Comparison table
- [ ] **OUT-016** Research-gap narrative
- [ ] **OUT-017** Novelty mapping
- [ ] **OUT-018** Conceptual-framework mapping
- [ ] **OUT-019** Method justification
- [ ] **OUT-020** Citation suggestions
- [ ] **OUT-021** Claim-source mapping
- [ ] **OUT-022** Literature synthesis
- [ ] **OUT-023** Contradiction detection
- [ ] **OUT-024** Evidence-supported paragraph generation

### Visualization

- [ ] **OUT-025** Publication-year chart
- [ ] **OUT-026** Document-type chart
- [ ] **OUT-027** Journal landscape
- [ ] **OUT-028** Country map
- [ ] **OUT-029** Author network
- [ ] **OUT-030** Keyword network
- [ ] **OUT-031** Topic cluster visualization
- [ ] **OUT-032** Method coverage chart
- [ ] **OUT-033** Research-gap chart
- [ ] **OUT-034** Thesis-alignment chart
- [ ] **OUT-035** PRISMA diagram
- [ ] **OUT-036** Evidence-level chart

### Word / PDF Report

- [ ] **OUT-037** Cover/title
- [ ] **OUT-038** Executive summary
- [ ] **OUT-039** Search strategy
- [ ] **OUT-040** Database/source list
- [ ] **OUT-041** Query list
- [ ] **OUT-042** Inclusion/exclusion criteria
- [ ] **OUT-043** PRISMA section
- [ ] **OUT-044** Dataset statistics
- [ ] **OUT-045** DOI audit
- [ ] **OUT-046** Scopus audit
- [ ] **OUT-047** Q1 audit
- [ ] **OUT-048** Journal analysis
- [ ] **OUT-049** Methodology matrix
- [ ] **OUT-050** Research-gap matrix
- [ ] **OUT-051** Evidence matrix
- [ ] **OUT-052** Thesis alignment section
- [ ] **OUT-053** Candidate literature
- [ ] **OUT-054** Bibliography
- [ ] **OUT-055** Limitations
- [ ] **OUT-056** Reproducibility appendix
- [ ] **OUT-057** Audit trail appendix

### Export & Packaging

- [ ] **OUT-058** CSV export
- [ ] **OUT-059** Excel export
- [ ] **OUT-060** Markdown report
- [ ] **OUT-061** TXT summary
- [ ] **OUT-062** JSON export
- [ ] **OUT-063** Word report
- [ ] **OUT-064** PDF report
- [ ] **OUT-065** BibTeX
- [ ] **OUT-066** RIS
- [ ] **OUT-067** ZIP package
- [ ] **OUT-068** Desktop packaging
- [ ] **OUT-069** Manifest file
- [ ] **OUT-070** File checksum manifest

---

## PHASE 7 — REPRODUCIBILITY, TESTING & SECURITY

### Reproducibility

- [ ] **REPRO-001** Python version recording
- [ ] **REPRO-002** Package version recording
- [ ] **REPRO-003** Requirements lock
- [ ] **REPRO-004** Git version
- [ ] **REPRO-005** Git commit hash
- [ ] **REPRO-006** Dataset SHA/hash
- [ ] **REPRO-007** Input hash
- [ ] **REPRO-008** Output hash
- [ ] **REPRO-009** Configuration snapshot
- [ ] **REPRO-010** Query snapshot
- [ ] **REPRO-011** API-source snapshot
- [ ] **REPRO-012** Execution timestamp
- [ ] **REPRO-013** Re-run capability
- [ ] **REPRO-014** Resume capability

### Testing

- [ ] **REPRO-015** Unit tests
- [ ] **REPRO-016** Integration tests
- [ ] **REPRO-017** Schema tests
- [ ] **REPRO-018** Data validation tests

### Security & Robustness

- [ ] **REPRO-019** API key environment variables
- [ ] **REPRO-020** No secrets in CSV
- [ ] **REPRO-021** No secrets in logs
- [ ] **REPRO-022** Input sanitization
- [ ] **REPRO-023** Path validation
- [ ] **REPRO-024** Safe file naming
- [ ] **REPRO-025** Temporary-file cleanup
- [ ] **REPRO-026** Network timeout
- [ ] **REPRO-027** Rate-limit protection
- [ ] **REPRO-028** Corrupt-file handling

### Evidence Traceability

- [ ] **REPRO-029** Claim ID
- [ ] **REPRO-030** Paper ID
- [ ] **REPRO-031** Source URL
- [ ] **REPRO-032** Source type
- [ ] **REPRO-033** Page number
- [ ] **REPRO-034** Section
- [ ] **REPRO-035** Supporting passage
- [ ] **REPRO-036** Evidence confidence
- [ ] **REPRO-037** Claim-to-paper mapping
- [ ] **REPRO-038** Claim-to-source mapping
- [ ] **REPRO-039** Audit trail

---

## PHASE 8 — STREAMLIT RESEARCH PLATFORM

### Dashboard

- [ ] **PLAT-001** Dashboard
- [ ] **PLAT-002** Search interface
- [ ] **PLAT-003** Filter by year
- [ ] **PLAT-004** Filter by document type
- [ ] **PLAT-005** Filter by DOI status
- [ ] **PLAT-006** Filter by Scopus status
- [ ] **PLAT-007** Filter by Q1 status
- [ ] **PLAT-008** Filter by methodology
- [ ] **PLAT-009** Filter by topic
- [ ] **PLAT-010** Paper detail page
- [ ] **PLAT-011** Evidence page
- [ ] **PLAT-012** Research-gap page
- [ ] **PLAT-013** Thesis-alignment page

### Data & Download

- [ ] **PLAT-014** Download CSV
- [ ] **PLAT-015** Download Excel
- [ ] **PLAT-016** Download Word
- [ ] **PLAT-017** Download ZIP

### Final QA Gate

- [ ] **QA-001** Semua CSV dapat dibaca pandas
- [ ] **QA-002** Tidak ada CSV kosong
- [ ] **QA-003** Master dataset konsisten
- [ ] **QA-004** DOI tidak mengarang
- [ ] **QA-005** DOI syntax tervalidasi
- [ ] **QA-006** DOI duplicate diaudit
- [ ] **QA-007** Publication year aman
- [ ] **QA-008** UNVERIFIED aman
- [ ] **QA-009** Scopus tidak diada-adakan
- [ ] **QA-010** Q1 tidak diada-adakan
- [ ] **QA-011** Retraction check
- [ ] **QA-012** Full-text status
- [ ] **QA-013** Methodology evidence
- [ ] **QA-014** Research-gap evidence
- [ ] **QA-015** PRISMA angka konsisten
- [ ] **QA-016** APA 7 valid
- [ ] **QA-017** Word bisa dibuka
- [ ] **QA-018** PDF bisa dibuka
- [ ] **QA-019** ZIP testzip() = None
- [ ] **QA-020** Semua path valid
- [ ] **QA-021** Semua file > 0 bytes
- [ ] **QA-022** Manifest tersedia
- [ ] **QA-023** Checksum tersedia
- [ ] **QA-024** Reproducibility metadata tersedia
- [ ] **QA-025** Clean error log
- [ ] **QA-026** Final audit PASS

---

## Task Count Summary

| Phase | Prefix  | Count |
|-------|---------|-------|
| 1 – Data Foundation             | DATA    | 30  |
| 2 – Verification                | VER     | 44  |
| 3 – Full-Text Intelligence      | FTX     | 45  |
| 4 – Research Synthesis          | SYN     | 62  |
| 5 – Thesis Alignment            | THESIS  | 74  |
| 6 – Academic Output             | OUT     | 70  |
| 7 – Reproducibility             | REPRO   | 39  |
| 8 – Platform + QA               | PLAT/QA | 43  |
| **Total**                       |         | **407** |

> Note: Final count is 407 unique task IDs after breaking the 392-item
> high-level list into individually trackable subtasks.

---

## GitHub Issues Integration

Each task ID maps directly to a GitHub Issue label:

```
DATA-001  →  label: phase-1, area: data-foundation
VER-022   →  label: phase-2, area: scopus-verification
THESIS-030 → label: phase-5, area: inter-annotator-agreement
QA-026    →  label: phase-8, area: final-qa-gate
```

Automate with:

```bash
gh issue create --title "DATA-001: Discovery literature" \
  --label "phase-1,area:data-foundation" \
  --body "Implement initial literature discovery via OpenAlex API."
```
