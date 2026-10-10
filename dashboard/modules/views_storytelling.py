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


    # Define paths
    def get_image_path(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        path = os.path.join(project_root, "results", filename)
        return path

    with st.expander("🕊️ Read Narrative Essay: A Meal of Ash and Irony (The Human Soul Behind Indonesia’s Trillion-Rupiah Promise)", expanded=False):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        essay_path = os.path.join(project_root, "docs", "A_MEAL_OF_ASH_AND_IRONY.md")
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
        st.image(os.path.join(PROJECT_ROOT, "results", "indobert_group_aware_v2", "confusion_matrix_v2.png") if os.path.exists(os.path.join(PROJECT_ROOT, "results", "indobert_group_aware_v2", "confusion_matrix_v2.png")) else get_image_path("confusion_matrix.png"), width='stretch')
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
            m3_mock_path = os.path.join(project_root, "docs", "assets", "m3_twitter_network_ui.png")
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
        st.image(os.path.join(PROJECT_ROOT, "results", "indobert_group_aware_v2", "confusion_matrix_v2.png") if os.path.exists(os.path.join(PROJECT_ROOT, "results", "indobert_group_aware_v2", "confusion_matrix_v2.png")) else get_image_path("confusion_matrix.png"), width='stretch', caption="Gambar 5: Confusion Matrix Evaluasi IndoBERT Group-Aware (test set n=1.058)")

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



