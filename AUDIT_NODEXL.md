# AUDIT NODEXL — Tesis Magister Ilmu Komunikasi
## Indri Anjar Kartika Sari — MBG (Makan Bergizi Gratis) Social Network Analysis

> **Tanggal Audit:** 22 September 2026  
> **Repository:** [INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA](https://github.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA)  
> **Paradigma Riset:** Computational Social Science (CNA × IndoBERT 9 Emosi)  
> **Teori Utama:** Situational Crisis Communication Theory & Phygital Gap (Kotler)

---

## 1. Inventaris File NodeXL

| File | Ukuran | Deskripsi |
|------|--------|-----------|
| `NodeXL_MBG_Tesis_Indri_Anjar.xlsx` | 81.6 KB | **Workbook Utama Tesis** — sudah diperkaya penuh (centrality + emotion + community) |
| `NodeXL_Scraped_Tweets_MBG.xlsx` | 397 KB | **Raw Scrape Export** — data mentah dengan tweet text, lebih besar, kurang terstruktur |

> [!NOTE]
> File yang sama tersedia rangkap di `/results/` — salinan, bukan versi berbeda.

---

## 2. Struktur Sheet NodeXL

Kedua file memiliki 4 sheet standar NodeXL:

### Sheet A: `Edges`
| | `NodeXL_MBG_Tesis_Indri_Anjar.xlsx` | `NodeXL_Scraped_Tweets_MBG.xlsx` |
|--|--|--|
| **Jumlah Baris** | 692 edges (693 rows − 1 header) | 726 edges |
| **Kolom** | `Vertex 1`, `Vertex 2`, `Color`, `Width`, `Style`, `Opacity`, `Relationship` | `Vertex 1`, `Vertex 2`, `Relationship`, `Tweet`, `Color`, `Width`, `Style`, `Opacity` |
| **Vertex 1** | ✅ Username akun pengirim (bersih) | ⚠️ Mengandung noise: `"username    ayyubi1127108\nusername "` |
| **Vertex 2** | ✅ Username akun penerima (bersih) | ✅ Relatif bersih |
| **Edge Weight** | ❌ Tidak ada kolom bobot eksplisit | ❌ Tidak ada kolom bobot eksplisit |
| **Relationship** | `"Mention / Retweet"` | `"Mention"` |
| **Tweet Text** | ❌ Tidak ada | ✅ Ada di kolom `Tweet` (terpotong) |
| **Timestamp** | ❌ Tidak ada | ❌ Tidak ada |
| **Contoh Baris** | `ayyubi1127108 → Sekjebn` | `ayyubi1127108 → sekjebn (Mention)` |

> [!IMPORTANT]
> **Edge Weight** tidak terdapat sebagai kolom terpisah di kedua file. Relasi diperlakukan sebagai **unweighted** (biner). Bobot implisit dapat dihitung dari frekuensi pasangan (Vertex 1, Vertex 2) yang muncul berulang.

---

### Sheet B: `Vertices`
| Kolom | `NodeXL_MBG_Tesis_Indri_Anjar.xlsx` | `NodeXL_Scraped_Tweets_MBG.xlsx` |
|-------|--------------------------------------|----------------------------------|
| **Vertex / Id Akun** | `Vertex` (username bersih) | `Vertex` (⚠️ mengandung noise multiline) |
| **Label** | `Label` = `@username` | `Label` (⚠️ noise sama) |
| **Warna Node** | `Color` (hex, e.g. `#E53935`) | `Color` |
| **Bentuk Node** | `Shape` = `Disk` | `Shape` = `Disk` |
| **Ukuran Node** | `Size` = `4` | `Size` = `4` |
| **Transparansi** | `Alpha` = `90` | `Alpha` = `90` |
| **Community** | ✅ `Community` (integer ID Louvain) | ❌ Tidak ada |
| **Degree Centrality** | ✅ `Degree Centrality` (normalized) | ✅ `Degree Centrality` |
| **Betweenness Centrality** | ✅ `Betweenness Centrality` | ❌ Tidak ada |
| **Emosi (IndoBERT)** | ✅ `Dominant Emotion (IndoBERT)` | ✅ `Dominant Emotion` |
| **Sentiment** | ❌ Tidak ada kolom terpisah | ❌ Tidak ada |
| **Jumlah Vertices** | **971** akun unik | **5.670** akun unik |

**Nilai emosi yang ditemukan** (dari `Dominant Emotion (IndoBERT)`):
- `disgust` — 56.24% (emosi dominan keseluruhan)
- `neutral`

> [!NOTE]
> Meski pipeline IndoBERT dilatih dengan **9 label emosi** (`anger`, `disgust`, `fear`, `joy`, `love`, `neutral`, `sadness`, `shame`, `surprise`), yang muncul dominan di workbook NodeXL hanya `disgust` dan `neutral`. Label lain muncul di data CSV terperinci.

---

### Sheet C: `Groups` (Community Detection)

**`NodeXL_MBG_Tesis_Indri_Anjar.xlsx`** — 10 komunitas teratas:

| Community ID | Vertex Count | Label Tema Wacana |
|:---:|:---:|:---|
| 15 | 46 | Cluster 15: Political & Policy Central Hub (`@prabowo`, `@regar_op0sisi`) |
| 61 | 43 | Cluster 16: Citizen Sarcasm & Viral Criticism (`@4Y4NKZ`, `@newIding30`) |
| 16 | 18 | Cluster 8: Public Budget & Fiscal Scrutiny (`@Casagrande10939`) |
| 259 | 14 | Cluster 3: School Logistics & Nutrition Complaints |
| 8 | 11 | Cluster 259: Regional Distribution Queries |
| 264 | 10 | Cluster 61: Algorithmic Verification Stream (`@grok`) |
| 313 | 9 | Cluster 264: Sarcastic Meme Amplification |
| 9 | 8 | Cluster 313: Student & Parent Commentary |
| 56 | 8 | Cluster 7: Health & Dietitian Perspective |
| 334 | 7 | Cluster 0: Grassroots Citizen Feedbacks |

**`NodeXL_Scraped_Tweets_MBG.xlsx`** — 3 kelompok ringkasan:

| Cluster | Fokus |
|:---:|:---|
| Group 1 | Policy Targets & Official Institutions (`@prabowo`, dll.) |
| Group 2 | Algorithmic Oracle & Fact Checking Streams (`@grok`) |
| Group 3 | Citizen Critique & Food Quality Scrutiny (Disgust Stream) |

---

### Sheet D: `Overall Metrics`

**`NodeXL_MBG_Tesis_Indri_Anjar.xlsx`** (Workbook Tesis Utama):

| Metrik Jaringan | Nilai |
|:---|:---|
| Graph Type | Directed (Graf Berarah) |
| Total Vertices (Akun) | **971** |
| Total Unique Edges (Relasi) | **692** |
| Graph Density | 0.000708 |
| Connected Components (WCC) | **341** |
| Louvain Modularity (Q) | **0.9837** *(Hiper-Terfragmentasi)* |
| Dominant Community | Community 15 (Political Policy Hub, n=89) |
| Top In-Degree Hub | `@prabowo` (15) |
| Top Out-Degree Hub | `@grok` (42) |
| Top Betweenness Broker | `@regar_op0sisi` (0.004564) |
| Dominant Affective Sentiment | **Disgust (56.24%)** |
| Verified Sarcasm Ratio | 9.28% (315 / 3.395 cuitan) |
| Primary Theory | SCCT & Phygital Gap (Kotler) |
| Research Paradigm | Computational Social Science (CNA × IndoBERT 9 Emotions) |

**`NodeXL_Scraped_Tweets_MBG.xlsx`**:

| Metrik Jaringan | Nilai |
|:---|:---|
| Graph Type | Directed (Media Sosial X) |
| Total Vertices (Akun) | **5.670** |
| Total Edges (Interaksi) | **726** |
| Top Active Accounts | `@lambesahamjja`, `@tanyarlfes`, `@regar_op0sisi`, `@prabowo` |
| Disgust / Critique Accounts | 77 |
| Neutral Accounts | 5.470 |
| Export Engine | Antigravity NodeXL Automation Bridge (Python) |

---

## 3. Metrik Jaringan yang Sudah Dihitung

Sumber: `results/macro_topology_metrics.json`

| Dimensi Analisis | Metrik | Nilai |
|:---|:---|:---|
| **Ukuran Jaringan** | Total Vertices `|V|` | 971 |
| | Total Edges `|E|` | 692 |
| | Unique Directed Edges | 666 |
| | Self-Loops | 17 |
| **Topologi** | Graph Density (Directed) | 0.000707 |
| | Graph Density (Undirected) | 0.001406 |
| | Weakly Connected Components (WCC) | 341 |
| | Strongly Connected Components (SCC) | 967 |
| | Giant Component Size | 89 simpul (9.17%) |
| | Network Diameter | 9 |
| | Average Geodesic Distance | 3.6731 |
| | Average Clustering Coefficient | 0.0171 |
| | Transitivity (Triadic Closure) | 0.0261 |
| **Fragmentasi** | Louvain Modularity (Q) | **0.9837** |
| | Degree Assortativity (r) | −0.0847 (disassortatif) |
| | Reciprocity | 0.0120 (1.20%) |
| **Derajat** | Average Degree | 1.37 |
| | Median Degree | 1.0 |
| | Maximum Degree | 42 (`@grok`) |
| | Power-Law Exponent (Alpha) | 2.168 |

---

## 4. Centrality & Tipologi Aktor

Sumber: `results/actor_centrality_typology.csv` (971 baris)

### 4.1 Kolom Tersedia

| Kolom | Keterangan |
|:---|:---|
| `Id` | Username akun (tanpa @) |
| `Label` | Username dengan awalan @ |
| `Community` | ID komunitas Louvain |
| `Dominant_Emotion` | Emosi dominan (IndoBERT) |
| `In_Degree` | Jumlah koneksi masuk |
| `Out_Degree` | Jumlah koneksi keluar |
| `Total_Degree` | Derajat total |
| `Normalized_Degree` | Degree centrality ternormalisasi |
| `Betweenness_Centrality` | Sentralitas perantara |
| `PageRank` | Skor PageRank (α=0.85) |
| `Closeness_Centrality` | Sentralitas kedekatan |
| `Communication_Role` | Tipologi peran komunikasi |

### 4.2 Tipologi Peran Komunikasi (6 Kategori)

| Tipologi | Kriteria | Contoh Akun |
|:---|:---|:---|
| **Algorithmic Oracle** | Akun `@grok` (AI Fact-Checker) | `@grok` (Out-Degree 42) |
| **Target Sink (Otoritas Kebijakan)** | Label spesifik pemerintah | `@prabowo` (In-Degree 15) |
| **Target Sink (Rujukan Keluhan)** | In-Degree ≥ 3, Out-Degree = 0 | Institusi/media |
| **Opinion Broker** | Betweenness ≥ 0.0015 | `@regar_op0sisi` (BW: 0.004564) |
| **Information Broadcaster** | Out-Degree ≥ 3, In-Degree ≤ 1 | Akun oposisi aktif |
| **Secondary Influencer** | Total Degree ≥ 2 | Akun penggerak wacana |
| **Peripheral Citizen** | Total Degree = 1 | Mayoritas akun biasa |

---

## 5. Community Detection

Sumber: `results/community_echo_chambers.json`

| Parameter | Nilai |
|:---|:---|
| **Algoritma** | Louvain Modularity Optimization (Blondel et al., 2008) |
| **Skor Modularitas (Q)** | **0.9837** (Ambang batas polarisasi: Q > 0.30) |
| **Total Komunitas** | **342** kelompok wacana independen |
| **Tepi Internal** | 691 / 692 (**99.86%**) |
| **Tepi Eksternal (Bridge)** | 1 / 692 (**0.14%**) |

> [!WARNING]
> Rasio isolasi 99.86% mengindikasikan **hiper-fragmentasi ekstrem** — hampir tidak ada dialog lintas komunitas. Ini merupakan temuan utama penelitian.

### Top 6 Komunitas dengan Distribusi Emosi

| Klaster | Nama Wacana | Aktor | Emosi Dominan | Tokoh Kunci |
|:---:|:---|:---:|:---:|:---|
| #15 | Klaster Elit & Target Otoritas | 46 (4.74%) | **DISGUST** (27/46) | `@prabowo`, `@regar_op0sisi` |
| #61 | Klaster AI Fact-Checking Oracle | 43 (4.43%) | **NEUTRAL** (36/43) | `@grok`, `@unmagnetism` |
| #16 | Klaster Diskursus #16 | 18 (1.85%) | **NEUTRAL** (15/18) | `@4Y4NKZ`, `@newIding30` |
| #259 | Klaster Diskursus #259 | 14 (1.44%) | **NEUTRAL** (13/14) | `@dbdbidip`, `@greeniefloo` |
| #8 | Klaster Diskursus #8 | 11 (1.13%) | **NEUTRAL** (10/11) | `@Casagrande10939` |
| #264 | Klaster Diskursus #264 | 10 (1.03%) | **NEUTRAL** (9/10) | `@luvdysh_`, `@helloyosh_` |

### Arketipe Jaringan (Pew Research Typology)

| Arketipe | Skor Kesesuaian | Status |
|:---|:---:|:---|
| Community Clusters | **96.8%** | PALING COCOK — 342 klaster mandiri terisolasi |
| Polarized Crowd | **94.5%** | SANGAT COCOK — Kubu elit vs oposisi sarkasme |
| Broadcast Network | **88.0%** | COCOK — `@prabowo` (sink) & `@grok` (oracle) |
| Brand Clusters | 65.0% | CUKUP COCOK |
| Support Network | 42.0% | KURANG COCOK |
| Tight Crowd | 5.2% | TIDAK COCOK |

---

## 6. Pipeline Klasifikasi Emosi (IndoBERT 9 Label)

```
Raw Tweet Data (mbg_tweets_indobert_ready.xlsx)
    ↓
[Preprocessing] Lowercase + hapus URL + hapus mention + Sastrawi Stemmer
    ↓
[Tokenizer] indobenchmark/indobert-base-p2 (max_length=128)
    ↓
[Model] IndoBERT Fine-tuned (9 label emosi)
        Checkpoint: results/indobert_finetuned_9_labels/checkpoint-792
        Training: 3 epoch, batch_size=16, weight_decay=0.01
    ↓
[Output] predicted_emotion per tweet
    ↓
[Agregasi] mode() per author_username → Dominant_Emotion per akun
    ↓
[SNA] NetworkX DiGraph + Louvain Community Detection
    ↓
[Export] mbg_network_nodes_final.csv + mbg_network_edges_final.csv
    ↓
[NodeXL Export] NodeXL_MBG_Tesis_Indri_Anjar.xlsx
```

### 9 Label Emosi yang Dilatih

| # | Label | Keterangan |
|:---:|:---|:---|
| 0 | `anger` | Kemarahan |
| 1 | `disgust` | Jijik/Kekecewaan — **DOMINAN (56.24%)** |
| 2 | `fear` | Ketakutan |
| 3 | `joy` | Kegembiraan |
| 4 | `love` | Kasih sayang |
| 5 | `neutral` | Netral |
| 6 | `sadness` | Kesedihan |
| 7 | `shame` | Malu |
| 8 | `surprise` | Kejutan |

---

## 7. Pemetaan Hubungan Data: Tweet → Actor → Edge → Emotion → Community

| Entitas | File Sumber | Kolom Kunci | Terhubung ke |
|:---|:---|:---|:---|
| **Tweet** | `mbg_tweets_indobert_ready.xlsx` | `text`, `author_username` | Actor via `author_username` |
| **Actor / Vertex** | `NodeXL_MBG_Tesis_Indri_Anjar.xlsx` → Sheet Vertices | `Vertex` = username | Edge via Vertex 1/2; Community via `Community` ID |
| **Edge** | Sheet Edges | `Vertex 1` → `Vertex 2` | Relationship = "Mention/Retweet" |
| **Emotion** | Sheet Vertices | `Dominant Emotion (IndoBERT)` | Actor; Community via agregasi mode() |
| **Community** | Sheet Groups | `Community ID` | Actor via `Community` kolom di Vertices |
| **Network Metric** | Sheet Overall Metrics | Key-Value | Global summary |
| **Centrality Detail** | `actor_centrality_typology.csv` | `Id`, `Betweenness_Centrality`, `PageRank` | Actor via `Id` = username |

---

## 8. Inventaris Script Python SNA

| Script | Fungsi | Input | Output |
|:---|:---|:---|:---|
| `scripts/sna.py` | **Pipeline Utama**: Inferensi IndoBERT + Graf + Louvain | `mbg_tweets_indobert_ready.xlsx` | `mbg_network_nodes_final.csv`, `mbg_network_edges_final.csv` |
| `scripts/train_indobert.py` | Fine-tuning IndoBERT 9 label | `indobert_9_emosi_fixed.csv` | `indobert_finetuned_9_labels/` |
| `scripts/compute_actor_centrality_typology.py` | Hitung In/Out Degree, Betweenness, PageRank, Closeness | CSVs | `actor_centrality_typology.csv`, `actor_centrality_top15.json` |
| `scripts/compute_community_echo_chambers.py` | Louvain community + echo chamber analysis | CSVs | `community_echo_chambers.json`, `.md` |
| `scripts/compute_macro_topology_metrics.py` | Metrik topologi makro (22 metrik) | CSVs | `macro_topology_metrics.json` |
| `scripts/compute_network_archetypes.py` | Pew Research archetype scoring | CSVs | `network_archetypes_pew.json` |
| `scripts/export_nodexl_workbook.py` | Export ke format NodeXL workbook | CSVs + JSONs | `NodeXL_MBG_Tesis_Indri_Anjar.xlsx` |

---

## 9. Kesimpulan Audit

Workbook **`NodeXL_MBG_Tesis_Indri_Anjar.xlsx`** adalah **sumber data tesis utama** dengan struktur lengkap:

| ✅ Tersedia | ❌ Tidak Tersedia |
|:---|:---|
| Vertex 1 (pengirim) | Edge Weight eksplisit |
| Vertex 2 (penerima) | Timestamp / waktu interaksi |
| Relationship (Mention/Retweet) | Sentiment label terpisah |
| Community ID (Louvain, 342 klaster) | Tweet text penuh di Edges |
| Degree Centrality (normalized) | Closeness Centrality (di NodeXL langsung) |
| Betweenness Centrality | PageRank (di NodeXL langsung) |
| Dominant Emotion (disgust / neutral) | 7 label emosi lainnya di NodeXL |
| 10 komunitas teridentifikasi di Groups | Dialog lintas komunitas (hanya 1 bridge edge) |
| Overall Metrics (15 metrik ringkasan) | |

**Pipeline analisis berjalan penuh dan konsisten** dari scraping Twitter → IndoBERT classification → NetworkX SNA → Louvain community detection → NodeXL workbook export. Semua output tersimpan di `/results/` dan siap digunakan untuk penulisan tesis.
