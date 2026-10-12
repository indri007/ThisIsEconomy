#!/usr/bin/env python3
"""
pipelines_30m/indobert_inference.py
==================================
Memproses Teks Bersih ke IndoBERT Fine-Tuned (indobenchmark/indobert-base-p2, 3 Epochs):
1. Memuat model IndoBERT yang TELAH DI-FINETUNE selama 3 epoch (GroupShuffleSplit, 75.99% akurasi).
2. Mendeteksi akselerasi Apple Silicon GPU (MPS Metal) atau CUDA secara otomatis.
3. Memastikan pemetaan kelas 9 Emosi Plutchik (Marah, Jijik, Takut, Bahagia, Percaya, Netral, Sedih, Tertarik, Kaget) 100% konsisten.
4. Mendukung Pengujian Varian Pra-pemrosesan (Ablation Study):
   - Varian 1 (clean_text): Mempertahankan konteks, negasi ("tidak", "bukan", "belum"), dan bahasa informal.
   - Varian 2 (processed_text): Sastrawi Stemming + Stopword Removal.
5. Pemrosesan skala besar terpartisi (30 Juta korpus / clean_30m_part_XXXXX.parquet).
"""

import os
import sys
import argparse
from pathlib import Path
import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Lokasi Model Fine-Tuned (Epoch 3, Group-Aware Protocol)
REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_BEST_MODEL = REPO_ROOT / "results" / "indobert_group_aware_v2" / "best_model"
EXTERNAL_BEST_MODEL = Path("/Users/jevin/Documents/tesis_mbg/results/indobert_group_aware_v2/best_model")

def resolve_model_path():
    """Menemukan lokasi checkpoint model fine-tuned. Menolak keras fallback ke base model."""
    if (LOCAL_BEST_MODEL / "model.safetensors").exists() or (LOCAL_BEST_MODEL / "pytorch_model.bin").exists():
        return str(LOCAL_BEST_MODEL)
    if (EXTERNAL_BEST_MODEL / "model.safetensors").exists() or (EXTERNAL_BEST_MODEL / "pytorch_model.bin").exists():
        return str(EXTERNAL_BEST_MODEL)
    raise FileNotFoundError(
        "FATAL: Checkpoint IndoBERT fine-tuned tidak ditemukan di "
        f"'{LOCAL_BEST_MODEL}' maupun '{EXTERNAL_BEST_MODEL}'. "
        "Sistem menolak keras fallback ke model dasar (base untrained) untuk mencegah prediksi emosi palsu."
    )

try:
    DEFAULT_MODEL_PATH = resolve_model_path()
except FileNotFoundError:
    DEFAULT_MODEL_PATH = str(LOCAL_BEST_MODEL)

# Konfigurasi Berkas Input/Output Default Skala 30 Juta
DATA_OUTPUT_DIR = Path("/Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output")
DEFAULT_INPUT_PARQUET = DATA_OUTPUT_DIR / "clean_30m_part_00001.parquet"
if not DEFAULT_INPUT_PARQUET.exists():
    _fallback = DATA_OUTPUT_DIR / "clean_part_00001.parquet"
    if _fallback.exists():
        DEFAULT_INPUT_PARQUET = _fallback

DEFAULT_OUTPUT_PARQUET = DATA_OUTPUT_DIR / "clean_30m_part_00001_with_indobert.parquet"

# Taksonomi Resmi 9 Emosi Plutchik Sesuai Tesis
FALLBACK_LABEL_MAP = {
    0: 'Marah',
    1: 'Jijik',
    2: 'Takut',
    3: 'Bahagia',
    4: 'Percaya',
    5: 'Netral',
    6: 'Sedih',
    7: 'Tertarik',
    8: 'Kaget'
}

