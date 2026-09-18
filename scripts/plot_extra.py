import os
import sys

# Ensure working directory is project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if os.getcwd() != PROJECT_ROOT:
    os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

os.makedirs(get_result_path(""), exist_ok=True)

# 1. Plot Emotion Distribution
print("Generating Emotion Distribution...")
df_emotion = pd.read_csv(get_data_path("indobert_9_emosi_fixed.csv"))
emotion_counts = df_emotion['predicted_emotion'].value_counts().reset_index()
emotion_counts.columns = ['Emotion', 'Count']

all_emotions = ['Marah', 'Jijik', 'Takut', 'Sedih', 'Bahagia/Senang', 'Netral', 'Percaya', 'Kaget', 'Tertarik']
missing = set(all_emotions) - set(emotion_counts['Emotion'])
if missing:
    missing_df = pd.DataFrame({'Emotion': list(missing), 'Count': 0})
    emotion_counts = pd.concat([emotion_counts, missing_df], ignore_index=True)
emotion_counts = emotion_counts.sort_values(by='Count', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Emotion', y='Count', data=emotion_counts, hue='Emotion', palette="viridis", legend=False)
plt.title("Distribusi 9 Kelas Emosi (IndoBERT)", fontsize=14, fontweight='bold')
plt.xlabel("Kategori Emosi", fontsize=12)
plt.ylabel("Jumlah Cuitan", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(get_result_path("emotion_distribution.png"), dpi=300)
plt.close()

