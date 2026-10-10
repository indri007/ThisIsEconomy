# BIT_CANONICAL_EWS_PATH
import sys
from pathlib import Path

_BIT_ROOT = Path(__file__).resolve().parents[1]
if str(_BIT_ROOT) not in sys.path:
    sys.path.insert(0, str(_BIT_ROOT))
# END BIT_CANONICAL_EWS_PATH

import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    try:
        _current_loop = asyncio.get_event_loop()
    except RuntimeError:
        _current_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_current_loop)

# Prevent NoEventLoopError on Python 3.14 / Starlette staticfiles in AnyIO
try:
    import sniffio
    _orig_sniffio_current = sniffio.current_async_library

    def _safe_sniffio_current() -> str:
        try:
            return _orig_sniffio_current()
        except Exception:
            return "asyncio"

    sniffio.current_async_library = _safe_sniffio_current
except Exception:
    pass

try:
    import anyio._core._eventloop as _anyio_el
    _orig_get_async_backend = _anyio_el.get_async_backend

    def _safe_get_async_backend(asynclib_name=None):
        try:
            return _orig_get_async_backend(asynclib_name)
        except Exception:
            return _orig_get_async_backend("asyncio")

    _anyio_el.get_async_backend = _safe_get_async_backend
except Exception:
    pass

import streamlit as st

# Import Modular Dashboard Modules
from dashboard.modules.config import (
    setup_page_config,
    apply_material3_theme,
    render_sidebar_downloads,
)
from dashboard.modules.ui_components import (
    render_submission_checklist_70_points,
    render_author_biography,
    render_downloads_footer,
)
from dashboard.modules.views_bab1 import render_bab1_page
from dashboard.modules.views_bab2 import render_bab2_page
from dashboard.modules.views_bab3 import render_bab3_page
from dashboard.modules.views_bab4 import render_bab4_page
from dashboard.modules.views_bab5 import render_bab5_page
from dashboard.modules.views_storytelling import render_storytelling_page
from dashboard.modules.views_audit import render_audit_page
from dashboard.modules.views_ews import (
    render_journal_page,
    render_twitter_ai_page,
    render_big_data_page,
    render_ews_page,
    render_brand24_page,
)

# 1. Page Configuration & Theme
setup_page_config()
apply_material3_theme()

# 2. Sidebar Navigation
st.sidebar.title("🧭 Navigasi Manuskrip Tesis")
st.sidebar.markdown("**Alur Pembacaan Berurutan (Bab I – Bab V):**")

menu_options = [
    "1️⃣ Bab I: Pendahuluan & 6 Rumusan Masalah",
    "2️⃣ Bab II: Landasan Teori & Tinjauan Pustaka",
    "3️⃣ Bab III: Metodologi & Pipeline Komputasional",
    "4️⃣ Bab IV: Hasil & Pembahasan (Empiris Terintegrasi)",
    "5️⃣ Bab V: Kesimpulan & Rekomendasi Kebijakan BGN",
    "📊 Tabel Dataset MBG",
    "🚨 Custom Early Warning System (EWS) v2",
    "🍱 Twitter AI & Scraper Monitor",
    "📡 Brand24 Real-Time Monitor (EWS)",
    "📑 Naskah Jurnal Internasional (Indonesia Emas Ready)",
    "🖼️ Galeri Visual Storytelling (10 Master Plot Tesis)",
    "📚 Audit Integritas Data & Referensi Scopus",
    "🎯 Checklist Submit Indonesia Emas (70 Poin)",
    "👤 Profil Peneliti & AI Engineer"
]

page = st.sidebar.radio("Pilih Bab / Modul:", menu_options, index=0)

# Sidebar download shortcuts
render_sidebar_downloads()

# 3. Dynamic Page Routing
if page.startswith("1️⃣") or page == "🏠 Beranda":
    render_bab1_page()
elif page.startswith("2️⃣") or "Bab II" in page or "Landasan Teori" in page:
    render_bab2_page()
elif page.startswith("3️⃣") or "Bab III" in page or "Metodologi" in page:
    render_bab3_page()
elif page.startswith("4️⃣") or "Bab IV" in page or "Analisis Emosi" in page or "Analisis Jaringan" in page or "Hasil & Pembahasan" in page:
    render_bab4_page()
elif page.startswith("5️⃣") or "Bab V" in page or "Kesimpulan" in page:
    render_bab5_page()
elif "Tabel Dataset MBG" in page or "Big Data MBG" in page:
    render_big_data_page()
elif "Custom Early Warning System" in page or "Custom EWS" in page:
    render_ews_page()
elif "Twitter AI" in page:
    render_twitter_ai_page()
elif "Brand24" in page:
    render_brand24_page()
elif "Naskah Jurnal" in page:
    render_journal_page()
elif "Visual Storytelling" in page or "Galeri" in page:
    render_storytelling_page()
elif "Audit Integritas Data" in page:
    render_audit_page()
elif "Checklist Submit" in page:
    render_submission_checklist_70_points()
elif "Profil Peneliti" in page:
    render_author_biography()

# 4. Centralized Downloads Footer
render_downloads_footer()
