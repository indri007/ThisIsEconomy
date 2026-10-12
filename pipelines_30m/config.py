"""
pipelines_30m/config.py
=======================
Konfigurasi terisolasi untuk pipeline pra-pemrosesan data 30 Juta (tweet_mbg_1juta.csv).
Pipeline ini sepenuhnya terpisah dari artefak dan data tesis utama.
"""

from pathlib import Path
import os
from nltk.corpus import stopwords

# --- PATH & FILE DEFINITIONS ---
BASE_DIR = Path(__file__).resolve().parent

# File sumber data besar (6.0 GB)
DEFAULT_INPUT_CSV = Path("/Users/jevin/Documents/tesis_mbg/data/processed/tweet_mbg_1juta.csv")

# Direktori output terpisah (di luar artefak tesis utama)
DEFAULT_OUTPUT_DIR = Path("/Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output")

# Berkas log progres & checkpoint
DEFAULT_PROGRESS_FILE = DEFAULT_OUTPUT_DIR / "progress_checkpoint.json"

# --- COMPUTATIONAL DEFAULTS ---
DEFAULT_CHUNK_SIZE = 50_000
DEFAULT_N_WORKERS = max(1, (os.cpu_count() or 4) - 2)  # Sisakan 2 core untuk OS

# --- KAMUS NORMALISASI (SESUAI ATURAN TESIS) ---
NORM_DICT = {
    "yg": "yang",
    "dgn": "dengan",
    "bgmn": "bagaimana",
    "bgt": "banget",
    "tp": "tapi",
    "dri": "dari",
    "krn": "karena",
    "klo": "kalau",
    "sma": "sama",
    "utk": "untuk",
    "udah": "sudah"
}

# --- STOPWORDS (SESUAI ATURAN TESIS) ---
TAMBAHAN_STOPWORDS = ["sih", "nya", "nih", "tuh", "dong", "yg", "di", "ke", "dari"]

def get_stopwords_set():
    words = set(stopwords.words("indonesian"))
    words.update(TAMBAHAN_STOPWORDS)
    return words
