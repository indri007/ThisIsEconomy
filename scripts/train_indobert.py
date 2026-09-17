import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

print("1. Load Dataset berlabel...")
df = pd.read_csv('/Users/jevin/Documents/tesis_mbg/data/results/indobert_9_emosi_fixed.csv')
df = df.dropna(subset=['processed_text', 'predicted_emotion'])

print("2. Encode Labels...")
labels = ['anger', 'disgust', 'fear', 'joy', 'love', 'neutral', 'sadness', 'shame', 'surprise']
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

df['label_id'] = df['predicted_emotion'].map(label2id)
df = df.dropna(subset=['label_id'])
df['label_id'] = df['label_id'].astype(int)

print(f"Menggunakan {len(labels)} label: {labels}")

print("3. Train-Test Split...")
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['processed_text'].tolist(), 
    df['label_id'].tolist(), 
    test_size=0.2, 
    random_state=42
)

print("4. Tokenizer IndoBERT...")
model_name = "indolem/indobert-base-uncased"
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
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)

print("7. Training Arguments...")
training_args = TrainingArguments(
    output_dir='/Users/jevin/Documents/tesis_mbg/results/indobert_finetuned_9_labels',
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

print("8. Eksekusi Fine-tuning...")
trainer.train()
print("Training selesai!")
