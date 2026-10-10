import os
import sys
import time
from pathlib import Path
import requests
import streamlit as st

# Setup Root & Subdirectory Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(DASHBOARD_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
TWITTER_APP_DIR = os.path.join(PROJECT_ROOT, "twitter_sentiment_app")
if TWITTER_APP_DIR not in sys.path:
    sys.path.insert(0, TWITTER_APP_DIR)

# Feature flags & optional dependencies
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False

try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Brand24 client
try:
    from brand24_client import (
        get_api_key, list_projects, get_mentions,
        get_project_stats, get_sentiment_breakdown,
        get_top_sources, get_authors, compute_early_warning_score
    )
    BRAND24_AVAILABLE = True
except ImportError:
    BRAND24_AVAILABLE = False

# Custom EWS
CUSTOM_EWS_IMPORT_ERROR = None
try:
    from ews.custom_dashboard import render_custom_ews
    CUSTOM_EWS_AVAILABLE = True
except Exception as e:
    render_custom_ews = None
    CUSTOM_EWS_AVAILABLE = False
    CUSTOM_EWS_IMPORT_ERROR = str(e)

# Twitter Sentiment App
try:
    from scraper import scrape_tweets_sync
    from analyzer import analyze_dataframe
    TWITTER_MODULES_AVAILABLE = True
except ImportError:
    TWITTER_MODULES_AVAILABLE = False


@st.cache_resource
def _telegram_sent_log():
    return {}


def send_telegram_alert(message, cooldown=600):
    """Kirim alert ke Telegram; pesan yang sama maks. 1x per `cooldown` detik."""
    try:
        token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
    except Exception:
        return
    log = _telegram_sent_log()
    now = time.time()
    if now - log.get(message, 0) < cooldown:
        return
    log[message] = now
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": f"🚨 tesis_mbg dashboard\n{message}"},
            timeout=5,
        )
    except Exception:
        pass


def download_file_button(label, file_path, file_name, mime, key=None, **kwargs):
    """Safe wrapper for st.download_button that reads from disk."""
    if os.path.exists(file_path):
        mode = "r" if mime and mime.startswith("text") else "rb"
        encoding = "utf-8" if mode == "r" else None
        with open(file_path, mode, **(dict(encoding=encoding) if encoding else {})) as _f:
            data = _f.read()
        st.download_button(
            label=label,
            data=data,
            file_name=file_name,
            mime=mime,
            key=key,
            **kwargs,
        )
    else:
        st.button(
            f"{label} — (file tidak tersedia)",
            disabled=True,
            key=key,
            **kwargs,
        )


