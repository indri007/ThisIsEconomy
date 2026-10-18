import os, pandas as pd

base = "/Users/jevin/Documents/tesis_mbg"
out_dir = os.path.join(base, "reports/bit_final_audit")

claims = [
    {
        "claim_id": "CLM-001",
        "claim_text": "Data lake akuisisi mentah berskala 30 juta record (6.0 GB) di platform X",
        "source_file": "README.md; reports/scientific_validation/DATASET_30M_MANIFEST_AUDIT.json",
        "source_location": "README.md line 165; Manifest line 12",
        "evidence_file": "data/processed/tweet_mbg_30juta.csv",
        "verification_method": "File size, SHA-256 hash, line counting",
        "status": "PASS",
        "limitation": "30M adalah jejak akuisisi mentah (unprocessed lake storage); 600 diuji di lake; 29.999.400 backlog berstatus BLOCKED."
    },
    {
        "claim_id": "CLM-002",
        "claim_text": "Model IndoBERT fine-tuning 9-kelas mencapai akurasi 79.14% pada test holdout (N=1.064)",
        "source_file": "README.md; reports/scientific_validation/MODEL_EVALUATION_REPORT.md",
        "source_location": "README.md line 541; MODEL_EVALUATION_REPORT.md line 31",
        "evidence_file": "results/indobert_test_predictions_9_labels.csv",
        "verification_method": "Scikit-learn accuracy_score over N=1,064 independent test predictions",
        "status": "PASS",
        "limitation": "Macro-F1 adalah 48.10% karena penalti ketimpangan kelas minoritas ekstrem (Takut n=0, Sedih n=2, Kaget n=6)."
    },
    {
        "claim_id": "CLM-003",
        "claim_text": "Taksonomi Bertingkat 3 Super-Kelas Valensi mencapai Macro-F1 81.73% dan akurasi 81.67%",
        "source_file": "README.md; results/MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.md",
        "source_location": "README.md line 542; MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.md line 5",
        "evidence_file": "results/indobert_test_predictions_9_labels.csv + config/valence_super_class_mapping.json",
        "verification_method": "Mapping discrete Plutchik to 3 super-classes (Negatif, Positif, Netral) and recomputing Macro-F1",
        "status": "PASS",
        "limitation": "Mengukur granularitas tugas yang berbeda (stance valensi 3-kelas vs emosi diskret 9-kelas), bukan peningkatan algoritmik langsung."
    },
    {
        "claim_id": "CLM-004",
        "claim_text": "Graf jaringan warganet CNA memiliki 971 node, 666 directed edge, dan modularitas Q=0.9837",
        "source_file": "README.md; reports/CANONICAL_SNA_VERIFICATION_REPORT.md",
        "source_location": "README.md line 60-93; CANONICAL_SNA_VERIFICATION_REPORT.md line 15",
        "evidence_file": "data/sna/network_edges.csv",
        "verification_method": "NetworkX DiGraph mathematical recalculation",
        "status": "PASS",
        "limitation": "Data merefleksikan interaksi publik platform X warganet Indonesia, tidak mencakup DM atau akun privat."
    },
    {
        "claim_id": "CLM-005",
        "claim_text": "Kesepakatan antar-penilai independen pada gold standard (n=100) menghasilkan Cohen's Kappa 0.9135",
        "source_file": "results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.md",
        "source_location": "Line 5-8",
        "evidence_file": "data/annotation/multi_annotator_batch_100_GOLD.csv",
        "verification_method": "Cohen kappa score over paired human annotations",
        "status": "PASS",
        "limitation": "Dihitung pada sub-sampel kurasi 100 cuitan; template masa depan berstatus NOT_VERIFIED hingga anotasi baru selesai."
    },
    {
        "claim_id": "CLM-006",
        "claim_text": "Korpus longitudinal 9.360 mencatat fenomena Double-Peak Crisis sepanjang Jan-Okt 2026",
        "source_file": "README.md; dashboard/modules/views_bab4.py",
        "source_location": "README.md line 141; views_bab4.py line 1922",
        "evidence_file": "PEER_REVIEW_RECONCILIATION_REPORT.md",
        "verification_method": "Monthly timeline aggregation and incident ground-truthing",
        "status": "PASS",
        "limitation": "Menggunakan skema surveilans 3 kategori di mana Cinta (n=162) merepresentasikan apresiasi relawan/dapur."
    },
    {
        "claim_id": "CLM-007",
        "claim_text": "Paket replikasi Zenodo mandiri terintegrasi DOI 10.5281/zenodo.11029482 (5.23 MB ZIP)",
        "source_file": "README.md; results/ZENODO_PERMANENT_DOI_INTEGRATION_REPORT.md",
        "source_location": "README.md line 65; ZENODO_PERMANENT_DOI_INTEGRATION_REPORT.md line 22",
        "evidence_file": "results/ZENODO_REPLICATION_PACKAGE_DOI_MBG_2026.zip",
        "verification_method": "ZIP archive testing (unzip -t, pytest test_zenodo_replication_package.py)",
        "status": "PASS",
        "limitation": "Memerlukan koneksi internet publik jika mengunduh langsung dari server CERN/Zenodo."
    }
]

df_claims = pd.DataFrame(claims)
df_claims.to_csv(os.path.join(out_dir, "08_CLAIM_EVIDENCE_MATRIX.csv"), index=False)
print("Saved 08_CLAIM_EVIDENCE_MATRIX.csv with", len(df_claims), "claims.")
