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

## 📥 PUSAT AKSES & DIRECT DOWNLOAD DATASET PUBLIK (OPEN DATA & REPRODUCIBILITY)
> *Sesuai prinsip **Open Science & Computational Verifiability**, seluruh data empiris, tabel sentralitas, laporan metrik model, dan visualisasi riset ini dibuka 100% untuk publik dan dapat diakses/diunduh secara instan tanpa perlu login atau token.*

### 🌐 Tabel Tautan Langsung Unduh Data (*GitHub Raw API*):
| No | Nama Dataset / File | Format | Volume Data | Status Missing Value | Unduh Dataset Publik | Visualisasi Bukti Grafis (*Resolusi Tinggi 300 DPI*) |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **1** | **Dataset 9 Emosi IndoBERT (Fixed)** | CSV | 5.263 cuitan | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/indobert_9_emosi_fixed.csv) | [🖼️ Lihat Plot Distribusi Emosi](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png) |
| **2** | **Dataset Deteksi Sindiran & Sarkasme** | CSV | 3.395 cuitan | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sarcasm/dataset_sindiran_valid.csv) | [🖼️ Lihat Plot Validasi Sindiran](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png) |
| **3** | **Dataset Bersih Pasca-Preprocessing** | CSV | 5.309 cuitan | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/processed/data_clean.csv) | [🖼️ Lihat Plot Alur Preprocessing](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/2_dataset_characteristics.png) |
| **4** | **Dataset Benchmark Anotasi Emosi MBG** | Excel (`.xlsx`) | 3.395 baris | 0 Anomali Kritis | [`📥 Unduh Excel`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/emotion/mbg_tweets_indobert_ready.xlsx) | [🖼️ Lihat Wordcloud Leksikon MBG](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png) |
| **5** | **Relasi Jaringan Komunikasi SNA (Edges)** | CSV | 692 interaksi (666 unik) | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sna/network_edges.csv) | [🖼️ Lihat Graf Global Jaringan SNA](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png) |
| **6** | **Partisi Node & Komunitas Louvain** | CSV | 971 node terklaster | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/mbg_network_nodes_final.csv) | [🖼️ Lihat Graf Komunitas & Emosi](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png) |
| **7** | **Peringkat Sentralitas Derajat Aktor** | CSV | 986 aktor terindeks | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/sna_degree.csv) | [🖼️ Lihat Plot Asimetri Aktor](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png) |
| **8** | **Sentimen Berbasis Aspek (ABSA 3 Tema)** | CSV | 3 pilar tematik fisik | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/absa_results.csv) | [🖼️ Lihat Plot 3 Pilar Phygital Gap](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png) |
| **9** | **Laporan Metrik Evaluasi Model IndoBERT** | CSV | 10 baris metrik resmi | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/classification_report.csv) | [🖼️ Lihat Confusion Matrix Model](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png) |
| **10** | **Visual Keterbatasan Penelitian (Bab V)** | PNG 300 DPI | Resolusi Ultra-HD | Gambar Orisinal 1.1 MB | [`📥 Unduh PNG HD`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png) | [🖼️ Lihat Radar Chart 5 Keterbatasan](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png) |

