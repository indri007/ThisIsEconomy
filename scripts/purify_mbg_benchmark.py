"""
Script untuk memurnikan korpus benchmark anotasi emosi MBG.
Kriteria Inklusi:
- Relevan eksplisit dengan Program Makan Bergizi Gratis (MBG), Badan Gizi Nasional (BGN),
  anggaran, SPPG, uji coba makanan, keracunan, menu sekolah, atau figur kebijakan terkait.
Kriteria Eksklusi:
- Spam promosi, voucher komersial (#zonauang, #zonajajan, diskon halodoc dll).
- Bahasa asing / non-bahasa Indonesia.
- Homonim singkatan MBG (misal fandom kpop / 'Mas Bahlil Ganteng' / 'My Bini Gue' / 'My Boyfriend Gua' dll).
- Konten personal murni tanpa relasi kebijakan.
Kategori Output:
- RELEVANT
- IRRELEVANT
- REVIEW_REQUIRED
"""

import os
import re
import pandas as pd

def classify_tweet_relevance(text: str) -> tuple[str, str]:
    if not isinstance(text, str) or not text.strip():
        return "IRRELEVANT", "Teks kosong atau bukan string"
        
    t = text.lower()
    
    # 1. Non-Indonesian foreign markers
    foreign_patterns = [
        r'\bevox\b', r'\bapex team\b', r'\bmember recruitment\b', 
        r'\bvai ficar parecendo\b', r'\bwhey protein crush\b', 
        r'\bbana gurban ol dedim\b', r'\bzalımın gızı\b'
    ]
    for fp in foreign_patterns:
        if re.search(fp, t):
            return "IRRELEVANT", "Bahasa asing / bukan wacana publik Indonesia"
            
    # 2. Obvious Ads / Vouchers / Spam
    ad_patterns = [
        r'voucher diskon halodoc', r'#zonauang', r'#zonajajan', 
        r'chat dokter umum/psikolog', r'hldxcpfp', r'hldxoc1j', r'hldxhrmzp'
    ]
    for ap in ad_patterns:
        if re.search(ap, t):
            return "IRRELEVANT", "Spam promosi komersial / voucher belanja"
            
    # 3. MBG Homonym (Kpop, personal fandom, Mas Bahlil Ganteng, My Bini Gue, dll)
    homonym_patterns = [
        r'mas bahlil ganteng', r'buahlil', r'my bini gue', r'my bini gw', 
        r'my boyfriend gua', r'my bebeb gue', r'goyang mbg', r'minbege', 
        r'drakor mbg', r'dorohedoro', r'\bgravt\b', r'boynextdoor', 
        r'lolfanfest', r'switch career ke koperasi', r'kaos kaki mbg'
    ]
    for hp in homonym_patterns:
        if re.search(hp, t):
            return "IRRELEVANT", "Homonim MBG (Slang Fandom / Singkatan nama orang non-program)"
            
    # 4. Explicit Policy & Food/Nutrition Grievance Markers
    policy_patterns = [
        r'makan bergizi gratis', r'badan gizi nasional', r'\bbgn\b', r'\bsppg\b', 
        r'keracunan', r'makanan beracun', r'dapur mbg', r'uang kas pemerintah di bi', 
        r'dana 5thn mbg', r'apbn per hari 1 triliun', r'1 triliun sehari', 
        r'anak yang tiap hari makan mbg', r'karyawan mbg', r'penyaluran mbg', 
        r'program mbg', r'makan mbg', r'sisa mbg', r'menu mbg', r'kasus mbg'
    ]
    for pp in policy_patterns:
        if re.search(pp, t):
            return "RELEVANT", "Wacana kebijakan Program Makan Bergizi Gratis (MBG)"
            
    # 5. Check acronym MBG with political / grievance context
    if 'mbg' in t:
        if any(w in t for w in ['prabowo', 'gibran', 'korupsi', 'anggaran', 'negara', 'rakyat', 'sekolah', 'siswa', 'gizi']):
            return "RELEVANT", "Wacana kebijakan MBG dalam konteks tata kelola dan pemerintahan"
        return "REVIEW_REQUIRED", "Memuat akronim MBG namun konteks memerlukan klarifikasi manual"
        
    return "IRRELEVANT", "Tidak berkaitan dengan diskursus Program MBG"

def run_benchmark_purification(input_path: str, output_path: str, log_path: str):
    print(f"Loading input benchmark from: {input_path}")
    df = pd.read_csv(input_path)
    
    results = [classify_tweet_relevance(t) for t in df['text']]
    df['relevance_status'] = [r[0] for r in results]
    df['relevance_rationale'] = [r[1] for r in results]
    
    # Save purified artifact
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved purified benchmark audit to: {output_path}")
    
    # Write summary stats
    summary = df['relevance_status'].value_counts()
    print("\nBenchmark Purification Summary:")
    print(summary)
    
    with open(log_path, 'w') as f:
        f.write("# Benchmark Purification Audit Log\n\n")
        f.write(f"- Input File: `{input_path}`\n")
        f.write(f"- Output Artifact: `{output_path}`\n")
        f.write(f"- Total Rows Evaluated: {len(df)}\n\n")
        f.write("## Status Breakdown:\n")
        for k, v in summary.items():
            f.write(f"- **{k}:** {v} ({v/len(df)*100:.2f}%)\n")
        f.write("\n## Breakdown per Item:\n")
        for idx, row in df.iterrows():
            f.write(f"- `{row['annotation_id']}`: [{row['relevance_status']}] {row['relevance_rationale']} — \"{str(row['text'])[:75]}...\"\n")
            
    print(f"Audit log written to: {log_path}")

if __name__ == "__main__":
    src = "data/multi_annotator_batch_100_GOLD.csv"
    if not os.path.exists(src):
        src = "/Users/jevin/Downloads/SUBMISI_JCMC_OXFORD_SCOPUS_Q1/multi_annotator_batch_100_GOLD.csv"
    out = "data/annotation/purified_benchmark_batch_100_audit.csv"
    log = "reports/scientific_validation/BENCHMARK_PURIFICATION_LOG.md"
    run_benchmark_purification(src, out, log)
