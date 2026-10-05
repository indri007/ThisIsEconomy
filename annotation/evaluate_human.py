import pandas as pd, numpy as np
from sklearn.metrics import cohen_kappa_score, classification_report, f1_score, accuracy_score
def load(prefix):
    A = pd.read_csv(f'annotation/lembar_{prefix}_A.csv'); B = pd.read_csv(f'annotation/lembar_{prefix}_B.csv')
    return A.merge(B, on=['uid','text'], suffixes=('_A','_B'))
for prefix in ['main273','audit_minor']:
    try: m = load(prefix)
    except FileNotFoundError: continue
    print(f'\n== {prefix} (n={len(m)}) ==')
    for t in ['relevan_MBG(ya/tidak)','emosi','sarkasme(ya/tidak)']:
        a, b = m[f'{t}_A'].astype(str), m[f'{t}_B'].astype(str)
        if a.nunique() > 1 or b.nunique() > 1:
            print(f'kappa {t}: {cohen_kappa_score(a,b):.3f} | agreement {(a==b).mean():.3f}')
        else: print(f'{t}: lembar belum diisi')
try:
    g = pd.read_csv('annotation/adjudicated_main273.csv')      # uid, emosi_final, sarkasme_final
    k = pd.read_csv('annotation/_key_main273.csv')[['uid','text','silver']]
    p = pd.read_csv('results/FINAL_indobert_predictions.csv').drop_duplicates('text')[['text','predicted_label']]
    d = g.merge(k, on='uid').merge(p, on='text')
    print('\nIndoBERT vs MANUSIA, n =', len(d))
    print(classification_report(d.emosi_final, d.predicted_label, zero_division=0))
    rng = np.random.default_rng(42); mf=[]
    for _ in range(2000):
        s = d.sample(len(d), replace=True, random_state=int(rng.integers(1e9)))
        mf.append(f1_score(s.emosi_final, s.predicted_label, average='macro', zero_division=0))
    print('macro-F1 95% CI:', np.percentile(mf,[2.5,97.5]).round(3))
    print('silver vs manusia: acc', round(accuracy_score(d.emosi_final,d.silver),3), '| kappa', round(cohen_kappa_score(d.emosi_final,d.silver),3))
except FileNotFoundError:
    print('\nadjudicated_main273.csv belum ada (normal)')
