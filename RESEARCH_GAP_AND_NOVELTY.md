# 🔬 ANALISIS KESENJANGAN RISET, KEBARUAN, & KELAYAKAN AKADEMIK
### *Research Gap, Scientific Novelty, Theoretical Framework, and Doctoral Research Agenda*

**Penelaah:** Peneliti Senior Computational Communication & Reviewer Ahli Jurnal Scopus Q1  
**Repositori:** `https://github.com/indri007/ThisIsEconomy`  
**Objek Analisis:** Komunikasi Krisis Kebijakan Makan Bergizi Gratis (MBG) di Media Sosial X  
**Kerangka Paradigma:** *Computational Social Science (CSS)* — Integrasi *Deep NLP*, *Social Network Analysis*, & *Public Administration Theory*

---

## 1. TINJAUAN PUSTAKA SISTEMATIS & IDENTIFIKASI KESENJANGAN RISET (*RESEARCH GAPS*)

Dalam literatur komunikasi politik komputasional dan kebijakan publik digital internasional, studi ini memosisikan diri pada perjumpaan empat kesenjangan keilmuan (*unresolved scholarly gaps*):

```
+----------------------------------------------------------------------------------------------------+
|                                    PETA KESENJANGAN RISET (GAPS)                                   |
+----------------------------------------------------------------------------------------------------+
| GAP 1: Pemisahan Metodologis Silo NLP vs Graf (Textual Silo vs Structural Silo)                    |
| - Masalah: Mayoritas riset menganalisis sentimen teks SAJA (Liew et al., 2022) ATAU menganalisis   |
|   topologi jaringan SAJA (Bail et al., 2018). Keduanya jarang diintegrasikan ke dalam satu ruang    |
|   keadaan komputasional untuk melihat bagaimana muatan afektif membentuk topologi graf.            |
|                                                                                                    |
| GAP 2: Dikotomi Usang: Deliberasi Demokratis vs Polarisasi Biner (Bipolar Trap)                    |
| - Masalah: Literatur dominan Barat mengasumsikan jaringan media sosial hanya terbagi dua:          |
|   deliberasi rasional (Habermas) ATAU perang dua kubu partisan terpolarisasi (Sunstein; Barberá).  |
|   Dalam krisis kebijakan di Global South, muncul realitas struktural ketiga: atomisasi wacana      |
|   ekstrem (hyper-fragmented grievance archipelago, Q > 0.95, WCC >> 100, Reciprocity < 2%).        |
|                                                                                                    |
| GAP 3: Sensor Diri Paralinguistik di Bawah Rezim Pidana Digital (UU ITE)                           |
| - Masalah: Model NLP standar mengasumsikan kritik publik diekspresikan lewat kemarahan literal     |
|   (Anger). Di Indonesia, ancaman pasal pencemaran nama baik memaksa publik menyamarkan kritik      |
|   menjadi sindiran disonan: kalimat pujian semu dengan emoji jijik (Disgust + Sarcasm).            |
|                                                                                                    |
| GAP 4: Ruang Hampa Institusional & Pengalihan Otoritas ke AI (Algorithmic Displacement)            |
| - Masalah: Ketika kementerian negara membisu (out-degree = 0), publik mengalihkan fungsi verifikasi|
|   fakta kepada bot kecerdasan buatan platform (@grok). Fenomena orakel algoritmik ini belum pernah |
|   dimodelkan dalam kerangka komunikasi krisis kebijakan publik.                                     |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. KEBARUAN METODOLOGIS: ARSITEKTUR KOMPUTASI TRI-LAYER

Penelitian ini menyajikan kontribusi metodologis orisinal berupa **Tri-Layer Computational Architecture** yang mengintegrasikan tiga tingkatan resolusi data:

```
[ LEVEL MAKRO-STRUKTURAL: Social Network Analysis ]
- NetworkX DiGraph (|V| = 971, |E| = 692, WCC = 341)
- Louvain Modularity Optimization (Q = 0.9837)
- Centrality & Tipologi Aktor (Sink, Oracle, Broker)
                     ▲
                     │ Pemetaan Afektif Simpul (Node Emotion Mapping)
                     ▼
