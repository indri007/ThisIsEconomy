import os
import re
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import sys

# Pastikan modul lokal (scraper, analyzer) selalu dapat diimport dari direktori mana pun
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from scraper import scrape_tweets_sync, get_secret
from analyzer import analyze_dataframe

st.set_page_config(
    page_title="Sentimen MBG — Twitter/X AI Monitor",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🍱 Dashboard Sentimen & Peringatan Dini MBG")
st.caption("Monitoring Twitter/X: Scraping (Twikit) + Analisis AI (Gemini) + Early Warning System (EWS Mandiri)")

if "df" not in st.session_state:
    st.session_state.df = None

# Cek status API Keys & Secrets default
gemini_key_default = get_secret("GEMINI_API_KEY", "")
tw_auth = get_secret("TWITTER_AUTH_TOKEN")
tw_ct0 = get_secret("TWITTER_CT0")

# ==============================================================================
# HELPER: EARLY WARNING SYSTEM (EWS) LOKAL
# ==============================================================================
CRISIS_TIERS = {
    "tier1": ["keracunan", "dirawat", "pingsan", "masuk rs", "mati", "meninggal", "ambulans", "rumah sakit"],
    "tier2": ["basi", "busuk", "belatung", "ulat", "korupsi", "sppg", "dihentikan", "ditutup", "dibekukan"],
    "tier3": ["kecewa", "malu", "gagal", "bohong", "janji", "tidak sesuai", "kurang", "tidak layak", "tidak enak"]
}
SARCASM_EMOJIS = ["🤡", "🙃", "🤮", "🤢", "😒", "💀", "😤", "🤬", "🤦", "😅", "🙄"]
FAKE_POS_EMOJIS = ["✨", "❤️", "🥰", "😍", "👍", "🎉", "🌟"]

def compute_ews(df: pd.DataFrame) -> dict:
    """Kalkulasi skor risiko krisis EWS (0-100) langsung dari data tweet."""
    if df is None or df.empty:
        return {"score": 0, "status": "⚪ TIDAK ADA DATA", "color": "#94a3b8", "action": "-", "details": {}}

    text_series = df["text"].fillna("").astype(str).str.lower()
    combined_text = " ".join(text_series.tolist())
    N = max(len(df), 1)

    # 1. Kata Kunci Krisis
    t1_hits = sum(combined_text.count(kw) for kw in CRISIS_TIERS["tier1"])
    t2_hits = sum(combined_text.count(kw) for kw in CRISIS_TIERS["tier2"])
    t3_hits = sum(combined_text.count(kw) for kw in CRISIS_TIERS["tier3"])
    kw_weighted = (t1_hits * 3) + (t2_hits * 2) + (t3_hits * 1)
    score_kw = min((kw_weighted / N * 100) / 15 * 30, 30)

    # 2. Emoji Sarkasme
    raw_text = " ".join(df["text"].fillna("").astype(str).tolist())
    sarcasm_em_hits = sum(raw_text.count(em) for em in SARCASM_EMOJIS)
    fake_pos_hits = sum(raw_text.count(em) for em in FAKE_POS_EMOJIS)
    emoji_total = (sarcasm_em_hits * 2) + fake_pos_hits
    score_emoji = min((emoji_total / N * 100) / 20 * 20, 20)

    # 3. Sentimen Negatif
    sent_col = "sentiment" if "sentiment" in df.columns else ("sentimen" if "sentimen" in df.columns else None)
    if sent_col:
        neg_ratio = (df[sent_col].astype(str).str.lower() == "negatif").sum() / N
        score_neg = min(neg_ratio * 30, 30)
    else:
        score_neg = 10.0  # baseline netral

    # 4. Rasio Sarkasme
    sarc_col = "is_sarcasm" if "is_sarcasm" in df.columns else ("sindiran" if "sindiran" in df.columns else None)
    if sarc_col:
        sarc_mask = (
            (df[sarc_col] == True) | 
            (df[sarc_col] == 1) | 
            (df[sarc_col].astype(str).str.lower().isin(["true", "1", "ya", "sindiran", "sarcasm"]))
        )
        sarc_ratio = sarc_mask.sum() / N
        score_sarc = min(sarc_ratio * 20, 20)
    else:
        score_sarc = 0.0

    total_score = round(score_kw + score_emoji + score_neg + score_sarc, 1)

    if total_score >= 75:
        status = "🔴 KRITIS — TINDAKAN SEGERA"
        color = "#ef4444"
        action = "Aktifkan protokol mitigasi krisis darurat. Koordinasikan Humas BGN & Kemenkes < 24 jam."
    elif total_score >= 50:
        status = "🟠 BAHAYA — RESPONS CEPAT"
        color = "#f97316"
        action = "Siapkan rilis pers dan tanggapan resmi. Pantau eskalasi isu setiap 6 jam."
    elif total_score >= 25:
        status = "🟡 WASPADA — PEMANTAUAN INTENSIF"
        color = "#eab308"
        action = "Pantau perkembangan isu secara intensif dan siapkan draf klarifikasi jika memburuk."
    else:
        status = "🟢 AMAN — SITUASI TERKENDALI"
        color = "#22c55e"
        action = "Situasi publik kondusif. Pemantauan rutin harian sudah memadai."

    return {
        "score": total_score,
        "status": status,
        "color": color,
        "action": action,
        "details": {
            "t1": t1_hits, "t2": t2_hits, "t3": t3_hits,
            "emoji_hits": sarcasm_em_hits + fake_pos_hits,
            "score_kw": round(score_kw, 1),
            "score_emoji": round(score_emoji, 1),
            "score_neg": round(score_neg, 1),
            "score_sarc": round(score_sarc, 1)
        }
    }


# ==============================================================================
# SIDEBAR PENGATURAN
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Pengaturan")

    with st.expander("🔑 Status Kredensial", expanded=False):
        if gemini_key_default:
            st.success("🟢 Gemini API Terkonfigurasi")
        else:
            st.caption("⚪ Gemini API belum ada di Secrets/.env")

        if tw_auth and tw_ct0:
            st.success("🟢 Twitter Session Terhubung")
        else:
            st.warning("🟡 Twitter Cookie belum lengkap")

    st.subheader("1. Scraping Twitter/X")
    keyword = st.text_input("Keyword pencarian", value='MBG OR "Makan Bergizi Gratis"')
    limit = st.number_input("Jumlah tweet", min_value=10, max_value=1000, value=50, step=10)
    product = st.selectbox("Tipe hasil", ["Latest", "Top"])
    scrape_btn = st.button("🔍 Scrape Tweet Baru", width='stretch')

    st.divider()
    st.subheader("2. Analisis AI (Gemini)")
    user_api_key = st.text_input(
        "Gemini API Key (Opsional)",
        value=gemini_key_default,
        type="password",
        help="Dapatkan gratis di aistudio.google.com. Kunci tersamarkan dengan aman."
    )
    batch_size = st.slider("Batch size (tweet/request)", 5, 20, 10)
    analyze_btn = st.button(
        "🤖 Analisis Sentimen & Sarkasme",
        width='stretch',
        disabled=st.session_state.df is None
    )

    st.divider()
    st.subheader("3. Data Input")
    
    # Tombol quick load sample dataset
    sample_csv_path = os.path.join(CURRENT_DIR, "sample_tweets.csv")
    if os.path.exists(sample_csv_path):
        if st.button("📂 Muat Contoh Data (50 Tweet MBG)", width='stretch'):
            sample_df = pd.read_csv(sample_csv_path)
            if "sindiran" in sample_df.columns and "is_sarcasm" not in sample_df.columns:
                sample_df["is_sarcasm"] = sample_df["sindiran"].astype(bool)
            st.session_state.df = sample_df
            st.toast("✅ Berhasil memuat 50 contoh tweet MBG!")

    uploaded = st.file_uploader("Upload CSV Dataset Tweet", type=["csv"])
    if uploaded is not None:
        try:
            up_df = pd.read_csv(uploaded)
            if "full_text" in up_df.columns and "text" not in up_df.columns:
                up_df["text"] = up_df["full_text"]
            if "sindiran" in up_df.columns and "is_sarcasm" not in up_df.columns:
                up_df["is_sarcasm"] = up_df["sindiran"].astype(bool)
            if "sentimen" in up_df.columns and "sentiment" not in up_df.columns:
                up_df["sentiment"] = up_df["sentimen"]
            st.session_state.df = up_df
            st.toast(f"Berhasil memuat {len(st.session_state.df)} tweet dari file CSV!")
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

# ==============================================================================
# LOGIKA TOMBOL SCRAPE & ANALISIS
# ==============================================================================
if scrape_btn:
    with st.spinner(f"Mengambil {limit} tweet tentang '{keyword}' ..."):
        try:
            st.session_state.df = scrape_tweets_sync(keyword=keyword, limit=limit, product=product)
            st.success(f"Berhasil scrape {len(st.session_state.df)} tweet")
        except Exception as e:
            st.error(f"Gagal scraping: {e}")

if analyze_btn and st.session_state.df is not None:
    progress_bar = st.progress(0.0, text="Menganalisis tweet via Gemini API...")

    def update_progress(pct):
        progress_bar.progress(pct, text=f"Menganalisis tweet... {int(pct * 100)}%")

    with st.spinner("Menghubungi Gemini AI..."):
        try:
            active_key = user_api_key.strip() if user_api_key else None
            st.session_state.df = analyze_dataframe(
                st.session_state.df,
                batch_size=batch_size,
                progress_callback=update_progress,
                api_key=active_key
            )
            st.success("✅ Analisis sentimen, sarkasme, dan topik aspek selesai!")
        except Exception as e:
            st.error(f"Gagal analisis: {e}")

df = st.session_state.df

if df is None:
    st.info("👈 Silakan mulai dengan melakukan scraping tweet atau upload file CSV di sidebar sebelah kiri.")
    st.stop()
else:
    # ==============================================================================
    # SECTION: EARLY WARNING SYSTEM (EWS) - SELALU AKTIF TANPA GEMINI
    # ==============================================================================
    ews_res = compute_ews(df)

    st.subheader("🚨 Early Warning System (EWS) — Indikator Krisis Publik")
    ews_col1, ews_col2 = st.columns([1, 2])

    with ews_col1:
        st.markdown(
            f"""
            <div style="background-color: #1e293b; padding: 18px; border-radius: 12px; border-left: 6px solid {ews_res['color']};">
                <span style="font-size: 13px; color: #94a3b8; text-transform: uppercase;">Skor Risiko Peringatan Dini</span>
                <h1 style="color: {ews_res['color']}; margin: 4px 0 0 0; font-size: 42px;">{ews_res['score']} <span style="font-size: 18px; color: #94a3b8;">/ 100</span></h1>
                <h4 style="margin: 6px 0; color: #f8fafc;">{ews_res['status']}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

    with ews_col2:
        st.markdown(f"**📌 Rekomendasi Tindakan Humas/BGN:**\n\n> {ews_res['action']}")
        det = ews_res["details"]
        st.caption(
            f"**Faktor Pemicu**: Kata Kritis Tier-1 ({det.get('t1', 0)}×) | "
            f"Tier-2 ({det.get('t2', 0)}×) | "
            f"Emoji Sarkasme ({det.get('emoji_hits', 0)}×) | "
            f"Skor Bobot: [Kata: {det.get('score_kw', 0)}/30, Emoji: {det.get('score_emoji', 0)}/20, "
            f"Negatif: {det.get('score_neg', 0)}/30, Sarkasme: {det.get('score_sarc', 0)}/20]"
        )

    st.divider()

    # ==============================================================================
    # SECTION: TABEL DATA
    # ==============================================================================
    st.subheader("📄 Dataset Tweet MBG")
    st.dataframe(df, width='stretch', height=260)

    st.download_button(
        "⬇️ Unduh CSV Hasil",
        df.to_csv(index=False).encode("utf-8"),
        "tweets_mbg.csv",
        "text/csv",
    )

    # ==============================================================================
    # SECTION: ANALISIS SENTIMEN & SARKASME (JIKA SUDAH DIANALISIS)
    # ==============================================================================
    if "sentiment" not in df.columns:
        st.info("💡 Data di atas telah dinilai oleh **EWS Lokal**. Untuk mendapatkan klasifikasi sentimen, alasan sarkasme, dan topik aspek yang lebih mendalam, klik tombol **'🤖 Analisis Sentimen & Sarkasme'** di sidebar.")
        st.stop()
    else:
        st.divider()
        st.subheader("📊 Distribusi Sentimen & Topik Aspek")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tweet", len(df))
        col2.metric("Positif", int((df["sentiment"].astype(str).str.lower() == "positif").sum()))
        col3.metric("Negatif", int((df["sentiment"].astype(str).str.lower() == "negatif").sum()))
        sarc_count = int(df["is_sarcasm"].astype(str).str.lower().isin(["true", "1", "ya", "sindiran"]).sum()) if "is_sarcasm" in df.columns else 0
        col4.metric("Terdeteksi Sarkasme", sarc_count)

        c1, c2 = st.columns(2)

        with c1:
            sentiment_counts = df["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["sentiment", "jumlah"]
            fig = px.pie(
                sentiment_counts,
                names="sentiment",
                values="jumlah",
                title="Distribusi Sentimen Publik",
                color="sentiment",
                color_discrete_map={
                    "positif": "#22c55e",
                    "negatif": "#ef4444",
                    "netral": "#94a3b8"
                },
            )
            st.plotly_chart(fig, width='stretch')

        with c2:
            if "topic_aspect" in df.columns:
                aspect_counts = df["topic_aspect"].value_counts().reset_index()
                aspect_counts.columns = ["aspek", "jumlah"]
                fig2 = px.bar(
                    aspect_counts,
                    x="aspek",
                    y="jumlah",
                    title="Frekuensi Percakapan per Aspek Topik",
                    color="aspek"
                )
                st.plotly_chart(fig2, width='stretch')

        if "created_at" in df.columns:
            st.subheader("📈 Tren Sentimen dari Waktu ke Waktu")
            try:
                df["created_date"] = pd.to_datetime(df["created_at"]).dt.date
                trend = df.groupby(["created_date", "sentiment"]).size().reset_index(name="jumlah")
                fig3 = px.line(
                    trend,
                    x="created_date",
                    y="jumlah",
                    color="sentiment",
                    markers=True,
                    color_discrete_map={
                        "positif": "#22c55e",
                        "negatif": "#ef4444",
                        "netral": "#94a3b8"
                    }
                )
                st.plotly_chart(fig3, width='stretch')
            except Exception:
                pass

        st.subheader("☁️ Word Cloud Percakapan Publik")
        wc_col1, wc_col2 = st.columns(2)
        for col, sentiment_label, title in [
            (wc_col1, "positif", "Kata Dominan — Sentimen Positif"),
            (wc_col2, "negatif", "Kata Dominan — Sentimen Negatif"),
        ]:
            text_data = " ".join(df[df["sentiment"] == sentiment_label]["text"].astype(str))
            with col:
                st.caption(f"**{title}**")
                if text_data.strip():
                    wc = WordCloud(width=500, height=280, background_color="white").generate(text_data)
                    fig, ax = plt.subplots()
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.caption("Tidak ada data teks yang cukup.")

        sarc_mask = df["is_sarcasm"].astype(str).str.lower().isin(["true", "1", "ya", "sindiran"]) if "is_sarcasm" in df.columns else pd.Series(False, index=df.index)
        if sarc_mask.any():
            st.subheader("😏 Tweet Terdeteksi Sarkasme / Sindiran")
            cols_to_show = [c for c in ["username", "text", "sentiment", "sentiment_if_sarcasm_removed", "reason"] if c in df.columns]
            sarcasm_df = df[sarc_mask][cols_to_show]
            st.dataframe(sarcasm_df, width='stretch')
