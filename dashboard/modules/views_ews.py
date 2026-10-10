import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.modules.config import (
    PROJECT_ROOT,
    download_file_button,
    get_journal_docx_path,
    BRAND24_AVAILABLE,
    CUSTOM_EWS_AVAILABLE,
    CUSTOM_EWS_IMPORT_ERROR,
    TWITTER_MODULES_AVAILABLE,
    WORDCLOUD_AVAILABLE,
    MATPLOTLIB_AVAILABLE,
)

if MATPLOTLIB_AVAILABLE:
    import matplotlib.pyplot as plt

if WORDCLOUD_AVAILABLE:
    from wordcloud import WordCloud

if BRAND24_AVAILABLE:
    from brand24_client import (
        get_api_key, list_projects, get_mentions,
        get_project_stats, get_sentiment_breakdown,
        get_top_sources, get_authors, compute_early_warning_score
    )

if CUSTOM_EWS_AVAILABLE:
    try:
        from ews.custom_dashboard import render_custom_ews
    except Exception:
        render_custom_ews = None
else:
    render_custom_ews = None

if TWITTER_MODULES_AVAILABLE:
    try:
        from scraper import scrape_tweets_sync
        from analyzer import analyze_dataframe
    except Exception:
        scrape_tweets_sync = None
        analyze_dataframe = None


