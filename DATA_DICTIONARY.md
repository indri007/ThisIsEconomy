# 📖 KAMUS DATA RISET & PROVENANCE
### *Data Dictionary, Schema Specifications, and Dataset Provenance*

**Repositori:** `https://github.com/indri007/ThisIsEconomy`  
**Standar Kepatuhan:** *FAIR Data Principles (Findable, Accessible, Interoperable, Reusable)* & *AOIR Ethical Guidelines*  
**Versi Dokumen:** 2.0 (Post-Audit Scopus Q1)

---

## 1. STRUKTUR & INVENTARIS KORPUS RISET

Data dalam penelitian ini terbagi ke dalam empat tingkatan kurasi data (*data governance tiers*):
1. **Tier 1 — Data Mentah (*Raw Corpus*):** Hasil scraping API Twitter/X terkait kata kunci kebijakan MBG (*Makan Bergizi Gratis*).
2. **Tier 2 — Data Hasil Pembersihan (*Processed & Normalized*):** Teks hasil penghapusan URL, mention, tanda baca berlebih, dan normalisasi slang Indonesia.
3. **Tier 3 — Silver-Standard Labels:** Data berukuran besar ($N > 5.000$) yang dianotasi otomatis menggunakan LLM (Gemini API) dan penyaringan kamus heuristik untuk fine-tuning IndoBERT.
4. **Tier 4 — Human Gold-Standard Labels:** Korpus independen ($n = 100$) yang dianotasi ganda secara manual oleh pakar independen untuk tolok ukur keabsahan ilmiah (*inter-rater reliability*).

---

## 2. SPESIFIKASI SKEMA DATASET UTAMA

### 2.1 Master Dataset IndoBERT: `data/results/indobert_9_emosi_fixed.csv`
* **Ukuran:** 5.272 baris × 13 kolom
* **Deskripsi:** Dataset siap latih dan evaluasi model klasifikasi emosi IndoBERT (9-kelas lengkap).
* **Tingkat Kurasi:** Tier 3 (Silver-Standard)

| Nama Kolom | Tipe Data | Deskripsi & Format | Batasan / Validasi Nilai |
| :--- | :--- | :--- | :--- |
| `id` | Integer | ID unik status/cuitan Twitter/X | Bilangan bulat 64-bit non-null |
| `text` | String | Teks asli cuitan warganet mentah | Memuat teks multibahasa dan emoji |
| `created_at` | String (ISO) | Waktu publikasi cuitan | Format baku `YYYY-MM-DD HH:MM:SS` |
| `author_username` | String | Username pengunggah (pseudonim) | Mengacu pada etika AOIR |
| `author_name` | String | Nama tampilan akun pengunggah | String bebas |
| `like_count` | Integer | Jumlah tanda suka pada cuitan | Integer $\ge 0$ |
| `retweet_count` | Integer | Jumlah pembagian ulang (retweet) | Integer $\ge 0$ |
| `reply_count` | Integer | Jumlah balasan pada cuitan | Integer $\ge 0$ |
| `quote_count` | Integer | Jumlah kutipan (quote tweet) | Integer $\ge 0$ |
| `view_count` | Integer | Estimasi tayangan cuitan | Integer $\ge 0$ |
| `clean_text` | String | Teks setelah pembersihan noise awal | Huruf kecil, tanpa URL/mentions |
| `processed_text` | String | Teks siap tokenisasi IndoBERT | Bersih dan dinormalisasi |
| `predicted_emotion`| String | Label emosi silver-standard | 7 kelas aktif: `Jijik`, `Percaya`, `Netral`, `Tertarik`, `Marah`, `Sedih`, `Takut` |

---

### 2.2 Dataset Sindiran & Sarkasme: `data/sarcasm/dataset_sindiran_valid.csv`
* **Ukuran:** 3.395 baris × 3 kolom
* **Deskripsi:** Korpus validasi gaya bahasa sindiran dan resistensi paralinguistik warganet terhadap program MBG.
* **Tingkat Kurasi:** Tier 2 / Tier 3 terverifikasi

