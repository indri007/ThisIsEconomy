import pandas as pd

file_path = "data/results/indobert_9_emosi_fixed.csv"
df = pd.read_csv(file_path)

# Mapping English to Indonesian (fitting 9 categories)
mapping = {
    'Anger': 'Marah',
    'Disgust': 'Jijik',
    'Fear': 'Takut',
    'Sadness': 'Sedih',
    'Joy': 'Bahagia/Senang',
    'Neutral': 'Netral',
    'Surprise': 'Kaget',
    'Love': 'Percaya',      # Mapping Love to Percaya (Trust)
    'Shame': 'Tertarik'     # Mapping Shame to Tertarik (Anticipation)
}

if 'predicted_emotion' in df.columns:
    df['predicted_emotion'] = df['predicted_emotion'].map(mapping).fillna(df['predicted_emotion'])
    df.to_csv(file_path, index=False)
    print("Labels updated successfully in CSV.")
else:
    print("Column predicted_emotion not found!")

