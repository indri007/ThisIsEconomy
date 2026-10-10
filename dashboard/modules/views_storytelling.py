import os
import sys
import re
import json
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components

from dashboard.modules.config import (
    PROJECT_ROOT,
    get_data_path,
    get_result_path,
    resolve_image_path,
    get_journal_docx_path,
    download_file_button,
    send_telegram_alert,
    PYVIS_AVAILABLE,
    WORDCLOUD_AVAILABLE,
    MATPLOTLIB_AVAILABLE,
)
from dashboard.modules.data_loader import (
    load_emotion_data,
    load_network_data,
    load_final_evaluation,
)
from dashboard.modules.ui_components import render_thesis_stepper

if PYVIS_AVAILABLE:
    from pyvis.network import Network

if WORDCLOUD_AVAILABLE:
    from wordcloud import WordCloud

if MATPLOTLIB_AVAILABLE:
    import matplotlib.pyplot as plt


def render_storytelling_page():
    st.title("🖼️ Galeri Visual Storytelling (10 Master Plot Tesis)")
    st.markdown("""
    > *Galeri visual interaktif ini merangkai 10 grafik utama naskah tesis secara kronologis
    > dari alur praproses, pemodelan NLP IndoBERT, topologi SNA Louvain, hingga Masterpiece Visual Phygital Gap.*
    """)
    st.title("🖼️ Visual Storytelling")

    st.info("""
    ### 📖 Filosofi Storytelling
    **Gambar 1-3: Data Apa yang Dianalisis?**
    *(Mendokumentasikan tahapan pemrosesan data, didominasi emosi Disgust dengan balutan sarkasme tingkat tinggi).*

    **Gambar 4-5: Bagaimana Model Membacanya?**
    *(Mendokumentasikan evaluasi arsitektur IndoBERT, meski agak kesulitan membedakan sarkasme Anger vs Disgust).*

    **Gambar 6-8: Siapa Terhubung dengan Siapa, dan Siapa Aktornya?**
    *(Menunjukkan struktur jaringan yang terfragmentasi, dan AI/grok memiliki out-degree tertinggi dalam graf yang dianalisis).*

    **Gambar 9-10: Bagaimana Emosi Membentuk Diskursus?**
    *(Menganalisis pola emosi dalam korpus memiliki distribusi teks terkait aspek logistik dan anggaran; hubungan dengan konsep Phygital Gap dibahas sebagai interpretasi konseptual, bukan bukti kausal).*
    """)


    # Define paths & crash-proof image rendering
    def get_image_path(filename):
        resolved = resolve_image_path(filename)
        if resolved:
            return resolved
        return get_result_path(filename)

    with st.expander("🕊️ Read Narrative Essay: A Meal of Ash and Irony (The Human Soul Behind Indonesia’s Trillion-Rupiah Promise)", expanded=False):
        essay_path = os.path.join(PROJECT_ROOT, "docs", "A_MEAL_OF_ASH_AND_IRONY.md")
        if os.path.exists(essay_path):
            with open(essay_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Narrative essay file is available in docs/A_MEAL_OF_ASH_AND_IRONY.md")

    v_tabs = st.tabs([
        "🌟 Galeri Lengkap (10 Gambar)",
        "🔍 Tahap 1: Praproses Data",
        "🤖 Tahap 2: NLP & IndoBERT",
        "🕸️ Tahap 3: CNA & Aktor",
        "💥 Tahap 4: Sintesis Phygital Masterpiece",
        "🏛️ Bab IV & Bab V: Peta Temuan Empiris & Rekomendasi (§4.1 - §5.4)"
    ])

    # ── TAB 1: GALERI LENGKAP ──
    with v_tabs[0]:
        st.markdown("### 🔍 Bagian I: Data Apa yang Dianalisis?")
        st.success("**Mendokumentasikan tahapan pemrosesan data, didominasi emosi Disgust dengan balutan sarkasme tingkat tinggi.**")

        st.subheader("1. Dataset & Data Collection Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.image(get_image_path("1_pipeline.png"), width='stretch', caption="Gambar 1A. Pipeline Komputasional Riset")
        with col2:
            st.image(get_image_path("2_dataset_characteristics.png"), width='stretch', caption="Gambar 1B. Tahapan Penyaringan Data")
        st.info("**Caption Akademik:** Figure 1 illustrates the end-to-end data processing pipeline and cleaning process from raw Twitter API scrapes (N=5,310) to the final annotated corpus (N=3,395).\n\n**Pesan/Temuan:** Ketegasan dan ketelitian arsitektur riset yang terukur secara komputasional.\n\n**Posisi Manuskrip:** Bab III Metodologi (§3.5)")
        st.markdown("---")

        st.subheader("2. Distribusi 9 Kategori Emosi")
        st.image(get_image_path("emotion_distribution.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 2 displays the distribution of predicted emotion labels; Disgust dominates (56.24%), followed by Trust (20.39%), Neutral (12.33%), and Interest (9.60%); labels are silver-standard.\n\n**Pesan/Temuan:** Distribusi emosi digunakan sebagai data analitik dan tidak diinterpretasikan secara substantif sebelum rekonsiliasi dataset.\n\n**Posisi Manuskrip:** Bab IV Hasil NLP (§4.5)")
        st.markdown("---")

        st.subheader("3. Karakteristik Sarkasme")
        st.image(get_image_path("3_sarcasm.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 3 highlights the prevalence of sarcasm and irony in public reactions, functioning as a primary coping mechanism toward logistical failures.\n\n**Pesan/Temuan:** Dataset menunjukkan adanya cuitan yang terklasifikasi sebagai sindiran; temuan ini dilaporkan sebagai karakteristik data tanpa menyimpulkan motif komunikasi publik.\n\n**Posisi Manuskrip:** Bab IV Hasil NLP (§4.5)")
        st.markdown("---")

        st.markdown("### 🤖 Bagian II: Bagaimana Model Membacanya?")
        st.success("**Mendokumentasikan evaluasi arsitektur IndoBERT mendeteksi emosi penolakan (evaluasi klasifikasi model).**")

        st.subheader("4. Kinerja IndoBERT (F1-Scores)")
        st.image(get_image_path("f1_scores.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 4 presents the normalized confusion matrix of the fine-tuned IndoBERT classifier on the group-aware test set (n = 1,058), which was never used for training or checkpoint selection: accuracy 75.99%, Macro-F1 0.4535, Weighted-F1 0.7434.\n\n**Pesan/Temuan:** Kelas dominan terdeteksi baik (Jijik F1 0,82; Netral 0,80; Percaya 0,70), sedangkan Tertarik kurang terdeteksi (recall 0,30) dan kelas minoritas Marah/Sedih tidak terprediksi.\n\n**Posisi Manuskrip:** Bab IV Evaluasi Model (§4.5)")
        st.markdown("---")

        st.subheader("5. Confusion Matrix Klasifikasi Emosi (Data Riil)")
        st.image(get_image_path("confusion_matrix_v2.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 5 details the classification confusion matrix on actual data, revealing high sensitivity on Disgust and high precision on Trust.\n\n**Pesan/Temuan:** Integritas dan transparansi komputasional dalam mengevaluasi kekuatan serta keterbatasan representasi korpus imbalanced.\n\n**Posisi Manuskrip:** Bab IV Evaluasi Model (§4.5)")
        st.markdown("---")

        st.markdown("### 🕸️ Bagian III: Siapa Terhubung dengan Siapa, dan Siapa Aktornya?")
        st.success("**Menunjukkan struktur jaringan yang terfragmentasi, dan AI (@grok) menduduki posisi sentral aktor dengan out-degree tinggi.**")

        st.subheader("6. Struktur Jaringan Global (SNA Topology)")
        st.image(get_image_path("6_global_network.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 6 visualizes the unclustered global network (971 nodes, 666 edges), showing sparse connectivity and lack of a central dialogue hub.\n\n**Pesan/Temuan:** Graf jaringan terdiri atas 341 weakly connected components; temuan ini digunakan untuk mendeskripsikan struktur keterhubungan jaringan, bukan untuk mengukur polarisasi ideologis.\n\n**Posisi Manuskrip:** Bab IV Hasil CNA (§4.2)")
        st.markdown("---")

        st.subheader("7. Struktur Komunitas Louvain (Modularity 0.9837)")
        st.image(get_image_path("network_graph.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 7 demonstrates the strong community structure of the network into 342 detected communities. Colors represent the detected community structure in the network.\n\n**Pesan/Temuan:** Struktur komunitas yang kuat (Modularity 0.9837) menunjukkan keterpisahan struktural antarkomunitas.\n\n**Posisi Manuskrip:** Bab IV Hasil CNA (§4.3)")
        st.markdown("---")

        st.subheader("8. 15 Aktor Sentral Tertinggi (Perbandingan Centrality Aktor)")
        st.image(get_image_path("top_actors.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 8 ranks the discourse leaders. The @grok dominates the network's out-degree influence (42), memiliki out-degree 42, sedangkan @prabowo memiliki in-degree 15; metrik tersebut hanya digunakan untuk mendeskripsikan posisi struktural dalam graf.\n\n**Pesan/Temuan:** Perbedaan posisi structural centrality. Perbedaan out-degree menggambarkan pola keterhubungan yang berbeda antaraktor; data jaringan tidak digunakan untuk menyimpulkan pergeseran otoritas kebenaran.\n\n**Posisi Manuskrip:** Bab IV Hasil CNA (§4.4)")
        st.markdown("---")

        st.subheader("🎨 Visualisasi Khusus Material Design 3: Hubungan Komunikasi Antar-Akun Twitter")
        st.markdown(
            "Visualisasi interaktif dengan sistem desain **Google Material Design 3 (M3 Dark Theme)** "
            "memetakan arah komunikasi asimetris antar-aktor: **High In-Degree Targets** (`@prabowo`), "
            "**High-Betweenness Actors** (`@regar_op0sisi`), **akun dengan out-degree tinggi** (`@grok`), dan klaster sarkasme warganet."
        )
        c_m3_1, c_m3_2 = st.columns([11, 7])
        with c_m3_1:
            st.image(get_image_path("15_material3_network_interaction.png"), width='stretch', caption="Visualisasi Empiris M3: Topologi Relasi Antar-Akun Platform X (Data Riil |V|=971, |E|=666, 300 DPI)")
        with c_m3_2:
            m3_mock_path = os.path.join(PROJECT_ROOT, "docs", "assets", "m3_twitter_network_ui.png")
            if os.path.exists(m3_mock_path):
                st.image(m3_mock_path, width='stretch', caption="Konsep Material Design 3 UI: Hubungan Interaksi Twitter X")
        st.info("**Pesan Kunci Material 3:** Hubungan komunikasi bersifat *asimetris* — akun dengan in-degree tinggi menjadi target mention yang menerima gelombang mention sepihak dengan reciprocity yang rendah, sementara *High-Betweenness Actor* oposisi memiliki posisi struktural dalam jaringan dan AI (*Grok*) dijadikan *akun dengan out-degree tinggi* aktor dengan out-degree tinggi.")
        st.markdown("---")

        st.subheader("📊 Visualisasi Standar Industri: NodeXL Pro Group-in-a-Box (GIB) Layout")
        st.markdown(
            "Visualisasi kanonis **NodeXL Pro** ([Lisensi Akademik Resmi Order #14103](https://nodexl.com/my-account/view-order/14103/)) "
            "dengan tata letak *Group-in-a-Box (GIB)* yang mengelompokkan simpul aktor ke dalam kotak partisi tematik, "
            "dilengkapi panel parameter graf baku NodeXL Graph Metrics Pane:"
        )
        st.image(
            get_image_path("16_nodexl_graph_visualization.png"),
            width='stretch',
            caption="Visualisasi Empiris NodeXL Pro: Group-in-a-Box Network Topology & Graph Pane Metrics (|V|=971, |E|=666, 300 DPI)"
        )
        st.info("**Pesan Kunci NodeXL Pro:** Tata letak Group-in-a-Box (GIB) menampilkan struktur kelompok yang teridentifikasi dalam partisi jaringan sembari menampilkan interkoneksi lintas batas (*inter-group bridge edges*) dan parameter global jaringan (*Graph Density = 0.00071, Modularity Q = 0.9837*).")
        st.markdown("---")

        st.markdown("### 💥 Bagian IV: Bagaimana Emosi Membentuk Diskursus?")
        st.info("**Interpretasi dalam kerangka Phygital Gap:** Temuan afektif dan aspek logistik/gizi dianalisis sebagai bagian dari hubungan antara wacana digital dan konteks implementasi fisik program.")

        st.subheader("9. Emotion × Network (Phygital Overlay)")
        st.image(get_image_path("9_emotion_network.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 9 correlates emotions with structural communities. Disgust permeates almost all fragmented clusters, acting as a unifying sentiment against logistical failures.\n\n**Pesan/Temuan:** Emosi jijik (Disgust) bukan sekadar opini acak, melainkan sentimen sistemik yang merata di seluruh klaster komunitas.\n\n**Posisi Manuskrip:** Bab V Pembahasan (§5.2)")
        st.markdown("---")

        st.subheader("10. ABSA / Thematic Network (3 Aspek Kebijakan)")
        st.image(get_image_path("10_absa_thematic.png"), width='stretch')
        st.info("**Caption Akademik:** Figure 10 highlights that public dissatisfaction is heavily directed toward logistical and budget aspects rather than the policy's conceptual merit, providing evidence relevant to the Phygital Gap framework.\n\n**Pesan/Temuan:** Temuan ini dibahas melalui kerangka Phygital Gap untuk menghubungkan wacana digital dengan aspek implementasi fisik yang muncul dalam data.\n\n**Posisi Manuskrip:** Bab V Pembahasan (§5.3)")
        st.markdown("---")

        st.subheader("🌟 Visual Masterpiece: Integrated Phygital Gap Analysis")
        st.image(get_image_path("integrated_sna_nlp.png"), width='stretch')
        st.success("**Master Visual ini merangkai 3 panel (Global Topology → Louvain Community → Integrasi Klaster × Emosi Riil) yang menjawab rumusan masalah secara holistik.**")

    # ── TAB 2: TAHAP 1 ──
    with v_tabs[1]:
        st.subheader("🔍 Tahap 1: Pipeline Riset & Karakteristik Data")
        st.markdown("Tahapan praproses data dari kueri scraping hingga korpus bersih teranotasi:")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.image(get_image_path("1_pipeline.png"), width='stretch', caption="Gambar 1A: End-to-End Computational Pipeline")
        with col_t2:
            st.image(get_image_path("2_dataset_characteristics.png"), width='stretch', caption="Gambar 1B: Data Preprocessing & Cleaning Funnel")
        st.image(get_image_path("emotion_distribution.png"), width='stretch', caption="Gambar 2: Distribusi Label Emosi (N=5.263; Jijik 56,24%)")

    # ── TAB 3: TAHAP 2 ──
    with v_tabs[2]:
        st.subheader("🤖 Tahap 2: NLP & Kinerja Model IndoBERT")
        st.markdown("Evaluasi klasifikasi emosi multi-kelas dan deteksi sindiran linguistik:")
        col_t3_a, col_t3_b = st.columns(2)
        with col_t3_a:
            st.image(get_image_path("3_sarcasm.png"), width='stretch', caption="Gambar 3: Distribusi Sarkasme & Penanda Linguistik")
        with col_t3_b:
            st.image(get_image_path("f1_scores.png"), width='stretch', caption="Gambar 4: F1-Scores IndoBERT per Kategori Emosi")
        st.image(get_image_path("confusion_matrix_v2.png"), width='stretch', caption="Gambar 5: Confusion Matrix Evaluasi IndoBERT Group-Aware (test set n=1.058)")

    # ── TAB 4: TAHAP 3 ──
    with v_tabs[3]:
        st.subheader("🕸️ Tahap 3: Communication Network Analysis (CNA)")
        st.markdown("Topologi makro, fragmentasi komunitas, dan hierarki sentralitas aktor:")
        st.image(get_image_path("6_global_network.png"), width='stretch', caption="Gambar 6: Struktur Graf Jaringan Global (971 Nodes, 666 Edges)")
        col_t4_a, col_t4_b = st.columns(2)
        with col_t4_a:
            st.image(get_image_path("network_graph.png"), width='stretch', caption="Gambar 7: Partisi Komunitas Louvain (Modularity 0.9837)")
        with col_t4_b:
            st.image(get_image_path("top_actors.png"), width='stretch', caption="Gambar 8: Sentralitas Aktor Utama (@grok vs @prabowo)")

        st.markdown("---")
        st.subheader("🎨 Visualisasi Material Design 3: Topologi Relasi Komunikasi Antar-Akun")
        st.image(get_image_path("15_material3_network_interaction.png"), width='stretch', caption="Gambar 8B: Pemetaan Interaksi Antar-Akun Platform X dalam Estetika Google Material 3 (300 DPI)")

        st.markdown("---")
        st.subheader("📊 Visualisasi Standar Industri: NodeXL Pro Group-in-a-Box (GIB) Layout")
        st.image(get_image_path("16_nodexl_graph_visualization.png"), width='stretch', caption="Gambar 8C: Pemetaan Jaringan Komunikasi Versi NodeXL Pro Group-in-a-Box Layout (300 DPI)")

        st.markdown("---")
        st.subheader("📊 Visualisasi Parameter Makro Topologi: NodeXL & NetworkX")
        st.image(get_image_path("17_macro_topology_metrics.png"), width='stretch', caption="Gambar 8D: Analisis Empiris Struktur Makro Topologi Jaringan Komunikasi MBG (300 DPI)")

        st.markdown("---")
        st.subheader("📊 Visualisasi Sentralitas Aktor & Tipologi Peran Komunikasi: Dimensi 2")
        st.image(get_image_path("18_actor_centrality_typology.png"), width='stretch', caption="Gambar 8E: Pemetaan Sentralitas Aktor & Tipologi Peran Komunikasi (High In-Degree Target, Oracle, Broker, 300 DPI)")

        st.markdown("---")
        st.subheader("📊 Visualisasi Partisi Komunitas & Deteksi Struktur Komunitas: Dimensi 3")
        st.image(get_image_path("19_community_echo_chambers.png"), width='stretch', caption="Gambar 8F: Analisis Empiris Partisi Komunitas Louvain & Struktur Internal Komunitas (300 DPI)")

    # ── TAB 5: TAHAP 4 ──
    with v_tabs[4]:
        st.subheader("💥 Tahap 4: Sintesis Marketing 6.0 & Phygital Gap")
        st.markdown("Integrasi temuan afektif dan struktural untuk menginterpretasikan wacana melalui kerangka Phygital Gap:")
        col_t5_a, col_t5_b = st.columns(2)
        with col_t5_a:
            st.image(get_image_path("9_emotion_network.png"), width='stretch', caption="Gambar 9: Overlay Emosi Dominan pada Komunitas Jaringan")
        with col_t5_b:
            st.image(get_image_path("10_absa_thematic.png"), width='stretch', caption="Gambar 10: Analisis Sentimen 3 Aspek (Logistik, Anggaran, Gizi)")
        st.image(get_image_path("integrated_sna_nlp.png"), width='stretch', caption="Masterpiece Visual: Triangulasi Terintegrasi SNA x NLP (Data Riil)")

    # ── TAB 6: BAB IV & BAB V ──
    with v_tabs[5]:
        st.subheader("🏛️ Peta Temuan Empiris Bab IV & Rekomendasi Kebijakan Bab V (§4.1 - §5.4)")
        st.markdown(
            "Sintesis komprehensif yang menghubungkan seluruh temuan analitik komputasional "
            "dengan kesimpulan akademis dan matriks rekomendasi kebijakan publik Badan Gizi Nasional (BGN)."
        )
        col_b4, col_b5 = st.columns(2)
        with col_b4:
            st.markdown("### 📊 BAB IV: HASIL & PEMBAHASAN EMPIRIS")
            with st.expander("📌 §4.1 Karakteristik Korpus & Preprocessing", expanded=True):
                st.markdown("""
                - **Volume Data:** Total korpus mentah 5.310 cuitan platform X, tersaring menjadi 3.395 data bersih (N=3.395).
                - **Penyaringan Noise:** Eliminasi bot spam, duplikasi, dan akun agregator menggunakan 5 pilar verifikasi.
                - **Distribusi Emosi:** Didominasi oleh emosi **Disgust (56,24%)**, diikuti Trust (20,39%), Neutral (12,33%), dan Interest (9,60%).
                """)
            with st.expander("📌 §4.2 Topologi Makro & Kerapatan Jaringan"):
                st.markdown("""
                - **Parameter Jaringan:** 971 node dan 666 edge (Graph Density = 0,00071).
                - **Resiprositas Rendah:** Reciprocity = 1,21% — mencerminkan komunikasi asimetris satu arah.
                - **Fragmentasi Graf:** Terbagi ke dalam 341 komponen terpisah tanpa satu sentral dialog nasional.
                """)
            with st.expander("📌 §4.3 Struktur Komunitas Louvain (Modularity Q=0.9837)"):
                st.markdown("""
                - **Tingkat Polarisasi:** Modularitas Q = 0,9837 menandakan segregasi echo chamber yang sangat kuat.
                - **Jumlah Komunitas:** Terdeteksi 342 komunitas partisi lokal yang terisolasi secara struktural.
                """)
            with st.expander("📌 §4.4 Sentralitas Aktor & Tipologi Peran Komunikasi"):
                st.markdown("""
                - **AI Oracle (@grok):** Out-degree tertinggi (42) — difungsikan publik sebagai mesin verifikasi argumen.
                - **Target Mention Pasif (@prabowo):** In-degree 15, Out-degree 0 — target aduan publik tanpa keterlibatan langsung.
                - **Grassroots Broker (@4Y4NKZ, @regar_op0sisi):** Sentralitas perantara penghubung klaster warganet.
                """)
            with st.expander("📌 §4.5 Kinerja IndoBERT & Analisis Sarkasme"):
                st.markdown("""
                - **Kinerja Klasifikasi:** Fine-tuned IndoBERT mencapai F1-Macro 0,7522 (Group-Aware Evaluated).
                - **Deteksi Sarkasme:** Disgust menjadi wadah utama ekspresi satire/ironi terhadap kebijakan fisik.
                """)
            with st.expander("📌 §4.6 Sintesis Phygital Gap"):
                st.markdown("""
                - **ABSA 3 Aspek:** Sentimen penolakan terkonsentrasi pada Logistik & Anggaran fisik, bukan visi gizi.
                - **Phygital Disconnect:** Jurang pemisah nyata antara narasi digital dan realitas eksekusi makanan di lapangan.
                """)

        with col_b5:
            st.markdown("### 🏛️ BAB V: KESIMPULAN & REKOMENDASI KEBIJAKAN")
            with st.expander("📌 §5.1 Kesimpulan Penelitian Terpadu", expanded=True):
                st.markdown("""
                1. **Anatomi Bahasa:** Kritik diartikulasikan lewat ironi dan oposisi biner di ruang digital.
                2. **Dominasi Afektif:** Emosi Jijik (*Disgust* 56,24%) merefleksikan kecemasan higienitas dan porsi.
                3. **Topologi Asimetris:** Polarisasi ekstrem (Q=0,9837) dengan resiprositas rendah (1,21%).
                4. **Hegemoni AI:** Publik beralih ke agen AI (@grok) akibat minimnya dialog dua arah dari pembuat kebijakan.
                5. **Phygital Gap:** Terkonfirmasi secara empiris kesenjangan antara narasi digital dan realitas fisik.
                """)
            with st.expander("📌 §5.2 Implikasi Akademis & Praktis"):
                st.markdown("""
                - **Implikasi Akademis:** Menetapkan metodologi komputasional terpadu (SNA x NLP) untuk sosiologi komunikasi publik Indonesia.
                - **Implikasi Praktis:** Memberikan kerangka kerja EWS multi-dimensi untuk deteksi dini sentimen krisis kebijakan publik.
                """)
            with st.expander("📌 §5.3 5 Rekomendasi Aksi untuk BGN"):
                st.markdown("""
                1. **Buka Dialog Terbuka:** Tingkatkan resiprositas dari 1,21% dengan kanal tanggapan humas aktif.
                2. **Rangkul Simpul Komunitas:** Kolaborasi dengan opinion leader non-formal untuk penetrasi klaster terisolasi.
                3. **Single Source of Truth Menu:** Publikasikan foto menu fisik harian dan uji laboratorium gizi per SPPG.
                4. **Transparansi Alokasi Anggaran:** Edukasi publik rincian biaya porsi untuk memutus narasi korupsi.
                5. **Optimalisasi Narasi Berbasis Bukti:** Siapkan data terbuka tervalidasi mesin pencari dan agen AI.
                """)
            with st.expander("📌 §5.4 Keterbatasan & Agenda Riset Lanjutan"):
                st.markdown("""
                - **Platform:** Fokus pada data platform X (Twitter); disarankan ekspansi ke TikTok/Instagram.
                - **Modalitas:** Analisis teks; riset lanjutan dapat mengintegrasikan computer vision pada foto menu fisik.
                """)

        st.markdown("---")
        st.subheader("📋 Matriks Pemetaan Komprehensif: Struktur Tesis Bab I – Bab V ↔ Bukti Data Riil")
        thesis_master_map = [
            {"Bab Tesis": "Bab I: Pendahuluan", "Sub-Bab": "1.2 & 1.4 Rumusan & Tujuan", "Fokus Kajian": "Harmonisasi 6 Pertanyaan ↔ 6 Target Riset", "Metode / Instrumen": "Sankey Flow & Matriks Keselarasan", "Data Empiris": "Harmonisasi simetris 1-to-1", "Halaman": "15 & 19"},
            {"Bab Tesis": "Bab II: Landasan Teori", "Sub-Bab": "2.1 s.d 2.6 Landasan Konseptual", "Fokus Kajian": "8 Pilar Teori & 37 Sub-Bab Terstruktur", "Metode / Instrumen": "Sunburst & Treemap Hierarkis", "Data Empiris": "37 Sub-bab, 5 Proposisi Kerja", "Halaman": "26 – 84"},
            {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.1 Karakteristik Data Korpus", "Fokus Kajian": "Penyaringan cuitan warganet platform X", "Metode / Instrumen": "Data Funnel & Preprocessing Pipeline", "Data Empiris": "N=5.263 korpus, 3.395 leksikal", "Halaman": "94"},
            {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.2 Topologi Jaringan Global", "Fokus Kajian": "Analisis kerapatan & resiprositas graf", "Metode / Instrumen": "Directed Graph SNA", "Data Empiris": "971 node, Reciprocity 1,21%", "Halaman": "95"},
            {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.3 Dinamika Komunitas Louvain", "Fokus Kajian": "Polarisasi ekstrem & echo chamber warganet", "Metode / Instrumen": "Algoritma Louvain Community", "Data Empiris": "Modularity Q=0.9837, 342 komunitas", "Halaman": "97"},
            {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.4 Struktur Kekuasaan Aktor", "Fokus Kajian": "Peran Oracle AI, Broker, dan Target Pasif", "Metode / Instrumen": "Centrality (Degree, Betweenness)", "Data Empiris": "@grok Out=42, @prabowo In=15 Out=0", "Halaman": "98"},
            {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.5 Evaluasi Model & Sindiran", "Fokus Kajian": "Performa IndoBERT & majas sindiran", "Metode / Instrumen": "Fine-tuned Transformer IndoBERT", "Data Empiris": "Macro F1 0.7522, Disgust 56,24%", "Halaman": "101 – 104"},
            {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.6 Sintesis Marketing 6.0", "Fokus Kajian": "Pembuktian Phygital Gap kebijakan publik", "Metode / Instrumen": "ABSA & Triangulasi SNA-NLP", "Data Empiris": "Logistik & anggaran sebagai akar krisis", "Halaman": "105 – 109"},
            {"Bab Tesis": "Bab V: Penutup", "Sub-Bab": "5.1 s.d 5.4 Simpulan & Solusi", "Fokus Kajian": "Rekomendasi BGN & Implikasi Kebijakan", "Metode / Instrumen": "Matriks Intervensi Kebijakan", "Data Empiris": "5 Aksi Strategis Mitigasi Krisis", "Halaman": "110 – 113"}
        ]
        st.dataframe(pd.DataFrame(thesis_master_map), use_container_width=True, hide_index=True)