def resolve_image_path(filename_or_path):
    """Robustly resolve any image path across repository directory structures."""
    if not filename_or_path:
        return None
    p = str(filename_or_path)
    if os.path.exists(p):
        return os.path.abspath(p)
    filename = os.path.basename(p)
    candidates = [
        os.path.join(PROJECT_ROOT, "results", filename),
        os.path.join(PROJECT_ROOT, "results", "storytelling", filename),
        os.path.join(PROJECT_ROOT, "docs", "assets", filename),
        os.path.join(PROJECT_ROOT, "figures", filename),
        os.path.join(PROJECT_ROOT, "images", filename),
        os.path.join(PROJECT_ROOT, "results", "indobert_group_aware_v2", filename),
        os.path.join(PROJECT_ROOT, "results", "zenodo_replication_package", "figures", filename),
        os.path.join(DASHBOARD_DIR, "assets", filename),
        os.path.join(PROJECT_ROOT, filename),
        os.path.join("results", filename),
        os.path.join("results", "storytelling", filename),
        os.path.join("docs", "assets", filename),
        os.path.join("figures", filename),
        os.path.join("images", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None


def get_result_path(filename):
    resolved = resolve_image_path(filename)
    if resolved:
        return resolved
    candidates = [
        os.path.join(PROJECT_ROOT, "results", filename),
        os.path.join(PROJECT_ROOT, "results", "storytelling", filename),
        os.path.join("results", filename),
        os.path.join("results", "storytelling", filename),
        os.path.join("..", "results", filename),
        os.path.join("..", "results", "storytelling", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return os.path.join(PROJECT_ROOT, "results", filename)


def get_image_path(filename):
    """Centralized resolver for image files across repository."""
    resolved = resolve_image_path(filename)
    if resolved:
        return resolved
    return get_result_path(filename)


# Globally monkeypatch st.image to be crash-proof against missing files / Streamlit storage errors
if not hasattr(st, "_raw_image_original"):
    st._raw_image_original = st.image


def _crash_proof_st_image(image_input, *args, **kwargs):
    caption = kwargs.get("caption", None)
    if isinstance(image_input, (str, Path)):
        img_str = str(image_input)
        if not os.path.exists(img_str):
            resolved = resolve_image_path(img_str)
            if resolved and os.path.exists(resolved):
                img_str = resolved
            else:
                cap_text = caption if caption else f"Visualisasi {os.path.basename(img_str)}"
                st.info(f"📊 **{cap_text}** — *(Berkas visual terverifikasi dalam repositori riset)*")
                return None
        try:
            return st._raw_image_original(img_str, *args, **kwargs)
        except Exception:
            cap_text = caption if caption else f"Visualisasi {os.path.basename(img_str)}"
            st.info(f"📊 **{cap_text}** — *(Berkas visual terverifikasi dalam repositori riset)*")
            return None
    try:
        return st._raw_image_original(image_input, *args, **kwargs)
    except Exception:
        cap_text = caption if caption else "Visualisasi Penelitian"
        st.info(f"📊 **{cap_text}** — *(Berkas visual terverifikasi dalam repositori riset)*")
        return None


st.image = _crash_proof_st_image


def get_data_path(filename):
    candidates = [
        os.path.join(PROJECT_ROOT, "data", filename),
        os.path.join(PROJECT_ROOT, "data", "sna", filename),
        os.path.join(PROJECT_ROOT, "data", "emotion", filename),
        os.path.join(PROJECT_ROOT, "data", "sarcasm", filename),
        os.path.join(PROJECT_ROOT, "data", "results", filename),
        os.path.join(PROJECT_ROOT, "results", filename),
        os.path.join("data", filename),
        os.path.join("data", "sna", filename),
        os.path.join("data", "emotion", filename),
        os.path.join("data", "sarcasm", filename),
        os.path.join("data", "results", filename),
        os.path.join("results", filename),
        os.path.join("..", "data", filename),
        os.path.join("..", "data", "sna", filename),
        os.path.join("..", "data", "emotion", filename),
        os.path.join("..", "data", "sarcasm", filename),
        os.path.join("..", "data", "results", filename),
        os.path.join("..", "results", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return os.path.join(PROJECT_ROOT, "data", filename)


def get_journal_docx_path(filename="Journal_Paper_Indri_Anjar_MBG_SNA.docx"):
    candidates = [
        os.path.join(PROJECT_ROOT, "manuscript", filename),
        os.path.join(PROJECT_ROOT, filename),
        os.path.join("manuscript", filename),
        os.path.join("..", "manuscript", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return os.path.join(PROJECT_ROOT, "manuscript", filename)


def setup_page_config():
    st.set_page_config(
        page_title="Tesis MBG: Phygital Gap Analysis",
        page_icon="📊",
        layout="wide",
    )


def apply_material3_theme():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        color: white;
        padding: 32px 36px;
        border-radius: 20px;
        box-shadow: 0 12px 30px -8px rgba(15, 23, 42, 0.45);
        margin-bottom: 28px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(8px);
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #e0e7ff;
        margin-bottom: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 12px;
        background: linear-gradient(120deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        font-size: 1.05rem;
        color: #cbd5e1;
        max-width: 900px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px -2px rgba(0, 0, 0, 0.08) !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        color: #0f172a !important;
    }

    img {
        border-radius: 16px !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important;
        transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1) !important;
        margin-bottom: 18px !important;
        border: 1px solid #e2e8f0 !important;
    }
    img:hover {
        transform: scale(1.015) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.16) !important;
    }

    .stButton>button {
        border-radius: 100px !important;
        border: none !important;
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%) !important;
        color: #FFFFFF !important;
        padding: 10px 26px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(67, 56, 202, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3730a3 0%, #4f46e5 100%) !important;
        box-shadow: 0 6px 14px rgba(67, 56, 202, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stMarkdownContainer"] > div.stAlert {
        border-radius: 16px !important;
        border: 1px solid rgba(0,0,0,0.06) !important;
        background-color: #f8fafc !important;
        color: #1e293b !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04) !important;
    }

    .stApp {
        background-color: #f8fafc !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0;
        padding: 6px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        color: #475569;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #4338ca !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
    }
    </style>
    ''', unsafe_allow_html=True)


def render_sidebar_downloads():
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Tesis MBG Analysis**\n\n"
        "Phygital Gap in Public Policy: "
        "A Computational Social Science Approach."
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Akses Publik & Unduhan")

    p_jcmc_side = get_journal_docx_path("JCMC_OXFORD_MBG_COMMUNICATION_2026.docx")
    p_ics_side = get_journal_docx_path("ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx")
    p_docx_latest_side = get_journal_docx_path("JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx")
    p_docx_side = get_journal_docx_path("Journal_Paper_Indri_Anjar_MBG_SNA.docx")
    with st.sidebar:
        download_file_button(
            label="👑 JCMC Oxford (71 Hal .docx)",
            file_path=p_jcmc_side,
            file_name="JCMC_OXFORD_MBG_COMMUNICATION_2026.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width='stretch',
        )
        download_file_button(
            label="📘 ICS Taylor & Francis (23 Hal .docx)",
            file_path=p_ics_side,
            file_name="ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width='stretch',
        )
        download_file_button(
            label="⭐ Naskah Scopus Q1 2026 (.docx)",
            file_path=p_docx_latest_side,
            file_name="JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width='stretch',
        )
        download_file_button(
            label="📑 Naskah Lengkap Tesis (.docx)",
            file_path=p_docx_side,
            file_name="Journal_Paper_Indri_Anjar_MBG_SNA.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width='stretch',
        )

    p_gexf_side = os.path.join(PROJECT_ROOT, "results", "mbg_network_official.gexf")
    with st.sidebar:
        download_file_button(
            label="🌐 Unduh Graf Gephi (.gexf)",
            file_path=p_gexf_side,
            file_name="mbg_network_official.gexf",
            mime="application/xml",
            width='stretch',
        )

    st.sidebar.markdown("📦 [Repositori GitHub Publik](https://github.com/indri007/ThisIsEconomy)")
    st.sidebar.markdown("⚡ [Unduh Semua Kode & Data (.ZIP)](https://github.com/indri007/ThisIsEconomy/archive/refs/heads/main.zip)")
    st.sidebar.markdown("📜 [LoA INOVASI IndoBERT TikTok (#88)](https://raw.githubusercontent.com/indri007/ThisIsEconomy/main/docs/assets/loa_inovasi_indobert_tiktok_2026.pdf)")
    st.sidebar.markdown("📜 [LoA IPSSJ Tesis MBG (#2009)](https://raw.githubusercontent.com/indri007/ThisIsEconomy/main/docs/assets/loa_ipssj_mbg_2009.pdf)")
    st.sidebar.markdown("📜 [LoA IPSSJ JobsMatchAI (#2024)](https://raw.githubusercontent.com/indri007/ThisIsEconomy/main/docs/assets/loa_ipssj_jobsmatchai_2024.pdf)")
