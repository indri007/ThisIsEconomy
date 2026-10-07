# 🌐 MBG Communication Network — Cytoscape Graph Explorer

> **Tier 3 Decoupled Web Client**: Modern interactive graph explorer and sentiment dashboard for Indonesia's Free Nutritious Meal Program (MBG) discourse on Platform X.

---

## 🛠️ Tech Stack
- **Framework**: Next.js 16 (App Router) + React 19
- **Graph Canvas**: Cytoscape.js & React-Cytoscapejs
- **Styling**: Tailwind CSS 4 + Material UI Icons
- **Data Visualizations**: Recharts + Axios HTTP Client

---

## 🔌 API Integration
This frontend consumes data from the Tier 2 FastAPI service (`backend/main.py`) running on `http://localhost:8000`:

- `GET /api/sna/summary` — High-level network metrics (nodes, edges, modularity)
- `GET /api/sna/network` — Cytoscape-formatted graph elements (nodes and edges)
- `GET /api/emotion-distribution` — 9-class Plutchik emotion percentages
- `GET /api/sarcasm/summary` — Sarcasm and irony frequency
- `GET /api/sna/communities` — Louvain community clusters and partitions
- `GET /api/absa/summary` — Aspect-Based Sentiment Analysis metrics

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Local Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Production Build
```bash
npm run build
npm run start
```
