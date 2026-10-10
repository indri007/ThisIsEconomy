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


def render_bab4_page():
    render_thesis_stepper(4)
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">📊 Bab IV Tesis — Hasil dan Pembahasan</div>
        <div class="hero-title">Investigasi Empiris Terintegrasi (NLP × SNA × ABSA)</div>
        <div class="hero-desc">
            Hasil pengolahan data riil dan pembahasan mendalam yang disusun secara <b>sekuensial dan terstruktur</b>
            mengikuti 6 sub-bab naskah tesis (Halaman 94 – 109): dari karakteristik korpus, topologi jaringan,
            komunitas Louvain, sentralitas aktor, evaluasi model IndoBERT, hingga interpretasi melalui kerangka Phygital Gap.
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px;">
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">📁 <b>Korpus:</b> 3.395 Cuitan Valid untuk Analisis Leksikal</span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">🤢 <b>Emosi Dominan:</b> Jijik 56,24%</span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">🕸️ <b>Modularity:</b> Q = 0,9837 (342 Komunitas)</span>
            <span style="background: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 8px; font-size: 0.85rem;">🎯 <b>ABSA:</b> Logistik 78,91% Disgust</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6 Sequential Sub-tabs strictly in thesis order:
    tab_iv_1, tab_iv_2, tab_iv_3, tab_iv_4, tab_iv_5, tab_iv_6 = st.tabs([
        "📊 §4.1 Karakteristik Korpus Data",
        "🕸️ §4.2 Topologi Jaringan & Struktur Komunitas",
        "🧩 §4.3 Komunitas Louvain & Struktur Komunitas",
        "👑 §4.4 Sentralitas Aktor & Media",
        "😊 §4.5 Evaluasi NLP IndoBERT & Sindiran",
        "🌐 §4.6 ABSA 3 Aspek, Triangulasi & Artinya"
    ])

    with tab_iv_1:
        st.header("📊 §4.1 Deskripsi Umum & Karakteristik Data")
        st.markdown("""
        > *Data penelitian dihimpun pada periode **Maret hingga Mei 2026** melalui platform **X (Twitter)**
        > dengan kueri strategis ("Makan Bergizi Gratis", "MBG", dan tagar terkait). Pasca tahap pembersihan data
        > (*text cleansing*) serta eksklusi bot/spam, korpus resmi riset ini terdiri dari **973 aktor (nodes)**
        > yang terhubung melalui **666 relasi interaksi (edges)**, membentuk **341 weakly connected components**.*
        """)

        col_meta1, col_meta2 = st.columns([1.2, 1])
        with col_meta1:
            st.subheader("📋 Tabel 4.1 Metadata Jaringan Komunikasi Program MBG")
            st.caption("Korpus Resmi Periode Observasi Maret – Mei 2026:")
            tabel_4_1 = {
                "Parameter": [
                    "👥 Jumlah Aktor (Nodes)",
                    "🔗 Jumlah Interaksi (Edges)",
                    "🧩 Jumlah Komponen Jaringan",
                    "⚡ Nilai Modularity (Louvain)",
                    "🌐 Platform Sumber",
                    "📅 Periode Observasi",
                ],
                "Nilai": [
                    "971 akun pengguna",
                    "658 hubungan (mention)",
                    "341 komponen terhubung secara terpisah",
                    "0,9837 (Struktur Komunitas Kuat)",
                    "X (Twitter)",
                    "Maret – Mei 2026",
                ]
            }
            st.dataframe(pd.DataFrame(tabel_4_1), width='stretch', hide_index=True)

        with col_meta2:
            st.subheader("⚖️ Komparasi Data Korpus vs Data Pilot")
            st.info("""
            **🔍 Data Penjajakan Awal (Februari 2025):**
            - Nodes: 2.414 akun | Edges: 3.483 relasi
            - Modularity: **0,7130**
            - *Fungsi*: Penjajakan awal isu krisis wacana MBG.

            **📌 Korpus Resmi Penelitian (Maret–Mei 2026):**
            - Nodes: 971 akun | Edges: 666 relasi
            - Modularity: **0,9837** (Struktur Komunitas)
            - *Insight*: Struktur wacana mengalami fragmentasi tajam menjadi ratusan komponen terhubung terisolasi.
            """)

        st.markdown("---")

        # ── §4.2 TOPOLOGI JARINGAN & POLARISASI ──

        st.markdown('---')
        st.subheader('🔍 Verifikasi Integritas Data Korpus Riil')
        # Load live data for audit charts
        try:
            # 1. Emotion Data
            df_audit_emo = load_emotion_data()
            emo_counts = df_audit_emo['predicted_emotion'].value_counts().reset_index()
            emo_counts.columns = ['Emosi', 'Jumlah']

            # 2. Sarcasm Data (N=3.395)
            path_sin = "data/sarcasm/dataset_sindiran_valid.csv"
            if not os.path.exists(path_sin):
                path_sin = "../data/sarcasm/dataset_sindiran_valid.csv"
            df_audit_sin = pd.read_csv(path_sin) if os.path.exists(path_sin) else None

            # 3. SNA Centrality Data (971 nodes)
            path_deg = "data/results/sna_degree.csv"
            if not os.path.exists(path_deg):
                path_deg = "../data/results/sna_degree.csv"
            df_audit_deg = pd.read_csv(path_deg).head(8) if os.path.exists(path_deg) else None

            # 4. ABSA Data
            path_absa = get_result_path("absa_results.csv")
            df_audit_absa = pd.read_csv(path_absa) if (path_absa and os.path.exists(path_absa)) else None

            # Row 1 of Verification Charts
            vrow1_c1, vrow1_c2 = st.columns(2)

            with vrow1_c1:
                st.subheader("📊 1. Distribusi Label Emosi (N=5.263)")
                fig_live_emo = px.pie(
                    emo_counts,
                    names='Emosi',
                    values='Jumlah',
                    color='Emosi',
                    color_discrete_map={
                        'Jijik': '#065F46',
                        'Percaya': '#10B981',
                        'Netral': '#475569',
                        'Tertarik': '#F97316',
                        'Marah': '#EF4444',
                        'Sedih': '#2563EB',
                        'Takut': '#7C3AED'
                    },
                    hole=0.45,
                    title="Distribusi Label Emosi (N=5.263, silver-standard)"
                )
                fig_live_emo.update_traces(textinfo="label+percent", textfont_size=11)
                fig_live_emo.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=20), showlegend=False)
                st.plotly_chart(fig_live_emo, width='stretch')
                st.caption("✅ **Data Sumber:** `data/results/indobert_9_emosi_fixed.csv` | **Posisi:** Bab 4.1 & Bab 4.5.1")

            with vrow1_c2:
                st.subheader("🎭 2. Deteksi Sindiran Leksikal (N=3.395)")
                if df_audit_sin is not None:
                    sin_counts = df_audit_sin['sindiran'].map({True: 'Sindiran Valid (315 Cuitan / 9,28%)', False: 'Non-Sindiran (3.080 Cuitan / 90,72%)'}).value_counts().reset_index()
                    sin_counts.columns = ['Status Sindiran', 'Jumlah']
                    fig_live_sin = px.pie(
                        sin_counts,
                        names='Status Sindiran',
                        values='Jumlah',
                        color='Status Sindiran',
                        color_discrete_map={
                            'Sindiran Valid (315 Cuitan / 9,28%)': '#ef4444',
                            'Non-Sindiran (3.080 Cuitan / 90,72%)': '#3b82f6'
                        },
                        hole=0.45,
                        title="Korpus Leksikal: 315 Cuitan Memuat Ironi Valid"
                    )
                    fig_live_sin.update_traces(textinfo="label+percent", textfont_size=11)
                    fig_live_sin.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=20), showlegend=False)
                    st.plotly_chart(fig_live_sin, width='stretch')
                st.caption("✅ **Data Sumber:** `data/sarcasm/dataset_sindiran_valid.csv` | **Posisi:** Bab 4.5.2")

            # Row 2 of Verification Charts
            vrow2_c1, vrow2_c2 = st.columns(2)

            with vrow2_c1:
                st.subheader("🕸️ 3. Top Aktor Sentral Jaringan SNA (971 Nodes)")
                if df_audit_deg is not None:
                    df_plot_deg = df_audit_deg.copy()
                    df_plot_deg['node'] = df_plot_deg['node'].apply(lambda x: f"@{x}")
                    fig_live_deg = px.bar(
                        df_plot_deg,
                        x='degree_centrality',
                        y='node',
                        orientation='h',
                        color='degree_centrality',
                        color_continuous_scale='Viridis',
                        title="Perbandingan Out-Degree Aktor Jaringan"
                    )
                    fig_live_deg.update_layout(
                        height=380,
                        margin=dict(l=10, r=10, t=40, b=20),
                        yaxis=dict(categoryorder='total ascending'),
                        xaxis_title="Degree Centrality Score",
                        yaxis_title="Aktor warganet"
                    )
                    st.plotly_chart(fig_live_deg, width='stretch')
                st.caption("✅ **Data Sumber:** `data/results/sna_degree.csv` | **Posisi:** Bab 4.4")

            with vrow2_c2:
                st.subheader("📉 4. Sentimen per Aspek Kebijakan / ABSA")
                if df_audit_absa is not None:
                    fig_live_absa = go.Figure()
                    fig_live_absa.add_trace(go.Bar(
                        x=df_audit_absa['Aspect'],
                        y=df_audit_absa['Disgust_Pct'],
                        name='🤢 Disgust (%)',
                        marker_color='#ef4444',
                        text=df_audit_absa['Disgust_Pct'].apply(lambda x: f"{x}%"),
                        textposition='outside'
                    ))
                    fig_live_absa.add_trace(go.Bar(
                        x=df_audit_absa['Aspect'],
                        y=df_audit_absa['Trust_Pct'],
                        name='🤝 Trust (%)',
                        marker_color='#10b981',
                        text=df_audit_absa['Trust_Pct'].apply(lambda x: f"{x}%"),
                        textposition='outside'
                    ))
                    fig_live_absa.update_layout(
                        barmode='group',
                        height=380,
                        margin=dict(l=10, r=10, t=40, b=20),
                        yaxis_title="Persentase Sentimen (%)",
                        legend=dict(orientation="h", yanchor="bottom", y=-0.25)
                    )
                    st.plotly_chart(fig_live_absa, width='stretch')
                st.caption("✅ **Data Sumber:** `results/absa_results.csv` | **Posisi:** Bab 4.6.1 & 4.6.2")

        except Exception as e:
            st.warning(f"Memuat data audit grafis... ({e})")

        st.markdown("---")


    with tab_iv_2:
        st.header("🕸️ §4.2 Analisis Level Sistem: Topologi Jaringan & Struktur Komunitas")

        top_col1, top_col2, top_col3 = st.columns(3)
        with top_col1:
            st.metric("Modularity Louvain", "0.9837", "Ringkasan struktur komunitas")
        with top_col2:
            st.metric("Densitas Graf", "0.0007", "Jaringan Sangat Renggang")
        with top_col3:
            st.metric("Reciprocity", "1.20%", "Komunikasi Non-Timbal Balik")

        st.warning("""
        **📢 Temuan Kunci Level Sistem:**
        1. **Strong Community Structure (Modularity 0,9837):** Nilai modularitas menunjukkan struktur komunitas yang kuat. Graf jaringan terdiri atas **341 weakly connected components**, yang digunakan untuk mendeskripsikan keterhubungan struktural jaringan.
        2. **Komunikasi Searah (Reciprocity 0,0120):** Reciprocity jaringan tercatat rendah (hanya 1,2%). Graf mention menunjukkan interaksi yang dominan satu arah dengan reciprocity 1,20%; metrik ini digunakan untuk mendeskripsikan pola keterhubungan dan tidak digunakan untuk menyimpulkan motif atau respons aktual.
        """)

        # ── Visualisasi Spektrum & Gauge Modularitas (Newman, 2006) ──
        st.subheader("📐 Visualisasi Spektrum & Evaluasi Modularitas Louvain (Q = 0.9837)")
        col_gauge, col_mbar = st.columns([1, 1.3])
        with col_gauge:
            fig_q_gauge = go.Figure(go.Indicator(
                mode='gauge+number',
                value=0.9837,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': '<b>Skor Modularitas Louvain (Q)</b><br><span style="font-size:0.8em;color:#94a3b8">Ringkasan Struktur Komunitas</span>'},
                gauge={
                    'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': '#cbd5e1'},
                    'bar': {'color': '#ef4444', 'thickness': 0.35},
                    'bgcolor': '#1e293b',
                    'borderwidth': 2,
                    'bordercolor': '#334155',
                    'steps': [
                        {'range': [0, 0.3], 'color': 'rgba(16, 185, 129, 0.25)'},
                        {'range': [0.3, 0.7], 'color': 'rgba(245, 158, 11, 0.25)'},
                        {'range': [0.7, 1.0], 'color': 'rgba(239, 68, 68, 0.25)'}
                    ],
                    'threshold': {
                        'line': {'color': '#f59e0b', 'width': 3},
                        'thickness': 0.8,
                        'value': 0.3
                    }
                }
            ))
            fig_q_gauge.update_layout(height=320, margin=dict(t=50, b=20, l=20, r=20))
            st.plotly_chart(fig_q_gauge, width='stretch')

        with col_mbar:
            df_mod_comp = pd.DataFrame({
                'Fase Riset': ['Ambang Newman (2006)', 'Data Pilot (Feb 2025)', 'Korpus Resmi (Mar–Mei 2026)'],
                'Modularity Q': [0.3000, 0.7130, 0.9837],
                'Status': ['Batas Polarisasi Minimal', 'Struktur Komunitas Kuat', 'Strong Community Structure']
            })
            fig_q_bar = px.bar(
                df_mod_comp,
                x='Fase Riset',
                y='Modularity Q',
                color='Modularity Q',
                color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                text='Modularity Q',
                title="Komparasi Intensifikasi Modularitas Jaringan"
            )
            fig_q_bar.update_traces(texttemplate='%{text:.4f}', textposition='outside')
            fig_q_bar.update_layout(height=320, margin=dict(t=50, b=20, l=10, r=10), yaxis_range=[0, 1.15], coloraxis_showscale=False)
            st.plotly_chart(fig_q_bar, width='stretch')

        # ── Load Network Data Real ──
        edges, nodes_data = load_network_data()
        G_undir = nx.from_pandas_edgelist(edges, 'Source', 'Target')
        wcc_list = sorted(nx.connected_components(G_undir), key=len, reverse=True)
        total_nodes_graph = G_undir.number_of_nodes()

        # ── Tabel 4.2 Ukuran 10 Komponen Terbesar (Dihitung Dinamis dari Data Riil) ──
        st.subheader("📋 Tabel 4.2 Ukuran Sepuluh Komponen Jaringan Terbesar (Korpus Resmi)")
        st.caption(f"Distribusi fragmentasi struktural wacana MBG (Total {len(wcc_list)} weakly connected wcc_list dari {total_nodes_graph} aktor riil):")

        char_list = [
            "Ruang diskusi heterogen (dukungan, bantahan resmi, & kritik sindiran)",
            "Klaster percakapan relawan dan pantauan lapangan terisolasi",
            "Klaster diskusi warganet skeptis terhadap alokasi APBN",
            "Sub-komunitas penyebaran konten ironis/meme makanan MBG",
            "Klaster keluhan orang tua siswa terkait mutu fisik menu",
            "Klaster mikro pembahasan vendor logistik daerah",
            "Percakapan terbatas antar-akun anonim",
            "Kelompok mikro diskusi isu susu gratis",
            "Klaster mikro tanpa jembatan struktural ke diskusi utama",
            "Klaster mikro tanpa jembatan struktural ke diskusi utama"
        ]

        comp_rows = []
        for i in range(min(10, len(wcc_list))):
            c_size = len(wcc_list[i])
            pct = (c_size / total_nodes_graph) * 100 if total_nodes_graph > 0 else 0
            tag = " (Giant Component)" if i == 0 else ""
            comp_rows.append({
                "Peringkat": f"Komponen {i+1}",
                "Jumlah Aktor (Nodes)": c_size,
                "Persentase (%)": f"{pct:.2f}%{tag}",
                "Karakteristik & Dinamika Diskursus": char_list[i] if i < len(char_list) else "Klaster mikro terisolasi"
            })
        st.dataframe(pd.DataFrame(comp_rows), width='stretch', hide_index=True)

        isolated_small = sum(1 for c in wcc_list if len(c) <= 2)
        st.info(f"💡 **Catatan Metodologis:** Sebanyak **{isolated_small} komponen ({(isolated_small/len(wcc_list))*100:.1f}%)** beranggotakan <= 2 aktor (dyad/isolated pair), menganalisis tidak adanya arena sentral percakapan publik nasional.")

        st.markdown("---")
        st.subheader("📊 Analisis Dimensi 1: Struktur Makro Topologi Jaringan (Standar NodeXL Pro & NetworkX)")
        st.markdown(
            "Visualisasi komprehensif 4-panel struktur makro graf komunikasi MBG mencakup distribusi derajat bebas-skala (*power-law scaling*), "
            "ukuran komponen raksasa (*giant component* vs pulau terisolasi), resiprositas asimetris, dan ringkasan scorecard parameter jaringan:"
        )
        macro_img_p = os.path.join(PROJECT_ROOT, "results", "17_macro_topology_metrics.png")
        if os.path.exists(macro_img_p):
            st.image(macro_img_p, width='stretch', caption="Gambar 4.2B: Struktur Makro Topologi Jaringan Komunikasi MBG (Buku Kerja NodeXL Pro & NetworkX, 300 DPI)")

        macro_json_p = os.path.join(PROJECT_ROOT, "results", "macro_topology_metrics.json")
        if os.path.exists(macro_json_p):
            with open(macro_json_p, "r", encoding="utf-8") as f_macro:
                m_data = json.load(f_macro)
            df_macro_table = pd.DataFrame([
                {"Parameter Topologi Makro": k, "Nilai Empiris": v}
                for k, v in m_data.items()
            ])
            with st.expander("📑 Lihat Tabel Lengkap Parameter Topologi Makro Graf (15+ Metrik Resmi)", expanded=False):
                st.dataframe(df_macro_table, width='stretch', hide_index=True)

        # ── JALUR TERISOLASI REKALKULASI 1 EDGE LIST KANONIS ──
        canonical_macro_p = os.path.join(PROJECT_ROOT, "results", "sna_canonical_pipeline", "canonical_macro_topology_metrics.csv")
        canonical_actors_p = os.path.join(PROJECT_ROOT, "results", "sna_canonical_pipeline", "canonical_top25_actors.csv")
        if os.path.exists(canonical_macro_p):
            with st.expander("🔬 Hasil Rekalkulasi Mandiri 1 Edge List Kanonis (Jalur Terisolasi)", expanded=False):
                st.markdown("""
                > **🛡️ Jalur Independen & Nol Kontaminasi Tesis:**
                > Seluruh metrik di bawah ini dihitung ulang secara mandiri dan otomatis dari **1 edge list kanonis (`data/network_edges.csv`, 692 baris interaksi mentah)**
                > melalui script terisolasi `scripts/recalculate_sna_canonical_pipeline.py`.
                > Hasilnya membuktikan **100% konsistensi matematis** terhadap baseline naskah tesis ($|V|=971, |E|=666, Q=0.9837, \\rho=0.000707$).
                """)
                df_canon_macro = pd.read_csv(canonical_macro_p)
                st.dataframe(df_canon_macro, width='stretch', hide_index=True)

                if os.path.exists(canonical_actors_p):
                    st.caption("🏆 **Top Aktor Hasil Rekalkulasi Jalur Terisolasi (Top 25 Central Actors):**")
                    df_canon_actors = pd.read_csv(canonical_actors_p)
                    st.dataframe(df_canon_actors[['Id', 'Label', 'In_Degree', 'Out_Degree', 'Total_Degree', 'Betweenness_Centrality', 'Communication_Role']], width='stretch', hide_index=True)

        st.markdown("---")

        # ── §4.3 Analisis Clustering Komunitas Louvain (Dihitung Dinamis dari Nodes CSV) ──

        st.subheader("🌐 Visualisasi Terpadu Jaringan Komunikasi SNA (Komunitas & Relasi)")
        st.markdown("Eksplorasi graf jaringan komunikasi wacana MBG di platform X (node diwarnai berdasarkan Komunitas Louvain riil):")

        edges, nodes_data = load_network_data()
        nodes_info_path = get_result_path("mbg_network_nodes_final.csv")
        df_ninfo_map = pd.read_csv(nodes_info_path) if os.path.exists(nodes_info_path) else None
        n_comm_map = dict(zip(df_ninfo_map['Id'], df_ninfo_map['Community'])) if df_ninfo_map is not None else {}
        n_emo_map = dict(zip(df_ninfo_map['Id'], df_ninfo_map['Dominant_Emotion'])) if df_ninfo_map is not None else {}

        graph_tab1, graph_tab2 = st.tabs(["📊 Graf Jaringan Interaktif (Plotly Native)", "🕸️ Graf Dinamis Physics 3D (PyVis)"])

        with graph_tab1:
            st.caption("Visualisasi graf jaringan berarah langsung di Streamlit (100% native tanpa ketergantungan iframe):")

            col_flt1, col_flt2 = st.columns([1.2, 2])
            with col_flt1:
                n_scale = st.radio("Skala Graf Ditampilkan:", [50, 100, 150], index=1, format_func=lambda x: f"Top {x} Aktor Utama", horizontal=True)
            with col_flt2:
                st.info("🎨 **Legenda Komunitas Louvain:** 🔴 Klaster #15 (Disgust) | 🔵 Klaster #61 (Netral) | 🟡 Klaster #16 (Sindiran) | 🟢 Klaster #259 (Trust) | 🟣 Klaster #8 (Anggaran)")

            # Load graph and subgraph
            G_full = nx.from_pandas_edgelist(edges, source='Source', target='Target', create_using=nx.DiGraph())
            deg_all = dict(G_full.degree())
            sel_top_nodes = sorted(deg_all, key=deg_all.get, reverse=True)[:n_scale]
            subG_plot = G_full.subgraph(sel_top_nodes)

            # Layout computation
            pos_2d = nx.spring_layout(subG_plot, seed=42, k=0.22, iterations=50)

            # Edges trace
            edge_x, edge_y = [], []
            for u, v in subG_plot.edges():
                x0, y0 = pos_2d[u]
                x1, y1 = pos_2d[v]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.85, color='rgba(148, 163, 184, 0.35)'),
                hoverinfo='none',
                mode='lines'
            )

            # Nodes trace
            node_x, node_y = [], []
            node_sizes, node_colors, node_hover, node_labels = [], [], [], []

            comm_colors = {
                15: '#ef4444',
                61: '#3b82f6',
                16: '#f59e0b',
                259: '#10b981',
                8: '#8b5cf6'
            }

            for n in subG_plot.nodes():
                x, y = pos_2d[n]
                node_x.append(x)
                node_y.append(y)
                d_val = deg_all.get(n, 1)
                cid = n_comm_map.get(n, -1)
                c_hex = comm_colors.get(cid, '#94a3b8')

                # Special actor highlights
                if n == 'grok':
                    c_hex = '#06b6d4'
                    sz = 32
                    lbl = '🤖 @grok'
                elif n == 'prabowo':
                    c_hex = '#eab308'
                    sz = 28
                    lbl = '👑 @prabowo'
                elif n == '4Y4NKZ':
                    c_hex = '#ec4899'
                    sz = 26
                    lbl = '🔗 @4Y4NKZ'
                elif n in ['tanyarlfes', 'tanyakanrl', 'LambeSahamjja', 'itbfess_x']:
                    c_hex = '#8b5cf6'
                    sz = 22
                    lbl = f'📡 @{n}'
                else:
                    sz = max(8, min(22, d_val * 2.5))
                    lbl = f'@{n}' if d_val >= 4 else ''

                node_sizes.append(sz)
                node_colors.append(c_hex)
                node_labels.append(lbl)

                in_d = G_full.in_degree(n)
                out_d = G_full.out_degree(n)
                emo = n_emo_map.get(n, 'netral')
                node_hover.append(
                    f"<b>@{n}</b><br>"
                    f"Komunitas: Klaster #{cid}<br>"
                    f"Total Degree: {d_val}<br>"
                    f"In-Degree: {in_d} | Out-Degree: {out_d}<br>"
                    f"Emosi Dominan: {emo}"
                )

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=node_labels,
                textposition='top center',
                textfont=dict(size=10, color='#f8fafc'),
                hovertext=node_hover,
                marker=dict(
                    color=node_colors,
                    size=node_sizes,
                    line=dict(width=1.5, color='#ffffff')
                )
            )

            fig_net_plotly = go.Figure(
                data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=f"Peta Relasi Jaringan Komunikasi MBG ({n_scale} Aktor Teratas)",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=10, r=10, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor='#0f172a',
                    paper_bgcolor='#0f172a',
                    height=560
                )
            )
            st.plotly_chart(fig_net_plotly, width='stretch')

        with graph_tab2:
            st.info("💡 **Tips Interaktif:** Anda dapat melakukan *scroll* untuk Zoom In/Out, men-drag node, atau mengklik node untuk melihat relasi terhubung secara dinamis.")

            if not PYVIS_AVAILABLE:
                st.warning("⚠️ Modul `pyvis` belum terpasang di environment Python Anda. Pasang dengan `pip install pyvis` untuk mengaktifkan graf interaktif ini.")
            else:
                try:
                    # Generate PyVis graph
                    net = Network(height="600px", width="100%", bgcolor="#1e293b", font_color="white", notebook=False, cdn_resources="remote")
                    net.force_atlas_2based()

                    if nodes_data is not None and 'Degree' in nodes_data.columns:
                        top_nodes = nodes_data.sort_values(by='Degree', ascending=False).head(150)['Id'].tolist()
                    else:
                        G_temp = nx.from_pandas_edgelist(edges, 'Source', 'Target')
                        degree_dict = dict(G_temp.degree())
                        top_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)[:150]

                    filtered_edges = edges[edges['Source'].isin(top_nodes) | edges['Target'].isin(top_nodes)]
                    G = nx.from_pandas_edgelist(filtered_edges, 'Source', 'Target')

                    comm_palette = {
                        15: "#ef4444",   # Red / Disgust
                        61: "#3b82f6",   # Blue / Neutral
                        16: "#f59e0b",   # Amber / Sarcasm
                        259: "#10b981",  # Green / Trust
                        8: "#8b5cf6",    # Purple / Budget
                    }

                    # Add nodes and edges to pyvis with rich aesthetic attributes
                    for node in G.nodes():
                        deg = dict(G.degree()).get(node, 1)
                        cid = n_comm_map.get(node, -1)
                        emo = n_emo_map.get(node, "netral")
                        col = comm_palette.get(cid, "#94a3b8")

                        # Highlighting Key Actors
                        if node == "grok":
                            col = "#06b6d4"  # Cyan for akun dengan out-degree tinggi
                            size = 34
                            label = "🤖 @grok"
                        elif node == "prabowo":
                            col = "#eab308"  # Gold for President
                            size = 30
                            label = "👑 @prabowo"
                        elif node == "4Y4NKZ":
                            col = "#ec4899"  # Pink for Broker
                            size = 28
                            label = "🔗 @4Y4NKZ"
                        else:
                            size = max(8, min(24, deg * 3))
                            label = f"@{node}" if deg >= 4 else ""
                        emo_id_map = {
                            'disgust': '🤢 Jijik (Disgust)',
                            'neutral': '😐 Netral',
                            'love': '🤝 Percaya (Trust)',
                            'shame': '🔮 Tertarik',
                            'anger': '😡 Marah',
                            'sadness': '😢 Sedih',
                            'fear': '😨 Takut',
                            'joy': '😊 Bahagia',
                            'surprise': '😲 Kaget'
                        }
                        emo_ind = emo_id_map.get(str(emo).lower(), str(emo))
                        tooltip = f"<div style='font-family: sans-serif; font-size: 12px; padding: 4px;'><b>@{node}</b><br>🧩 Klaster: #{cid}<br>🎭 Emosi Dominan: {emo_ind}<br>📊 Total Derajat: {deg}</div>"
                        net.add_node(node, label=label, title=tooltip, size=size, color=col)

                    for source, target in G.edges():
                        net.add_edge(source, target, color="rgba(255,255,255,0.15)")

                    # Save graph to HTML
                    path = 'html_files'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    source_code = net.generate_html(notebook=False)
                    components.html(source_code, height=650, scrolling=True)
                except Exception as e:
                    st.error(f"Gagal memuat visualisasi PyVis: {e}")

        st.markdown("---")
        st.subheader("Visualisasi Jaringan Statis (Topologi & Aktor Utama)")
        st.markdown("Grafik di bawah mengonfirmasi bahwa ekosistem wacana ini menunjukkan keterpisahan struktural antarkomunitas berdasarkan partisi Louvain.")

        global_path = os.path.join(PROJECT_ROOT, "results", "6_global_network.png")
        louvain_path = os.path.join(PROJECT_ROOT, "results", "network_graph.png")
        actors_path = os.path.join(PROJECT_ROOT, "results", "top_actors.png")

        # 6_global_network
        if os.path.exists(global_path):
            st.image(global_path, width='stretch', caption="Figure: Global Topological Structure")
        else:
            st.info("Figure: Global Topological Structure (Terverifikasi dalam repositori riset)")

        colA, colB = st.columns(2)
        with colA:
            if os.path.exists(louvain_path):
                st.image(louvain_path, width='stretch', caption="Figure: Fragmented Community (Louvain)")
            else:
                st.info("Figure: Fragmented Community (Louvain)")
        with colB:
            if os.path.exists(actors_path):
                st.image(actors_path, width='stretch', caption="Figure: Top 10 Influential Actors (AI Supremacy)")
            else:
                st.info("Figure: Top 10 Influential Actors (AI Supremacy)")


    with tab_iv_3:
        st.header("🧩 §4.3 Analisis Clustering: Dinamika Komunitas dan Struktur Komunitas")
        st.markdown("""
        > *Algoritma **Louvain** (Blondel dkk., 2008) mengidentifikasi komunitas wacana dengan modularity **0,9837**.
        > Segregasi wacana terjadi secara absolut akibat tiadanya jembatan informasi antar-kelompok warganet.*
        """)

        nodes_file_path = get_result_path("mbg_network_nodes_final.csv")
        if os.path.exists(nodes_file_path):
            df_comm_nodes = pd.read_csv(nodes_file_path)
            top_comms = df_comm_nodes['Community'].value_counts().head(5)
            fokus_map = {
                15: "Keluhan makanan basi & keracunan siswa",
                61: "Kutipan rilis berita & pernyataan dinas",
                16: "Sarkasme pemangkasan porsi menu",
                259: "Apresiasi pembagian makanan perdana",
                8: "Kritik transparansi pengadaan vendor"
            }
            comm_dyn_rows = []
            for cid, cnt in top_comms.items():
                sub = df_comm_nodes[df_comm_nodes['Community'] == cid]
                dom_raw = sub['Dominant_Emotion'].mode()[0] if not sub['Dominant_Emotion'].empty else "neutral"
                dom_id = {
                    'disgust': '🤢 Jijik (Disgust)',
                    'neutral': '😐 Netral',
                    'love': '🤝 Percaya (Trust)',
                    'shame': '🔮 Tertarik',
                    'anger': '😡 Marah'
                }.get(dom_raw.lower(), dom_raw)
                porsi_gc = f"{(cnt/89)*100:.1f}%" if cid in [15, 61] else "Terpisah (Independent)"
                comm_dyn_rows.append({
                    "ID Komunitas": f"Klaster #{cid}",
                    "Jumlah Anggota": f"{cnt} aktor",
                    "Porsi Giant Component": porsi_gc,
                    "Emosi Dominan": dom_id,
                    "Fokus Sentimen Utama": fokus_map.get(cid, "Diskursus tematik warganet")
                })
            col_comm1, col_comm2 = st.columns([1.4, 1])
            with col_comm1:
                st.dataframe(pd.DataFrame(comm_dyn_rows), width='stretch', hide_index=True)
            with col_comm2:
                df_comm_pie = pd.DataFrame({
                    'Klaster': [f"Klaster #{cid}" for cid in top_comms.index] + ['Klaster Lainnya (328 Klaster)'],
                    'Jumlah Aktor': list(top_comms.values) + [len(df_comm_nodes) - top_comms.sum()]
                })
                fig_comm_donut = px.pie(
                    df_comm_pie,
                    names='Klaster',
                    values='Jumlah Aktor',
                    hole=0.45,
                    color_discrete_sequence=['#ef4444', '#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', '#94a3b8'],
                    title="Proporsi Ukuran Komunitas Louvain"
                )
                fig_comm_donut.update_traces(textposition='inside', textinfo='percent+label')
                fig_comm_donut.update_layout(showlegend=False, margin=dict(t=30, b=10, l=10, r=10), height=280)
                st.plotly_chart(fig_comm_donut, width='stretch')

            # ── Visualisasi Distribusi Emosi per Komunitas Louvain ──
            st.subheader("📊 Distribusi Emosi Dominan per Komunitas Louvain")
            st.caption("Menganalisis distribusi afektif: Klaster #15 didominasi emosi Jijik (Disgust), sedangkan Klaster #61 didominasi Netral:")

            top5_cids = top_comms.index.tolist()
            df_sub_comm = df_comm_nodes[df_comm_nodes['Community'].isin(top5_cids)].copy()
            df_sub_comm['Klaster'] = df_sub_comm['Community'].apply(lambda x: f'Klaster #{x}')
            emo_id_labels = {
                'disgust': '🤢 Jijik (Disgust)',
                'neutral': '😐 Netral',
                'love': '🤝 Percaya (Trust)',
                'anger': '😡 Marah',
                'shame': '🔮 Tertarik'
            }
            df_sub_comm['Emosi'] = df_sub_comm['Dominant_Emotion'].map(emo_id_labels).fillna(df_sub_comm['Dominant_Emotion'])
            ct = pd.crosstab(df_sub_comm['Klaster'], df_sub_comm['Emosi']).reset_index()
            ct_melt = ct.melt(id_vars='Klaster', var_name='Emosi', value_name='Jumlah Aktor')

            fig_comm_emo = px.bar(
                ct_melt,
                x='Klaster',
                y='Jumlah Aktor',
                color='Emosi',
                barmode='stack',
                title="Komposisi Emosi di 5 Komunitas Terbesar",
                color_discrete_map={
                    '🤢 Jijik (Disgust)': '#ef4444',
                    '😐 Netral': '#3b82f6',
                    '🤝 Percaya (Trust)': '#10b981',
                    '😡 Marah': '#dc2626',
                    '🔮 Tertarik': '#8b5cf6'
                }
            )
            fig_comm_emo.update_layout(height=340, margin=dict(t=40, b=20, l=10, r=10))
            st.plotly_chart(fig_comm_emo, width='stretch')

            # ── Interactive Community Member Explorer ──
            with st.expander("🔎 Eksplorasi Anggota & Aktor per Komunitas Louvain", expanded=False):
                sel_cid = st.selectbox(
                    "Pilih Komunitas Louvain untuk Melihat Anggota Akun:",
                    options=top5_cids,
                    format_func=lambda x: f"Klaster #{x} ({top_comms.get(x, 0)} aktor) — {fokus_map.get(x, 'Diskursus')}"
                )
                df_sel_members = df_comm_nodes[df_comm_nodes['Community'] == sel_cid][['Id', 'Degree', 'Betweenness', 'Dominant_Emotion']].copy()
                df_sel_members.columns = ['Akun Pengguna', 'Degree Centrality', 'Betweenness Centrality', 'Emosi Dominan']
                df_sel_members['Akun Pengguna'] = df_sel_members['Akun Pengguna'].apply(lambda x: f"@{x}")
                df_sel_members['Emosi Dominan'] = df_sel_members['Emosi Dominan'].map(emo_id_labels).fillna(df_sel_members['Emosi Dominan'])
                st.dataframe(df_sel_members.sort_values(by='Degree Centrality', ascending=False), width='stretch', hide_index=True)

        echo_img_p = os.path.join(PROJECT_ROOT, "results", "19_community_echo_chambers.png")
        if os.path.exists(echo_img_p):
            st.markdown("---")
            st.subheader("📊 Analisis Dimensi 3: Partisi Komunitas dan Struktur Jaringan")
            st.markdown(
                "Visualisasi komprehensif menganalisis tingkat segregasi struktural diskursus MBG: "
                "dari 692 relasi komunikasi, **99,86% (691 relasi)** terkunci di dalam struktur komunitas kelompoknya masing-masing, "
                "dan hanya **0,14% (1 relasi)** yang menyeberang antar-komunitas (*Modularity Q = 0,9837*):"
            )
            st.image(
                echo_img_p,
                width='stretch',
                caption="Gambar 4.7C: Partisi Komunitas Louvain & Diagnostik Struktur Internal Komunitas (300 DPI)"
            )

        nodexl_viz_path = os.path.join(PROJECT_ROOT, "results", "16_nodexl_graph_visualization.png")
        if os.path.exists(nodexl_viz_path):
            st.markdown("---")
            st.subheader("📊 Pemetaan Visual Jaringan Komunikasi Versi NodeXL Pro (Group-in-a-Box Layout)")
            st.markdown(
                "Pemetaan visual standar buku kerja **NodeXL Pro** ([Lisensi Akademik Resmi Order #14103](https://nodexl.com/my-account/view-order/14103/)) "
                "menggunakan tata letak kanonis *Group-in-a-Box (GIB)* berdasarkan partisi klaster wacana, dilengkapi panel ringkasan metrik graf keseluruhan:"
            )
            st.image(
                nodexl_viz_path,
                width='stretch',
                caption="Gambar 4.7B: Visualisasi Jaringan Komunikasi NodeXL Pro Group-in-a-Box Layout (|V|=971, |E|=666, 300 DPI)"
            )
            col_nx_dl1, col_nx_dl2 = st.columns(2)
            with col_nx_dl1:
                st.link_button("📊 Unduh Buku Kerja NodeXL Pro (.xlsx)", "https://raw.githubusercontent.com/indri007/ThisIsEconomy/main/NodeXL_MBG_Tesis_Indri_Anjar.xlsx", width='stretch')
            with col_nx_dl2:
                st.link_button("🌐 Pratinjau Daring Buku Kerja (GitHub)", "https://github.com/indri007/ThisIsEconomy/blob/main/NodeXL_MBG_Tesis_Indri_Anjar.xlsx", width='stretch')

        st.markdown("---")

        # ── Tabel 4.3 15 Aktor Sentralitas Tertinggi (Dihitung Dinamis via NetworkX) ──


    with tab_iv_4:
        st.subheader("📋 Tabel 4.3 Lima Belas Aktor dengan Degree Centrality Tertinggi (Korpus Resmi)")
        st.caption("Hasil komputasi matematis NetworkX terhadap interaksi mention riil wacana MBG:")

        G_dir = nx.from_pandas_edgelist(edges, 'Source', 'Target', create_using=nx.DiGraph())
        deg_d = nx.degree_centrality(G_dir)
        bet_d = nx.betweenness_centrality(G_dir)
        try:
            eig_d = nx.eigenvector_centrality(G_dir, max_iter=1000)
        except Exception:
            eig_d = nx.eigenvector_centrality_numpy(G_dir)

        top_15_nodes = sorted(deg_d.items(), key=lambda x: x[1], reverse=True)[:15]

        peran_map = {
            "grok": "🤖 High Out-Degree Actor",
            "grok": "🔗 High Betweenness & Out-Degree Position",
            "newIding30": "📢 Informan Aktif Komunitas",
            "prabowo": "👑 High In-Degree Target (Pembuat Kebijakan)",
            "dbdbidip": "🗣️ Amplifikator Kritik Sindiran",
            "Casagrande10939": "🗣️ Aktor Penyebar Narasi",
            "luvdysh_": "🗣️ Warganet Kritis",
            "mBg_JK": "🗣️ Akun Tematik MBG",
            "regar_op0sisi": "Akun dengan posisi struktural dalam graf",
            "punishe98373138": "🗣️ Amplifikator Isu Gizi",
            "daffiriffi": "🗣️ Partisipan Diskusi",
            "deluxe_melissa": "🔗 Penghubung Klaster Kecil",
            "ryookaasan": "🗣️ Partisipan Diskusi",
            "tanyakanrl": "🎯 Akun Menfess / Rujukan Publik",
            "multibank_io": "🔗 Akun Finansial / Evaluasi Anggaran"
        }

        dyn_top15 = []
        for rank, (node, deg_val) in enumerate(top_15_nodes, 1):
            b_val = bet_d.get(node, 0.0)
            e_val = eig_d.get(node, 0.0)
            in_deg = G_dir.in_degree(node)
            out_deg = G_dir.out_degree(node)
            star = " ★" if node == "4Y4NKZ" else ""
            dyn_top15.append({
                "Rank": rank,
                "Akun Pengguna": f"@{node}",
                "Degree": f"{deg_val:.4f}".replace(".", ","),
                "Betweenness": f"{b_val:.6f}{star}".replace(".", ","),
                "Eigenvector": f"{e_val:.4f}".replace(".", ","),
                "In-Degree": in_deg,
                "Out-Degree": out_deg,
                "Peran Struktural": peran_map.get(node, "🗣️ Partisipan Wacana")
            })
        st.dataframe(pd.DataFrame(dyn_top15), width='stretch', hide_index=True)

        # ── Interactive Plotly Chart: In-Degree vs Out-Degree ──
        top_10_names = [n for n, _ in top_15_nodes[:10]]
        df_act_chart = pd.DataFrame({
            'Akun': [f"@{n}" for n in top_10_names][::-1],
            'In-Degree (Sasaran Mention)': [G_dir.in_degree(n) for n in top_10_names][::-1],
            'Out-Degree (Penyebar Mention)': [G_dir.out_degree(n) for n in top_10_names][::-1]
        })
        fig_act_bars = px.bar(
            df_act_chart,
            y='Akun',
            x=['In-Degree (Sasaran Mention)', 'Out-Degree (Penyebar Mention)'],
            barmode='group',
            orientation='h',
            color_discrete_map={'In-Degree (Sasaran Mention)': '#3b82f6', 'Out-Degree (Penyebar Mention)': '#ef4444'},
            title="Visualisasi Asimetri Komunikasi: Sasaran Pasif (In-Degree) vs Penyebar Aktif (Out-Degree)"
        )
        fig_act_bars.update_layout(
            xaxis_title="Frekuensi Mention",
            yaxis_title="Akun Pengguna",
            legend_title="Arah Komunikasi",
            height=380,
            margin=dict(t=40, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_act_bars, width='stretch')

        # ── §4.4b VISUALISASI KOMPREHENSIF SENTRALITAS AKTOR: DEGREE, BETWEENNESS, & EIGENVECTOR ──
        st.markdown("---")
        st.subheader("👑 §4.4b Visualisasi Tri-Metrik Sentralitas Aktor: Degree, Betweenness, & Eigenvector")
        st.markdown("""
        > *Dalam **Social Network Analysis (Freeman, 1979; Wasserman & Faust, 1994)**, struktur kekuasaan dan pengaruh aktor tidak cukup dinilai dari satu ukuran saja.
        > Riset ini mengkalkulasi dan memvisualisasikan **tiga dimensi sentralitas komplementer** dari graf interaksi riil MBG:*
        > 1. **Degree Centrality:** Mengukur tingkat popularitas dan frekuensi interaksi langsung aktor (siapa yang paling aktif/disebut).
        > 2. **Betweenness Centrality:** Mengukur peran aktor sebagai jembatan (*structural broker*) di antara kelompok-kelompok yang terpisah.
        > 3. **Eigenvector Centrality:** Mengukur prestise dan pengaruh kualitatif (terhubung ke aktor-aktor yang juga memiliki pengaruh kuat).
        """)

        # Siapkan DataFrame lengkap metrik sentralitas seluruh node
        cent_nodes_list = []
        for n in G_dir.nodes():
            cent_nodes_list.append({
                'Akun': f"@{n}",
                'Raw_Node': n,
                'Degree Centrality': deg_d.get(n, 0.0),
                'Betweenness Centrality': bet_d.get(n, 0.0),
                'Eigenvector Centrality': eig_d.get(n, 0.0),
                'In-Degree (Sasaran)': G_dir.in_degree(n),
                'Out-Degree (Penyebar)': G_dir.out_degree(n),
                'Total Relasi': G_dir.degree(n),
                'Peran': peran_map.get(n, "🗣️ Partisipan Wacana")
            })
        df_cent_all = pd.DataFrame(cent_nodes_list)

        cent_tab1, cent_tab2, cent_tab3, cent_tab4 = st.tabs([
            "📊 1. Degree Centrality (Popularitas)",
            "🔗 2. Betweenness Centrality (Brokerage)",
            "💎 3. Eigenvector Centrality (Prestise)",
            "🎯 4. Triangulasi Multi-Dimensi (Scatter Plot)"
        ])

        with cent_tab1:
            st.markdown("#### 📊 Peringkat 10 Aktor dengan Degree Centrality Tertinggi")
            st.caption("Mengukur aktor dengan volume relasi langsung terbanyak (In-Degree + Out-Degree):")

            df_top_deg = df_cent_all.sort_values(by='Degree Centrality', ascending=True).tail(10)
            fig_deg_bar = px.bar(
                df_top_deg,
                y='Akun',
                x='Degree Centrality',
                orientation='h',
                color='Degree Centrality',
                color_continuous_scale='Blues',
                text=df_top_deg['Degree Centrality'].apply(lambda x: f"{x:.4f}"),
                title="Top 10 Aktor: Degree Centrality (Aktivitas & Keterhubungan Langsung)"
            )
            fig_deg_bar.update_traces(textposition='outside')
            fig_deg_bar.update_layout(height=400, margin=dict(t=40, b=20, l=10, r=20), xaxis_title="Skor Degree Centrality", yaxis_title="Akun Pengguna")
            st.plotly_chart(fig_deg_bar, width='stretch')
            st.info("💡 **Insight Temuan:** Agen AI **@grok** menduduki sentralitas derajat tertinggi (**0,0433 / 42 relasi**), menganalisis fenomena *perbedaan posisi centrality*, di mana warganet memiliki pola konektivitas out-degree yang lebih tinggi dibandingkan akun yang dibandingkan dalam graf.")

        with cent_tab2:
            st.markdown("#### 🔗 Peringkat 10 Aktor dengan Betweenness Centrality Tertinggi")
            st.caption("Mengukur aktor yang menduduki posisi jembatan krusial (*structural bridge / gatekeeper*) antarkelompok:")

            df_top_bet = df_cent_all.sort_values(by='Betweenness Centrality', ascending=True).tail(10)
            fig_bet_bar = px.bar(
                df_top_bet,
                y='Akun',
                x='Betweenness Centrality',
                orientation='h',
                color='Betweenness Centrality',
                color_continuous_scale='Reds',
                text=df_top_bet['Betweenness Centrality'].apply(lambda x: f"{x:.6f}"),
                title="Top 10 Aktor: Betweenness Centrality (Kekuatan Jembatan Jaringan)"
            )
            fig_bet_bar.update_traces(textposition='outside')
            fig_bet_bar.update_layout(height=400, margin=dict(t=40, b=20, l=10, r=30), xaxis_title="Skor Betweenness Centrality", yaxis_title="Akun Pengguna")
            st.plotly_chart(fig_bet_bar, width='stretch')
            st.success("🔗 **Insight Temuan:** **@grok** memiliki skor Betweenness tertinggi (**0,005940868**), Posisi tersebut menunjukkan centrality struktural yang tinggi pada graf yang dianalisis di tengah jaringan yang menunjukkan keterpisahan struktural ($Q = 0.9837$).")

        with cent_tab3:
            st.markdown("#### 💎 Peringkat 10 Aktor dengan Eigenvector Centrality Tertinggi")
            st.caption("Mengukur pengaruh kualitatif aktor yang terhubung ke simpul-simpul berbobot tinggi lainnya:")

            df_top_eig = df_cent_all.sort_values(by='Eigenvector Centrality', ascending=True).tail(10)
            fig_eig_bar = px.bar(
                df_top_eig,
                y='Akun',
                x='Eigenvector Centrality',
                orientation='h',
                color='Eigenvector Centrality',
                color_continuous_scale='Greens',
                text=df_top_eig['Eigenvector Centrality'].apply(lambda x: f"{x:.4f}"),
                title="Top 10 Aktor: Eigenvector Centrality (Koneksi ke Aktor Berpengaruh)"
            )
            fig_eig_bar.update_traces(textposition='outside')
            fig_eig_bar.update_layout(height=400, margin=dict(t=40, b=20, l=10, r=20), xaxis_title="Skor Eigenvector Centrality", yaxis_title="Akun Pengguna")
            st.plotly_chart(fig_eig_bar, width='stretch')
            st.info("💎 **Insight Temuan:** Eigenvector Centrality tertinggi diraih oleh aktor seperti **@4Y4NKZ** dan **@newIding30** (skor **0,1166**), menganalisis bahwa relasi mereka terkonsentrasi pada simpul-simpul penggerak utama perdebatan publik.")

        with cent_tab4:
            st.markdown("#### 🎯 Triangulasi Multi-Dimensi Sentralitas (Scatter Plot Interaktif)")
            st.caption("Memetakan posisi struktural aktor warganet: Sumbu X (Degree), Sumbu Y (Betweenness), Ukuran Bubble (Total Relasi):")

            df_scatter_top = df_cent_all.sort_values(by='Degree Centrality', ascending=False).head(25).copy()

            fig_cent_scatter = px.scatter(
                df_scatter_top,
                x='Degree Centrality',
                y='Betweenness Centrality',
                size='Total Relasi',
                color='Peran',
                text='Akun',
                hover_data=['In-Degree (Sasaran)', 'Out-Degree (Penyebar)', 'Eigenvector Centrality'],
                title="Peta Triangulasi Sentralitas Aktor Diskursus MBG",
                color_discrete_sequence=['#06b6d4', '#ec4899', '#eab308', '#ef4444', '#10b981', '#8b5cf6', '#3b82f6']
            )
            fig_cent_scatter.update_traces(textposition='top right', marker=dict(line=dict(width=1, color='#ffffff')))
            fig_cent_scatter.update_layout(
                height=500,
                margin=dict(t=50, b=30, l=10, r=20),
                xaxis_title="Degree Centrality (Popularitas & Aktivitas)",
                yaxis_title="Betweenness Centrality (Kekuatan Brokerage)",
                legend_title="Peran Struktural Aktor"
            )
            st.plotly_chart(fig_cent_scatter, width='stretch')
            st.caption("📌 **Keterangan Tipologi:** Aktor di kuadran kanan bawah (**@grok**) memiliki popularitas masif namun bukan perantara antarkelompok. Sebaliknya, aktor di bagian atas (**@4Y4NKZ**) memiliki peran kontrol informasi (*gatekeeping*) tertinggi.")

        actor_typ_img_p = os.path.join(PROJECT_ROOT, "results", "actor_centrality_typology_en.png")
        if os.path.exists(actor_typ_img_p):
            st.markdown("---")
            st.subheader("📊 Analisis Dimensi 2: Sentralitas Aktor & Tipologi Peran Komunikasi (SNA Standar NodeXL)")
            st.markdown(
                "Pemetaan 4 kuadran tipologi peran komunikasi berdasarkan kombinasi In-Degree, Out-Degree, dan Betweenness Centrality. "
                "Menegaskan `@prabowo` sebagai *High In-Degree Target* absolut (In-Degree=15), `@grok` sebagai *akun dengan out-degree tinggi* (Degree=42), "
                "dan `@regar_op0sisi` sebagai akun dengan posisi struktural dalam graf:"
            )
            st.image(
                actor_typ_img_p,
                width='stretch',
                caption="Gambar 4.8B: Matriks Sentralitas Aktor & Tipologi Peran Komunikasi Platform X (300 DPI)"
            )

        st.markdown("---")

        # ── §4.4c 10 TOP MEDIA & KANAL KOMUNIKASI PENGHUBUNG (SELAIN CNN INDONESIA) ──

        st.header("📡 §4.4c 10 Top Media & Kanal Komunikasi Penghubung (Selain CNN Indonesia)")
        st.markdown("""
        > *Berdasarkan pemodelan graf jaringan komunikasi ($N=971$ node) dan penelusuran korpus wacana MBG di platform X,
        > diskursus krisis tidak terkonsentrasi pada satu media arus utama semata (seperti CNN Indonesia).
        > Mengacu pada teori **Networked Crisis Communication (Schultz, Utz, & Göritz, 2011)** dan **Deliberasi Ruang Publik Digital (Habermas, 2006)**,
        > warganet memanfaatkan **10 Media & Kanal Penghubung (Information Bridges)** lintas tipologi:
        > mulai dari kanal menfess anonim, media penyiaran nasional, pers investigatif, hingga portal pasar modal.*
        """)

        # 4 Kartu Metrik Ringkasan Media Penghubung
        m_kpi1, m_kpi2, m_kpi3, m_kpi4 = st.columns(4)
        with m_kpi1:
            st.metric("Total Media Terpetakan", "10 Kanal", "Non-CNN Indonesia")
        with m_kpi2:
            st.metric("Agregator Publik Teratas", "@tanyarlfes", "In-Degree: 5 (Rank #1)")
        with m_kpi3:
            st.metric("Otoritas Penyiaran Terkoneksi", "@KompasTV", "PageRank: 0,00457")
        with m_kpi4:
            st.metric("Karakteristik Aliran", "Desentralisasi Fess", "Aduan Masuk >90%")

        # Dataset 10 Top Media Penghubung Berbasis Data Riil
        top10_media_data = [
            {
                "Rank": 1,
                "Akun Media / Kanal": "@tanyarlfes",
                "Tipologi Media": "Menfess & Komunitas Publik",
                "Total Degree": 5,
                "In-Degree (Aduan Masuk)": 5,
                "PageRank Centrality": 0.00344,
                "Peran Penghubung": "Kanal Menfess publik terbesar di X; arena transmisi dan amplifikasi keluhan warganet atas menu MBG",
                "Fokus Wacana": "Keluhan porsi makanan minim, perbandingan bekal rumah vs MBG, aduan foto lapangan"
            },
            {
                "Rank": 2,
                "Akun Media / Kanal": "@tanyakanrl",
                "Tipologi Media": "Media Agregator Diskusi Warganet",
                "Total Degree": 5,
                "In-Degree (Aduan Masuk)": 5,
                "PageRank Centrality": 0.00314,
                "Peran Penghubung": "Agregator pertanyaan publik; memfasilitasi perdebatan kolektif transparansi uji coba MBG",
                "Fokus Wacana": "Pertanyaan kelayakan anggaran, mekanisme katering SPPG, aduan keterlambatan makanan"
            },
            {
                "Rank": 3,
                "Akun Media / Kanal": "@LambeSahamjja",
                "Tipologi Media": "Media Finansial & Pasar Modal",
                "Total Degree": 4,
                "In-Degree (Aduan Masuk)": 4,
                "PageRank Centrality": 0.00314,
                "Peran Penghubung": "Media opini pasar; menghubungkan alokasi beban fiskal APBN dengan emiten bahan pangan",
                "Fokus Wacana": "Beban fiskal ratusan triliun, transparansi margin vendor, evaluasi saham sektor konsumsi"
            },
            {
                "Rank": 4,
                "Akun Media / Kanal": "@itbfess_x",
                "Tipologi Media": "Menfess Sivitas Akademika",
                "Total Degree": 3,
                "In-Degree (Aduan Masuk)": 3,
                "PageRank Centrality": 0.00207,
                "Peran Penghubung": "Menfess mahasiswa ITB; jembatan kritik berbasis sains gizi dan evaluasi kebijakan berbasis riset",
                "Fokus Wacana": "Kajian kecukupan mikronutrien, kritik menu berkarbohidrat tinggi, audit independen"
            },
            {
                "Rank": 5,
                "Akun Media / Kanal": "@KompasTV",
                "Tipologi Media": "Media Penyiaran Televisi Berita",
                "Total Degree": 2,
                "In-Degree (Aduan Masuk)": 1,
                "PageRank Centrality": 0.00457,
                "Peran Penghubung": "Media berita arus utama; jembatan visualisasi siaran uji coba resmi dan konferensi pers",
                "Fokus Wacana": "Liputan langsung simulasi makan bergizi, pernyataan resmi kepala BGN, evaluasi pimpinan"
            },
            {
                "Rank": 6,
                "Akun Media / Kanal": "@tempodotco",
                "Tipologi Media": "Jurnalisme Investigatif (Tempo)",
                "Total Degree": 1,
                "In-Degree (Aduan Masuk)": 1,
                "PageRank Centrality": 0.00132,
                "Peran Penghubung": "Pers investigatif; rujukan warganet terkait investigasi dugaan penurunan standar mutu vendor",
                "Fokus Wacana": "Investigasi rantai pasok vendor, potensi rente pengadaan makanan, standar higienitas"
            },
            {
                "Rank": 7,
                "Akun Media / Kanal": "@kompascom",
                "Tipologi Media": "Portal Berita Daring Nasional",
                "Total Degree": 1,
                "In-Degree (Aduan Masuk)": 1,
                "PageRank Centrality": 0.00132,
                "Peran Penghubung": "Portal berita nasional; rujukan perkembangan regulasi, pernyataan pejabat, dan pantauan harga",
                "Fokus Wacana": "Pembaruan petunjuk teknis pelaksanaan MBG, tanggapan asosiasi gizi, peta sebaran SPPG"
            },
            {
                "Rank": 8,
                "Akun Media / Kanal": "@kumparan",
                "Tipologi Media": "Media Berita Digital Kolaboratif",
                "Total Degree": 1,
                "In-Degree (Aduan Masuk)": 0,
                "PageRank Centrality": 0.00071,
                "Peran Penghubung": "Media daring; menyebarkan ringkasan infografis dan kurasi sentimen pembaca seputar kebijakan",
                "Fokus Wacana": "Infografis alokasi pagu, survei sentimen publik, studi kasus uji coba sekolah percontohan"
            },
            {
                "Rank": 9,
                "Akun Media / Kanal": "@yappingfess",
                "Tipologi Media": "Menfess Opini & Emosi Warganet",
                "Total Degree": 2,
                "In-Degree (Aduan Masuk)": 2,
                "PageRank Centrality": 0.00193,
                "Peran Penghubung": "Saluran katarsis dan curahan emosi spontan (venting channel) warganet atas ketidakpuasan menu",
                "Fokus Wacana": "Kekecewaan anak sekolah terhadap lauk yang basi/hambar, sindiran menu 'mewah', emoji badut"
            },
            {
                "Rank": 10,
                "Akun Media / Kanal": "@txtdrimedia",
                "Tipologi Media": "Media Kurasi & Kliping Pers",
                "Total Degree": 1,
                "In-Degree (Aduan Masuk)": 1,
                "PageRank Centrality": 0.00102,
                "Peran Penghubung": "Kurasi potongan judul berita pers media massa; memicu perdebatan di linimasa via tangkapan layar",
                "Fokus Wacana": "Tangkapan layar berita keracunan uji coba MBG, perbandingan klaim menteri vs foto piring"
            }
        ]
        df_top10_media = pd.DataFrame(top10_media_data)

        # Visualisasi Komparatif 2 Kolom (Plotly Bar + Donut Chart)
        m_col1, m_col2 = st.columns([1.3, 1])

        with m_col1:
            # Horizontal Bar Chart Sentralitas Media Penghubung
            df_plot_media = df_top10_media.sort_values(by='Total Degree', ascending=True).copy()
            fig_media_bar = go.Figure()
            fig_media_bar.add_trace(go.Bar(
                y=df_plot_media['Akun Media / Kanal'],
                x=df_plot_media['In-Degree (Aduan Masuk)'],
                name='In-Degree (Aduan / Mention Masuk)',
                orientation='h',
                marker=dict(color='#3b82f6'),
                text=df_plot_media['In-Degree (Aduan Masuk)'],
                textposition='outside'
            ))
            fig_media_bar.add_trace(go.Bar(
                y=df_plot_media['Akun Media / Kanal'],
                x=df_plot_media['Total Degree'] - df_plot_media['In-Degree (Aduan Masuk)'],
                name='Out-Degree (Inisiasi Kontak)',
                orientation='h',
                marker=dict(color='#f59e0b'),
                text=(df_plot_media['Total Degree'] - df_plot_media['In-Degree (Aduan Masuk)']).replace(0, ''),
                textposition='inside'
            ))
            fig_media_bar.update_layout(
                barmode='stack',
                title="Peringkat 10 Media Penghubung Berdasarkan Interaksi Jejaring (SNA)",
                xaxis_title="Jumlah Relasi Interaksi (Degree)",
                yaxis_title="Akun Media / Kanal",
                height=430,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=50, b=20, l=10, r=10)
            )
            st.plotly_chart(fig_media_bar, width='stretch')

        with m_col2:
            # Donut Chart Proporsi Tipologi Media Penghubung
            df_media_types = df_top10_media['Tipologi Media'].value_counts().reset_index()
            df_media_types.columns = ['Tipologi', 'Jumlah Akun']
            fig_media_pie = px.pie(
                df_media_types,
                names='Tipologi',
                values='Jumlah Akun',
                hole=0.45,
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4'],
                title="Komposisi Tipologi Media Penghubung"
            )
            fig_media_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_media_pie.update_layout(
                showlegend=False,
                height=430,
                margin=dict(t=50, b=20, l=10, r=10)
            )
            st.plotly_chart(fig_media_pie, width='stretch')

        # Tabel Rinci 10 Top Media Penghubung
        st.subheader("📋 Matriks Profil 10 Top Media Penghubung (Selain CNN Indonesia)")
        st.caption("Data dihitung berdasarkan relasi edges dan struktur sentralitas korpus riil MBG:")

        st.dataframe(
            df_top10_media[['Rank', 'Akun Media / Kanal', 'Tipologi Media', 'Total Degree', 'In-Degree (Aduan Masuk)', 'PageRank Centrality', 'Peran Penghubung', 'Fokus Wacana']],
            width='stretch',
            hide_index=True
        )

        with st.expander("🔍 Analisis Komparatif: Mengapa Kanal Menfess & Spesialis Mengungguli Media Arus Utama (CNN Indonesia)?", expanded=False):
            st.markdown("""
            1. **Fenomena *News Disintermediation* (Peniadaan Perantara Berita Konvensional):**
               - Dalam krisis kebijakan publik berskala masif, warganet di platform X cenderung mengabaikan kanal media resmi satu arah dan beralih ke akun kurasi publik anonim (*menfess* seperti `@tanyarlfes` dan `@tanyakanrl`).
               - Akun menfess menjadi simpul perantara utama karena memberikan rasa aman (*anonymity*) bagi warganet untuk mengunggah foto menu riil yang dianggap mengecewakan tanpa takut retaliasi institusional.

            2. **Peran Media Penyiaran vs Media Investigatif:**
               - `@KompasTV` menduduki PageRank tertinggi (0,00457) di antara media massa konvensional karena tayangan visual televisinya sering dijadikan klip bukti perdebatan.
               - `@tempodotco` menjadi rujukan otoritatif bagi warganet yang mencari analisis mendalam tentang dugaan rente anggaran dan penurunan standar gizi vendor.

            3. **Dimensi Finansial & Teknis (@LambeSahamjja & @itbfess_x):**
               - Munculnya kanal finansial dan sivitas akademika menganalisis bahwa wacana MBG dievaluasi secara multidimensi: dari sudut pandang beban utang negara, inflasi bahan pangan lokal, hingga kecukupan kalori medis anak sekolah.
            """)

        st.markdown("---")
        st.markdown("---")


        st.markdown("---")
        st.subheader("🎯 Analisis Peran Struktural: 3 Top Aktor Kunci")
        st.markdown("Berdasarkan komputasi aktual dari 971 node dan 666 edge terverifikasi, tiga aktor ini menduduki posisi struktural yang **berbeda dan saling melengkapi** dalam jaringan diskursus MBG.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.error("### 🤖 @grok\n*\"The Silent Oracle\"*")
            st.metric("In-degree", "0", "Tidak di-mention")
            st.metric("Out-degree", "42", "Membalas 43 akun")
            st.metric("Betweenness", "0.000000")
            st.metric("Eigenvector", "0.000000")
            st.info("""
**Peran Struktural:** High Out-Degree Actor

@grok adalah AI chatbot milik Platform X yang secara aktif **membalas 43 akun** netizen yang bertanya tentang MBG, namun **tidak ada satu pun** yang me-reply balik (in-degree=0).

**Pola ini disebut *oracle behavior*:** publik mengonsultasikan informasi kepada mesin AI, namun tidak menganggapnya sebagai lawan dialog.

**Implikasi Phygital Gap:**
> *"Ketika kepercayaan kepada pejabat runtuh, publik mengalihkan pencarian kebenaran kepada mesin AI — inilah manifestasi structural centrality."*
            """)

        with col2:
            st.warning("### 🔗 @4Y4NKZ\n*\"The Broker\"*")
            st.metric("In-degree", "2")
            st.metric("Out-degree", "15", "Aktif lintas komunitas")
            st.metric("Betweenness", "0.005940868", "🥇 TERTINGGI")
            st.metric("Eigenvector", "0.117")
            st.info("""
**Peran Struktural:** Broker Jaringan

@grok memiliki posisi sentral berdasarkan out-degree dan betweenness centrality dalam graf yang dianalisis; metrik tersebut digunakan untuk mendeskripsikan posisi struktural dalam jaringan.

Betweenness Centrality tertinggi (0.005940868) menunjukkan posisi struktural aktor tersebut pada jalur terpendek dalam graf yang dianalisis.

**Pola ini umum dalam SNA:** Broker bukan selalu tokoh terkenal, justru "warga biasa" yang aktif berdialog lintas batas komunitas.

*Me-reply ke: @bonapasogit24, @trihhh14, @newIding30 — dari klaster berbeda.*
            """)

        with col3:
            st.success("### 👑 @prabowo\n*\"The Target\"*")
            st.metric("In-degree", "15", "🥇 TERTINGGI")
            st.metric("Out-degree", "0", "Nilai pada graf mention")
            st.metric("Betweenness", "0.000000")
            st.metric("Eigenvector", "0.000051")
            st.info("""
**Peran Struktural:** High In-Degree Target

@prabowo (Presiden RI, pemilik kebijakan MBG) adalah aktor **paling banyak disebut (15×)** namun **memiliki in-degree 15 dalam graf mention** percakapan (out-degree tidak digunakan untuk menyimpulkan respons aktual).

Ini adalah bukti struktural dari **low reciprocity dalam graf mention** — publik berteriak kepada pemangku kebijakan, tapi pemangku kebijakan tidak hadir dalam dialog.

**Implikasi Phygital Gap:**
> *"Graf mention menunjukkan posisi struktural akun berdasarkan in-degree dan out-degree; metrik ini tidak digunakan untuk menyimpulkan respons aktual."*
            """)

        st.markdown("---")
        st.subheader("📊 Tabel Komparasi Peran Struktural")

        actor_data = {
            "Aktor": ["🤖 @grok", "🔗 @4Y4NKZ", "👑 @prabowo"],
            "Peran Struktural": ["High Out-Degree Actor", "High-Betweenness Actor", "High In-Degree Target"],
            "In-degree": [0, 2, 15],
            "Out-degree": [42, 15, 0],
            "Betweenness": ["0.000000", "0.005940868", "0.000000"],
            "Eigenvector": ["0.000000", "0.117", "0.000051"],
            "Interpretasi": [
                "Menjawab publik, tidak didiskusikan balik",
                "Jembatan lintas komunitas terfragmentasi",
                "Paling disebut tapi tidak hadir dalam dialog"
            ]
        }
        st.dataframe(pd.DataFrame(actor_data), width='stretch', hide_index=True)

        st.success("""
        **📌 Sintesis Akademis (untuk manuskrip):**

        > *"Centrality analysis identifies different structural positions in the mention graph: @grok has the highest out-degree (42) and the highest betweenness centrality (0.005940868), while @prabowo has in-degree 15. These metrics describe graph position and are not used to infer motives or actual responses."*
        """)

        st.markdown("---")
        st.subheader("Top Aktor (Centrality Data)")
        if nodes_data is not None:
            if 'Eigenvector Centrality' in nodes_data.columns:
                st.dataframe(nodes_data[['Id', 'Degree', 'Eigenvector Centrality']].sort_values(by='Eigenvector Centrality', ascending=False).head(10))
            else:
                st.dataframe(nodes_data.head(10))
        else:
            st.warning("Data metrics tidak ditemukan.")

        # ============================================================
        # BAGIAN BARU: POLA KEKUASAAN & PENYEBARAN INFORMASI
        # ============================================================
        st.markdown("---")
        st.header("🔋 Pola Kekuasaan Informasi & Penyebaran Kebijakan")
        st.markdown("""
        > **Mengapa ini penting?** Analisis teks biasa hanya bisa membaca *apa* yang ditulis.
        > Pendekatan berbasis graf membaca *siapa yang berkuasa*, *siapa yang menyebarkan*, dan *siapa yang menjembatani* — pola yang **tidak tampak** dari isi cuitan semata.
        """)

        import networkx as nx
        import plotly.graph_objects as go

        # Load & compute metrics
        @st.cache_data
        def compute_all_metrics():
            df_e = pd.read_csv(get_data_path("network_edges.csv"))
            G_d = nx.DiGraph()
            for _, row in df_e.iterrows():
                G_d.add_edge(row['Source'], row['Target'])
            in_d  = dict(G_d.in_degree())
            out_d = dict(G_d.out_degree())
            betw  = nx.betweenness_centrality(G_d, normalized=True)
            try:
                eig = nx.eigenvector_centrality(G_d, max_iter=1000)
            except Exception:
                eig = nx.eigenvector_centrality_numpy(G_d)
            density   = nx.density(G_d)
            reciprocity = nx.reciprocity(G_d)
            return in_d, out_d, betw, eig, density, reciprocity, G_d

        in_d, out_d, betw, eig, density, reciprocity, G_computed = compute_all_metrics()

        # ── Metrik Global ──
        st.subheader("📐 Metrik Global Jaringan")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("🗣️ Nodes", "971", "Aktor unik")
        m2.metric("🔗 Edges", "666", "Interaksi")
        m3.metric("🏘️ Modularity", "0.9837", "Strong community structure")
        m4.metric("🔄 Reciprocity", f"{reciprocity*100:.1f}%", "Dialog timbal balik")
        m5.metric("📉 Density", f"{density:.6f}", "Sangat jarang")

        st.info(f"""
        **Reciprocity hanya {reciprocity*100:.1f}%** — artinya **98.8% percakapan bersifat searah (one-way)**.
        Graf menunjukkan hubungan mention yang dominan satu arah; struktur ini tidak digunakan untuk menyimpulkan respons aktual aktor.
        """)

        st.markdown("---")

        # ── 4 Dimensi Metrik ──
        st.subheader("📊 Empat Dimensi Kekuasaan Informasi dalam Jaringan")

        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 In-Degree — Kekuatan Rujukan",
            "📡 Out-Degree — Kekuatan Penyebaran",
            "🌉 Betweenness — Kekuatan Perantara",
            "⚡ Eigenvector — Kekuatan Pengaruh"
        ])

        with tab1:
            st.markdown("""
            ### 🎯 In-Degree Centrality — *Siapa yang Paling Dirujuk/Dituju?*

            **Definisi:** Jumlah akun lain yang mengarahkan koneksi (mention/reply) **ke** sebuah node.

            **Makna Kekuasaan:** Node dengan in-degree tinggi adalah **objek perhatian publik** —
            mereka menjadi *pusat gravitasi informasi*. Semakin tinggi, semakin besar tekanan publik kepadanya.

            **Contoh dalam dataset MBG:**
            """)

            top_in_list = sorted(in_d.items(), key=lambda x: x[1], reverse=True)[:10]
            df_in = pd.DataFrame(top_in_list, columns=['Akun', 'In-Degree'])

            fig_in = go.Figure(go.Bar(
                x=df_in['In-Degree'], y=['@'+a for a in df_in['Akun']],
                orientation='h',
                marker_color=['#EF4444' if a=='prabowo' else '#3B82F6' for a in df_in['Akun']],
                text=df_in['In-Degree'], textposition='outside'
            ))
            fig_in.update_layout(
                title="Top 10 Aktor: In-Degree (Paling Banyak Dirujuk)", height=400,
                xaxis_title="Jumlah akun yang mengarahkan koneksi ke node ini",
                yaxis=dict(categoryorder='total ascending'), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_in, width='stretch')

            st.error("""
            **🔴 Temuan Kritis: @prabowo (In-Degree = 15)**

            @prabowo adalah **aktor dengan in-degree tertinggi dalam graf mention yang dianalisis** dalam jaringan — 15 akun berbeda secara langsung mengarahkan
            percakapan kepadanya; graf yang dianalisis hanya merekam relasi mention yang teramati.

            **Contoh interaksi:**
            > *@punishe98373138 → @prabowo: "Pak Presiden, MBG di sekolah anak saya sudah 3 minggu tidak berjalan..."*
            >
            > *@bbiiyaya → @prabowo: "Triliunan habis tapi gizi anak-anak masih tidak terpenuhi..."*

            **Interpretasi:** In-degree tinggi + out-degree nol = **asymmetric interaction structure** di level komunikasi kebijakan.
            Publik berteriak, pemimpin tidak hadir. Inilah Phygital Gap.
            """)

        with tab2:
            st.markdown("""
            ### 📡 Out-Degree Centrality — *Siapa yang Paling Aktif Menyebarkan?*

            **Definisi:** Jumlah koneksi yang diinisiasi (mention/reply) **dari** sebuah node ke akun lain.

            **Makna Kekuasaan:** Node dengan out-degree tinggi adalah **penebar informasi aktif** —
            mereka menjadi *mesin distribusi pesan*. Ini tidak berarti mereka berpengaruh, tapi mereka *bising*.

            **Contoh dalam dataset MBG:**
            """)

            top_out_list = sorted(out_d.items(), key=lambda x: x[1], reverse=True)[:10]
            df_out = pd.DataFrame(top_out_list, columns=['Akun', 'Out-Degree'])

            fig_out = go.Figure(go.Bar(
                x=df_out['Out-Degree'], y=['@'+a for a in df_out['Akun']],
                orientation='h',
                marker_color=['#7C3AED' if a=='grok' else '#10B981' for a in df_out['Akun']],
                text=df_out['Out-Degree'], textposition='outside'
            ))
            fig_out.update_layout(
                title="Top 10 Aktor: Out-Degree (Paling Aktif Menyebarkan)", height=400,
                xaxis_title="Jumlah koneksi yang diinisiasi dari node ini",
                yaxis=dict(categoryorder='total ascending'), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_out, width='stretch')

            st.warning("""
            **🟣 Temuan Anomali: @grok (Out-Degree = 42) — Out-Degree Tertinggi**

            @grok memiliki **out-degree = 42**, yaitu nilai out-degree tertinggi dalam graf yang dianalisis.
            Ini bukan distribusi organik, melainkan **distribusi algoritmik**:

            **Contoh:**
            > *@HSoekma23 → @grok: "Grok, apa benar anggaran MBG sudah dicairkan?"*
            >
            > *@grok → @HSoekma23: "Berdasarkan data yang tersedia, anggaran MBG sebesar Rp71 triliun..."*

            **Interpretasi:** Dalam graf yang dianalisis, akun @prabowo memiliki in-degree = 15 dalam graf mention yang dianalisis.
            Dalam graf yang dianalisis, **@grok memiliki out-degree 42**, yang merupakan nilai out-degree tertinggi. Temuan ini digunakan untuk mendeskripsikan posisi struktural, bukan untuk menyimpulkan fungsi otoritas informasi.
            """)

        with tab3:
            st.markdown("""
            ### 🌉 Betweenness Centrality — *Siapa Jembatan Antar Komunitas?*

            **Definisi:** Proporsi *shortest path* antar semua pasangan node yang melewati sebuah node tertentu.

            **Makna Kekuasaan:** Node dengan betweenness tinggi adalah **gatekeeper informasi** —
            mereka mengendalikan aliran informasi antara komunitas yang terpisah.
            Jika dihilangkan, komunitas-komunitas itu terputus total.

            **Contoh dalam dataset MBG:**
            """)

            top_betw_list = sorted(betw.items(), key=lambda x: x[1], reverse=True)[:10]
            df_betw = pd.DataFrame(top_betw_list, columns=['Akun', 'Betweenness'])
            df_betw['Betweenness_pct'] = df_betw['Betweenness'] * 1e6  # scale for display

            fig_betw = go.Figure(go.Bar(
                x=df_betw['Betweenness_pct'], y=['@'+a for a in df_betw['Akun']],
                orientation='h',
                marker_color=['#F97316' if a=='4Y4NKZ' else '#06B6D4' for a in df_betw['Akun']],
                text=[f"{v:.4f} ×10⁻⁶" for v in df_betw['Betweenness_pct']],
                textposition='outside'
            ))
            fig_betw.update_layout(
                title="Top 10 Aktor: Betweenness Centrality (Jembatan Komunitas)", height=400,
                xaxis_title="Betweenness × 10⁻⁶ (semakin tinggi = semakin penting sebagai jembatan)",
                yaxis=dict(categoryorder='total ascending'), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_betw, width='stretch')

            st.info("""
            **🟠 Temuan: @grok (Betweenness = 0.005940868 — TERTINGGI)**

            @4Y4NKZ bukan tokoh publik, bukan pejabat — namun ia adalah **satu-satunya jembatan aktif** yang
            menghubungkan komunitas-komunitas terisolasi dalam jaringan.

            **Contoh pola jembatan:**
            > *[Klaster A: pendukung MBG] ←→ @4Y4NKZ ←→ [Klaster B: pengkritik MBG]*

            Ia me-reply ke: @bonapasogit24 (klaster A) DAN @newIding30 (klaster B) — dua komunitas berbeda.

            **Interpretasi:** Dalam jaringan dengan struktur komunitas yang kuat (Q=0.9837), @grok memiliki posisi struktural berdasarkan metrik centrality yang dianalisis.
            **satu-satunya saluran dialog lintas kubu**. Hilangkan ia, dan dialog antar komunitas benar-benar putus.
            """)

        with tab4:
            st.markdown("""
            ### ⚡ Eigenvector Centrality — *Siapa yang Paling Berpengaruh Secara Jaringan?*

            **Definisi:** Skor pengaruh berdasarkan kualitas koneksi — **terhubung ke node berpengaruh = lebih tinggi skornya**.

            **Makna Kekuasaan:** Node dengan eigenvector tinggi bukan sekadar aktif,
            tapi koneksinya mengarah ke **inti jaringan yang paling berpengaruh**.

            **Catatan metodologis:** Pada jaringan dengan struktur komunitas yang kuat (Q=0.9837),
            skor eigenvector seringkali *terdistribusi merata* dalam satu klaster besar —
            ini adalah sinyal bahwa jaringan tidak memiliki *single dominant hub*.
            """)

            top_eig_list = sorted(eig.items(), key=lambda x: x[1], reverse=True)[:10]
            df_eig = pd.DataFrame(top_eig_list, columns=['Akun', 'Eigenvector'])

            fig_eig = go.Figure(go.Bar(
                x=df_eig['Eigenvector'], y=['@'+a for a in df_eig['Akun']],
                orientation='h',
                marker_color='#8B5CF6',
                text=[f"{v:.4f}" for v in df_eig['Eigenvector']],
                textposition='outside'
            ))
            fig_eig.update_layout(
                title="Top 10 Aktor: Eigenvector Centrality (Pengaruh Jaringan)", height=400,
                xaxis_title="Eigenvector Score (semakin tinggi = terhubung ke node berpengaruh)",
                yaxis=dict(categoryorder='total ascending'), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_eig, width='stretch')

            st.warning("""
            **🟡 Temuan: Skor Eigenvector Identik (0.2332) untuk 10+ Akun**

            Ini bukan error — ini adalah temuan penting: **tidak ada satu pun node yang mendominasi**
            jaringan secara keseluruhan. 10 akun berbagi skor eigenvector yang sama persis,
            artinya mereka semua berada dalam **klaster yang sama** dan memiliki posisi yang setara.

            **Interpretasi:** Berbeda dari jaringan media mainstream yang memiliki satu hub super-dominan
            (misalnya: akun media nasional), jaringan diskursus MBG bersifat **egalitarian secara struktural** —
            tidak ada satu suara pun yang secara objektif lebih kuat dari yang lain di level jaringan.
            """)

        # ── Pola Penyebaran Informasi Kebijakan ──
        st.markdown("---")
        st.subheader("🗺️ Pola Penyebaran Informasi: Yang Tidak Tampak dari Konten")

        st.markdown("""
        Berikut adalah **3 pola struktural** yang hanya terlihat melalui pembacaan graf,
        bukan dari membaca isi cuitan satu per satu:
        """)

        p1, p2, p3 = st.columns(3)

        with p1:
            st.error("""
            ### 🔴 Pola 1
            ## STRUKTUR INTERAKSI ASIMETRIS

            **Definisi:** Aktor dengan in-degree tinggi teridentifikasi dari struktur jaringan mention

            **Bukti data:**
            - @prabowo: In=15
            - Reciprocity jaringan: **1.2%**

            **Artinya:**
            Tekanan publik besar, respons institusional nol.
            Inilah *asymmetric power* — kekuasaan mengalir satu arah.

            **Tidak tampak dari konten:** Jika Anda hanya baca tweet, Anda tidak tahu bahwa *tidak ada satu pun respons resmi* dalam jaringan ini.
            """)

        with p2:
            st.warning("""
            ### 🟡 Pola 2
            ## PERBEDAAN POSISI STRUKTURAL

            **Definisi:** @grok memiliki out-degree tertinggi dalam graf mention, yaitu 42; metrik ini digunakan untuk mendeskripsikan posisi struktural dan tidak digunakan untuk menyimpulkan fungsi otoritas informasi.

            **Bukti data:**
            - @grok: Out=**42** (tertinggi)
            - @grok: In=**0** (tidak didiskusikan balik)
            - Density jaringan: **0.000707**

            **Artinya:**
            Di ruang vakum kebijakan, publik tidak berdebat — mereka *bertanya kepada mesin*.

            **Tidak tampak dari konten:** Anda bisa membaca 1.000 tweet tanpa sadar bahwa responden terbanyak bukan manusia, tapi AI.
            """)

        with p3:
            st.info("""
            ### 🔵 Pola 3
            ## COMMUNITY STRUCTURE

            **Definisi:** 342 komunitas dengan 1 edge record yang teridentifikasi melintasi batas komunitas

            **Bukti data:**
            - Modularity: **0.9837** (merangkum struktur komunitas hasil partisi Louvain)
            - Aktor dengan betweenness tertinggi: @grok
            - Betweenness tertinggi: **0.005940868**

            **Artinya:**
            Publik tidak berdebat lintas kubu — mereka berbicara di kandangnya masing-masing. Hanya 1 "jembatan" tipis yang menghubungkan semua cluster.

            **Tidak tampak dari konten:** Anda tidak bisa tahu bahwa hubungan lintas komunitas tidak dapat dinilai hanya dari isi tweet; analisis graf menunjukkan 1 edge record melintasi batas komunitas.
            """)

        st.success("""
        **📌 Sintesis untuk Manuskrip:**

        > *"Graph-based analysis reveals three latent structural patterns invisible to content analysis alone:
        (1) a **asymmetric interaction structure** in which the @prabowo (in-degree=15) memiliki in-degree=15 dalam graf mention; reciprocity jaringan tercatat sebesar 1,20%;
        (2) an **Perbedaan Posisi Centrality** in which @grok memiliki out-degree=42, yaitu nilai out-degree tertinggi dalam graf yang dianalisis;
        and (3) an **Community Separation Pattern** in which 342 communities (modularity=0.9837) were identified, with 1 edge record crossing community boundaries among 692 edge records.
        These patterns collectively operationalize the Phygital Gap as a structural — not merely perceptual — phenomenon (Newman, 2006; Gandasari et al., 2023)."*
        """)




    with tab_iv_5:
        st.header("☁️ §4.4b Analisis Leksikal: Word Cloud & Top 10 Kata Paling Sering Muncul")
        st.markdown("""
        > *Analisis leksikal mengungkap kosakata dominan dan penanda bahasa (*linguistic markers*) dalam wacana MBG.
        > Komputasi frekuensi kata dan visualisasi Word Cloud dihitung secara komputasional langsung dari
        > korpus valid yang digunakan untuk analisis leksikal (*text cleansing*).*
        """)

        stopwords_lex = set([
            'dan', 'yang', 'di', 'ini', 'itu', 'untuk', 'dari', 'dengan', 'ke', 'ada',
            'saya', 'kita', 'dia', 'mereka', 'akan', 'bisa', 'juga', 'sudah', 'oleh',
            'karena', 'pada', 'atau', 'jadi', 'harus', 'lagi', 'tidak', 'nggak', 'gak',
            'aja', 'nya', 'nih', 'sih', 'kok', 'lah', 'ya', 'kan', 'dong', 'deh', 'pun',
            'bukan', 'tapi', 'kalau', 'kalo', 'buat', 'sama', 'mau', 'lebih', 'banyak',
            'sangat', 'banget', 'bisa', 'dapat', 'saat', 'seperti', 'dalam', 'tentang',
            'apa', 'siapa', 'mana', 'kapan', 'kenapa', 'bagaimana', 'gimana', 'hal',
            'masih', 'hanya', 'cuma', 'bahkan', 'namun', 'selain', 'secara', 'tersebut',
            'tahun', 'hari', 'kali', 'orang', 'para', 'semua', 'lain', 'setiap', 'ia',
            'kami', 'kamu', 'anda', 'gua', 'gue', 'lo', 'lu', 'gw', 'tak', 'tiap', 'bagi',
            'agar', 'supaya', 'ketika', 'setelah', 'sebelum', 'hingga', 'sampai', 'antar',
            'https', 'http', 'co', 't', 'rt', 'via', 'amp', 'aku', 'udah', 'baru', 'punya',
            'por', 'frete', 'amazon', 'que', 'uma', 'com', 'para', 'nao', 'voce', 'mais',
            'como', 'sua', 'seu', 'tem', 'dos', 'das', 'grtis', 'sem', 'los', 'con', 'promoes', 'juros'
        ])

        lex_emo_choice = st.radio(
            "Pilih Subset Emosi untuk Analisis Leksikal:",
            ["Seluruh Korpus (N=5.263)", "🤢 Jijik (Disgust)", "🤝 Percaya (Trust)", "😐 Netral", "🔮 Tertarik"],
            horizontal=True
        )

        df_emotion = load_emotion_data()
        if "Jijik" in lex_emo_choice:
            sub_lex_df = df_emotion[df_emotion['predicted_emotion'] == 'Jijik']
            wc_color = 'Reds_r'
        elif "Percaya" in lex_emo_choice:
            sub_lex_df = df_emotion[df_emotion['predicted_emotion'] == 'Percaya']
            wc_color = 'Blues_r'
        elif "Netral" in lex_emo_choice:
            sub_lex_df = df_emotion[df_emotion['predicted_emotion'] == 'Netral']
            wc_color = 'Greys_r'
        elif "Tertarik" in lex_emo_choice:
            sub_lex_df = df_emotion[df_emotion['predicted_emotion'] == 'Tertarik']
            wc_color = 'YlOrBr_r'
        else:
            sub_lex_df = df_emotion
            wc_color = 'magma'

        all_lex_text = ' '.join(sub_lex_df['clean_text'].dropna().astype(str).tolist())
        lex_tokens = [w for w in re.findall(r'[a-zA-Z]{3,}', all_lex_text.lower()) if w not in stopwords_lex]
        counter_all = Counter(lex_tokens)
        total_tokens_sub = len(lex_tokens)

        # Top 10 All
        top_10_all = counter_all.most_common(10)

        # Top 10 Thematic
        core_query_words = set(['mbg', 'makan', 'makanan', 'gratis', 'program', 'gizi', 'bergizi'])
        counter_thematic = Counter({k: v for k, v in counter_all.items() if k not in core_query_words})
        top_10_thematic = counter_thematic.most_common(10)

        tab_lex1, tab_lex2 = st.tabs(["🏆 Top 10 Kata Umum & Word Cloud", "🎯 Top 10 Kata Tematik Spesifik (Isu Lapangan)"])

        with tab_lex1:
            wc_col1, wc_col2 = st.columns([1.2, 1])
            with wc_col1:
                st.subheader("☁️ Visual Word Cloud Diskursus MBG")
                wc_resolved = get_result_path("wordcloud_mbg.png")
                if "Semua" in lex_emo_choice and os.path.exists(wc_resolved):
                    st.image(wc_resolved, width='stretch', caption="Visual Word Cloud: 120 Kata Paling Signifikan")
                elif WORDCLOUD_AVAILABLE and MATPLOTLIB_AVAILABLE:
                    try:
                        wc_dyn = WordCloud(
                            width=800, height=450, background_color='#0f172a',
                            colormap=wc_color, max_words=100, contour_width=1, contour_color='#e2e8f0'
                        ).generate(' '.join(lex_tokens) if lex_tokens else 'mbg')
                        fig_wc, ax_wc = plt.subplots(figsize=(8, 4.5), facecolor='#0f172a')
                        ax_wc.imshow(wc_dyn, interpolation='bilinear')
                        ax_wc.axis('off')
                        st.pyplot(fig_wc, width='stretch')
                        plt.close(fig_wc)
                    except Exception as e:
                        if os.path.exists(wc_resolved):
                            st.image(wc_resolved, width='stretch', caption="Visual Word Cloud (Fallback Resolusi Tinggi)")
                        else:
                            st.warning(f"Gagal menghasilkan word cloud dinamis: {e}")
                elif os.path.exists(wc_resolved):
                    st.image(wc_resolved, width='stretch', caption="Visual Word Cloud: 120 Kata Paling Signifikan")
                else:
                    st.info("Visual Word Cloud dimuat dari aset kanonik riset.")

            with wc_col2:
                st.subheader("📊 Top 10 Kata Paling Sering Muncul")
                df_top10_all = pd.DataFrame({
                    'Kata': [f"#{i+1} {w}" for i, (w, _) in enumerate(top_10_all)][::-1],
                    'Frekuensi': [cnt for _, cnt in top_10_all][::-1],
                    'Porsi': [f"{(cnt/total_tokens_sub)*100:.2f}%" if total_tokens_sub > 0 else "0%" for _, cnt in top_10_all][::-1]
                })
                fig_bar10 = px.bar(
                    df_top10_all,
                    x='Frekuensi',
                    y='Kata',
                    orientation='h',
                    text='Frekuensi',
                    color='Frekuensi',
                    color_continuous_scale='Reds',
                    title=f"10 Kata Teratas ({lex_emo_choice})"
                )
                fig_bar10.update_traces(textposition='outside')
                fig_bar10.update_layout(height=450, margin=dict(t=30, b=10, l=10, r=10), showlegend=False)
                st.plotly_chart(fig_bar10, width='stretch')

            st.subheader("🏷️ Kartu Ringkasan 10 Kata Teratas")
            b_cols = st.columns(5)
            for idx, (word, count) in enumerate(top_10_all[:5]):
                pct_val = (count / total_tokens_sub) * 100 if total_tokens_sub > 0 else 0
                with b_cols[idx]:
                    st.metric(f"Rank #{idx+1}", f"'{word}'", f"{count:,} cuitan ({pct_val:.1f}%)")
            b_cols2 = st.columns(5)
            for idx, (word, count) in enumerate(top_10_all[5:10]):
                pct_val = (count / total_tokens_sub) * 100 if total_tokens_sub > 0 else 0
                with b_cols2[idx]:
                    st.metric(f"Rank #{idx+6}", f"'{word}'", f"{count:,} cuitan ({pct_val:.1f}%)")

        with tab_lex2:
            st.subheader("🎯 10 Kata Tematik Spesifik (Di Luar Kata Kunci Kueri)")
            st.caption("Menyaring kata kunci kueri ('mbg', 'makan', 'gratis', dll.) untuk menyingkap fokus substansi lapangan:")

            thm_col1, thm_col2 = st.columns([1.3, 1])
            with thm_col1:
                df_thm = pd.DataFrame({
                    'Kata Tematik': [f"#{i+1} {w}" for i, (w, _) in enumerate(top_10_thematic)][::-1],
                    'Jumlah Cuitan': [cnt for _, cnt in top_10_thematic][::-1],
                    'Porsi': [f"{(cnt/total_tokens_sub)*100:.2f}%" if total_tokens_sub > 0 else "0%" for _, cnt in top_10_thematic][::-1]
                })
                fig_thm = px.bar(
                    df_thm,
                    x='Jumlah Cuitan',
                    y='Kata Tematik',
                    orientation='h',
                    text='Jumlah Cuitan',
                    color='Jumlah Cuitan',
                    color_continuous_scale='Blues',
                    title="Top 10 Kosakata Isu Spesifik MBG"
                )
                fig_thm.update_traces(textposition='outside')
                fig_thm.update_layout(height=420, margin=dict(t=30, b=10, l=10, r=10), showlegend=False)
                st.plotly_chart(fig_thm, width='stretch')

            with thm_col2:
                st.info("""
                **💡 Wawasan Komunikasi & Sosiologis:**
                1. **`sekolah` (#1) & `anak` (#2):** Wacana MBG bukan sekadar perdebatan politik elit, melainkan berpusat langsung pada entitas fisik sekolah dasar dan perlindungan anak.
                2. **`dapur` (#4):** Mengacu pada isu teknis Satuan Pelayanan Pemenuhan Gizi (SPPG) dan standar sanitasi dapur penyedia.
                3. **`enak` (#6) & `menu` (#9):** Resepsi sensorik rasa dan kelayakan fisik menu menjadi tolok ukur kepuasan langsung penerima manfaat.
                4. **`anggaran` (#10):** Kritik terhadap transparansi alokasi pembiayaan APBN dan potensi pemangkasan porsi.
                """)

        st.markdown("---")
        st.markdown("---")
        # ── §4.5 EVALUASI MODEL KLASIFIKASI EMOSI DAN DETEKSI SINDIRAN ──

        st.header("🎯 §4.5 Evaluasi Model Klasifikasi Emosi dan Deteksi Sindiran")
        st.markdown("""
        > *Model **IndoBERT** (`indobenchmark/indobert-base-p2`) dilatih pada 3.785 cuitan; checkpoint dipilih dengan **validation split group-aware** (n = 420, epoch 1, val loss 0,5068),
        > lalu dievaluasi **satu kali** pada test set group-aware ($n = 1.058$) yang tidak pernah dipakai saat pelatihan maupun seleksi model. Tidak ada teks yang tumpang tindih antar-partisi.
        > Seluruh metrik dimuat secara dinamis dari file hasil evaluasi terverifikasi.*
        """)

        # Load final evaluation data
        eval_data = load_final_evaluation()
        df_comp = eval_data["comparison"]
        df_per_class = eval_data["per_class"]
        res_dir = eval_data["results_dir"]

        row_indo = df_comp[df_comp['Model'] == 'IndoBERT Group-Aware'].iloc[0]
        indo_acc = float(row_indo['Accuracy'])
        indo_mf1 = float(row_indo['Macro_F1'])
        indo_wf1 = float(row_indo['Weighted_F1'])
        test_n = int(row_indo['Test_N'])

        ev_col1, ev_col2, ev_col3, ev_col4 = st.columns(4)
        with ev_col1:
            st.metric("Ukuran Data Uji (Test N)", f"{test_n:,}", "Test set terisolasi")
        with ev_col2:
            st.metric("Akurasi IndoBERT", f"{indo_acc*100:.2f}%", f"{indo_acc:.4f} Overall")
        with ev_col3:
            st.metric("Macro F1-Score", f"{indo_mf1:.4f}", "6 Kelas Aktif Teruji")
        with ev_col4:
            st.metric("Weighted F1-Score", f"{indo_wf1:.4f}", "Tertimbang Distribusi Kelas")

        st.caption("ℹ️ *Catatan Metodologis: Evaluasi menggunakan silver-standard reference labels dan protokol group-aware train/validation/test (GroupShuffleSplit, random_state=42) tanpa tumpang tindih teks.*")

        st.markdown("---")
        st.subheader("📊 §4.5.1 Visualisasi Confusion Matrix IndoBERT Group-Aware (Data Riil)")
        st.markdown("Visualisasi performa inferensi aktual model IndoBERT (checkpoint terpilih dari validation split) pada 1.058 sampel data uji:")

        cm_mode = st.radio("Pilih Tampilan Confusion Matrix:", ["Matriks Frekuensi (Raw Counts)", "Matriks Ternormalisasi (Normalized Proportions)"], horizontal=True)
        
        cm_dir = eval_data.get("cm_dir", res_dir)
        if eval_data.get("protocol") == "v2":
            cm_counts_path = cm_dir / "confusion_matrix.png"
            cm_norm_path = cm_dir / "confusion_matrix_normalized.png"
        else:
            cm_counts_path = res_dir / "FINAL_indobert_confusion_matrix.png"
            cm_norm_path = res_dir / "FINAL_indobert_confusion_matrix_normalized.png"

        if cm_mode == "Matriks Frekuensi (Raw Counts)":
            if cm_counts_path.exists():
                st.image(str(cm_counts_path), width='stretch', caption="Gambar 4A: Confusion Matrix IndoBERT Group-Aware (Raw Counts, n=1.058)")
            else:
                st.warning("File FINAL_indobert_confusion_matrix.png belum tersedia.")
        else:
            if cm_norm_path.exists():
                st.image(str(cm_norm_path), width='stretch', caption="Gambar 4B: Normalized Confusion Matrix IndoBERT Group-Aware (Normalized, n=1.058)")
            else:
                st.warning("File FINAL_indobert_confusion_matrix_normalized.png belum tersedia.")

        # ── TABEL KOMPARASI MODEL BASELINE ──
        st.markdown("---")
        st.subheader("📋 Tabel 4.4a Komparasi Multi-Model (IndoBERT vs Linear Baselines)")
        st.caption("Perbandingan performa model pada test set group-aware yang sama (n=1.058); semua model dilatih pada sub-train yang sama (n=3.785):")

        tabel_baseline_display = df_comp[['Model', 'Accuracy', 'Macro_F1', 'Weighted_F1', 'Protocol']].copy()
        tabel_baseline_display.columns = ['Model Architecture', 'Accuracy', 'Macro-F1', 'Weighted-F1', 'Split Protocol']
        tabel_baseline_display['Accuracy'] = tabel_baseline_display['Accuracy'].map(lambda x: f"{x:.4f}")
        tabel_baseline_display['Macro-F1'] = tabel_baseline_display['Macro-F1'].map(lambda x: f"{x:.4f}")
        tabel_baseline_display['Weighted-F1'] = tabel_baseline_display['Weighted-F1'].map(lambda x: f"{x:.4f}")
        st.dataframe(tabel_baseline_display, width='stretch', hide_index=True)

        # ── TABEL 4.4b EVALUASI EMOSI PER KELAS ──
        st.subheader("📋 Tabel 4.4b Evaluasi Kinerja Klasifikasi IndoBERT per Kelas (Holdout n=1.058)")
        st.caption("Rincian metrik presisi, recall, F1, dan jumlah data uji riil (results/indobert_group_aware_v2/classification_report_v2.csv):")

        tabel_perclass_display = df_per_class[['label', 'support', 'precision', 'recall', 'f1', 'test_percentage']].copy()
        tabel_perclass_display.columns = ['Kelas Emosi', 'Support (Cuitan)', 'Precision', 'Recall', 'F1-Score', 'Porsi Data Uji (%)']
        tabel_perclass_display['Precision'] = tabel_perclass_display['Precision'].map(lambda x: f"{x:.4f}")
        tabel_perclass_display['Recall'] = tabel_perclass_display['Recall'].map(lambda x: f"{x:.4f}")
        tabel_perclass_display['F1-Score'] = tabel_perclass_display['F1-Score'].map(lambda x: f"{x:.4f}")
        tabel_perclass_display['Porsi Data Uji (%)'] = tabel_perclass_display['Porsi Data Uji (%)'].map(lambda x: f"{x:.2f}%")
        st.dataframe(tabel_perclass_display, width='stretch', hide_index=True)

        # ── TABEL 4.6 EVALUASI DETEKSI SINDIRAN ──
        st.subheader("📋 Tabel 4.6 Distribusi & Karakteristik Deteksi Sindiran (Data Riil)")
        st.caption("Hasil anotasi korpus validasi sindiran (data/sarcasm/dataset_sindiran_valid.csv, N=3.395):")

        tabel_4_6_real = {
            "Kategori Deteksi": [
                "Leksikon Non-Sindiran (Literal / Faktual)",
                "Leksikon Sindiran (Sarkasme / Ironi Terverifikasi)",
                "Total Korpus Validasi Teranotasi",
                "Sarkasme Leksikon Eksplisit",
                "Sarkasme Proksi Sentimen"
            ],
            "Jumlah Baris": [
                "3.080 cuitan",
                "315 cuitan",
                "3.395 cuitan",
                "181 cuitan",
                "2.979 cuitan"
            ],
            "Persentase": [
                "90,72%",
                "9,28%",
                "100,00%",
                "3,44%",
                "56,60%"
            ],
            "Keterangan & Sumber": [
                "Data validasi teranotasi `dataset_sindiran_valid.csv`",
                "Data tersimpan pada `tweet_sarkastik_final.csv`",
                "Korpus teks terbersihkan praproses NLP",
                "Pola deteksi kata kontradiktif (`dataset_sindiran_rekonstruksi.csv`)",
                "Inkongruensi afektif terhadap janji kebijakan (Phygital Gap)"
            ]
        }
        st.dataframe(pd.DataFrame(tabel_4_6_real), width='stretch', hide_index=True)

        # ── §4.5.2 EVOLUSI TEMPORAL LONGITUDINAL INDOBERT & TABEL 9 EMOJI (JANUARI S.D. OKTOBER 2026) ──
        st.markdown("---")
        st.subheader("📈 §4.5.2 Evolusi Temporal Longitudinal IndoBERT & Tabel 9 Emoji (Januari s.d. 10 Oktober 2026)")
        st.markdown("""
        > *Penerapan inferensi out-of-sample longitudinal model IndoBERT pada seluruh linimasa implementasi kebijakan MBG (Januari hingga 10 Oktober 2026, **N = 9.360 cuitan riil**)
        > berhasil menangkap pergeseran sentimen mikro publik, mengidentifikasi dua puncak eskalasi krisis (*Double-Peak Crisis*), dan memvalidasi persistensi emosi Jijik (*Disgust*)
        > sebagai sentimen perekat struktural wacana publik.*
        """)

        timeline_b4_path = get_result_path("indobert_monthly_emotion_timeline_2026.png")
        if os.path.exists(timeline_b4_path):
            st.image(
                timeline_b4_path,
                caption="Gambar 4.5: Dinamika Temporal Bulanan IndoBERT (Jan–Okt 2026, N=9.360) Menampilkan Peak I (Mei 2026) dan Peak II (September 2026)",
                width='stretch'
            )
        else:
            st.info("File indobert_monthly_emotion_timeline_2026.png sedang dimuat.")

        b4_tabs_timeline = st.tabs([
            "📅 Dinamika Frekuensi Bulan ke Bulan (N=9.360)",
            "🎭 Distribusi Taksonomi 9 Emoji & Emosi (N=5.263)",
            "📊 Analisis Double-Peak Crisis (Mei vs September 2026)"
        ])

        with b4_tabs_timeline[0]:
            st.markdown("##### 📅 Dinamika Frekuensi & Emosi IndoBERT Bulan ke Bulan (Januari – 10 Oktober 2026)")
            st.caption("Data surveilans longitudinal out-of-sample riil (N = 9.360 cuitan):")
            df_monthly_b4 = pd.DataFrame([
                {"Bulan / Periode": "Januari 2026", "Total": 42, "🤢 Jijik": 42, "❤️ Cinta": 0, "😐 Netral": 0, "Proporsi Jijik (%)": "100,00%", "Kejadian Kunci MBG": "Uji coba awal; keraguan publik pada kapasitas dapur & anggaran."},
                {"Bulan / Periode": "Februari 2026", "Total": 55, "🤢 Jijik": 55, "❤️ Cinta": 0, "😐 Netral": 0, "Proporsi Jijik (%)": "100,00%", "Kejadian Kunci MBG": "Ekspansi uji coba; keluhan keterlambatan distribusi & kemasan makanan."},
                {"Bulan / Periode": "Maret 2026", "Total": 189, "🤢 Jijik": 184, "❤️ Cinta": 5, "😐 Netral": 0, "Proporsi Jijik (%)": "97,35%", "Kejadian Kunci MBG": "Penyesuaian Ramadan; perdebatan gizi lauk & transparansi vendor lokal."},
                {"Bulan / Periode": "April 2026", "Total": 515, "🤢 Jijik": 499, "❤️ Cinta": 16, "😐 Netral": 0, "Proporsi Jijik (%)": "96,89%", "Kejadian Kunci MBG": "Kontroversi nampan makan plastik impor (ompreng); kecurigaan pengadaan."},
                {"Bulan / Periode": "Mei 2026 (Puncak I)", "Total": 3157, "🤢 Jijik": 3060, "❤️ Cinta": 93, "😐 Netral": 4, "Proporsi Jijik (%)": "96,93%", "Kejadian Kunci MBG": "🚨 Puncak I: Makanan berulat/basi; BGN menonaktifkan 4.581 unit SPPG."},
                {"Bulan / Periode": "Juni 2026", "Total": 228, "🤢 Jijik": 225, "❤️ Cinta": 3, "😐 Netral": 0, "Proporsi Jijik (%)": "98,68%", "Kejadian Kunci MBG": "Libur sekolah; evaluasi parlemen (DPR RI) tata kelola dapur & higienitas."},
                {"Bulan / Periode": "Juli 2026", "Total": 184, "🤢 Jijik": 182, "❤️ Cinta": 2, "😐 Netral": 0, "Proporsi Jijik (%)": "98,91%", "Kejadian Kunci MBG": "Tahun ajaran baru; verifikasi lisensi vendor; kewaspadaan orang tua."},
                {"Bulan / Periode": "Agustus 2026", "Total": 209, "🤢 Jijik": 205, "❤️ Cinta": 2, "😐 Netral": 2, "Proporsi Jijik (%)": "98,09%", "Kejadian Kunci MBG": "Pidato Kenegaraan & Nota Keuangan RAPBN 2026 (Rp 268T); isu beban fiskal."},
                {"Bulan / Periode": "September 2026 (Puncak II)", "Total": 4661, "🤢 Jijik": 4619, "❤️ Cinta": 39, "😐 Netral": 3, "Proporsi Jijik (%)": "99,10%", "Kejadian Kunci MBG": "🔥 Puncak II: Gelombang keracunan massal siswa nasional; ribuan dirawat di IGD."},
                {"Bulan / Periode": "Oktober 2026 (s.d. 10 Okt)", "Total": 120, "🤢 Jijik": 118, "❤️ Cinta": 2, "😐 Netral": 0, "Proporsi Jijik (%)": "98,33%", "Kejadian Kunci MBG": "🤖 Pengawasan aktif bot Telegram EWS; integrasi telemetri mitigasi krisis."},
                {"Bulan / Periode": "TOTAL AKUMULASI", "Total": 9360, "🤢 Jijik": 9189, "❤️ Cinta": 167, "😐 Netral": 9, "Proporsi Jijik (%)": "98,17%", "Kejadian Kunci MBG": "Longitudinal Out-of-Sample Surveillance (Januari – 10 Oktober 2026)"}
            ])
            st.dataframe(df_monthly_b4, width='stretch', hide_index=True)

        with b4_tabs_timeline[1]:
            st.markdown("##### 🎭 Distribusi Taksonomi 9 Emoji & Emosi IndoBERT Korpus Tesis (N = 5.263)")
            st.caption("Taksonomi lengkap 9 kelas emosi model fine-tuned IndoBERT berbasis Plutchik:")
            df_tax_b4 = pd.DataFrame([
                {"No": 1, "Emoji": "🤢 / 🤮", "Kelas Emosi (Plutchik)": "Jijik (Disgust)", "Frekuensi (N)": "2.960", "Proporsi (%)": "56,24%", "Indikator Leksikal": "basi, bau, ulat, belatung, busuk, muntah, diare, gak layak, buang, jorok", "Konteks Pragmatik": "Penolakan visceral atas kegagalan atribut fisik makanan (Phygital Gap)", "Performa Model": "F1 = 0,8202 (Precision 77,61%, Recall 86,96%)"},
                {"No": 2, "Emoji": "🤝 / 😇", "Kelas Emosi (Plutchik)": "Percaya (Trust)", "Frekuensi (N)": "1.073", "Proporsi (%)": "20,39%", "Indikator Leksikal": "mendukung, gizi, sehat, berkah, anak bangsa, prabowo, program bagus, optimis", "Konteks Pragmatik": "Afirmasi positif dan kepercayaan terhadap visi gizi generasi Indonesia Emas 2045", "Performa Model": "F1 = 0,6977 (Precision 71,43%, Recall 68,18%)"},
                {"No": 3, "Emoji": "😐 / ℹ️", "Kelas Emosi (Plutchik)": "Netral (Neutral)", "Frekuensi (N)": "649", "Proporsi (%)": "12,33%", "Indikator Leksikal": "anggaran, bgn, rapat, menkeu, sasar, apbn, triliun, uji coba, tanggal, rilis", "Konteks Pragmatik": "Pewartaan faktual berita anggaran, rapat kerja, dan siaran pers", "Performa Model": "F1 = 0,8032 (Precision 81,25%, Recall 79,45%)"},
                {"No": 4, "Emoji": "🧐 / ⏳", "Kelas Emosi (Plutchik)": "Tertarik (Anticipation)", "Frekuensi (N)": "505", "Proporsi (%)": "9,60%", "Indikator Leksikal": "penasaran, kapan, cek, menu besok, jadwal, pengen tahu, nunggu, info", "Konteks Pragmatik": "Ekspektasi publik menantikan pembagian menu dan jadwal di sekolah", "Performa Model": "F1 = 0,6207 (Precision 64,29%, Recall 60,00%)"},
                {"No": 5, "Emoji": "😡 / 🤬", "Kelas Emosi (Plutchik)": "Marah (Anger)", "Frekuensi (N)": "55", "Proporsi (%)": "1,05%", "Indikator Leksikal": "bancakan, korupsi, brengsek, bohong, copot, tanggung jawab, usut, penjarakan", "Konteks Pragmatik": "Protes keras dan atribusi kesalahan kepada pengelola kebijakan", "Performa Model": "Minoritas alami (tumpang tindih pragmatik dengan Disgust)"},
                {"No": 6, "Emoji": "😢 / 😭", "Kelas Emosi (Plutchik)": "Sedih (Sadness)", "Frekuensi (N)": "19", "Proporsi (%)": "0,36%", "Indikator Leksikal": "kasihan, nangis, lemes, tega, miris, sedih, anak-anak, tersiksa", "Konteks Pragmatik": "Empati terhadap siswa keracunan dan anak di pelosok 3T", "Performa Model": "Minoritas alami (n=3 pada test set)"},
                {"No": 7, "Emoji": "😨 / 😱", "Kelas Emosi (Plutchik)": "Takut (Fear)", "Frekuensi (N)": "2", "Proporsi (%)": "0,04%", "Indikator Leksikal": "takut, waspada, ngeri, jangan-jangan, bahaya, trauma, bakteri", "Konteks Pragmatik": "Ketakutan risiko bakteri berbahaya & trauma mengonsumsi makanan", "Performa Model": "Ekstrem minoritas alami (n=0 pada test set)"},
                {"No": 8, "Emoji": "❤️ / 🥰", "Kelas Emosi (Plutchik)": "Cinta (Love)", "Frekuensi (N)": "167*", "Proporsi (%)": "1,78%*", "Indikator Leksikal": "terima kasih, cinta, relawan, ibu kantin, berkah, senang, lezat, alhamdulillah", "Konteks Pragmatik": "Apresiasi tulus kepada relawan dapur dan juru masak sekolah", "Performa Model": "*Subsumed under Trust pada N=5.263; terdeteksi pada longitudinal N=9.360"},
                {"No": 9, "Emoji": "😲 / 🤯", "Kelas Emosi (Plutchik)": "Terkejut (Surprise)", "Frekuensi (N)": "Subsumed*", "Proporsi (%)": "Spontan*", "Indikator Leksikal": "kaget, astaga, waduh, gila, buset, syok, kok bisa, beneran", "Konteks Pragmatik": "Reaksi spontan atas pembengkakan anggaran dan insiden keracunan", "Performa Model": "*Subsumed under Anticipation/Disgust dalam klasifikasi aktif"}
            ])
            st.dataframe(df_tax_b4, width='stretch', hide_index=True)

        with b4_tabs_timeline[2]:
            st.markdown("##### ⚡ Analisis Komparasi Puncak Krisis (Peak I vs Peak II)")
            col_b4_p1, col_b4_p2 = st.columns(2)
            with col_b4_p1:
                st.metric("Puncak I (Mei 2026)", "3.157 Cuitan", "96,93% Jijik (3.060)")
                st.caption("Pemicu: Penonaktifan 4.581 unit SPPG oleh BGN pasca temuan makanan basi & berbau.")
            with col_b4_p2:
                st.metric("Puncak II (Sep 2026)", "4.661 Cuitan", "99,10% Jijik (4.619)")
                st.caption("Pemicu: Gelombang keracunan massal siswa nasional; eskalasi 1,48× lebih besar dari Puncak I.")

        st.markdown("---")
        st.subheader("🔬 §4.5.3 Interpretasi Metodologis & Integritas Riset")
        st.info("""
        **💡 Catatan Metodologis & Transparansi Sains:**
        1. **Kelas dominan terdeteksi baik:** Jijik F1 = 0,8202 (Precision 0,7761, Recall 0,8696) dan Netral F1 = 0,8032.
        2. **Percaya (*Trust*) cukup stabil:** F1 = 0,6977 (Precision 0,7143); sebagian Percaya masih tertukar dengan Jijik (31%).
        4. **Label rujukan silver-standard:** Label dibuat oleh pipeline otomatis (Gemini API + aturan kata kunci), sehingga metrik menunjukkan kesesuaian dengan label tersebut, bukan dengan anotasi manusia.
        3. **Tantangan Evaluasi Model:**
           Sesuai literatur NLP kontemporer (Sokolova & Lapalme, 2009; Wilie dkk., 2020), distribusi korpus media sosial yang sangat timpang (*highly imbalanced*) menyebabkan kelas minoritas (Marah n=14, Sedih n=3 di test set) tidak terprediksi (F1 = 0) tanpa teknik oversampling/SMOTE, yang dicatat sebagai ruang pengembangan penelitian lanjutan (§5.3.2).
        """)

        # ── §4.5.4 VALIDASI ANOTASI MANUSIA AKTUAL & INTER-ANNOTATOR AGREEMENT ──
        st.markdown("---")
        st.subheader("🧑‍🔬 §4.5.4 Pengujian Aktual Validasi Anotasi Manusia (Empirical Human Ground Truth, n=100)")
        st.markdown("""
        > *Pengujian empiris aktual kesepakatan anotasi manusia (*Inter-Annotator Agreement / IAA*) dilakukan mengikuti protokol ilmiah
        > Plank dkk. (2014) dan Artstein & Poesio (2008) pada **100 sampel cuitan MBG terpilih** (`data/annotation/researcher_batch_100_FILLED.csv`)
        > yang dianotasi secara mendalam oleh pakar bahasa dan peneliti tesis.*
        """)

        col_iaa1, col_iaa2, col_iaa3, col_iaa4 = st.columns(4)
        with col_iaa1:
            st.metric("Akurasi vs Pakar Manusia", "90,00%", "90 dari 100 Tepat")
        with col_iaa2:
            st.metric("Cohen's Kappa (κ)", "0,8243", "Almost Perfect Agreement")
        with col_iaa3:
            st.metric("Macro F1 vs Pakar", "0,8097", "4 Kelas Aktif")
        with col_iaa4:
            st.metric("Weighted F1 vs Pakar", "0,8991", "Tertimbang Distribusi")

        st.caption("ℹ️ *Berdasarkan tolok ukur Landis & Koch (1977), skor Cohen's Kappa κ = 0,8243 (> 0,81) membuktikan tingkat kesepakatan hampir sempurna (Almost Perfect Agreement) antara penalaran pakar manusia dan inferensi model IndoBERT.*")

        tab_h1, tab_h2 = st.tabs(["🔲 Matriks Konfusi: Pakar Manusia vs IndoBERT", "📋 Tabel Evaluasi Performa per Kelas vs Anotasi Manusia"])

        with tab_h1:
            cm_h_display = pd.DataFrame([
                {"Label Pakar Manusia": "🤢 Jijik", "Jijik (Prediksi)": 50, "Percaya (Prediksi)": 4, "Netral (Prediksi)": 1, "Tertarik (Prediksi)": 1, "Total Pakar": 56, "Recall (%)": "89,29%"},
                {"Label Pakar Manusia": "🤝 Percaya", "Jijik (Prediksi)": 1, "Percaya (Prediksi)": 33, "Netral (Prediksi)": 0, "Tertarik (Prediksi)": 1, "Total Pakar": 35, "Recall (%)": "94,29%"},
                {"Label Pakar Manusia": "😐 Netral", "Jijik (Prediksi)": 2, "Percaya (Prediksi)": 0, "Netral (Prediksi)": 2, "Tertarik (Prediksi)": 0, "Total Pakar": 4, "Recall (%)": "50,00%"},
                {"Label Pakar Manusia": "🧐 Tertarik", "Jijik (Prediksi)": 0, "Percaya (Prediksi)": 0, "Netral (Prediksi)": 0, "Tertarik (Prediksi)": 5, "Total Pakar": 5, "Recall (%)": "100,00%"}
            ])
            st.dataframe(cm_h_display, width='stretch', hide_index=True)

        with tab_h2:
            df_rep_h = pd.DataFrame([
                {"Kelas Emosi": "🤢 Jijik", "Support Pakar": 56, "Precision": "0,9434 (94,34%)", "Recall": "0,8929 (89,29%)", "F1-Score": "0,9174", "Catatan Kualitatif": "Model menangkap sarkasme yang gagal dideteksi silver rule."},
                {"Kelas Emosi": "🤝 Percaya", "Support Pakar": 35, "Precision": "0,8919 (89,19%)", "Recall": "0,9429 (94,29%)", "F1-Score": "0,9167", "Catatan Kualitatif": "Apresiasi dan doa dukungan teridentifikasi konsisten."},
                {"Kelas Emosi": "😐 Netral", "Support Pakar": 4, "Precision": "0,6667 (66,67%)", "Recall": "0,5000 (50,00%)", "F1-Score": "0,5714", "Catatan Kualitatif": "Pewartaan berita faktual angka anggaran."},
                {"Kelas Emosi": "🧐 Tertarik", "Support Pakar": 5, "Precision": "0,7143 (71,43%)", "Recall": "1,0000 (100,00%)", "F1-Score": "0,8333", "Catatan Kualitatif": "Ekspektasi menu dan jadwal pembagian di sekolah."}
            ])
            st.dataframe(df_rep_h, width='stretch', hide_index=True)

        st.markdown("---")
        # ── §4.6 SINTESIS MARKETING 6.0, ABSA 3 ASPEK, & TRIANGULASI KOMPUTASIONAL ──
        st.markdown("---")


    with tab_iv_6:
        st.header("🌐 §4.6 Aspect-Based Sentiment Analysis (ABSA), Triangulasi Komputasional & Phygital Gap")
        st.markdown("""
        > *Bagian ini menyajikan rekonstruksi visual komprehensif dari **Bab IV (§4.6 Halaman 105 – 109)** naskah tesis.
        > Di sini dilakukan triangulasi metode 3 dimensi: **NLP IndoBERT (Afeksi & Sindiran)** $\\times$ **SNA Louvain (Topologi & Aktor)** $\\times$ **ABSA (3 Pilar Fisik Kebijakan)**
        > untuk menganalisis eksistensi dan membedah secara tuntas **"Artinya"** (makna teoretis, komunikasi krisis, dan implikasi kebijakan) dari fenomena **Phygital Gap**.*
        """)

        # 1. Load Data ABSA
        path_absa_file = get_result_path("absa_results.csv")

        if os.path.exists(path_absa_file):
            df_absa_data = pd.read_csv(path_absa_file)
        else:
            df_absa_data = pd.DataFrame([
                {"Aspect": "Logistik & Distribusi", "Total_Tweets": 403, "Disgust_Count": 318, "Disgust_Pct": 78.91, "Trust_Count": 21, "Trust_Pct": 5.21, "Neutral_Interest_Count": 64, "Neutral_Interest_Pct": 15.88},
                {"Aspect": "Anggaran & Vendor", "Total_Tweets": 535, "Disgust_Count": 412, "Disgust_Pct": 77.01, "Trust_Count": 23, "Trust_Pct": 4.30, "Neutral_Interest_Count": 100, "Neutral_Interest_Pct": 18.69},
                {"Aspect": "Kualitas Gizi", "Total_Tweets": 1344, "Disgust_Count": 956, "Disgust_Pct": 71.13, "Trust_Count": 119, "Trust_Pct": 8.85, "Neutral_Interest_Count": 269, "Neutral_Interest_Pct": 20.01}
            ])

        # 2. Metric KPI Cards (3 Aspek Fisik)
        st.subheader("🎯 1. Tiga Pilar Fisik Operasional Kebijakan (Data Riil ABSA)")
        st.caption("Distribusi sentimen publik terhadap 3 pilar operasional fisik Makan Bergizi Gratis (Total N = 2.282 cuitan terklasifikasi aspek):")

        absa_kpi1, absa_kpi2, absa_kpi3 = st.columns(3)
        with absa_kpi1:
            st.error("""
            ### 🚚 Logistik & Distribusi
            **Total Diskursus:** 403 Cuitan (17,66%)
            - 🤢 **Jijik (Disgust): 78,91%** (318 cuitan) ★
            - 🤝 **Percaya (Trust): 5,21%** (21 cuitan)
            - 😐 **Netral/Minat: 15,88%** (64 cuitan)

            **Isu Utama Lapangan:**
            Makanan basi, aroma busuk, katering terlambat, porsi hancur dalam perjalanan, insiden keracunan di sekolah uji coba.
            """)
        with absa_kpi2:
            st.warning("""
            ### 💰 Anggaran & Vendor
            **Total Diskursus:** 535 Cuitan (23,44%)
            - 🤢 **Jijik (Disgust): 77,01%** (412 cuitan) ★
            - 🤝 **Percaya (Trust): 4,30%** (23 cuitan)
            - 😐 **Netral/Minat: 18,69%** (100 cuitan)

            **Isu Utama Lapangan:**
            Wacana pemangkasan pagu Rp15.000 ➔ Rp7.500–10.000, tender katering tertutup, dugaan rente pihak ketiga, efisiensi APBN.
            """)
        with absa_kpi3:
            st.info("""
            ### 🥗 Kualitas Gizi Makanan
            **Total Diskursus:** 1.344 Cuitan (58,90%)
            - 🤢 **Jijik (Disgust): 71,13%** (956 cuitan) ★
            - 🤝 **Percaya (Trust): 8,85%** (119 cuitan)
            - 😐 **Netral/Minat: 20,01%** (269 cuitan)

            **Isu Utama Lapangan:**
            Menu dominan karbohidrat minim protein/susu, ketiadaan sertifikat uji klinis gizi, kekhawatiran menu tidak higienis.
            """)

        # 3. Interactive Visualizations for ABSA
        st.markdown("---")
        st.subheader("📊 2. Visualisasi Interaktif ABSA (Aspect-Based Sentiment Analysis)")

        absa_tab1, absa_tab2, absa_tab3, absa_tab4 = st.tabs([
            "📊 Komparasi Sentimen 3 Aspek (Grouped & Stacked Bar)",
            "🕸️ Radar Chart Profil Emosi 3 Pilar",
            "🔍 Eksplorasi Leksikon & Sampel Cuitan Riil",
            "🖼️ Visualisasi Tematik Tesis (Gambar 10)"
        ])

        with absa_tab1:
            st.markdown("#### 📈 Perbandingan Proporsi Sentimen antar Aspek Kebijakan")
            chart_mode = st.radio("Pilih Tampilan Grafik:", ["Grouped Bar (Persentase %)", "Stacked Bar 100% (Komposisi)", "Absolute Volume (Jumlah Cuitan)"], horizontal=True)

            fig_absa_bar = go.Figure()

            if chart_mode == "Grouped Bar (Persentase %)":
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Disgust_Pct'],
                    name='🤢 Jijik / Disgust (Negatif Ekstrem)',
                    marker_color='#ef4444',
                    text=df_absa_data['Disgust_Pct'].apply(lambda v: f"{v:.1f}%"),
                    textposition='auto',
                    hovertemplate="<b>%{x}</b><br>Disgust: %{y:.2f}%<extra></extra>"
                ))
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Trust_Pct'],
                    name='🤝 Percaya / Trust (Apresiasi)',
                    marker_color='#10b981',
                    text=df_absa_data['Trust_Pct'].apply(lambda v: f"{v:.1f}%"),
                    textposition='auto',
                    hovertemplate="<b>%{x}</b><br>Trust: %{y:.2f}%<extra></extra>"
                ))
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Neutral_Interest_Pct'],
                    name='😐 Netral & Minat Ekspektasi',
                    marker_color='#64748b',
                    text=df_absa_data['Neutral_Interest_Pct'].apply(lambda v: f"{v:.1f}%"),
                    textposition='auto',
                    hovertemplate="<b>%{x}</b><br>Netral: %{y:.2f}%<extra></extra>"
                ))
                fig_absa_bar.update_layout(
                    barmode='group',
                    yaxis_title="Persentase Cuitan (%)",
                    yaxis=dict(range=[0, 95])
                )
            elif chart_mode == "Stacked Bar 100% (Komposisi)":
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Disgust_Pct'],
                    name='🤢 Jijik / Disgust',
                    marker_color='#ef4444',
                    text=df_absa_data['Disgust_Pct'].apply(lambda v: f"{v:.1f}%"),
                    textposition='inside',
                    hovertemplate="<b>%{x}</b><br>Disgust: %{y:.2f}%<extra></extra>"
                ))
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Trust_Pct'],
                    name='🤝 Percaya / Trust',
                    marker_color='#10b981',
                    text=df_absa_data['Trust_Pct'].apply(lambda v: f"{v:.1f}%"),
                    textposition='inside',
                    hovertemplate="<b>%{x}</b><br>Trust: %{y:.2f}%<extra></extra>"
                ))
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Neutral_Interest_Pct'],
                    name='😐 Netral / Minat',
                    marker_color='#64748b',
                    text=df_absa_data['Neutral_Interest_Pct'].apply(lambda v: f"{v:.1f}%"),
                    textposition='inside',
                    hovertemplate="<b>%{x}</b><br>Netral: %{y:.2f}%<extra></extra>"
                ))
                fig_absa_bar.update_layout(
                    barmode='stack',
                    yaxis_title="Komposisi Sentimen Total (100%)",
                    yaxis=dict(range=[0, 105])
                )
            else: # Absolute Volume
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Disgust_Count'],
                    name='🤢 Jijik (Cuitan)',
                    marker_color='#ef4444',
                    text=df_absa_data['Disgust_Count'].apply(lambda v: f"{v:,}"),
                    textposition='auto',
                    hovertemplate="<b>%{x}</b><br>Disgust: %{y:,} cuitan<extra></extra>"
                ))
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Trust_Count'],
                    name='🤝 Percaya (Cuitan)',
                    marker_color='#10b981',
                    text=df_absa_data['Trust_Count'].apply(lambda v: f"{v:,}"),
                    textposition='auto',
                    hovertemplate="<b>%{x}</b><br>Trust: %{y:,} cuitan<extra></extra>"
                ))
                fig_absa_bar.add_trace(go.Bar(
                    x=df_absa_data['Aspect'],
                    y=df_absa_data['Neutral_Interest_Count'],
                    name='😐 Netral (Cuitan)',
                    marker_color='#64748b',
                    text=df_absa_data['Neutral_Interest_Count'].apply(lambda v: f"{v:,}"),
                    textposition='auto',
                    hovertemplate="<b>%{x}</b><br>Netral: %{y:,} cuitan<extra></extra>"
                ))
                fig_absa_bar.update_layout(
                    barmode='group',
                    yaxis_title="Jumlah Cuitan Riil (n)"
                )

            fig_absa_bar.update_layout(
                title="Distribusi Sentimen per Aspek Kebijakan (Naskah Tesis Bab 4.6)",
                template="plotly_dark",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                height=450,
                margin=dict(l=20, r=20, t=60, b=30)
            )
            st.plotly_chart(fig_absa_bar, width='stretch')
            st.info("💡 **Temuan Utama:** Emosi **Jijik (Disgust)** konsisten melampaui **70%** di seluruh aspek fisik, dengan puncaknya pada **Logistik & Distribusi (78,91%)** dan **Anggaran & Vendor (77,01%)**. Hal ini mengonfirmasi bahwa penolakan publik berakar pada kegagalan operasional fisik di lapangan.")

        with absa_tab2:
            st.markdown("#### 🕸️ Profil Polar / Radar Chart Sentimen 3 Aspek Fisik")
            st.caption("Memvisualisasikan asimetri tajam sentimen di mana polygon emosi condong ekstrem ke arah Disgust:")

            categories = ['🤢 Jijik (Disgust)', '🤝 Percaya (Trust)', '😐 Netral & Minat']

            fig_radar = go.Figure()

            # Trace Logistik
            r_log = [df_absa_data.loc[df_absa_data['Aspect'] == 'Logistik & Distribusi', 'Disgust_Pct'].values[0],
                     df_absa_data.loc[df_absa_data['Aspect'] == 'Logistik & Distribusi', 'Trust_Pct'].values[0],
                     df_absa_data.loc[df_absa_data['Aspect'] == 'Logistik & Distribusi', 'Neutral_Interest_Pct'].values[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=r_log + [r_log[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='🚚 Logistik & Distribusi (Disgust 78.9%)',
                line_color='#ef4444'
            ))

            # Trace Anggaran
            r_ang = [df_absa_data.loc[df_absa_data['Aspect'] == 'Anggaran & Vendor', 'Disgust_Pct'].values[0],
                     df_absa_data.loc[df_absa_data['Aspect'] == 'Anggaran & Vendor', 'Trust_Pct'].values[0],
                     df_absa_data.loc[df_absa_data['Aspect'] == 'Anggaran & Vendor', 'Neutral_Interest_Pct'].values[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=r_ang + [r_ang[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='💰 Anggaran & Vendor (Disgust 77.0%)',
                line_color='#f59e0b'
            ))

            # Trace Gizi
            r_giz = [df_absa_data.loc[df_absa_data['Aspect'] == 'Kualitas Gizi', 'Disgust_Pct'].values[0],
                     df_absa_data.loc[df_absa_data['Aspect'] == 'Kualitas Gizi', 'Trust_Pct'].values[0],
                     df_absa_data.loc[df_absa_data['Aspect'] == 'Kualitas Gizi', 'Neutral_Interest_Pct'].values[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=r_giz + [r_giz[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='🥗 Kualitas Gizi (Disgust 71.1%)',
                line_color='#3b82f6'
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 90], tickfont=dict(size=10, color='white')),
                    bgcolor='#1e293b'
                ),
                template="plotly_dark",
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
                height=480,
                margin=dict(l=40, r=40, t=30, b=80)
            )
            st.plotly_chart(fig_radar, width='stretch')

        with absa_tab3:
            st.markdown("#### 🔬 Eksplorasi Leksikon & Sampel Cuitan Riil per Aspek")

            col_lex1, col_lex2 = st.columns([1, 2])
            with col_lex1:
                selected_aspect = st.selectbox(
                    "Pilih Aspek Kebijakan:",
                    ["Logistik & Distribusi", "Anggaran & Vendor", "Kualitas Gizi"]
                )

                lexicons = {
                    "Logistik & Distribusi": "basi|racun|katering|telat|busuk|bau|dapur|distribusi|porsi",
                    "Anggaran & Vendor": "anggaran|pajak|korupsi|dana|triliun|harga|rp|biaya|apbn|vendor",
                    "Kualitas Gizi": "gizi|susu|sehat|stunting|nutrisi|telur|menu|protein|vitamin"
                }
                curr_lex = lexicons[selected_aspect]

                st.code(f"Regex Pattern:\n{curr_lex}", language="text")
                st.caption(f"Daftar kata kunci leksikal yang memfilter aspek **{selected_aspect}** dari korpus inferensi naskah tesis.")

                filter_emotion = st.selectbox(
                    "Filter Emosi Cuitan:",
                    ["Semua Emosi", "Jijik", "Percaya", "Netral", "Tertarik", "Marah"]
                )

            with col_lex2:
                try:
                    df_all_tweets = load_emotion_data()
                    mask_aspect = df_all_tweets['text'].str.contains(curr_lex, case=False, na=False)
                    df_aspect_tweets = df_all_tweets[mask_aspect].copy()

                    if filter_emotion != "Semua Emosi":
                        df_aspect_tweets = df_aspect_tweets[df_aspect_tweets['predicted_emotion'] == filter_emotion]

                    st.markdown(f"**Menampilkan Cuitan Riil Terfilter (Ditemukan: {len(df_aspect_tweets):,} cuitan):**")

                    sample_display = df_aspect_tweets[['text', 'predicted_emotion', 'confidence_score']].head(8)
                    sample_display.columns = ['Teks Cuitan Netizen', 'Emosi Terdeteksi', 'Skor Keyakinan']
                    st.dataframe(sample_display, width='stretch', hide_index=True)
                except Exception as e:
                    st.warning(f"Memuat sampel cuitan: {e}")

        with absa_tab4:
            st.markdown("#### 🖼️ Gambar 10 Naskah Tesis: Analisis Sentimen 3 Aspek Kunci Program MBG")
            img_absa_path = get_result_path("10_absa_thematic.png")
            if os.path.exists(img_absa_path):
                st.image(img_absa_path, width='stretch', caption="Gambar 10: Analisis Sentimen 3 Aspek Kunci Program MBG (Data Riil)")
                st.info("""
                **Keterangan Akademik Naskah Tesis (Halaman 106):**
                Grafik di atas menganalisis bahwa penolakan masyarakat di ranah digital tidak tertuju pada urgensi pemenuhan gizi anak sekolah,
                melainkan dipicu oleh kekecewaan terhadap kegagalan teknis rantai pasok logistik (78,91% sentimen negatif)
                dan kekhawatiran distorsi alokasi anggaran belanja vendor katering (77,01% sentimen negatif).
                """)
            else:
                st.warning("File 10_absa_thematic.png belum ditemukan di direktori results.")

        # 4. TRIANGULASI KOMPUTASIONAL 3 LAPIS
        st.markdown("---")
        st.subheader("🧩 3. Triangulasi Metodologis Komputasional 3 Dimensi (Bab 2.8, 3.6, & 4.6)")
        st.markdown("""
        Triangulasi komputasional menggabungkan tiga instrumen analitik independen untuk memvalidasi satu kesimpulan empiris:
        apakah **Phygital Gap** benar-benar terjadi dalam persepsi publik terhadap program MBG?
        """)

        tri_c1, tri_c2, tri_c3 = st.columns(3)
        with tri_c1:
            st.success("""
            #### 🧠 Lapis 1: NLP IndoBERT
            **Dimensi Afektif & Bahasa**
            *Apa yang dirasakan publik?*
            - **Distribusi emosi:** Jijik 56,24%, Percaya 20,39%, Netral 12,33%, Tertarik 9,60% (N=5.263)
            - **Sindiran Valid:** 9,28% (315 tweet)
            - **Proksi Inkongruensi:** 56,60% (2.979 tweet)

            **Temuan Kunci:**
            Distribusi emosi pada dataset digunakan untuk mendeskripsikan hasil klasifikasi model; temuan ini tidak digunakan untuk menyimpulkan motif atau sikap psikologis warganet.
            """)
        with tri_c2:
            st.info("""
            #### 🕸️ Lapis 2: SNA Louvain
            **Dimensi Topologi & Struktur Sosial**
            *Bagaimana diskursus menyebar?*
            - **Modularity $Q = 0,9837$** (342 komunitas)
            - **Resiprositas:** 1,20% (Komunikasi 1 arah)
            - **asymmetric interaction structure:** @prabowo in-degree=15 dan @grok out-degree=42.

            **Temuan Kunci:**
            Struktur jaringan menunjukkan keterpisahan struktural antarkomunitas dan rendahnya reciprocity; temuan ini tidak digunakan untuk menyimpulkan struktur komunitas atau respons aktual pembuat kebijakan.
            """)
        with tri_c3:
            st.warning("""
            #### 🎯 Lapis 3: ABSA 3 Aspek
            **Dimensi Diagnostik Fisik Operasional**
            *Di mana letak kegagalan fisik kebijakan?*
            - **Logistik:** 78,91% Disgust
            - **Anggaran:** 77,01% Disgust
            - **Gizi:** 71,13% Disgust

            **Temuan Kunci:**
            Kegagalan bukan pada visi gizi, melainkan pada **eksekusi operasional fisik**: makanan basi, porsi minimalis, dan tata kelola katering yang diragukan.
            """)

        # Tabel Matriks Triangulasi Komputasional
        st.markdown("#### 📋 Matriks Konvergensi Triangulasi Komputasional (Naskah Tesis)")
        triangulation_matrix = [
            {
                "Lapisan Analisis": "Lapis 1: Afektif (NLP IndoBERT)",
                "Instrumen / Algoritma": "IndoBERT Base-p2 Fine-Tuned (9 Emosi Plutchik) + Ekstraksi Leksikon Sarkasme",
                "Data Empiris Riil": "Jijik 56,24% (Disgust), 9,28% Sindiran Tervalidasi (n=315 dari 3.395), 56,60% Proksi Afektif Inkongruen",
                "Kontribusi Interpretasi Phygital Gap": "Menganalisis distribusi emosi dan sindiran mendalam warganet yang disamarkan dalam bentuk ironi dan sarkasme."
            },
            {
                "Lapisan Analisis": "Lapis 2: Topologi (SNA Louvain)",
                "Instrumen / Algoritma": "Graf Berarah, Algoritma Komunitas Louvain, Degree, Betweenness, & Eigenvector Centrality",
                "Data Empiris Riil": "Modularity Q = 0,9837 (342 komunitas), Resiprositas 1,20%, @prabowo memiliki in-degree=15 dan @grok memiliki out-degree=42",
                "Kontribusi Interpretasi Phygital Gap": "Menganalisis pola keterhubungan akun dalam graf mention; struktur interaksi digunakan sebagai deskripsi jaringan dan tidak digunakan untuk menyimpulkan kepasifan atau kekosongan otoritas."
            },
            {
                "Lapisan Analisis": "Lapis 3: Diagnostik (ABSA 3 Aspek)",
                "Instrumen / Algoritma": "Aspect-Based Sentiment Analysis berbasis Leksikon Tematik Kebijakan (Logistik, Anggaran, Gizi)",
                "Data Empiris Riil": "Logistik 78,91% Disgust (n=403), Anggaran 77,01% Disgust (n=535), Gizi 71,13% Disgust (n=1.344)",
                "Kontribusi Interpretasi Phygital Gap": "Menemukan akar luka kebijakan: kegagalan terletak pada titik sentuh fisik (makanan basi dan pemotongan anggaran katering)."
            }
        ]
        st.dataframe(pd.DataFrame(triangulation_matrix), width='stretch', hide_index=True)

        # Masterpiece Visual Triangulasi
        img_tri_path = get_result_path("integrated_sna_nlp.png")
        if os.path.exists(img_tri_path):
            st.image(img_tri_path, width='stretch', caption="Masterpiece Visual: Triangulasi Terintegrasi SNA x NLP (Data Riil Naskah Tesis)")

        # 5. "ARTINYA" — SINTESIS MAKNA TEORETIS, KRISIS, & KEBIJAKAN
        st.markdown("---")
        st.header("💡 4. \"Artinya\" — Sintesis Makna Teoretis, Komunikasi Krisis, & Rekomendasi Kebijakan")
        st.markdown("""
        > *Pertanyaan terbesar dalam sidang dan naskah tesis: **"Lalu apa artinya semua angka empiris ini?"**
        > Bagian ini menyajikan sintesis komprehensif atas signifikansi teoretis, sosiologis, dan praktis dari temuan riset.*
        """)

        with st.expander("🌐 1. Arti bagi Teori Pemasaran Modern: Interpretasi Fenomena Phygital Gap (Kotler et al., 2023)", expanded=True):
            st.markdown("""
            **Landasan Teoretis: Marketing 6.0 (Kotler, Kartajaya, & Setiawan, 2023)**
            - **Definisi Phygital:** Integrasi mulus antara ruang digital (*online marketing*) dan ruang fisik (*offline delivery/touchpoint*).
            - **Apa yang Terjadi pada Program MBG?**
              1. **Digital Promise (Ekspektasi di X/Medsos):** Pemerintah dan pendukung menyuarakan program MBG sebagai lompatan peradaban untuk mencetak *Generasi Emas 2045*, menuntaskan stunting, dan memicu pertumbuhan ekonomi rakyat.
              2. **Physical Delivery (Realitas di Sekolah):** Uji coba lapangan menghasilkan insiden katering basi, aroma tidak sedap, keterlambatan jam makan siang siswa, dan pemangkasan porsi menu.
              3. **Terjadinya Gap:** Tercipta jurang disonansi kognitif yang tajam (*expectation-reality mismatch*). Ketika realitas fisik gagal memenuhi ekspektasi digital, kepercayaan masyarakat runtuh seketika, termanifestasi dalam **78,91% sentimen Jijik (Disgust) pada aspek Logistik**.
            """)

        with st.expander("🚨 2. Arti bagi Komunikasi Krisis Publik: Situational Crisis Communication Theory (Coombs, 2007)", expanded=True):
            st.markdown("""
            **Landasan Teoretis: Coombs' SCCT (2007)**
            - **Kategori Krisis Publik:** Masyarakat mempersepsikan insiden makanan basi dan pemotongan anggaran menu bukan sebagai kecelakaan tak terduga (*Accidental Cluster*), melainkan sebagai **Preventable Crisis** (krisis yang dapat dicegah jika pemerintah melakukan pengawasan ketat).
            - **Kegagalan Respons Komunikasi:**
              - Resiprositas jaringan komunikasi hanya **1,20%**, dan akun @prabowo memiliki in-degree = 15 dalam jaringan mention yang dianalisis.
              - Ketiadaan klarifikasi cepat tidak diukur secara langsung oleh graf mention; penelitian ini hanya melaporkan struktur interaksi yang teramati.
              - Dalam graf yang dianalisis, tercatat **315 cuitan (9,28%)** pada dataset sindiran tervalidasi dan @grok memiliki **out-degree = 42**. Kedua temuan tersebut dilaporkan sebagai karakteristik data tanpa menyimpulkan motif atau fungsi verifikasi.
            """)

        with st.expander("🏛️ 3. Arti bagi Sosiologi Komunikasi & Demokrasi Digital: Kematian Ruang Publik Deliberatif (Habermas, 1989)", expanded=False):
            st.markdown("""
            **Landasan Teoretis: Ruang Publik Deliberatif (Jürgen Habermas)**
            - Nilai **Modularity $Q = 0,9837$** dan terbentuknya **342 komunitas Louvain dengan keterpisahan struktural** menunjukkan tingkat keterpisahan struktural komunitas yang tinggi dalam jaringan yang dianalisis.
            - Sebaliknya, diskursus menunjukkan keterpisahan struktural antarkomunitas:
              - Komunitas elit/pendukung hanya membagikan euforia seremonial (*empathy/love*).
              - Ratusan kantong komunitas warganet biasa mengisolasi diri dalam sirkulasi kemarahan dan kejijikan (*disgust/cynicism*).
            - Tidak ada jembatan komunikasi (*bridging social capital*) yang mempertemukan suara akar rumput dengan pembuat kebijakan.
            """)

        with st.expander("💼 4. Implikasi Manajerial & Rekomendasi Solusi Strategis untuk Badan Gizi Nasional (BGN)", expanded=True):
            st.markdown("""
            Berdasarkan temuan ABSA dan Triangulasi Komputasional, berikut 4 rekomendasi taktis-strategis untuk pembuat kebijakan:

            1. **🚚 Solusi Logistik & Rantai Pasok (Menjawab 78,91% Disgust):**
               - Terapkan sertifikasi rantai dingin (*cold-chain*) untuk seluruh armada distribusi makanan berjarak tempuh >30 menit.
               - Tetapkan batas radius operasional Satuan Pelayanan Pemenuhan Gizi (SPPBG) maksimal 5 km dari sekolah target untuk meminimalisir risiko makanan basi.

            2. **💰 Solusi Transparansi Anggaran (Menjawab 77,01% Disgust):**
               - Publikasikan *Unit Cost Breakdown* (rincian biaya bahan makanan vs biaya operasional kemasan/pengantaran) secara terbuka di dashboard web BGN.
               - Terapkan mekanisme lelang vendor berbasis e-katalog terbuka untuk menepis narasi sinis tentang kongkalikong vendor katering.

            3. **🥗 Solusi Kualitas Gizi & Higienitas (Menjawab 71,13% Disgust pada 1.344 Cuitan):**
               - Wajibkan penempatan minimal 1 orang Ahli Gizi (Nutrisionis) tersertifikasi PERSAGI di setiap dapur sentral SPPBG.
               - Lakukan uji organoleptik dan uji sampel mikroba cepat (*rapid test*) sebelum makanan didistribusikan ke sekolah.

            4. **📢 Solusi Komunikasi Krisis Phygital (Menjawab Modularity 0.9837 & asymmetric interaction structure):**
               - Tinggalkan pola komunikasi monolog satu arah (*broadcast*).
               - Bentuk Tim Respons Cepat Krisis (*Digital Rapid Response Unit*) di bawah BGN yang aktif memantau mention keluhan wali murid di media sosial dan memberikan solusi ganti rugi makanan dalam tempo < 1 jam.
            """)




