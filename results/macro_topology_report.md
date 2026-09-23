# Laporan Analisis Makro Topologi Jaringan Komunikasi MBG (NodeXL & NetworkX)

Tabel ini merangkum metrik parameter topologi makro dari graf komunikasi platform X (|V|=971; 692 raw interaction records; 666 unique directed edges; 662 unique undirected pairs):

| Parameter Topologi Makro | Nilai Empiris | Interpretasi Ilmiah |
| :--- | :---: | :--- |
| **Tipe Graf** | Directed (Asymmetric Mention & Reply Network) | Arah komunikasi interaksi (mention/reply) |
| **Jumlah Simpul (|V|)** | **971** | Total akun pengguna aktif teridentifikasi |
| **Jumlah Tepi Total (|E|)** | **692** | Total relasi komunikasi empiris |
| **Tepi Terarah Unik** | 666 | Relasi asimetris antar-pasang akun |
| **Resiprositas (Reciprocity)** | **1.20%** | Proporsi dialog timbal balik (sangat rendah = monolog) |
| **Kepadatan Graf (Graph Density)** | **0.000707** | Tingkat kerapatan interaksi (sangat renggang/sparse) |
| **Komponen Terhubung (WCC)** | 341 | Jumlah pulau diskursus independen |
| **Ukuran Komponen Raksasa** | 89 (9.17%) | Inti gravitasi percakapan utama wacana MBG |
| **Diameter Jaringan** | **9** | Jarak terpanjang yang memisahkan dua aktor |
| **Jarak Rerata Terpendek** | **3.67** | Langkah transmisi rata-rata penyebaran pesan |
| **Koefisien Clustering Rerata** | 0.0171 | Kecenderungan warganet membentuk kelompok segitiga |
| **Modularitas Louvain (Q)** | **0.9837** | Struktur komunitas kuat; Q tidak dengan sendirinya membuktikan echo chamber |
| **Koefisien Asortativitas (r)** | **-0.0847** | Pola pencampuran derajat yang cenderung disassortative |
| **Eksponen Power-Law (Alpha)** | **2.17** | Estimasi struktur derajat heavy-tailed; bukan bukti definitif power-law |

