import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABSA_PATH = os.path.join(PROJECT_ROOT, "data", "results", "mbg_absa_dataset.csv")

def get_absa_summary():
    try:
        df = pd.read_csv(ABSA_PATH)
        
        # Aggregate by Aspect and Sentiment
        aspect_counts = df['aspect'].value_counts().reset_index()
        aspect_counts.columns = ['aspect', 'total']
        
        summary = []
        for _, row in aspect_counts.iterrows():
            aspect = row['aspect']
            total = row['total']
            
            aspect_df = df[df['aspect'] == aspect]
            sent_counts = aspect_df['sentiment'].value_counts().to_dict()
            
            summary.append({
                "aspect": aspect,
                "total": total,
                "positif": sent_counts.get("Positif", 0),
                "negatif": sent_counts.get("Negatif", 0),
                "netral": sent_counts.get("Netral", 0)
            })
            
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}
