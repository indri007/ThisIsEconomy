import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("results", exist_ok=True)

# 1. Plot Emotion Distribution
print("Generating Emotion Distribution...")
df_emotion = pd.read_csv("data/results/indobert_9_emosi_fixed.csv")
emotion_counts = df_emotion['predicted_emotion'].value_counts().reset_index()
emotion_counts.columns = ['Emotion', 'Count']

plt.figure(figsize=(10, 6))
sns.barplot(x='Emotion', y='Count', data=emotion_counts, hue='Emotion', palette="viridis", legend=False)
plt.title("Distribusi 9 Kelas Emosi (IndoBERT)", fontsize=14, fontweight='bold')
plt.xlabel("Kategori Emosi", fontsize=12)
plt.ylabel("Jumlah Cuitan", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/emotion_distribution.png", dpi=300)
plt.close()

