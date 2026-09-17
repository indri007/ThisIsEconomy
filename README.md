# INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)

Repositori ini berisi keseluruhan kode (*source code*), dataset, dan hasil analisis komputasional untuk tesis yang mengkaji **"Phygital Gap"** pada kebijakan Makan Bergizi Gratis (MBG) di Indonesia melalui platform sosial media X (Maret–Mei 2026).

🚀 **Akses Dashboard Interaktif Tesis MBG secara publik di sini: [https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/](https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/)**

Penelitian ini menggunakan pendekatan **Computational Social Science** yang menggabungkan *Natural Language Processing* (NLP) menggunakan model transformer **IndoBERT** dengan **Communication Network Analysis** (CNA / Analisis Jaringan Komunikasi) menggunakan algoritma Louvain.

---

## 🏗️ Arsitektur Riset (Pipeline)

Sistem ini dirancang secara modular dan berjalan melalui 3 tahapan (*pipeline*) utama:

1.  **Data Preprocessing & Annotation**
    *   **Input:** Data organik Twitter/X hasil *crawling* (3,395 cuitan unik).
    *   **Proses:** Pembersihan *noise* (URL, bot, *mention*), *stemming* (Sastrawi), dan labelisasi manual (*ground truth*) ke dalam 9 kategori emosi granular: *Anger, Disgust, Fear, Joy, Love, Neutral, Sadness, Shame, Surprise*.
    *   **Output:** `mbg_tweets_indobert_ready.xlsx`
2.  **Emotion Classification (NLP - IndoBERT)**
    *   **Input:** Teks yang telah dibersihkan.
    *   **Proses:** 
        *   Tokenisasi menggunakan `indobenchmark/indobert-base-p2`.
        *   *Fine-tuning* model Transformer berbasis PyTorch untuk klasifikasi 9 kelas (3 *epochs*, *batch size* 16).
        *   Evaluasi metrik (Accuracy, Macro F1, Precision, Recall) dengan penanganan *zero division* untuk kelas minoritas.
    *   **Output:** `indobert_finetuned` model checkpoints, `classification_report.csv`, `confusion_matrix.png`.
3.  **Topological Graph (Social Network Analysis)**
    *   **Input:** Data interaksi (*reply, quote, retweet*).
    *   **Proses:**
        *   Penyusunan *directed graph* menggunakan pustaka `NetworkX`.
        *   Kalkulasi sentralitas (*Degree, Betweenness, Eigenvector*).
        *   Deteksi komunitas/klaster menggunakan algoritma *Louvain* (mengukur *Modularity*).
    *   **Output:** `network_edges.csv`, `sna_results.csv`, plot *Network Fragmentation*.

---

## 📂 Struktur Direktori

```bash
tesis_mbg/
├── data/                  # Tempat penyimpanan dataset utama
│   ├── raw/               # Data mentah hasil crawling awal
│   ├── emotion/           # Dataset yang sudah dilabeli untuk IndoBERT
│   ├── sarcasm/           # Dataset khusus identifikasi sindiran (future use)
│   ├── sna/               # Data edge/node (source, target) untuk NetworkX
│   └── absa/              # Placeholder untuk Aspect-Based Sentiment
│
├── notebooks/             # Jupyter Notebooks untuk eksperimen iteratif
│   └── tesis_mbg.ipynb
│
├── scripts/               # Skrip Python untuk produksi (Production Code)
│   ├── preprocessing.py   # Pembersihan teks (Sastrawi, Regex)
│   ├── train_indobert.py  # Skrip fine-tuning IndoBERT (PyTorch/HuggingFace)
│   ├── evaluate.py        # Kalkulasi F1-Score & Confusion Matrix
│   └── sna.py             # Pemrosesan graf topology & Louvain Modularity
│
└── results/               # Seluruh output komputasi model
    ├── classification_report.csv
    ├── confusion_matrix.png
    └── sna_results.csv
```

---

## 🔬 Penjelasan Detail Metode

### 1. The Phygital Gap (Theoretical Framework)
Studi ini mengadopsi konsep *Phygital Gap* (Marketing 6.0) untuk menjelaskan kegagalan komunikasi publik. *Gap* ini terjadi ketika janji manis pemerintah di dunia maya (pengentasan stunting) bertabrakan dengan realitas operasi fisik di lapangan (krisis logistik, keracunan). 

### 2. Natural Language Processing (IndoBERT)
Pendekatan *binary sentiment analysis* (Positif/Negatif) tidak mampu membedakan tingkat kekecewaan publik secara akurat. Oleh karena itu, penelitian ini menggunakan **IndoBERT** yang merupakan model bahasa berbasis *bidirectional transformer* pra-latih (Pre-trained) dari *corpus* bahasa Indonesia raksasa. Model ini mampu menangkap konteks kalimat bolak-balik sehingga sangat jitu dalam mendeteksi sarkasme dan makian khas *slang* netizen Indonesia (misalnya membedakan antara makian marah *Anger* dan cibiran *Disgust*). **Akurasi final: 83%.**

### 3. Communication Network Analysis (CNA)
Untuk menguji bagaimana afeksi (emosi) publik ini didistribusikan, CNA diaplikasikan untuk merekonstruksi interaksi netizen menjadi "jaringan komunikasi". 
*   **Modularity (0.9837):** Angka yang ekstrem ini membuktikan bahwa tidak terjadi polarisasi dua kubu besar (pro vs anti pemerintah), melainkan *Hyper-Fragmentation*—netizen terpecah ke dalam 333 gelembung kecil yang saling mengeluh sendiri tanpa berdiskusi silang.
*   **Algorithmic Trust:** Analisis Eigenvector menemukan bahwa bukan akun institusi atau menteri yang paling berpengaruh di jaringan, melainkan agen AI (**@grok**). Publik menjadikan AI sebagai pilar verifikator akhir saat kredibilitas manusia runtuh.

---

## 🚀 Cara Menjalankan Kode (How to Run)

1. **Persiapan Lingkungan (Environment Setup)**
   ```bash
   conda create -n mbg_env python=3.10
   conda activate mbg_env
   pip install torch transformers pandas scikit-learn networkx matplotlib seaborn python-louvain
   ```
2. **Training Model IndoBERT**
   ```bash
   python scripts/train_indobert.py
   ```
3. **Evaluasi Metrik Model**
   ```bash
   python scripts/evaluate.py
   ```
4. **Menghasilkan Metrik dan Plot SNA**
   ```bash
   python scripts/sna.py
   ```

---
*Dikembangkan untuk keperluan Tesis Magister Bidang Komunikasi / Computational Social Science.*
