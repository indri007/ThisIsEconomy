import pandas as pd
import torch
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df = pd.read_csv('/Users/jevin/Documents/tesis_mbg/data/results/indobert_9_emosi_fixed.csv')
df = df.dropna(subset=['processed_text', 'predicted_emotion'])

# 9 Kategori Emosi sesuai urutan id2label model checkpoint-792:
# 0: anger (Marah), 1: disgust (Jijik), 2: fear (Takut), 3: joy (Bahagia),
# 4: love (Percaya), 5: neutral (Netral), 6: sadness (Sedih), 7: shame (Tertarik), 8: surprise (Kaget)
label_map = {
    'Marah': 0,
    'Jijik': 1,
    'Takut': 2,
    'Bahagia': 3,
    'Percaya': 4,
    'Netral': 5,
    'Sedih': 6,
    'Tertarik': 7,
    'Kaget': 8
}
id2label = {v: k for k, v in label_map.items()}

df['label_id'] = df['predicted_emotion'].map(label_map)
df = df.dropna(subset=['label_id'])
df['label_id'] = df['label_id'].astype(int)

_, val_texts, _, val_labels = train_test_split(
    df['processed_text'].tolist(), 
    df['label_id'].tolist(), 
    test_size=0.2, 
    random_state=42
)

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "results", "indobert_finetuned_9_labels", "checkpoint-792")
tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
model = AutoModelForSequenceClassification.from_pretrained(model_path)

val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

class EmotionDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

val_dataset = EmotionDataset(val_encodings, val_labels)

trainer = Trainer(model=model)
predictions = trainer.predict(val_dataset)
preds = np.argmax(predictions.predictions, axis=-1)

present_labels_idx = np.unique(np.concatenate((val_labels, preds)))
target_names = [id2label[i] for i in present_labels_idx]

accuracy = accuracy_score(val_labels, preds)

precision = precision_score(
    val_labels, preds,
    average="macro",
    zero_division=0
)

recall = recall_score(
    val_labels, preds,
    average="macro",
    zero_division=0
)

f1 = f1_score(
    val_labels, preds,
    average="macro",
    zero_division=0
)

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("Macro F1 :", round(f1, 4))

print("\n=== CLASSIFICATION REPORT ===")
report = classification_report(
    val_labels,
    preds,
    labels=present_labels_idx,
    target_names=target_names,
    digits=4,
    zero_division=0,
    output_dict=True
)
print(classification_report(
    val_labels,
    preds,
    labels=present_labels_idx,
    target_names=target_names,
    digits=4,
    zero_division=0
))

# Save Confusion Matrix
cm = confusion_matrix(val_labels, preds, labels=present_labels_idx)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.xlabel('Predicted (Prediksi)')
plt.ylabel('Actual (Aktual)')
plt.title('Confusion Matrix: IndoBERT 9 Kategori Emosi (Data Riil)', fontsize=14, fontweight='bold')
plt.tight_layout()
cm_save_path = os.path.join(base_dir, "results", "confusion_matrix.png")
plt.savefig(cm_save_path, dpi=300)
plt.close()
print(f"Confusion Matrix saved to {cm_save_path}")

# Save F1-Scores Plot
f1_per_class = [report[name]['f1-score'] for name in target_names]
plt.figure(figsize=(10, 6))
bars = plt.bar(target_names, f1_per_class, color=['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#34495e'][:len(target_names)], edgecolor='black')
plt.axhline(f1, color='red', linestyle='--', label=f'Macro F1 ({f1:.4f})')
plt.axhline(report['weighted avg']['f1-score'], color='blue', linestyle=':', label=f"Weighted F1 ({report['weighted avg']['f1-score']:.4f})")
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.01, f"{yval:.4f}", ha='center', va='bottom', fontweight='bold', fontsize=10)
plt.xlabel('Kategori Emosi', fontsize=12)
plt.ylabel('F1-Score', fontsize=12)
plt.title('IndoBERT Emotion Classification Performance (F1-Scores)', fontsize=14, fontweight='bold')
plt.ylim(0, 1.05)
plt.legend()
plt.tight_layout()
f1_save_path = os.path.join(base_dir, "results", "f1_scores.png")
plt.savefig(f1_save_path, dpi=300)
plt.close()
print(f"F1 Scores plot saved to {f1_save_path}")
