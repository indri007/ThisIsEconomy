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

## 📊 RESEARCH SNAPSHOT (GROUND-TRUTH METRICS)

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
<h1><b>666</b></h1>
<sub>Directed Edges (692 Raw)</sub>
</td>
<td align="center" width="16%">
<h2>📝</h2>
<h1><b>3,395</b></h1>
<sub>Validated Sarcasm Corpus</sub>
</td>
<td align="center" width="16%">
<h2>🤖</h2>
<h1><b>5,263</b></h1>
<sub>Inference Corpus</sub>
</td>
<td align="center" width="16%">
<h2>🏘️</h2>
<h1><b>332–341</b></h1>
<sub>Louvain Communities</sub>
</td>
<td align="center" width="16%">
<h2>📐</h2>
<h1><b>0.9837</b></h1>
<sub>Modularity (Hyper-Frag.)</sub>
</td>
</tr>
</table>

> **📌 Catatan Metodologis Triangulasi:** Riset ini menerapkan *multi-layer measurement* yang saling melengkapi:
> 1. **Tingkat Linguistik (N=3.395):** 315 cuitan (**9,28%**) terverifikasi sindiran/sarkasme (*dataset_sindiran_valid.csv*), dengan 181 cuitan (3,44%) leksikon kontradiktif eksplisit.
> 2. **Tingkat Afektif Holistik (N=5.263):** Model IndoBERT mengklasifikasikan **56,24% (2.960 cuitan)** sebagai emosi **Jijik (*Disgust*)**, menangkap spektrum penolakan publik yang lebih luas terhadap eksekusi fisik program.
> 3. **Estimasi Wacana Media Awal:** ~37% percakapan bersindiran (kutipan referensi eksternal media massa).

</div>

---

## 📖 PANDUAN LENGKAP & TUTORIAL REPRODUKSI RISET (END-TO-END TUTORIAL)

Repositori ini dirancang agar dapat direproduksi (*fully reproducible*) dengan mudah oleh penguji tesis, dosen pembimbing, peneliti *computational social science*, maupun praktisi kebijakan publik. Berikut adalah seluruh panduan dan tutorial teknis:

---

### 🚀 TUTORIAL 1: MENJALANKAN DASHBOARD STREAMLIT (LOCAL & CLOUD)

#### Opsi A: Akses Cepat via Cloud (Tanpa Instalasi)
Dashboard telah terdeploy secara publik dan aktif 24/7 di Streamlit Community Cloud:
- 🌐 **URL Cloud:** [https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)

#### Opsi B: Menjalankan di Komputer Lokal (*Localhost*)

1. **Prasyarat Sistem (*System Prerequisites*):**
   - **Python 3.10** atau lebih baru.
   - **Git** terpasang di komputer Anda.
   - RAM disarankan minimal 4 GB.

2. **Langkah 1 — Kloning Repositori dari GitHub:**
   ```bash
   git clone https://github.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA.git
   cd INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA
   ```

3. **Langkah 2 — Menyiapkan Python Virtual Environment (Sangat Disarankan):**
   ```bash
   # Membuat virtual environment bernama .venv
   python3 -m venv .venv

   # Mengaktifkan di macOS / Linux:
   source .venv/bin/activate

   # Mengaktifkan di Windows (PowerShell / Command Prompt):
   # .venv\Scripts\activate
   ```

4. **Langkah 3 — Instalasi Seluruh Dependensi:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   *Dependensi mencakup: `streamlit`, `plotly`, `pandas`, `numpy`, `networkx`, `torch`, `transformers`, `wordcloud`, `matplotlib`, `seaborn`, `pyvis`, `scikit-learn`.*

