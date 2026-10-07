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


def render_bab2_page():
    render_thesis_stepper(2)
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">📖 Bab II Tesis — Kerangka Epistemologis & Teoretis</div>
        <div class="hero-title">Landasan Teori dan Kerangka Pemikiran</div>
        <div class="hero-desc">
            Peta komprehensif 8 pilar konseptual (Halaman 26 – 84), taksonomi komunikasi krisis fiskal,
            teori inkongruensi pragmatik, arsitektur komputasi deep learning IndoBERT, Social Network Analysis,
            serta sintesis operasionalisasi <b>Phygital Gap</b> dalam kerangka Marketing 6.0.
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px;">
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">🏛️ <b>8 Pilar Utama</b></span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">📑 <b>37 Sub-Bab Terstruktur</b></span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">📄 <b>Hal. 26 – 84 (59 Halaman)</b></span>
            <span style="background: rgba(34, 197, 94, 0.25); color: #86efac; padding: 5px 14px; border-radius: 8px; font-size: 0.85rem; border: 1px solid rgba(34, 197, 94, 0.4);">✨ <b>100% Sesuai Daftar Isi Tesis</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary KPI Badges
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        st.metric("🏛️ Pilar Utama Teori", "8 Domain", "Dari Fiskal ke SNA")
    with b_col2:
        st.metric("📑 Total Sub-Bab", "37 Bagian", "Kajian Mendalam & Rigor")
    with b_col3:
        st.metric("🎯 Proposisi Kerja", "5 Proposisi", "Evaluasi Berbasis Bukti Data")
    with b_col4:
        st.metric("🌐 Konstruk Inti", "Phygital Gap", "Marketing 6.0 Synthesis")

    st.markdown("---")

    # ─── INTERACTIVE HIERARCHY EXPLORER (SUNBURST & TREEMAP) ───
    st.header("🧭 Peta Interaktif Taksonomi Teori (Hierarki Bab II)")
    st.markdown("""
    Visualisasi di bawah memetakan seluruh **37 sub-bab** dari Bab II ke dalam hierarki interaktif.
    Klik pada salah satu pilar untuk melakukan *drill-down* ke sub-bagian dan halaman buku tesis.
    """)

    viz_type = st.radio("Pilih Mode Tampilan Visual:", ["🌟 Sunburst Radial (Lingkaran Bertingkat)", "🔲 Treemap Hierarkis (Proporsi Luas)"], horizontal=True)

    # Hierarchical Dataframe Construction (Robust path-based structure)
    hier_data = [
        # 2.1
        {'Pilar': '2.1 Risiko Fiskal Makro (Hal. 26)', 'SubBab': '2.1.1 Konsep Dasar Risk Comm (Hal. 27)', 'Deskripsi': 'Komunikasi risiko fiskal & transparansi', 'Bobot': 1},
        {'Pilar': '2.1 Risiko Fiskal Makro (Hal. 26)', 'SubBab': '2.1.2 Fiscal Risk & Kepercayaan (Hal. 28)', 'Deskripsi': 'Dampak beban APBN pada persepsi publik', 'Bobot': 1},
        {'Pilar': '2.1 Risiko Fiskal Makro (Hal. 26)', 'SubBab': '2.1.3 Risiko Reputasi Negara (Hal. 29)', 'Deskripsi': 'Kredibilitas fiskal & sovereign rating', 'Bobot': 1},
        {'Pilar': '2.1 Risiko Fiskal Makro (Hal. 26)', 'SubBab': '2.1.4 Erosi Kepercayaan Institusi (Hal. 29)', 'Deskripsi': 'Defisit kepercayaan terhadap institusi publik', 'Bobot': 1},
        {'Pilar': '2.1 Risiko Fiskal Makro (Hal. 26)', 'SubBab': '2.1.5 Optimism Bias Anggaran (Hal. 31)', 'Deskripsi': 'Overestimasi manfaat & underestimasi biaya', 'Bobot': 1},

        # 2.2
        {'Pilar': '2.2 Networked Crisis Comm (Hal. 32)', 'SubBab': '2.2.1 SCCT Titik Tolak (Coombs) (Hal. 32)', 'Deskripsi': 'Situational Crisis Communication Theory', 'Bobot': 1},
        {'Pilar': '2.2 Networked Crisis Comm (Hal. 32)', 'SubBab': '2.2.2 NCC (Schultz et al.) (Hal. 32)', 'Deskripsi': 'Dinamika krisis multi-aktor di era jejaring', 'Bobot': 1},
        {'Pilar': '2.2 Networked Crisis Comm (Hal. 32)', 'SubBab': '2.2.3 Krisis Terdesentralisasi (Hal. 34)', 'Deskripsi': 'Pusat kontrol narasi yang terpecah', 'Bobot': 1},
        {'Pilar': '2.2 Networked Crisis Comm (Hal. 32)', 'SubBab': '2.2.4 Kritik Lanjutan atas NCC (Hal. 34)', 'Deskripsi': 'Keterbatasan model respons krisis linear', 'Bobot': 1},
        {'Pilar': '2.2 Networked Crisis Comm (Hal. 32)', 'SubBab': '2.2.5 Compound Crisis & Akumulatif (Hal. 35)', 'Deskripsi': 'Tumpukan isu logistik, gizi & anggaran', 'Bobot': 1},
        {'Pilar': '2.2 Networked Crisis Comm (Hal. 32)', 'SubBab': '2.2.6 Single Source of Truth & Jubir (Hal. 36)', 'Deskripsi': 'Urgensi kanal otoritatif tunggal komunikasi krisis', 'Bobot': 1},

        # 2.3
        {'Pilar': '2.3 Ruang Publik & Afordansi X (Hal. 37)', 'SubBab': '2.3.1 Deliberasi Publik Digital (Hal. 37)', 'Deskripsi': 'Habermas dalam lanskap media sosial X/Twitter', 'Bobot': 1},
        {'Pilar': '2.3 Ruang Publik & Afordansi X (Hal. 37)', 'SubBab': '2.3.2 Karakteristik Afordansi X (Hal. 38)', 'Deskripsi': 'Fitur quote, repost, thread penentu dinamika wacana', 'Bobot': 1},
        {'Pilar': '2.3 Ruang Publik & Afordansi X (Hal. 37)', 'SubBab': '2.3.3 Budaya Reply-Thread & Kritik (Hal. 39)', 'Deskripsi': 'Konfrontasi argumen di kolom komentar warganet', 'Bobot': 1},
        {'Pilar': '2.3 Ruang Publik & Afordansi X (Hal. 37)', 'SubBab': '2.3.4 Slang & Campur Kode (Hal. 40)', 'Deskripsi': 'Bahasa satir warganet dan ekspresi vernakular', 'Bobot': 1},
        {'Pilar': '2.3 Ruang Publik & Afordansi X (Hal. 37)', 'SubBab': '2.3.5 Algoritma Rekomendasi & Atensi (Hal. 41)', 'Deskripsi': 'Amplifikasi konten polaritatif oleh rekomendasi platform', 'Bobot': 1},

        # 2.4
        {'Pilar': '2.4 Inkongruensi & Sindiran (Hal. 42)', 'SubBab': '2.4.1 Pragmatik & Implikatur (Hal. 42)', 'Deskripsi': 'Makna tersirat di balik ujaran literal', 'Bobot': 1},
        {'Pilar': '2.4 Inkongruensi & Sindiran (Hal. 42)', 'SubBab': '2.4.2 Incongruity Theory Makna (Hal. 43)', 'Deskripsi': 'Kesenjangan ekspektasi vs realitas empiris', 'Bobot': 1},
        {'Pilar': '2.4 Inkongruensi & Sindiran (Hal. 42)', 'SubBab': '2.4.3 Sindiran dalam CMC (Hal. 43)', 'Deskripsi': 'Bentuk ironi dalam interaksi berbasis komputer', 'Bobot': 1},
        {'Pilar': '2.4 Inkongruensi & Sindiran (Hal. 42)', 'SubBab': '2.4.4 Inkongruensi Teks-Emoji (Hal. 44)', 'Deskripsi': 'Pujian semu disertai emoji tawa/ironi', 'Bobot': 1},
        {'Pilar': '2.4 Inkongruensi & Sindiran (Hal. 42)', 'SubBab': '2.4.5 Sindiran Resistensi Simbolik (Hal. 46)', 'Deskripsi': 'Kritik warga sebagai bentuk counter-power rakyat', 'Bobot': 1},
        {'Pilar': '2.4 Inkongruensi & Sindiran (Hal. 42)', 'SubBab': '2.4.6 Multimodalitas Sindiran (Hal. 47)', 'Deskripsi': 'Kombinasi meme, foto menu, dan teks sarkas', 'Bobot': 1},

        # 2.5
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.1 Evolusi NLP: Statistik ke DL (Hal. 48)', 'Deskripsi': 'Transisi representasi n-gram ke dense transformer', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.2 Transformer & Self-Attention (Hal. 49)', 'Deskripsi': 'Mekanisme perhatian kontekstual bidirectional', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.3 Arsitektur Dasar BERT (Hal. 49)', 'Deskripsi': 'Devlin et al. pre-training MLM + NSP', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.4 IndoBERT Bhs Indonesia (Hal. 50)', 'Deskripsi': 'Pre-training korpus bahasa Indonesia 4B+ token', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.5 Fine-Tuning 9 Emosi Granular (Hal. 51)', 'Deskripsi': 'Klasifikasi multi-kelas emosi granular spesifik MBG', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.6 Evaluasi Akurasi & F1-Score (Hal. 52)', 'Deskripsi': 'Metrik Macro/Weighted F1 & Confusion Matrix', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.7 Bias & Imbalanced Data (Hal. 53)', 'Deskripsi': 'Mitigasi ketimpangan kelas emosi minoritas', 'Bobot': 1},
        {'Pilar': '2.5 IndoBERT & NLP (Hal. 48)', 'SubBab': '2.5.8 Komparasi Model Alternatif (Hal. 54)', 'Deskripsi': 'Benchmarking IndoBERT vs RoBERTa vs SVM', 'Bobot': 1},

        # 2.6
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.1 Dasar Teori Graf (Hal. 55)', 'Deskripsi': 'Node, edge, dan representasi matriks relasional', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.2 Sentralitas Derajat (Hal. 55)', 'Deskripsi': 'In-Degree, Out-Degree & keaktifan interaksi aktor', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.3 Deteksi Komunitas Louvain (Hal. 56)', 'Deskripsi': 'Optimasi modularitas partisi hierarkis', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.4 Modularity dan Struktur Komunitas (Hal. 57)', 'Deskripsi': 'Skor modularitas Q sebagai ringkasan struktur komunitas jaringan', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.5 Homofili & Community Structure (Hal. 58)', 'Deskripsi': 'Klasterisasi aktor berbasis kesamaan pandangan', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.6 Visualisasi Diagnostik (Hal. 59)', 'Deskripsi': 'Peta topologi aktor utama penggerak opini', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.7 Jaringan Bipartit (Hal. 60)', 'Deskripsi': 'Relasi dua moda antara pengguna dan narasi isu', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.8 Komparasi Algoritma Komunitas (Hal. 61)', 'Deskripsi': 'Louvain vs Girvan-Newman vs Walktrap', 'Bobot': 1},
        {'Pilar': '2.6 SNA & Teori Graf (Hal. 55)', 'SubBab': '2.6.9 Sentralitas Jaringan (Hal. 62)', 'Deskripsi': 'Betweenness, Closeness, & PageRank aktor kunci', 'Bobot': 1},

        # 2.9
        {'Pilar': '2.9 Kerangka Pemikiran (Hal. 74)', 'SubBab': '2.9.1 Kausalitas Konseptual (Hal. 77)', 'Deskripsi': 'Alur logis stimulus kebijakan MBG ke reaksi siber', 'Bobot': 1},
        {'Pilar': '2.9 Kerangka Pemikiran (Hal. 74)', 'SubBab': '2.9.2 Definisi Variabel Phygital (Hal. 78)', 'Deskripsi': 'Operasionalisasi diskrepansi fisik-digital program', 'Bobot': 1},

        # 2.10-11
        {'Pilar': '2.10-11 Proposisi & Etika (Hal. 80)', 'SubBab': '2.10 Proposisi Riset P1–P5 (Hal. 80)', 'Deskripsi': '5 proposisi kerja yang dievaluasi terhadap bukti data yang tersedia', 'Bobot': 1},
        {'Pilar': '2.10-11 Proposisi & Etika (Hal. 80)', 'SubBab': '2.11.1 Privasi & Ekspektasi Wajar (Hal. 83)', 'Deskripsi': 'Kepatuhan etika anonimisasi data media sosial', 'Bobot': 1},
        {'Pilar': '2.10-11 Proposisi & Etika (Hal. 80)', 'SubBab': '2.11.2 Akun Bot & Validitas Data (Hal. 83)', 'Deskripsi': 'Filtrasi noise dan validasi keaslian sentimen publik', 'Bobot': 1}
    ]

    df_hierarchy = pd.DataFrame(hier_data)

    if "Sunburst" in viz_type:
        fig_hier = px.sunburst(
            df_hierarchy,
            path=['Pilar', 'SubBab'],
            values='Bobot',
            color='Pilar',
            color_discrete_sequence=px.colors.qualitative.Prism,
            height=650
        )
        fig_hier.update_traces(
            textinfo="label",
            insidetextorientation='radial',
            hovertemplate="<b>%{label}</b><br>Jumlah Sub-Bab: %{value}<extra></extra>"
        )
        fig_hier.update_layout(
            margin=dict(t=20, l=20, r=20, b=20),
            paper_bgcolor="#0f172a",
            font=dict(family="Outfit, sans-serif", color="white", size=13)
        )
        st.plotly_chart(fig_hier, width='stretch')
    else:
        fig_hier = px.treemap(
            df_hierarchy,
            path=['Pilar', 'SubBab'],
            values='Bobot',
            color='Pilar',
            color_discrete_sequence=px.colors.qualitative.Prism,
            height=620
        )
        fig_hier.update_traces(
            hovertemplate="<b>%{label}</b><br>Jumlah Sub-Bab: %{value}<extra></extra>"
        )
        fig_hier.update_layout(
            margin=dict(t=20, l=20, r=20, b=20),
            paper_bgcolor="#0f172a",
            font=dict(family="Outfit, sans-serif", color="white", size=13)
        )
        st.plotly_chart(fig_hier, width='stretch')

    st.markdown("---")

    # ─── TAB-BASED EXPLORATION OF THE 8 THEORETICAL PILLARS ───
    st.header("📚 Eksplorasi Rinci 8 Pilar Landasan Teori")
    st.markdown("Pilih tab di bawah untuk menelaah landasan teoritis, rujukan akademis, dan implikasinya pada studi empiris MBG:")

    theory_tabs = st.tabs([
        "📉 2.1 Risiko Fiskal",
        "🚨 2.2 Networked Crisis",
        "🌐 2.3 Ruang Publik X",
        "😏 2.4 Inkongruensi Sindiran",
        "🧠 2.5 NLP & IndoBERT",
        "🕸️ 2.6 SNA & Graf",
        "🧩 2.9 Kerangka Pemikiran",
        "🎯 2.10 Proposisi & Etika"
    ])

    with theory_tabs[0]:
        st.subheader("📉 §2.1 Komunikasi Risiko dalam Skala Fiskal Makro (Halaman 26–31)")
        st.markdown("""
        Membahas konsekuensi komunikasi dari kebijakan belanja publik berskala masif (megaproject) di mana transparansi
        fiskal berbanding lurus dengan stabilitas reputasi pemerintahan.
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **2.1.1 Konsep Dasar Risk Communication (Hal. 27)**
            - Pertukaran informasi interaktif terkait besaran, urgensi, dan mitigasi risiko kebijakan publik kepada masyarakat luas.
            - Menghubungkan persepsi subjektif publik dengan data teknis implementasi di lapangan.

            **2.1.2 Fiscal Risk Communication dan Kepercayaan Publik (Hal. 28)**
            - Transparansi alokasi anggaran dan akuntabilitas vendor pengadaan pangan sebagai pilar utama menjaga legitimasi moral pemerintah.
            - Deviasi anggaran memicu kecurigaan sistemik dan sinisme publik.

            **2.1.3 Krisis Kepercayaan sebagai Risiko Reputasi Negara (Hal. 29)**
            - Kegagalan program pangan nasional tidak hanya berdampak operasional, tetapi bereskalasi menjadi krisis kepercayaan institusional terhadap kepemimpinan nasional.
            """)
        with c2:
            st.warning("""
            **2.1.4 Media Sosial sebagai Katalisator Erosi Kepercayaan Institusional (Hal. 29)**
            - Arsitektur media sosial mempercepat amplifikasi ketidakpuasan lokal (kasus nasi basi/keracunan di satu sekolah) menjadi krisis reputasi berskala nasional dalam hitungan jam.

            **2.1.5 Optimism Bias dan Anggaran Kebijakan Berskala Besar (Hal. 31)**
            - Kecenderungan pengambil kebijakan memproyeksikan keberhasilan program secara berlebihan (*planning fallacy*), sementara kesiapan logistik di daerah terpencil kerap diabaikan.
            - Celah antara proyeksi optimis vs realitas inilah yang melahirkan frustrasi massal.
            """)

    with theory_tabs[1]:
        st.subheader("🚨 §2.2 Networked Crisis Communication & SCCT (Halaman 32–36)")
        st.markdown("""
        Mengintegrasikan Situational Crisis Communication Theory (SCCT) dari Coombs ke dalam paradigma jejaring terdesentralisasi
        (Schultz, Utz, & Göritz).
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **2.2.1 Situational Crisis Communication Theory (SCCT) sebagai Titik Tolak (Hal. 32)**
            - Kerangka Coombs menilai tingkat tanggung jawab krisis yang diatribusikan publik kepada organisasi/pemerintah (*crisis responsibility*).
            - Atribusi krisis MBG berada pada kluster *preventable crisis* karena menyangkut standar kebersihan dan pemotongan anggaran.

            **2.2.2 Networked Crisis Communication (Schultz, Utz, & Göritz) (Hal. 32)**
            - Krisis di era digital tidak lagi bergerak linear dari institusi ke publik, melainkan terdistribusi horizontal antar warganet di jejaring sosial.

            **2.2.3 Media Sosial sebagai Arena Krisis yang Terdesentralisasi (Hal. 34)**
            - Warganet menjadi co-creator narasi krisis; informasi menyebar tanpa bergantung pada siaran pers formal kementerian.
            """)
        with c2:
            st.warning("""
            **2.2.4 Kritik dan Perkembangan Lanjutan atas NCC (Hal. 34)**
            - Menyoroti kelemahan strategi komunikasi krisis tradisional yang mengasumsikan publik pasif menerima klarifikasi otoritas.

            **2.2.5 Krisis Berlapis (Compound Crisis) dan Efek Akumulatif (Hal. 35)**
            - Insiden berulang (keracunan makanan di berbagai kota + isu pemotongan pagu) menciptakan efek akumulatif yang memperberat resistensi publik.

            **2.2.6 Single Source of Truth dan Peran Juru Bicara dalam Krisis Terdesentralisasi (Hal. 36)**
            - Ketika narasi resmi terlambat atau tidak transparan, warganet mencari rujukan alternatif di media sosial, memicu fenomena delegasi otoritas kepada pihak ketiga.
            """)

    with theory_tabs[2]:
        st.subheader("🌐 §2.3 Ruang Publik dan Deliberasi dalam Bingkai Digital (Halaman 37–41)")
        st.markdown("""
        Menganalisis afordansi teknologis Platform X dalam memfasilitasi wacana kritis, polarisasi, dan diskursus kebijakan publik.
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **2.3.1 Ruang Publik dan Deliberasi dalam Bingkai Digital (Hal. 37)**
            - Meninjau konsep Habermas tentang ruang publik di era digital: ruang deliberasi warga yang terfragmentasi oleh bias konfirmasi dan algoritma.

            **2.3.2 Karakteristik Afordansi Platform X (Hal. 38)**
            - Fitur *Retweet, Quote Tweet, Mentions, Threads, dan Bookmark* sebagai saluran amplifikasi kritik dan pengawasan sosial (*networked surveillance*).

            **2.3.3 Budaya Reply-Thread dan Wacana Kritik Kebijakan (Hal. 39)**
            - Utas (*threads*) panjang menjadi sarana warganet menyusun investigasi amatir (*open-source intelligence* / OSINT) membongkar kejanggalan menu di sekolah.
            """)
        with c2:
            st.warning("""
            **2.3.4 Bahasa Gaul, Campur Kode, dan Kreativitas Leksikal Warganet (Hal. 40)**
            - Warganet Indonesia memanfaatkan slang (*bgt, beneran, yaampun, porsinya kocak*), singkatan, dan campur kode untuk menyamarkan kritik tajam dari pemblokiran.

            **2.3.5 Algoritma Rekomendasi dan Ekonomi Perhatian (Hal. 41)**
            - Algoritma *For You* memprioritaskan konten dengan keterlibatan afektif tinggi (terutama amarah dan rasa jijik), mempercepat viralitas krisis MBG.
            """)

    with theory_tabs[3]:
        st.subheader("😏 §2.4 Teori Inkongruensi & Sindiran Digital (Halaman 42–47)")
        st.markdown("""
        Landasan linguistik dan pragmatik mengenai bagaimana sindiran (*sarcasm*) dan inkongruensi teks-emoji menjadi bentuk resistensi simbolik warganet.
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **2.4.1 Pragmatik dan Implikatur Percakapan (Grice) (Hal. 42)**
            - Pelanggaran maksim kualitas (*maxim of quality*): warganet sengaja menyampaikan pernyataan positif palsu untuk mengartikan makna negatif sebenarnya.

            **2.4.2 Incongruity Theory dan Inkongruensi Makna (Hal. 43)**
            - Tabrakan semantik antara ekspektasi logis (makanan bergizi seimbang) dan kenyataan yang dipotret (menu tahu tempe seadanya) melahirkan ironi dan gelak tawa sinis.

            **2.4.3 Sindiran dalam Computer-Mediated Communication (CMC) (Hal. 43)**
            - Ketiadaan intonasi suara dan ekspresi wajah di dunia maya dikompensasikan melalui pilihan diksi hiperbolis dan emoji.
            """)
        with c2:
            st.warning("""
            **2.4.4 Inkongruensi Teks-Emoji sebagai Fokus Analitis (Hal. 44)**
            - Diksi pujian (*"enak banget ya gratisan ini"*) yang disandingkan dengan emoji muntah 🤮 atau tawa menangis 😭 sebagai penanda kunci sindiran.

            **2.4.5 Sindiran sebagai Bentuk Resistensi Simbolik (Hal. 46)**
            - James C. Scott (*weapons of the weak*): sindiran memungkinkan publik mengkritik kekuasaan tanpa risiko konfrontasi frontal secara hukum atau politik.

            **2.4.6 Multimodalitas Sindiran: Melampaui Teks dan Emoji (Hal. 47)**
            - Perpaduan teks cuitan dengan foto piring kotor, tangkapan layar berita keracunan, dan meme sebagai paket komprehensif kritik sosial.
            """)

    with theory_tabs[4]:
        st.subheader("🧠 §2.5 NLP & Arsitektur IndoBERT (Halaman 48–54)")
        st.markdown("""
        Fondasi komputasional pemrosesan bahasa alami menggunakan transformer berbasis deep learning untuk klasifikasi 9 emosi granular Plutchik.
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **2.5.1 Evolusi Pemrosesan Bahasa Alami: Statistik ke Deep Learning (Hal. 48)**
            - Pergeseran dari bag-of-words dan n-gram menuju model representasi vektor berbasis konteks sekuensial.

            **2.5.2 Arsitektur Transformer dan Mekanisme Self-Attention (Hal. 49)**
            - Konsep Vaswani et al. (2017): kemampuan transformer mengkorelasikan ketergantungan antar-kata tanpa memedulikan jarak posisi dalam kalimat.

            **2.5.3 BERT: Bidirectional Encoder Representations from Transformers (Hal. 49)**
            - Pemahaman dua arah (kiri-ke-kanan dan kanan-ke-kiri) yang sangat krusial dalam mendeteksi kontradiksi makna dalam kalimat bersindiran.

            **2.5.4 IndoBERT: Adaptasi Model Bahasa untuk Konteks Indonesia (Hal. 50)**
            - Wilie et al. (2020): model pretrained pada miliaran token korpus bahasa Indonesia, mengenali ragam morfologi dan partikel percakapan lokal.
            """)
        with c2:
            st.warning("""
            **2.5.5 Fine-Tuning IndoBERT untuk Klasifikasi Emosi Granular 9 Kelas (Hal. 51)**
            - Adaptasi model pada taksonomi Plutchik (Marah, Jijik, Takut, Bahagia, Sedih, Kaget, Percaya, Tertarik, Netral) untuk menangkap nuansa afektif tajam.

            **2.5.6 Evaluasi Kinerja Model: Akurasi, Presisi, Recall, dan F1-Score (Hal. 52)**
            - Metrik standar evaluasi supervised learning pada data uji holdout group-aware ($n=1.058$, akurasi 75,99%, Macro F1 0,4535, Weighted F1 0,7434, F1 Jijik 0,8202; checkpoint dipilih via validation split).

            **2.5.7 Isu Bias dan Ketidakseimbangan Data (Imbalanced Data) (Hal. 53)**
            - Analisis dampak ketimpangan sampel kelas mayoritas (Jijik) terhadap macro-F1 pada kelas langka (Takut/Sedih).

            **2.5.8 Perbandingan IndoBERT dengan Model Bahasa Alternatif (Hal. 54)**
            - Mengapa IndoBERT lebih unggul dibandingkan LSTM, FastText, maupun mBERT standar untuk teks media sosial Indonesia.
            """)

    with theory_tabs[5]:
        st.subheader("🕸️ §2.6 Social Network Analysis & Teori Graf (Halaman 55–62)")
        st.markdown("""
        Fondasi struktural Social Network Analysis berbasis NetworkX dan Algoritma Louvain untuk mengungkap struktur komunitas dan posisi struktural aktor dalam jaringan wacana.
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **2.6.1 Dasar-Dasar Teori Graf (Hal. 55)**
            - Representasi matematis $G = (V, E)$ di mana $V$ adalah akun warganet (nodes) dan $E$ adalah interaksi *mentions/replies* berarah (directed edges).

            **2.6.2 Sentralitas dalam Jaringan (Hal. 55)**
            - Metrik *In-Degree* (prestise/target aduan), *Out-Degree* (keaktifan intervensi), *Betweenness* (kapasitas broker informasi), dan *Eigenvector* (kedekatan dengan aktor berpengaruh).

            **2.6.3 Deteksi Komunitas dan Algoritma Louvain (Hal. 56)**
            - Metode heuristik optimasi modularitas Blondel et al. untuk mempartisi jaringan besar menjadi klaster-klaster percakapan organik.

            **2.6.4 Modularity sebagai Ringkasan Struktur Komunitas (Hal. 57)**
            - Nilai modularity **0.9837** digunakan untuk merangkum struktur komunitas yang teridentifikasi oleh algoritma Louvain; interpretasinya difokuskan pada keterpisahan struktural antarkomunitas.
            """)
        with c2:
            st.warning("""
            **2.6.5 Homofili dan Struktur Komunitas (Hal. 58)**
            - Kecenderungan warganet berinteraksi hanya dengan akun sefaham, mengunci narasi kritik di dalam klaster dengan hubungan timbal balik yang terbatas lintas kelompok.

            **2.6.6 Visualisasi Jaringan sebagai Instrumen Diagnostik Kebijakan (Hal. 59)**
            - Graf jaringan sebagai alat pembuat kebijakan membaca titik api krisis dan mengevaluasi efektivitas diseminasi klarifikasi.

            **2.6.7 Jaringan Bipartit dan Keterbatasan Graf Sederhana (Hal. 60)**
            - Refleksi metodologis relasi aktor-isu vs relasi langsung aktor-ke-aktor.

            **2.6.8 Perbandingan Algoritma Deteksi Komunitas (Hal. 61)**
            - Keunggulan komputasional Louvain dibanding Girvan-Newman pada graf berukuran ratusan node.

            **2.6.9 Analisis Sentralitas Jaringan (Triangulasi Metodologis) (Hal. 62)**
            - Validasi komputasional sentralitas multi-dimensi untuk memastikan tidak terjadi bias representasi pada akun anonim.
            """)

    with theory_tabs[6]:
        st.subheader("🧩 §2.9 Kerangka Pemikiran Konseptual (Halaman 74–79)")
        st.markdown("""
        Sintesis integratif menautkan dimensi fisik dan digital ke dalam kerangka **Marketing 6.0: The Future is Immersive** (Kotler, Kartajaya, & Setiawan, 2023).
        """)

        st.info("""
        ### 🔄 Diagram Alur Kerangka Pemikiran: Manifestasi Phygital Gap

        ```
        ┌────────────────────────────────────────────────────────────────────────┐
        │                 KEBIJAKAN FISIK PUBLIK (Program MBG)                   │
        │      Janji Kebijakan Digital: Makanan Bergizi, Gratis, Bebas Stunting   │
        └───────────────────────────────────┬────────────────────────────────────┘
                                            │ Diseminasi & Pengalaman Lapangan
                                            ▼
        ┌────────────────────────────────────────────────────────────────────────┐
        │                 TRANSFORMASI DISKURSUS DI PLATFORM X                   │
        │           Afordansi Mention, Retweet, Reply-Thread, Bahasa Slang       │
        └──────────────────┬──────────────────────────────────┬──────────────────┘
                           │                                  │
                           ▼                                  ▼
        ┌──────────────────────────────────┐ ┌──────────────────────────────────┐
        │   DIMENSI AFEKTIF & LINGUISTIK   │ │   DIMENSI STRUKTURAL JARINGAN    │
        │       (IndoBERT 9 Emosi)         │ │   (NetworkX SNA & Louvain)       │
        │  - Distribusi emosi IndoBERT       │ │  - Modularity 0.9837 (342 Komunitas) │
        │  - Deteksi Sindiran (9,28%–56,6%)│ │  - asymmetric interaction structure (@prabowo In=15) │
        │  - Penolakan Mutu Fisik Makanan  │ │  - akun dengan out-degree tinggi (@grok=42) │
        └──────────────────┬───────────────┘ └──────────────────┬───────────────┘
                           │                                  │
                           └─────────────────┬────────────────┘
                                             │ Sintesis Komputasional
                                             ▼
        ┌────────────────────────────────────────────────────────────────────────┐
        │                  INTERPRETASI PHYGITAL GAP (Marketing 6.0)              │
        │  Jurang pemisah antara narasi digital pemerintah dan pengalaman fisik  │
        │   nyata penerima manfaat (makanan basi, porsi minim, keracunan).       │
        └────────────────────────────────────────────────────────────────────────┘
        ```
        """)

        k1, k2 = st.columns(2)
        with k1:
            st.success("""
            **2.9.1 Justifikasi Arah Kausalitas Konseptual (Hal. 77)**
            - Menjelaskan bahwa stimulus fisik di lapangan (kualitas hidangan dan rantai pasok) mendahului (*precedes*) produksi diskursus digital di Platform X.
            - Narasi resistensi dan sindiran merupakan respons reaktif atas inkonsistensi yang dialami secara indrawi oleh siswa dan wali murid.
            """)
        with k2:
            st.success("""
            **2.9.2 Definisi Konseptual Variabel-Variabel Kunci (Hal. 78)**
            - **Phygital Gap**: Kesenjangan antara ekspektasi yang dibangun antarmuka digital dan kepuasan pengalaman fisik riil.
            - **Inkongruensi Afektif**: Ketidaksesuaian antara diksi formal program dan emosi jijik (*disgust*) yang diekspresikan warganet.
            - **Asimetri Struktur Interaksi**: Pola di mana akun dengan in-degree tinggi menerima lebih banyak mention (*asymmetric interaction structure*), sementara pola keterhubungan akun AI terlihat dalam struktur jaringan.
            """)

    with theory_tabs[7]:
        st.subheader("🎯 §2.10 Proposisi Kerja & §2.11 Etika Riset Komputasional (Halaman 80–84)")
        st.markdown("""
        Evaluasi 5 Proposisi Kerja Penelitian terhadap data empiris riil dan standar etika ekstraksi data media sosial.
        """)

        prop_data = [
            {
                "Proposisi": "P1: Dominasi Strategi Sindiran",
                "Klaim Teoretis (Hal. 80)": "Kritik publik terhadap kegagalan kebijakan lebih banyak disampaikan melalui gaya bahasa sindiran ketimbang penolakan frontal.",
                "Status Empiris": "✅ Terkonfirmasi",
                "Bukti Data Riil": "315 cuitan (9,28%) validasi leksikon; 2.979 cuitan (56,60%) memuat proksi afektif penolakan/jijik."
            },
            {
                "Proposisi": "P2: Keunggulan IndoBERT pada Bahasa Slang",
                "Klaim Teoretis (Hal. 81)": "Arsitektur transformer bidirectional mampu membaca inkongruensi makna pada bahasa gaul/campur kode warganet.",
                "Status Empiris": "✅ Terkonfirmasi",
                "Bukti Data Riil": "IndoBERT (test n=1.058): akurasi 75,99%, Macro-F1 0,4535, Weighted-F1 0,7434."
            },
            {
                "Proposisi": "P3: Strong Community Structure Jaringan Komunikasi",
                "Klaim Teoretis (Hal. 81)": "Struktur keterhubungan jaringan menunjukkan ratusan komponen terhubung; temuan ini digunakan untuk mendeskripsikan struktur jaringan, bukan untuk mengukur polarisasi ideologis.",
                "Status Empiris": "✅ Terkonfirmasi",
                "Bukti Data Riil": "Modularity 0,9837; 342 komunitas Louvain; komponen raksasa hanya 9,1% (89 node); reciprocity 1,20%."
            },
            {
                "Proposisi": "P4: Asimetri Distribusi Pengaruh & asymmetric interaction structure",
                "Klaim Teoretis (Hal. 82)": "Terdapat perbedaan posisi struktural antaraktor dalam graf mention; @grok memiliki out-degree 42, sedangkan @prabowo memiliki in-degree 15.",
                "Status Empiris": "✅ Terkonfirmasi",
                "Bukti Data Riil": "@prabowo In-degree=15 & in-degree digunakan untuk mendeskripsikan posisi struktural; @grok Out-degree=42 (#1 di seluruh jaringan)."
            },
            {
                "Proposisi": "P5: Eksistensi Phygital Gap Kebijakan Publik",
                "Klaim Teoretis (Hal. 82)": "Dominasi emosi jijik dan fragmentasi jaringan menganalisis keberadaan jurang tajam antara janji digital dan realitas fisik.",
                "Status Empiris": "✅ Terkonfirmasi",
                "Bukti Data Riil": "ABSA: Jijik mendominasi ketiga aspek (71,13%–78,91%); Kualitas Gizi paling banyak dibicarakan (1.344 cuitan)."
            }
        ]
        st.dataframe(pd.DataFrame(prop_data), width='stretch', hide_index=True)

        st.markdown("---")
        st.subheader("⚖️ §2.11 Etika Komputasional & Validitas Data (Halaman 83–84)")
        e1, e2 = st.columns(2)
        with e1:
            st.info("""
            **2.11.1 Privasi dan Ekspektasi Wajar Pengguna Media Sosial (Hal. 83)**
            - Penanganan etis data cuitan publik: teks dianonimisasi, identitas privat dilindungi, dan analisis berfokus pada dinamika agregat sentimen kebijakan, bukan profiling personal.
            """)
        with e2:
            st.warning("""
            **2.11.2 Akun Bot, Manipulasi Wacana, dan Validitas Data (Hal. 83)**
            - Pipeline filtering ketat menyaring 1.915 cuitan sampah/bot dari total 5.310 data mentah (36% reduksi kebisingan) untuk memastikan temuan mencerminkan aspirasi warganet autentik.
            """)





