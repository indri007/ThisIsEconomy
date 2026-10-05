#!/usr/bin/env python3
"""
scripts/train_indobert_v2_val_protocol.py
=========================================
Retraining IndoBERT Group-Aware dengan protokol validasi yang ketat:
1. results/emotion_test_group_split.csv (N=1,058) sebagai TEST set murni (TIDAK pernah masuk Trainer).
2. Dari results/emotion_train_group_split.csv (N=4,205), dibuat VALIDATION split (10%)
   menggunakan GroupShuffleSplit(test_size=0.1, random_state=42) berdasarkan processed_text.
   Verifikasi 0 text overlap antara train/val/test.
3. Train indobenchmark/indobert-base-p2, num_labels=9, max_length=128, batch 32, lr 2e-5,
   epochs=3, eval_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True,
   metric_for_best_model="eval_loss", eval_dataset = VALIDATION only.
4. Evaluasi checkpoint terbaik SATU KALI pada TEST set. Simpan metrik, laporan per kelas,
   confusion matrix, trainer_state.json, dan info epoch terpilih.
5. Retrain baseline TF-IDF + LogReg dan TF-IDF + Linear SVM pada reduced train split yang sama
   dan evaluasi pada TEST set yang sama.
6. Tampilkan tabel komparasi side-by-side: old (test-selected) vs new (val-selected).
Seluruh output disimpan ke results/indobert_group_aware_v2/.
"""

import os
import sys
import json
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import GroupShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

