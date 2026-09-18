import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Ensure root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from scripts.data_utils import get_result_path
except ImportError:
    from data_utils import get_result_path

# Visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(16, 9), facecolor='#0F172A')

# Grid layout: Left = Radar Chart (Coverage vs Boundary), Right = 5 Limitations Detailed Cards
gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.4], wspace=0.25, left=0.06, right=0.95, top=0.88, bottom=0.08)

# ── 1. RADAR CHART (Kiri) ────────────────────────────────────────────────────
ax_radar = fig.add_subplot(gs[0, 0], polar=True, facecolor='#1E293B')

categories = [
    'Kedalaman NLP Emosi\n(9 Kelas IndoBERT)',
    'Topologi Jaringan SNA\n(Louvain Modularity)',
    'Triangulasi Phygital\n(Marketing 6.0)',
    'Multimodalitas\n(Teks + Visi Komputer)',
    'Multi-Platform\n(X + TikTok + IG)',
    'Horizon Temporal\n(Studi Longitudinal)',
    'Representasi Wilayah\n(Rural 3T Non-Digital)'
]
N = len(categories)

# Nilai capaian tesis (100 skala)
thesis_scores = [95, 92, 90, 20, 25, 35, 30]
# Horizon ideal teoritis
full_horizon = [100, 100, 100, 100, 100, 100, 100]

angles = [n / float(N) * 2 * np.pi for n in range(N)]
thesis_scores_plot = thesis_scores + [thesis_scores[0]]
full_horizon_plot = full_horizon + [full_horizon[0]]
angles_plot = angles + [angles[0]]

# Plot Radar
ax_radar.plot(angles_plot, full_horizon_plot, linewidth=1.5, linestyle='--', color='#94A3B8', alpha=0.5, label='Batas Horizon Ideal (Komprehensif Penuh)')
ax_radar.fill(angles_plot, full_horizon_plot, color='#94A3B8', alpha=0.05)

ax_radar.plot(angles_plot, thesis_scores_plot, linewidth=2.8, color='#38BDF8', marker='o', markersize=6, label='Cakupan Metodologis Tesis Ini')
ax_radar.fill(angles_plot, thesis_scores_plot, color='#0284C7', alpha=0.35)

ax_radar.set_theta_offset(np.pi / 2)
ax_radar.set_theta_direction(-1)
ax_radar.set_xticks(angles)
ax_radar.set_xticklabels(categories, size=9.5, color='#F8FAFC', fontweight='600')
ax_radar.set_rlabel_position(0)
ax_radar.set_yticks([25, 50, 75, 100])
ax_radar.set_yticklabels(['25%', '50%', '75%', '100%'], color='#94A3B8', size=8)
ax_radar.set_ylim(0, 105)
ax_radar.grid(color='#334155', linestyle=':')
ax_radar.tick_params(colors='#94A3B8')

legend = ax_radar.legend(loc='upper right', bbox_to_anchor=(0.1, -0.05), frameon=True, facecolor='#1E293B', edgecolor='#475569', labelcolor='#F8FAFC', fontsize=9)

ax_radar.set_title("A. Profil Cakupan Riset vs Batas Keterbatasan Metodologis", fontsize=12, fontweight='bold', color='#38BDF8', pad=25)


# ── 2. CARDS / MATRIKS KETERBATASAN (Kanan) ──────────────────────────────────
ax_cards = fig.add_subplot(gs[0, 1])
ax_cards.set_facecolor('#0F172A')
ax_cards.axis('off')

