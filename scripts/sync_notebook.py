import json

with open('notebooks/tesis_mbg.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update cell 65
c65 = ''.join(nb['cells'][65]['source'])
c65 = c65.replace('Modularity Score 0.7130 (High Polarization Detected)', 'Modularity Score 0.9837 (Hyper-Fragmentation & Echo Chambers Detected)')
c65 = c65.replace('indobert_9_emosi.csv', 'indobert_9_emosi_fixed.csv')
nb['cells'][65]['source'] = [c65]

# Update cell 71
updated_c71 = """### 18. Temuan Empiris & Pembahasan (Sinkronisasi Bab 4 & Bab 5 Tesis)

Berikut adalah ringkasan data hasil evaluasi komputasional empiris yang telah diverifikasi dan disinkronkan secara penuh dengan manuskrip tesis (*tesis_text.txt*):

**4.2.1 Karakteristik Sistem Jaringan Komunikasi (SNA)**
- **Ukuran Jaringan:** Korpus resmi mencakup **971–973 aktor (*nodes*)** dan **658–666 interaksi berarah (*edges*)**.
- **Polarisasi & Fragmentasi Ekstrem:** Skor **Modularity Louvain mencapai 0,9837** dengan **332–341 komponen terhubung** (*weakly connected components*). Komponen raksasa (*giant component*) hanya mencakup **9,1% (89 node)** dari total aktor, dengan nilai *reciprocity* sangat rendah (**1,21%**). Hal ini membuktikan bahwa polarisasi diskursus MBG berwujud *hyper-fragmentation* (ratusan kantong percakapan kecil yang terisolasi), bukan sekadar dua kubu ideologis besar yang solid.

**4.2.3 Aktor Dominan & Fenomena Power Vacuum**
- **Sentralitas Masuk (In-Degree):** Akun `@prabowo` memegang *In-Degree* tertinggi (15) namun memiliki *Out-Degree* 0 (*Degree Centrality* = 15, *Betweenness* = 0,0030), mengonfirmasi terjadinya **power vacuum** di mana figur otoritas pasif dalam dialog dua arah.
- **Sentralitas Keluar (Out-Degree):** Agen kecerdasan buatan `@grok` mendominasi *Out-Degree* tertinggi (42; *Degree Centrality* = 43, *Betweenness* = 0,0034), bertindak sebagai rujukan verifikasi independen publik (*algorithmic oracle*).
- **Aktor Penghubung & Klaster:** Akun warganet seperti `@4Y4NKZ` (*Degree* = 18, *Betweenness* = 0,0003) dan `@newIding30` (*Degree* = 17) menjadi simpul penyebar narasi di klaster masing-masing.

**4.2.4 Klasifikasi Emosi & Evaluasi IndoBERT (9 Emosi Plutchik)**
- **Performa Evaluasi Model:** Model fine-tuned IndoBERT (checkpoint-792) dievaluasi pada data uji validasi riil ($n=1.053$, subset 20% dari korpus inferensi $N=5.263$):
  - **Overall Accuracy:** **57,45%** (0,5745)
  - **Weighted F1-score:** **0,4563**
  - **Macro F1-score:** **0,1444** (akibat distribusi data imbalanced pada kelas minoritas)
  - **Sensitivitas Emosi Jijik (*Disgust*):** Recall **96,92%** (566 dari 584 benar), Precision **0,5700**, F1-score **0,7178**.
  - **Ketepatan Emosi Percaya (*Trust*):** Precision **68,42%** (39 dari 57 benar), Recall **18,66%**, F1-score **0,2932**.
- **Distribusi Emosi Korpus Riil ($N=5.263$ Cuitan):**
  1. **Jijik (*Disgust*):** **2.960 cuitan (56,24%)** — Dominasi mutlak sentimen penolakan.
  2. **Percaya (*Trust*):** **1.073 cuitan (20,39%)**
  3. **Netral (*Neutral*):** **649 cuitan (12,33%)**
  4. **Tertarik (*Interest/Shame*):** **505 cuitan (9,60%)**
  5. **Marah (*Anger*):** **55 cuitan (1,05%)**
  6. **Sedih (*Sadness*):** **19 cuitan (0,36%)**
  7. **Takut (*Fear*):** **2 cuitan (0,04%)**
  8. **Bahagia & Kaget:** 0 cuitan (0,00%)

**4.2.5 Karakteristik Deteksi Sindiran & Sarkasme**
- **Korpus Validasi Sindiran ($N=3.395$):** Sebanyak **3.080 cuitan (90,72%)** terklasifikasi non-sindiran dan **315 cuitan (9,28%)** terverifikasi memuat gaya bahasa sindiran (*dataset_sindiran_valid.csv* & *tweet_sarkastik_final.csv*).
- **Korpus Inferensi Rekonstruksi ($N=5.263$):** Leksikon kontradiktif mencatat **181 cuitan sindiran eksplisit (3,44%)**, sementara proksi afektif penolakan/jijik menjangkau **2.979 cuitan (56,60%)**.

**4.3.5 Sintesis Phygital Gap (Marketing 6.0)**
- Kesenjangan tajam antara janji digital komunikasi kebijakan pemerintah (*'makanan bergizi gratis untuk generasi emas'*) dan realitas fisik implementasi di lapangan (*makanan basi, keracunan massal, vendor bermasalah*) secara empiris terbukti melalui:
  1. Dominasi afektif emosi **Jijik (56,24%)** dan resistensi sindiran warganet.
  2. Fragmentasi jaringan komunikasi yang terpecah (**Modularity 0,9837**, 332–341 klaster).
  3. Ketiadaan arena dialog resmi dua arah dari figur kunci kebijakan (**Power Vacuum** `@prabowo` In=15, Out=0).
"""

nb['cells'][71]['source'] = [updated_c71]

with open('notebooks/tesis_mbg.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Successfully synchronized notebooks/tesis_mbg.ipynb!')
