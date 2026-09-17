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

plt.figure(figsize=(10, 6))
# Plot using seaborn barplot
sns.barplot(x=counts, y=labels, hue=labels, palette="Blues_r", legend=False)

plt.title("Gambar 2: Dataset Characteristics & Preprocessing Funnel", fontsize=14, fontweight='bold', pad=20)
plt.xlabel("Number of Tweets", fontsize=12)
plt.ylabel("Processing Stage", fontsize=12)
plt.yticks(fontsize=11)

# Add text labels on bars
for index, value in enumerate(counts):
    plt.text(value - 450, index, f"{value} tweets", color='white', fontweight='bold', fontsize=11, va='center')

# Add an explanatory text box about cleaning factors
cleaning_factors = (
    "Data Cleaning Factors:\n"
    "• Removal of automated Bot accounts\n"
    "• Filtering out spam / promotional links\n"
    "• De-duplication of identical texts\n"
    "• Stripping URLs, mentions (@), and hashtags (#)"
)
plt.figtext(0.5, -0.05, cleaning_factors, wrap=True, horizontalalignment='center', fontsize=10, 
            bbox={"facecolor":"#f0f0f0", "alpha":0.5, "pad":5, "boxstyle":"round,pad=0.5"})

plt.tight_layout()
plt.savefig("results/2_dataset_characteristics.png", dpi=300, bbox_inches="tight")
plt.close()
print("Gambar 2 berhasil diupdate!")