5. **Langkah 4 — Menjalankan Aplikasi Streamlit:**
   ```bash
   streamlit run dashboard/app.py
   ```
   Peramban web (*browser*) Anda akan otomatis membuka antarmuka dashboard pada:
   - 🌐 **Local URL:** [`http://localhost:8501`](http://localhost:8501)
   - 📡 **Network URL:** `http://<ip-lokal-anda>:8501` *(dapat dibuka dari HP atau tablet dalam satu jaringan Wi-Fi)*

   *Tips:* Jika port 8501 sedang digunakan oleh aplikasi lain, jalankan pada port alternatif:
   ```bash
   streamlit run dashboard/app.py --server.port 8502
   ```

---

### 🧭 TUTORIAL 2: PANDUAN NAVIGASI & EKSPLORASI FITUR DASHBOARD

Dashboard tesis ini memiliki **6 menu utama** yang dapat dipilih melalui panel navigasi sidebar di sebelah kiri:

#### 1. 🏠 Beranda & Sintesis Masterpiece
- **Ringkasan Metrik Ground-Truth:** Memeriksa 6 metrik utama (971 nodes, 666 edges, 3.395 sampel validasi sindiran, 5.263 korpus inferensi, 332 komunitas Louvain, dan skor modularitas $Q = 0.9837$).
- **Rumusan Masalah Utama (Grand RQ):** Menelaah integrasi teori krisis berjejaring (*Networked Crisis Communication*) dan sintesis *Phygital Gap* (Marketing 6.0 Kotler et al.).
- **Word Cloud Interaktif & Top 10 Kata Populer:** Menampilkan leksikon wacana publik teratas bertema gelap modern serta komparasi kata umum vs kata tematik kebijakan MBG (anggaran, gizi, siswa, uji coba, dsb.).

#### 2. 🏛️ Landasan Teori & Pemikiran (Bab II)
- **Peta Interaktif Taksonomi Teori:**
  - **Mode Sunburst Radial:** Klik pada salah satu pilar teori (misal: *2.1 Risiko Fiskal* atau *2.6 SNA & Graf*) untuk melakukan *drill-down* visual ke sub-bab dan nomor halaman tesis. Klik bagian tengah untuk *zoom out*.
  - **Mode Treemap Hierarkis:** Memetakan proporsi luas kajian 37 sub-bab secara proporsional.
- **Eksplorasi 8 Pilar Teori:** Membuka tab teori untuk menelaah landasan teoritis (SCCT Coombs, Schultz et al., Habermas, Devlin et al., Blondel et al., dsb.).
- **Diagram Alur Kausalitas Phygital Gap:** Bagan visual alur stimulus kebijakan fisik ke reaksi siber berjejaring.
- **Validasi 5 Proposisi Riset (P1–P5):** Matriks pengujian empiris hipotesis tesis terhadap bukti data riil.

#### 3. 📊 Eksplorasi Data Mentah
- **Filter Multi-Kriteria:** Filter data cuitan riil ($N=5.263$) berdasarkan kelas emosi, kategori sindiran (sarkas/non-sarkas), serta pencarian kata kunci tertentu.
- **Ekspor Data:** Mengunduh subset data hasil filter ke file CSV untuk audit independen.

#### 4. 😊 Analisis Emosi (NLP) & Leksikal
- **Treemap Distribusi 9 Emosi Plutchik:** Visualisasi dominasi emosi *Disgust* (56,24%), *Anger*, *Joy*, *Trust*, dan lainnya.
- **Analisis Sindiran & Inkongruensi:** Grafik proporsi sindiran warganet (315 cuitan bersindiran valid pada korpus n=3.395).
- **Showcase Kata Sering Muncul:** Visualisasi kata kunci bernilai diagnostik kebijakan.

#### 5. 🕸️ Analisis Jaringan Komunikasi (CNA / SNA)
- **Graf Interaktif PyVis:**
  - Node diwarnai berdasarkan klaster komunitas Louvain riil.
  - Interaksi drag-and-drop, zoom-in/zoom-out, dan hover untuk melihat metrik derajat tiap pengguna.
- **Analisis Tiga Anomali Struktural Kunci:**
  1. `@grok` (AI Oracle Takeover — out-degree=42, mengisi kekosongan komunikasi otoritatif).
  2. `@prabowo` (Power Vacuum — in-degree=68, out-degree=0, sasaran kritik tanpa respons timbal-balik).
  3. `@4Y4NKZ` (Structural Broker — penghubung klaster komunitas terisolasi).
- **Grafik Asimetri Sentralitas:** Komparasi In-Degree vs Out-Degree aktor utama.

#### 6. 🖼️ Visual Storytelling
- **Galeri 10 Visual Resolusi Tinggi:** Menyajikan visualisasi standar publikasi akademik yang membedah data dari tahap pra-proses, performa model IndoBERT, topologi graf jaringan, hingga sintesis master 3-panel.
- **Interpretasi Naratif Akademik:** Penjelasan mendalam dari setiap gambar sebagai basis penulisan artikel jurnal.

#### 7. 📑 Audit Referensi Scopus
- **Matriks Reputasi Literatur:** Audit kepatuhan sitasi terhadap jurnal internasional bereputasi (Q1/Q2 Scopus) dan konfirmasi keselarasan teori di Bab II tesis.

---

### 🧪 TUTORIAL 3: MENJALANKAN SKRIP PIPELINE & EVALUASI MODEL (CLI)

Seluruh komputasi dapat diverifikasi secara mandiri melalui perintah terminal:

```bash
# 1. Menjalankan Evaluasi Kinerja Model IndoBERT
python scripts/evaluate.py
```
*Output yang dihasilkan:*
- Menghitung metrik akurasi, Precision, Recall, Macro F1-Score, dan Weighted F1-Score pada data validasi riil ($n=1.053$).
- Memperbarui file grafik resolusi tinggi: `results/confusion_matrix.png` dan `results/f1_scores.png`.

```bash
# 2. Menghasilkan Master Visual Terintegrasi (3-Panel SNA x NLP x ABSA)
python scripts/plot_integrated.py
```
*Output yang dihasilkan:*
- Menggabungkan topologi graf jaringan Louvain, heatmap emosi per klaster komunitas, dan diagram aspek sentimen ke dalam satu gambar komprehensif: `results/integrated_sna_nlp.png`.

```bash
# 3. Menghasilkan Plot Distribusi Dataset & Word Cloud
python scripts/plot_dataset.py
```
*Output yang dihasilkan:*
- Grafik batang distribusi 9 kelas emosi dan visualisasi kata paling sering muncul ke direktori `results/`.

```bash
# 4. Menjalankan Komputasi Topologi Jaringan & Louvain Community Detection
python scripts/sna.py
```
*Output yang dihasilkan:*
- Menghitung In-Degree, Out-Degree, Betweenness, Closeness, dan partisi komunitas Louvain dengan skor modularitas $Q = 0.9837$.

---

### 📓 TUTORIAL 4: MENJALANKAN REPRODUKSI VIA JUPYTER NOTEBOOK

Bagi peneliti yang ingin memeriksa kode sel demi sel (*step-by-step interactive execution*):

1. **Jalankan Jupyter Notebook di terminal:**
   ```bash
   jupyter notebook notebooks/tesis_mbg.ipynb
   ```
2. **Urutan Eksekusi Sel:**
   - **Bagian 1: Data Ingestion & Preprocessing:** Memuat data mentah cuitan X ($N=5.310$), pembersihan noise, dan penanganan teks slang bahasa Indonesia.
   - **Bagian 2: Deteksi Sindiran & Anotasi Leksikal:** Ekstraksi pola inkongruensi leksikal dan filter kevalidan sindiran ($N=3.395$).
   - **Bagian 3: IndoBERT Fine-Tuning & Inference:** Arsitektur transformer `indobert-base-p2` untuk 9 kelas emosi Plutchik.
   - **Bagian 4: Social Network Analysis (SNA):** Ekstraksi interaksi mention/reply, pemodelan directed graph via NetworkX, deteksi komunitas Louvain, dan metrik sentralitas.
   - **Bagian 5: Visualisasi Terintegrasi:** Plot komparatif multi-dimensi.

---

### 🛠️ TUTORIAL 5: TROUBLESHOOTING & FAQ

- **T: Mengapa visual Sunburst sempat tidak tampil (layar gelap)?**  
  *J:* Pada implementasi awal, parameter `branchvalues='total'` di Plotly Express mewajibkan nilai node induk (*parent*) sama persis secara matematis dengan jumlah anak (*children*). Hal ini telah diperbaiki tuntas dengan menerapkan struktur hierarkis `path=['Pilar', 'SubBab']` yang secara inheren mengkalkulasi proporsi secara otomatis tanpa kendala nilai hierarki.

- **T: Kendala saat instalasi pustaka `wordcloud` di sistem macOS Apple Silicon (M1/M2/M3)?**  
  *J:* Jalankan perintah instalasi tanpa isolasi build atau melalui conda-forge:
  ```bash
  pip install wordcloud --no-build-isolation
  # atau
  conda install -c conda-forge wordcloud
  ```

- **T: Bagaimana memastikan metrik di dashboard 100% konsisten dengan data penelitian tesis?**  
  *J:* Dashboard tidak menggunakan angka statis tiruan (*mock data*). Seluruh visualisasi membaca langsung dari dataset kanonik di direktori `data/` dan `results/` (`indobert_9_emosi_fixed.csv`, `network_edges.csv`, `dataset_sindiran_valid.csv`, dan `sna_degree.csv`).

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

## 🎨 9-EMOTION TAXONOMY — SEMANTIC COLOR MAP & EMPIRICAL DISTRIBUTION

<div align="center">

<table>
<tr>
<th>Emotion (EN)</th><th>Emosi (ID)</th><th>Color</th><th>HEX</th><th>Frekuensi</th><th>Proporsi</th><th>Karakteristik Diskursus</th>
</tr>
<tr><td>🤢 <b>Disgust</b></td><td><b>Jijik</b></td><td>🟩</td><td><code>#065F46</code></td><td><b>2.960</b></td><td><b>56,24%</b></td><td><b>DOMINAN MUTLAK</b> (Penolakan mutu fisik makanan & porsi)</td></tr>
<tr><td>🤝 <b>Trust</b></td><td><b>Percaya</b></td><td>🟢</td><td><code>#10B981</code></td><td><b>1.073</b></td><td><b>20,39%</b></td><td>Dukungan narasi gizi & apresiasi program</td></tr>
<tr><td>😐 <b>Neutral</b></td><td><b>Netral</b></td><td>⚪</td><td><code>#475569</code></td><td><b>649</b></td><td><b>12,33%</b></td><td>Pernyataan berita & kutipan media informatif</td></tr>
<tr><td>🔮 <b>Anticipation</b></td><td><b>Tertarik</b></td><td>🟠</td><td><code>#F97316</code></td><td><b>505</b></td><td><b>9,60%</b></td><td>Ekspektasi & rasa ingin tahu masyarakat</td></tr>
<tr><td>😡 <b>Anger</b></td><td><b>Marah</b></td><td>🔴</td><td><code>#EF4444</code></td><td><b>55</b></td><td><b>1,05%</b></td><td>Kemarahan atas transparansi vendor & korupsi</td></tr>
<tr><td>😢 <b>Sadness</b></td><td><b>Sedih</b></td><td>🔵</td><td><code>#2563EB</code></td><td><b>19</b></td><td><b>0,36%</b></td><td>Empati pada siswa & keprihatinan mutu menu</td></tr>
<tr><td>😨 <b>Fear</b></td><td><b>Takut</b></td><td>🟣</td><td><code>#7C3AED</code></td><td><b>2</b></td><td><b>0,04%</b></td><td>Kekhawatiran atas dampak keracunan massal</td></tr>
<tr><td>😊 <b>Joy</b></td><td><b>Bahagia</b></td><td>🟡</td><td><code>#EAB308</code></td><td><b>0</b></td><td><b>0,00%</b></td><td>—</td></tr>
<tr><td>😲 <b>Surprise</b></td><td><b>Kaget</b></td><td>🔵</td><td><code>#06B6D4</code></td><td><b>0</b></td><td><b>0,00%</b></td><td>—</td></tr>
<tr><td colspan="4" align="right"><b>TOTAL</b></td><td><b>5.263</b></td><td><b>100,00%</b></td><td><i>Korpus Inferensi IndoBERT Terverifikasi</i></td></tr>
</table>

</div>

---

## ☁️ ANALISIS LEKSIKAL: WORD CLOUD & TOP 10 KATA DOMINAN

Selain klasifikasi emosi kalimat penuh dengan IndoBERT, riset ini melakukan **analisis leksikal berbasis frekuensi token** untuk membedakan antara diksi umum kebijakan (*core policy words*) dan isu tematik spesifik di lapangan (*ground-level complaints*).

<div align="center">

<img width="85%" src="results/wordcloud_mbg.png" alt="Word Cloud 120 Kata Paling Signifikan"/>

*Gambar: Visual Word Cloud 120 Kata Kunci Paling Sering Muncul pada Korpus MBG (N=5.263)*

</div>

### 📊 Perbandingan Kata Kunci Umum vs Kata Tematik Lapangan

<table>
<tr>
<th width="50%">🏆 Top 10 Kata Kunci Umum (Core Query)</th>
<th width="50%">🎯 Top 10 Kata Tematik Spesifik (Isu Lapangan)</th>
</tr>
<tr>
<td valign="top">

| Peringkat | Kata Kunci | Frekuensi | Porsi Korpus |
| :---: | :--- | :---: | :---: |
| **#1** | `mbg` | 2.147 | 40,8% |
| **#2** | `makanan` | 1.490 | 28,3% |
| **#3** | `makan` | 1.409 | 26,8% |
| **#4** | `gratis` | 1.200 | 22,8% |
| **#5** | `gizi` | 829 | 15,8% |
| **#6** | `program` | 694 | 13,2% |
| **#7** | `sekolah` | 679 | 12,9% |
| **#8** | `bergizi` | 537 | 10,2% |
| **#9** | `anak` | 442 | 8,4% |
| **#10** | `indonesia` | 297 | 5,6% |

> *Mencerminkan payung formal wacana kebijakan pangan nasional.*

</td>
<td valign="top">

| Peringkat | Kata Tematik | Frekuensi | Konteks Wacana Lapangan |
| :---: | :--- | :---: | :--- |
| **#1** | `sekolah` | 679 | Lokasi penerima manfaat & titik distribusi |
| **#2** | `anak` | 442 | Subjek siswa penerima paket MBG |
| **#3** | `indonesia` | 297 | Cakupan skala nasional program |
| **#4** | `dapur` | 247 | Sentra pengolahan Satuan Pelayanan Gizi |
| **#5** | `terus` | 246 | Kritik atas krisis/isu yang berulang |
| **#6** | `enak` | 228 | Sindiran sarkastis mutu hidangan |
| **#7** | `bikin` | 225 | Keluhan dampak (mual/keracunan) |
| **#8** | `bgt` *(banget)* | 202 | Partikel hiperbola sindiran warganet |
| **#9** | `menu` | 189 | Polemik variasi & pemangkasan lauk |
| **#10** | `anggaran` | 184 | Sorotan pagu Rp15.000 vs realitas menu |

> *Mengungkap titik kritis resistensi: dapur vendor, variasi menu, dan pemangkasan anggaran.*

</td>
</tr>
</table>

---

## 🖼️ 10 VISUAL LENSES INTO THE MBG CONVERSATION

> 🚀 **Interactive dashboard** → [y6cqezpxxq2ftdwb6yvrab.streamlit.app](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)

<table>
<tr>
<td width="50%" valign="top">

### `Figure 01` — Dataset & Pipeline Overview
📍 *Methods §3*
End-to-end pipeline: raw collection (N=5,310) → cleaning → validated sarcasm corpus (N=3,395) → full inference corpus (N=5,263).
> **"Penyaringan data berlapis menjamin integritas dan validitas analitis."**

---

### `Figure 02` — Nine Emotion Distribution
📍 *Results §4*
Diagram batang 9 kelas emosi pada 5.263 cuitan riil. **Jijik mendominasi secara mutlak sebesar 56,24%**, diikuti Percaya (20,39%) dan Netral (12,33%).
> **"Jijik bukan sekadar anomali — ini adalah respons afektif sistemik."**

---

### `Figure 03` — Sarcasm Distribution
📍 *Results §4*
Pada korpus validasi (N=3.395), **9,28% (315 cuitan)** terverifikasi memuat sindiran. Pada rekonstruksi leksikon kontradiktif (N=5.263), tercatat 181 cuitan sindiran eksplisit (3,44%) dan 2.979 cuitan (56,60%) proksi penolakan.
> **"Publik merespons kegagalan implementasi fisik dengan bahasa sindiran."**

---

### `Figure 04` — IndoBERT Performance
📍 *Results §4*
Evaluasi model pada validation set riil ($n=1.053$, checkpoint-792): Akurasi **57,45%**, Weighted F1 **0,4563**, Macro F1 **0,1444**. Kelas dominan Jijik mencapai Recall **96,92%** (F1 0,7178) dan kelas Percaya mencapai Presisi **68,42%**.
> **"Model IndoBERT terbukti sensitif mendeteksi sinyal keluhan fisik makanan."**

---

### `Figure 05` — Confusion Matrix
📍 *Results §4*
Matriks konfusi 9×9 mengonfirmasi 566 dari 584 cuitan berlabel aktual Jijik berhasil diprediksi tepat oleh model (96,92% recall), membuktikan tingginya daya tangkap sentimen penolakan.
> **"Transparansi komputasional dalam mengevaluasi kekuatan model deep learning."**

</td>
<td width="50%" valign="top">

### `Figure 06` — Global Social Network
📍 *Results §4*
971 nodes · 666 directed edges (692 raw interactions). Tanpa hub dialog pusat; membuktikan kondisi **hyper-fragmentation**, bukan polarisasi dua kubu.
> **"Wacana publik terfragmentasi dalam ratusan kantong percakapan terisolasi."**

---

### `Figure 07` — Community Structure
📍 *Results §4*
332–341 komunitas Louvain · **Modularity = 0,9837** (sangat tinggi). Giant component hanya mencakup 9,1% (89 node) dari total aktor, dengan resiprositas hanya 1,21%.
> **"Hyper-fragmentation: ratusan pulau percakapan terpisah tanpa arena konsensus."**

---

### `Figure 08` — Top Central Actors
📍 *Results §4*
**@grok (AI agent) memegang Out-degree tertinggi (#1 = 42)** sebagai rujukan verifikasi klaim publik (*Algorithmic Oracle*), sementara **@prabowo memiliki In-degree tertinggi (15) dengan Out-degree 0** (*Power Vacuum*).
> **"Algorithmic Trust mengambil alih fungsi di tengah kevakuman otoritas manusia."**

---

### `Figure 09` — Emotion × Network Pattern
📍 *Discussion §5*
Analisis silang: Emosi Jijik meresap ke hampir seluruh klaster komunitas independen — menjadi sentimen perekat di balik fragmentasi wacana.
> **"Emosi jijik menjadi benang merah struktural di seluruh jaringan wacana."**

---

### `Figure 10` — ABSA / Thematic Analysis
📍 *Discussion §5*
Sentimen berbasis aspek: Kekecewaan publik terkonsentrasi pada **eksekusi logistik (makanan basi) & pemotongan anggaran**, bukan pada konsep gizi itu sendiri.
> **"Program didukung, tetapi eksekusi fisik menu ditolak — Inilah Phygital Gap."**

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
├── 📄 requirements.txt                    # Dependensi Python untuk localhost
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
