# Pedoman Anotasi 9 Emosi Plutchik Diskursus Program Makan Bergizi Gratis (MBG)

Dokumen ini merupakan panduan operasional independen untuk dua penilai (*double-blind independent annotators*) dalam mengklasifikasikan ekspresi afektif warganet terkait Program MBG.

## 1. Etika & Integritas Independensi
1. **Double-Blind**: Kedua penilai TIDAK DIPERBOLEHKAN berkomunikasi, bertukar lembar kerja, atau melihat prediksi model IndoBERT selama proses anotasi berlangsung.
2. **Objektivitas**: Beri label berdasarkan apa yang tertulis dalam teks dan konteks wacana, bukan asumsi politik pribadi.
3. **Kerahasiaan**: Anotasi disimpan menggunakan pseudonim penilai (`ANON_RATR_01` dan `ANON_RATR_02`).

## 2. Taksonomi 9 Kategori Emosi
Setiap cuitan wajib diberi tepat satu label emosi dominan dari 9 kategori berikut:

1. **Jijik (Disgust)**: Reaksi visceral terhadap makanan basi, bau, ulat, belatung, keracunan, keluhan fisik mual/diare, atau penolakan moral terhadap korupsi pengadaan vendor.
2. **Percaya (Trust)**: Ekspresi keyakinan, dukungan afirmatif terhadap program, kepuasan terhadap transparansi pemerintah, pujian atas niat baik kepemimpinan.
3. **Netral (Neutral)**: Berita fakta, statistik resmi, pengumuman anggaran tanpa muatan opini, atau cuitan yang tidak menunjukkan muatan afeksi spesifik.
4. **Tertarik (Interest/Anticipation)**: Rasa ingin tahu, antusiasme menunggu jadwal distribusi, pertanyaan konstruktif, pengawasan kritis tanpa sentimen jijik.
5. **Marah (Anger)**: Kemarahan meledak-ledak, makian kasar, ancaman, kemurkaan terhadap ketidakadilan birokrasi tanpa penekanan pada aspek visceral fisik.
6. **Sedih (Sadness)**: Kesedihan, keprihatinan mendalam atas nasib anak sekolah, perasaan iba, patah hati atas kegagalan program.
7. **Takut (Fear)**: Kecemasan akan keselamatan anak, kekhawatiran dampak jangka panjang racun atau defisit fiskal negara.
8. **Bahagia (Joy)**: Kegembiraan murni, tawa bahagia anak-anak menyantap makanan enak.
9. **Kaget (Surprise)**: Keterkejutan mendadak atas informasi tak terduga terkait program.

## 3. Skala Keyakinan (*Confidence Score*)
Isi kolom `confidence_1to5` dengan skala:
- `5`: Sangat yakin (makna eksplisit dan tanpa ambiguitas).
- `4`: Yakin (makna tersirat jelas).
- `3`: Cukup yakin (ada potensi makna ganda / satir tipis).
- `2`: Ragu (sangat bergantung pada konteks luar teks).
- `1`: Sangat ragu.

## 4. Alur Adjudikasi Konsensus
- Setelah kedua penilai selesai mengisi lembar kerja masing-masing secara independen:
  1. Skrip otomatis akan menghitung nilai riil Cohen's Kappa ($\kappa$) dan Krippendorff's Alpha ($\alpha$).
  2. Entri yang memiliki perbedaan label akan masuk ke tahap **Adjudikasi Konsensus** yang ditinjau bersama arbiter ketiga untuk menyusun *Gold Standard Final*.
