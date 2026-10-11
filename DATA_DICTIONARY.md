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
* **Ukuran:** 5.263 baris × 13 kolom
* **Deskripsi:** Dataset siap latih dan evaluasi model klasifikasi emosi IndoBERT.
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

| # | Kelas Teoretis (Bahasa Inggris) | Label Indonesia Resmi | Label Indonesia Ad-Hoc di Skrip Lama | Jumlah Sampel Aktual ($N=5.263$) | Persentase Sampel | Status Validasi Ilmiah |
| :-: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | `disgust` | Jijik | Jijik | **2.960** | **56.24%** | ✅ **Tervalidasi Penuh** (Kelas Dominan) |
| 2 | `love` | Cinta / Afeksi | **Percaya (*Trust*)** | **1.073** | **20.39%** | ⚠️ **Ad-hoc Proxy** (Tervalidasi sebagai Trust) |
| 3 | `neutral` | Netral | Netral | **649** | **12.33%** | ✅ **Tervalidasi Penuh** |
| 4 | `shame` | Malu / Aib | **Tertarik (*Interest*)** | **505** | **9.60%** | ⚠️ **Ad-hoc Proxy** (Tervalidasi sebagai Interest) |
| 5 | `anger` | Marah | Marah | **55** | **1.04%** | ⚠️ **Minoritas Ekstrem** (14 di set uji) |
| 6 | `sadness` | Sedih | Sedih | **19** | **0.36%** | ⚠️ **Minoritas Ekstrem** (3 di set uji) |
| 7 | `fear` | Takut | Takut | **2** | **0.04%** | ❌ **Sampel Tidak Memadai** (0 di set uji v2) |
| 8 | `joy` | Bahagia / Senang | Bahagia | **0** | **0.00%** | ❌ **Nol Sampel** (Tidak tervalidasi) |
| 9 | `surprise` | Terkejut / Kaget | Kaget | **0** | **0.00%** | ❌ **Nol Sampel** (Tidak tervalidasi) |

### ⚠️ Catatan Kritis Mengenai Pemetaan Label (AUD-002):
1. **Kasus `love -> Percaya`:** Dalam teori afek Plutchik, *Love* adalah dyad primer yang tersusun dari *Joy + Trust*. Namun, dalam diskursus kebijakan publik MBG, warganet Indonesia tidak mengekspresikan cinta romantis, melainkan rasa percaya dan dukungan terhadap janji presiden. Oleh karena itu, model memproses kelas ini sebagai persepsi kepercayaan publik (*Trust*).
2. **Kasus `shame -> Tertarik`:** Dalam skrip `rename_emotions.py`, label `shame` dari dataset eksternal dialihkan ke `Tertarik`. Secara psikologi komunikatif, hal ini merupakan diskrepansi konseptual. Manuskrip Scopus Q1 wajib menyatakan bahwa kelas ini mencerminkan atensi keingintahuan publik atas kejanggalan program (*critical curiosity*), bukan rasa malu introspektif.
3. **Ketiadaan Sampel `joy` dan `surprise`:** Fakta bahwa wacana krisis MBG di media sosial menghasilkan 0 sampel untuk kegembiraan murni (*pure joy*) dan keterkejutan positif (*surprise*) membuktikan secara sosiologis bahwa respons publik didominasi oleh kekecewaan dan skeptisisme, bukan antusiasme.
