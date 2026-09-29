import os
import pandas as pd
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_PATH = os.path.join(PROJECT_ROOT, "data", "results", "indobert_9_emosi_fixed.csv")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data", "results", "mbg_absa_dataset.csv")

# Kamus Aspek MBG
ASPECT_DICT = {
    "Anggaran & Dana": ["anggaran", "dana", "pajak", "triliun", "biaya", "apbn", "korupsi", "potong"],
    "Menu & Nutrisi": ["menu", "gizi", "susu", "telur", "daging", "sayur", "nutrisi", "ikan", "protein", "karbohidrat", "stunting"],
    "Distribusi & Logistik": ["distribusi", "kirim", "penyaluran", "daerah terpencil", "sekolah", "logistik", "akses", "infrastruktur"],
    "Implementasi & Regulasi": ["regulasi", "aturan", "wajib", "pemerintah", "prabowo", "gibran", "menteri", "program", "kebijakan", "uji coba"]
}

def determine_aspects(text):
    if pd.isna(text):
        return ["Tidak Diketahui"]
    text = str(text).lower()
    
    found_aspects = []
    for aspect, keywords in ASPECT_DICT.items():
        if any(kw in text for kw in keywords):
            found_aspects.append(aspect)
            
    if not found_aspects:
        return ["Umum (Lainnya)"]
    return found_aspects

def determine_sentiment(emotion):
    emotion = str(emotion).title()
    if emotion in ["Percaya", "Tertarik", "Bahagia"]:
        return "Positif"
    elif emotion in ["Jijik", "Marah", "Sedih", "Takut", "Antisipasi"]:
        return "Negatif"
    else:
        return "Netral"

def main():
    print(f"Membaca data dari {INPUT_PATH}...")
    df = pd.read_csv(INPUT_PATH)
    
    absa_rows = []
    
    for idx, row in df.iterrows():
        text = row.get("clean_text", row.get("text", ""))
        emotion = row.get("predicted_emotion", "Netral")
        
        aspects = determine_aspects(text)
        sentiment = determine_sentiment(emotion)
        
        # If a tweet has multiple aspects, create a row for each aspect
        # Alternatively, for simplicity, we can do multi-label or explode. Let's explode.
        for asp in aspects:
            absa_rows.append({
                "id": row.get("id"),
                "text": row.get("text"),
                "clean_text": text,
                "aspect": asp,
                "sentiment": sentiment,
                "emotion": emotion
            })
            
    df_absa = pd.DataFrame(absa_rows)
    print(f"Berhasil mengekstrak {len(df_absa)} relasi ABSA.")
    
    df_absa.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset ABSA berhasil disimpan ke {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