def render_journal_page():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">📑 International Journal Article — Indonesia Emas Submission Ready</div>
        <div class="hero-title">Digital Sarcasm as a Signal of Policy Distrust: Social Network Analysis and Emotion Classification of Indonesia's Free Nutritious Meal Program Discourse on X (Twitter)</div>
        <div class="hero-subtitle">Penulis: <b>Indri Anjar Kartika Sari</b> | Magister Ilmu Komunikasi UPN 'Veteran' Jawa Timur | Target: <i>Telematics and Informatics</i> (Elsevier, Q1) / <i>New Media & Society</i> (SAGE, Q1)</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Kata Naskah", "12,355 Kata", "Academic English")
    with m2:
        st.metric("Estimasi Halaman", "46–48 Halaman", "Standard Double-Spaced")
    with m3:
        st.metric("Gambar Ilmiah Tersemat", "11 Gambar", "300 DPI High-Res")
    with m4:
        st.metric("Tabel Empiris & Notasi", "7 Tabel + 4 Appendix", "APA 7th Standard")

    st.markdown("---")

    st.markdown("### 📥 Unduh Naskah Lengkap & Berkas Graf Penelitian (Format Microsoft Word .docx)")
    j_col1, j_col2 = st.columns(2)
    p_jcmc_doc = get_journal_docx_path("JCMC_OXFORD_MBG_COMMUNICATION_2026.docx")
    p_jcmc_pdf = get_journal_docx_path("JCMC_OXFORD_MBG_COMMUNICATION_2026.pdf")
    p_ics_doc = get_journal_docx_path("ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx")
    p_ics_pdf = get_journal_docx_path("ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.pdf")
    p_docx_latest = get_journal_docx_path("JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx")
    p_docx = get_journal_docx_path("Journal_Paper_Indri_Anjar_MBG_SNA.docx")
    p_md = os.path.join(PROJECT_ROOT, "journal_paper_mbg_sna.md")
    p_gexf = os.path.join(PROJECT_ROOT, "results", "mbg_network_official.gexf")

    with j_col1:
        st.markdown("""
        <div style="background: #f8fafc; border-left: 4px solid #4338ca; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
            <b>👑 Journal of Computer-Mediated Communication (JCMC)</b><br>
            <span style="font-size: 0.85rem; color: #475569;">Oxford University Press / ICA | Scopus Q1 | <b>71 Halaman (.docx)</b></span>
        </div>
        """, unsafe_allow_html=True)
        jb1, jb2 = st.columns(2)
        with jb1:
            download_file_button(
                label="📥 Unduh Word (.docx, 71 Hal)",
                file_path=p_jcmc_doc,
                file_name="JCMC_OXFORD_MBG_COMMUNICATION_2026.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                width='stretch',
            )
        with jb2:
            download_file_button(
                label="📄 Unduh PDF (71 Hal)",
                file_path=p_jcmc_pdf,
                file_name="JCMC_OXFORD_MBG_COMMUNICATION_2026.pdf",
                mime="application/pdf",
                width='stretch',
            )

    with j_col2:
        st.markdown("""
        <div style="background: #f8fafc; border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
            <b>📘 Information, Communication & Society (ICS)</b><br>
            <span style="font-size: 0.85rem; color: #475569;">Taylor & Francis | Scopus/SSCI Q1 | <b>23 Halaman (.docx)</b></span>
        </div>
        """, unsafe_allow_html=True)
        jb3, jb4 = st.columns(2)
        with jb3:
            download_file_button(
                label="📥 Unduh Word (.docx, 23 Hal)",
                file_path=p_ics_doc,
                file_name="ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                width='stretch',
            )
        with jb4:
            download_file_button(
                label="📄 Unduh PDF (23 Hal)",
                file_path=p_ics_pdf,
                file_name="ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.pdf",
                mime="application/pdf",
                width='stretch',
            )

    st.markdown("#### 📂 Berkas Riset Pendukung & Repositori")
    d0, d1, d2, d3, d4 = st.columns(5)
    with d0:
        download_file_button(
            label="⭐ Naskah Q1 2026 (.docx)",
            file_path=p_docx_latest,
            file_name="JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width='stretch',
        )

    with d1:
        download_file_button(
            label="📑 Tesis Lengkap (.docx)",
            file_path=p_docx,
            file_name="Journal_Paper_Indri_Anjar_MBG_SNA.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width='stretch',
        )

    with d2:
        download_file_button(
            label="📄 Unduh Markdown (.md)",
            file_path=p_md,
            file_name="journal_paper_mbg_sna.md",
            mime="text/markdown",
            width='stretch',
        )

    with d3:
        download_file_button(
            label="🌐 Graf Gephi (.gexf)",
            file_path=p_gexf,
            file_name="mbg_network_official.gexf",
            mime="application/xml",
            width='stretch',
        )

    with d4:
        st.link_button(
            "📦 Repositori GitHub",
            "https://github.com/indri007/ThisIsEconomy",
            width='stretch'
        )

    st.markdown("---")

    jtab1, jtab2, jtab3, jtab4 = st.tabs([
        "🔄 Matriks Sebab-Akibat-Solusi",
        "🤖 Analisis Aktor @grok & Solusi",
        "🚀 5 Poin Agenda Riset Lanjutan",
        "📖 Teks Lengkap Naskah Jurnal"
    ])

    with jtab1:
        st.subheader("Closed-Loop Governance Matrix: Mengaitkan Akar Masalah Awal dengan Solusi Strategis")
        matrix_data = [
            {
                "No": "1",
                "Akar Masalah Awal (Teori)": "The Phygital Gap (Kotler et al., 2023)\nBranding digital mewah bertolak belakang dengan fakta fisik makanan di sekolah.",
                "Bukti Komputasional (Data)": "ABSA: Kualitas Gizi menghasilkan volume terbesar (1.344 tweet) dengan 71.13% Disgust; leksikal keracunan & basi dominan.",
                "Dampak Institusional": "Penolakan moral & disonansi kognitif warga; kemarahan orang tua atas bahaya fisik anak.",
                "Solusi Tata Kelola": "Section 6.3: Alihkan 100% dana PR/influencer ke audit independen higienitas SPPG.\nSection 6.6: Aplikasi ko-monitoring partisipatif oleh wali murid & komite sekolah."
            },
            {
                "No": "2",
                "Akar Masalah Awal (Teori)": "Politik Simbolik Fiskal (Edelman, 1964)\nPengumuman pemotongan anggaran Rp 67T tanpa kalkulasi teknis transparan.",
                "Bukti Komputasional (Data)": "ABSA: Budget & Procurement mencatat 77.01% Disgust; asosiasi kata 'triliun' dengan 'bancakan/korupsi'.",
                "Dampak Institusional": "Angka pemangkasan ditafsirkan sebagai simbol kegagalan kebijakan dan bancakan politik.",
                "Solusi Tata Kelola": "Section 6.4: Buka API publik machine-readable rincian biaya per porsi (bahan baku, operasional, logistik) secara real-time."
            },
            {
                "No": "3",
                "Akar Masalah Awal (Teori)": "Vakum Deliberatif (Habermas, 1989)\nKomunikasi monolog satu arah birokrasi dan bantahan defensif dari pusat.",
                "Bukti Komputasional (Data)": "SNA: Modularity Q = 0.9837 (341 komponen terpisah), Densitas 0.0007, Resiprositas hanya 1.20% (monolog warganet ke @prabowo).",
                "Dampak Institusional": "Insularitas total; siaran pers satu arah dari Jakarta tidak mampu menembus 340 pulau komunitas warganet.",
                "Solusi Tata Kelola": "Section 6.2: Bubarkan rilis terpusat; bentuk kader respon cepat regional yang berdialog empatik di kolom balasan warganet."
            },
            {
                "No": "4",
                "Akar Masalah Awal (Teori)": "Perisai Paralinguistik (Scott, 1985; Camp, 2012)\nAncaman UU ITE memaksa warga menyamarkan kemarahan dalam sarkasme (🤡, 🙃).",
                "Bukti Komputasional (Data)": "Sarkasme Tipologi 1 mendominasi (pembuka laudatori dibatalkan emoji sindiran); NLP konvensional tertipu membaca 'positif'.",
                "Dampak Institusional": "Intelijen media pemerintah gagal mendeteksi krisis kepercayaan sejak dini hingga meledak ke aksi fisik.",
                "Solusi Tata Kelola": "Section 6.5: Integrasikan model Transformer sadar-emoji (IndoBERT) pada dashboard intelijen media sebagai indikator peringatan dini."
            },
            {
                "No": "5",
                "Akar Masalah Awal (Teori)": "Vakum Epistemik Otoritas Kebenaran\nKeterlambatan verifikasi resmi membuat warga kehilangan kepercayaan pada rujukan fakta.",
                "Bukti Komputasional (Data)": "SNA Centrality: Akun AI @grok menduduki Peringkat 1 Out-Degree (k=42, balasan otomatis) dan betweenness tertinggi (0,0059); @prabowo menjadi target keluhan (In-Degree 15).",
                "Dampak Institusional": "Warga menggusur jurnalis dan humas negara, mendelegasikan otoritas kebenaran pada bot AI swasta asing.",
                "Solusi Tata Kelola": "Section 6.4: Kemitraan grounding algoritmik dengan xAI/OpenAI & peluncuran bot verifikasi resmi BGN (@BGN_VerifikasiBot)."
            }
        ]
        st.dataframe(pd.DataFrame(matrix_data), width='stretch', hide_index=True)

    with jtab2:
        st.subheader("Fenomena Algorithmic Epistemic Displacement: Posisi Sentral Akun @grok")
        st.info("""
        Dalam jaringan komunikasi MBG, akun **`@grok` (AI asisten bawaan platform X milik xAI)** memiliki **Out-Degree = 42**: 42 balasan otomatis kepada warganet berbeda yang memanggilnya (tertinggi di seluruh jaringan), dengan betweenness tertinggi (0,0059). Sebaliknya, akun Presiden `@prabowo` memiliki **In-Degree = 15** tanpa satu pun balasan.
        Ini membuktikan terjadinya fenomena pergeseran otoritas kebenaran (*Algorithmic Epistemic Displacement*).
        """)

        gcol1, gcol2 = st.columns(2)
        with gcol1:
            st.markdown("#### 🚨 4 Dampak Kritis Akun @grok:")
            st.markdown("""
            1. **Disintermediasi Lembaga Cek Fakta Tradisional**: Warga tidak lagi me-mention jurnalis investigasi atau akademisi, melainkan memanggil `@grok` sebagai hakim kebenaran instan.
            2. **Kerentanan Halusinasi & Black-Box AI**: Respons Grok terdengar objektif dan netral, sehingga kesalahan inferensi atau rumor liar yang diserap Grok langsung dianggap sebagai "fakta ilmiah" oleh warganet.
            3. **Kehilangan Monopoli Narasi Pemerintah**: Siaran pers panjang dari birokrasi tidak dibaca warga; warga lebih percaya rangkuman 3 kalimat dari Grok.
            4. **Ketergantungan Kedaulatan Digital pada Swasta Asing**: Logika inferensi dan parameter bot berada di yurisdiksi korporasi asing (xAI) tanpa pengawasan otoritas Indonesia.
            """)
        with gcol2:
            st.markdown("#### 🛡️ 5 Solusi Strategis untuk Pemerintah:")
            st.markdown("""
            1. **Open Data Machine-Readable API**: BGN & Kemenkeu menyediakan API terbuka agar data anggaran dan status SPPG terbaca otomatis oleh mesin AI.
            2. **Algorithmic Grounding**: Kemkomdigi bermitra dengan penyedia LLM agar kueri gizi nasional merujuk ke *Knowledge Graph* resmi negara.
            3. **Sovereign Counter-Oracle Bot**: Meluncurkan `@BGN_VerifikasiBot` resmi di X dan WhatsApp yang responsif dan berbasis bukti lapangan.
            4. **Predictive Sentiment Mining**: Memantau topik pertanyaan warga ke Grok sebagai *early warning indicator* 24–48 jam sebelum krisis meledak.
            5. **Penyempurnaan Titik Sentuh Fisik**: Memastikan makanan di sekolah higienis, hangat, dan bergizi karena keunggulan fisik adalah komunikasi paling kredibel.
            """)

    with jtab3:
        st.subheader("5 Poin Agenda Penelitian Lanjutan (Future Research Agenda)")
        f1, f2 = st.columns(2)
        with f1:
            st.markdown("##### 1. Rekalibrasi IndoBERT & Benchmark Terbuka")
            st.write("Anotasi ulang korpus uji dengan 3 anotator independen (Cohen's Kappa > 0.85, Krippendorff's Alpha > 0.80) untuk mempublikasikan benchmark F1 9 emosi dan deteksi sarkasme terbuka.")

            st.markdown("##### 2. Analisis Komparatif Multimodal (X vs TikTok vs Instagram)")
            st.write("Mengintegrasikan visi komputer (CLIP/ViT) untuk mengkaji unboxing makanan MBG di TikTok vs kurasi visual di Instagram vs sindiran teks di X.")

            st.markdown("##### 3. Pemodelan Jaringan Temporal (TERGM & SIENA 2025–2029)")
            st.write("Melacak evolusi struktural longitudinal: apakah atomisasi (Q = 0.9837) menetap permanen atau mengkristal menjadi polarisasi biner dua kubu.")

        with f2:
            st.markdown("##### 4. Formulasi Digital Public Policy Trust Index (DPPTI)")
            st.latex(r"\text{DPPTI}_t = w_1 \cdot \left(\frac{\text{Trust}_t}{\text{Trust}_t + \text{Disgust}_t + \epsilon}\right) + w_2 \cdot (1 - Q_t) + w_3 \cdot R_t + w_4 \cdot \text{NetValence}_t")
            st.write("Metrik komposit terintegrasi berbasis waktu nyata untuk mendeteksi krisis legitimasi institusi sebelum terjadi penolakan fisik.")

            st.markdown("##### 5. Audit Algoritmik & Tata Kelola Epistemik AI")
            st.write("Eksperimen audit empiris pada LLM komersial (Grok, ChatGPT, Claude, Gemini) untuk mengukur tingkat halusinasi, bias ideologis, dan ketergantungan warga terhadap AI.")

    with jtab4:
        st.subheader("Teks Lengkap Manuskrip Jurnal Internasional (Indonesia Emas)")
        if os.path.exists(p_md):
            with open(p_md, "r", encoding="utf-8") as f_full:
                full_text = f_full.read()
            st.markdown(full_text)
        else:
            st.warning("Berkas journal_paper_mbg_sna.md belum ditemukan di repositori.")


