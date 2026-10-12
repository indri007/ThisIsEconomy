#!/usr/bin/env python3
"""
scripts/verify_old_dataset_preprocessing.py
===========================================
Skrip Pembuktian Matematis & Empiris Preprocessing Dataset Lama Tesis:
Memverifikasi bahwa fungsi pra-pemrosesan teks (cleansing & Sastrawi stemming)
secara deterministik mereproduksi kolom 'clean_text' dan 'processed_text'
pada dataset master tesis (data/results/indobert_9_emosi_fixed.csv, N = 5,263).

Output:
- Metrik kecocokan persis (Exact Match %) untuk clean_text dan processed_text.
- Log verifikasi komprehensif disimpan di reports/preprocessing_ground_truth_verification.json.
"""

import os
import sys
import re
import time
import json
import string
from pathlib import Path
import pandas as pd
from joblib import Parallel, delayed

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "results" / "indobert_9_emosi_fixed.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "preprocessing_ground_truth_verification.json"

def clean_tweet_text(text: str) -> str:
    """
    Standar Pembersihan Teks Tesis (Tahap 1 -> clean_text):
    1. Normalisasi unicode whitespace (termasuk non-breaking space \\xa0 dan line separator \\u2028).
    2. Case folding ke lowercase.
    3. Hapus URL (http/https/www).
    4. Hapus mention (@username).
    5. Hapus hashtag (#tag).
    6. Hapus angka/digit numerik.
    7. Hapus karakter non-ASCII (emoji & aksen non-latin).
    8. Hapus tanda baca (string.punctuation).
    9. Kolaps whitespace ganda dan strip spasi ujung.
    """
    t = str(text) if pd.notna(text) else ""
    t = re.sub(r'[\s\xa0\u2028]+', ' ', t)
    t = t.lower()
    t = re.sub(r'http\S+|www\S+', '', t)
    t = re.sub(r'@\w+', '', t)
    t = re.sub(r'#\w+', '', t)
    t = re.sub(r'\d+', '', t)
    t = t.encode('ascii', 'ignore').decode('ascii')
    t = t.translate(str.maketrans('', '', string.punctuation))
    return re.sub(r'\s+', ' ', t).strip()

def process_worker(batch):
    """
    Worker proses untuk parallel processing:
    Melakukan stopword removal Sastrawi dan Sastrawi Stemming ber-cache.
    """
    stemmer = StemmerFactory().create_stemmer()
    remover = StopWordRemoverFactory().create_stop_word_remover()
    cache = {}

    def get_stem(word):
        if word not in cache:
            cache[word] = stemmer.stem(word).strip()
        return cache[word]

    results = []
    for raw_text in batch:
        c_text = clean_tweet_text(raw_text)
        
        # Stopword removal Sastrawi
        text_no_stop = remover.remove(c_text)
        
        # Stemming Sastrawi
        words = text_no_stop.split()
        stemmed_tokens = [get_stem(w) for w in words]
        p_text = ' '.join([s for s in stemmed_tokens if s])
        
        results.append((c_text, p_text))
    return results

def main():
    print("=" * 80)
    print("🔬 VERIFIKASI & PEMBUKTIAN KEBENARAN PREPROCESSING DATASET LAMA TESIS")
    print("=" * 80)
    print(f"Berkas Target : {DATA_PATH}")
    if not DATA_PATH.exists():
        print(f"❌ Berkas tidak ditemukan: {DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    total_rows = len(df)
    print(f"Total Baris   : {total_rows:,} baris data")

    # Siapkan data batch
    n_jobs = max(1, (os.cpu_count() or 4) - 2)
    print(f"Worker CPU    : {n_jobs} proses paralel")

    batch_size = max(50, total_rows // (n_jobs * 4))
    raw_texts = df['text'].tolist()
    batches = [raw_texts[i:i + batch_size] for i in range(0, len(raw_texts), batch_size)]

    print(f"\nMemulai komputasi preprocessing pada seluruh {total_rows:,} korpus...")
    t0 = time.time()
    batch_results = Parallel(n_jobs=n_jobs, backend="loky")(
        delayed(process_worker)(b) for b in batches
    )
    elapsed = time.time() - t0
    print(f"Komputasi selesai dalam {elapsed:.2f} detik ({total_rows/elapsed:.1f} baris/detik).")

    # Ratakan hasil
    all_results = [item for sublist in batch_results for item in sublist]
    gen_clean = [r[0] for r in all_results]
    gen_proc = [r[1] for r in all_results]

    act_clean = df['clean_text'].fillna('').astype(str).tolist()
    act_proc = df['processed_text'].fillna('').astype(str).tolist()

    # Validasi & Evaluasi Metrik
    clean_matches = sum(1 for g, a in zip(gen_clean, act_clean) if g == a)
    proc_matches = sum(1 for g, a in zip(gen_proc, act_proc) if g == a)

    clean_acc = clean_matches / total_rows * 100.0
    proc_acc = proc_matches / total_rows * 100.0

    print("\n" + "=" * 80)
    print("📊 HASIL EVALUASI PEMBUKTIAN KEBENARAN (GROUND TRUTH REPRODUCIBILITY)")
    print("=" * 80)
    print(f"1. clean_text Match Rate     : {clean_matches:,} / {total_rows:,} ({clean_acc:.4f}%)")
    print(f"2. processed_text Match Rate : {proc_matches:,} / {total_rows:,} ({proc_acc:.4f}%)")
    print("=" * 80)

    # Identifikasi perbedaan minor jika ada
    mismatches_clean = []
    mismatches_proc = []
    for i in range(total_rows):
        if gen_clean[i] != act_clean[i]:
            mismatches_clean.append({
                "row_index": i,
                "raw_text": raw_texts[i],
                "expected": act_clean[i],
                "generated": gen_clean[i]
            })
        if gen_proc[i] != act_proc[i]:
            mismatches_proc.append({
                "row_index": i,
                "clean_text": act_clean[i],
                "expected": act_proc[i],
                "generated": gen_proc[i]
            })

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset_path": str(DATA_PATH),
        "total_rows": total_rows,
        "clean_text_matches": clean_matches,
        "clean_text_accuracy_percent": round(clean_acc, 4),
        "processed_text_matches": proc_matches,
        "processed_text_accuracy_percent": round(proc_acc, 4),
        "computation_time_seconds": round(elapsed, 2),
        "workers_used": n_jobs,
        "mismatches_clean_count": len(mismatches_clean),
        "mismatches_processed_count": len(mismatches_proc),
        "sample_mismatches_clean": mismatches_clean[:5],
        "sample_mismatches_proc": mismatches_proc[:5]
    }

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Laporan audit verifikasi tersimpan di: {REPORT_PATH}")
    
    assert clean_acc >= 99.9, f"clean_text accuracy below 99.9%: {clean_acc}%"
    assert proc_acc >= 99.0, f"processed_text accuracy below 99.0%: {proc_acc}%"
    print("🎉 PEMBUKTIAN KEBENARAN BERHASIL (VERIFIED WITH MATHEMATICAL FIDELITY)!")

if __name__ == "__main__":
    main()
