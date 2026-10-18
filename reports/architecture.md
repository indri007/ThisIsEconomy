# 🏛️ Monorepo Architecture & Subsystem Specification
**Repository**: `indri007/ThisIsEconomy` / `tesis_mbg`  
**Version**: 2.4.0 (Synchronized Operational Monorepo)  
**Research Focus**: Social Network Analysis & Sarcasm Classification in Indonesia's MBG Discourse  
**Author**: Indri Anjar Kartika Sari (UPN "Veteran" Jawa Timur)  

---

## 1. Architectural Overview & Design Pattern

The repository implements a **Polyglot Monorepo Architecture** designed to balance high-rigor academic reproducibility with real-world public policy surveillance.

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

## 2. Monorepo Tiers & Component Responsibilities

### Tier 1: Primary Research Analytics Engine (`dashboard/`)
* **Technology**: Python 3.12, Streamlit 1.35+, Plotly, NetworkX, PyVis.
* **Role**: The canonical presentation interface for academic examination and public demonstration.
* **Component Breakdown**:
  * `dashboard/app.py`: Central routing orchestrator (< 150 lines) using session state and headless AnyIO event loop guards.
  * `dashboard/modules/views_bab1.py` – `views_bab5.py`: Structured presentation of Thesis Chapters I to V.
  * `dashboard/modules/views_ews.py`: Triangulated early warning telemetry console and social listening fallback.
  * `dashboard/modules/views_storytelling.py`: 10 high-resolution narrative plots.
  * `dashboard/modules/data_loader.py`: In-memory LRU-cached data loading with schema validation.
  * `dashboard/modules/config.py`: Centralized asset path resolution, crash-proof image wrappers, and styling.

### Tier 2: Headless Data API (`backend/`)
* **Technology**: FastAPI, Uvicorn, Pydantic, Pandas.
* **Role**: Headless microservice providing programmatic access to graph and affective metrics.
* **Endpoints**:
  * `GET /api/sna/summary`: Macro network topology metrics ($|V|=971, |E|=666, Q=0.9837$).
  * `GET /api/sna/network`: Complete Cytoscape-compatible node and edge list.
  * `GET /api/emotion-distribution`: 9-class Plutchik emotion distribution.
  * `GET /api/sarcasm/summary`: Sarcasm prevalence ($n=315, 9.28\%$).

### Tier 3: Graph Explorer Client (`frontend/`)
* **Technology**: Next.js 16, React 19, TypeScript, Cytoscape.js, Tailwind CSS v4.
* **Role**: Dedicated high-performance canvas for exploring large-scale social interaction graphs without server-side rendering lag.

### Tier 4: Automated Ingestion & Early Warning Telemetry (`ews/` & `scripts/`)
* **Technology**: Twikit / Twifork, Google Gemini 2.5 Flash, Telegram Bot API.
* **Role**: Autonomous ingestion pipeline executing scheduled monitoring jobs (cron) to detect food safety and policy crises in real time, pushing structured alerts to decision-makers.

---

## 3. Data Flow Architecture & Lineage

The data pipeline connects raw microblogging streams to publication-ready scientific outputs:

```
[ Twitter/X API / Data Lake (30M) ]
                 │
                 ▼
[ Cleaning & Normalization (`pipelines_30m/`) ]
  ├── Sastrawi Morphology Stripping
  └── SHA-256 HMAC AoIR 3.0 Pseudonymization
                 │
                 ▼
[ Multi-Corpus Master Datastores (`data/`) ]
  ├── 30M Data Lake (`tweet_mbg_30juta.csv`)
  ├── Longitudinal Timeline (`N = 9.360`)
  ├── Master 9-Emotion Corpus (`N = 5.272`)
  └── Interaction & Sarcasm Corpus (`N = 3.395`)
                 │
                 ├───────────────────────────┐
                 ▼                           ▼
[ Fine-Tuned IndoBERT Model ]   [ Social Network Topologies ]
  ├── Train Split (4.208)         ├── Louvain Communities (342 clusters)
  └── Holdout Test Split (1.064)  └── Degree / Betweenness Centrality
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
               [ Custom EWS v2 Engine (`ews/`) ]
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
   [ Streamlit Live Dashboard ]    [ Scopus Q1 Manuscripts ]
```

---

## 4. Architectural Invariants & Boundary Rules

1. **Zero Text Leakage**: The holdout evaluation set ($N = 1.064$) is isolated strictly via `GroupShuffleSplit` (`seed=42`) with verified zero text overlap against training partitions.
2. **Crash-Proof Cloud Rendering**: The dashboard must never crash or show unhandled traceback pages when external APIs (Brand24, Twitter) are unavailable; it must silently and gracefully degrade to local cached datasets.
3. **Requirement Equivalence**: `requirements.txt` and `dashboard/requirements.txt` must remain byte-identical to ensure consistent builds across Docker, local venv, and Streamlit Cloud.
4. **Decoupled Business Logic**: Mathematical formulas (EWS scores, Cohen's Kappa, Gini inequality) reside in importable modules (`ews/`, `scripts/utils/`), separate from UI rendering logic.