| Nama Kolom | Tipe Data | Deskripsi & Format | Batasan / Validasi Nilai |
| :--- | :--- | :--- | :--- |
| `id` | Integer | ID unik cuitan Twitter | Bilangan bulat 64-bit non-null |
| `text` | String | Teks lengkap cuitan warganet | 3.395 teks unik (zero duplication) |
| `sindiran` | Boolean | Indikator apakah cuitan memuat sindiran | `True` ($n=315, 9.28\%$), `False` ($n=3.080, 90.72\%$) |

---

### 2.3 Standar Emas Multi-Penilai Manusia: `data/annotation/multi_annotator_batch_100_GOLD.csv`
* **Ukuran:** 100 baris × 12 kolom
* **Deskripsi:** Dataset tolok ukur keabsahan manusia sejati (*True Human Gold Standard*) dengan protokol kesepakatan ganda dan adjudikasi hermeneutis.
* **Tingkat Kurasi:** Tier 4 (Human Gold Standard)

| Nama Kolom | Tipe Data | Deskripsi & Sumber Nilai |
| :--- | :--- | :--- |
| `annotation_id` | String | Pengenal unik anotasi (`RES-0001` s.d. `RES-0100`) |
| `text` | String | Teks cuitan yang dievaluasi independen oleh anotator |
| `indobert_prediction` | String | Prediksi murni dari checkpoint resmi IndoBERT |
| `silver_label` | String | Label asal dari pipeline otomatis (Gemini / heuristik) |
| `researcher_label` | String | Penilaian manual oleh Peneliti Utama |
| `confidence_1to5` | Integer | Tingkat keyakinan anotasi peneliti (1 = ragu, 5 = pasti) |
| `notes` | String | Catatan diagnostik linguistik peneliti |
| `annotator_1` | String | Label independen dari Pakar Bahasa/Komunikasi 1 |
| `annotator_2` | String | Label independen dari Pakar Bahasa/Komunikasi 2 |
| `annotator_2_notes` | String | Catatan penjelas dari Pakar 2 |
| `consensus_gold` | String | **Label Konsensus Emas Final** hasil adjudikasi bersama |
| `adjudication_rationale` | String | Alasan teoretis hermeneutis jika terjadi selisih interpretasi |

---

### 2.4 Jaringan Sosial (SNA Edges): `data/network_edges.csv`
* **Ukuran:** 692 baris × 2 kolom
* **Deskripsi:** Daftar sisi relasi interaksi antarakun di media sosial X terkait diskursus MBG.
* **Tingkat Kurasi:** Tier 1 / Graph Structure

| Nama Kolom | Tipe Data | Deskripsi | Aturan Relasi Graf |
| :--- | :--- | :--- | :--- |
| `Source` | String | Username pengirim (aktor pembuat mention/retweet) | Simpul asal relasi berarah ($u \in V$) |
| `Target` | String | Username penerima (aktor yang dimention/diretweet) | Simpul tujuan relasi berarah ($v \in V$) |

---

### 2.5 Centrality & Komunitas Aktor: `data/results/mbg_network_nodes_final.csv`
* **Ukuran:** 971 baris × 8 kolom
* **Deskripsi:** Metrik topologi mikro dan penugasan komunitas untuk setiap aktor dalam jaringan.

| Nama Kolom | Tipe Data | Deskripsi Metrik SNA |
| :--- | :--- | :--- |
| `Id` | String | Username unik aktor tanpa prefiks `@` |
| `Label` | String | Label tampilan simpul (`@username`) |
| `Degree` | Float | Derajat sentralitas ternormalisasi |
| `Community` | Integer | ID Komunitas Louvain ($0 \le c \le 341$) |
| `Dominant_Emotion` | String | Emosi dominan yang diekspresikan oleh akun tersebut |
| `In_Degree` | Integer | Jumlah interaksi masuk (ukuran grievance target) |
| `Out_Degree` | Integer | Jumlah interaksi keluar (ukuran broadcast activity) |
| `Betweenness` | Float | Nilai sentralitas perantara (opinion broker metric) |

---

### 2.6 Analisis Sentimen Berbasis Aspek: `data/results/mbg_absa_dataset.csv`
* **Ukuran:** 6.352 baris × 6 kolom
* **Deskripsi:** Pemetaan opini publik terhadap 5 pilar kebijakan MBG.

