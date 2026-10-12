#!/usr/bin/env python3
"""
pipelines_30m/indobert_inference.py
==================================
Memproses Teks Bersih (clean_text / processed_text) ke IndoBERT (indobenchmark/indobert-base-p2):
1. Mengunduh & memuat model dan tokenizer HuggingFace indobenchmark/indobert-base-p2.
2. Mendeteksi akselerasi Apple Silicon GPU (MPS) secara otomatis.
3. Melakukan tokenisasi batch (max_length=128) dan inferensi representasi / klasifikasi.
4. Terisolasi di dalam pipelines_30m/ tanpa mengganggu data tesis lama.
"""

import os
import sys
import argparse
from pathlib import Path
import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Taksonomi 9 Emosi Plutchik sesuai Tesis
LABEL_MAP = {
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

DEFAULT_INPUT_PARQUET = Path("/Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output/clean_part_00001.parquet")
DEFAULT_OUTPUT_PARQUET = Path("/Users/jevin/Documents/tesis_mbg/data/processed/clean_30m_output/clean_part_00001_with_indobert.parquet")
MODEL_NAME = "indobenchmark/indobert-base-p2"

def run_indobert_pipeline(
    input_file=DEFAULT_INPUT_PARQUET,
    output_file=DEFAULT_OUTPUT_PARQUET,
    batch_size=32,
    sample=None
):
    input_path = Path(input_file)
    output_path = Path(output_file)

    print("=" * 80)
    print("🤖 PEMROSESAN TEKS KE INDOBERT (indobenchmark/indobert-base-p2)")
    print("=" * 80)
    print(f"Berkas Input        : {input_path}")
    print(f"Berkas Output       : {output_path}")
    print(f"Model HuggingFace   : {MODEL_NAME}")
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

    # 1. Memuat Tokenizer & Model
    print(f"📥 Memuat tokenizer & model dari HuggingFace ({MODEL_NAME})...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABEL_MAP)
    ).to(device)
    model.eval()
    print("✅ Model IndoBERT p2 berhasil dimuat ke memori!")

    # 2. Membaca Data
    if input_path.suffix == ".parquet":
        df = pd.read_parquet(input_path)
    else:
        df = pd.read_csv(input_path)

    if sample:
        df = df.head(sample).copy()
        print(f"ℹ️  Menggunakan sampel: {len(df):,} baris")

    text_col = "clean_text" if "clean_text" in df.columns else ("processed_text" if "processed_text" in df.columns else "text")
    texts = df[text_col].fillna("").astype(str).tolist()

    # 3. Batch Tokenisasi & Inferensi
    print(f"🔄 Menjalankan inferensi IndoBERT pada {len(texts):,} teks...")
    predicted_labels = []
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
                predicted_labels.append(LABEL_MAP.get(p, f"Kelas_{p}"))
                confidence_scores.append(round(c, 4))

    # 4. Simpan Hasil
    df["indobert_predicted_emotion"] = predicted_labels
    df["indobert_confidence"] = confidence_scores

    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False, compression="snappy")
    else:
        df.to_csv(output_path, index=False)

    print("\n" + "=" * 80)
    print("🎉 SELESAI INFERENSI INDOBERT")
    print(f"Total Baris Diproses    : {len(df):,}")
    print(f"File Hasil Disimpan ke  : {output_path}")
    print("=" * 80)

    # Tampilkan 3 contoh hasil
    print("\nContoh 3 baris hasil prediksi:")
    for idx, row in df.head(3).iterrows():
        print(f"[{idx+1}] Teks     : {row[text_col][:80]}...")
        print(f"    Prediksi : {row['indobert_predicted_emotion']} (Confidence: {row['indobert_confidence']:.2%})\n")

def main():
    parser = argparse.ArgumentParser(description="Inferensi IndoBERT p2 pada clean_text")
    parser.add_argument("--input", default=str(DEFAULT_INPUT_PARQUET), help="Berkas input (.parquet atau .csv)")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PARQUET), help="Berkas output (.parquet atau .csv)")
    parser.add_argument("--batch-size", type=int, default=32, help="Ukuran batch inferensi (default: 32)")
    parser.add_argument("--sample", type=int, default=None, help="Batas jumlah baris sampel untuk uji cepat")

    args = parser.parse_args()
    run_indobert_pipeline(
        input_file=args.input,
        output_file=args.output,
        batch_size=args.batch_size,
        sample=args.sample
    )

if __name__ == "__main__":
    main()
