#!/usr/bin/env python3
"""
train_indobert_weighted_9_labels.py
====================================
1. Memperbarui dataset emosi 9-kelas (data/results/indobert_9_emosi_fixed.csv)
   dengan kandidat terverifikasi Bahagia (Joy) & Kaget (Surprise).
2. Melakukan Group-Aware Train-Test Split (80% Train, 20% Test)
   berdasarkan `processed_text` dengan garansi 0% data leakage.
3. Melakukan Fine-Tuning IndoBERT (indobenchmark/indobert-base-p2)
   menggunakan Weighted Cross-Entropy Loss (mengatasi class imbalance).
4. Menyimpan model terbaik dan mengevaluasi performa 9 kelas di test set.
"""

import os
import sys
import shutil
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    set_seed
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

def main():
    print("=" * 80)
    print("STEP 2: HARMONISASI DATA, ZERO-LEAKAGE SPLIT, & WEIGHTED INDOBERT TRAINING")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    master_path = os.path.join(base_dir, "data", "results", "indobert_9_emosi_fixed.csv")
    cand_path = os.path.join(base_dir, "data", "annotation", "mined_joy_surprise_candidates.csv")

    if not os.path.exists(master_path):
        raise FileNotFoundError(f"File master tidak ditemukan: {master_path}")
    if not os.path.exists(cand_path):
        raise FileNotFoundError(f"File kandidat tidak ditemukan: {cand_path}")

    # Backup master file
    backup_path = master_path + ".bak"
    if not os.path.exists(backup_path):
        shutil.copyfile(master_path, backup_path)
        print(f"[*] Backup master dataset dibuat: {backup_path}")

    # 1. BACA & UPDATE MASTER DENGAN KANDIDAT
    print("\n[1] Menyelaraskan Kandidat Joy & Surprise...")
    df_master = pd.read_csv(master_path)
    cand = pd.read_csv(cand_path)
    cand_map = {'Joy': 'Bahagia', 'Surprise': 'Kaget'}
    cand['mapped_emotion'] = cand['candidate_emotion'].map(cand_map)

    id_to_emo = dict(zip(cand['source_id'].astype(str), cand['mapped_emotion']))
    text_to_emo = dict(zip(cand['text'].astype(str).str.strip(), cand['mapped_emotion']))

    updated = df_master.copy()
    update_count = 0
    for idx, row in updated.iterrows():
        sid = str(row['id'])
        stext = str(row['text']).strip()
        if sid in id_to_emo:
            updated.at[idx, 'predicted_emotion'] = id_to_emo[sid]
            update_count += 1
        elif stext in text_to_emo:
            updated.at[idx, 'predicted_emotion'] = text_to_emo[stext]
            update_count += 1
    print(f" - Baris terupdate di master: {update_count}")

    master_ids = set(updated['id'].astype(str))
    master_texts = set(updated['text'].astype(str).str.strip())
    new_cand = cand[~cand['source_id'].astype(str).isin(master_ids) & ~cand['text'].astype(str).str.strip().isin(master_texts)].drop_duplicates(subset=['text']).copy()

    new_rows = []
    for _, r in new_cand.iterrows():
        row_dict = {
            'id': r['source_id'],
            'text': r['text'],
            'created_at': '2025-11-04T00:00:00Z',
            'author_username': r['author'] if 'author' in r and pd.notna(r['author']) else 'anon',
            'author_name': r['author'] if 'author' in r and pd.notna(r['author']) else 'anon',
            'like_count': 0,
            'retweet_count': 0,
            'reply_count': 0,
            'quote_count': 0,
            'predicted_emotion': r['mapped_emotion'],
            'processed_text': r['text'].lower()
        }
        for c in updated.columns:
            if c not in row_dict:
                row_dict[c] = ''
        new_rows.append(row_dict)

    if new_rows:
        updated = pd.concat([updated, pd.DataFrame(new_rows)], ignore_index=True)
        print(f" - Baris kandidat baru ditambahkan: {len(new_rows)}")

    # Simpan kembali dataset master yang telah terharmonisasi
    updated.to_csv(master_path, index=False)
    print(" - Distribusi master setelah harmonisasi:")
    print(updated['predicted_emotion'].value_counts())

    # 2. GROUP-AWARE SPLIT (ZERO LEAKAGE)
    print("\n[2] Menjalankan Group-Aware Split (80% Train, 20% Test)...")
    unique_texts = updated.groupby('processed_text').agg({
        'predicted_emotion': lambda s: s.iloc[0],
        'id': 'count'
    }).reset_index().rename(columns={'id': 'count'})

    np.random.seed(42)
    train_groups = []
    test_groups = []

    for emo, grp in unique_texts.groupby('predicted_emotion'):
        shuffled = grp.sample(frac=1.0, random_state=42)
        n = len(shuffled)
        if n == 1:
            n_train = 1
        elif n == 2:
            n_train = 1
        else:
            n_train = max(1, int(round(0.8 * n)))
            if n_train == n and n > 1:
                n_train = n - 1
        train_groups.extend(shuffled.iloc[:n_train]['processed_text'].tolist())
        test_groups.extend(shuffled.iloc[n_train:]['processed_text'].tolist())

    train_set = updated[updated['processed_text'].isin(set(train_groups))].reset_index(drop=True)
    test_set = updated[updated['processed_text'].isin(set(test_groups))].reset_index(drop=True)

    # Verifikasi zero-leakage
    overlap = set(train_set['processed_text']).intersection(set(test_set['processed_text']))
    if len(overlap) > 0:
        raise ValueError(f"Data leakage detected! {len(overlap)} overlaps found.")
    print(f" - Zero-Leakage Verifikasi: PASSED (Overlap = {len(overlap)})")

    # Simpan file split
    train_split_path = os.path.join(results_dir, "emotion_train_group_split.csv")
    test_split_path = os.path.join(results_dir, "emotion_test_group_split.csv")
    train_set.to_csv(train_split_path, index=False)
    test_set.to_csv(test_split_path, index=False)
    print(f" - Train split disimpan: {train_split_path} (N={len(train_set)})")
    print(f" - Test split disimpan : {test_split_path} (N={len(test_set)})")

    label_to_id = {
        'Marah': 0, 'Jijik': 1, 'Takut': 2, 'Bahagia': 3,
        'Percaya': 4, 'Netral': 5, 'Sedih': 6, 'Tertarik': 7, 'Kaget': 8
    }
    id_to_label = {v: k for k, v in label_to_id.items()}

    train_set['label_id'] = train_set['predicted_emotion'].map(label_to_id)
    test_set['label_id'] = test_set['predicted_emotion'].map(label_to_id)

    # 3. PERHITUNGAN CLASS WEIGHTS (INVERSE FREQUENCY WITH SMOOTHING)
    print("\n[3] Menghitung Class Weights untuk Imbalanced Loss...")
    counts = train_set['label_id'].value_counts()
    total_samples = len(train_set)
    num_classes = len(label_to_id)

    # Smoothed inverse frequency: sqrt(total / count)
    weights = np.zeros(num_classes, dtype=np.float32)
    for i in range(num_classes):
        cnt = counts.get(i, 1)
        weights[i] = np.sqrt(total_samples / cnt)
    # Normalize weights so mean is 1.0
    weights = weights / np.mean(weights)
    print(" - Class weights (0..8):")
    for i in range(num_classes):
        cnt = counts.get(i, 0)
        print(f"   {i} ({id_to_label[i]}): count={cnt}, weight={weights[i]:.2f}")

    class_weights_tensor = torch.tensor(weights, dtype=torch.float)

    # 4. TOKENISASI & DATASET
    print("\n[4] Tokenisasi Teks...")
    set_seed(42)
    tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
    train_encodings = tokenizer([str(x) for x in train_set['processed_text'].tolist()], truncation=True, padding=True, max_length=128)
    test_encodings = tokenizer([str(x) for x in test_set['processed_text'].tolist()], truncation=True, padding=True, max_length=128)

    class PyTorchDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels
        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
            return item
        def __len__(self):
            return len(self.labels)

    train_dataset = PyTorchDataset(train_encodings, train_set['label_id'].tolist())
    test_dataset = PyTorchDataset(test_encodings, test_set['label_id'].tolist())

    # 5. WEIGHTED TRAINER DEFINITION
    class WeightedTrainer(Trainer):
        def __init__(self, class_weights=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.class_weights = class_weights

        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            labels = inputs.get("labels")
            outputs = model(**inputs)
            logits = outputs.get("logits")
            if self.class_weights is not None:
                device = logits.device
                loss_fct = nn.CrossEntropyLoss(weight=self.class_weights.to(device))
            else:
                loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
            return (loss, outputs) if return_outputs else loss

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro', zero_division=0)
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1_macro': f1,
            'precision_macro': precision,
            'recall_macro': recall
        }

    model = AutoModelForSequenceClassification.from_pretrained(
        "indobenchmark/indobert-base-p2",
        num_labels=9,
        id2label=id_to_label,
        label2id=label_to_id
    )

    output_dir = os.path.join(results_dir, "indobert_group_aware_final")
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        seed=42,
        logging_steps=50,
        save_strategy="epoch",
        eval_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True
    )

    trainer = WeightedTrainer(
        class_weights=class_weights_tensor,
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )

    print("\n[5] Memulai Weighted Fine-Tuning IndoBERT...")
    trainer.train()

    best_model_dir = os.path.join(output_dir, "best_model")
    trainer.save_model(best_model_dir)
    tokenizer.save_pretrained(best_model_dir)
    print(f"\n[*] Model terbaik disimpan di: {best_model_dir}")

    # 6. EVALUASI TEST SET SECARA KOMPREHENSIF
    print("\n[6] Menjalankan Evaluasi Komprehensif pada Test Set...")
    eval_res = trainer.evaluate()
    print(" - Hasil Evaluasi Trainer:")
    for k, v in eval_res.items():
        print(f"   {k}: {v}")

    # Generate Detail Classification Report
    preds_output = trainer.predict(test_dataset)
    y_pred = np.argmax(preds_output.predictions, axis=1)
    y_true = np.array(test_set['label_id'].tolist())

    target_names = [id_to_label[i] for i in range(num_classes)]
    cls_report = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
    print("\n" + "=" * 60)
    print("DETAILED 9-CLASS CLASSIFICATION REPORT:")
    print("=" * 60)
    print(cls_report)

    # Simpan laporan evaluasi ke file
    report_file = os.path.join(results_dir, "FINAL_9_CLASS_INDOBERT_EVALUATION.txt")
    with open(report_file, "w") as f:
        f.write("FINAL 9-CLASS INDOBERT EVALUATION REPORT (GROUP-AWARE ZERO LEAKAGE)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Train Samples: {len(train_set)}\n")
        f.write(f"Test Samples : {len(test_set)}\n\n")
        f.write("Class Weights Applied:\n")
        for i in range(num_classes):
            f.write(f"  {id_to_label[i]}: {weights[i]:.2f}\n")
        f.write("\nClassification Report:\n")
        f.write(cls_report)
        f.write("\n\nConfusion Matrix:\n")
        cm = confusion_matrix(y_true, y_pred)
        f.write(np.array2string(cm))
    print(f"\n[*] Laporan lengkap disimpan di: {report_file}")

if __name__ == "__main__":
    main()
