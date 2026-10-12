"""
pipelines_30m/test_pipeline.py
==============================
Unit & Integration Test untuk Pipeline 30M Terisolasi:
1. Menguji fungsi pembersihan teks (cleansing, slang, stopword, stemming Sastrawi).
2. Memverifikasi ekivalensi hasil antara mode fast cached dan fungsi referensi tesis.
3. Menguji pipeline end-to-end pada batch sampel kecil.
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path

# Pastikan root proyek masuk ke sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import pytest

from pipelines_30m.config import NORM_DICT, get_stopwords_set
from pipelines_30m.clean_30m_pipeline import FastTextCleaner, run_pipeline

def test_text_cleaner_components():
    stopwords_set = get_stopwords_set()
    cleaner = FastTextCleaner(NORM_DICT, stopwords_set, strict=False)

    # 1. Test URL, RT, Mentions & Lowercase
    raw_text = "RT @jokowi: Kunjungi kami di https://kemensos.go.id untuk info MBG! #gizi"
    cleaned = cleaner.clean(raw_text)
    assert "rt" not in cleaned.split()
    assert "@jokowi" not in cleaned
    assert "https" not in cleaned
    assert "kunjungi" not in cleaned  # Harus ter-stem menjadi "kunjung"
    assert "kunjung" in cleaned

    # 2. Test Normalisasi Slang (norm_dict)
    # 'yg' -> 'yang' -> stopword terbuang
    # 'dgn' -> 'dengan' -> stopword terbuang
    # 'bgt' -> 'banget'
    raw_text2 = "Anak-anak sekolah senang bgt makan makanan bergizi"
    cleaned2 = cleaner.clean(raw_text2)
    assert "banget" in cleaned2
    assert "makan" in cleaned2
    assert "gizi" in cleaned2  # bergizi -> gizi

def test_equivalence_strict_vs_fast():
    stopwords_set = get_stopwords_set()
    cleaner_strict = FastTextCleaner(NORM_DICT, stopwords_set, strict=True)
    cleaner_fast = FastTextCleaner(NORM_DICT, stopwords_set, strict=False)

    test_samples = [
        "Program makan bergizi gratis di sekolah dasar jakarta",
        "Pemerintah membagikan makanan kepada anak-anak dgn tertib",
        "ANIES GANJAR nawarin sekolah gratis, lu pilih nasi 10000",
        "Kalo anak sekolah mana tendanya panas banget"
    ]

    for s in test_samples:
        res_strict = cleaner_strict.clean(s)
        res_fast = cleaner_fast.clean(s)
        assert res_strict == res_fast, f"Mismatch!\nStrict: {res_strict}\nFast: {res_fast}"

def test_mini_pipeline_end_to_end():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sample_csv = tmp_path / "sample_input.csv"
        out_dir = tmp_path / "output_test"

        # Buat dummy DataFrame
        df_sample = pd.DataFrame({
            "id": [1, 2, 3],
            "text": [
                "Program MBG sangat membantu siswa di sekolah dasar",
                "Makan gratis bergizi bikin anak-anak sehat dan cerdas",
                "Pemerintah bagi porsi makanan gratis utk masyarakat"
            ],
            "created_at": ["2026-05-17", "2026-05-18", "2026-05-19"]
        })
        df_sample.to_csv(sample_csv, index=False)

        # Jalankan pipeline pada sample
        run_pipeline(
            input_csv=sample_csv,
            output_dir=out_dir,
            chunk_size=2,
            batch_size=2,
            n_workers=2,
            output_format="parquet"
        )

        out_files = list(out_dir.glob("clean_30m_part_*.parquet"))
        assert len(out_files) >= 1, f"Expected clean_30m_part_*.parquet, got: {list(out_dir.glob('*'))}"

        # Cek isi file hasil
        df_out = pd.read_parquet(out_files[0])
        assert "clean_text" in df_out.columns
        assert "processed_text" in df_out.columns
        assert len(df_out) > 0
        assert isinstance(df_out["clean_text"].iloc[0], str)

def test_naming_convention_30m():
    from pipelines_30m.config import DEFAULT_INPUT_CSV
    assert "30juta" in str(DEFAULT_INPUT_CSV) or "1juta" in str(DEFAULT_INPUT_CSV)
    assert DEFAULT_INPUT_CSV.exists(), f"Input CSV file not found: {DEFAULT_INPUT_CSV}"

def test_dual_variants_context_vs_sastrawi():
    stopwords_set = get_stopwords_set()
    cleaner = FastTextCleaner(NORM_DICT, stopwords_set, strict=False)

    # Teks dengan negasi & bahasa informal
    sample = "program mbg ini tidak bagus sama sekali dan bgt mengecewakan"
    c_text, p_text = cleaner.clean_both(sample)

    # Varian 1 (clean_text): Mempertahankan negasi 'tidak' dan struktur kalimat untuk Transformer
    assert "tidak" in c_text
    assert "bagus" in c_text
    assert "mengecewakan" in c_text

    # Varian 2 (processed_text): Sastrawi stemming & stopword removal
    assert "kecewa" in p_text or "mengecewakan" in p_text

def test_ground_truth_reproducibility():
    """Menguji kecocokan 100% pada baris sampel dataset master tesis."""
    thesis_data_path = PROJECT_ROOT / "data" / "results" / "indobert_9_emosi_fixed.csv"
    if not thesis_data_path.exists():
        pytest.skip("Thesis master data file not found")

    df_thesis = pd.read_csv(thesis_data_path).head(20)
    stopwords_set = get_stopwords_set()
    cleaner = FastTextCleaner(norm_dict={}, stopwords_set=stopwords_set, strict=False)

    for idx, row in df_thesis.iterrows():
        c_gen, p_gen = cleaner.clean_both(row["text"])
        assert c_gen == str(row["clean_text"]).strip(), f"Mismatch clean_text at row {idx}"
        assert p_gen == str(row["processed_text"]).strip(), f"Mismatch processed_text at row {idx}"

def test_indobert_fine_tuned_inference_sanity():
    """Menguji inferensi model IndoBERT fine-tuned 3 epoch."""
    from pipelines_30m.indobert_inference import run_indobert_pipeline, DEFAULT_MODEL_PATH
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        dummy_in = tmp_path / "test_input.parquet"
        dummy_out = tmp_path / "test_output.parquet"

        df_dummy = pd.DataFrame({
            "clean_text": [
                "makanan bergizi gratis sangat bermanfaat untuk siswa sekolah",
                "anggaran program mbg diduga dikorupsi sangat mengecewakan"
            ],
            "processed_text": [
                "makan gizi gratis manfaat siswa sekolah",
                "anggar program mbg duga korupsi sangat kecewa"
            ]
        })
        df_dummy.to_parquet(dummy_in, index=False)

        res_df = run_indobert_pipeline(
            input_file=dummy_in,
            output_file=dummy_out,
            model_path=DEFAULT_MODEL_PATH,
            batch_size=2,
            sample=2
        )

        assert "indobert_predicted_emotion" in res_df.columns
        assert "indobert_predicted_id" in res_df.columns
        assert "indobert_confidence" in res_df.columns
        valid_labels = {'Marah', 'Jijik', 'Takut', 'Bahagia', 'Percaya', 'Netral', 'Sedih', 'Tertarik', 'Kaget'}
        for pred in res_df["indobert_predicted_emotion"]:
            assert pred in valid_labels, f"Unexpected predicted emotion label: {pred}"

if __name__ == "__main__":
    test_text_cleaner_components()
    test_equivalence_strict_vs_fast()
    test_mini_pipeline_end_to_end()
    test_naming_convention_30m()
    test_dual_variants_context_vs_sastrawi()
    test_ground_truth_reproducibility()
    test_indobert_fine_tuned_inference_sanity()
    print("✅ Semua unit & integration test pipeline 30M lulus dengan sukses!")