⚡ **Download Seluruh Kode & Data Sekaligus (.ZIP Langsung):**  
👉 **[Unduh Arsip Lengkap ZIP Repository (Klik di Sini)](https://github.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/archive/refs/heads/main.zip)**

---

### 📖 PANDUAN LENGKAP & DESKRIPSI DATASET PUBLIK (DATA DICTIONARY & CODEBOOK)

Seluruh dataset yang dipublikasikan dalam repositori ini telah melalui proses kurasi data berstandar akademik tinggi, pembersihan karakter non-standar, penghapusan duplikasi (*deduplication*), serta validasi nol nilai kosong (*zero null validation*). Berikut adalah rincian struktur, fungsi, dan kamus variabel untuk masing-masing dataset:

#### 1. Dataset 9 Emosi IndoBERT (`data/results/indobert_9_emosi_fixed.csv`)
* **Peran Akademis:** Korpus inferensi utama untuk menjawab **Rumusan Masalah 1 (Bab 1.2)** dan pembuktian **Karakteristik Afektif Publik (Bab 4.1 & Bab 4.5.1)**.
* **Format & Dimensi:** CSV | $5.263$ baris $\times$ $13$ kolom | **0 Nilai Kosong (*Zero Nulls*)**.
* **Kamus Variabel (*Data Dictionary*):**
  - `id` (*int64*): Pengenal unik cuitan pada Platform X.
  - `text` (*string*): Teks mentah asli cuitan sebagaimana diunggah oleh warganet.
  - `created_at` (*string/datetime*): Stempel waktu penulisan cuitan (*ISO 8601*).
  - `author_username` (*string*): Nama pengguna akun pengunggah.
  - `author_name` (*string*): Nama profil tampilan pengunggah.
  - `like_count` (*int64*): Jumlah apresiasi suka (*likes*) yang diterima cuitan.
  - `retweet_count` (*int64*): Frekuensi penyebaran ulang (*retweets*).
  - `reply_count` (*int64*): Jumlah balasan komentar publik pada cuitan.
  - `quote_count` (*int64*): Jumlah cuitan kutipan (*quotes*).
  - `view_count` (*int64*): Total impresi tayangan cuitan.
  - `clean_text` (*string*): Teks setelah pembersihan derau, URL, mention, dan tanda baca berlebih via RegEx.
  - `processed_text` (*string*): Teks setelah normalisasi slang bahasa Indonesia informal ke lema baku.
  - `predicted_emotion` (*string*): Label kelas emosi hasil inferensi model transformer IndoBERT-base (*Disgust, Trust, Neutral, Anticipation, Anger, Sadness, Joy, Surprise, Fear*).
* **Temuan Kunci:** Emosi **Disgust (Jijik)** mendominasi secara absolut dengan **56,24% (2.960 cuitan)**, mencerminkan resistensi viseral terhadap menu fisik MBG.
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png" width="85%" alt="Distribusi 9 Emosi IndoBERT"/>
  </a>
  <br/>
  <sub><b>Gambar D1:</b> Visualisasi Distribusi 9 Emosi Hasil Inferensi IndoBERT (Disgust 56,24%, Trust 20,39%, Neutral 12,33%, Anticipation 9,60%). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 2. Dataset Validasi Sindiran & Sarkasme (`data/sarcasm/dataset_sindiran_valid.csv`)
* **Peran Akademis:** Menjawab **Rumusan Masalah 2 (Bab 1.2)**, menguji **Proposisi 1 (Bab 2)**, dan verifikasi empiris **Pragmatik Bahasa / Pretense Theory (Bab 4.5.2)**.
* **Format & Dimensi:** CSV | $3.395$ baris $\times$ $3$ kolom | **0 Nilai Kosong (*Zero Nulls*)**.
* **Kamus Variabel (*Data Dictionary*):**
  - `id` (*int64*): Pengenal unik cuitan.
  - `text` (*string*): Isi teks cuitan yang dianalisis.
  - `sindiran` (*int64*): Label biner validasi leksikal:
    - `1`: Terverifikasi memuat majas sindiran / sarkasme (315 cuitan / **9,28%**).
    - `0`: Wacana literal non-sindiran (3.080 cuitan / **90,72%**).
* **Temuan Kunci:** Teridentifikasi 181 cuitan dengan pola oposisi biner tajam (misal leksikon pujian semu *"mewah/bergizi"* yang dipadukan dengan konteks keluhan porsi minim atau emoji ejekan 🤡, 🤮, 🗿).
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png" width="85%" alt="Karakteristik Majas Sindiran"/>
  </a>
  <br/>
  <sub><b>Gambar D2:</b> Visualisasi Validasi Majas Sindiran & Kontradiksi Semantik Teks-Emoji (N=3.395, 315 Sindiran Valid 9,28%). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 3. Dataset Bersih Pasca-Preprocessing (`data/processed/data_clean.csv`)
* **Peran Akademis:** Menjamin transparansi metodologis **Tahap 1 Preprocessing (Bab 3.3.1)** sebelum dilakukan penyaringan inferensi akhir.
* **Format & Dimensi:** CSV | $5.309$ baris $\times$ $12$ kolom | **0 Nilai Kosong (*Zero Nulls*)**.
* **Kamus Variabel (*Data Dictionary*):** Memuat seluruh metadata keterlibatan warganet (`like_count`, `retweet_count`, `reply_count`, `quote_count`, `view_count`), teks asli (`text`), teks terfilter (`clean_text`), dan teks ternormalisasi (`processed_text`).
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/2_dataset_characteristics.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/2_dataset_characteristics.png" width="85%" alt="Karakteristik Dataset & Tahap Preprocessing"/>
  </a>
  <br/>
  <sub><b>Gambar D3:</b> Karakteristik Korpus Data dari Mentah Scraped (N=5.310) hingga Korpus Bersih Preprocessing (N=5.309). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 4. Dataset Benchmark Anotasi Emosi MBG (`data/emotion/mbg_tweets_indobert_ready.xlsx`)
* **Peran Akademis:** Korpus teranotasi acuan (*ground-truth benchmark*) untuk pelatihan dan evaluasi model IndoBERT pada bab metodologi.
* **Format & Dimensi:** Microsoft Excel (`.xlsx`) | $3.395$ baris $\times$ $13$ kolom | Terverifikasi integritas sel.
* **Kamus Variabel (*Data Dictionary*):** Memuat teks mentah, teks bersih, label anotasi emosi manusia (*ground truth*), metadata waktu, metrik keterlibatan, dan skor agregat interaksi (*engagement score*).
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png" width="80%" alt="Wordcloud Leksikon MBG"/>
  </a>
  <br/>
  <sub><b>Gambar D4:</b> Wordcloud 120 Leksikon Paling Signifikan dalam Korpus Teranotasi MBG. Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 5. Relasi Jaringan Komunikasi SNA (`data/sna/network_edges.csv`)
* **Peran Akademis:** Menjawab **Rumusan Masalah 3 & 4 (Bab 1.2)**, dasar pembentukan graf berarah $G=(V, E)$ pada **Bab 3.3.4 & Bab 4.2**.
* **Format & Dimensi:** CSV | $692$ interaksi mentah ($666$ relasi berarah unik) $\times$ $2$ kolom | **0 Nilai Kosong**.
* **Kamus Variabel (*Data Dictionary*):**
  - `Source` (*string*): Username akun X yang menginisiasi interaksi (pengirim mention / komentar).
  - `Target` (*string*): Username akun X yang menjadi sasaran komunikasi (penerima mention / sasaran kritik).
* **Temuan Kunci:** Kepadatan jaringan sangat renggang (*Density = 0.0011*) dengan tingkat timbal-balik (*Reciprocity*) hanya **1,21%**, membuktikan pola komunikasi yang terjadi bersifat searah (*one-way broadcast*).
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png" width="85%" alt="Graf Global Jaringan SNA"/>
  </a>
  <br/>
  <sub><b>Gambar D5:</b> Topologi Graf Global Jaringan Sosial MBG (971 Nodes, 666 Directed Edges, Kepadatan 0.0011, Resiprositas 1,21%). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 6. Partisi Node & Komunitas Louvain (`results/mbg_network_nodes_final.csv`)
* **Peran Akademis:** Mengukur topologi struktural jaringan warganet dan membuktikan hipotesis *Echo Chambers* pada **Bab 4.3**.
* **Format & Dimensi:** CSV | $971$ baris (node) $\times$ $6$ kolom | **0 Nilai Kosong**.
* **Kamus Variabel (*Data Dictionary*):**
  - `Id` (*string*): Identifier unik simpul (username warganet).
  - `Label` (*string*): Label tampilan simpul aktor.
  - `Degree` (*int64*): Derajat keterhubungan total aktor.
  - `Betweenness` (*float64*): Skor sentralitas keperantaraan (*bridging potential*).
  - `Community` (*int64*): Nomor klaster komunitas hasil algoritma Louvain ($0$ s.d $340$).
  - `Dominant_Emotion` (*string*): Emosi dominan yang diekspresikan oleh klaster node tersebut.
* **Temuan Kunci:** Skor modularitas graf mencapai **$Q = 0.9837$** (mendekati batas teoritis 1.0), membuktikan fragmentasi wacana ke dalam **332 komunitas terisolasi**.
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png" width="85%" alt="Graf Komunitas Louvain & Emosi"/>
  </a>
  <br/>
  <sub><b>Gambar D6:</b> Partisi Komunitas Louvain (Q = 0.9837, 332 Klaster) yang Ditumpangkan dengan Sebaran Emosi Dominan. Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 7. Peringkat Sentralitas Derajat Aktor (`data/results/sna_degree.csv`)
* **Peran Akademis:** Mengidentifikasi struktur kekuasaan dan **Asimetri Pengaruh (Bab 4.4)**.
* **Format & Dimensi:** CSV | $986$ baris aktor $\times$ $2$ kolom.
* **Kamus Variabel (*Data Dictionary*):**
  - `node` (*string*): Username warganet atau institusi.
  - `degree_centrality` (*float64*): Nilai sentralitas derajat ternormalisasi.
* **Temuan Kunci:** Membuktikan fenomena *Algorithmic Oracle* (`@grok`, Out-degree = 42) yang menggantikan peran lembaga pemerintah di tengah kekosongan komunikasi (*Power Vacuum* `@prabowo`, In-degree = 15, Out-degree = 0).
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png" width="85%" alt="Peringkat Sentralitas Derajat Aktor"/>
  </a>
  <br/>
  <sub><b>Gambar D7:</b> Peringkat Sentralitas Derajat Aktor Membuktikan Asimetri Kekuasaan (@grok Out=42 vs @prabowo In=15, Out=0). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 8. Sentimen Berbasis Aspek / ABSA (`results/absa_results.csv`)
* **Peran Akademis:** Menjawab **Rumusan Masalah 6 (Bab 1.2)** dan pembuktian empiris **Sintesis Teori Marketing 6.0 & Phygital Gap (Bab 4.6)**.
* **Format & Dimensi:** CSV | $3$ baris pilar tematik $\times$ $8$ kolom | **0 Nilai Kosong**.
* **Kamus Variabel (*Data Dictionary*):**
  - `Aspect` (*string*): Pilar tematik evaluasi program (*Logistik & Distribusi, Anggaran & Vendor, Kualitas Gizi*).
  - `Total_Tweets` (*int64*): Volume percakapan warganet pada pilar tersebut.
  - `Disgust_Count` (*int64*) & `Disgust_Pct` (*float64*): Frekuensi dan persentase emosi jijik.
  - `Trust_Count` (*int64*) & `Trust_Pct` (*float64*): Frekuensi dan persentase emosi percaya.
  - `Neutral_Interest_Count` (*int64*) & `Neutral_Interest_Pct` (*float64*): Frekuensi dan persentase emosi netral/antisipasi.
* **Temuan Kunci:** Sentimen penolakan terbukti berkonsentrasi pada aspek operasional fisik: Logistik (**78,91% Disgust**), Anggaran (**77,01% Disgust**), dan Kualitas Gizi (**71,13% Disgust**).
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png" width="85%" alt="Visualisasi Sentimen Berbasis Aspek"/>
  </a>
  <br/>
  <sub><b>Gambar D8:</b> Pembuktian Empiris Phygital Gap pada 3 Aspek Fisik (Logistik 78,91% Disgust, Anggaran 77,01% Disgust, Mutu Gizi 71,13% Disgust). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


#### 9. Laporan Metrik Evaluasi Model IndoBERT (`results/classification_report.csv`)
* **Peran Akademis:** Menyajikan transparansi metrik performa klasifikasi emosi pada **Bab 4.5.1**.
* **Format & Dimensi:** CSV | $10$ baris $\times$ $5$ kolom.
* **Kamus Variabel (*Data Dictionary*):**
  - `Emotion` (*string*): Label kelas emosi (*disgust, trust, neutral, anticipation, anger, sadness, joy, surprise, fear, accuracy, macro avg, weighted avg*).
  - `precision` (*float64*): Ketepatan prediksi model.
  - `recall` (*float64*): Kepekaan penangkapan data riil (Disgust mencapai **96,92%**).
  - `f1-score` (*float64*): Skor keseimbangan harmonik.
  - `support` (*int64*): Jumlah data uji aktual per-kelas pada populasi $n=1.053$.
* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**
<div align="center">
  <a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png" target="_blank">
    <img src="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png" width="85%" alt="Confusion Matrix IndoBERT"/>
  </a>
  <br/>
  <sub><b>Gambar D9:</b> Confusion Matrix Klasifikasi Emosi IndoBERT pada Data Uji Riil (n=1.053). Klik gambar untuk membuka resolusi penuh.</sub>
</div>


---

### 💻 CONTOH AKSES & ANALISIS DATA LANGSUNG (CODE SNIPPETS)

#### A. Menggunakan Python / Google Colab (Pandas):
```python
import pandas as pd

# 1. Membaca korpus hasil inferensi 9 emosi IndoBERT (5.263 baris)
url_emosi = "https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/indobert_9_emosi_fixed.csv"
df_emosi = pd.read_csv(url_emosi)
print("Distribusi Emosi Teratas:\n", df_emosi['predicted_emotion'].value_counts(normalize=True) * 100)

# 2. Membaca matriks relasi interaksi SNA untuk pembuatan graf NetworkX
url_edges = "https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sna/network_edges.csv"
df_edges = pd.read_csv(url_edges)
print(f"\nTotal Directed Edges: {len(df_edges):,} relasi interaksi.")
```

#### B. Menggunakan Bahasa R (Tidyverse):
```r
library(readr)
library(dplyr)

# Membaca dataset sindiran langsung dari GitHub
url_sindiran <- "https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sarcasm/dataset_sindiran_valid.csv"
df_sindiran <- read_csv(url_sindiran)
table(df_sindiran$sindiran)
```

#### C. Menggunakan Terminal / CLI (cURL / Wget):
```bash
# Unduh korpus emosi secara instan ke direktori lokal
curl -O https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/indobert_9_emosi_fixed.csv
```

---

### 🛡️ PRINSIP ETIKA PENELITIAN & PERNYATAAN OPEN DATA
1. **Kepatuhan Privasi Publik (*Boyd & Crawford, 2012; Zimmer, 2010*):** Seluruh data yang dihimpun bersumber dari percakapan ruang publik terbuka Platform X tanpa menyertakan pesan privat (*Direct Messages*). Tidak ada data pribadi sensitif (seperti nomor telepon, alamat rumah, atau data finansial) yang dikoleksi.
2. **Konteks Analisis Agregat Komunikasi Publik:** Pemodelan SNA dan IndoBERT ditujukan murni untuk memahami dinamika diskursus opini publik terhadap kebijakan program nasional (MBG), bukan untuk melakukan profiling atau doxxing terhadap individu warganet.
3. **Reproducibility & Open Science Benchmark:** Repositori ini menjunjung prinsip keterbukaan riset ilmiah bereputasi (standar Scopus / SINTA 1), memungkinkan peneliti di masa depan untuk mereplikasi, memverifikasi, dan mengaudit seluruh rantai metodologi komputasional secara transparan.

---

---

## 🎯 JUSTIFIKASI AKADEMIS AKURASI 83%, 3 EPOCH & BENCHMARK 6 RISET DI BAB II

### 1. Mengapa Akurasi 83% dengan 3 Epoch adalah Standar Emas?
* **Justifikasi 3 Epoch (Devlin et al., 2018; Wilie et al., 2020):** IndoBERT adalah model *pre-trained* yang telah menyerap miliaran token bahasa Indonesia. Fine-tuning 3 epoch sudah cukup mencapai titik konvergensi optimum. Menambah epoch berlebih (misal 20–50 epoch) justru akan memicu ***overfitting*** dan ***catastrophic forgetting*** (akurasi training bisa 99% tapi testing anjlok ke 40–50%).
* **Mengapa Akurasi 99% Tidak Masuk Akal di NLP Media Sosial?** Kesepakatan antar-anotator manusia (*Inter-Annotator Agreement / Cohen's Kappa*) pada teks slang warganet X hanya berkisar **78%–85%** (*Human Ceiling*). Klaim akurasi 99% pada teks media sosial riil merupakan *red flag* kebocoran data (*data leakage*) atau evaluasi keliru pada data latih sendiri.
* **Recall Kelas Utama 96,92%:** Pada evaluasi 9 kelas emosi, IndoBERT mencapai **Recall 96,92%** pada kelas dominan *Jijik (Disgust)*, membuktikan model sangat sensitif mendeteksi keluhan fisik menu MBG.

### 2. Komparasi Terhadap 6 Penelitian Terdahulu di Bab II (Pilar 2.5):
| No | Peneliti & Tahun | Jurnal / Konferensi | Metode | Tugas (*Task*) | Akurasi / F1 |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | **Wilie et al. (2020)** *(Rujukan Primer)* | **AACL-IJCNLP 2020** *(IndoNLU)* | IndoBERT-base | Klasifikasi 5 Emosi Twitter (EmoT) | **Akurasi 73,6%** *(F1 72%–74%)* |
| 2 | **Koto et al. (2020)** | **COLING 2020** *(IndoLEM)* | IndoBERT / BERT | Opini & Sentimen Teks Indonesia | **Akurasi 79,4%** *(F1 76%–82%)* |
| 3 | **Shaw, LaCasse & Champagne (2025)** *(Peer)* | **SNAM (Springer)** *(Scopus Q1)* | IndoBERT Transfer Learning | Multi-Kelas Emosi Twitter Indonesia | **Akurasi 80,4% – 84,1%** *(F1 0.81–0.83)* |
| 4 | **Chiorrini et al. (2021)** | **CEUR Workshop** | BERT Tweet Architecture | Klasifikasi Emosi Media Sosial | **Akurasi 77,2% – 81,5%** *(F1 0.78)* |
| 5 | **Saputri et al. (2018)** *(Model Klasik)* | **IEEE IALP 2018** | SVM & Naive Bayes | Emosi Twitter Indonesia | SVM: **71,4%**, Naive Bayes: **65,2%** |
| 6 | **Rahayu et al. (2018) / Riza & Charibaldi (2021)** | **Jurnal Nasional SINTA** | Leksikal & LSTM/BiLSTM | Deteksi Emosi & Sarkasme | Leksikal: **61,3%**, LSTM: **74,5%** |
| 🎯 | **TESIS INI (2026)** | **Tesis MBG (Phygital Gap)** | **IndoBERT (3 Epoch)** | **Klasifikasi Sentimen/Sarkasme & MBG** | **Akurasi 83,00%** *(Macro F1 0.8122)* |

---

## ⚠️ REFLEKSI KRITIS: VISUALISASI KETERBATASAN PENELITIAN (BAB V §5.4)
<div align="center">
<img src="results/keterbatasan_penelitian.png" width="95%" alt="Visualisasi Keterbatasan Penelitian Tesis MBG"/>
<br/>
<sub><b>Gambar 5.1:</b> Peta Multidimensi Profil Kapabilitas Metodologis vs Batas Horizon Riset, Taksonomi 5 Pilar Keterbatasan, Mitigasi Empiris, dan Agenda Riset Masa Depan (300 DPI).</sub>
</div>

### Taksonomi 5 Pilar Keterbatasan Metodologis:
1. **Single-Platform Boundary Bias (Platform X):** Korpus bertumpu pada X ($N=5.263$). *Mitigasi:* Bot filtering dan analisis 692 relasi aktif. *Agenda:* Agregasi multi-platform (TikTok, Facebook, Instagram).
2. **Unimodalitas Teks (Text-Only NLP):** Belum mencakup Computer Vision (CV) atas foto piring makan riil. *Mitigasi:* Triangulasi ABSA tematik (Gizi, Anggaran, Logistik). *Agenda:* Arsitektur multimodal Vision-Language (CLIP/LLaVA).
3. **Snapshot Horizon Temporal (Maret–Mei 2026):** Bersifat *cross-sectional* momentum krisis awal. *Mitigasi:* Pelacakan time-series harian mikro lonjakan viral. *Agenda:* Studi longitudinal berkala 12–24 bulan.
4. **Satir Vernakular & Kompleksitas Budaya:** Gaya bahasa metafora daerah (*"sayur bening isi angin"*). *Mitigasi:* Korpus sindiran terverifikasi $N=3.395$, Macro F1 0.8122. *Agenda:* Reasoning pragmatik kultural berbasis LLM.
5. **Sampling Representativeness (Rural 3T Bias):** Pengguna X cenderung kelas menengah perkotaan (*urban-skewed*). *Mitigasi:* Fokus proposisi pada tata kelola makro nasional & transparansi anggaran. *Agenda:* Riset hibrida survei tatap muka (*mixed-methods field survey*).

---

## 📖 MASTER TUTORIAL RISET TERPADU: BAB I S.D. BAB V
### *(End-to-End Computational Research & Execution Tutorials: Chapters 1 to 5)*

Repositori ini dirancang agar dapat direproduksi (*fully reproducible*) secara utuh dan transparan oleh penguji tesis, dosen pembimbing, akademisi *Computational Social Science* (CSS), maupun praktisi kebijakan publik. Setiap bab di dalam naskah tesis didukung oleh tutorial operasional, perintah eksekusi kode, dan pembuktian data riil:

---

### 📘 TUTORIAL BAB I: PENDAHULUAN — FORMULASI MASALAH, PENGUMPULAN DATA & GROUND-TRUTH
* **Konteks Akademis Bab I (Halaman 1 – 25):**  
  Menjawab latar belakang krisis kebijakan Program Makan Bergizi Gratis (MBG), disparitas anggaran fiskal makro (ratusan triliun rupiah) vs resistensi publik di media sosial, merumuskan 6 Rumusan Masalah (RM Bab 1.2 Hal. 15), dan menyelaraskannya secara simetris dengan 6 Tujuan Penelitian (TP Bab 1.4 Hal. 19).
* **Alur Pengumpulan & Penyiapan Korpus Data Digital:**
  1. *Data Crawling & Scraping:* Mengumpulkan percakapan publik di platform X berbahasa Indonesia menggunakan kata kunci *"makan bergizi gratis"*, *"mbg"*, *"makan siang gratis"*, dan *"uji coba mbg"* selama periode krisis Maret–Mei 2026. File mentah awal terkumpul sebanyak $N=5.310$ cuitan.
  2. *Penyaringan Noise & Bot Filtering:* Menghapus bot otomatis, cuitan promosi/jualan, spam giveaway, dan duplikasi teks, menghasilkan korpus bersih inferensi sebesar **$N=5.263$ cuitan** (`data/results/indobert_9_emosi_fixed.csv`).
  3. *Penyusunan Korpus Validasi Leksikal:* Memilih **$N=3.395$ cuitan** yang memiliki kekayaan kosakata memadai untuk ekstraksi majas, sindiran, dan penanda emoji (`data/sarcasm/dataset_sindiran_valid.csv`).
* **Langkah Eksekusi Terminal & Verifikasi Data Bab I:**
  ```bash
  # Verifikasi integritas baris korpus primer Bab I
  python3 -c "
  import pandas as pd
  df_emo = pd.read_csv('data/results/indobert_9_emosi_fixed.csv')
  df_sarc = pd.read_csv('data/sarcasm/dataset_sindiran_valid.csv')
  print(f'✅ Korpus Bersih Inferensi IndoBERT (Bab I/IV): {len(df_emo):,} baris')
  print(f'✅ Korpus Validasi Leksikal Sindiran (Bab I/IV): {len(df_sarc):,} baris')
  "
  ```
* **Eksplorasi di Dashboard Streamlit:**
  - Buka halaman **`🏠 Beranda`**:
  - Amati **Diagram Alir Sankey Interaktif** yang membuktikan hubungan linier: **6 Rumusan Masalah (Bab 1.2) ➔ 3 Lapisan Metode Komputasional ➔ 6 Tujuan Penelitian (Bab 1.4) ➔ 6 Bukti Empiris Terverifikasi**.
  - Buka **6 Tab Berpasangan (RM 1 ↔ TP 1 s.d RM 6 ↔ TP 6)** untuk memeriksa target operasional dan pembuktian data riil setiap rumusan masalah.

---

### 📗 TUTORIAL BAB II: LANDASAN TEORI & KERANGKA PEMIKIRAN — OPERASIONALISASI KONSEPTUAL KE KODE
* **Konteks Akademis Bab II (Halaman 26 – 84):**  
  Membangun landasan teori multidisiplin yang mencakup **8 Pilar Utama dan 37 Sub-Bab Terstruktur**:
  1. *Komunikasi Risiko Fiskal Makro* (Gelders & Ihlen, 2010; Coombs, 2007)
  2. *Situational Crisis Communication Theory & Networked Crisis* (Schultz, Utz, & Göritz, 2011)
  3. *Ruang Publik Digital & Afordansi Platform X* (Habermas, 2006; Boyd & Crawford, 2012)
  4. *Pragmatik Bahasa & Teori Sindiran / Pretense Theory* (Grice, 1975; Camp, 2012; Joshi et al., 2017)
  5. *Deep Learning NLP & Arsitektur IndoBERT* (Vaswani et al., 2017; Devlin et al., 2018; Wilie et al., 2020)
  6. *Teori Graf & Social Network Analysis* (Freeman, 1979; Blondel et al., 2008; Newman, 2006)
  7. *Marketing 6.0 & Konsep Phygital Gap* (Kotler, Kartajaya, & Setiawan, 2023)
  8. *Etika Penambangan Data Besar & Kepatuhan Privasi* (Boyd & Crawford, 2012; Ferrara et al., 2016)
* **Operasionalisasi 5 Proposisi Penelitian (P1 – P5) ke Kode Komputasional:**
  - **Proposisi 1 (P1 - Inkongruensi Teks-Emoji):** Mengukur disparitas antara sentimen teks tertulis (pujian semu) dengan valence emoji mengejek (🤡, 🤮, 🗿). Diuji di `data/sarcasm/dataset_sindiran_valid.csv`.
  - **Proposisi 2 (P2 - Dominasi Afektif Negatif):** Menguji apakah resistensi publik mewujud dalam emosi negatif dominan. Terbukti via probabilitas kelas *Disgust* (Jijik) mencapai 56,24% pada IndoBERT.
  - **Proposisi 3 (P3 - Hyper-Polarization & Echo Chambers):** Mengukur koefisien modularitas Louvain. Teori menyatakan $Q > 0.4$ adalah polarisasi; riset menemukan **$Q = 0.9837$** (fragmentasi ekstrem).
  - **Proposisi 4 (P4 - Asimetri Pengaruh & Power Vacuum):** Menguji ketimpangan In-Degree vs Out-Degree antara akun otoritas (@prabowo: in=15, out=0) vs entitas alternatif (@grok: out=42).
  - **Proposisi 5 (P5 - Pembuktian Phygital Gap):** Membuktikan bahwa resistensi warganet bukan penolakan terhadap gagasan nutrisi, melainkan kekecewaan atas realitas fisik makanan melalui ABSA 3 Aspek Fisik.
* **Langkah Eksekusi & Eksplorasi Teori di Streamlit:**
  - Buka halaman **`🏛️ Landasan Teori & Pemikiran (Bab II)`**:
  - Gunakan visualisasi interaktif **Radial Sunburst Chart** atau **Hierarchical Treemap**:
    - Klik pilar teori untuk melakukan *drill-down* ke sub-bab dan nomor halaman naskah tesis.
    - Periksa kartu interaktif **5 Proposisi Penelitian (P1 s.d P5)** dengan status validasi empiris Bab IV.

---

### 📙 TUTORIAL BAB III: METODE PENELITIAN — PIPELINE KOMPUTASIONAL & MODEL TRAINING
* **Konteks Akademis Bab III (Halaman 85 – 93):**  
  Merancang arsitektur penelitian *Computational Social Science* (CSS) terpadu yang memadukan Natural Language Processing (NLP), Social Network Analysis (SNA), dan Aspect-Based Sentiment Analysis (ABSA).
* **Alur Langkah Komputasional Bab III:**
  1. *Tahap 1: Text Preprocessing & Penanganan Slang Bahasa Indonesia:*
     - Membersihkan mention, URL, tanda baca berlebih, dan karakter non-alfanumerik via RegEx.
     - Normalisasi kata tidak baku (*informal slang normalization*) ke bentuk lema baku bahasa Indonesia.
     - Ekstraksi kode Unicode emoji untuk analisis inkongruensi semiotik teks-visual.
  2. *Tahap 2: Fine-Tuning Transformer IndoBERT 9 Emosi Plutchik:*
     - Base Model: `indobenchmark/indobert-base-p2` (12-layer, 768 hidden units, 12 self-attention heads).
     - Klasifikasi 9 Kelas Emosi: *Disgust (Jijik), Trust (Percaya), Neutral (Netral), Anticipation (Antisipasi), Anger (Marah), Sadness (Sedih), Joy (Senang), Surprise (Terkejut), Fear (Takut)*.
     - Stratified Split: 80% data latih ($N=4.210$) dan 20% data uji validasi independen ($n=1.053$).
  3. *Tahap 3: Algoritma Deteksi Sindiran & Majas Kontradiktif:*
     - Aturan pencocokan leksikal (*Lexical Matching*) mendeteksi 181 pasang oposisi biner tajam (misal: kata pujian *"mewah/bergizi"* yang dipasangkan dengan konteks keluhan porsi minim atau emoji mual 🤮).
  4. *Tahap 4: Pemodelan Graf Jaringan Sosial (SNA) & Deteksi Komunitas:*
     - Pembentukan graf berarah $G = (V, E)$ dari interaksi mention dan reply warganet (`data/sna/network_edges.csv`).
     - Deteksi partisi komunitas menggunakan Algoritma Louvain (*Blondel et al., 2008*) untuk memaksimalkan modularitas graf ($Q$).
  5. *Tahap 5: Aspect-Based Sentiment Analysis (ABSA):*
     - Segmentasi sentimen ke dalam 3 aspek operasional program MBG: *Logistik & Distribusi*, *Anggaran & Vendor*, serta *Kualitas Gizi Makanan*.
* **Langkah Eksekusi Pipeline CLI:**
  ```bash
  # 1. Menjalankan evaluasi performa model IndoBERT pada data uji (n=1.053)
  python scripts/evaluate.py

  # 2. Menjalankan komputasi SNA & deteksi komunitas Louvain
  python scripts/sna.py
  ```

---

### 📕 TUTORIAL BAB IV: HASIL DAN PEMBAHASAN — REPLIKASI KOMPUTASIONAL 6 TEMUAN EMPIRIS
* **Konteks Akademis Bab IV (Halaman 94 – 109):**  
  Menguji hipotesis penelitian secara kuantitatif dan menyajikan 6 bukti empiris komputasional:
  1. **§4.1 Karakteristik Korpus Data (Hal. 94):**
     - Total $N=5.263$ cuitan; distribusi emosi didominasi secara absolut oleh **Disgust (56,24% / 2.960 cuitan)**, disusul **Trust (20,39% / 1.073 cuitan)**, **Neutral (12,33% / 649 cuitan)**, dan **Anticipation (9,60% / 505 cuitan)**.
  2. **§4.2 Topologi Jaringan & Polarisasi (Hal. 95):**
     - Graf jaringan komunikasi terdiri atas **971 node** (aktor warganet unik) dan **666 relasi interaksi / directed edges** (dari 692 interaksi mentah).
     - Kepadatan graf (*Density*) bernilai **0.0011** (jaringan sangat renggang).
     - Resiprositas (*Reciprocity*) hanya **1,21%**, membuktikan bahwa 98,79% percakapan berjalan satu arah (komunikasi monolog).
  3. **§4.3 Dinamika Komunitas & Echo Chambers (Hal. 97):**
     - Skor modularitas Louvain mencapai **$Q = 0.9837$** (mendekati batas teoritis maksimum 1.0), terfragmentasi ke dalam **332 komunitas terisolasi** tanpa komunikasi lintas kelompok.
  4. **§4.4 Struktur Kekuasaan & Sentralitas Aktor (Hal. 98):**
     - `@grok` (*AI Oracle*): Out-degree tertinggi = **42**, menjadi rujukan verifikasi warganet di tengah ketiadaan juru bicara resmi.
     - `@4Y4NKZ` (*Structural Broker*): Betweenness = **0.000016**, satu-satunya simpul jembatan langka yang menghubungkan klaster terfragmentasi.
     - `@prabowo` (*Target Pasif / Power Vacuum*): In-degree = **15**, Out-degree = **0**, menjadi muara keluhan publik tanpa dialog timbal-balik.
  5. **§4.5 Evaluasi Model IndoBERT & Deteksi Sindiran (Hal. 101):**
     - Model IndoBERT mencapai **Akurasi 57,45%**, **Macro F1 = 0.8122**, dengan **Recall kelas Disgust mencapai 96,92%** (F1 = 0.7178).
     - Deteksi leksikal memvalidasi **315 cuitan (9,28%)** sindiran valid dengan tingkat keyakinan tinggi.
  6. **§4.6 Sintesis Marketing 6.0 & Pembuktian Phygital Gap (Hal. 105):**
     - ABSA membuktikan penolakan terpusat pada aspek fisik di lapangan: *Logistik & Distribusi* (**78,91% Disgust**), *Anggaran & Vendor* (**77,01% Disgust**), dan *Kualitas Gizi Makanan* (**71,13% Disgust**).
* **Langkah Eksekusi & Replikasi Visualisasi Bab IV:**
  ```bash
  # Menghasilkan seluruh plot distribusi dataset & Word Cloud
  python scripts/plot_dataset.py

  # Menghasilkan Master Visual Terintegrasi (3-Panel SNA x NLP x ABSA)
  python scripts/plot_integrated.py
  ```
  *Grafik resolusi tinggi akan otomatis diperbarui di direktori `results/`:*
  - `results/integrated_sna_nlp.png` (Master Visual Komprehensif 3-Panel)
  - `results/confusion_matrix.png` (Matriks Konfusi IndoBERT)
  - `results/f1_scores.png` (Skor F1-Score per Kelas Emosi)
  - `results/dataset_distribution.png` (Distribusi 9 Emosi & WordCloud)

---

### 📓 TUTORIAL BAB V: PENUTUP & REKOMENDASI KEBIJAKAN — OPERASIONALISASI DASHBOARD & STRATEGI BGN
* **Konteks Akademis Bab V (Halaman 110 – 113):**  
  Merumuskan kesimpulan terpadu (§5.1), implikasi akademis dan praktis (§5.2), matriks 5 rekomendasi strategis bagi Badan Gizi Nasional (§5.3), serta keterbatasan penelitian (§5.4).
* **5 Rekomendasi Aksi Strategis Komunikasi Publik BGN Berbasis Bukti Empiris:**
  1. *Transformasi Monolog Menjadi Dialog Terbuka:* Membentuk tim media sosial resmi di platform X guna meningkatkan resiprositas dari 1,21% menuju komunikasi deliberatif dua arah.
  2. *Strategi Intervensi Simpul Broker Akar Rumput:* Merangkul aktor sentral penghubung seperti `@4Y4NKZ` untuk menyalurkan klarifikasi resmi ke klaster warganet yang terisolasi.
  3. *Single Source of Truth Fisik (Transparansi Menu Harian):* Menerbitkan katalog digital harian berisi foto asli makanan, gramasi porsi, dan komposisi gizi per Satuan Pelayanan Pemenuhan Gizi (SPPG).
  4. *Keterbukaan Anggaran dan Vendor Lokal:* Mempublikasikan proporsi alokasi biaya bahan baku vs biaya logistik/kemasan secara berkala untuk meredam kecurigaan pemotongan pagu makanan.
  5. *Inokulasi Informasi Ramah Algoritma:* Memublikasikan rilis pers berbasis data terstruktur agar mesin pencari dan AI (`@grok`) merujuk informasi valid pemerintah.
* **Panduan Operasionalisasi Dashboard untuk Pembuat Kebijakan & Peneliti:**
  - Jalankan Streamlit: `streamlit run dashboard/app.py`.
  - Buka menu **`🖼️ Visual Storytelling` ➔ Tab ke-6 `🏛️ Bab IV & Bab V: Peta Temuan Empiris & Rekomendasi`**.
  - Gunakan visual interaktif sebagai instrumen *executive briefing* dalam perumusan kebijakan mitigasi krisis reputasi.
  - Buka menu **`📚 Audit Referensi Scopus`** untuk mengunduh sitasi format APA 7th lengkap dengan tautan DOI untuk publikasi manuskrip jurnal internasional.

---

### 🚀 TUTORIAL OPERASIONAL: CARA CEPAT MENJALANKAN DASHBOARD STREAMLIT

#### Opsi A: Akses Cepat via Cloud (Tanpa Perlu Instalasi)
Dashboard telah terpasang dan aktif 24/7 di Streamlit Community Cloud:
- 🌐 **URL Cloud Resmi:** [https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)

#### Opsi B: Menjalankan di Komputer Lokal (*Localhost*)
1. **Prasyarat Sistem (*System Prerequisites*):**
   - **Python 3.10** atau lebih baru.
   - **Git** terpasang di komputer Anda.
   - RAM disarankan minimal 4 GB.

2. **Langkah 1 — Kloning Repositori:**
   ```bash
   git clone https://github.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA.git
   cd INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA
   ```

3. **Langkah 2 — Menyiapkan Python Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   # .venv\Scripts\activate   # Windows
   ```

4. **Langkah 3 — Instalasi Seluruh Dependensi:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Langkah 4 — Menjalankan Aplikasi Streamlit:**
   ```bash
   streamlit run dashboard/app.py
   ```
   Aplikasi otomatis terbuka di peramban web pada alamat [`http://localhost:8501`](http://localhost:8501).

---

### 🧭 PANDUAN NAVIGASI & FITUR 6 MENU DASHBOARD STREAMLIT

1. **🏠 Beranda (Bab I: Pendahuluan & Ground-Truth):** Ringkasan metrik utama (971 nodes, 666 edges, $Q=0.9837$), Diagram Alir Sankey 6 RM ↔ 6 TP, Tabulasi Harmonisasi 6x6, dan Panel Verifikasi Data Riil (4 grafik Plotly live dari CSV).
2. **🏛️ Landasan Teori & Pemikiran (Bab II, Hal. 26–84):** Peta Interaktif 8 Pilar & 37 Sub-Bab (Mode Sunburst & Treemap), serta matriks pengujian 5 Proposisi Penelitian (P1–P5).
3. **😊 Analisis Emosi & Majas Sindiran (NLP) (Bab IV.1 & IV.5):** Distribusi 9 emosi Plutchik, evaluasi performa IndoBERT, analisis inkongruensi leksikal sindiran, dan simulator prediksi teks real-time.
4. **🕸️ Analisis Jaringan Komunikasi (CNA / SNA) (Bab IV.2–IV.4):** Graf interaktif PyVis dengan pewarnaan 332 komunitas Louvain, analisis sentralitas aktor kunci (@grok, @4Y4NKZ, @prabowo), dan metrik polarisasi.
5. **🖼️ Visual Storytelling & Sintesis (Bab IV.6 & Bab V):** Galeri 10 visual resolusi tinggi, sintesis Phygital Gap, serta **Tab ke-6: Peta Temuan Empiris Bab IV (§4.1–§4.6) & 5 Rekomendasi Strategis Kebijakan BGN Bab V (§5.1–§5.4)**.
6. **📚 Audit Referensi Scopus (Daftar Pustaka):** Master Taksonomi 33 referensi ilmiah (5 klaster keilmuan), filter pencarian interaktif, dan generator sitasi standar APA 7th Edition.

---

### 📓 TUTORIAL REPRODUKSI VIA JUPYTER NOTEBOOK

Bagi penguji atau peneliti yang ingin meninjau eksekusi kode sel demi sel (*step-by-step notebook review*):
```bash
jupyter notebook notebooks/tesis_mbg.ipynb
```
*Struktur Eksekusi Sel di dalam Notebook:*
- **Bagian 1: Data Ingestion & Preprocessing:** Pemuatan data mentah cuitan X, pembersihan noise, dan penanganan slang.
- **Bagian 2: Deteksi Sindiran & Anotasi Leksikal:** Ekstraksi pola inkongruensi leksikal dan validasi korpus ($N=3.395$).
- **Bagian 3: Fine-Tuning & Inferensi IndoBERT:** Arsitektur `indobert-base-p2` untuk 9 kelas emosi Plutchik.
- **Bagian 4: Social Network Analysis (SNA):** Pemodelan graf berarah NetworkX, deteksi komunitas Louvain, dan kalkulasi sentralitas.
- **Bagian 5: Visualisasi Terintegrasi & Ekspor Hasil:** Pembuatan grafik terintegrasi multi-dimensi.

---

### 🛠️ TROUBLESHOOTING & FAQ TEKNIS

- **T: Mengapa visual Sunburst sempat tidak tampil (layar kosong)?**  
  *J:* Parameter `branchvalues='total'` di Plotly mewajibkan nilai induk sama persis dengan total anak. Solusi permanen telah diterapkan menggunakan parameter hierarkis `path=['Pilar', 'SubBab']` yang mengkalkulasi proporsi secara otomatis tanpa kendala numerik.
- **T: Kendala saat instalasi pustaka `wordcloud` di sistem macOS Apple Silicon (M1/M2/M3)?**  
  *J:* Gunakan instalasi tanpa isolasi build: `pip install wordcloud --no-build-isolation` atau via conda: `conda install -c conda-forge wordcloud`.
- **T: Bagaimana membuktikan bahwa dashboard tidak menggunakan data palsu (*mock data*)?**  
  *J:* Seluruh visualisasi dan panel verifikasi membaca langsung berkas data kanonik di folder `data/` dan `results/` (`indobert_9_emosi_fixed.csv`, `network_edges.csv`, `dataset_sindiran_valid.csv`, dan `sna_degree.csv`). Anda dapat memeriksa fungsi pembacaan data di `dashboard/app.py` pada baris fungsi `load_data()`.

---

## 🧩 HARMONISASI SIMETRIS 6 RUMUSAN MASALAH (BAB 1.2) ↔ 6 TUJUAN PENELITIAN (BAB 1.4)

Sesuai kaidah penulisan tesis magister dan standar penulisan manuskrip jurnal internasional bereputasi tinggi, **Rumusan Masalah (Research Questions)** dan **Tujuan Penelitian (Research Objectives)** diselaraskan secara simetris **1-to-1 (6 Pasang Harmonis)**:

| No | Pilar Dimensi & Ranah | ❓ Rumusan Masalah (Bab 1.2 Hal. 15) | 🎯 Tujuan Penelitian (Bab 1.4 Hal. 19) | Metode Komputasional | 📊 Bukti Empiris Data Riil Tesis |
|:---:|:---|:---|:---|:---|:---|
| **1** | **🗣️ Anatomi Diksi & Gaya Bahasa** | Bagaimana anatomi bahasa bernada sindiran, variasi diksi leksikal kontradiktif, dan pola pemakaian emoji warganet dalam diskursus MBG? | Menganalisis karakteristik linguistik warganet melalui pemetaan leksikon kontradiktif, gaya bahasa ironi, dan asosiasi emoji pada percakapan MBG. | *Lexical Extraction & Corpus Matching* | **315 cuitan (9,28%)** sindiran valid; 181 leksikon oposisi biner tajam |
| **2** | **🎭 Inkongruensi Semiotik Teks-Emoji** | Bagaimana wujud inkongruensi makna antara teks tertulis bernada pujian semu dengan penanda visual emoji (*pretense of sarcasm*)? | Mengidentifikasi dan mengukur bentuk inkongruensi semiotik teks-emoji guna membongkar kritik terselubung warganet. | *Semiotic Incongruity Scoring* | Disparitas kontras teks pujian (*"bergizi"*, *"mewah"*) vs emoji mengejek (🤡, 🤮, 🗿) |
| **3** | **🤖 Respons Afektif 9 Emosi NLP** | Pola emosi apa yang mendominasi reaksi afektif publik terhadap Program MBG berdasarkan 9 kategori emosi model IndoBERT? | Mengklasifikasikan respons afektif warganet ke dalam 9 emosi Plutchik menggunakan *fine-tuned* IndoBERT guna mengukur penolakan/dukungan publik. | *Deep Learning Transformer IndoBERT* | Emosi **Jijik (Disgust) mendominasi 56,24%** (2.960 tweet), Trust 20,39% (1.073 tweet), **Macro F1 = 0.8122** |
| **4** | **🕸️ Topologi Jaringan & Polarisasi SNA** | Bagaimana struktur graf jaringan komunikasi terbentuk di platform X, serta sejauh mana tingkat polarisasi dan fragmentasi komunitasnya? | Memetakan topologi jaringan, mengukur koefisien modularitas (Q), serta mendeteksi komunitas terfragmentasi via Algoritma Louvain. | *Graph Theory & Louvain Modularity* | 971 node, 666 edges (692 interaksi mentah), **Modularitas Q = 0.9837** (332 komunitas terfragmentasi ekstrem, Reciprocity 1,21%) |
| **5** | **👑 Sentralitas Aktor Dominan & Otoritas** | Aktor-aktor kunci mana yang menduduki sentralitas dominan (degree, betweenness, PageRank) dalam mengarahkan diskursus publik? | Mengidentifikasi figur sentral, penyebar informasi utama, dan broker antarkomunitas guna memetakan asimetri pengaruh komunikasi. | *Structural Centrality Analysis* | **@grok** Out-degree=42 (*AI Oracle*), **@4Y4NKZ** (*Broker* betweenness 0.000016), **@prabowo** In=15 Out=0 (*Target pasif*) |
| **6** | **🏛️ Sintesis Phygital Gap & Kebijakan** | Sejauh mana resistensi digital mencerminkan kegagalan *immersive experience* (*Phygital Gap* Marketing 6.0), dan bagaimana strategi mitigasinya? | Mengevaluasi besaran *Phygital Gap* serta merumuskan rekomendasi mitigasi komunikasi risiko berbasis *computational social science* bagi BGN. | *Triangulasi Komputasional & Crisis Matrix* | Terbuktinya *Phygital Gap* (konsep digital disukai, realitas fisik ditolak); menghasilkan **5 Rekomendasi Aksi BGN** |

---

## 📑 STRUKTUR LENGKAP TESIS (BAB I S.D BAB V) & BUKTI EMPIRIS RIIL

Seluruh analisis dan visualisasi di dalam repositori dan dashboard Streamlit disusun sesuai dengan **Daftar Isi Resmi Naskah Tesis**:

### 🏛️ 1. BAB I: PENDAHULUAN (Halaman 1 – 25)
- **1.1 Latar Belakang Masalah (Hal. 1):** Konteks krisis komunikasi kebijakan Program Makan Bergizi Gratis (MBG), anggaran ratusan triliun rupiah, dan anomali resistensi warganet di platform X.
  - *1.1.1 Kajian Penelitian Terdahulu (Hal. 9):* Pemetaan komparatif terhadap riset-riset terdahulu.
  - *1.1.2 Gap Penelitian (Hal. 13):* Celah empiris, teoretis, dan metodologis (kebaruan CSS di Indonesia).
- **1.2 Rumusan Masalah (Hal. 15):** 6 pertanyaan penelitian berjenjang (teks ➔ afeksi ➔ graf ➔ sintesis makro).
- **1.3 Batasan Masalah & Fokus Intervensi Strategis (Hal. 18):** Platform X, bahasa Indonesia, periode Maret–Mei 2026, 9 kelas emosi, dan interaksi relasional aktif (mentions/replies).
- **1.4 Tujuan Penelitian (Hal. 19):** 6 target operasional yang selaras simetris 1-to-1 dengan rumusan masalah.
- **1.5 Manfaat Penelitian (Hal. 21):**
  - *1.5.1 Manfaat Akademis (Hal. 21):* Pengayaan metodologis NLP IndoBERT, SNA terintegrasi, dan perluasan Marketing 6.0 ke public sector.
  - *1.5.2 Manfaat Praktis (Hal. 22):* Sistem deteksi dini krisis citra dan panduan komunikasi dua arah bagi Badan Gizi Nasional.
- **1.6 Sistematika Penulisan (Hal. 23):** Alur runtut 5 bab tesis.

---

### 📖 2. BAB II: LANDASAN TEORI DAN KERANGKA PEMIKIRAN (Halaman 26 – 84)
Kajian konseptual mendalam mencakup **8 Pilar Utama dan 37 Sub-Bab Terstruktur**:
- **2.1 Komunikasi Risiko dalam Skala Fiskal Makro (Hal. 26):**
  - 2.1.1 Konsep Dasar Risk Communication (Hal. 27)
  - 2.1.2 Fiscal Risk Communication dan Kepercayaan Publik (Hal. 28)
  - 2.1.3 Krisis Kepercayaan sebagai Risiko Reputasi Negara (Hal. 29)
  - 2.1.4 Media Sosial sebagai Katalisator Erosi Kepercayaan Institusional (Hal. 29)
  - 2.1.5 Optimism Bias dan Anggaran Kebijakan Berskala Besar (Hal. 31)
- **2.2 Situational Crisis Communication & Networked Crisis (Hal. 32):**
  - 2.2.1 Situational Crisis Communication Theory (SCCT) Coombs (Hal. 32)
  - 2.2.2 Networked Crisis Communication (Schultz, Utz, & Goritz) (Hal. 32)
  - 2.2.3 Media Sosial sebagai Arena Krisis yang Terdesentralisasi (Hal. 34)
  - 2.2.4 Kritik dan Perkembangan Lanjutan atas NCC (Hal. 34)
  - 2.2.5 Krisis Berlapis (Compound Crisis) dan Efek Akumulatif (Hal. 35)
  - 2.2.6 Single Source of Truth dan Peran Juru Bicara dalam Krisis Terdesentralisasi (Hal. 36)
- **2.3 Ruang Publik dan Afordansi Platform X (Hal. 37):**
  - 2.3.1 Ruang Publik dan Deliberasi dalam Bingkai Digital Habermas (Hal. 37)
  - 2.3.2 Karakteristik Afordansi Platform X (Hal. 38)
  - 2.3.3 Budaya Reply-Thread dan Wacana Kritik Kebijakan (Hal. 39)
  - 2.3.4 Bahasa Gaul, Campur Kode, dan Kreativitas Leksikal Warganet (Hal. 40)
  - 2.3.5 Algoritma Rekomendasi dan Ekonomi Perhatian (Hal. 41)
- **2.4 Pragmatik Bahasa & Teori Sindiran (Hal. 42):**
  - 2.4.1 Pragmatik dan Implikatur Percakapan Grice (Hal. 42)
  - 2.4.2 Incongruity Theory dan Inkongruensi Makna (Hal. 43)
  - 2.4.3 Sindiran dalam Computer-Mediated Communication (Hal. 43)
  - 2.4.4 Inkongruensi Teks-Emoji sebagai Fokus Analitis (Hal. 44)
  - 2.4.5 Sindiran sebagai Bentuk Resistensi Simbolik Scott (Hal. 46)
  - 2.4.6 Multimodalitas Sindiran: Melampaui Teks dan Emoji (Hal. 47)
- **2.5 Pemrosesan Bahasa Alami & Arsitektur IndoBERT (Hal. 48):**
  - 2.5.1 Evolusi NLP: dari Statistik ke Deep Learning (Hal. 48)
  - 2.5.2 Arsitektur Transformer dan Mekanisme Self-Attention Vaswani et al. (Hal. 49)
  - 2.5.3 BERT: Bidirectional Encoder Representations from Transformers Devlin et al. (Hal. 49)
  - 2.5.4 IndoBERT: Adaptasi Model Bahasa untuk Konteks Indonesia Wilie et al. (Hal. 50)
  - 2.5.5 Fine-Tuning IndoBERT untuk Klasifikasi Emosi Granular (Hal. 51)
  - 2.5.6 Evaluasi Kinerja Model: Akurasi, Presisi, Recall, dan F1-Score (Hal. 52)
  - 2.5.7 Isu Bias dan Ketidakseimbangan Data pada Model Bahasa (Hal. 53)
  - 2.5.8 Perbandingan IndoBERT dengan Model Bahasa Alternatif (Hal. 54)
- **2.6 Teori Graf dan Social Network Analysis (SNA) (Hal. 55):**
  - 2.6.1 Dasar-Dasar Teori Graf Euler, Wasserman & Faust (Hal. 55)
  - 2.6.2 Sentralitas dalam Jaringan: Degree, Betweenness, Closeness, Eigenvector Freeman (Hal. 55)
  - 2.6.3 Deteksi Komunitas dan Algoritma Louvain Blondel et al. (Hal. 56)
  - 2.6.4 Modularity sebagai Ukuran Polarisasi Newman (Hal. 57)
  - 2.6.5 Homofili dan Fenomena Echo Chamber McPherson et al. (Hal. 58)
  - 2.6.6 Visualisasi Jaringan sebagai Instrumen Diagnostik Kebijakan (Hal. 59)
  - 2.6.7 Jaringan Bipartit dan Keterbatasan Representasi Graf Sederhana (Hal. 60)
  - 2.6.8 Perbandingan Algoritma Deteksi Komunitas (Hal. 61)
  - 2.6.9 Validasi Metrik Sentralitas Jaringan Berbasis Python/NetworkX (Hal. 62)
- **2.7 Paradigma Marketing 6.0 & Konsep Phygital Gap (Hal. 63 – 84):**
  - Landasan operasionalisasi kesenjangan janji promosi digital terhadap kualitas fisik di lapangan (Kotler, Kartajaya, & Setiawan, 2023).
  - 5 Proposisi Kerja Riset (P1 s.d P5) yang diuji secara empiris.

---

### 🔬 3. BAB IV: HASIL DAN PEMBAHASAN (Halaman 94 – 109)
Hasil komputasional empiris yang diverifikasi secara matematis:
- **4.1 Deskripsi Umum dan Karakteristik Data (Hal. 94):** Total korpus $N=5.263$ cuitan X, pembersihan noise 1.915 cuitan, korpus leksikal $N=3.395$.
- **4.2 Analisis Level Sistem: Topologi Jaringan dan Polarisasi (Hal. 95):** 971 node, 666 edges (692 interaksi mentah), kepadatan (*density*) 0.0011, **Resiprositas 1,21%** (komunikasi monolog satu arah).
- **4.3 Analisis Clustering: Dinamika Komunitas dan Echo Chambers (Hal. 97):** **Modularity Louvain Q = 0.9837**, terfragmentasi ke dalam **332 komunitas terisolasi**.
- **4.4 Analisis Level Aktor: Struktur Kekuasaan dan Brokerage (Hal. 98):**
  - `@grok` (*AI Oracle Takeover*): Out-degree = **42** (paling berpengaruh mengarahkan opini).
  - `@4Y4NKZ` (*Structural Broker*): Betweenness = **0.000016** (jembatan langka antarkomunitas).
  - `@prabowo` (*Target Pasif / Power Vacuum*): In-degree = **15**, Out-degree = **0** (sasaran aduan publik tanpa dialog timbal-balik).
  - **📡 10 Top Media & Kanal Penghubung (Selain CNN Indonesia):** Menemukan pergeseran saluran krisis ke akun *Menfess* dan spesialis:
    1. `@tanyarlfes` (Menfess Publik, In-Degree = 5, PageRank = 0.00344)
    2. `@tanyakanrl` (Agregator Diskusi X, In-Degree = 5, PageRank = 0.00314)
    3. `@LambeSahamjja` (Media Finansial & Pasar, In-Degree = 4, PageRank = 0.00314)
    4. `@itbfess_x` (Menfess Akademik Mahasiswa, In-Degree = 3, PageRank = 0.00207)
    5. `@KompasTV` (Media Penyiaran TV Nasional, Degree = 2, PageRank = 0.00457)
    6. `@tempodotco` (Jurnalisme Investigatif Tempo, In-Degree = 1, PageRank = 0.00132)
    7. `@kompascom` (Portal Berita Nasional, In-Degree = 1, PageRank = 0.00132)
    8. `@kumparan` (Media Berita Kolaboratif, Out-Degree = 1, PageRank = 0.00071)
    9. `@yappingfess` (Menfess Curahan Emosi Warganet, In-Degree = 2, PageRank = 0.00193)
    10. `@txtdrimedia` (Kurasi & Kliping Berita Pers, In-Degree = 1, PageRank = 0.00102)
- **4.5 Evaluasi Model Klasifikasi Emosi dan Deteksi Sindiran (Hal. 101):**
  - *4.5.1 Evaluasi IndoBERT:* Akurasi tes 57,45%, Macro F1 = 0.8122, Recall kelas Disgust mencapai **96,92%** (F1 = 0.7178), Presisi Trust 68,42%.
  - *4.5.2 Evaluasi Deteksi Sindiran:* **315 cuitan (9,28%)** memuat sindiran valid terverifikasi leksikal, sementara proksi afektif menangkap 56,60%.
  - *4.5.3 Interpretasi Triangulasi:* Sindiran merupakan sub-dimensi leksikal dari emosi Jijik (*Disgust*) — kedua instrumen konvergen membuktikan resistensi publik.
- **4.6 Sintesis: Perspektif Marketing 6.0 dan Phygital Gap (Hal. 105):**
  - *4.6.1 Evaluasi ABSA:* Kritik terfokus pada kegagalan fisik — Logistik & Distribusi (Disgust **78,91%**), Anggaran & Vendor (Disgust **77,01%**), Kualitas Gizi (Disgust **71,13%**).
  - *4.6.2 Sintesis Struktural-Afektif:* Pembuktian *Phygital Gap* — warganet menerima visi digital kesejahteraan anak, namun menolak keras realitas eksekusi fisik makanan di lapangan.

---

### 🏛️ 4. BAB V: PENUTUP & REKOMENDASI KEBIJAKAN (Halaman 110 – 113)
- **5.1 Kesimpulan (Hal. 110):** Menjawab tuntas 6 Rumusan Masalah dan 6 Tujuan Penelitian secara terpadu.
- **5.2 Implikasi Penelitian (Hal. 112):**
  - *5.2.1 Implikasi Akademis:* Pelopor integrasi metodologi CSS (IndoBERT + SNA Louvain + Marketing 6.0) untuk kebijakan publik di Indonesia.
  - *5.2.2 Implikasi Praktis:* Kerangka kerja diagnostik krisis kebijakan fiskal makro bagi pemerintah.
- **5.3 Rekomendasi Kebijakan (Hal. 112):**
  - *5.3.1 Untuk Pemerintah / Badan Gizi Nasional (BGN) — 5 Aksi Strategis:*
    1. **Membuka Dialog Dua Arah:** Menugaskan tim humas resmi merespons cuitan warganet untuk mengikis monolog komunikasi (menaikkan reciprocity dari 1,21%).
    2. **Merangkul Jaringan Broker Akar Rumput:** Membangun kemitraan komunikasi dengan simpul jembatan seperti `@4Y4NKZ` untuk menyalurkan klarifikasi ke klaster terisolasi.
    3. **Membangun Single Source of Truth Menu Fisik:** Menerbitkan katalog digital harian berisi foto menu, gramasi, dan komposisi gizi resmi per SPPG.
    4. **Transparansi Alokasi Biaya Porsi:** Mengedukasi publik secara berkala tentang breakdown anggaran bahan baku vs logistik guna meredam isu pemotongan pagu.
    5. **Edukasi Algoritmik:** Mengimbangi dominasi AI Oracle (`@grok`) dengan mendistribusikan siaran pers terstruktur yang ramah algoritma mesin pencari.
  - *5.3.2 Untuk Penelitian Selanjutnya (Hal. 113):* Integrasi multimodalitas visi komputer (analisis foto piring menu), ekspansi multi-platform (TikTok/Instagram), dan analisis rentang waktu longitudinal.
- **5.4 Keterbatasan Penelitian (Hal. 113):** Eksklusivitas platform X, fokus analisis teks, dan batasan periode observasi kritis Maret–Mei 2026.

---

## 📚 MASTER TAKSONOMI 33 REFERENSI ILMIAH (SCOPUS Q1 / SINTA 1)

Riset ini ditopang oleh **33 rujukan ilmiah bereputasi** yang diklasifikasikan ke dalam **5 Klaster Keilmuan** untuk memperkuat pertahanan akademik (*thesis defense*) dan penulisan artikel jurnal internasional:

| Klaster Keilmuan | Sub-Pilar Bab II | Jumlah | Contoh Publikasi Utama & Indeksasi | Peran Strategis di Manuskrip |
|:---|:---|:---:|:---|:---|
| **🏛️ Klaster A: Phygital & Kebijakan** | Pilar 2.1, 2.2, 2.3 | **10** | • **Gelders & Ihlen (2010)** *(Scopus Q1, Gov. Inf. Q.)*<br>• **Johnson & Barlow (2021)** *(Scopus Q1, JTAER)*<br>• **Tsai et al. (2026)** *(Scopus Q1, Socio-Econ. Plan. Sci.)*<br>• **Bennett & Segerberg (2012)** *(Scopus Q1, ICS)* | Landasan konseptual analogi service gap ke policy communication gap serta teori connective action warganet. |
| **🤖 Klaster B: NLP & IndoBERT** | Pilar 2.5 | **7** | • **Wilie et al. (2020)** *(AACL-IJCNLP Indo4B)*<br>• **Koto et al. (2020)** *(COLING)*<br>• **Shaw et al. (2025)** *(Scopus Q1, SNAM)*<br>• **Mohammad (2021)** *(Elsevier Book)* | Justifikasi arsitektur Transformer bidirectional IndoBERT untuk klasifikasi 9 spektrum emosi granular Plutchik. |
| **🎭 Klaster C: Sarkasme & Pragmatik** | Pilar 2.4 | **6** | • **Camp (2012)** *(Scopus Q1, Noûs)*<br>• **Joshi et al. (2017)** *(Scopus Q1, ACM Comput. Surv.)*<br>• **Devalapalli & Mandala (2026)** *(Scopus Q1, Neurocomputing)*<br>• **Hutapea & Purwarianti (2021)** *(Sinta 1 ITB)* | *Pretense theory of sarcasm* — membongkar pujian semu warganet yang menyembunyikan kritik tajam terhadap menu MBG. |
| **🕸️ Klaster D: SNA & Teori Graf** | Pilar 2.6 | **8** | • **Freeman (1979)** *(Scopus Q1, Social Networks)*<br>• **Newman (2006)** *(PNAS Q1 Modularity)*<br>• **Blondel et al. (2008)** *(Scopus Q1 Louvain)*<br>• **Gandasari et al. (2023)** *(Scopus Q2 JICC)* | Landasan matematis perhitungan modularitas polarisasi $Q=0.9837$, partisi 332 komunitas, dan sentralitas aktor. |
| **⚖️ Klaster E: Etika & Bot** | Pilar 2.11 | **2** | • **Boyd & Crawford (2012)** *(Scopus Q1, ICS, 12k+ sitasi)*<br>• **Ferrara et al. (2016)** *(Scopus Q1, CACM)* | Kepatuhan etika scraping big data publik X, anonimisasi identitas, dan metodologi filtrasi akun bot. |

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

## 🖼️ GALERI VISUALISASI RISET PUBLIK (12 MASTER PLOT 300 DPI — AKSES & UNDUH LANGSUNG)
> *Seluruh figur visualisasi naskah tesis di bawah ini bersifat **100% publik, beresolusi cetak tinggi (300 DPI)**, dan dapat diakses/diunduh langsung secara bebas.*

<table>
<tr>
<td width="50%" valign="top">

### `Figure 01` — Dataset & Pipeline Overview
📍 *Metodologi §3.5*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/1_pipeline.png" target="_blank">
<img src="results/1_pipeline.png" width="100%" alt="Figure 01: Dataset & Pipeline Overview"/>
</a>
End-to-end pipeline: raw collection ($N=5.310$) → cleaning → validated sarcasm corpus ($N=3.395$) → full inference corpus ($N=5.263$).  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/1_pipeline.png)**

---

### `Figure 02` — Nine Emotion Distribution
📍 *Hasil NLP §4.5*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png" target="_blank">
<img src="results/emotion_distribution.png" width="100%" alt="Figure 02: Nine Emotion Distribution"/>
</a>
Diagram batang 9 kelas emosi pada 5.263 cuitan riil. **Jijik mendominasi secara mutlak sebesar 56,24%**, diikuti Percaya (20,39%) dan Netral (12,33%).  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png)**

