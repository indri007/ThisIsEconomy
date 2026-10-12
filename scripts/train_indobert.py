import pandas as pd
import torch
from sklearn.model_selection import GroupShuffleSplit
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
try:
    from scripts.data_utils import get_data_path, get_result_path
except ImportError:
    from data_utils import get_data_path, get_result_path

print("1. Load Dataset berlabel (Silver-standard reference annotations)...")
data_path = get_data_path("indobert_9_emosi_fixed.csv")
df = pd.read_csv(data_path)
df = df.dropna(subset=['processed_text', 'predicted_emotion'])

print("2. Encode Labels (Silver-standard reference labels)...")
ID_TO_LABEL = {
    0: 'Marah', 1: 'Jijik', 2: 'Takut', 3: 'Bahagia',
    4: 'Percaya', 5: 'Netral', 6: 'Sedih', 7: 'Tertarik', 8: 'Kaget'
}
LABEL_TO_ID = {v: k for k, v in ID_TO_LABEL.items()}
LABEL_TO_ID.update({
    'anger': 0, 'disgust': 1, 'fear': 2, 'joy': 3,
    'love': 4, 'neutral': 5, 'sadness': 6, 'shame': 7, 'surprise': 8
})
id2label = ID_TO_LABEL
label2id = {v: k for k, v in ID_TO_LABEL.items()}

# Catatan Metodologis: Korpus empiris memuat 6 kelas aktif (joy=0, surprise=0, fear=2).
df['label_id'] = df['predicted_emotion'].map(LABEL_TO_ID)
df = df.dropna(subset=['label_id'])
df['label_id'] = df['label_id'].astype(int)

print(f"Skema target 9 kelas: {list(ID_TO_LABEL.values())}")
print(f"Distribusi kelas empiris: {dict(df['predicted_emotion'].value_counts())}")

print("3. Group-Aware Split (Protocol v2: GroupShuffleSplit, random_state=42, test_size=0.2)...")
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, val_idx = next(gss.split(df, groups=df['processed_text']))
train_df = df.iloc[train_idx]
val_df = df.iloc[val_idx]

train_texts = train_df['processed_text'].tolist()
val_texts = val_df['processed_text'].tolist()
train_labels = train_df['label_id'].tolist()
val_labels = val_df['label_id'].tolist()

# Verifikasi programatik zero leakage
overlap = set(train_texts).intersection(set(val_texts))
assert len(overlap) == 0, f"Critical Data Leakage: Terdeteksi {len(overlap)} teks duplikat antara train dan val!"
print(f"✓ Zero Leakage Terverifikasi: overlap = {len(overlap)} teks (Train: {len(train_texts)}, Val: {len(val_texts)})")

print("4. Tokenizer IndoBERT...")
model_name = "indobenchmark/indobert-base-p2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

print("5. Custom Dataset Class...")
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

train_dataset = EmotionDataset(train_encodings, train_labels)
val_dataset = EmotionDataset(val_encodings, val_labels)

print("6. Inisialisasi Model...")
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=len(ID_TO_LABEL),
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)

print("7. Training Arguments...")
training_args = TrainingArguments(
    output_dir=os.path.join(base_dir, 'results', 'indobert_finetuned_9_labels'),
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=50,
    eval_strategy="epoch",
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

if __name__ == "__main__":
    print("8. Eksekusi Fine-tuning...")
    trainer.train()
    print("Training selesai!")
