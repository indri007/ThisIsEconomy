import os
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import GroupShuffleSplit

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
train_df = pd.read_csv(os.path.join(base_dir, "results", "emotion_train_group_split.csv"))
test_df = pd.read_csv(os.path.join(base_dir, "results", "emotion_test_group_split.csv"))

label_to_id = {
    'Marah': 0, 'Jijik': 1, 'Takut': 2, 'Bahagia': 3,
    'Percaya': 4, 'Netral': 5, 'Sedih': 6, 'Tertarik': 7, 'Kaget': 8
}
id_to_label = {v: k for k, v in label_to_id.items()}

train_df['label_id'] = train_df['predicted_emotion'].map(label_to_id)
test_df['label_id'] = test_df['predicted_emotion'].map(label_to_id)

tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
train_encodings = tokenizer(train_df['processed_text'].tolist(), truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_df['processed_text'].tolist(), truncation=True, padding=True, max_length=128)

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_encodings, train_df['label_id'].tolist())
test_dataset = Dataset(test_encodings, test_df['label_id'].tolist())

model = AutoModelForSequenceClassification.from_pretrained(
    "indobenchmark/indobert-base-p2",
    num_labels=9,
    id2label=id_to_label,
    label2id=label_to_id
)

training_args = TrainingArguments(
    output_dir=os.path.join(base_dir, "results", "indobert_group_aware_final"),
    num_train_epochs=3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    seed=42,
    logging_steps=50,
    save_strategy="epoch",
    eval_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

print("Starting group-aware fine-tuning...")
trainer.train()
trainer.save_model(os.path.join(base_dir, "results", "indobert_group_aware_final", "best_model"))
print("Retraining completed successfully!")