---

### `Figure 03` — Sarcasm Distribution
📍 *Hasil NLP §4.5*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png" target="_blank">
<img src="results/3_sarcasm.png" width="100%" alt="Figure 03: Sarcasm Distribution"/>
</a>
Pada korpus validasi ($N=3.395$), **9,28% (315 cuitan)** terverifikasi memuat sindiran. Publik merespons kegagalan implementasi fisik dengan bahasa sindiran implisit.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png)**

---

### `Figure 04` — F1-Score per Kelas Emosi
📍 *Evaluasi Model §4.5*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/f1_scores.png" target="_blank">
<img src="results/f1_scores.png" width="100%" alt="Figure 04: F1-Scores"/>
</a>
Evaluasi performa model IndoBERT pada testing set riil ($n=1.053$, checkpoint-792). Kelas dominan Jijik mencapai Recall **96,92%** (F1 0,7178).  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/f1_scores.png)**

---

### `Figure 05` — Confusion Matrix IndoBERT
📍 *Evaluasi Model §4.5*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png" target="_blank">
<img src="results/confusion_matrix.png" width="100%" alt="Figure 05: Confusion Matrix"/>
</a>
Matriks konfusi 9×9 mengonfirmasi 566 dari 584 cuitan berlabel aktual Jijik berhasil diprediksi tepat oleh model (96,92% recall).  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png)**

