import pandas as pd
import numpy as np
import os

def run_perbaikan():
    print("=== SCRIPT PERBAIKAN_LABELING.py ===")
    print("Tujuan: Memperbaiki cacat hardcoding label 'Neutral' pada Testing Set (Bab 4.5.3 Tesis)")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        from scripts.data_utils import get_data_path
    except ImportError:
        from data_utils import get_data_path
        
    # 1. Load data mentah yang valid (hasil prediksi/anotasi yang benar)
    raw_data_path = get_data_path("indobert_9_emosi.csv")
    if not os.path.exists(raw_data_path):
        print(f"Error: File {raw_data_path} tidak ditemukan.")
        return
        
    print(f"1. Membaca dataset asli: {raw_data_path}")
    df_raw = pd.read_csv(raw_data_path)
    
    # 2. Identifikasi masalah hardcode (simulasi bug)
    print("2. Menganalisis masalah pelabelan...")
    if 'predicted_emotion' in df_raw.columns:
        print(" -> Ditemukan kolom 'predicted_emotion' asli dari hasil anotasi.")
    else:
        print(" -> Peringatan: Kolom 'predicted_emotion' asli tidak ditemukan.")
        return
        
    # 3. Membersihkan dan menyusun ulang dataset
    print("3. Memperbaiki distribusi label...")
    df_clean = df_raw.copy()
    valid_emotions = ['anger', 'disgust', 'fear', 'joy', 'love', 'neutral', 'sadness', 'shame', 'surprise']
    df_clean['predicted_emotion'] = df_clean['predicted_emotion'].astype(str).str.lower().str.strip()
    df_clean = df_clean[df_clean['predicted_emotion'].isin(valid_emotions)]
    
    if 'processed_text' not in df_clean.columns:
        print(" -> Error: kolom 'processed_text' tidak ditemukan.")
        return
        
    df_clean = df_clean.dropna(subset=['processed_text', 'predicted_emotion'])
    
    print(f" -> Berhasil memulihkan {len(df_clean)} baris data dengan label emosi aktual.")
    print(" -> Distribusi emosi yang telah diperbaiki:")
    print(df_clean['predicted_emotion'].value_counts())
    
    # 4. Menyimpan data bersih untuk Retraining
    output_dir = os.path.join(base_dir, "data", "results")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "indobert_9_emosi_fixed.csv")
    
    df_clean.to_csv(output_path, index=False)
    print(f"\n4. SELESAI! Dataset siap-train yang valid telah disimpan ke: {output_path}")
    print("   Silakan gunakan file ini untuk menjalankan ulang 'train_9_labels.py' agar metrik evaluasi model di Tesis Anda valid.")

if __name__ == "__main__":
    run_perbaikan()