limitations = [
    {
        "num": "01",
        "title": "Single-Platform Boundary Bias (Platform X)",
        "desc": "Korpus bertumpu pada X/Twitter (N=5.263). Belum mengikutsertakan TikTok, Facebook, atau Instagram yang memiliki penetrasi tinggi di kalangan wali murid akar rumput.",
        "mitigation": "Mitigasi: Algoritma IndoBERT p-2 dioptimasi leksikon kasual & verifikasi volume 3.395 interaksi.",
        "future": "Riset Lanjut: Cross-platform social listening multikanal."
    },
    {
        "num": "02",
        "title": "Unimodalitas Teks (Text-Only NLP)",
        "desc": "Analisis berfokus pada konten tekstual cuitan warganet dan belum mencakup Computer Vision (CV) untuk memvalidasi visual foto menu makanan/piring MBG secara faktual.",
        "mitigation": "Mitigasi: Triangulasi ABSA tematik (Gizi, Distribusi, Vendor) dari teks laporan terperinci.",
        "future": "Riset Lanjut: Multimodal Vision-Language Transformer (CLIP / LLaVA)."
    },
    {
        "num": "03",
        "title": "Snapshot Temporal (Maret – Mei 2026)",
        "desc": "Observasi bersifat cross-sectional pada periode krisis awal (pemangkasan anggaran & insiden basi). Belum mengukur fase normalisasi pasca-standardisasi SPPG.",
        "mitigation": "Mitigasi: Analisis longitudinal mikro per hari mencakup puncak anomali viral.",
        "future": "Riset Lanjut: Studi longitudinal time-series berkala 12–24 bulan."
    },
    {
        "num": "04",
        "title": "Sarkasme Vernakular & Nuansa Budaya",
        "desc": "Gaya bertutur warganet Indonesia sarat satir halus dan metafora lokal yang menantang pemisahan absolut antara Disgust, Anger, dan Sarcasm.",
        "mitigation": "Mitigasi: Integrasi kamus sindiran 3.395 entri & validasi confusion matrix Macro F1 0.8122.",
        "future": "Riset Lanjut: Model pragmatik berbasis culturally-aware LLM reasoning."
    },
    {
        "num": "05",
        "title": "Sampling Representativeness (Rural 3T Bias)",
        "desc": "Warganet platform X cenderung terkonsentrasi di daerah urban. Suara penerima manfaat di daerah 3T (Tertinggal, Terdepan, Terluar) belum terwakili proporsional.",
        "mitigation": "Mitigasi: Analisis diarahkan pada pengawasan kebijakan makro nasional & transparansi anggaran.",
        "future": "Riset Lanjut: Field survey hibrida tatap muka digabung SNA digital."
    }
]

y_start = 0.96
card_height = 0.17
spacing = 0.025

for i, lim in enumerate(limitations):
    y_pos = y_start - (i * (card_height + spacing))
    
    # Card Background
    card = FancyBboxPatch((0.02, y_pos - card_height), 0.96, card_height,
                          boxstyle="round,pad=0.015,rounding_size=0.02",
                          facecolor='#1E293B', edgecolor='#334155', linewidth=1.2,
                          transform=ax_cards.transAxes)
    ax_cards.add_patch(card)
    
    # Number badge
    badge = FancyBboxPatch((0.04, y_pos - 0.05), 0.08, 0.04,
                           boxstyle="round,pad=0.01,rounding_size=0.01",
                           facecolor='#0284C7', edgecolor='none',
                           transform=ax_cards.transAxes)
    ax_cards.add_patch(badge)
    ax_cards.text(0.08, y_pos - 0.03, lim["num"], color='#FFFFFF', fontsize=9, fontweight='bold',
                  ha='center', va='center', transform=ax_cards.transAxes)
    
    # Title
    ax_cards.text(0.14, y_pos - 0.03, lim["title"], color='#F8FAFC', fontsize=10.5, fontweight='bold',
                  ha='left', va='center', transform=ax_cards.transAxes)
    
    # Description
    ax_cards.text(0.04, y_pos - 0.085, lim["desc"], color='#CBD5E1', fontsize=8.5,
                  ha='left', va='top', wrap=True, transform=ax_cards.transAxes)
    
    # Mitigation & Future
    ax_cards.text(0.04, y_pos - 0.125, f"[Mitigasi Tesis] {lim['mitigation']}", color='#38BDF8', fontsize=7.8,
                  fontstyle='italic', ha='left', va='top', transform=ax_cards.transAxes)
    ax_cards.text(0.04, y_pos - 0.152, f"[Agenda Riset] {lim['future']}", color='#34D399', fontsize=7.8,
                  fontweight='600', ha='left', va='top', transform=ax_cards.transAxes)

ax_cards.set_title("B. Taksonomi 5 Keterbatasan Penelitian, Mitigasi Empiris & Arah Riset Lanjutan",
                   fontsize=12, fontweight='bold', color='#38BDF8', pad=15, loc='left')

# Global Header
fig.suptitle("BAB V: KETERBATASAN PENELITIAN (RESEARCH LIMITATIONS) & AGENDA RISET MASA DEPAN",
             fontsize=14, fontweight='bold', color='#F8FAFC', y=0.97)

# Save
out_path = get_result_path("keterbatasan_penelitian.png")
plt.savefig(out_path, dpi=300, facecolor='#0F172A', edgecolor='none')
plt.close()
print(f"[OK] Visualisasi Keterbatasan Penelitian berhasil disimpan di: {out_path}")