def run_indobert_pipeline(
    input_file=DEFAULT_INPUT_PARQUET,
    output_file=DEFAULT_OUTPUT_PARQUET,
    model_path=DEFAULT_MODEL_PATH,
    text_col=None,
    batch_size=32,
    sample=None
):
    input_path = Path(input_file)
    output_path = Path(output_file)

    print("=" * 80)
    print("🤖 PEMROSESAN TEKS SKALA BESAR KE INDOBERT TERLATIH (FINE-TUNED 3 EPOCHS)")
    print("=" * 80)
    print(f"Berkas Input        : {input_path}")
    print(f"Berkas Output       : {output_path}")
    print(f"Model Path          : {model_path}")
    print(f"Batch Size          : {batch_size}")

    if not input_path.exists():
        print(f"❌ File tidak ditemukan: {input_path}")
        sys.exit(1)

    # Deteksi Akselerasi Apple Silicon (MPS / Metal)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("⚡ Perangkat Eksekusi: Apple Silicon GPU (MPS Metal Acceleration)")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print("⚡ Perangkat Eksekusi: NVIDIA CUDA GPU")
    else:
        device = torch.device("cpu")
        print("⚡ Perangkat Eksekusi: CPU")

    # 1. Memuat Tokenizer & Model Terlatih
    print(f"📥 Memuat tokenizer & bobot model terlatih dari: {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()

    # Ekstrak label mapping dari model config terlatih
    if hasattr(model.config, 'id2label') and model.config.id2label:
        label_map = {int(k): v for k, v in model.config.id2label.items()}
    else:
        label_map = FALLBACK_LABEL_MAP

    if model.num_labels != 9:
        raise ValueError(
            f"FATAL: Model memiliki {model.num_labels} output kelas, "
            f"tetapi taksonomi Plutchik MBG mensyaratkan tepat 9 kelas (8 polar + Netral)!"
        )

    print("✅ Model IndoBERT fine-tuned 9-kelas berhasil diverifikasi dan dimuat!")
    print(f"   Taksonomi Emosi: {label_map}")

    # 2. Membaca Data
    if input_path.suffix == ".parquet":
        df = pd.read_parquet(input_path)
    else:
        df = pd.read_csv(input_path)

    if sample:
        df = df.head(sample).copy()
        print(f"ℹ️  Menggunakan sampel: {len(df):,} baris")

    # Deteksi Varian Teks
    if text_col is None:
        if "clean_text" in df.columns:
            text_col = "clean_text"
        elif "processed_text" in df.columns:
            text_col = "processed_text"
        else:
            text_col = "text"

    print(f"ℹ️  Varian Kolom Teks Dipakai: '{text_col}'")
    if text_col == "clean_text":
        print("   -> Varian 1 (Context-Preserving): Mempertahankan negasi & ekspresi emosi informal.")
    elif text_col == "processed_text":
        print("   -> Varian 2 (Sastrawi Stemmed): Morfologi dasar & stopwords dieliminasi.")

    texts = df[text_col].fillna("").astype(str).tolist()

    # 3. Batch Tokenisasi & Inferensi
    print(f"🔄 Menjalankan inferensi IndoBERT pada {len(texts):,} teks...")
    predicted_labels = []
    predicted_ids = []
    confidence_scores = []

    with torch.no_grad():
        for i in tqdm(range(0, len(texts), batch_size), desc="IndoBERT Inference"):
            batch_texts = texts[i:i + batch_size]
            encoded = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=128,
                return_tensors="pt"
            ).to(device)

            outputs = model(**encoded)
            probs = torch.softmax(outputs.logits, dim=1)
            conf, preds = torch.max(probs, dim=1)

            for p, c in zip(preds.cpu().tolist(), conf.cpu().tolist()):
                predicted_ids.append(p)
                predicted_labels.append(label_map.get(p, f"Kelas_{p}"))
                confidence_scores.append(round(c, 4))

    # 4. Simpan Hasil
    df["indobert_predicted_emotion"] = predicted_labels
    df["indobert_predicted_id"] = predicted_ids
    df["indobert_confidence"] = confidence_scores

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False, compression="snappy")
    else:
        df.to_csv(output_path, index=False)

    print("\n" + "=" * 80)
    print("🎉 SELESAI INFERENSI INDOBERT")
    print(f"Total Baris Diproses    : {len(df):,}")
    print(f"File Hasil Disimpan ke  : {output_path}")
    print("Distribusi Prediksi Emosi:")
    print(df["indobert_predicted_emotion"].value_counts())
    print("=" * 80)

    # Tampilkan 3 contoh hasil
    print("\nContoh 3 baris hasil prediksi:")
    for idx, row in df.head(3).iterrows():
        print(f"[{idx+1}] Teks     : {str(row[text_col])[:80]}...")
        print(f"    Prediksi : {row['indobert_predicted_emotion']} (ID: {row['indobert_predicted_id']}, Confidence: {row['indobert_confidence']:.2%})\n")

    return df

def main():
    parser = argparse.ArgumentParser(description="Inferensi IndoBERT Fine-Tuned (3 Epochs) pada Data MBG")
    parser.add_argument("--input", default=str(DEFAULT_INPUT_PARQUET), help="Berkas input (.parquet atau .csv)")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PARQUET), help="Berkas output (.parquet atau .csv)")
    parser.add_argument("--model-path", default=DEFAULT_MODEL_PATH, help="Path model IndoBERT terlatih")
    parser.add_argument("--text-col", default=None, choices=["clean_text", "processed_text", "text"], help="Varian teks yang dianalisis")
    parser.add_argument("--batch-size", type=int, default=32, help="Ukuran batch inferensi (default: 32)")
    parser.add_argument("--sample", type=int, default=None, help="Batas jumlah baris sampel untuk uji cepat")

    args = parser.parse_args()
    run_indobert_pipeline(
        input_file=args.input,
        output_file=args.output,
        model_path=args.model_path,
        text_col=args.text_col,
        batch_size=args.batch_size,
        sample=args.sample
    )

if __name__ == "__main__":
    main()
