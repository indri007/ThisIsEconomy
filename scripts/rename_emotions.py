import pandas as pd

file_path = "data/results/indobert_9_emosi_fixed.csv"
df = pd.read_csv(file_path)

mapping = {
    'anger': 'Marah',
    'disgust': 'Jijik',
    'fear': 'Takut',
    'sadness': 'Sedih',
    'joy': 'Bahagia/Senang',
    'neutral': 'Netral',
    'surprise': 'Kaget',
    'love': 'Percaya',      
    'shame': 'Tertarik'     
}

if 'predicted_emotion' in df.columns:
    df['predicted_emotion'] = df['predicted_emotion'].str.lower().map(mapping).fillna(df['predicted_emotion'])
    df.to_csv(file_path, index=False)
    print("Labels updated successfully in CSV.")
else:
    print("Column predicted_emotion not found!")