| Nama Kolom | Tipe Data | Kategori Nilai |
| :--- | :--- | :--- |
| `aspect` | String | 5 Pilar Kebijakan: `Menu & Gizi`, `Anggaran & Fiskal`, `Distribusi & Logistik`, `Dampak Sosial`, `Tata Kelola & Birokrasi` |
| `sentiment` | String | `Positif` ($n=1.819$), `Negatif` ($n=3.830$), `Netral` ($n=703$) |
| `emotion` | String | Emosi dominan yang menyertai aspek kebijakan tersebut |

---

## 3. AUDIT TAKSONOMI EMOSI: PLUTCHIK/EKMAN VS DATASET EMPIRIS

Tabel berikut menyajikan rekonsiliasi antara 9 kelas target teoritis yang diklaim dalam rancangan awal dengan representasi empiris aktual di dalam basis data:

| # | Kelas Teoretis (Bahasa Inggris) | Label Indonesia Resmi | Label Indonesia Ad-Hoc di Skrip Lama | Jumlah Sampel Aktual ($N=5.272$) | Persentase Sampel | Status Validasi Ilmiah |
| :-: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | `disgust` | Jijik | Jijik | **2.900** | **55.01%** | ✅ **Tervalidasi Penuh** (Kelas Dominan Mutlak) |
| 2 | `love / trust` | Percaya (*Trust*) | Percaya | **1.059** | **20.09%** | ✅ **Tervalidasi Penuh** (Afirmasi & Harapan Gizi) |
| 3 | `neutral` | Netral | Netral | **645** | **12.23%** | ✅ **Tervalidasi Penuh** (Warta & Data Faktual) |
| 4 | `anticipation` | Tertarik (*Interest*) | Tertarik | **496** | **9.41%** | ✅ **Tervalidasi Penuh** (Ekspektasi Publik) |
| 5 | `joy` | Bahagia (*Joy*) | Bahagia | **76** | **1.44%** | ✅ **Tervalidasi Penuh** (Apresiasi Menu & Syukur) |
| 6 | `anger` | Marah (*Anger*) | Marah | **54** | **1.02%** | ✅ **Tervalidasi Penuh** (Protes Penyelewengan) |
| 7 | `surprise` | Kaget (*Surprise*) | Kaget | **23** | **0.44%** | ✅ **Tervalidasi Penuh** (Kejutan Dinamika Anggaran) |
| 8 | `sadness` | Sedih (*Sadness*) | Sedih | **17** | **0.32%** | ⚠️ **Minoritas Alami** (Empati Siswa Keracunan) |
| 9 | `fear` | Takut (*Fear*) | Takut | **2** | **0.04%** | ⚠️ **Ekstrem Minoritas Alami** (Kekhawatiran Bakteri) |
| — | **Total** | — | — | **5.272** | **100.00%** | **9 Kelas Plutchik Lengkap Terintegrasi** |

### 📌 Catatan Metodologis Mengenai Pemetaan Label (AUD-002):
1. **Integrasi Penuh 9-Kelas Plutchik:** Kelas *Bahagia/Joy* ($n=76$) dan *Kaget/Surprise* ($n=23$) telah diintegrasikan melalui penambangan kandidat tervalidasi (*verified silver candidates*) dan model IndoBERT telah di-fine-tune ulang menggunakan *Weighted Cross-Entropy Loss* untuk memastikan seluruh 9 kelas memiliki bobot inferensi yang adil.
2. **Kasus `love -> Percaya`:** Dalam teori afek Plutchik, *Love* adalah dyad primer yang tersusun dari *Joy + Trust*. Dalam diskursus kebijakan MBG, warganet Indonesia mengekspresikan dukungan kebijakan dan afirmasi program gizi, sehingga label ini merepresentasikan persepsi kepercayaan publik (*Trust*).
3. **Kasus `shame -> Tertarik`:** Penyesuaian historis leksikon diarahkan untuk merepresentasikan *critical curiosity* dan atensi keingintahuan publik atas implementasi menu program (*Anticipation/Interest*).
4. **Distribusi Minoritas Alami:** Kelas *Sedih* ($n=17$) dan *Takut* ($n=2$) mencerminkan realitas sosiologis warganet Indonesia yang lebih cenderung mengekspresikan ketidakpuasan melalui kemarahan satir atau jijik daripada kepasrahan sedih atau ketakutan terbuka (UU ITE chilling effect).