[ LEVEL MESO-KEBIJAKAN: Aspect-Based Sentiment Analysis ]
- 5 Pilar Operasional: Menu/Gizi, Fiskal/Anggaran, Logistik, Tata Kelola, Dampak Sosial
- Ekstraksi Sentimen Aspek (Negatif = 60.3%, Positif = 28.6%, Netral = 11.1%)
                     ▲
                     │ Asosiasi Semantik Frasa (Lexico-Semantic Binding)
                     ▼
[ LEVEL MIKRO-LINGUISTIK: Contextual Transformer & Semiotika ]
- IndoBERT Base Fine-Tuned (6-Kelas Aktif, Val Loss 0.5068, Macro-F1 = 0.4535 / Super-Class = 0.7522)
- Deteksi Sindiran Paralinguistik & Disonansi Teks-Emoji (N = 3.395, 9.28% Sarcasm)
```

**Nilai Tambah Integrasi Tri-Layer vs Baseline Terpisah:**
1. **Analisis Teks Tanpa Graf:** Hanya mengetahui bahwa 56% cuitan bermuatan *Jijik*, tetapi buta terhadap fakta bahwa keluhan tersebut terkurung di 341 kantong percakapan kecil tanpa didengar oleh pembuat kebijakan.
2. **Analisis Graf Tanpa NLP:** Hanya mengetahui $Q = 0.9837$, namun rentan menarik kesimpulan keliru bahwa jaringan terbelah menjadi dua kubu kohesif pendukung vs penentang pemerintah.
3. **Integrasi Tri-Layer:** Mengungkapkan secara presisi bahwa krisis MBG adalah krisis struktural di mana masyarakat merasa muak (*Disgust*), mengekspresikannya melalui sindiran (*Sarcasm*), terisolasi dalam kantong mikro (*Hyper-fragmentation*), dan mencari bantuan dari agen AI (`@grok`) karena otoritas resmi membisu (*Power Vacuum*).

---

## 3. KEBARUAN TEORETIS: FORMALISASI KERANGKA *THE PHYGITAL GAP*

### 3.1 Konstruk Konseptual
Konsep *The Phygital Gap* diadaptasi dari teori pemasaran imersif (Kotler et al., 2023) dan direkonseptualisasi ke dalam ranah administrasi publik komputasional. *The Phygital Gap* didefinisikan sebagai:

> **Definisi:** Diskrepansi struktural yang tajam antara representasi naratif kebijakan di ruang digital (keberhasilan seremonial, anggaran fantastis, etalase media sosial) dengan pengalaman inderawi riil warga di ruang fisik (makanan basi, keracunan katering, keterlambatan distribusi sekolah).

---

### 3.2 Formulasi 5 Proposisi Kausal yang Dapat Diuji (*Testable Propositions*)

Untuk memandu agenda riset tingkat Doktor (S3), model diformalkan ke dalam lima proposisi ilmiah yang memiliki kriteria falsifikasi (*falsification criteria*):

* **Proposisi 1 (Paralinguistic Shielding / Perlindungan Paralinguistik):**  
  *Di bawah rezim hukum dengan restriksi pidana pencemaran nama baik (UU ITE), resistensi warganet terhadap kegagalan pelayanan publik bermutasi dari agresi verbal eksplisit (Anger) menjadi disonansi paralinguistik berupa pujian semu yang dipadukan dengan penanda visual penolakan (Sarcasm & Disgust).*  
  *Kriteria Falsifikasi:* P1 gugur jika pada korpus kritik MBG ditemukan frekuensi kemarahan literal leksikal lebih tinggi daripada ekspresi sindiran ber-emoji ($f(\text{Anger}) > f(\text{Sarcasm})$).

* **Proposisi 2 (Affective Primacy of Moral Disgust / Keutamaan Jijik Moral):**  
  *Kegagalan penyediaan kebutuhan fisiologis dasar yang menyangkut keselamatan anak-anak memicu dominasi afek penolakan moral (Disgust $\ge 50\%$), yang secara pragmatis menyerap kesedihan dan mengikis legitimasi institusi publik.*  
  *Kriteria Falsifikasi:* P2 gugur jika emosi dominan wacana krisis berada pada kelas netral atau deliberasi rasional ($f(\text{Disgust}) < 30\%$).

* **Proposisi 3 (Structural Atomization of Public Grievance / Atomisasi Struktural Keluhan):**  
  *Ketiadaan saluran mediasi institusional yang responsif melahirkan topologi jaringan kepulauan terisolasi ($Q > 0.90, \text{WCC} \gg 100$), bukan polarisasi dua kubu yang saling beradu argumen.*  
  *Kriteria Falsifikasi:* P3 gugur jika graf membentuk struktur raksasa biner dengan ukuran komponen utama $> 50\%$ total populasi.

* **Proposisi 4 (Algorithmic Displacement / Pemindahan Peran ke Algoritma):**  
  *Ketika pemegang otoritas kebijakan mempraktikkan komunikasi asimetris searah ($\text{Reciprocity} < 2\%, \text{Out-degree} = 0$), publik secara sadar mengangkat agen AI platform (`@grok`) ke posisi sentralitas perantara tertinggi untuk memverifikasi kebenaran lapangan.*  
  *Kriteria Falsifikasi:* P4 gugur jika sentralitas perantara (*betweenness*) dan derajat keluar aktor resmi pemerintah lebih tinggi daripada agen AI platform ($C_B(\text{Gov}) > C_B(\text{AI})$).

* **Proposisi 5 (Spatial-Epidemiological Coupling / Korelasi Spasial-Epidemiologis):**  
  *Densitas penolakan afektif digital di suatu wilayah berkorelasi positif secara signifikan dengan frekuensi insiden riil kegagalan fisik di daerah tersebut ($\rho > 0.60, p < 0.05$).*  
  *Kriteria Falsifikasi:* P5 gugur jika korelasi spasial Spearman antara sebaran cuitan kritis provinsi dan data insiden dinas kesehatan bernilai tidak signifikan ($p \ge 0.05$).

---

## 4. PEMISAHAN KONTRIBUSI REKAYASA PERANGKAT LUNAK VS KONTRIBUSI ILMIAH

Komite penilai menekankan demarkasi epistemologis antara kedua ranah:

```
+----------------------------------------------------------------------------------------------------+
|                                    DEMARKASI KESIAPAN SISTEM                                       |
+----------------------------------------------------------------------------------------------------+
| KESIAPAN REKAYASA PERANGKAT LUNAK (TRL 6-7) :                                                      |
| - Dasbor Streamlit port 8502 & 8503 dengan visualisasi interaktif multi-tab.                       |
| - Bot Telegram real-time dispatcher untuk broadcast peringatan dini.                              |
| - Backend FastAPI terstandarisasi dengan 7 endpoint RESTful.                                       |
| - Automasi NodeXL Excel pipeline bridge.                                                           |
| STATUS: Telah berfungsi sempurna sebagai purwarupa operasional (*Software Achievement*).           |
|                                                                                                    |
| KESIAPAN RISET ILMIAH (EPISTEMIC MATURITY) :                                                       |
| - Desain penelitian bersifat observasional-retrospektif, BUKAN eksperimen kausal terkontrol.       |
| - Efektivitas sistem EWS dalam 'mencegah eskalasi krisis fisik' adalah klaim hipotesis terapan,    |
|   bukan fakta empiris yang sudah terbukti di lapangan.                                             |
| - Validitas prediksi prospektif memerlukan pengujian 'time-forward testing' pada insiden masa depan.|
| STATUS: Merupakan agenda pengujian empiris jangka panjang (S3 Doctoral Roadmap).                   |
+----------------------------------------------------------------------------------------------------+
```

---

## 5. BATASAN PENELITIAN (*LIMITATIONS*) & ANCAMAN VALIDITAS (*THREATS TO VALIDITY*)

Setiap karya ilmiah Scopus Q1 wajib mendeklarasikan batas validitasnya secara jujur:
1. **Bias Platform & Representasi Ekologis (*Platform Bias*):**  
   Pengguna media sosial X di Indonesia didominasi oleh kelas menengah perkotaan, jurnalis, dan aktivis politik. Lived experiences siswa SD pedesaan dan pengusaha katering lokal beredar lebih luas di **TikTok** (video unboxing makanan) dan **WhatsApp** (grup wali murid), yang tidak terjangkau oleh scraper API X.
2. **Keterbatasan Pelabelan Perak (*Silver-Standard Pretraining*):**  
   Korpus latih utama $N = 5.263$ dilabeli secara semi-otomatis menggunakan Gemini API + filter heuristik (*silver-standard*). Meskipun model dievaluasi secara ketat pada data uji holdout ($n = 1.058$, akurasi 75,99%, Macro-F1 0,4535), potensi noise pelabelan pada kelas minoritas (seperti *anger* dan *sadness* dengan F1 = 0,000) memerlukan validasi anotasi manual multi-penilai independen pada studi lanjutan.
3. **Ketiadaan Sampel Kelas Minoritas Tertentu:**  
   Tidak adanya sampel untuk *joy* dan *surprise*, serta minimnya sampel *fear* ($n=2$), membatasi daya generalisasi model pada 6 kelas emosi aktif.
4. **Sifat Observasional (Non-Kausalitas):**  
   Korelasi antara modularitas jaringan dan dominasi rasa jijik tidak membuktikan bahwa rasa jijik menyebabkan fragmentasi graf secara kausal. Keduanya dapat dipicu oleh variabel perancu ketiga (*confounding factor*), seperti penutupan katering massal oleh dinas kesehatan.

---

## 6. AGENDA RISET JANGKA PANJANG DISERTASI DOKTOR (S3 ROADMAP)

Untuk mengembangkan temuan ini menjadi program riset doktoral berkelas dunia:

1. **Replikasi Lintas Domain Kebijakan Publik (*Cross-Policy Generalization*):**  
   Menguji apakah model *Phygital Gap* berlaku pada kebijakan publik lain di Indonesia, seperti penyesuaian subsidi BBM, integrasi Kelas Rawat Inap Standar (KRIS) BPJS Kesehatan, atau zonasi PPDB sekolah negeri.
2. **Pemodelan Jaringan Dinamis Longitudinal (*TERGM & SIENA*):**  
   Menerapkan *Temporal Exponential Random Graph Models* (TERGM; Krivitsky & Handcock, 2014) dan *Stochastic Actor-Oriented Models* (SAOM; Snijders et al., 2010) untuk memodelkan proses pembentukan relasi jaringan melintasi tahapan siklus kebijakan 2025–2029.
3. **Studi Komparasi Lintas Negara (*Cross-National Comparative Analysis*):**  
   Membandingkan respons afektif digital program makan siang sekolah gratis di Indonesia (MBG) vs India (*PM POSHAN*) vs Jepang (*Kyushoku*), dengan mengontrol indeks kebebasan pers dan penetrasi internet.
4. **Uji Validasi Intervensi Prospektif (*Prospective Intervention Testing*):**  
   Menguji efektivitas sistem peringatan dini (EWS) secara kuasi-eksperimen di dinas komunikasi daerah untuk mengukur apakah respon humas berbasis deteksi dini mampu menurunkan skor modularitas $Q$ dan mengurangi sentimen *Disgust* di ruang publik.
