# 06 IndoBERT Checkpoint Audit Report

## 1. Checkpoint Artifact Metadata
- **Path:** `/Users/jevin/Documents/tesis_mbg/results/indobert_finetuned_9_labels/checkpoint-792`
- **Model Architecture:** `BertForSequenceClassification`
- **Model Type:** `bert`
- **Number of Labels:** None
- **Label Mapping (`id2label`):** {
  "0": "anger",
  "1": "disgust",
  "2": "fear",
  "3": "joy",
  "4": "love",
  "5": "neutral",
  "6": "sadness",
  "7": "shame",
  "8": "surprise"
}
- **Training Epochs:** 3.0
- **Global Training Steps:** 792

## 2. Split Reconstruction & Provenance Investigation
- Evidence from `scripts/train.py` line 30:
  `train_texts, val_texts, train_labels, val_labels = train_test_split(df['processed_text'].tolist(), df['label_id'].tolist(), test_size=0.2, random_state=42)`
- **Finding:** The training script used standard `sklearn.model_selection.train_test_split` with `random_state=42` and `test_size=0.2`.
- **Crucial Flaw:** It did NOT perform group-aware splitting. Duplicate texts were randomly scattered across both training and evaluation partitions.