def main():
    print("=" * 80)
    print("RE-TRAINING INDOBERT GROUP-AWARE (VALIDATION PROTOCOL V2)")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "results")
    out_dir = os.path.join(results_dir, "indobert_group_aware_v2")
    os.makedirs(out_dir, exist_ok=True)
    ckpt_dir = os.path.join(out_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # 1. LOAD DATA & GROUP-AWARE VALIDATION SPLIT
    # -------------------------------------------------------------------------
    print("\n[Step 1] Memuat dataset dan membuat Train/Val split...")
    orig_train_path = os.path.join(results_dir, "emotion_train_group_split.csv")
    test_path = os.path.join(results_dir, "emotion_test_group_split.csv")

    orig_train_df = pd.read_csv(orig_train_path)
    test_df = pd.read_csv(test_path)

    print(f"Total baris train asli : {len(orig_train_df)}")
    print(f"Total baris test murni  : {len(test_df)}")

    gss = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    train_idx, val_idx = next(gss.split(orig_train_df, groups=orig_train_df['processed_text']))

    train_df = orig_train_df.iloc[train_idx].copy().reset_index(drop=True)
    val_df = orig_train_df.iloc[val_idx].copy().reset_index(drop=True)

    print(f"-> Reduced Train Set   : {len(train_df)} rows ({train_df['processed_text'].nunique()} unique processed texts)")
    print(f"-> Validation Set (10%): {len(val_df)} rows ({val_df['processed_text'].nunique()} unique processed texts)")
    print(f"-> Test Set (Untouched): {len(test_df)} rows ({test_df['processed_text'].nunique()} unique processed texts)")

    # Simpan split
    train_df.to_csv(os.path.join(out_dir, "train_split.csv"), index=False)
    val_df.to_csv(os.path.join(out_dir, "val_split.csv"), index=False)
    print("✓ Disimpan: train_split.csv & val_split.csv")

    # -------------------------------------------------------------------------
    # 2. VERIFIKASI ZERO TEXT OVERLAP
    # -------------------------------------------------------------------------
    print("\n[Step 2] Verifikasi kebocoran data (Zero Text Overlap)...")
    train_p = set(train_df['processed_text'])
    val_p   = set(val_df['processed_text'])
    test_p  = set(test_df['processed_text'])

    train_t = set(train_df['text'])
    val_t   = set(val_df['text'])
    test_t  = set(test_df['text'])

    overlap_train_val_p = len(train_p & val_p)
    overlap_val_test_p  = len(val_p & test_p)
    overlap_train_test_p = len(train_p & test_p)

    overlap_train_val_t = len(train_t & val_t)
    overlap_val_test_t  = len(val_t & test_t)
    overlap_train_test_t = len(train_t & test_t)

    print(f"  Overlap processed_text (Train vs Val) : {overlap_train_val_p}")
    print(f"  Overlap processed_text (Val vs Test)  : {overlap_val_test_p}")
    print(f"  Overlap processed_text (Train vs Test): {overlap_train_test_p}")
    print(f"  Overlap raw text (Train vs Val)       : {overlap_train_val_t}")
    print(f"  Overlap raw text (Val vs Test)        : {overlap_val_test_t}")
    print(f"  Overlap raw text (Train vs Test)      : {overlap_train_test_t}")

    if any(x != 0 for x in [overlap_train_val_p, overlap_val_test_p, overlap_train_test_p,
                            overlap_train_val_t, overlap_val_test_t, overlap_train_test_t]):
        raise ValueError("FATAL: Text overlap terdeteksi! Protokol bocor.")
    print("✓ ZERO TEXT OVERLAP terkonfirmasi 100%!")

    # -------------------------------------------------------------------------
    # 3. PERSIAPAN MODEL & DATASET ENCODING
    # -------------------------------------------------------------------------
    print("\n[Step 3] Tokenisasi dan konfigurasi IndoBERT...")
    label_to_id = {
        'Marah': 0, 'Jijik': 1, 'Takut': 2, 'Bahagia': 3,
        'Percaya': 4, 'Netral': 5, 'Sedih': 6, 'Tertarik': 7, 'Kaget': 8
    }
    id_to_label = {v: k for k, v in label_to_id.items()}

    train_df['label_id'] = train_df['predicted_emotion'].map(label_to_id)
    val_df['label_id']   = val_df['predicted_emotion'].map(label_to_id)
    test_df['label_id']  = test_df['predicted_emotion'].map(label_to_id)

    tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")

    train_encodings = tokenizer(train_df['processed_text'].tolist(), truncation=True, padding=True, max_length=128)
    val_encodings   = tokenizer(val_df['processed_text'].tolist(), truncation=True, padding=True, max_length=128)

    class TorchEmotionDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels
        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item
        def __len__(self):
            return len(self.labels)

    train_dataset = TorchEmotionDataset(train_encodings, train_df['label_id'].tolist())
    val_dataset   = TorchEmotionDataset(val_encodings, val_df['label_id'].tolist())

    model = AutoModelForSequenceClassification.from_pretrained(
        "indobenchmark/indobert-base-p2",
        num_labels=9,
        id2label=id_to_label,
        label2id=label_to_id
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=1)
        acc = accuracy_score(labels, preds)
        macro_f1 = f1_score(labels, preds, average='macro', zero_division=0)
        return {
            "accuracy": acc,
            "macro_f1": macro_f1
        }

    training_args = TrainingArguments(
        output_dir=ckpt_dir,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        seed=42,
        logging_steps=20,
        save_strategy="epoch",
        eval_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        save_total_limit=3,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # -------------------------------------------------------------------------
    # 4. TRAINING
    # -------------------------------------------------------------------------
    print("\n[Step 4] Memulai fine-tuning IndoBERT (evaluasi HANYA pada VALIDATION set)...")
    train_result = trainer.train()

    best_ckpt = trainer.state.best_model_checkpoint
    best_eval_loss = trainer.state.best_metric

    # Ekstrak epoch terpilih
    selected_epoch = None
    for h in trainer.state.log_history:
        if 'eval_loss' in h and abs(h['eval_loss'] - best_eval_loss) < 1e-5:
            selected_epoch = h.get('epoch')
            break
    if selected_epoch is None:
        selected_epoch = 2.0  # fallback

    print("\n✓ Training selesai!")
    print(f"  Best Checkpoint : {best_ckpt}")
    print(f"  Best Eval Loss  : {best_eval_loss:.4f}")
    print(f"  Selected Epoch  : {selected_epoch}")

    # Simpan best_model dan trainer_state.json di out_dir
    best_model_dir = os.path.join(out_dir, "best_model")
    trainer.save_model(best_model_dir)
    tokenizer.save_pretrained(best_model_dir)

    # Salin / simpan trainer_state.json
    state_dict = {
        "best_model_checkpoint": best_ckpt,
        "best_metric": best_eval_loss,
        "metric_for_best_model": "eval_loss",
        "selected_epoch": selected_epoch,
        "log_history": trainer.state.log_history
    }
    with open(os.path.join(out_dir, "trainer_state.json"), "w") as f:
        json.dump(state_dict, f, indent=2)
    print("✓ Disimpan: results/indobert_group_aware_v2/trainer_state.json")

    # -------------------------------------------------------------------------
    # 5. EVALUASI SATU KALI PADA TEST SET
    # -------------------------------------------------------------------------
    print("\n[Step 5] Mengevaluasi model terbaik SATU KALI pada TEST set (N=1,058)...")
    device = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
    best_model = AutoModelForSequenceClassification.from_pretrained(best_model_dir).to(device)
    best_model.eval()

    test_proc_texts = test_df['processed_text'].tolist()
    test_true_labels = test_df['predicted_emotion'].tolist()
    y_test_num = test_df['label_id'].tolist()

    pred_ids = []
    batch_size = 32
    for i in range(0, len(test_proc_texts), batch_size):
        b_texts = test_proc_texts[i:i+batch_size]
        inputs = tokenizer(b_texts, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
        with torch.no_grad():
            logits = best_model(**inputs).logits
            preds = torch.argmax(logits, dim=1).cpu().numpy().tolist()
            pred_ids.extend(preds)

    pred_labels = [id_to_label[p] for p in pred_ids]

    # Hitung metrik IndoBERT
    indo_acc = accuracy_score(y_test_num, pred_ids)
    indo_macro_p = precision_score(y_test_num, pred_ids, average='macro', zero_division=0)
    indo_macro_r = recall_score(y_test_num, pred_ids, average='macro', zero_division=0)
    indo_macro_f1 = f1_score(y_test_num, pred_ids, average='macro', zero_division=0)
    indo_weight_p = precision_score(y_test_num, pred_ids, average='weighted', zero_division=0)
    indo_weight_r = recall_score(y_test_num, pred_ids, average='weighted', zero_division=0)
    indo_weight_f1 = f1_score(y_test_num, pred_ids, average='weighted', zero_division=0)

    # Simpan metrics CSV
    indo_metrics_df = pd.DataFrame([{
        'Model': 'IndoBERT Group-Aware (v2 Val-Selected)',
        'Validation_Protocol': 'Group-Aware Val (10%)',
        'Selected_Epoch': selected_epoch,
        'Best_Checkpoint': os.path.basename(best_ckpt) if best_ckpt else 'checkpoint',
        'Best_Val_Loss': round(best_eval_loss, 4),
        'Test_N': len(test_df),
        'Accuracy': round(indo_acc, 4),
        'Macro_Precision': round(indo_macro_p, 4),
        'Macro_Recall': round(indo_macro_r, 4),
        'Macro_F1': round(indo_macro_f1, 4),
        'Weighted_Precision': round(indo_weight_p, 4),
        'Weighted_Recall': round(indo_weight_r, 4),
        'Weighted_F1': round(indo_weight_f1, 4)
    }])
    indo_metrics_df.to_csv(os.path.join(out_dir, "indobert_metrics.csv"), index=False)
    print("✓ Disimpan: results/indobert_group_aware_v2/indobert_metrics.csv")

    # Simpan classification report
    present_eval_classes = sorted(list(set(y_test_num).union(set(pred_ids))))
    present_eval_names = [id_to_label[c] for c in present_eval_classes]
    report_dict = classification_report(
        y_test_num, pred_ids, labels=present_eval_classes, target_names=present_eval_names,
        digits=4, zero_division=0, output_dict=True
    )
    report_df = pd.DataFrame(report_dict).transpose().reset_index().rename(columns={'index': 'Emotion'})
    report_df.to_csv(os.path.join(out_dir, "classification_report.csv"), index=False)
    print("✓ Disimpan: results/indobert_group_aware_v2/classification_report.csv")

    # Simpan predictions
    preds_df = pd.DataFrame({
        'text': test_df['text'],
        'processed_text': test_df['processed_text'],
        'true_label': test_true_labels,
        'predicted_label': pred_labels
    })
    preds_df.to_csv(os.path.join(out_dir, "predictions_test.csv"), index=False)
    print("✓ Disimpan: results/indobert_group_aware_v2/predictions_test.csv")

    # Confusion matrix
    cm = confusion_matrix(y_test_num, pred_ids, labels=present_eval_classes)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    cm_norm = np.nan_to_num(cm_norm)

    plt.figure(figsize=(8.5, 6.5), dpi=300)
    sns.set_theme(style="white")
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=present_eval_names, yticklabels=present_eval_names,
        linewidths=.5, linecolor='gray', cbar=True
    )
    plt.xlabel('Predicted Label (IndoBERT Group-Aware v2)', fontsize=11, fontweight='bold')
    plt.ylabel('True Label (Reference)', fontsize=11, fontweight='bold')
    plt.title('Confusion Matrix (Counts): IndoBERT Group-Aware v2 (Val-Selected)', fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "confusion_matrix.png"), dpi=300)
    plt.close()

    plt.figure(figsize=(8.5, 6.5), dpi=300)
    sns.heatmap(
        cm_norm, annot=True, fmt='.2f', cmap='Blues',
        xticklabels=present_eval_names, yticklabels=present_eval_names,
        linewidths=.5, linecolor='gray', cbar=True
    )
    plt.xlabel('Predicted Label (IndoBERT Group-Aware v2)', fontsize=11, fontweight='bold')
    plt.ylabel('True Label (Reference)', fontsize=11, fontweight='bold')
    plt.title('Normalized Confusion Matrix: IndoBERT Group-Aware v2 (Val-Selected)', fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "confusion_matrix_normalized.png"), dpi=300)
    plt.close()
    print("✓ Disimpan: confusion_matrix.png & confusion_matrix_normalized.png")

    # -------------------------------------------------------------------------
    # 6. RETRAIN TF-IDF BASELINES PADA REDUCED TRAIN SPLIT
    # -------------------------------------------------------------------------
    print("\n[Step 6] Melatih baseline TF-IDF pada reduced train split...")
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = tfidf.fit_transform(train_df['processed_text'])
    X_test_tfidf  = tfidf.transform(test_df['processed_text'])

    y_train = train_df['predicted_emotion'].values
    y_test  = test_df['predicted_emotion'].values

    # Logistic Regression
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_tfidf, y_train)
    lr_preds = lr.predict(X_test_tfidf)

    lr_acc = accuracy_score(y_test, lr_preds)
    lr_macro_p = precision_score(y_test, lr_preds, average='macro', zero_division=0)
    lr_macro_r = recall_score(y_test, lr_preds, average='macro', zero_division=0)
    lr_macro_f1 = f1_score(y_test, lr_preds, average='macro', zero_division=0)
    lr_weight_p = precision_score(y_test, lr_preds, average='weighted', zero_division=0)
    lr_weight_r = recall_score(y_test, lr_preds, average='weighted', zero_division=0)
    lr_weight_f1 = f1_score(y_test, lr_preds, average='weighted', zero_division=0)

    pd.DataFrame([{
        'Model': 'TF-IDF + Logistic Regression (v2)',
        'Train_N': len(train_df),
        'Test_N': len(test_df),
        'Accuracy': round(lr_acc, 4),
        'Macro_Precision': round(lr_macro_p, 4),
        'Macro_Recall': round(lr_macro_r, 4),
        'Macro_F1': round(lr_macro_f1, 4),
        'Weighted_Precision': round(lr_weight_p, 4),
        'Weighted_Recall': round(lr_weight_r, 4),
        'Weighted_F1': round(lr_weight_f1, 4)
    }]).to_csv(os.path.join(out_dir, "tfidf_logreg_metrics.csv"), index=False)

    # Linear SVM
    svm = LinearSVC(max_iter=2000, random_state=42)
    svm.fit(X_train_tfidf, y_train)
    svm_preds = svm.predict(X_test_tfidf)

    svm_acc = accuracy_score(y_test, svm_preds)
    svm_macro_p = precision_score(y_test, svm_preds, average='macro', zero_division=0)
    svm_macro_r = recall_score(y_test, svm_preds, average='macro', zero_division=0)
    svm_macro_f1 = f1_score(y_test, svm_preds, average='macro', zero_division=0)
    svm_weight_p = precision_score(y_test, svm_preds, average='weighted', zero_division=0)
    svm_weight_r = recall_score(y_test, svm_preds, average='weighted', zero_division=0)
    svm_weight_f1 = f1_score(y_test, svm_preds, average='weighted', zero_division=0)

    pd.DataFrame([{
        'Model': 'TF-IDF + Linear SVM (v2)',
        'Train_N': len(train_df),
        'Test_N': len(test_df),
        'Accuracy': round(svm_acc, 4),
        'Macro_Precision': round(svm_macro_p, 4),
        'Macro_Recall': round(svm_macro_r, 4),
        'Macro_F1': round(svm_macro_f1, 4),
        'Weighted_Precision': round(svm_weight_p, 4),
        'Weighted_Recall': round(svm_weight_r, 4),
        'Weighted_F1': round(svm_weight_f1, 4)
    }]).to_csv(os.path.join(out_dir, "tfidf_svm_metrics.csv"), index=False)
    print("✓ Baseline TF-IDF selesai dievaluasi.")

    # -------------------------------------------------------------------------
    # 7. TABEL SIDE-BY-SIDE: OLD (TEST-SELECTED) VS NEW (VAL-SELECTED)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("KOMPARASI SIDE-BY-SIDE: OLD (TEST-SELECTED) VS NEW (VAL-SELECTED)")
    print("=" * 80)

    # Old results from results/FINAL_model_comparison.csv
    old_comp_path = os.path.join(results_dir, "FINAL_model_comparison.csv")
    old_df = pd.read_csv(old_comp_path)
    old_map = {row['Model']: row for _, row in old_df.iterrows()}

    table_rows = [
        {
            'Model': 'TF-IDF + Logistic Regression',
            'Old_Train_N': old_map['TF-IDF + Logistic Regression']['Train_N'],
            'New_Train_N': len(train_df),
            'Old_Acc': f"{old_map['TF-IDF + Logistic Regression']['Accuracy']:.4f}",
            'New_Acc': f"{lr_acc:.4f}",
            'Old_Macro_F1': f"{old_map['TF-IDF + Logistic Regression']['Macro_F1']:.4f}",
            'New_Macro_F1': f"{lr_macro_f1:.4f}",
            'Old_Weighted_F1': f"{old_map['TF-IDF + Logistic Regression']['Weighted_F1']:.4f}",
            'New_Weighted_F1': f"{lr_weight_f1:.4f}",
            'Selection_Criterion': 'N/A (Standard Fit)'
        },
        {
            'Model': 'TF-IDF + Linear SVM',
            'Old_Train_N': old_map['TF-IDF + Linear SVM']['Train_N'],
            'New_Train_N': len(train_df),
            'Old_Acc': f"{old_map['TF-IDF + Linear SVM']['Accuracy']:.4f}",
            'New_Acc': f"{svm_acc:.4f}",
            'Old_Macro_F1': f"{old_map['TF-IDF + Linear SVM']['Macro_F1']:.4f}",
            'New_Macro_F1': f"{svm_macro_f1:.4f}",
            'Old_Weighted_F1': f"{old_map['TF-IDF + Linear SVM']['Weighted_F1']:.4f}",
            'New_Weighted_F1': f"{svm_weight_f1:.4f}",
            'Selection_Criterion': 'N/A (Standard Fit)'
        },
        {
            'Model': 'IndoBERT Group-Aware',
            'Old_Train_N': old_map['IndoBERT Group-Aware']['Train_N'],
            'New_Train_N': len(train_df),
            'Old_Acc': f"{old_map['IndoBERT Group-Aware']['Accuracy']:.4f}",
            'New_Acc': f"{indo_acc:.4f}",
            'Old_Macro_F1': f"{old_map['IndoBERT Group-Aware']['Macro_F1']:.4f}",
            'New_Macro_F1': f"{indo_macro_f1:.4f}",
            'Old_Weighted_F1': f"{old_map['IndoBERT Group-Aware']['Weighted_F1']:.4f}",
            'New_Weighted_F1': f"{indo_weight_f1:.4f}",
            'Selection_Criterion': f'Old: Test ckpt-264 | New: Val Epoch {selected_epoch}'
        }
    ]

    comp_df = pd.DataFrame(table_rows)
    comp_df.to_csv(os.path.join(out_dir, "model_comparison_side_by_side.csv"), index=False)

    # Print markdown table
    print("\n" + comp_df.to_markdown(index=False))
    print(f"\nSeluruh hasil telah disimpan di direktori: {out_dir}")

if __name__ == "__main__":
    main()
