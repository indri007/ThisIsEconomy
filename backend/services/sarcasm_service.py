import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_sarcasm_summary():
    try:
        sarcasm_path = os.path.join(PROJECT_ROOT, "data", "sarcasm", "dataset_sindiran_valid.csv")
        df_sarcasm = pd.read_csv(sarcasm_path)
        
        df_sarcasm['is_sarcasm'] = df_sarcasm['sindiran'].astype(str).str.lower().isin(['true', '1', 'ya'])
        
        sarcasm_counts = df_sarcasm['is_sarcasm'].value_counts().to_dict()
        
        total = sum(sarcasm_counts.values())
        sarcasm_true = sarcasm_counts.get(True, 0)
        sarcasm_false = sarcasm_counts.get(False, 0)
        
        SARCASM_EMOJIS = ["🤡", "🙃", "🤮", "🤢", "😒", "💀", "😤", "🤬", "🤦", "😅", "🙄"]
        emoji_hits = 0
        
        for text in df_sarcasm[df_sarcasm['is_sarcasm']]['text'].dropna():
            for em in SARCASM_EMOJIS:
                if em in text:
                    emoji_hits += text.count(em)

        return {
            "total_tweets": total,
            "sarcastic_tweets": sarcasm_true,
            "non_sarcastic_tweets": sarcasm_false,
            "sarcasm_percentage": round((sarcasm_true / total) * 100, 2) if total > 0 else 0,
            "emoji_hits": emoji_hits
        }
    except Exception as e:
        return {"error": str(e)}
