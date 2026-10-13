# Social Network Analysis (SNA) Consistency Report

## 1. Topologi Jaringan Canonical
Analisis graf interaksi media sosial warganet terkait MBG dibangun dari daftar edge tunggal canonical (`data/network_edges.csv`).

### Hasil Verifikasi Matematis Ulang (NetworkX DiGraph):
- **Jumlah Node Vertices ($\|V\|$):** 971 aktor unik
- **Jumlah Edge Terarah ($\|E\|$):** 666 interaksi unik (berasal dari 692 interaksi mentah setelah pembersihan duplikasi dan self-loops)
- **Densitas Jaringan ($d$):** 0.000707 (ekstrem jarang / *sparse*)
- **Resiprositas ($r$):** 0.01201 (1.20% interaksi dua arah)
- **Modularity Louvain ($Q$):** 0.9837 (332 komunitas terdeteksi)

## 2. Aktor Kunci & Verifikasi Tipologi
- **In-Degree Tertinggi (Otoritas Pasif):**
  - `@prabowo`: In-Degree = 15, Out-Degree = 0 (Konfirmasi empiris fenomena *power vacuum* / *unresponsive broadcast posture*)
  - `@tanyakanrl`: In-Degree = 5
  - `@regar_op0sisi`: In-Degree = 5
- **Out-Degree Tertinggi (Penyebar Informasi / Rujukan):**
  - `@grok`: Out-Degree = 42, In-Degree = 1 (*Algorithmic Oracle* kecerdasan buatan)
  - `@4Y4NKZ`: Out-Degree = 15
  - `@newIding30`: Out-Degree = 15

## 3. Konsistensi Terhadap Purifikasi Emosi
Topologi jaringan komunikasi dibangun berdasarkan relasi interaksi langsung (mention, quote, reply) antarakun. Struktur graf canonical terbukti stabil dan independen dari klasifikasi teks. Namun, pemetaan profil emosi per klaster (*community emotion profiling*) harus menggunakan data inferensi yang telah dipurifikasi dari spam homonim non-kebijakan agar proporsi sentimen komunitas mencerminkan sikap autentik publik.
