import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "results", "indobert_9_emosi_fixed.csv")

def get_emotion_distribution():
    try:
        df = pd.read_csv(DATA_PATH)
        emotion_counts = df['predicted_emotion'].value_counts().reset_index()
        emotion_counts.columns = ['emotion', 'count']
        return emotion_counts.to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}
