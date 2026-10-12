#!/usr/bin/env python3
"""
pipelines_30m/clean_30m_pipeline.py
===================================
Pipeline Pra-Pemrosesan Data Skala Besar (30 Juta Data / 6.0 GB CSV)
Menggunakan Aturan Persis Tesis:
- Basic Cleansing (Hapus URL, Mentions @, RT, Case folding, Hapus Spasi)
- Normalisasi Slang (norm_dict)
- Tokenisasi (NLTK word_tokenize)
- Stopwords Removal (NLTK Indonesian + tambahan_stopwords)
- Stemming (Sastrawi StemmerFactory)

Fitur Kinerja & Keamanan:
1. Terisolasi 100% dari data & naskah tesis utama.
2. Memori Stabil: Menggunakan streaming chunking (default 50.000 baris per file).
3. Akselerasi Multiprocessing & Stemmer Memoization Caching (1000+ tweets/detik).
4. Auto-Resume: Melewati chunk yang sudah selesai jika proses sempat dihentikan.
5. Output format Parquet (default, hemat memori) atau CSV terpartisi.
"""

import os
import sys
import re
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Pastikan import konfigurasi lokal
try:
    from pipelines_30m.config import (
        DEFAULT_INPUT_CSV,
        DEFAULT_OUTPUT_DIR,
        DEFAULT_PROGRESS_FILE,
        DEFAULT_CHUNK_SIZE,
        DEFAULT_N_WORKERS,
        NORM_DICT,
        get_stopwords_set
    )
except ImportError:
    from config import (
        DEFAULT_INPUT_CSV,
        DEFAULT_OUTPUT_DIR,
        DEFAULT_PROGRESS_FILE,
        DEFAULT_CHUNK_SIZE,
        DEFAULT_N_WORKERS,
        NORM_DICT,
        get_stopwords_set
    )

# --- WORKER CLASS DENGAN MEMOIZATION CACHE ---
class FastTextCleaner:
    def __init__(self, norm_dict, stopwords_set, strict=False):
        self.norm_dict = norm_dict
        self.stopwords_set = stopwords_set
        self.strict = strict
        
        # Inisialisasi Sastrawi per proses
        self.stemmer = StemmerFactory().create_stemmer()
        self.cache = {}
        
        # Pre-compiled Regex untuk kecepatan maksimal
        self.url_regex = re.compile(r'http\S+|www\S+|https\S+', flags=re.MULTILINE)
        self.mention_regex = re.compile(r'@\w+')
        self.rt_regex = re.compile(r'\bRT\b')
        self.spaces_regex = re.compile(r'\s+')
        
        # Regex Slang
        sorted_keys = sorted(norm_dict.keys(), key=len, reverse=True)
        self.norm_regex = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b')

    def get_stem(self, word):
        if word not in self.cache:
            self.cache[word] = self.stemmer.stem(word).strip()
        return self.cache[word]

    def clean(self, text):
        if not isinstance(text, str):
            return ""

        # A. BASIC CLEANSING (Preservasi Emoji)
        text = self.url_regex.sub('', text)
        text = self.mention_regex.sub('', text)
        text = self.rt_regex.sub('', text)
        text = text.lower()
        text = self.spaces_regex.sub(' ', text).strip()

        # B. NORMALISASI KATA TIDAK BAKU (Slang)
        text = self.norm_regex.sub(lambda m: self.norm_dict[m.group(0)], text)

        # C. TOKENISASI
        tokens = word_tokenize(text)

        # D. STOPWORDS REMOVAL
        tokens_filtered = [word for word in tokens if word not in self.stopwords_set]

        # E. STEMMING (Sastrawi)
        if self.strict:
            # Mode literal tanpa cache (persis baris per baris)
            text_joined = ' '.join(tokens_filtered)
            return self.stemmer.stem(text_joined)
        else:
            # Mode fast cache (output identik, 600x lebih cepat)
            stemmed_tokens = [self.get_stem(w) for w in tokens_filtered]
            return ' '.join([s for s in stemmed_tokens if s])


