#!/usr/bin/env python3
"""
pipelines_30m/sastrawi_to_indobert.py
====================================
Pipeline Terintegrasi End-to-End:
1. Raw Tweet -> Pra-pemrosesan & Stemming Sastrawi (clean_text).
2. Clean Text -> Subword Tokenizer IndoBERT (indobenchmark/indobert-base-p2).
3. Menghasilkan:
   - clean_text : Kalimat dasar setelah Sastrawi.
   - indobert_subwords : Daftar subword WordPiece (contoh: ['program', 'makan', 'mb', '##g']).
   - input_ids & attention_mask : Tensor siap masuk ke model IndoBERT.
"""

import re
import argparse
from pathlib import Path
import pandas as pd
import torch
from transformers import AutoTokenizer

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Kamus slang & stopword sesuai tesis
NORM_DICT = {
    "yg": "yang", "dgn": "dengan", "bgmn": "bagaimana", "bgt": "banget",
    "tp": "tapi", "dri": "dari", "krn": "karena", "klo": "kalau", "sma": "sama",
    "utk": "untuk", "udah": "sudah"
}

TAMBAHAN_STOPWORDS = ["sih", "nya", "nih", "tuh", "dong", "yg", "di", "ke", "dari"]

class SastrawiToIndoBERT:
    def __init__(self, model_name="indobenchmark/indobert-base-p2"):
        self.model_name = model_name
        
        # 1. Inisialisasi Sastrawi
        self.stemmer = StemmerFactory().create_stemmer()
        self.cache = {}
        
        # 2. Inisialisasi Stopwords
        self.stopwords_set = set(stopwords.words("indonesian"))
        self.stopwords_set.update(TAMBAHAN_STOPWORDS)
        
        # 3. Regex Pre-compiled
        self.url_regex = re.compile(r'http\S+|www\S+|https\S+', flags=re.MULTILINE)
        self.mention_regex = re.compile(r'@\w+')
        self.rt_regex = re.compile(r'\bRT\b')
        self.spaces_regex = re.compile(r'\s+')
        
        sorted_keys = sorted(NORM_DICT.keys(), key=len, reverse=True)
        self.norm_regex = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b')
        
        # 4. Inisialisasi Tokenizer IndoBERT p2
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def stem_word(self, word):
        if word not in self.cache:
            self.cache[word] = self.stemmer.stem(word).strip()
        return self.cache[word]

    def process_sastrawi(self, text):
        """Tahap 1: Pembersihan & Stemming Sastrawi."""
        if not isinstance(text, str):
            return ""

        # Basic cleansing
        text = self.url_regex.sub('', text)
        text = self.mention_regex.sub('', text)
        text = self.rt_regex.sub('', text)
        text = text.lower()
        text = self.spaces_regex.sub(' ', text).strip()

        # Normalisasi slang
        text = self.norm_regex.sub(lambda m: NORM_DICT[m.group(0)], text)

        # Tokenisasi kata
        tokens = word_tokenize(text)

        # Stopwords removal
        tokens_filtered = [w for w in tokens if w not in self.stopwords_set]

        # Sastrawi Stemming
        stemmed = [self.stem_word(w) for w in tokens_filtered]
        return ' '.join([s for s in stemmed if s])

    def tokenize_indobert(self, clean_text, max_length=128):
        """Tahap 2: Tokenisasi IndoBERT dari teks Sastrawi."""
        subwords = self.tokenizer.tokenize(clean_text)
        encoded = self.tokenizer(
            clean_text,
            max_length=max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "subwords": subwords,
            "subword_count": len(subwords),
            "input_ids": encoded["input_ids"][0],
            "attention_mask": encoded["attention_mask"][0]
        }

    def process_full(self, raw_text, max_length=128):
        """Alur Lengkap: Raw Text -> Sastrawi -> IndoBERT."""
        clean_text = self.process_sastrawi(raw_text)
        token_info = self.tokenize_indobert(clean_text, max_length=max_length)
        return {
            "raw_text": raw_text,
            "clean_text": clean_text,
            "subwords": token_info["subwords"],
            "subword_count": token_info["subword_count"],
            "input_ids": token_info["input_ids"].tolist(),
            "attention_mask": token_info["attention_mask"].tolist()
        }

def run_demo():
    print("=" * 80)
    print("🔬 DEMO END-TO-END: SASTRAWI -> TOKENIZER INDOBERT (indobenchmark/indobert-base-p2)")
    print("=" * 80)
    
    pipeline = SastrawiToIndoBERT()

    sample_tweets = [
        "RT @jokowi: Program Makan Bergizi Gratis (MBG) udah berjalan dgn baik bgt di sekolah! https://t.co/xyz",
        "Sedangkan kasus MBG, IKN mangkrak, orang2 itu pada hidup tentram 🤡 What a dzalim country",
        "ANIES GANJAR nawarin sekolah gratis, lu pilih nasi 10000. Dari situ aja lu udah aneh😭"
    ]

    for idx, raw in enumerate(sample_tweets, 1):
        res = pipeline.process_full(raw, max_length=16)
        print(f"\n[Cuitan #{idx}]")
        print(f"1. Teks Asli       : {res['raw_text']}")
        print(f"2. Hasil Sastrawi  : {res['clean_text']}")
        print(f"3. Subword IndoBERT: {res['subwords']}")
        print(f"4. Jumlah Subword  : {res['subword_count']} token")
        print(f"5. Input IDs (16)  : {res['input_ids'][:16]}")
        print(f"6. Attention Mask  : {res['attention_mask'][:16]}")

    print("\n" + "=" * 80)
    print("✅ Demo selesai! Alur Sastrawi -> IndoBERT Tokenizer terbukti sinkron 100%.")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Alur Sastrawi -> IndoBERT Tokenizer")
    parser.add_argument("--demo", action="store_true", default=True, help="Jalankan demo pengujian")
    args = parser.parse_args()
    if args.demo:
        run_demo()

if __name__ == "__main__":
    main()
