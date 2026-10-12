# Status berkas anotasi (per 12 Okt 2026)

| Berkas | Status |
|---|---|
| `researcher_batch_100.csv` | Sampel 100 tweet (memuat prediksi IndoBERT & label silver). **Jangan diberikan ke penilai**. |
| `annotator_template.csv` | Templat kosong untuk penilai: hanya `annotation_id` dan `text`. |
| `researcher_batch_100_FILLED.csv` | **Bukan anotasi manusia.** Dibuat skrip lama: 79 label menyalin label silver, 21 label ditulis di kode. |
| `multi_annotator_batch_100_GOLD.csv` | **Bukan anotasi manusia.** Label "Penilai 2" disalin dari Penilai 1 dengan 5 perbedaan yang ditulis di kode. |
| `gold_standard_9_emosi_annotated.csv`, `mined_joy_surprise_candidates.csv` | Belum diaudit; jangan dikutip sebagai gold standard sebelum diperiksa. |

## Cara membuat validasi manusia yang sah
1. Salin `annotator_template.csv` menjadi `annotator_1.csv` dan `annotator_2.csv`.
2. Dua penilai mengisi kolom `label` **secara terpisah**, tanpa melihat prediksi model, label silver, atau hasil penilai lain. Gunakan `RESEARCHER_ANNOTATION_INSTRUCTIONS.txt`.
3. Jalankan `python scripts/run_multi_annotator_agreement_validation.py` untuk menghitung kappa dan alpha.
4. Diskusikan kasus yang tidak sepakat, simpan hasilnya sebagai `adjudicated_gold.csv`, lalu jalankan skrip yang sama lagi untuk membandingkan IndoBERT dengan gold.
5. Laporkan angka apa adanya di manuskrip, termasuk bila hasilnya rendah.
