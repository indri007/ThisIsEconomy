# Laporan Analisis Makro Topologi Jaringan Komunikasi MBG (NodeXL & NetworkX)

Tabel ini merangkum metrik parameter topologi makro dari graf komunikasi platform X (|V|=971, |E|=666):

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
| **Modularitas Louvain (Q)** | **0.9837** | Polarisasi ekstrem (Q > 0.4 membuktikan echo chamber) |
| **Koefisien Asortativitas (r)** | **-0.0847** | Hubungan disassortative (warga biasa mengarah ke hub elit) |
| **Eksponen Power-Law (Alpha)** | **2.17** | Struktur jaringan bebas-skala (*scale-free topology*) |

