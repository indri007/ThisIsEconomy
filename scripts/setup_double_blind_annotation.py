"""
Script untuk menyiapkan template anotasi double-blind independen
dan menghitung metrik reliabilitas inter-rater (Cohen's Kappa & Krippendorff's Alpha)
secara jujur tanpa konfirmasi bias.
"""

import os
import pandas as pd
import numpy as np

def generate_double_blind_templates(purified_csv: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(purified_csv)
    
    # Hanya sertakan teks yang berstatus RELEVANT atau REVIEW_REQUIRED
    valid_candidates = df[df['relevance_status'].isin(['RELEVANT', 'REVIEW_REQUIRED'])].copy()
    
    # Buat template bersih: hanya ID dan Text, TANPA label prediksi atau anotator lain
    template_annotator_1 = pd.DataFrame({
        'item_id': valid_candidates['annotation_id'],
        'tweet_text': valid_candidates['text'],
        'assigned_emotion': '',  # Pilihan: Marah, Jijik, Takut, Bahagia, Sedih, Kaget, Percaya, Tertarik, Netral
        'confidence_1to5': '',
        'annotation_notes': '',
        'annotator_pseudonym': 'ANON_RATR_01',
        'timestamp_iso': ''
    })
    
    template_annotator_2 = pd.DataFrame({
        'item_id': valid_candidates['annotation_id'],
        'tweet_text': valid_candidates['text'],
        'assigned_emotion': '',  # Pilihan: Marah, Jijik, Takut, Bahagia, Sedih, Kaget, Percaya, Tertarik, Netral
        'confidence_1to5': '',
        'annotation_notes': '',
        'annotator_pseudonym': 'ANON_RATR_02',
        'timestamp_iso': ''
    })
    
    f1 = os.path.join(output_dir, 'DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1.csv')
    f2 = os.path.join(output_dir, 'DOUBLE_BLIND_TEMPLATE_ANNOTATOR_2.csv')
    
    template_annotator_1.to_csv(f1, index=False)
    template_annotator_2.to_csv(f2, index=False)
    
    print(f"Generated {len(valid_candidates)} items in double-blind templates:")
    print(f" - {f1}")
    print(f" - {f2}")
    return f1, f2

def calculate_inter_rater_reliability(ann1_csv: str, ann2_csv: str) -> dict:
    if not os.path.exists(ann1_csv) or not os.path.exists(ann2_csv):
        return {
            'status': 'NOT_VERIFIED',
            'reason': 'File input anotasi independen belum ditemukan.',
            'cohen_kappa': None,
            'krippendorff_alpha': None
        }

    df1 = pd.read_csv(ann1_csv)
    df2 = pd.read_csv(ann2_csv)
    
    merged = pd.merge(df1, df2, on='item_id', suffixes=('_1', '_2'))
    
    # Bersihkan string label
    col1 = 'assigned_emotion_1' if 'assigned_emotion_1' in merged.columns else merged.columns[2]
    col2 = 'assigned_emotion_2' if 'assigned_emotion_2' in merged.columns else merged.columns[7]
    
    labels_1 = merged[col1].fillna('').astype(str).str.strip()
    labels_2 = merged[col2].fillna('').astype(str).str.strip()
    
    # Mask untuk nilai kosong / unassigned
    empty_vals = ['', 'nan', 'none', 'null', '<na>']
    empty_mask = labels_1.str.lower().isin(empty_vals) | labels_2.str.lower().isin(empty_vals)
    
    if empty_mask.all():
        return {
            'status': 'NOT_VERIFIED',
            'reason': 'Semua entri label independen masih kosong (menunggu input annotator manusia). Dilarang mengarang label sintetis.',
            'sample_size': len(merged),
            'filled_count': 0,
            'cohen_kappa': None,
            'krippendorff_alpha': None
        }
        
    valid = merged[~empty_mask].copy()
    n = len(valid)
    if n < 5:
        return {
            'status': 'NOT_VERIFIED',
            'reason': f'Sampel anotasi terisi terlalu sedikit ({n} entri) untuk menghitung reliabilitas statistik yang valid.',
            'sample_size': len(merged),
            'filled_count': n,
            'cohen_kappa': None,
            'krippendorff_alpha': None
        }
        
    v_l1 = valid[col1].astype(str).str.strip()
    v_l2 = valid[col2].astype(str).str.strip()
    
    categories = sorted(list(set(v_l1).union(set(v_l2))))
    conf_mat = pd.crosstab(v_l1, v_l2, dropna=False)
    
    # Reindex agar matriks simetris dengan semua kategori
    conf_mat = conf_mat.reindex(index=categories, columns=categories, fill_value=0)
    
    # Observed agreement (Po)
    po = np.trace(conf_mat.values) / n
    
    # Expected agreement (Pe)
    marg1 = conf_mat.sum(axis=1) / n
    marg2 = conf_mat.sum(axis=0) / n
    pe = float(np.sum(marg1.values * marg2.values))
    
    kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 1.0
    
    # Krippendorff's Alpha untuk data nominal (2 penilai, tanpa missing di data valid)
    # Untuk 2 rater nominal lengkap: alpha = (Po - Pe*) / (1 - Pe*) di mana Pe* adalah variasi marginal gabungan
    # D_o = 1 - Po
    # D_e = sum_c (n_c * (n - n_c)) / (2 * n * (2*n - 1))
    joint_counts = {}
    for c in categories:
        joint_counts[c] = (v_l1 == c).sum() + (v_l2 == c).sum()
    total_units = 2 * n
    de = sum(cnt * (total_units - cnt) for cnt in joint_counts.values()) / (total_units * (total_units - 1))
    do = 1.0 - po
    alpha = 1.0 - (do / de) if de > 0 else 1.0

    return {
        'status': 'VERIFIED_CALCULATED',
        'sample_size': len(merged),
        'filled_count': n,
        'observed_agreement': float(po),
        'expected_agreement': float(pe),
        'cohen_kappa': float(kappa),
        'krippendorff_alpha': float(alpha),
        'categories': categories,
        'confusion_matrix': conf_mat.to_dict()
    }

if __name__ == "__main__":
    purified_csv = "data/annotation/purified_benchmark_batch_100_audit.csv"
    out_dir = "data/annotation/double_blind"
    generate_double_blind_templates(purified_csv, out_dir)
    res = calculate_inter_rater_reliability(
        os.path.join(out_dir, 'DOUBLE_BLIND_TEMPLATE_ANNOTATOR_1.csv'),
        os.path.join(out_dir, 'DOUBLE_BLIND_TEMPLATE_ANNOTATOR_2.csv')
    )
    print("Reliability Check Result:", res)
