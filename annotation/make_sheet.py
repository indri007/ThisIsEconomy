import pandas as pd
t = pd.read_csv('results/emotion_test_group_split.csv')
t = t.drop_duplicates('text')
quota = {'Jijik':60,'Percaya':60,'Netral':60,'Tertarik':60,'Marah':14,'Sedih':3}
parts = []
for lab, n in quota.items():
    s = t[t.predicted_emotion==lab]
    parts.append(s.sample(min(n,len(s)), random_state=42))
s = pd.concat(parts).sample(frac=1, random_state=7).reset_index(drop=True)
# kunci silver disimpan terpisah (anotator tidak boleh melihatnya)
s[['id','predicted_emotion']].rename(columns={'predicted_emotion':'silver'}).to_csv('annotation/_key_silver.csv', index=False)
cols = ['relevan_MBG(ya/tidak)','emosi','sarkasme(ya/tidak)']
for a in ['A','B']:
    out = s[['id','text']].copy()
    for c in cols: out[c] = ''
    out.to_csv(f'annotation/lembar_anotator_{a}.csv', index=False, encoding='utf-8-sig')
print(len(s), 'cuitan; label emosi yang boleh dipakai: Jijik, Percaya, Netral, Tertarik, Marah, Sedih, Takut, Bahagia, Kaget')
