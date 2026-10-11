import os
import sys
import pandas as pd

# Ensure working directory is project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from scripts.data_utils import get_data_path
except ImportError:
    from data_utils import get_data_path

file_path = get_data_path("indobert_9_emosi_fixed.csv")
df = pd.read_csv(file_path)

# ==============================================================================
# AUDIT & METODOLOGIS NOTE (Scopus Q1 & Komite Disertasi):
# Pemetaan 'love' -> 'Percaya' dan 'shame' -> 'Tertarik' adalah translasi ad-hoc
# heuristik awal dalam repositori. Secara taksonomi psikologi formal (Plutchik, Ekman):
# - 'Love' (Cinta/Kasih) TIDAK identik dengan 'Trust' (Percaya/Kepercayaan).
# - 'Shame' (Malu/Aib) adalah emosi negatif kesadaran-diri, sedangkan 'Tertarik'
#   (Interest/Antisipasi) adalah emosi positif/eksploratif berorientasi pendekatan.
# Dalam publikasi ilmiah, diskrepansi ini WAJIB dilaporkan secara transparan
# sebagai batasan leksikal pra-anotasi silver standard.
# ==============================================================================
mapping = {
    'anger': 'Marah',
    'disgust': 'Jijik',
    'fear': 'Takut',
    'sadness': 'Sedih',
    'joy': 'Bahagia/Senang',
    'neutral': 'Netral',
    'surprise': 'Kaget',
    'love': 'Percaya',      # Ad-hoc proxy: afeksi/afiliasi publik dipetakan ke persepsi kepercayaan
    'shame': 'Tertarik'     # Ad-hoc proxy: keheranan/kejanggalan dipetakan ke keingintahuan wacana
}

if 'predicted_emotion' in df.columns:
    df['predicted_emotion'] = df['predicted_emotion'].str.lower().map(mapping).fillna(df['predicted_emotion'])
    df.to_csv(file_path, index=False)
    print("Labels updated successfully in CSV.")
else:
    print("Column predicted_emotion not found!")

