# 🔄 PANDUAN REPRODUSIBILITAS RISET
### *Step-by-Step Reproducibility and Replication Guide*

**Repositori:** `https://github.com/indri007/ThisIsEconomy`  
**Protokol Baku:** Standar Protokol Validasi v2 (Group-Aware Split & Validation-Selected Checkpoint)  
**Versi Lingkungan:** Python 3.10–3.13, PyTorch 2.x, Transformers 4.x, NetworkX 3.x

---

## 1. PENYIAPAN LINGKUNGAN KOMPUTASI

### 1.1 Persyaratan Dependensi
Pastikan dependensi utama terpasang sesuai berkas [`requirements.txt`](file:///Users/jevin/ThisIsEconomy/requirements.txt):
```bash
# Buat dan aktifkan virtual environment (opsional namun disarankan)
python3 -m venv venv
source venv/bin/activate

# Instal dependensi riset inti
pip install -r requirements.txt
```

### 1.2 Standarisasi Random Seed
Untuk menjamin determinisme hasil komputasi di seluruh mesin, variabel pseudo-random distandarisasi pada:
```python
RANDOM_SEED = 42
```
Semua skrip pelatihan, partisi data, dan pembentukan komunitas Louvain menggunakan benih acak ini.

---

## 2. TAHAPAN MENJALANKAN PIPELINE LENGKAP

### Langkah 1: Verifikasi Integritas Data & Partisi Bebas Kebocoran
Jalankan skrip pemeriksaan integritas data:
```bash
python scripts/verify_all_data_integrity.py
```
*Tujuan:* Memastikan berkas data utama ada, tidak korup, dan tidak ada baris kosong pada teks maupun label.

Untuk memverifikasi bahwa partisi data latih dan uji bebas dari kebocoran teks duplikat:
```bash
python -c "
import pandas as pd
train_df = pd.read_csv('results/emotion_train_group_split.csv')
test_df = pd.read_csv('results/emotion_test_group_split.csv')
overlap = set(train_df['processed_text']).intersection(set(test_df['processed_text']))
assert len(overlap) == 0, f'Terdeteksi kebocoran {len(overlap)} teks!'
print('✅ VERIFIKASI BERHASIL: 0 Text Overlap antara Train dan Test set!')
"
```

---

### Langkah 2: Pelatihan & Seleksi Model IndoBERT (Protokol v2)
Jalankan pelatihan IndoBERT dengan protokol seleksi model murni pada *Validation Split*:
```bash
python scripts/train_indobert_v2_val_protocol.py
```
*Deskripsi Alur:*
1. Membaca `results/emotion_train_group_split.csv` ($N = 4.205$).
2. Membagi 10% subset validasi independen ($N = 420$) menggunakan `GroupShuffleSplit(random_state=42)`.
3. Melakukan fine-tuning model dasar `indobenchmark/indobert-base-p2` selama 3 epoch dengan batch size 32 dan learning rate $2 \times 10^{-5}$.
4. Memilih checkpoint terbaik berdasarkan nilai terendah `eval_loss` pada subset validasi (terpilih: Epoch 1.0, val loss = 0.5068).
5. Mengevaluasi checkpoint terbaik tepat SATU KALI pada set uji holdout murni `results/emotion_test_group_split.csv` ($N = 1.058$).
6. Melatih ulang baseline klasik TF-IDF + Logistic Regression dan TF-IDF + Linear SVM pada subset latih yang sama.
7. Menyimpan seluruh artefak ke direktori `results/indobert_group_aware_v2/`.

---

### Langkah 3: Evaluasi Konsensus Standar Emas Manusia (n = 100)
Untuk mereproduksi metrik reliabilitas antar-penilai (Cohen's $\kappa$, Fleiss' $\kappa$, Krippendorff's $\alpha$):
```bash
python scripts/run_multi_annotator_agreement_validation.py
```
*Hasil yang Dihasilkan:*
- Kesepakatan antar-pakar: $\kappa = 0.9135$, raw agreement = $95.00\%$.
- Tri-rater reliability: Fleiss' $\kappa = 0.8442$, Krippendorff's $\alpha = 0.8447$.
- IndoBERT vs Gold Standard: Akurasi = $90.00\%$, Macro-F1 = $0.8097$.
- Berkas output: `results/MULTI_ANNOTATOR_GOLD_VALIDATION_REPORT.json` dan `.md`.

---

### Langkah 4: Rekalkulasi Analisis Jaringan Sosial (SNA) Kanonis
Untuk menghitung ulang 22 metrik topologi jaringan dari edge list kanonis (`data/network_edges.csv`):
```bash
python scripts/recalculate_sna_canonical_pipeline.py
```
*Hasil yang Dihasilkan:*
- Memvalidasi $|V| = 971$, $|E| = 692$ (666 unik berarah).
- Menghitung densitas $\rho = 0.000707$, resiprositas $r = 1.20\%$, WCC $= 341$, modularitas Louvain $Q = 0.9837$.
- Berkas output tersimpan di `results/sna_canonical_pipeline/`.

---

### Langkah 5: Eksekusi Uji Sensitivitas & Ketahanan Struktur Graf
Untuk mereproduksi uji sensitivitas definisi tepi dan sapuan parameter resolusi komunitas Louvain:
```bash
python scripts/run_sna_sensitivity_analysis.py
```
*Hasil yang Dihasilkan:*
- Membandingkan graf berarah, tak berarah, tanpa self-loops, dan ambang bobot $w \ge 2$.
- Sapuan parameter resolusi $\gamma \in [0.5, 2.0]$.
- Uji stabilitas stokastik modularitas pada 10 random seed ($\text{std}(Q) = 0.0$).
- Berkas output: `results/sna_sensitivity_analysis.json`, `sna_sensitivity_analysis.csv`, dan `sna_resolution_sweep.csv`.

---

### Langkah 6: Audit Ketimpangan Minoritas & Taksonomi Bertingkat
Untuk mereproduksi diseksi sampel minoritas (Marah $n=14$, Sedih $n=3$) dan kinerja taksonomi bertingkat 3-super-kelas:
```bash
python scripts/run_minority_class_imbalance_audit.py
```
*Hasil yang Dihasilkan:*
- Membuktikan lonjakan Macro-F1 dari 0.4535 ke **0.7522 (+29.87%)** saat diagregasi ke valensi Negatif/Positif/Netral.
- Berkas output: `results/MINORITY_CLASS_IMBALANCE_AUDIT_REPORT.json` dan `.md`.

---

### Langkah 7: Pengujian Regresi Otomatis (Automated Test Suite)
Jalankan seluruh rangkaian uji unit dan integrasi untuk memastikan stabilitas sistem:
```bash
pytest
```
*Kriteria Lulus:* Seluruh 85 pengujian wajib berstatus **PASSED (100%)**.

---

## 3. MANIFEST ARTEFAK HASIL EVALUASI

| Nama File Artefak | Lokasi | Keterangan Isi |
| :--- | :--- | :--- |
| `classification_report_v2.csv` | `results/indobert_group_aware_v2/` | Metrik resmi per kelas IndoBERT Protokol v2 |
| `model_comparison_v2.csv` | `results/indobert_group_aware_v2/` | Komparasi IndoBERT vs TF-IDF LogReg & SVM |
| `confusion_matrix_v2.png` | `results/indobert_group_aware_v2/` | Visualisasi matriks konfusi resmi |
| `macro_topology_metrics.json` | `results/` | 22 parameter makro graf berarah |
| `sna_sensitivity_analysis.json` | `results/` | Hasil uji sensitivitas graf dan komunitas |
| `multi_annotator_batch_100_GOLD.csv` | `data/annotation/` | Standar emas manusia 100 cuitan teradjudikasi |
| `dataset_sindiran_valid.csv` | `data/sarcasm/` | 3.395 cuitan validasi sindiran |