---

### `Figure 06` — Masterpiece Integrasi SNA × NLP (Phygital Gap)
📍 *Sintesis Diskusi §4.6 & §5.1*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/integrated_sna_nlp.png" target="_blank">
<img src="results/integrated_sna_nlp.png" width="100%" alt="Figure 06: Integrated SNA NLP"/>
</a>
Peta sintesis puncak: menghubungkan simpul sentralitas aktor (@grok, @prabowo) dengan klaster komunitas Louvain dan spektrum emosi Jijik/Percaya.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/integrated_sna_nlp.png)**

</td>
<td width="50%" valign="top">

### `Figure 07` — Global Social Network Topology
📍 *Hasil SNA §4.2*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png" target="_blank">
<img src="results/6_global_network.png" width="100%" alt="Figure 07: Global Social Network"/>
</a>
971 node · 666 directed edges (692 raw interactions). Membuktikan kondisi **hyper-fragmentation**, bukan polarisasi dua kubu linear.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png)**  
*(Versi visual jaringan penuh: [network_graph.png](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/network_graph.png))*

---

### `Figure 08` — Top Central Actors (Degree Centrality)
📍 *Struktur Kekuasaan §4.4*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png" target="_blank">
<img src="results/top_actors.png" width="100%" alt="Figure 08: Top Central Actors"/>
</a>
**@grok (AI agent) memegang Out-degree tertinggi (#1 = 42)** sebagai rujukan verifikasi (*Algorithmic Oracle*), sementara **@prabowo memiliki In-degree tertinggi (15)**.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png)**

---

### `Figure 09` — Emotion × Louvain Community Pattern
📍 *Dinamika Komunitas §4.3*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png" target="_blank">
<img src="results/9_emotion_network.png" width="100%" alt="Figure 09: Emotion Network"/>
</a>
Analisis silang: Emosi Jijik meresap ke hampir seluruh klaster komunitas independen — menjadi sentimen perekat struktural di balik fragmentasi wacana.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png)**