CRISIS_TIERS = {
    "tier1": ["keracunan", "dirawat", "pingsan", "masuk rs", "mati", "meninggal", "ambulans", "rumah sakit"],
    "tier2": ["basi", "busuk", "belatung", "ulat", "korupsi", "sppg", "dihentikan", "ditutup", "dibekukan"],
    "tier3": ["kecewa", "malu", "gagal", "bohong", "janji", "tidak sesuai", "kurang", "tidak layak", "tidak enak"]
}
SARCASM_EMOJIS = ["🤡", "🙃", "🤮", "🤢", "😒", "💀", "😤", "🤬", "🤦", "😅", "🙄"]
FAKE_POS_EMOJIS = ["✨", "❤️", "🥰", "😍", "👍", "🎉", "🌟"]


def compute_ews_local(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {"score": 0, "status": "⚪ TIDAK ADA DATA", "color": "#94a3b8", "action": "-", "details": {}}

    text_col = "text" if "text" in df.columns else ("full_text" if "full_text" in df.columns else None)
    if text_col is None:
        return {"score": 0, "status": "⚪ KOLOM TEKS TIDAK DITEMUKAN", "color": "#94a3b8", "action": "-", "details": {}}

    text_series = df[text_col].fillna("").astype(str).str.lower()
    combined_text = " ".join(text_series.tolist())
    N = max(len(df), 1)

    t1_hits = sum(combined_text.count(kw) for kw in CRISIS_TIERS["tier1"])
    t2_hits = sum(combined_text.count(kw) for kw in CRISIS_TIERS["tier2"])
    t3_hits = sum(combined_text.count(kw) for kw in CRISIS_TIERS["tier3"])
    kw_weighted = (t1_hits * 3) + (t2_hits * 2) + (t3_hits * 1)
    score_kw = min((kw_weighted / N * 100) / 15 * 30, 30)

    raw_text = " ".join(df[text_col].fillna("").astype(str).tolist())
    sarcasm_em_hits = sum(raw_text.count(em) for em in SARCASM_EMOJIS)
    fake_pos_hits = sum(raw_text.count(em) for em in FAKE_POS_EMOJIS)
    emoji_total = (sarcasm_em_hits * 2) + fake_pos_hits
    score_emoji = min((emoji_total / N * 100) / 20 * 20, 20)

    sent_col = "sentiment" if "sentiment" in df.columns else ("sentimen" if "sentimen" in df.columns else None)
    if sent_col:
        neg_ratio = (df[sent_col].astype(str).str.lower() == "negatif").sum() / N
        score_neg = min(neg_ratio * 30, 30)
    else:
        score_neg = 10.0

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
        "score": total_score, "status": status, "color": color, "action": action,
        "details": {
            "t1": t1_hits, "t2": t2_hits, "t3": t3_hits,
            "emoji_hits": sarcasm_em_hits + fake_pos_hits,
            "score_kw": round(score_kw, 1), "score_emoji": round(score_emoji, 1),
            "score_neg": round(score_neg, 1), "score_sarc": round(score_sarc, 1)
        }
    }


