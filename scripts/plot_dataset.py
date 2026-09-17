import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Create results folder if it doesn't exist
os.makedirs("results", exist_ok=True)

# Updated Dataset Characteristics based on the thesis numbers
labels = [
    'Raw Scraped Data\n(via Twitter API)', 
    'After Cleaning\n(Removed: Spam, Bots, Duplicates)', 
    'Final Annotated\n(Ready for NLP)'
]
counts = [5310, 4300, 3395]

plt.figure(figsize=(10, 7))
# Plot using seaborn barplot
sns.barplot(x=counts, y=labels, hue=labels, palette="Blues_r", legend=False)

plt.title("Gambar 2: Dataset Characteristics & Preprocessing Funnel", fontsize=14, fontweight='bold', pad=20)
plt.xlabel("Number of Tweets", fontsize=12, labelpad=10)
plt.ylabel("Processing Stage", fontsize=12)
plt.yticks(fontsize=11)

# Add text labels on bars
for index, value in enumerate(counts):
    plt.text(value - 450, index, f"{value} tweets", color='white', fontweight='bold', fontsize=11, va='center')

# Make room for the text box below the plot
plt.subplots_adjust(bottom=0.3)

# Add an explanatory text box about cleaning factors WITH EXAMPLES
cleaning_factors = (
    "Data Cleaning Factors & Examples:\n"
    "• Bot Removal: Menghapus akun otomatis (misal: aktivitas spam 100+ tweet/hari)\n"
    "• Spam Filtering: Membuang tautan promosi (misal: link judi online/iklan)\n"
    "• De-duplication: Menghilangkan cuitan duplikat (misal: Retweet otomatis)\n"
    "• Text Cleansing: Memotong simbol non-semantik (misal: @user, #MBG, https://...)"
)
plt.figtext(0.5, 0.05, cleaning_factors, wrap=True, horizontalalignment='center', fontsize=11, 
            bbox={"facecolor":"#f0f0f0", "alpha":0.8, "pad":8, "boxstyle":"round,pad=0.5"})

plt.savefig("results/2_dataset_characteristics.png", dpi=300, bbox_inches="tight")
plt.close()
print("Gambar 2 berhasil diupdate dan dirapikan!")
