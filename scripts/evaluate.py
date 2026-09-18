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

# 9 Kategori Emosi sesuai penelitian (Plutchik's Wheel — versi Indonesia)
# Dataset aktual memiliki 7 kelas yang muncul; 2 kelas (Bahagia, Kaget) hadir di skema 9 kelas
labels = ['Marah', 'Jijik', 'Takut', 'Bahagia', 'Tertarik', 'Netral', 'Percaya', 'Sedih', 'Kaget']
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

df['label_id'] = df['predicted_emotion'].map(label2id)
df = df.dropna(subset=['label_id'])
df['label_id'] = df['label_id'].astype(int)

_, val_texts, _, val_labels = train_test_split(
    df['processed_text'].tolist(), 
    df['label_id'].tolist(), 
    test_size=0.2, 
    random_state=42
)

model_path = "/Users/jevin/Documents/tesis_mbg/results/indobert_finetuned_9_labels/checkpoint-792"
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
print(classification_report(
    val_labels,
    preds,
    labels=present_labels_idx,
    target_names=target_names,
    digits=4,
    zero_division=0
))

cm = confusion_matrix(val_labels, preds, labels=present_labels_idx)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix: IndoBERT 9 Emotions')
plt.savefig('/Users/jevin/Documents/tesis_mbg/results/confusion_matrix.png')
print("Confusion Matrix saved to /Users/jevin/Documents/tesis_mbg/results/confusion_matrix.png")
