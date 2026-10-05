import pandas as pd
from sklearn.metrics import cohen_kappa_score, classification_report, f1_score, accuracy_score
A = pd.read_csv('annotation/lembar_anotator_A.csv'); B = pd.read_csv('annotation/lembar_anotator_B.csv')
m = A.merge(B, on=['id','text'], suffixes=('_A','_B'))
for task in ['emosi','sarkasme(ya/tidak)']:
    a, b = m[f'{task}_A'].astype(str), m[f'{task}_B'].astype(str)
    print(f'Cohen kappa {task}: {cohen_kappa_score(a,b):.3f} | agreement {(a==b).mean():.3f}')
# Selisih A vs B diselesaikan manual: isi kolom emosi_final / sarkasme_final di annotation/adjudicated.csv
try:
    g = pd.read_csv('annotation/adjudicated.csv')   # kolom: id, text, emosi_final, sarkasme_final
    p = pd.read_csv('results/FINAL_indobert_predictions.csv')[['text','predicted_label']]
    d = g.merge(p, on='text')
    print(f'n evaluasi: {len(d)}')
    print(classification_report(d.emosi_final, d.predicted_label, zero_division=0))
    print('macro-F1 vs gold manusia:', round(f1_score(d.emosi_final, d.predicted_label, average="macro", zero_division=0),4))
    k = pd.read_csv('annotation/_key_silver.csv').merge(g, on='id')
    print('Kesesuaian silver vs manusia (acc):', round(accuracy_score(k.emosi_final, k.silver),4),
          '| kappa:', round(cohen_kappa_score(k.emosi_final, k.silver),3))
except FileNotFoundError:
    print('adjudicated.csv belum ada (normal sebelum anotasi selesai)')
