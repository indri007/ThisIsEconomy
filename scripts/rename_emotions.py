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

mapping = {
    'anger': 'Marah',
    'disgust': 'Jijik',
    'fear': 'Takut',
    'sadness': 'Sedih',
    'joy': 'Bahagia/Senang',
    'neutral': 'Netral',
    'surprise': 'Kaget',
    'love': 'Percaya',      
    'shame': 'Tertarik'     
}

if 'predicted_emotion' in df.columns:
    df['predicted_emotion'] = df['predicted_emotion'].str.lower().map(mapping).fillna(df['predicted_emotion'])
    df.to_csv(file_path, index=False)
    print("Labels updated successfully in CSV.")
else:
    print("Column predicted_emotion not found!")