def render_twitter_ai_page():
    st.markdown("# 🍱 Monitor Twitter/X AI & Early Warning System (EWS)")
    st.markdown("""
    > **Sistem Peringatan Dini Mandiri & Pemantauan Opini Publik MBG**
    > Mengintegrasikan scraping Twitter/X (Twikit), inferensi sentimen mendalam + deteksi sarkasme (Google Gemini 2.5 Flash),
    > serta komputasi skor risiko krisis otomatis (*Zero API Cost/Latency*).
    """)

    if "twitter_live_df" not in st.session_state or st.session_state.twitter_live_df is None:
        sample_path = os.path.join(PROJECT_ROOT, "twitter_sentiment_app", "sample_tweets.csv")
        if os.path.exists(sample_path):
            try:
                init_df = pd.read_csv(sample_path)
                if "sindiran" in init_df.columns and "is_sarcasm" not in init_df.columns:
                    init_df["is_sarcasm"] = init_df["sindiran"].astype(bool)
                st.session_state.twitter_live_df = init_df
            except Exception:
                st.session_state.twitter_live_df = None
        else:
            st.session_state.twitter_live_df = None

    df = st.session_state.twitter_live_df

    default_gemini_key = ""
    try:
        if "GEMINI_API_KEYS" in st.secrets:
            val = st.secrets["GEMINI_API_KEYS"]
            default_gemini_key = ", ".join(val) if isinstance(val, (list, tuple)) else str(val).strip()
        elif "GEMINI_API_KEY" in st.secrets:
            val = st.secrets["GEMINI_API_KEY"]
            default_gemini_key = ", ".join(val) if isinstance(val, (list, tuple)) else str(val).strip()
    except Exception:
        pass
    if not default_gemini_key:
        default_gemini_key = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY", "")

    with st.expander("⚙️ Panel Pengaturan & Kredensial AI", expanded=False):
        c_cfg1, c_cfg2 = st.columns(2)
        with c_cfg1:
            st.markdown("##### 🔑 Kredensial Gemini AI")
            user_gemini_key = st.text_input(
                "Gemini API Key(s):",
                value=default_gemini_key,
                type="password",
                help="Multi-key pool: Masukkan 1 key atau beberapa key dipisah koma. Otomatis rotasi dan failover jika kuota habis.",
                key="twitter_user_gemini_key"
            )
            configured_keys = []
            if TWITTER_MODULES_AVAILABLE:
                try:
                    from analyzer import parse_api_keys
                    configured_keys = parse_api_keys(user_gemini_key or default_gemini_key)
                except Exception:
                    pass
            if configured_keys:
                st.caption(f"Status Kredensial: 🟢 Terkonfigurasi ({len(configured_keys)} API Key dalam pool)")
            else:
                st.caption("Status Kredensial: ⚪ Kosong (masukkan API key atau atur di Secrets)")

        with c_cfg2:
            st.markdown("##### 📂 Muat atau Unggah Dataset")
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("📂 Muat Contoh Data (50 MBG)", width='stretch', key="load_sample_inside_btn"):
                    sample_path = os.path.join(PROJECT_ROOT, "twitter_sentiment_app", "sample_tweets.csv")
                    if os.path.exists(sample_path):
                        sample_df = pd.read_csv(sample_path)
                        if "sindiran" in sample_df.columns and "is_sarcasm" not in sample_df.columns:
                            sample_df["is_sarcasm"] = sample_df["sindiran"].astype(bool)
                        st.session_state.twitter_live_df = sample_df
                        st.rerun()

            up_file = st.file_uploader("Upload CSV Tweet:", type=["csv"], key="dash_uploader")
            if up_file is not None:
                try:
                    up_df = pd.read_csv(up_file)
                    if "full_text" in up_df.columns and "text" not in up_df.columns:
                        up_df["text"] = up_df["full_text"]
                    if "sindiran" in up_df.columns and "is_sarcasm" not in up_df.columns:
                        up_df["is_sarcasm"] = up_df["sindiran"].astype(bool)
                    if "sentimen" in up_df.columns and "sentiment" not in up_df.columns:
                        up_df["sentiment"] = up_df["sentimen"]
                    st.session_state.twitter_live_df = up_df
                    st.toast(f"Berhasil memuat {len(up_df)} tweet!")
                except Exception as e:
                    st.error(f"Gagal memuat file: {e}")

    tab_ews, tab_scrape, tab_ai = st.tabs([
        "🚨 Early Warning System (EWS)",
        "🔍 Scrape Tweet Baru (Twikit)",
        "🤖 Analisis Sentimen AI (Gemini)"
    ])

    with tab_scrape:
        st.markdown("### 🔍 Scraping Data Tweet MBG Terbaru")
        sc1, sc2, sc3 = st.columns([2, 1, 1])
        with sc1:
            kw = st.text_input("Keyword pencarian:", value='MBG OR "Makan Bergizi Gratis"', key="kw_dash")
        with sc2:
            lim = st.number_input("Jumlah tweet:", min_value=10, max_value=500, value=30, step=10, key="lim_dash")
        with sc3:
            prod = st.selectbox("Tipe hasil:", ["Latest", "Top"], index=0, key="prod_dash")

        if st.button("🚀 Mulai Scraping Tweet", width='stretch'):
            if not TWITTER_MODULES_AVAILABLE or scrape_tweets_sync is None:
                st.error("Modul scraper belum tersedia. Pastikan twitter_sentiment_app/ ada.")
            else:
                with st.spinner(f"Mengambil {lim} tweet tentang '{kw}' via Twikit..."):
                    try:
                        scraped = scrape_tweets_sync(keyword=kw, limit=lim, product=prod)
                        st.session_state.twitter_live_df = scraped
                        st.success(f"Berhasil mengunduh {len(scraped)} tweet!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal scraping: {e}")

    with tab_ai:
        st.markdown("### 🤖 Inferensi Sentimen & Sarkasme via Gemini AI")
        if df is None or df.empty:
            st.info("Muat data terlebih dahulu di tab EWS atau panel atas.")
        else:
            c_ai1, c_ai2 = st.columns([3, 1])
            with c_ai1:
                st.write(f"Dataset saat ini memiliki **{len(df)}** baris data tweet yang siap dianalisis.")
            with c_ai2:
                b_size = st.slider("Batch size:", 5, 20, 10, key="bsize_dash_ai", help="Tweet per API call")

            if st.button("⚡ Jalankan Analisis AI Sekarang", width='stretch', key="run_ai_dash"):
                if not TWITTER_MODULES_AVAILABLE or analyze_dataframe is None:
                    st.error("Modul analyzer belum tersedia.")
                else:
                    active_key = user_gemini_key.strip() if user_gemini_key else None
                    prog = st.progress(0.0, text="Menghubungi Gemini AI...")
                    def _cb(pct):
                        prog.progress(pct, text=f"Proses analisis AI: {int(pct * 100)}%")

                    with st.spinner("Menganalisis tweet via Gemini..."):
                        try:
                            analyzed = analyze_dataframe(df, batch_size=b_size, progress_callback=_cb, api_key=active_key)
                            st.session_state.twitter_live_df = analyzed
                            st.success("✅ Analisis sentimen, sarkasme, dan topik aspek sukses!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal analisis AI: {e}")

    with tab_ews:
        if df is None or df.empty:
            st.warning("⚠️ Belum ada dataset tweet yang dimuat. Klik tombol '📂 Muat Contoh Data (50 MBG)' di atas untuk melihat demonstrasi.")
            return

        ews_res = compute_ews_local(df)
        det = ews_res["details"]

        st.markdown("### 🚨 Indikator Risiko Publik & Peringatan Dini (EWS)")
        ews_col1, ews_col2 = st.columns([1, 2])

        with ews_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=ews_res["score"],
                title={"text": f"Skor Risiko EWS<br><span style='font-size:12px; color:{ews_res['color']}'>{ews_res['status']}</span>", "font": {"size": 16}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": ews_res["color"]},
                    "steps": [
                        {"range": [0, 25], "color": "#dcfce7"},
                        {"range": [25, 50], "color": "#fef9c3"},
                        {"range": [50, 75], "color": "#ffedd5"},
                        {"range": [75, 100], "color": "#fee2e2"},
                    ],
                    "threshold": {"line": {"color": "red", "width": 3}, "value": 75},
                }
            ))
            fig_gauge.update_layout(height=260, margin={"t": 30, "b": 10})
            st.plotly_chart(fig_gauge, width='stretch')

        with ews_col2:
            st.markdown(
                f"""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 6px solid {ews_res['color']}; margin-top: 10px;">
                    <h4 style="margin: 0 0 8px 0; color: {ews_res['color']};">{ews_res['status']}</h4>
                    <p style="margin: 0; color: #f1f5f9; font-size: 14.5px; line-height: 1.6;">
                        <b>📌 Rekomendasi Tindakan BGN / Humas:</b><br>{ews_res['action']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("🚨 Kata Tier-1 (Berat)", f"{det.get('t1', 0)}×")
            m2.metric("⚠️ Kata Tier-2 (Sedang)", f"{det.get('t2', 0)}×")
            m3.metric("😏 Emoji Sarkasme", f"{det.get('emoji_hits', 0)}×")
            m4.metric("📄 Total Tweet", f"{len(df):,}")

        st.markdown("---")
        st.markdown("### 📄 Data Tweet MBG")
        st.dataframe(df, width='stretch', height=260)
        st.download_button(
            "⬇️ Unduh Dataset Ini (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "dataset_mbg_monitor.csv",
            "text/csv"
        )

        if "sentiment" in df.columns:
            st.markdown("---")
            st.markdown("### 📊 Distribusi Sentimen Publik & Analisis Aspek")
            c_vis1, c_vis2 = st.columns(2)
            with c_vis1:
                sent_counts = df["sentiment"].value_counts().reset_index()
                sent_counts.columns = ["sentiment", "jumlah"]
                fig_p = px.pie(
                    sent_counts, names="sentiment", values="jumlah",
                    title="Distribusi Sentimen",
                    color="sentiment",
                    color_discrete_map={"positif": "#22c55e", "negatif": "#ef4444", "netral": "#94a3b8"}
                )
                st.plotly_chart(fig_p, width='stretch')

            with c_vis2:
                if "topic_aspect" in df.columns:
                    asp_counts = df["topic_aspect"].value_counts().reset_index()
                    asp_counts.columns = ["aspek", "jumlah"]
                    fig_b = px.bar(asp_counts, x="aspek", y="jumlah", title="Topik Aspek Kebijakan", color="aspek")
                    st.plotly_chart(fig_b, width='stretch')

            if WORDCLOUD_AVAILABLE and MATPLOTLIB_AVAILABLE:
                st.markdown("### ☁️ Word Cloud Opini Warganet")
                wc1, wc2 = st.columns(2)
                pos_txt = " ".join(df[df["sentiment"].astype(str).str.lower() == "positif"]["text"].astype(str))
                neg_txt = " ".join(df[df["sentiment"].astype(str).str.lower() == "negatif"]["text"].astype(str))

                with wc1:
                    st.caption("🟢 **Kata Kunci Sentimen Positif**")
                    if pos_txt.strip():
                        wc_pos = WordCloud(width=450, height=250, background_color="white").generate(pos_txt)
                        fig_w1, ax1 = plt.subplots()
                        ax1.imshow(wc_pos, interpolation="bilinear")
                        ax1.axis("off")
                        st.pyplot(fig_w1)
                    else:
                        st.caption("Tidak cukup data positif.")

                with wc2:
                    st.caption("🔴 **Kata Kunci Sentimen Negatif**")
                    if neg_txt.strip():
                        wc_neg = WordCloud(width=450, height=250, background_color="white").generate(neg_txt)
                        fig_w2, ax2 = plt.subplots()
                        ax2.imshow(wc_neg, interpolation="bilinear")
                        ax2.axis("off")
                        st.pyplot(fig_w2)
                    else:
                        st.caption("Tidak cukup data negatif.")

        sarc_col = "is_sarcasm" if "is_sarcasm" in df.columns else ("sindiran" if "sindiran" in df.columns else None)
        if sarc_col:
            s_mask = df[sarc_col].astype(str).str.lower().isin(["true", "1", "ya", "sindiran"])
            if s_mask.any():
                st.markdown("### 😏 Cuitan Mengandung Sindiran / Sarkasme")
                cols_show = [c for c in ["username", "text", "sentiment", "sentiment_if_sarcasm_removed", "reason"] if c in df.columns]
                if not cols_show:
                    cols_show = ["text", sarc_col]
                st.dataframe(df[s_mask][cols_show], width='stretch')


def render_big_data_page():
    st.markdown("### 📊 Tabel Dataset MBG")
    sample_path = os.path.join(PROJECT_ROOT, "data", "processed", "tweet_mbg_sample_public.csv")
    if not os.path.exists(sample_path):
        sample_path = os.path.join(PROJECT_ROOT, "data", "research", "tesis_dataset_final.csv")

    if os.path.exists(sample_path):
        @st.cache_data
        def load_public_sample():
            return pd.read_csv(sample_path)

        df_sample = load_public_sample()
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            q_search = st.text_input("Cari kata kunci:", placeholder="Ketik kata kunci pencarian...", label_visibility="collapsed")
        with col_f2:
            src_col = "source" if "source" in df_sample.columns else None
            if src_col:
                sources = ["Semua"] + list(df_sample[src_col].dropna().unique())
                src_filter = st.selectbox("Filter Sumber:", sources, label_visibility="collapsed")
            else:
                src_filter = "Semua"

        df_filtered = df_sample
        if q_search:
            text_col = "text" if "text" in df_filtered.columns else df_filtered.columns[1]
            df_filtered = df_filtered[df_filtered[text_col].astype(str).str.contains(q_search, case=False, na=False)]
        if src_col and src_filter != "Semua":
            df_filtered = df_filtered[df_filtered[src_col] == src_filter]

        st.dataframe(df_filtered, width='stretch', height=650)
        with open(sample_path, "rb") as f_samp:
            st.download_button(
                label="📥 Unduh Dataset CSV",
                data=f_samp.read(),
                file_name="dataset_mbg.csv",
                mime="text/csv"
            )
    else:
        st.warning("Berkas dataset tidak ditemukan.")


def render_ews_page():
    if CUSTOM_EWS_AVAILABLE and render_custom_ews:
        render_custom_ews()
    else:
        st.error("❌ Modul Custom EWS v2 tidak dapat dimuat.")
        if CUSTOM_EWS_IMPORT_ERROR:
            st.caption(f"Detail kendala: `{CUSTOM_EWS_IMPORT_ERROR}`")


def render_brand24_page():
    st.markdown("# 📡 Brand24 Real-Time Monitor")
    st.markdown("""
    > **Early Warning System (EWS)** — Pemantauan real-time sebaran diskusi MBG
    > di platform digital: Twitter/X, Instagram, berita online, forum, dan blog.
    > Data ditarik langsung dari API Brand24 (server-side) dan dianalisis secara otomatis.
    """)

    if not BRAND24_AVAILABLE:
        st.warning("🟡 **Brand24 tidak tersedia — otomatis beralih ke Custom EWS.**")
        if CUSTOM_EWS_AVAILABLE and render_custom_ews:
            render_custom_ews(7)
        else:
            st.error("❌ Modul Custom EWS juga tidak tersedia.")
        st.stop()

    st.markdown("### 🔑 Konfigurasi API Key")
    col_key1, col_key2 = st.columns([3, 1])
    with col_key1:
        manual_key = st.text_input(
            "Masukkan Brand24 API Key (opsional — bisa juga via .env):",
            type="password",
            placeholder="b24-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="API Key tersimpan hanya di session ini dan tidak dikirim ke server eksternal selain Brand24."
        )
    with col_key2:
        since_days = st.selectbox("Rentang Waktu:", [7, 14, 30, 90], index=0, format_func=lambda x: f"{x} Hari Terakhir")

    api_key = manual_key.strip() if manual_key.strip() else get_api_key()
    if not api_key:
        st.warning("🟡 **Brand24 API Key belum tersedia — otomatis beralih ke Custom EWS.**")
        st.info("Custom EWS menggunakan engine `early_warning_system.py` dan dataset MBG lokal.")
        if CUSTOM_EWS_AVAILABLE and render_custom_ews:
            render_custom_ews(since_days)
        else:
            st.error("❌ Modul Custom EWS tidak tersedia.")
        st.stop()

    with st.spinner("🔌 Menghubungkan ke Brand24 API..."):
        projects_data = list_projects(api_key)

    if not projects_data:
        st.warning("🟡 **Brand24 tidak dapat dihubungi — otomatis beralih ke Custom EWS.**")
        st.caption("Fallback aktif: Custom EWS → dataset MBG lokal.")
        if CUSTOM_EWS_AVAILABLE and render_custom_ews:
            render_custom_ews(since_days)
        else:
            st.error("❌ Modul Custom EWS tidak tersedia.")
        st.stop()

    project_list = projects_data.get("results", projects_data if isinstance(projects_data, list) else [])
    if not project_list:
        st.warning("🟡 **Tidak ada proyek Brand24 — otomatis beralih ke Custom EWS.**")
        if CUSTOM_EWS_AVAILABLE and render_custom_ews:
            render_custom_ews(since_days)
        else:
            st.error("❌ Modul Custom EWS tidak tersedia.")
        st.stop()

    proj_options = {f"[{p.get('id','?')}] {p.get('name', p.get('keyword','Proyek'))}": p for p in project_list}
    selected_label = st.selectbox("📁 Pilih Proyek Monitoring:", list(proj_options.keys()))
    selected_proj = proj_options[selected_label]
    project_id = selected_proj.get("id") or selected_proj.get("project_id")

    st.markdown("---")
    try:
        with st.spinner("⏳ Mengambil data dari Brand24..."):
            stats = get_project_stats(api_key, project_id, since_days=since_days)
            sents = get_sentiment_breakdown(api_key, project_id, since_days=since_days)
            mentions = get_mentions(api_key, project_id, since_days=since_days, max_results=200)
            sources = get_top_sources(api_key, project_id, since_days=since_days)
            authors = get_authors(api_key, project_id, since_days=since_days)
    except Exception as brand24_error:
        st.warning("🟡 **Brand24 mengalami error — otomatis beralih ke Custom EWS.**")
        st.caption(f"Fallback aktif. Detail: {brand24_error}")
        if CUSTOM_EWS_AVAILABLE and render_custom_ews:
            render_custom_ews(since_days)
        else:
            st.error("❌ Modul Custom EWS tidak tersedia.")
        st.stop()

    ews = compute_early_warning_score(stats, sents)
    st.markdown("### 🚨 Early Warning Score (EWS)")
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    col_g1.metric("🎯 EWS Score", f"{ews['score']}/100", ews['level'])
    col_g2.metric("💬 Total Mention", f"{ews['raw']['total_mentions']:,}")
    col_g3.metric("😡 Rasio Negatif", f"{ews['raw']['neg_ratio_pct']}%")
    col_g4.metric("😊 Positif", f"{ews['raw']['positive']:,}")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ews['score'],
        title={"text": "Early Warning Score (EWS)", "font": {"size": 18}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": "#EF4444" if ews['score'] >= 75 else "#F97316" if ews['score'] >= 50 else "#EAB308" if ews['score'] >= 25 else "#22C55E"},
            "steps": [
                {"range": [0, 25], "color": "#DCFCE7"},
                {"range": [25, 50], "color": "#FEF9C3"},
                {"range": [50, 75], "color": "#FFEDD5"},
                {"range": [75, 100], "color": "#FEE2E2"},
            ],
            "threshold": {"line": {"color": "red", "width": 3}, "value": 75},
        },
        delta={"reference": 50, "increasing": {"color": "red"}, "decreasing": {"color": "green"}},
    ))
    fig_gauge.update_layout(height=280, margin={"t": 40, "b": 10})
    st.plotly_chart(fig_gauge, width='stretch')

    st.markdown("---")
    st.markdown("### 📊 Distribusi Sentimen")
    sent_raw = ews['raw']
    sent_df = pd.DataFrame({
        "Sentimen": ["😡 Negatif", "😊 Positif", "😐 Netral"],
        "Jumlah": [sent_raw['negative'], sent_raw['positive'], sent_raw['neutral']],
    })
    fig_sent = px.bar(
        sent_df, x="Sentimen", y="Jumlah", color="Sentimen",
        color_discrete_map={"😡 Negatif": "#EF4444", "😊 Positif": "#22C55E", "😐 Netral": "#94A3B8"},
        title=f"Distribusi Sentimen — {since_days} Hari Terakhir",
        text="Jumlah",
    )
    fig_sent.update_traces(textposition="outside")
    fig_sent.update_layout(showlegend=False, height=340)
    st.plotly_chart(fig_sent, width='stretch')
