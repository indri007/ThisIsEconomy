"""
ews/custom_dashboard.py
=======================
Komponen Antarmuka Pengguna (UI) Dasbor Custom Early Warning System (EWS) v2.
Terintegrasi secara mulus ke dalam dashboard/app.py dan menyediakan
analisis multimodal: IndoBERT 7-Emosi, SNA Centrality, dan Deteksi Anomali.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ews.config import (
    INDOBERT_MODEL_METADATA,
    EWS_WEIGHTS,
    DATA_PATHS,
)
from ews.ews_engine import compute_custom_ews_v2


@st.cache_data(ttl=600)
def get_cached_ews_results(anomaly_threshold: float = 2.0) -> dict:
    """Mengambil hasil komputasi EWS dengan caching agar dasbor responsif."""
    return compute_custom_ews_v2(anomaly_threshold=anomaly_threshold)


def render_custom_ews(since_days: int = 7) -> None:
    """
    Fungsi utama penampil dasbor Custom EWS v2.
    Dapat dipanggil sebagai standalone tab maupun sebagai fallback otomatis saat Brand24 belum aktif.
    """
    # ── HEADER & BANNER ──────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 24px; border-radius: 12px; border-left: 6px solid #EF4444; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <h2 style="color: #F8FAFC; margin: 0 0 8px 0; font-size: 26px; font-weight: 700;">
            🚨 MBG Early Warning System — Custom EWS v2
        </h2>
        <p style="color: #94A3B8; margin: 0; font-size: 14px; line-height: 1.5;">
            Sistem Peringatan Dini Risiko Wacana Kebijakan Makan Bergizi Gratis (MBG) berbasis triangulasi
            <b>NLP IndoBERT (7 Emosi Aktual)</b>, <b>Social Network Analysis (971 Aktor, 342 Komunitas)</b>,
            dan <b>Deteksi Anomali Statistik Runtut Waktu</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Indikator Status Sumber Data & Fallback
    c_status1, c_status2, c_status3 = st.columns([2, 1, 1])
    with c_status1:
        st.info("ℹ️ **Status Operasional:** Berjalan menggunakan **Custom EWS Local Engine** (Analisis dataset empiris MBG 5.263 tweet).")
    with c_status2:
        st.caption("📡 **Integrasi Brand24:** Tersedia sebagai fallback otomatis jika API key/kuota Brand24 tidak aktif.")
    with c_status3:
        threshold_input = st.slider("Sensitivitas Z-Score:", min_value=1.5, max_value=3.5, value=2.0, step=0.1, help="Ambang batas deteksi lonjakan anomali volume harian.")

    # ── HITUNG HASIL EWS ENGINE ──────────────────────────────────
    with st.spinner("🔄 Memproses matriks risiko EWS multimodal..."):
        ews = get_cached_ews_results(anomaly_threshold=threshold_input)

    score = ews["score"]
    status_label = ews["level_label"]
    status_color = ews["color"]
    metrics = ews["metrics"]
    components = ews["components"]
    daily_df = ews["daily_anomaly_df"]
    sna = ews["sna_summary"]

    # ── 1. KPI TOP SUMMARY CARDS ─────────────────────────────────
    st.markdown("### 📊 Indikator Utama Risiko Wacana (KPI)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; text-align: center;">
            <span style="font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase;">EWS RISK SCORE</span>
            <div style="font-size: 32px; font-weight: 800; color: {status_color}; margin: 4px 0;">{score} <span style="font-size: 16px; color: #64748B;">/100</span></div>
            <span style="background: {status_color}20; color: {status_color}; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 13px;">{status_label}</span>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; text-align: center;">
            <span style="font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase;">VOLUME CUUTAN</span>
            <div style="font-size: 32px; font-weight: 800; color: #0F172A; margin: 4px 0;">{metrics['total_tweets']:,}</div>
            <span style="color: #64748B; font-size: 13px;">{metrics['active_days']} Hari Aktif</span>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; text-align: center;">
            <span style="font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase;">EMOSI DOMINAN</span>
            <div style="font-size: 30px; font-weight: 800; color: #E11D48; margin: 4px 0;">{metrics['dominant_emotion']}</div>
            <span style="color: #E11D48; font-weight: 600; font-size: 13px;">{metrics['dominant_pct']}% Korpus</span>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; text-align: center;">
            <span style="font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase;">RASIO SINDIRAN</span>
            <div style="font-size: 32px; font-weight: 800; color: #D97706; margin: 4px 0;">{metrics['sarcasm_rate_pct']}%</div>
            <span style="color: #D97706; font-weight: 600; font-size: 13px;">Sarkasme Terverifikasi</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 2. TIME-SERIES MENTION VOLUME & ANOMALY DETECTION ─────────
    st.markdown("### 📈 Runtut Waktu Volume Cuitan & Deteksi Anomali Statistik")
    st.caption("Deteksi lonjakan mendadak berdasarkan deviasi Z-Score (Ambang batas: Z ≥ {:.1f}). Titik merah menandai tanggal anomali.".format(threshold_input))

    if not daily_df.empty:
        fig_vol = go.Figure()

        # Garis Volume Harian
        fig_vol.add_trace(go.Scatter(
            x=daily_df["date"],
            y=daily_df["mentions"],
            mode="lines+markers",
            name="Cuitan Harian",
            line=dict(color="#3B82F6", width=2),
            marker=dict(size=4)
        ))

        # Garis Rata-rata Bergerak 7 Hari
        fig_vol.add_trace(go.Scatter(
            x=daily_df["date"],
            y=daily_df["rolling_mean"],
            mode="lines",
            name="Moving Average (7 Hari)",
            line=dict(color="#94A3B8", width=1.5, dash="dash")
        ))

        # Titik Anomali (Spike)
        anomalies = daily_df[daily_df["is_anomaly"]]
        if not anomalies.empty:
            fig_vol.add_trace(go.Scatter(
                x=anomalies["date"],
                y=anomalies["mentions"],
                mode="markers",
                name="Anomali Terdeteksi (Spike)",
                marker=dict(color="#EF4444", size=12, symbol="circle-open-dot", line=dict(width=3, color="#EF4444")),
                hovertext=[
                    f"Tanggal: {d}<br>Volume: {m:,} cuitan<br>Z-Score: {z:.2f}"
                    for d, m, z in zip(anomalies["date"], anomalies["mentions"], anomalies["z_score"])
                ],
                hoverinfo="text"
            ))

        fig_vol.update_layout(
            height=360,
            margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Tanggal Pemantauan", showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(title="Jumlah Cuitan", showgrid=True, gridcolor="#F1F5F9"),
            hovermode="x unified"
        )
        st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.info("Data runtut waktu harian belum tersedia.")

    st.markdown("---")

    # ── 3. DUA KOLOM: EMOSI INDOBERT & SNA TOP ACTORS ────────────
    col_mid1, col_mid2 = st.columns(2)

    with col_mid1:
        st.markdown("### 🧠 Sebaran 7 Emosi Aktual IndoBERT")
        st.caption("Distribusi emosi dari 5.263 cuitan (Model IndoBERT fine-tuned 7 kelas aktual).")

        emo_dist = components["emotion_risk"]["details"]["distribution"]
        palette = INDOBERT_MODEL_METADATA["label_color_palette"]

        df_emo_chart = pd.DataFrame([
            {"Emosi": k, "Jumlah": v, "Persen": round(v / metrics["total_tweets"] * 100, 2)}
            for k, v in emo_dist.items()
        ]).sort_values("Jumlah", ascending=True)

        fig_emo = px.bar(
            df_emo_chart,
            x="Jumlah",
            y="Emosi",
            orientation="h",
            text="Persen",
            color="Emosi",
            color_discrete_map=palette,
        )
        fig_emo.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_emo.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=20, r=40, t=10, b=30),
            xaxis=dict(title="Jumlah Tweet"),
            yaxis=dict(title="")
        )
        st.plotly_chart(fig_emo, use_container_width=True)

    with col_mid2:
        st.markdown("### 🕸️ Simpul Jejaring Kunci SNA")
        st.caption("Aktor dengan sentralitas konektivitas (Degree) dan penjembatan informasi (Betweenness) tertinggi.")

        top_actors = sna["top_degree_actors"][:5]
        df_actors = pd.DataFrame([
            {
                "Akun / Label": f"@{a['Label']}",
                "Degree": f"{a['Degree']:.4f}",
                "Betweenness": f"{a['Betweenness']:.4f}",
                "Komunitas": f"K-{a['Community']}",
                "Emosi Dominan": a["Dominant_Emotion"]
            }
            for a in top_actors
        ])
        st.dataframe(df_actors, use_container_width=True, hide_index=True)

        st.caption(
            "💡 *Catatan metodologis:* Simpul sentralitas tinggi berfungsi sebagai pusat agregasi atau jembatan transmisi wacana, "
            "bukan representasi kausal penyebab krisis."
        )

    st.markdown("---")

    # ── 4. DUA KOLOM: KATA KUNCI KRISIS & PARTISI KOMUNITAS ───────
    col_bot1, col_bot2 = st.columns(2)

    with col_bot1:
        st.markdown("### 🔥 Sinyal Kata Kunci Krisis & Emoji")
        st.caption("Deteksi frekuensi istilah kritis bertingkat (Tier 1 Medis, Tier 2 Higienis, Tier 3 Kebijakan).")

        top_terms = components["keyword_risk"]["details"]["top_crisis_terms"]
        if top_terms:
            df_terms = pd.DataFrame(top_terms).sort_values("hits", ascending=True)
            tier_colors = {1: "#EF4444", 2: "#F59E0B", 3: "#3B82F6"}
            df_terms["Warna"] = df_terms["tier"].map(tier_colors)

            fig_kw = px.bar(
                df_terms,
                x="hits",
                y="term",
                orientation="h",
                color="tier",
                color_discrete_map={1: "#EF4444", 2: "#F59E0B", 3: "#3B82F6"},
                text="hits",
                labels={"term": "Istilah", "hits": "Frekuensi", "tier": "Tier Risiko"}
            )
            fig_kw.update_traces(textposition="outside")
            fig_kw.update_layout(
                height=320,
                margin=dict(l=20, r=40, t=10, b=30),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                xaxis=dict(title="Frekuensi"),
                yaxis=dict(title="")
            )
            st.plotly_chart(fig_kw, use_container_width=True)
        else:
            st.info("Belum ada kata kunci krisis terdeteksi.")

    with col_bot2:
        st.markdown("### 👥 Klaster Komunitas Terbesar (SNA)")
        st.caption("10 komunitas terbesar dari total 342 partisi modularitas ($Q=0.9837$).")

        comm_data = sna["top_community_clusters"]
        df_comm = pd.DataFrame([
            {
                "ID Komunitas": f"Komunitas {c['Community']}",
                "Jumlah Anggota": c["Node_Count"],
                "Emosi Dominan": c["Dominant_Emotion"].capitalize(),
            }
            for c in comm_data
        ])
        st.dataframe(df_comm, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── 5. TRANSPARANSI SKOR (EXPLAINABILITY BOX) ─────────────────
    st.markdown("### 🚨 Mengapa Skor EWS Berada pada Tingkat Ini? (Explainability)")

    # Rincian Matriks Komponen Bobot
    st.markdown("""
    Skor EWS v2 dihitung secara transparan dari 5 dimensi risiko terbobot (Total: 100 Poin):
    """)

    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
    b_col1.metric("1. Emosi Negatif", f"{components['emotion_risk']['score']} / {components['emotion_risk']['max']}", "IndoBERT")
    b_col2.metric("2. Sarkasme", f"{components['sarcasm_risk']['score']} / {components['sarcasm_risk']['max']}", "Sindiran")
    b_col3.metric("3. Kata Kunci", f"{components['keyword_risk']['score']} / {components['keyword_risk']['max']}", "Tier 1-3")
    b_col4.metric("4. Volume Puncak", f"{components['volume_risk']['score']} / {components['volume_risk']['max']}", "Rasio Mean")
    b_col5.metric("5. Deteksi Anomali", f"{components['anomaly_risk']['score']} / {components['anomaly_risk']['max']}", f"{metrics['spikes_count']} Lonjakan")

    with st.expander("📝 Uraian Analisis dan Bukti Empiris Lengkap", expanded=True):
        for idx, exp_text in enumerate(ews["explanation"], 1):
            st.markdown(f"**{idx}.** {exp_text}")

        st.markdown(f"""
        ---
        **💡 Rekomendasi Tindakan Strategis Humas & Kebijakan:**
        {ews['action_recommendation']}
        """)
