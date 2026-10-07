# 🏛️ System Architecture Specification: Multi-Tier Research Monorepo

**Repository**: `indri007/ThisIsEconomy`  
**Research Focus**: Communication Network Analysis (CNA) of Sarcasm in MBG Discourse  
**Author**: Indri Anjar Kartika Sari (UPN "Veteran" Jawa Timur)  

---

## 1. Architectural Philosophy

This repository is structured as a **Polyglot Research Monorepo**. It unites empirical academic research (Social Network Analysis, Fine-tuned IndoBERT, and Ground-Truth Corpera) with four synchronized operational software tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TIER 1: PRIMARY PRODUCTION                       │
│      Streamlit Research Analytics Engine (`dashboard/`)                │
│    • Public Cloud Live: https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/   │
│    • Scope: Thesis Chapters I-V, PyVis Graphs, EWS, Scopus Audit       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Shared Data & Result Models
        ┌───────────────────────────┴───────────────────────────┐
        ▼                                                       ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│     TIER 2: HEADLESS REST API   │   │  TIER 4: SCRAPING & AUTOMATION  │
│       FastAPI (`backend/`)      │   │  Twikit + Gemini (`ews/`, bot)  │
│  • Port: 8000                   │   │  • Cron: 07:00 & 19:00 WIB      │
│  • Endpoints: SNA, ABSA, Emotion│   │  • Output: Telegram EWS Alerts  │
└────────────────┬────────────────┘   └─────────────────────────────────┘
                 │ REST / JSON
                 ▼
┌─────────────────────────────────┐
│  TIER 3: GRAPH EXPLORER CLIENT  │
│   Next.js + Cytoscape (`frontend`)
│  • Port: 3000                   │
│  • Canvas: Interactive Cytoscape│
└─────────────────────────────────┘
```

---

## 2. Subsystems & Component Responsibilities

| Subsystem | Directory | Tech Stack | Role & Responsibility | Default Port |
| :--- | :--- | :--- | :--- | :---: |
| **Tier 1: Research Dashboard** | [`dashboard/`](dashboard/) | Python 3.12, Streamlit, NetworkX, Plotly, PyVis | **Canonical user-facing interface.** Hosts full academic thesis walkthrough (Bab I–V), empirical evaluation, and EWS console. Deployed to Streamlit Cloud. | `8501` |
| **Tier 2: Headless Data API** | [`backend/`](backend/) | FastAPI, Uvicorn, Pandas, NetworkX | **Service-oriented data gateway.** Exposes normalized JSON endpoints (`/api/sna/*`, `/api/emotion-distribution`, `/api/absa/summary`) for external consumption. | `8000` |
| **Tier 3: Graph Web Client** | [`frontend/`](frontend/) | Next.js 16, React 19, TypeScript, Cytoscape.js, Tailwind 4 | **Decoupled web visualization.** Renders client-side graph topologies and emotion dashboards via Cytoscape canvas querying Tier 2 API. | `3000` |
| **Tier 4: Ingestion & EWS** | [`twitter_sentiment_app/`](twitter_sentiment_app/), [`ews/`](ews/) | Twikit, Google Gemini 2.5 Flash, Telegram Bot API | **Automated telemetry.** Scheduled scraping job running twice daily to evaluate public crisis risk and push HTML-formatted alerts to Telegram. | Standalone CLI / Cron |

---

## 3. Directory Layout & Boundary Rules

```text
├── dashboard/                  # Tier 1: Streamlit Research Platform
│   ├── app.py                  # Streamlined entrypoint coordinator (<100 LOC)
│   ├── requirements.txt        # Isolated dashboard runtime dependencies
│   └── modules/                # Domain-driven view and data modules
│       ├── config.py           # Path resolvers, CSS styles & download buttons
│       ├── data_loader.py      # LRU-cached dataset & metrics loaders
│       ├── ui_components.py    # Stepper, 70-point checklist & author bio
│       ├── views_bab1.py       # Chapter I: Introduction & 6 Research Questions
│       ├── views_bab2.py       # Chapter II: Theoretical Framework & Sunburst
│       ├── views_bab3.py       # Chapter III: Computational Methodology
│       ├── views_bab4.py       # Chapter IV: Empirical Findings, CNA & IndoBERT
│       ├── views_bab5.py       # Chapter V: Conclusions & Policy Recommendations
│       ├── views_ews.py        # Early Warning System, Brand24 & Twitter AI
│       ├── views_storytelling.py # 10 Master Storytelling Visual Plots
│       └── views_audit.py      # Data Integrity Audit & Scopus APA 7th Taxonomy
│
├── backend/                    # Tier 2: FastAPI Microservice
│   ├── main.py                 # FastAPI app routing & CORS middleware
│   ├── requirements.txt        # Backend dependencies
│   └── services/               # Modular REST data providers
│       ├── sna_service.py      # Node, edge, and density calculators
│       ├── emotion_service.py  # 9-class affective distribution
│       ├── sarcasm_service.py  # Sarcasm / irony ratio and linguistic metrics
│       └── absa_service.py     # Aspect-based sentiment analysis data
│
├── frontend/                   # Tier 3: Next.js Cytoscape Client
│   ├── package.json            # Next.js 16 + React 19 dependencies
│   └── src/app/                # App router and Cytoscape canvas views
│
├── twitter_sentiment_app/      # Tier 4: Scraping & Sentiment Subsystem
│   ├── scraper.py              # Twikit session-based Twitter/X fetcher
│   ├── analyzer.py             # Gemini 2.5 Flash batch inference engine
│   └── app.py                  # Standalone monitor console
│
├── ews/                        # Early Warning System Risk Engine
│   ├── config.py               # Crisis threshold definitions & weights
│   ├── anomaly_detector.py     # Z-score & heuristic anomaly algorithms
│   └── ews_engine.py           # Multi-criteria composite risk calculator
│
├── data/                       # Ground-truth verified datasets (CSV, XLSX)
├── results/                    # Validated empirical outputs & 300 DPI figures
├── manuscript/                 # Camera-ready journal papers & thesis documents
└── tests/                      # Automated regression & integrity test suite
```

---

## 4. Execution Guide per Subsystem

### Running Tier 1 (Streamlit Primary Dashboard)
```bash
streamlit run dashboard/app.py
# URL: http://localhost:8501
```

### Running Tier 2 (FastAPI REST Backend)
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
# Swagger Docs: http://localhost:8000/docs
```

### Running Tier 3 (Next.js Graph Explorer)
```bash
cd frontend
npm install
npm run dev
# URL: http://localhost:3000
```

### Running Tier 4 (Automated Ingestion & EWS Alert)
```bash
python scripts/auto_scrape_job.py
```

### Running Test Suite
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
