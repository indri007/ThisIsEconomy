# Laporan Analisis Dimensi 3: Partisi Komunitas & Deteksi Ruang Gema (SNA MBG)

## 1. Parameter Topologi & Isolasi Struktural (Echo Chamber Metrics)

- **Algoritma Partisi:** Louvain Modularity Optimization (Blondel dkk., 2008)
- **Skor Modularitas ($Q$):** **0.9837** (Ambang Batas Polarisasi Ekstrem $Q > 0,30$; Newman, 2006)
- **Total Komunitas Terbentuk:** **342** kelompok wacana independen
- **Total Relasi Komunikasi (|E|):** **692** interaksi terarah
- **Tepi Internal (Dalam Komunitas / Ruang Gema):** **691** relasi (**99.86%**)
- **Tepi Lintas-Batas (Penghubung Antar-Komunitas):** **1** relasi (**0.14%**)
- **Tingkat Kedap Ruang Gema (*Echo Chamber Ratio*):** **99.86%** (Menunjukkan fragmentasi komunikasi parah tanpa adanya jembatan dialog publik antar-kelompok)

## 2. Tabel Ringkasan Komunitas Utama & Karakteristik Afektif

| No | Klaster | Label Tema Wacana | Aktor (|V|) | Emosi Dominan | Tokoh Kunci |
| :-: | :---: | :--- | :---: | :---: | :--- |
| 1 | **#15** | Klaster Elit & Target Otoritas (@prabowo, @regar_op0sisi) | 46 (4.74%) | **DISGUST** | @prabowo, @regar_op0sisi, @daffiriffi |
| 2 | **#61** | Klaster AI Fact-Checking Oracle (@grok) | 43 (4.43%) | **NEUTRAL** | @grok, @unmagnetism, @JuanJulianto2 |
| 3 | **#16** | Klaster Diskursus Kritis Warganet (@4Y4NKZ, @newIding30) | 18 (1.85%) | **NEUTRAL** | @4Y4NKZ, @newIding30, @Capitalisborju |
| 4 | **#259** | Klaster Percakapan Solidaritas Publik (@dbdbidip, @greeniefloo) | 14 (1.44%) | **NEUTRAL** | @dbdbidip, @greeniefloo, @renregalia |
| 5 | **#8** | Klaster Komunikasi Internasional / Akun Global (@Casagrande10939) | 11 (1.13%) | **NEUTRAL** | @Casagrande10939, @SauloLinsFreir1, @misteriouspavao |
| 6 | **#264** | Klaster Diskusi Sosial Interaktif (@luvdysh_, @helloyosh_) | 10 (1.03%) | **NEUTRAL** | @luvdysh_, @helloyosh_, @ayiurswoo |

---

*Catatan Metodologis:* Data dihitung dari korpus resmi relasi interaksi media sosial X (|V|=971 aktor, |E|=692 relasi terarah) yang dipartisi menggunakan optimasi modularitas Louvain standar NodeXL Pro & NetworkX.
