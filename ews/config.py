"""
ews/config.py
=============
Konfigurasi terpusat untuk Custom Early Warning System (EWS) v2.
Mengunci jalur dataset, metadata model IndoBERT, dan parameter ambang batas.

ATURAN METODOLOGIS TESIS:
- Dataset IndoBERT memiliki 7 label output aktual dari hasil fine-tuning
  ('Marah', 'Jijik', 'Takut', 'Percaya', 'Netral', 'Sedih', 'Tertarik').
- Label 'Tertarik' berasal dari kelas 'shame' pada model asli dan TIDAK BOLEH
  diubah menjadi emosi lain tanpa bukti pelatihan ulang.
- SNA mencakup 971 simpul aktor dan 342 komunitas (Modularity Q=0.9837).
- Seluruh metrik berbasis dataset historis empiris (bukan prediksi kausal real-time).
"""

from __future__ import annotations
import os
from pathlib import Path

# Jalur Basis Proyek
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Jalur Dataset Terpusat
DATA_PATHS = {
    # 1. Dataset Emosi IndoBERT (5.263 tweet)
    "emotion": PROJECT_ROOT / "data" / "results" / "indobert_9_emosi_fixed.csv",
    # 2. Dataset SNA Simpul Jaringan (971 nodes, 342 komunitas)
    "sna_nodes": PROJECT_ROOT / "data" / "results" / "mbg_network_nodes_final.csv",
    # 3. Dataset SNA Sisi Jaringan (666 edges)
    "sna_edges": PROJECT_ROOT / "data" / "results" / "mbg_network_edges_final.csv",
    # 4. Dataset Sarkasme / Sindiran Valid (3.395 baris)
    "sarcasm": PROJECT_ROOT / "data" / "sarcasm" / "dataset_sindiran_valid.csv",
}

# Metadata Model IndoBERT Fine-Tuned (7 Kelas Aktual)
INDOBERT_MODEL_METADATA = {
    "num_actual_labels": 7,
    "actual_labels": [
        "Jijik",
        "Percaya",
        "Netral",
        "Tertarik",
        "Marah",
        "Sedih",
        "Takut",
    ],
    "negative_risk_labels": ["Jijik", "Marah", "Takut", "Sedih"],
    "constructive_neutral_labels": ["Percaya", "Netral", "Tertarik"],
    "label_color_palette": {
        "Jijik": "#E11D48",      # Rose red
        "Percaya": "#059669",    # Emerald green
        "Netral": "#64748B",     # Slate gray
        "Tertarik": "#2563EB",   # Royal blue
        "Marah": "#DC2626",      # Bright red
        "Sedih": "#D97706",      # Amber
        "Takut": "#7C3AED",      # Violet
    },
    "note": (
        "Dataset hasil inferensi IndoBERT memiliki 7 kelas aktual "
        "('Jijik', 'Percaya', 'Netral', 'Tertarik', 'Marah', 'Sedih', 'Takut'). "
        "Label dipertahankan secara jujur sesuai konfigurasi model."
    )
}

# Parameter Ambang Batas Skor EWS (0 - 100)
EWS_SCORE_LEVELS = [
    {"range": (0, 24),   "status": "SAFE",     "label": "🟢 AMAN",     "color": "#10B981"},
    {"range": (25, 49),  "status": "WARNING",  "label": "🟡 WASPADA",  "color": "#F59E0B"},
    {"range": (50, 74),  "status": "DANGER",   "label": "🟠 BAHAYA",   "color": "#F97316"},
    {"range": (75, 100), "status": "CRITICAL", "label": "🔴 KRITIS",   "color": "#EF4444"},
]

# Bobot Komponen EWS v2 (Total Maksimum = 100 Poin)
EWS_WEIGHTS = {
    "emotion_risk": 30.0,    # Rasio emosi krisis (Jijik + Marah + Takut + Sedih)
    "sarcasm_risk": 20.0,    # Rasio sindiran/sarkasme empiris
    "keyword_risk": 20.0,    # Bobot kata kunci krisis bertingkat + emoji sinis
    "volume_risk": 15.0,     # Deviasi volume dari rata-rata baseline
    "anomaly_risk": 15.0,    # Lonjakan z-score harian (z >= 2.0)
}

# Kamus Kata Kunci Krisis Bertingkat (MBG Context)
CRISIS_KEYWORDS = {
    "tier1": [
        "keracunan", "dirawat", "pingsan", "masuk rs", "mati", "meninggal",
        "ambulans", "rumah sakit", "opname", "gawat darurat", "muntah", "diare"
    ],
    "tier2": [
        "basi", "busuk", "belatung", "ulat", "kotor", "menjijikkan", "korupsi",
        "fiktif", "vendor bodong", "vendor fiktif", "dihentikan", "ditutup",
        "dibekukan", "ditangguhkan", "sppg"
    ],
    "tier3": [
        "kecewa", "malu", "gagal", "bohong", "janji", "tidak sesuai", "kurang",
        "tidak layak", "tidak bergizi", "tidak enak", "hambar", "tipuan",
        "kebohongan", "omong kosong", "harapan palsu", "anggaran bengkak"
    ],
}

# Emoji Sarkasme & Penanda Pragmatik
SARCASM_EMOJIS = [
    "🤡", "🙃", "🤮", "🤢", "😒", "😑", "😤", "🤬",
    "💀", "☠️", "🗑️", "🚮", "👎", "🤦", "😅", "🙄"
]

FAKE_POSITIVE_EMOJIS = [
    "😍", "🥰", "👍", "🎉", "✨", "🌟", "❤️", "🥺", "😊"
]
