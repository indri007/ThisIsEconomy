<div align="center">

<!-- HERO -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=DECODING%20THE%20EMOTION%20BEHIND%20THE%20NETWORK&fontSize=32&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=SNA%20%C3%97%20IndoBERT%20%C3%97%209%20Emotions%20%C3%97%20Sarcasm%20%C3%97%20ABSA%20%C3%97%20Public%20Discourse&descAlignY=60&descAlign=50"/>

<h2>Social Network Analysis of Sarcasm in MBG Discourse</h2>
<h3><i>Computational analysis of sarcasm, emotions, social networks, and public discourse surrounding Indonesia's<br/>Free Nutritious Meal Program (Makan Bergizi Gratis) on Platform X</i></h3>

<br/>

<!-- BADGES -->
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![IndoBERT](https://img.shields.io/badge/IndoBERT-Fine--tuned-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/indobenchmark/indobert-base-p2)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Platform X](https://img.shields.io/badge/Data_Source-Platform%20X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)
[![NetworkX](https://img.shields.io/badge/SNA-NetworkX-4BA3C7?style=for-the-badge)](https://networkx.org)
[![NLP](https://img.shields.io/badge/NLP-9_Emotion_Classes-DB2777?style=for-the-badge)](notebooks/)
[![ABSA](https://img.shields.io/badge/ABSA-Thematic_Analysis-EAB308?style=for-the-badge)](notebooks/)
[![License: MIT](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)

<br/>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)

</div>

---

## 📊 RESEARCH SNAPSHOT

<div align="center">

<table>
<tr>
<td align="center" width="16%">
<h2>🗣️</h2>
<h1><b>971</b></h1>
<sub>Network Nodes</sub>
</td>
<td align="center" width="16%">
<h2>🔗</h2>
<h1><b>692</b></h1>
<sub>Network Edges</sub>
</td>
<td align="center" width="16%">
<h2>📝</h2>
<h1><b>3,395</b></h1>
<sub>Annotated Corpus</sub>
</td>
<td align="center" width="16%">
<h2>🤖</h2>
<h1><b>5,263</b></h1>
<sub>Inference Corpus</sub>
</td>
<td align="center" width="16%">
<h2>🏘️</h2>
<h1><b>333</b></h1>
<sub>Communities</sub>
</td>
<td align="center" width="16%">
<h2>📐</h2>
<h1><b>0.9837</b></h1>
<sub>Modularity</sub>
</td>
</tr>
</table>

> **Methodological Note:** The 37% sarcasm figure (lexical-based, N=3,395) and 56.2% Disgust classification (IndoBERT, N=5,263) represent a **deliberate multi-layer measurement triangulation** — capturing both the *linguistic structure* and the *emotional valence* of public irony. They are convergent, not contradictory.

</div>

---

## 🧩 RESEARCH QUESTIONS

| # | Question |
|:---:|---|
| 🕸️ | How is public discourse surrounding MBG **structured** on Platform X? |
| 🎯 | Which actors occupy **structurally important positions** in the network? |
| 💬 | What **emotional patterns** characterize the discourse? |
| 😏 | How does **sarcasm manifest** as a rhetorical device in public discussion? |
| 📌 | What **thematic and sentiment patterns** emerge from the discourse? |

---

## 🔬 RESEARCH PIPELINE

```
╔════════════════════════════════════════════════════════════════════╗
║                      🐦 PLATFORM X                                 ║
║             Public Discourse on MBG Policy                         ║
╚══════════════════════════╤═════════════════════════════════════════╝
                           │
              ┌────────────▼────────────┐
              │  📥 DATA COLLECTION     │ Raw crawling · API extract
              │       N = 5,310         │ tweets • Mar–May 2026
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  🧹 DATA CLEANING       │ Bot removal · De-dup
              │       N → 3,395         │ Spam filter · Validation
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  ✂️  TEXT PREPROCESSING  │ Sastrawi · Regex
              │    Normalization         │ Slang handling
              └────────────┬────────────┘
                           │
         ┌─────────────────┼──────────────────┐
         │                 │                   │
┌────────▼────────┐ ┌──────▼──────┐  ┌────────▼────────┐
│ 😏 SARCASM      │ │ 🧠 EMOTION  │  │ 📋 THEMATIC     │
│  DETECTION      │ │CLASSIFIC.   │  │  ANALYSIS       │
│ Lexical-based   │ │ IndoBERT    │  │  ABSA           │
│    ~37%         │ │ 9 Classes   │  │  Aspect-Sent.   │
│ N=3,395         │ │ N=5,263     │  │                 │
└────────┬────────┘ └──────┬──────┘  └────────┬────────┘
         │                 │                   │
         └─────────────────▼───────────────────┘
                           │
              ┌────────────▼────────────┐
              │  🕸️  SOCIAL NETWORK     │ NetworkX · python-louvain
              │     ANALYSIS            │ 971 nodes · 692 edges
              │                         │ Modularity = 0.9837
              └────────────┬────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
   ┌───────▼───────┐ ┌─────▼──────┐ ┌─────▼──────┐
   │ 🏘️ COMMUNITY  │ │🎯 CENTRAL- │ │💬 DISCOURSE│
   │  DETECTION    │ │    ITY     │ │INTERPRET.  │
   │ 333 Louvain   │ │@grok → #1  │ │Phygital Gap│
   │   clusters    │ │Eigenvector │ │            │
   └───────────────┘ └────────────┘ └────────────┘
```

---

## 🎨 9-EMOTION TAXONOMY — SEMANTIC COLOR MAP

<div align="center">

<table>
<tr>
<th>Emotion</th><th>Indonesian</th><th>Color</th><th>HEX</th><th>Distribution</th>
</tr>
<tr><td>😡 <b>Anger</b></td><td>Marah</td><td>🔴</td><td><code>#EF4444</code></td><td>1.0%</td></tr>
<tr><td>😊 <b>Joy</b></td><td>Bahagia/Senang</td><td>🟡</td><td><code>#EAB308</code></td><td>—</td></tr>
<tr><td>😢 <b>Sadness</b></td><td>Sedih</td><td>🔵</td><td><code>#2563EB</code></td><td>0.4%</td></tr>
<tr><td>🔮 <b>Anticipation</b></td><td>Antisipasi/Tertarik</td><td>🟠</td><td><code>#F97316</code></td><td>9.6%</td></tr>
<tr><td>😨 <b>Fear</b></td><td>Takut</td><td>🟣</td><td><code>#7C3AED</code></td><td>0.0%</td></tr>
<tr><td>😐 <b>Neutral</b></td><td>Netral</td><td>⚪</td><td><code>#475569</code></td><td>12.3%</td></tr>
<tr><td>🤝 <b>Trust</b></td><td>Percaya</td><td>🟢</td><td><code>#10B981</code></td><td>20.4%</td></tr>
<tr><td>🤢 <b>Disgust</b></td><td>Jijik</td><td>🟩</td><td><code>#065F46</code></td><td><b>56.2% ← DOMINANT</b></td></tr>
<tr><td>😲 <b>Surprise</b></td><td>Kaget</td><td>🔵</td><td><code>#06B6D4</code></td><td>—</td></tr>
</table>

</div>

---

## 🖼️ 10 VISUAL LENSES INTO THE MBG CONVERSATION

> 🚀 **Interactive dashboard** → [y6cqezpxxq2ftdwb6yvrab.streamlit.app](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)

<table>
<tr>
<td width="50%" valign="top">

### `Figure 01` — Dataset & Pipeline Overview
📍 *Methods §3*
End-to-end pipeline: raw collection (N=5,310) → cleaning → annotated corpus (N=3,395) → full inference corpus (N=5,263)
> **"Strict data quality gates ensure analytical validity."**

---

### `Figure 02` — Nine Emotion Distribution
📍 *Results §4*
Bar chart of 9 emotion classes across 5,263 tweets. **Disgust dominates at 56.2%**, revealing systematic public dissatisfaction.
> **"Jijik bukan anomali — ini adalah sentimen sistemik."**

---

### `Figure 03` — Sarcasm Distribution
📍 *Results §4*
~37% of the annotated corpus (N=3,395) contains sarcastic linguistic markers — irony as a primary rhetorical coping mechanism.
> **"Publik merespons krisis dengan sindiran, bukan argumen logis."**

---

### `Figure 04` — IndoBERT Performance
📍 *Results §4*
Model evaluation: Accuracy · Precision · Recall · Macro-F1 · Weighted-F1. Fine-tuned on 9-class Indonesian emotion taxonomy.
> **"Model validates: AI reads Indonesian irony with high fidelity."**

---

### `Figure 05` — Confusion Matrix
📍 *Results §4*
9×9 heatmap: actual vs. predicted emotion classes. Key finding: minor Anger ↔ Disgust overlap in sarcastic contexts.
> **"Sarcastic anger and disgust share structural linguistic features."**

</td>
<td width="50%" valign="top">

### `Figure 06` — Global Social Network
📍 *Results §4*
971 nodes · 692 edges · No dominant central hub. Network structure reveals **hyper-fragmentation**, not polarization.
> **"Discourse is fragmented into isolated complaint bubbles."**

---

### `Figure 07` — Community Structure
📍 *Results §4*
333 Louvain communities · **Modularity = 0.9837** (extremely high). Public retreats into isolated echo chambers.
> **"Hyper-fragmentation: 333 islands, not 2 camps."**

---

### `Figure 08` — Top Central Actors
📍 *Results §4*
**@grok (AI agent) ranks #1** in Eigenvector Centrality — overtaking political elites and government accounts.
> **"Algorithmic Trust replaces institutional authority."**

---

### `Figure 09` — Emotion × Network Pattern
📍 *Discussion §5*
Cross-analysis: Disgust permeates nearly **all 333 communities** — a systemic emotional pattern, not random individual expression.
> **"Disgust is the connective tissue of the fragmented discourse."**

---

### `Figure 10` — ABSA / Thematic Analysis
📍 *Discussion §5*
Aspect-Based Sentiment: frustration is directed at **logistics & budget execution**, not the policy concept itself.
> **"Policy liked. Execution hated. This is the Phygital Gap."**

</td>
</tr>
</table>

---

## 🏛️ THEORETICAL FRAMEWORK: THE PHYGITAL GAP

```
DIGITAL PROMISE (Government)      vs      PHYSICAL REALITY (Public)
──────────────────────────────            ──────────────────────────────
"Free nutritious meals for all            Logistical failures
 Indonesian school children"              Budget irregularities
                                          Food safety incidents

          │                                         │
          └──────────────────┬──────────────────────┘
                             │
                      ╔══════▼══════╗
                      ║  PHYGITAL   ║   ← Core Theoretical Construct
                      ║    GAP      ║       (Kartajaya & Setiawan, 2023)
                      ╚══════╤══════╝
                             │
                  Public Responds via Platform X:
                  ├─ 🤢 Disgust: 56.2% (IndoBERT)
                  ├─ 😏 Sarcasm: ~37% (lexical)
                  ├─ 🕸️ Hyper-fragmented: M = 0.9837
                  └─ 🤖 @grok as trusted AI authority (#1 Eigenvector)
```

*Theoretical anchors: Kartajaya & Setiawan (2023) · Gelders & Ihlen (2010) · Johnson & Barlow (2021) · Tsai et al. (2026)*

---

## 🛠️ TOOLS & TECHNOLOGIES

### ✅ USED IN RESEARCH

<table>
<tr>
<th>Category</th><th>Tool</th><th>Function</th>
</tr>
<tr>
<td rowspan="2"><b>📥 Data Collection</b></td>
<td><img src="https://img.shields.io/badge/Platform%20X-000000?style=flat-square&logo=x&logoColor=white"/> Platform X</td>
<td>Primary data source — public tweet corpus</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/> Python</td>
<td>API integration & data extraction scripts</td>
</tr>
<tr>
<td rowspan="4"><b>🧹 Data Processing</b></td>
<td><img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white"/> Pandas</td>
<td>Dataframe operations & data cleaning</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/> NumPy</td>
<td>Numerical computation & array ops</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Regex-EF4444?style=flat-square"/> Regex</td>
<td>Pattern-based text cleaning</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Sastrawi-10B981?style=flat-square"/> Sastrawi</td>
<td>Indonesian language stemming</td>
</tr>
<tr>
<td rowspan="4"><b>🧠 NLP & AI</b></td>
<td><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-FFD21E?style=flat-square&logoColor=black"/> Hugging Face</td>
<td>NLP model ecosystem & tokenizers</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/IndoBERT-7C3AED?style=flat-square"/> IndoBERT</td>
<td>Core NLP model — emotion & sarcasm classification</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/> PyTorch</td>
<td>Deep learning framework for fine-tuning</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white"/> Jupyter Notebook</td>
<td>Interactive research notebook</td>
</tr>
<tr>
<td rowspan="2"><b>🕸️ SNA</b></td>
<td><img src="https://img.shields.io/badge/NetworkX-4BA3C7?style=flat-square"/> NetworkX</td>
<td>Graph construction & centrality analysis</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Louvain-06B6D4?style=flat-square"/> Louvain</td>
<td>Community detection algorithm (M=0.9837)</td>
</tr>
<tr>
<td rowspan="4"><b>📊 Visualization</b></td>
<td><img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square"/> Matplotlib</td>
<td>Static research charts & figures</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Seaborn-4C72B0?style=flat-square"/> Seaborn</td>
<td>Statistical visualizations & heatmaps</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white"/> Plotly</td>
<td>Interactive dashboard charts</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/> Streamlit</td>
<td>Research dashboard deployment</td>
</tr>
<tr>
<td rowspan="2"><b>⚙️ Development</b></td>
<td><img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white"/> Git</td>
<td>Version control</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white"/> GitHub</td>
<td>Research repository & reproducibility</td>
</tr>
</table>

### ⚠️ PROPOSED (Not yet implemented)

| Tool | Purpose | Status |
|------|---------|--------|
| Gephi | Advanced network visualization | `Proposed` |
| NodeXL | Excel-based SNA | `Proposed` |

---

## 🧠 METHODOLOGY CARDS

<table>
<tr>
<td align="center" width="33%">

**🧠 IndoBERT**
*Fine-tuned Transformer*

Emotion & sarcasm classification on Indonesian tweets using bidirectional contextual embeddings

</td>
<td align="center" width="33%">

**🕸️ Social Network Analysis**
*NetworkX + Louvain*

971 nodes · 692 edges Network topology & community structure

</td>
<td align="center" width="33%">

**🎯 Centrality Analysis**
*Degree · Betweenness · Eigenvector*

Identifies structurally influential actors — @grok ranks #1

</td>
</tr>
<tr>
<td align="center" width="33%">

**👥 Community Detection**
*Louvain Algorithm*

333 communities · Modularity = 0.9837 Hyper-fragmented discourse structure

</td>
<td align="center" width="33%">

**😊 Emotion Analysis**
*9-Category Taxonomy*

Disgust (56.2%) · Trust (20.4%) · Neutral (12.3%) Anticipation (9.6%) · Anger (1.0%)

</td>
<td align="center" width="33%">

**💬 ABSA / Thematic**
*Aspect-Based Sentiment*

Identifies key discourse aspects: logistics, budget, nutrition, policy trust

</td>
</tr>
</table>

---

## 📂 REPOSITORY STRUCTURE

```
tesis_mbg/
├── 📄 README.md
│
├── 📁 data/
│   ├── raw/                           # Raw Platform X tweets (N=5,310)
│   ├── emotion/
│   │   └── mbg_tweets_indobert_ready.xlsx  # Annotated corpus (N=3,395)
│   ├── sarcasm/
│   │   ├── dataset_sindiran_valid.csv      # Lexical sarcasm labels
│   │   └── tweet_sarkastik_final.csv       # Sarcastic tweets subset
│   ├── sna/
│   │   └── network_edges.csv               # 692 directed edges
│   └── processed/
│       └── data_clean.csv                  # Cleaned corpus
│
├── 📓 notebooks/
│   └── tesis_mbg.ipynb                     # Main research notebook
│
├── 📜 scripts/
│   ├── preprocessing.py                    # Text cleaning & normalization
│   ├── train_indobert.py                   # IndoBERT fine-tuning (PyTorch)
│   ├── evaluate.py                         # F1-Score & Confusion Matrix
│   ├── sna.py                              # Network topology & Louvain
│   └── plot_integrated.py                  # Master visualization (3-panel)
│
├── 📊 results/
│   ├── indobert_9_emosi_fixed.csv          # Final emotion classifications
│   ├── sna_degree.csv                      # Centrality metrics
│   ├── confusion_matrix.png                # Figure 05
│   ├── network_graph.png                   # Figure 07
│   └── integrated_sna_nlp.png              # Master Visual (3-panel)
│
└── 🌐 dashboard/
    └── app.py                              # Streamlit dashboard (5 pages)
```

---

## 📰 MEDIA COVERAGE & PUBLICATIONS

| | Reference |
|:---:|---|
| 📄 | **Sari, I. A. K., Suratnoaji, C., & Widiyarta, A.** (2026). Analisis jaringan sosial dalam isu percakapan MBG di media sosial X. *IPSSJ, 3*(9), 248–257. |
| 📄 | **Sari, I. A. K.** (2026). JobMatchAI: Platform generatif AI pencocokan kerja semantik. *IPSSJ, 3*(9), 333–340. |
| 📺 | Portal **JTV** (2026). *"Lebih dari 37 persen percakapan MBG di X bernada sindiran"* |
| 📰 | **Netral News** (2026). *"Riset UPN Jatim: 37 persen percakapan MBG di X bernada sindiran"* |

---

## 📖 CITATION

```bibtex
@mastersthesis{sari2026mbg,
  author  = {Sari, I. A. K.},
  title   = {Social Network Analysis of Sarcasm in MBG Discourse:
             Decoding Emotion Behind the Network},
  school  = {Universitas Pembangunan Nasional Veteran Jawa Timur},
  year    = {2026},
  type    = {Master's Thesis in Communication Science},
  note    = {SNA · IndoBERT · 9-Emotion Classification · Phygital Gap · Platform X}
}
```

---

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer"/>

*Developed for Master's Thesis · Communication Science / Computational Social Science*
*Universitas Pembangunan Nasional Veteran Jawa Timur · 2026*

**[🚀 Live Dashboard](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/) &nbsp;·&nbsp; [📊 Data](data/) &nbsp;·&nbsp; [📓 Notebook](notebooks/) &nbsp;·&nbsp; [📜 Scripts](scripts/)**

</div>
