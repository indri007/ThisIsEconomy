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


def render_bab5_page():
    render_thesis_stepper(5)
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🎯 Bab V Tesis — Penutup & Rekomendasi Kebijakan</div>
        <div class="hero-title">Kesimpulan, Implikasi, Keterbatasan & Rekomendasi BGN</div>
        <div class="hero-desc">
            Sintesis akhir jawaban terhadap <b>6 Rumusan Masalah Penelitian</b>, pengakuan jujur atas 5 keterbatasan metodologis,
            serta perumusan 4 rekomendasi manajerial solutif dan aksi nyata bagi <b>Badan Gizi Nasional (BGN)</b>.
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px;">
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">✅ <b>6 Rumusan Masalah:</b> Terjawab Tuntas</span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">🏛️ <b>Rekomendasi BGN:</b> 4 Pilar Aksi Nyata</span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">⚠️ <b>Keterbatasan Riset:</b> 5 Poin Terbuka</span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">📈 <b>Agenda Riset Lanjutan:</b> Multimodal Vision</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("🏛️ Peta Temuan Empiris Bab IV (Hasil & Pembahasan) & Bab V (Penutup)")
    st.markdown("""
    > *Bagian ini menyajikan rekonstruksi visual komprehensif dari naskah tesis **Bab IV (Halaman 94 – 109)**
    > dan **Bab V (Halaman 110 – 113)** — menganalisis bahwa setiap sub-bab ditopang secara mutlak
    > oleh bukti data empiris komputasional (NLP IndoBERT, SNA Louvain, dan Sintesis Marketing 6.0).*
    """)

    # KPI Metrics Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("📊 Korpus Data Bab IV", "3.395 Cuitan Valid", "Analisis Leksikal")
    with kpi2:
        st.metric("😊 Emosi Dominan (§4.5)", "Jijik 56,24%", "2.960 dari 5.263 cuitan")
    with kpi3:
        st.metric("🕸️ Struktur Komunitas Jaringan (§4.3)", "Q = 0.9837", "342 Komunitas Louvain")
    with kpi4:
        st.metric("🏛️ Rekomendasi BGN (§5.3)", "5 Aksi Nyata", "Mitigasi Phygital Gap")

    st.markdown("---")

    # Two Main Pillars: Bab IV and Bab V
    col_b4, col_b5 = st.columns(2)

    with col_b4:
        st.markdown("### 🔬 BAB IV: HASIL DAN PEMBAHASAN (Hal. 94 – 109)")

        with st.expander("📌 4.1 Deskripsi Umum & Karakteristik Data (Hal. 94)", expanded=True):
            st.markdown("""
            - **Populasi & Sampel:** 3.395 cuitan valid yang digunakan dalam analisis leksikal di platform X (periode krisis Maret–Mei 2026).
            - **Pembersihan Data:** Mendokumentasikan keterbatasan identifikasi bot, akun promosi, dan duplikasi teks.
            - **Korpus Leksikal:** 3.395 cuitan dianalisis secara mendalam untuk ekstraksi majas dan penanda emoji.
            - **Distribusi Emosi:** Jijik 56,24%, Percaya 20,39%, Netral 12,33%, Tertarik 9,60% (N=5.263).
            """)

        with st.expander("📌 4.2 Analisis Sistem: Topologi Jaringan & Struktur Komunitas (Hal. 95)"):
            st.markdown("""
            - **Parameter Graf:** 971 node (aktor warganet unik) dan 666 relasi interaksi / edges (692 interaksi mentah).
            - **Kepadatan (Density):** 0.000707104 — jaringan memiliki kepadatan rendah.
            - **Resiprositas (Reciprocity):** **1,20%** — nilai reciprocity sebesar 1,20% menunjukkan rendahnya hubungan timbal balik dalam graf mention yang dianalisis.
            - **Diameter Graf & Komponen:** Terpecah ke dalam 341 weakly connected components.
            """)

        with st.expander("📌 4.3 Analisis Clustering: Dinamika Struktur Komunitas (Hal. 97)"):
            st.markdown("""
            - **Modularitas Louvain:** **Q = 0.9837** (digunakan untuk merangkum struktur komunitas hasil partisi Louvain).
            - **Jumlah Komunitas:** 342 komunitas yang menunjukkan keterpisahan struktural antarkomunitas.
            - **Isolasi Diskursus:** Warganet berbicara di dalam gelembung opini kelompoknya sendiri tanpa jembatan dialog antarkubu.
            """)

        with st.expander("📌 4.4 Analisis Level Aktor: Struktur Kekuasaan & Brokerage (Hal. 98)"):
            st.markdown("""
            - **🤖 @grok (akun dengan out-degree tinggi):** Out-degree = 42 (paling dominan), aktor dengan out-degree tinggi dalam graf.
            - **🔗 @grok (High-Betweenness Actor):** Betweenness = 0.005940868 (posisi struktural pada jalur terpendek dalam graf).
            - **@prabowo:** In-degree = 15 (paling sering dimention dalam graf yang dianalisis).
            - **Fenomena asymmetric interaction structure:** Kekosongan narasi resmi pemerintah diisi oleh agen kecerdasan buatan.
            """)

        with st.expander("📌 4.5 Evaluasi Model Emosi & Deteksi Sindiran (Hal. 101)"):
            st.markdown("""
            - **4.5.1 Evaluasi IndoBERT:** Akurasi 75,99%, Macro-F1 0,4535, Weighted-F1 0,7434 pada test set terisolasi (n=1.058).
            - **4.5.2 Evaluasi Deteksi Sindiran:** 315 cuitan (9,28%) memuat majas sindiran tervalidasi leksikal, sementara proksi afektif menangkap 56,60%.
            - **4.5.3 Interpretasi Triangulasi:** Sindiran merupakan sub-dimensi leksikal dari emosi Jijik (*Disgust*) — kedua metode konvergen dan saling mengonfirmasi.
            """)

        with st.expander("📌 4.6 Sintesis: Perspektif Marketing 6.0 & Phygital Gap (Hal. 105)"):
            st.markdown("""
            - **4.6.1 Evaluasi ABSA Tiga Aspek:** Kritik publik terkonsentrasi pada kegagalan fisik: Logistik (basi/terlambat) dan Anggaran (pemangkasan nilai porsi).
            - **4.6.2 Sintesis Struktural-Afektif:** Interpretasi melalui kerangka *Phygital Gap* — publik menerima visi digital kebijakan, namun menolak keras realitas eksekusi fisik di lapangan.
            """)

    with col_b5:
        st.markdown("### 🏛️ BAB V: PENUTUP & REKOMENDASI (Hal. 110 – 113)")

        with st.expander("📌 5.1 Kesimpulan Penelitian (Hal. 110)", expanded=True):
            st.markdown("""
            1. **Anatomi Bahasa (RM 1):** Kritik MBG diekspresikan lewat sindiran halus dan oposisi biner (315 cuitan valid).
            2. **Inkongruensi Semiotik (RM 2):** Disparitas tajam antara teks pujian semu dengan emoji sinis (🤡, 🤮).
            3. **Respons Afektif (RM 3):** Distribusi label emosi dalam korpus: Jijik 56,24%, Percaya 20,39%, Netral 12,33%, Tertarik 9,60% (N=5.263).
            4. **Topologi Jaringan (RM 4):** Struktur komunitas (Q=0.9837) yang terdiri atas 342 komunitas.
            5. **Sentralitas Aktor (RM 5):** Dominasi AI (@grok Out=42) dan nilai in-degree @prabowo sebesar 15 dalam graf mention.
            6. **Phygital Gap (RM 6):** Kesenjangan absolut antara janji digital pemerintah dan eksekusi fisik SPPG di lapangan.
            """)

        with st.expander("📌 5.2 Implikasi Penelitian (Hal. 112)"):
            st.markdown("""
            - **5.2.1 Implikasi Akademis:**
              - Memperkaya kajian *Computational Social Science* di Indonesia dengan integrasi deep learning IndoBERT dan teori graf SNA.
              - Memperluas aplikasi teori *Marketing 6.0* dari sektor korporasi ke ranah evaluasi kebijakan publik makro.
            - **5.2.2 Implikasi Praktis:**
              - Memberikan kerangka kerja pemantauan sentimen real-time berbasis multi-dimensi bagi kementerian/lembaga.
              - Menghindarkan pembuat kebijakan dari ilusi sentimen linear biner yang menyesatkan.
            """)

        with st.expander("📌 5.3 Rekomendasi Kebijakan BGN & Riset Lanjutan (Hal. 112)"):
            st.markdown("""
            - **5.3.1 Rekomendasi untuk Badan Gizi Nasional (BGN):**
              1. *Buka Dialog Dua Arah:* Naikkan resiprositas dari 1,20% dengan menugaskan humas merespons kritik secara aktif.
              2. *Analisis hubungan lintas komunitas: gunakan edge record lintas komunitas sebagai dasar untuk mengidentifikasi koneksi antarkomunitas.
              3. *Single Source of Truth Menu:* Terbitkan katalog foto dan komposisi gizi menu harian di platform digital resmi.
              4. *Transparansi Alokasi Biaya:* Edukasi publik mengenai rincian biaya porsi makan guna memutus rumor pemangkasan anggaran.
              5. *Optimalisasi Narasi Berbasis Bukti:* Imbangi hegemoni akun dengan out-degree tinggi (@grok) dengan data terbuka yang dapat diverifikasi mesin pencari.
            - **5.3.2 Rekomendasi untuk Riset Selanjutnya (Hal. 113):**
              - Menambahkan analisis multimodal (analisis gambar/foto menu fisik dan meme).
              - Memperluas jangkauan ke platform visual seperti TikTok dan Instagram.
            """)

        # ── §5.4 KETERBATASAN PENELITIAN & AGENDA RISET MENDATANG ──
        st.markdown("---")
        st.subheader("⚠️ 5.4 Visualisasi Keterbatasan Penelitian (Research Limitations) & Refleksi Kritis")
        st.markdown("""
        > *Transparansi akademik menuntut pengakuan jujur atas batas-batas ruang lingkup metodologis studi.
        > Berikut adalah pemetaan multidimensi 5 keterbatasan utama riset ini, strategi mitigasi yang telah diterapkan,
        > serta rekomendasi arah penelitian lanjutan (*future research agenda*).*
        """)

        # Panel 1: Interactive Radar Chart (Plotly)
        col_rad, col_mat = st.columns([1.1, 1.3])

        with col_rad:
            st.markdown("##### 🕸️ A. Radar Profil Kapabilitas Metodologis vs Batas Horizon Riset")

            categories_radar = [
                'Kedalaman NLP Emosi (9 Kelas)',
                'Topologi Jaringan SNA (Louvain)',
                'Triangulasi Phygital Mkt 6.0',
                'Multimodalitas (Teks + CV)',
                'Multi-Platform (X + TikTok + FB)',
                'Horizon Temporal (Longitudinal)',
                'Representasi Rural 3T'
            ]

            fig_radar_lim = go.Figure()

            # Ideal Full Horizon
            fig_radar_lim.add_trace(go.Scatterpolar(
                r=[100, 100, 100, 100, 100, 100, 100, 100],
                theta=categories_radar + [categories_radar[0]],
                fill='toself',
                fillcolor='rgba(148, 163, 184, 0.08)',
                line=dict(color='#94A3B8', dash='dash', width=1.5),
                name='Batas Horizon Ideal (Teoritis)'
            ))

            # Thesis Scope
            fig_radar_lim.add_trace(go.Scatterpolar(
                r=[95, 92, 90, 20, 25, 35, 30, 95],
                theta=categories_radar + [categories_radar[0]],
                fill='toself',
                fillcolor='rgba(2, 132, 199, 0.35)',
                line=dict(color='#38BDF8', width=3),
                name='Cakupan Metodologis Tesis Ini'
            ))

            fig_radar_lim.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 105],
                        tickvals=[25, 50, 75, 100],
                        ticktext=['25%', '50%', '75%', '100%'],
                        color='#94A3B8',
                        gridcolor='#334155'
                    ),
                    angularaxis=dict(
                        color='#F8FAFC',
                        gridcolor='#334155'
                    ),
                    bgcolor='#1E293B'
                ),
                paper_bgcolor='#0F172A',
                plot_bgcolor='#0F172A',
                margin=dict(l=40, r=40, t=30, b=30),
                height=380,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(color='#F8FAFC', size=10)
                )
            )
            st.plotly_chart(fig_radar_lim, width='stretch')

        with col_mat:
            st.markdown("##### 📊 B. Skor Keterbatasan Metodologis & Potensi Risiko Bias")

            lim_bar_df = pd.DataFrame([
                {"Dimensi Keterbatasan": "Single-Platform Boundary (X/Twitter Bias)", "Tingkat Keterbatasan": 75, "Area Fokus": "Eksternalitas"},
                {"Dimensi Keterbatasan": "Unimodalitas Teks (Tanpa Visi Komputer)", "Tingkat Keterbatasan": 80, "Area Fokus": "Modalitas"},
                {"Dimensi Keterbatasan": "Snapshot Temporal (Maret–Mei 2026)", "Tingkat Keterbatasan": 65, "Area Fokus": "Horizon Waktu"},
                {"Dimensi Keterbatasan": "Ambiguitas Satir Vernakular Budaya", "Tingkat Keterbatasan": 45, "Area Fokus": "Linguistik"},
                {"Dimensi Keterbatasan": "Representasi Demografis Rural 3T", "Tingkat Keterbatasan": 70, "Area Fokus": "Sampling"}
            ])

            fig_bar_lim = px.bar(
                lim_bar_df,
                x="Tingkat Keterbatasan",
                y="Dimensi Keterbatasan",
                orientation='h',
                color="Area Fokus",
                color_discrete_map={
                    "Eksternalitas": "#F59E0B",
                    "Modalitas": "#EF4444",
                    "Horizon Waktu": "#6366F1",
                    "Linguistik": "#10B981",
                    "Sampling": "#EC4899"
                },
                text="Tingkat Keterbatasan"
            )
            fig_bar_lim.update_traces(texttemplate='%{text}% Batasan', textposition='inside')
            fig_bar_lim.update_layout(
                paper_bgcolor='#0F172A',
                plot_bgcolor='#1E293B',
                font=dict(color='#F8FAFC'),
                margin=dict(l=10, r=20, t=20, b=20),
                height=380,
                xaxis=dict(range=[0, 100], gridcolor='#334155', title="Skor Derajat Keterbatasan (0 = Bebas Bias, 100 = Sangat Dibatasi)"),
                yaxis=dict(autorange="reversed", title="")
            )
            st.plotly_chart(fig_bar_lim, width='stretch')

        # Detailed 5 Limitations Tabs
        st.markdown("##### 🔍 C. Eksplorasi 5 Pilar Keterbatasan, Mitigasi & Riset Lanjutan")

        tab_lim1, tab_lim2, tab_lim3, tab_lim4, tab_lim5 = st.tabs([
            "1️⃣ Platform X Bias",
            "2️⃣ Unimodalitas Teks",
            "3️⃣ Rentang Waktu",
            "4️⃣ Satir & Budaya",
            "5️⃣ Sampling Rural 3T"
        ])

        with tab_lim1:
            st.markdown("""
            **Pilar 1: Single-Platform Boundary Bias (Platform X / Twitter)**
            * **Batas Metodologi:** Korpus data diambil khusus dari platform X (dataset emosi N=5.263). Percakapan di TikTok, Facebook Group, dan Instagram yang memiliki penetrasi tinggi di kalangan ibu rumah tangga dan wali murid belum tertangkap.
            * **Risiko Bias:** Kecenderungan pengguna X yang lebih politis, kritis, dan berpendidikan tinggi dapat melebih-lebihkan sentimen *Disgust* dibanding populasi umum.
            * **Mitigasi dalam Tesis:** Dokumentasi keterbatasan identifikasi bot; metrik SNA digunakan untuk analisis jaringan, verifikasi rasio edge/node (692 relasi aktif), serta normalisasi leksikon ragam santai Twitter.
            * **Agenda Riset Masa Depan:** Mengembangkan agregator *cross-platform social listening* terintegrasi (X + TikTok + YouTube Comments + Facebook).
            """)

        with tab_lim2:
            st.markdown("""
            **Pilar 2: Unimodalitas Teks (Text-Only NLP vs Computer Vision)**
            * **Batas Metodologi:** Analisis murni mengolah teks cuitan warganet dan belum mencakup *Computer Vision* (CV) untuk menganalisis jutaan foto menu/piring makanan fisik yang diunggah warganet.
            * **Risiko Bias:** Klaim tekstual "porsi sedikit" atau "sayur basi" diterima sebagai persepsi afektif warganet tanpa verifikasi visual komparatif atas piring makanan riil secara objektif.
            * **Mitigasi dalam Tesis:** Triangulasi aspek ABSA (Gizi, Anggaran, Logistik) untuk memvalidasi konsistensi topik antar-klaster warganet yang independen.
            * **Agenda Riset Masa Depan:** Menerapkan arsitektur multimodal Vision-Language (VLM) seperti CLIP atau LLaVA untuk mengkorelasikan teks sindiran dengan kalori visual piring makan.
            """)

        with tab_lim3:
            st.markdown("""
            **Pilar 3: Snapshot Horizon Temporal (Maret – Mei 2026)**
            * **Batas Metodologi:** Pengambilan data difokuskan pada jendela krisis awal peluncuran kebijakan (isu pemangkasan anggaran dan kejadian makanan basi pertama kali).
            * **Risiko Bias:** Bersifat *cross-sectional snapshot*, belum menangkap fase pemulihan (*recovery stage*) setelah Badan Gizi Nasional (BGN) mendirikan SPPG terstandar.
            * **Mitigasi dalam Tesis:** Analisis time-series harian mikro untuk membedah titik lonjakan viralitas krisis (*viral crisis spikes*) secara presisi.
            * **Agenda Riset Masa Depan:** Studi longitudinal berkala (12–24 bulan) untuk memotret kurva transisi dari krisis menuju penerimaan stabil kebijakan publik.
            """)

        with tab_lim4:
            st.markdown("""
            **Pilar 4: Sarkasme Vernakular & Kompleksitas Budaya Lokal**
            * **Batas Metodologi:** Gaya tutur warganet Indonesia dipenuhi satir halus, metafora hiperbolik, serta idiom daerah (Jawa/Sunda) seperti *"sayur bening isi angin doang"*.
            * **Risiko Bias:** Klasifikasi emosi berisiko mengalami *misclassification* antara emosi *Marah (Anger)*, *Jijik (Disgust)*, dan *Netral (Neutral)*.
            * **Mitigasi dalam Tesis:** Integrasi korpus sindiran terverifikasi (N=3.395) dan evaluasi performa model IndoBERT mencapai metrik evaluasi model.
            * **Agenda Riset Masa Depan:** Memanfaatkan model penalaran pragmatik berbasis LLM kultural yang peka terhadap majas ironi bahasa daerah Indonesia.
            """)

        with tab_lim5:
            st.markdown("""
            **Pilar 5: Representasi Sampling (Urban-Skewed vs Rural 3T Non-Digital)**
            * **Batas Metodologi:** Mayoritas pengguna aktif X berada di wilayah perkotaan (*urban-centric*). Persepsi penerima manfaat langsung di daerah 3T (Tertinggal, Terdepan, Terluar) belum memiliki jejak digital setara.
            * **Risiko Bias:** Tesis lebih merefleksikan opini publik kelas menengah perkotaan dan aktivis media sosial ketimbang suara riil anak-anak sekolah pedesaan.
            * **Mitigasi dalam Tesis:** Memfokuskan proposisi kesimpulan pada *pengawasan kebijakan makro nasional, transparansi tata kelola anggaran, dan relasi komunikasi krisis*.
            * **Agenda Riset Masa Depan:** Triangulasi hibrida dengan survei lapangan tatap muka (*mixed-methods fieldwork*) bersamaan dengan pemantauan SNA digital.
            """)

        # Matriks Komprehensif Tabel
        st.markdown("##### 📋 D. Matriks Komparasi Keterbatasan ↔ Mitigasi ↔ Riset Lanjutan")
        lim_matrix_data = [
            {"No": 1, "Pilar Keterbatasan": "Single-Platform Boundary", "Batas Ruang Lingkup": "Khusus platform X (Twitter)", "Mitigasi Riset Tesis": "Dokumentasi keterbatasan identifikasi bot; analisis menggunakan 692 edge records", "Agenda Riset Masa Depan": "Agregasi multi-platform (TikTok, FB, IG)"},
            {"No": 2, "Pilar Keterbatasan": "Unimodalitas Teks", "Batas Ruang Lingkup": "Hanya analisis teks cuitan", "Mitigasi Riset Tesis": "Triangulasi ABSA 3 pilar tematik", "Agenda Riset Masa Depan": "Multimodal Vision-Language (CLIP/LLaVA)"},
            {"No": 3, "Pilar Keterbatasan": "Horizon Temporal", "Batas Ruang Lingkup": "Snapshot krisis Maret–Mei 2026", "Mitigasi Riset Tesis": "Pelacakan harian mikro lonjakan viralitas", "Agenda Riset Masa Depan": "Studi longitudinal berkala 12–24 bulan"},
            {"No": 4, "Pilar Keterbatasan": "Satir Vernakular Lokal", "Batas Ruang Lingkup": "Metafora & idiom daerah", "Mitigasi Riset Tesis": "Dataset sindiran N=3.395, metrik evaluasi model", "Agenda Riset Masa Depan": "Reasoning pragmatik kultural berbasis LLM"},
            {"No": 5, "Pilar Keterbatasan": "Representasi Rural 3T", "Batas Ruang Lingkup": "Urban-skewed pengguna Twitter", "Mitigasi Riset Tesis": "Fokus pada tata kelola makro & transparansi", "Agenda Riset Masa Depan": "Mixed-methods hibrida survei tatap muka"}
        ]
        st.dataframe(pd.DataFrame(lim_matrix_data), width='stretch', hide_index=True)

        # Display High-Resolution Thesis Plot
        p_lim_img = get_result_path("keterbatasan_penelitian.png")
        if os.path.exists(p_lim_img):
            st.markdown("##### 🖼️ E. Gambar Masterpiece Keterbatasan Penelitian (Publikasi Naskah Tesis)")
            st.image(p_lim_img, width='stretch', caption="Gambar 5.1. Peta Multidimensi Keterbatasan Penelitian, Mitigasi Empiris, dan Agenda Riset Masa Depan (300 DPI)")
            download_file_button(
                label="⬇️ Unduh Gambar Keterbatasan Penelitian (PNG 300 DPI)",
                file_path=p_lim_img,
                file_name="keterbatasan_penelitian_mbg.png",
                mime="image/png",
            )

    # Comprehensive Summary Table
    st.markdown("---")
    st.subheader("📋 Matriks Pemetaan Komprehensif: Struktur Tesis Bab I – Bab V ↔ Bukti Data Riil")

    thesis_master_map = [
        {"Bab Tesis": "Bab I: Pendahuluan", "Sub-Bab": "1.2 & 1.4 Rumusan & Tujuan", "Fokus Kajian": "Harmonisasi 6 Pertanyaan ↔ 6 Target Riset", "Metode / Instrumen": "Sankey Flow & Matriks Keselarasan", "Data Empiris": "Harmonisasi simetris 1-to-1", "Halaman": "15 & 19"},
        {"Bab Tesis": "Bab II: Landasan Teori", "Sub-Bab": "2.1 s.d 2.6 Landasan Konseptual", "Fokus Kajian": "8 Pilar Teori & 37 Sub-Bab Terstruktur", "Metode / Instrumen": "Sunburst & Treemap Hierarkis", "Data Empiris": "37 Sub-bab, 5 Proposisi Kerja", "Halaman": "26 – 84"},
        {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.1 Karakteristik Data Korpus", "Fokus Kajian": "Penyaringan cuitan warganet platform X", "Metode / Instrumen": "Data Funnel & Preprocessing Pipeline", "Data Empiris": "N=3.395 data valid untuk analisis leksikal", "Halaman": "94"},
        {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.2 Topologi Jaringan Global", "Fokus Kajian": "Analisis kerapatan & resiprositas graf", "Metode / Instrumen": "Directed Graph SNA", "Data Empiris": "971 node, Reciprocity 1,20%", "Halaman": "95"},
        {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.3 Dinamika Komunitas Louvain", "Fokus Kajian": "Fragmentasi struktural & struktur komunitas warganet", "Metode / Instrumen": "Algoritma Louvain Community", "Data Empiris": "Modularity Q=0.9837, 342 komunitas", "Halaman": "97"},
        {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.4 Struktur Sentralitas Aktor", "Fokus Kajian": "Perbedaan posisi struktural berdasarkan Degree dan Betweenness", "Metode / Instrumen": "Centrality (Degree, Betweenness)", "Data Empiris": "@grok Out=42, @prabowo In=15", "Halaman": "98"},
        {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.5 Evaluasi Model & Sindiran", "Fokus Kajian": "Performa IndoBERT & majas sindiran", "Metode / Instrumen": "Fine-tuned Transformer IndoBERT", "Data Empiris": "Akurasi 75,99%, Macro-F1 0,4535 (test n=1.058); sindiran 9,28% (315/3.395)", "Halaman": "101 – 104"},
        {"Bab Tesis": "Bab IV: Hasil & Pembahasan", "Sub-Bab": "4.6 Sintesis Marketing 6.0", "Fokus Kajian": "Interpretasi Phygital Gap kebijakan publik", "Metode / Instrumen": "ABSA & Triangulasi SNA-NLP", "Data Empiris": "Logistik & anggaran sebagai aspek yang teridentifikasi", "Halaman": "105 – 109"},
        {"Bab Tesis": "Bab V: Penutup", "Sub-Bab": "5.1 s.d 5.4 Simpulan & Solusi", "Fokus Kajian": "Rekomendasi BGN & Implikasi Kebijakan", "Metode / Instrumen": "Matriks Intervensi Kebijakan", "Data Empiris": "5 Aksi Strategis Mitigasi Krisis", "Halaman": "110 – 113"}
    ]
    st.dataframe(pd.DataFrame(thesis_master_map), width='stretch', hide_index=True)




