import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Simulate Dataset Characteristics based on the thesis numbers
labels = ['Raw Crawled Data', 'After Cleaning (Spam/Bot Removal)', 'Final Annotated for NLP']
counts = [10500, 5200, 3395]

plt.figure(figsize=(8, 5))
sns.barplot(x=counts, y=labels, palette="Blues_r")
plt.title("Gambar 2: Dataset Characteristics & Preprocessing Funnel", fontsize=12, fontweight='bold')
plt.xlabel("Number of Tweets", fontsize=11)
plt.ylabel("Processing Stage", fontsize=11)

# Add text labels on bars
for index, value in enumerate(counts):
    plt.text(value - 800, index, str(value), color='white', fontweight='bold', va='center')

plt.tight_layout()
plt.savefig("results/2_dataset_characteristics.png", dpi=300)
plt.close()