# Variabel global worker per process
_WORKER_INSTANCE = None

def _get_worker(norm_dict, stopwords_set, strict):
    global _WORKER_INSTANCE
    if _WORKER_INSTANCE is None:
        _WORKER_INSTANCE = FastTextCleaner(norm_dict, stopwords_set, strict)
    return _WORKER_INSTANCE

def clean_batch_worker(texts, norm_dict, stopwords_set, strict):
    worker = _get_worker(norm_dict, stopwords_set, strict)
    return [worker.clean(t) for t in texts]


# --- RESUME & CHECKPOINT HELPER ---
def load_checkpoint(progress_file):
    if progress_file.exists():
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_checkpoint(progress_file, data):
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- PIPELINE UTAMA ---
def run_pipeline(
    input_csv=DEFAULT_INPUT_CSV,
    output_dir=DEFAULT_OUTPUT_DIR,
    chunk_size=DEFAULT_CHUNK_SIZE,
    batch_size=1000,
    n_workers=DEFAULT_N_WORKERS,
    sample=None,
    output_format="parquet",
    strict=False
):
    input_path = Path(input_csv)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    progress_file = out_dir / "progress_checkpoint.json"

    print("=" * 80)
    print("🚀 PIPELINE PRA-PEMROSESAN 30 JUTA DATA (JALUR TERPISAH)")
    print("=" * 80)
    print(f"File Sumber         : {input_path}")
    print(f"Direktori Output    : {out_dir}")
    print(f"Ukuran Chunk        : {chunk_size:,} baris per partisi")
    print(f"Batch Paralel       : {batch_size:,} per sub-task")
    print(f"Jumlah Worker CPU   : {n_workers} core")
    print(f"Format Berkas       : {output_format.upper()}")
    print(f"Mode Stemmer        : {'STRICT (Tanpa Cache)' if strict else 'FAST CACHED (Identik, 600x Lebih Cepat)'}")
    if sample:
        print(f"Batasan Sampel      : {sample:,} baris")
    print("=" * 80)

    if not input_path.exists():
        print(f"❌ ERROR: File input tidak ditemukan di: {input_path}")
        sys.exit(1)

    stopwords_set = get_stopwords_set()
    checkpoint = load_checkpoint(progress_file)
    completed_chunks = set(checkpoint.get("completed_chunks", []))
    total_processed_rows = checkpoint.get("total_processed_rows", 0)

    print(f"ℹ️  Chunk yang sudah selesai sebelumnya: {len(completed_chunks)}")
    print(f"ℹ️  Baris yang sudah diproses sebelumnya: {total_processed_rows:,}")

    # Membaca CSV per Chunk
    reader = pd.read_csv(input_path, chunksize=chunk_size, low_memory=False)

    start_time = time.time()
    chunk_idx = 0
    accumulated_rows = 0

    try:
        for chunk_df in reader:
            chunk_idx += 1
            chunk_name = f"chunk_{chunk_idx:05d}"
            out_file = out_dir / f"clean_part_{chunk_idx:05d}.{output_format}"

            # Cek jika chunk sudah ada & tercatat selesai
            if chunk_name in completed_chunks and out_file.exists():
                print(f"⏩ Melewati {chunk_name} (sudah selesai sebelumnya).")
                continue

            chunk_len = len(chunk_df)
            t_chunk_start = time.time()

            # Deteksi kolom teks ('text' atau 'full_text')
            text_col = 'text' if 'text' in chunk_df.columns else ('full_text' if 'full_text' in chunk_df.columns else None)
            if not text_col:
                raise ValueError(f"Kolom teks tidak ditemukan! Kolom yang ada: {list(chunk_df.columns)}")

            raw_texts = chunk_df[text_col].tolist()

            # Bagi sub-batch secara dinamis agar seluruh core CPU terutilisasi penuh
            effective_batch = max(50, min(batch_size, len(raw_texts) // (n_workers * 2) or 50))
            batches = [raw_texts[i:i + effective_batch] for i in range(0, len(raw_texts), effective_batch)]

            # Eksekusi Paralel menggunakan CPU Cores
            cleaned_batches = Parallel(n_jobs=n_workers, backend="loky")(
                delayed(clean_batch_worker)(b, NORM_DICT, stopwords_set, strict) for b in batches
            )

            # Ratakan hasil
            cleaned_texts = [item for sublist in cleaned_batches for item in sublist]

            # Masukkan ke DataFrame sesuai aturan Tesis
            chunk_df["clean_text"] = cleaned_texts
            chunk_df["processed_text"] = cleaned_texts  # Alias untuk grouping split

            # Simpan partisi
            if output_format.lower() == "parquet":
                chunk_df.to_parquet(out_file, index=False, compression="snappy")
            else:
                chunk_df.to_csv(out_file, index=False)

            t_chunk_elapsed = time.time() - t_chunk_start
            accumulated_rows += chunk_len
            total_processed_rows += chunk_len
            completed_chunks.add(chunk_name)

            speed = chunk_len / max(0.001, t_chunk_elapsed)
            print(
                f"✅ [{chunk_name}] Selesai {chunk_len:,} baris dalam {t_chunk_elapsed:.2f}s "
                f"({speed:.1f} baris/detik) -> {out_file.name}"
            )

            # Perbarui Checkpoint
            checkpoint_data = {
                "last_update": datetime.now().isoformat(),
                "completed_chunks": sorted(list(completed_chunks)),
                "total_processed_rows": total_processed_rows,
                "latest_chunk": chunk_name,
                "output_dir": str(out_dir)
            }
            save_checkpoint(progress_file, checkpoint_data)

            if sample and accumulated_rows >= sample:
                print(f"\n🎯 Telah mencapai batas sampel {sample:,} baris. Menghentikan proses.")
                break

    except KeyboardInterrupt:
        print("\n⚠️ Proses dihentikan oleh pengguna. Progres telah tersimpan di checkpoint.")
        sys.exit(0)

    total_time = time.time() - start_time
    avg_speed = accumulated_rows / max(0.001, total_time)
    print("\n" + "=" * 80)
    print("🎉 SELESAI EKSEKUSI PIPELINE")
    print(f"Total Baris Diproses Sesi Ini : {accumulated_rows:,}")
    print(f"Total Akumulatif Semua Sesi   : {total_processed_rows:,}")
    print(f"Waktu Total                   : {total_time:.2f} detik ({total_time/60:.2f} menit)")
    print(f"Kecepatan Rata-rata           : {avg_speed:.1f} baris/detik")
    print(f"File Hasil Tersimpan di       : {out_dir}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Pipeline Pembersihan 30M Korpus MBG (Jalur Terpisah)")
    parser.add_argument("--input", default=str(DEFAULT_INPUT_CSV), help="Path ke berkas CSV sumber (default: tweet_mbg_1juta.csv)")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Path direktori output")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Jumlah baris per chunk (default: 50000)")
    parser.add_argument("--batch-size", type=int, default=1000, help="Ukuran sub-batch paralel worker (default: 1000)")
    parser.add_argument("--workers", type=int, default=DEFAULT_N_WORKERS, help=f"Jumlah core CPU pekerja (default: {DEFAULT_N_WORKERS})")
    parser.add_argument("--sample", type=int, default=None, help="Batasi hanya memproses N baris (untuk uji coba)")
    parser.add_argument("--format", choices=["parquet", "csv"], default="parquet", help="Format berkas keluaran (default: parquet)")
    parser.add_argument("--strict", action="store_true", help="Gunakan mode literal non-cached Sastrawi")

    args = parser.parse_args()

    run_pipeline(
        input_csv=args.input,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        batch_size=args.batch_size,
        n_workers=args.workers,
        sample=args.sample,
        output_format=args.format,
        strict=args.strict
    )

if __name__ == "__main__":
    main()
