import os

def update_readme():
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Update Table header and rows with visual column
    old_table_header = "| No | Nama Dataset / File | Format | Volume Data | Status Missing Value | Tautan Langsung Publik (*Klik / Salin URL*) |"
    new_table_header = "| No | Nama Dataset / File | Format | Volume Data | Status Missing Value | Unduh Dataset Publik | Visualisasi Bukti Grafis (*Resolusi Tinggi 300 DPI*) |"

    text = text.replace(old_table_header, new_table_header)
    text = text.replace("| :---: | :--- | :---: | :---: | :---: | :--- |", "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |")

    # Update table rows
    text = text.replace(
        "| **1** | **Dataset 9 Emosi IndoBERT (Fixed)** | CSV | 5.263 cuitan | 0 Null (100% Bersih) | [`data/results/indobert_9_emosi_fixed.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/indobert_9_emosi_fixed.csv) |",
        "| **1** | **Dataset 9 Emosi IndoBERT (Fixed)** | CSV | 5.263 cuitan | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/indobert_9_emosi_fixed.csv) | [🖼️ Lihat Plot Distribusi Emosi](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png) |"
    )
    text = text.replace(
        "| **2** | **Dataset Deteksi Sindiran & Sarkasme** | CSV | 3.395 cuitan | 0 Null (100% Bersih) | [`data/sarcasm/dataset_sindiran_valid.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sarcasm/dataset_sindiran_valid.csv) |",
        "| **2** | **Dataset Deteksi Sindiran & Sarkasme** | CSV | 3.395 cuitan | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sarcasm/dataset_sindiran_valid.csv) | [🖼️ Lihat Plot Validasi Sindiran](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png) |"
    )
    text = text.replace(
        "| **3** | **Dataset Bersih Pasca-Preprocessing** | CSV | 5.309 cuitan | 0 Null (100% Bersih) | [`data/processed/data_clean.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/processed/data_clean.csv) |",
        "| **3** | **Dataset Bersih Pasca-Preprocessing** | CSV | 5.309 cuitan | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/processed/data_clean.csv) | [🖼️ Lihat Plot Alur Preprocessing](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/2_dataset_characteristics.png) |"
    )
    text = text.replace(
        "| **4** | **Dataset Benchmark Anotasi Emosi MBG** | Excel (`.xlsx`) | 3.395 baris | 0 Anomali Kritis | [`data/emotion/mbg_tweets_indobert_ready.xlsx`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/emotion/mbg_tweets_indobert_ready.xlsx) |",
        "| **4** | **Dataset Benchmark Anotasi Emosi MBG** | Excel (`.xlsx`) | 3.395 baris | 0 Anomali Kritis | [`📥 Unduh Excel`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/emotion/mbg_tweets_indobert_ready.xlsx) | [🖼️ Lihat Wordcloud Leksikon MBG](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png) |"
    )
    text = text.replace(
        "| **5** | **Relasi Jaringan Komunikasi SNA (Edges)** | CSV | 692 interaksi (666 unik) | 0 Null (100% Bersih) | [`data/sna/network_edges.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sna/network_edges.csv) |",
        "| **5** | **Relasi Jaringan Komunikasi SNA (Edges)** | CSV | 692 interaksi (666 unik) | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/sna/network_edges.csv) | [🖼️ Lihat Graf Global Jaringan SNA](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png) |"
    )
    text = text.replace(
        "| **6** | **Partisi Node & Komunitas Louvain** | CSV | 971 node terklaster | 0 Null (100% Bersih) | [`results/mbg_network_nodes_final.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/mbg_network_nodes_final.csv) |",
        "| **6** | **Partisi Node & Komunitas Louvain** | CSV | 971 node terklaster | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/mbg_network_nodes_final.csv) | [🖼️ Lihat Graf Komunitas & Emosi](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png) |"
    )
    text = text.replace(
        "| **7** | **Peringkat Sentralitas Derajat Aktor** | CSV | 986 aktor terindeks | 0 Null (100% Bersih) | [`data/results/sna_degree.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/sna_degree.csv) |",
        "| **7** | **Peringkat Sentralitas Derajat Aktor** | CSV | 986 aktor terindeks | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/data/results/sna_degree.csv) | [🖼️ Lihat Plot Asimetri Aktor](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png) |"
    )
    text = text.replace(
        "| **8** | **Sentimen Berbasis Aspek (ABSA 3 Tema)** | CSV | 3 pilar tematik fisik | 0 Null (100% Bersih) | [`results/absa_results.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/absa_results.csv) |",
        "| **8** | **Sentimen Berbasis Aspek (ABSA 3 Tema)** | CSV | 3 pilar tematik fisik | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/absa_results.csv) | [🖼️ Lihat Plot 3 Pilar Phygital Gap](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png) |"
    )
    text = text.replace(
        "| **9** | **Laporan Metrik Evaluasi Model IndoBERT** | CSV | 10 baris metrik resmi | 0 Null (100% Bersih) | [`results/classification_report.csv`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/classification_report.csv) |",
        "| **9** | **Laporan Metrik Evaluasi Model IndoBERT** | CSV | 10 baris metrik resmi | 0 Null (100% Bersih) | [`📥 Unduh CSV`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/classification_report.csv) | [🖼️ Lihat Confusion Matrix Model](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png) |"
    )
    text = text.replace(
        "| **10** | **Visual Keterbatasan Penelitian (Bab V)** | PNG 300 DPI | Resolusi Ultra-HD | Gambar Orisinal 1.1 MB | [`results/keterbatasan_penelitian.png`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png) |",
        "| **10** | **Visual Keterbatasan Penelitian (Bab V)** | PNG 300 DPI | Resolusi Ultra-HD | Gambar Orisinal 1.1 MB | [`📥 Unduh PNG HD`](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png) | [🖼️ Lihat Radar Chart 5 Keterbatasan](https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/keterbatasan_penelitian.png) |"
    )

    # 2. Add visual previews under each dataset in Codebook
    img_d1 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/emotion_distribution.png\" width=\"85%\" alt=\"Distribusi 9 Emosi IndoBERT\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D1:</b> Visualisasi Distribusi 9 Emosi Hasil Inferensi IndoBERT (Disgust 56,24%, Trust 20,39%, Neutral 12,33%, Anticipation 9,60%). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d2 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/3_sarcasm.png\" width=\"85%\" alt=\"Karakteristik Majas Sindiran\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D2:</b> Visualisasi Validasi Majas Sindiran & Kontradiksi Semantik Teks-Emoji (N=3.395, 315 Sindiran Valid 9,28%). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d3 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/2_dataset_characteristics.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/2_dataset_characteristics.png\" width=\"85%\" alt=\"Karakteristik Dataset & Tahap Preprocessing\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D3:</b> Karakteristik Korpus Data dari Mentah Scraped (N=5.310) hingga Korpus Bersih Preprocessing (N=5.309). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d4 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/wordcloud_mbg.png\" width=\"80%\" alt=\"Wordcloud Leksikon MBG\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D4:</b> Wordcloud 120 Leksikon Paling Signifikan dalam Korpus Teranotasi MBG. Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d5 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/6_global_network.png\" width=\"85%\" alt=\"Graf Global Jaringan SNA\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D5:</b> Topologi Graf Global Jaringan Sosial MBG (971 Nodes, 666 Directed Edges, Kepadatan 0.0011, Resiprositas 1,21%). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d6 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/9_emotion_network.png\" width=\"85%\" alt=\"Graf Komunitas Louvain & Emosi\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D6:</b> Partisi Komunitas Louvain (Q = 0.9837, 332 Klaster) yang Ditumpangkan dengan Sebaran Emosi Dominan. Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d7 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/top_actors.png\" width=\"85%\" alt=\"Peringkat Sentralitas Derajat Aktor\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D7:</b> Peringkat Sentralitas Derajat Aktor Membuktikan Asimetri Kekuasaan (@grok Out=42 vs @prabowo In=15, Out=0). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d8 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/10_absa_thematic.png\" width=\"85%\" alt=\"Visualisasi Sentimen Berbasis Aspek\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D8:</b> Pembuktian Empiris Phygital Gap pada 3 Aspek Fisik (Logistik 78,91% Disgust, Anggaran 77,01% Disgust, Mutu Gizi 71,13% Disgust). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    img_d9 = (
        "\n* **Bukti Visualisasi Publik (Resolusi Tinggi 300 DPI):**\n"
        "<div align=\"center\">\n"
        "  <a href=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png\" target=\"_blank\">\n"
        "    <img src=\"https://raw.githubusercontent.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/main/results/confusion_matrix.png\" width=\"85%\" alt=\"Confusion Matrix IndoBERT\"/>\n"
        "  </a>\n"
        "  <br/>\n"
        "  <sub><b>Gambar D9:</b> Confusion Matrix Klasifikasi Emosi IndoBERT pada Data Uji Riil (n=1.053). Klik gambar untuk membuka resolusi penuh.</sub>\n"
        "</div>\n"
    )

    # Insert under each dataset
    target_d1 = "* **Temuan Kunci:** Emosi **Disgust (Jijik)** mendominasi secara absolut dengan **56,24% (2.960 cuitan)**, mencerminkan resistensi viseral terhadap menu fisik MBG."
    if target_d1 in text:
        text = text.replace(target_d1, target_d1 + img_d1)

    target_d2 = "* **Temuan Kunci:** Teridentifikasi 181 cuitan dengan pola oposisi biner tajam (misal leksikon pujian semu *\"mewah/bergizi\"* yang dipadukan dengan konteks keluhan porsi minim atau emoji ejekan 🤡, 🤮, 🗿)."
    if target_d2 in text:
        text = text.replace(target_d2, target_d2 + img_d2)

    target_d3 = "teks terfilter (`clean_text`), dan teks ternormalisasi (`processed_text`)."
    if target_d3 in text:
        text = text.replace(target_d3, target_d3 + img_d3)

    target_d4 = "waktu, metrik keterlibatan, dan skor agregat interaksi (*engagement score*)."
    if target_d4 in text:
        text = text.replace(target_d4, target_d4 + img_d4)

    target_d5 = "* **Temuan Kunci:** Kepadatan jaringan sangat renggang (*Density = 0.0011*) dengan tingkat timbal-balik (*Reciprocity*) hanya **1,21%**, membuktikan pola komunikasi yang terjadi bersifat searah (*one-way broadcast*)."
    if target_d5 in text:
        text = text.replace(target_d5, target_d5 + img_d5)

    target_d6 = "* **Temuan Kunci:** Skor modularitas graf mencapai **$Q = 0.9837$** (mendekati batas teoritis 1.0), membuktikan fragmentasi wacana ke dalam **332 komunitas terisolasi**."
    if target_d6 in text:
        text = text.replace(target_d6, target_d6 + img_d6)

    target_d7 = "* **Temuan Kunci:** Membuktikan fenomena *Algorithmic Oracle* (`@grok`, Out-degree = 42) yang menggantikan peran lembaga pemerintah di tengah kekosongan komunikasi (*Power Vacuum* `@prabowo`, In-degree = 15, Out-degree = 0)."
    if target_d7 in text:
        text = text.replace(target_d7, target_d7 + img_d7)

    target_d8 = "* **Temuan Kunci:** Sentimen penolakan terbukti berkonsentrasi pada aspek operasional fisik: Logistik (**78,91% Disgust**), Anggaran (**77,01% Disgust**), dan Kualitas Gizi (**71,13% Disgust**)."
    if target_d8 in text:
        text = text.replace(target_d8, target_d8 + img_d8)

    target_d9 = "  - `support` (*int64*): Jumlah data uji aktual per-kelas pada populasi $n=1.053$."
    if target_d9 in text:
        text = text.replace(target_d9, target_d9 + img_d9)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("Updated README.md with direct visual previews successfully.")

if __name__ == "__main__":
    update_readme()