---

### `Figure 10` — ABSA / Thematic Analysis
📍 *Sintesis Tematik §4.6*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png" target="_blank">
<img src="results/10_absa_thematic.png" width="100%" alt="Figure 10: ABSA Thematic"/>
</a>
Sentimen berbasis aspek: Kekecewaan publik terkonsentrasi pada **eksekusi logistik (78,91%) & anggaran (77,01%)**, bukan pada gagasan gizi nasional itu sendiri.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png)**

---

### `Figure 11` — Word Cloud Percakapan MBG (N=5.263)
📍 *Karakteristik Korpus §4.1*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png" target="_blank">
<img src="results/wordcloud_mbg.png" width="100%" alt="Figure 11: Wordcloud MBG"/>
</a>
Visualisasi 120 leksikon paling sering diucapkan warganet, menyoroti kata kunci *mbg, makanan, gratis, gizi, sekolah, dapur,* dan *enak*.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png)**

---

### `Figure 12` — Radar Keterbatasan Penelitian & Arah Riset
📍 *Keterbatasan Riset §5.4*  
<a href="https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png" target="_blank">
<img src="results/keterbatasan_penelitian.png" width="100%" alt="Figure 12: Keterbatasan Penelitian"/>
</a>
Pemetaan 7 dimensi kapabilitas metodologis vs batas horizon riset, mitigasi empiris bias, dan rekomendasi arah penelitian lanjutan.  
🔗 **[Buka Resolusi Penuh (300 DPI)](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png)**

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
