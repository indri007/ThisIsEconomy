#!/usr/bin/env python3
"""
evaluate_best_indobert_9_labels.py
==================================
Evaluasi komprehensif model IndoBERT 9-kelas terbaik pada test set bebas-leakage.
"""

import os
import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "results")
    test_path = os.path.join(results_dir, "emotion_test_group_split.csv")
    model_path = os.path.join(results_dir, "indobert_group_aware_final", "best_model")

    print(f"Loading test set from: {test_path}")
    test_df = pd.read_csv(test_path)
    print(f"Total test samples: {len(test_df)}")

    label_to_id = {
        'Marah': 0, 'Jijik': 1, 'Takut': 2, 'Bahagia': 3,
        'Percaya': 4, 'Netral': 5, 'Sedih': 6, 'Tertarik': 7, 'Kaget': 8
    }
    id_to_label = {v: k for k, v in label_to_id.items()}
    num_classes = len(label_to_id)

    test_df['label_id'] = test_df['predicted_emotion'].map(label_to_id)
    y_true = test_df['label_id'].values

    device = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
    print(f"Using device: {device}")
    print(f"Loading model from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()

    batch_size = 32
    preds = []
    texts = [str(x) for x in test_df['processed_text'].tolist()]

    print("Running batch inference on test set...")
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
            outputs = model(**inputs)
            batch_preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
            preds.extend(batch_preds)

    y_pred = np.array(preds)

    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    macro_prec = precision_score(y_true, y_pred, average='macro', zero_division=0)
    macro_rec = recall_score(y_true, y_pred, average='recall' if 'recall' in [] else 'macro', zero_division=0)

    print("\n" + "=" * 70)
    print("HASIL EVALUASI MODEL INDOBERT 9-KELAS (TEST SET)")
    print("=" * 70)
    print(f"Akurasi Total : {acc:.4f} ({acc*100:.2f}%)")
    print(f"Macro F1-Score: {macro_f1:.4f} ({macro_f1*100:.2f}%)")
    print(f"Weighted F1   : {weighted_f1:.4f} ({weighted_f1*100:.2f}%)")
    print(f"Macro Precision: {macro_prec:.4f}")
    print(f"Macro Recall  : {macro_rec:.4f}")

    target_names = [id_to_label[i] for i in range(num_classes)]
    labels_list = list(range(num_classes))
    report = classification_report(y_true, y_pred, labels=labels_list, target_names=target_names, zero_division=0)

    print("\nKLASIFIKASI PER KELAS:")
    print("-" * 70)
    print(report)

    cm = confusion_matrix(y_true, y_pred, labels=labels_list)
    print("\nCONFUSION MATRIX (Baris=True, Kolom=Pred):")
    print("-" * 70)
    cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)
    print(cm_df.to_string())

    # Simpan ke file teks dan CSV
    report_file = os.path.join(results_dir, "FINAL_9_CLASS_INDOBERT_EVALUATION.txt")
    with open(report_file, "w") as f:
        f.write("HASIL EVALUASI INDOBERT 9-KELAS EMOSI (ZERO-LEAKAGE TEST SET)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total Test Samples: {len(test_df)}\n")
        f.write(f"Akurasi Total     : {acc:.4f} ({acc*100:.2f}%)\n")
        f.write(f"Macro F1-Score    : {macro_f1:.4f} ({macro_f1*100:.2f}%)\n")
        f.write(f"Weighted F1-Score : {weighted_f1:.4f} ({weighted_f1*100:.2f}%)\n\n")
        f.write("Classification Report:\n")
        f.write(report + "\n\n")
        f.write("Confusion Matrix:\n")
        f.write(cm_df.to_string() + "\n")
    print(f"\n[*] Laporan berhasil disimpan ke: {report_file}")

    # Simpan prediksi test set
    test_df['predicted_model_emotion'] = [id_to_label[p] for p in y_pred]
    test_df['is_correct'] = (test_df['label_id'] == y_pred)
    pred_csv_path = os.path.join(results_dir, "indobert_test_predictions_9_labels.csv")
    test_df.to_csv(pred_csv_path, index=False)
    print(f"[*] Prediksi test set disimpan ke: {pred_csv_path}")

if __name__ == "__main__":
    main()
