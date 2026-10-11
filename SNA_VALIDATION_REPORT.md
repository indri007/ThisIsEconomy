# 🕸️ LAPORAN VALIDASI SOCIAL NETWORK ANALYSIS & UJI SENSITIVITAS
### *Social Network Analysis (SNA) Topology, Modularity Decomposition, and Robustness Report*

**Penilai:** Senior Computational Social Science Researcher & Reviewer Scopus Q1  
**Repositori:** `https://github.com/indri007/ThisIsEconomy`  
**Sumber Graf Kanonis:** `data/network_edges.csv`  
**Engine Komputasi:** Python `NetworkX` 3.x, `python-louvain` (Blondel et al., 2008), & NodeXL Pro Academic

---

## 1. DEFINISI FORMAL GRAF & ENTITAS JARINGAN

Graf komunikasi diskursus MBG dimodelkan sebagai graf berarah terbobot (*weighted directed graph*) $G = (V, E, W)$:
* **Himpunan Simpul ($V$):** Akun media sosial X warganet, tokoh politik, kementerian/lembaga negara, media massa, dan agen kecerdasan buatan (`@grok`). Total simpul unik $|V| = 971$.
* **Himpunan Sisi Berarah ($E$):** Interaksi komunikasi langsung berupa *mention* (`@username`) dan balasan (*reply*). Total interaksi mentah $|E_{raw}| = 692$; total relasi berarah unik $|E_{dir}| = 666$; total relasi tak berarah unik $|E_{undir}| = 662$.
* **Bobot Sisi ($W$):** Frekuensi interaksi antara pasangan akun yang sama ($1 \le w \le 10$, rerata bobot $= 1.04$).
* **Penyebutan Diri (*Self-Loops*):** Ditemukan 17 interaksi di mana akun menyebutkan dirinya sendiri dalam utas panjang (*thread self-mention*).

---

## 2. METRIK TOPOLOGI MAKRO KANONIS TERVERIFIKASI

Berdasarkan kalkulasi deterministik pada [`results/macro_topology_metrics.json`](file:///Users/jevin/ThisIsEconomy/results/macro_topology_metrics.json):

```
+-------------------------------------------------------------------------------+
|                      METRIK MAKRO-TOPOLOGI JARINGAN KANONIS                   |
+-------------------------------------------------------------------------------+
| Jumlah Simpul (|V|)                       : 971 akun                          |
| Jumlah Relasi Berarah (|E|)               : 666 relasi unik (692 raw)         |
| Kepadatan Graf (Graph Density)            : 0.000707 (sangat sparse)          |
| Resiprositas Interaksi (Reciprocity)      : 0.0120 (1.20% komunikasi timbal-balik)
| Komponen Terhubung Lemah (WCC)            : 341 komponen terpisah             |
| Komponen Terhubung Kuat (SCC)             : 967 komponen                      |
| Ukuran Komponen Raksasa (|V_giant|)       : 89 simpul (hanya 9.17% populasi)  |
| Diameter Jaringan (Giant Component)       : 9 hop                             |
| Jarak Geodesik Rata-rata (Shortest Path)  : 3.6731                            |
| Koefisien Klastering Rerata               : 0.0171                            |
| Transitivitas (Triadic Closure)           : 0.0261                            |
| Modularity Louvain (Q)                    : 0.9837 (Hiper-terfragmentasi)     |
| Koefisien Asortativitas Derajat (r)       : -0.0847 (Disassortatif)           |
| Derajat Rata-rata (Average Degree)        : 1.37                              |
| Derajat Median (Median Degree)            : 1.0                               |
| Derajat Maksimum (Max Degree)             : 42 (@grok)                        |
| Power-Law Scaling Exponent (Alpha)        : 2.168                             |
+-------------------------------------------------------------------------------+
```

---

## 3. DEKOMPOSISI MATEMATIS MODULARITAS LOUVAIN ($Q = 0.9837$)

### 3.1 Landasan Matematis Formula Newman & Blondel
Modularitas Louvain mengukur kualitas pembagian komunitas dengan membandingkan fraksi sisi internal terhadap ekspektasi acak:
$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i^{in} k_j^{out}}{2m} \right] \delta(c_i, c_j)$$

Dalam graf MBG:
- **Total Sisi Internal Komunitas:** **691 dari 692 sisi (99.86%)** berada di dalam komunitas yang sama ($\delta(c_i, c_j) = 1$).
- **Total Sisi Eksternal Penyeberang (*Bridging Edges*):** Hanya **1 dari 692 sisi (0.14%)** yang menghubungkan dua komunitas yang berbeda!
- Karena hampir seluruh bobot sisi terkonsentrasi di dalam klaster masing-masing dan kepadatan graf global sangat renggang ($\rho = 0.0007$), nilai suku pengurang $\frac{k_i k_j}{2m}$ mendekati nol. Akibatnya, nilai $Q$ secara matematis terdorong mendekati batas atas teoritis ($Q \to 1.0$).

---

### 3.2 Penolakan Hipotesis Polarisasi Biner (Bukan "Perang 2 Kubu")

> [!WARNING]
> **Koreksi Ilmiah Fundamental untuk Manuskrip:**  
> Skor $Q = 0.9837$ sering disalahartikan sebagai bukti terbentuknya polarisasi politik dua kubu besar (*polarized partisan echo chambers*) seperti polarisasi pemilu. Bukti empiris menolak hipotesis ini:
> 1. Graf terpecah menjadi **341 komponen terpisah (Weakly Connected Components)**.
> 2. Sebanyak **232 komponen hanya terdiri dari $\le 2$ simpul** (dyad terisolasi).
> 3. Komponen terbesar (*giant component*) hanya mencakup **89 simpul (9.17%)**.
> 
> **Kesimpulan Substantif:** Struktur ini adalah **Kepulauan Keluhan Terfragmentasi Radikal (*Archipelago of Atomized Grievance Networks*)**. Warganet tidak saling bertempur argumen dalam ruang deliberatif bersama; mereka mengunggah keluhan secara terpisah dalam kantong-kantong percakapan kecil yang terputus satu sama lain.

---

## 4. HASIL UJI SENSITIVITAS & KETAHANAN GRAF (ROBUSTNESS CHECKS)

Berdasarkan eksekusi skrip baru [`scripts/run_sna_sensitivity_analysis.py`](file:///Users/jevin/ThisIsEconomy/scripts/run_sna_sensitivity_analysis.py), diperoleh hasil empiris berikut:

### 4.1 Uji Sensitivitas Definisi Sisi (Edge Definitions)

| Kondisi Eksperimen | Simpul ($|V|$) | Sisi ($|E|$) | Komponen (WCC) | Densitas ($\rho$) | Resiprositas | Interpretasi Ketahanan |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baseline Berarah (Raw)** | 971 | 666 | 341 | 0.000707 | 1.20% | Graf kanonis mention & reply |
| **Representasi Tak Berarah** | 971 | 662 | 341 | 0.001406 | 100.0% | Simetrisasi relasi dyadik |
| **Tanpa Self-Loops** | 971 | 651 | 341 | 0.000691 | 1.23% | Menghapus 15 penyebutan diri; topologi tetap stabil ($Q = 0.9834$) |
| **Ambang Bobot $w \ge 2$** | 27 | 18 | 10 | 0.025641 | 0.00% | Hanya menyisakan 27 akun; membuktikan mayoritas relasi bersifat sporadis |
| **Komponen Raksasa Saja** | 89 | 89 | 1 | 0.011364 | 0.00% | Inti terhubung MBG tetap memiliki resiprositas nol |

---

### 4.2 Uji Sapuan Parameter Resolusi Louvain ($\gamma \in [0.5, 2.0]$)

| Resolusi ($\gamma$) | Modularitas ($Q$) | Total Komunitas | Ukuran Komunitas Terbesar | Komunitas Tunggal | Status Ketahanan |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **0.5** | 0.9816 | 344 | 43 | 11 | Sangat Stabil |
| **0.7** | 0.9834 | 342 | 46 | 11 | Titik Konvergensi Baseline |
| **0.8** | 0.9834 | 342 | 46 | 11 | Titik Konvergensi Baseline |
| **0.9** | 0.9834 | 342 | 46 | 11 | Titik Konvergensi Baseline |
| **1.0 (Default)** | **0.9834** | **342** | **46** | **11** | **Standar Baku Manuskrip** |
| **1.1** | 0.9834 | 342 | 46 | 11 | Titik Konvergensi Baseline |
| **1.2** | 0.9834 | 342 | 46 | 11 | Titik Konvergensi Baseline |
| **1.5** | 0.9826 | 343 | 43 | 11 | Variasi Minimal ($< 0.1\%$) |
| **2.0** | 0.9826 | 343 | 43 | 11 | Variasi Minimal ($< 0.1\%$) |

> **Temuan Kritis:** Nilai modularitas $Q$ berada stabil di rentang **0.9816 – 0.9834** di seluruh rentang parameter resolusi $\gamma \in [0.5, 2.0]$. Ini membuktikan bahwa modularitas ekstrem $Q > 0.98$ adalah sifat intrinsik dari struktur wacana data, bukan akibat artefak sensitivitas algoritma.

---

### 4.3 Uji Stabilitas Stokastik Multi-Seed (Seeds 1 s.d. 10)
Uji partisi Louvain pada 10 random seed berbeda menghasilkan:
* **Mean Modularitas:** $Q = 0.983392$
* **Standar Deviasi:** $\sigma = 0.000000$ (Variansi nol)
* **Jumlah Komunitas:** 342 komunitas konsisten di seluruh 10 run.

---

## 5. TIPOLOGI PERAN KOMUNIKASI AKTOR KUNCI

| Aktor | Peran Struktural | In-Degree | Out-Degree | Betweenness | Signifikansi Komunikasi Politik |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `@prabowo` | **Target Sink (Otoritas Kebijakan)** | **15** | **0** | 0.000000 | Menjadi sasaran utama aduan masyarakat; menerapkan *broadcast detachment* (nol balasan). |
| `@grok` | **Algorithmic Oracle (AI Platform)** | 0 | **42** | **0.005941** | Sentralitas derajat keluar tertinggi; diangkat warganet menjadi wasit verifikasi fakta keracunan makanan. |
| `@regar_op0sisi`| **Opinion Broker (Pialang Opini)** | 4 | 2 | **0.004564** | Menghubungkan klaster warganet kritis dengan diskursus oposisi nasional. |
| `@4Y4NKZ` | **Secondary Influencer** | 3 | 1 | 0.001820 | Penggerak amplifikasi satire dan bukti foto menu katering MBG. |

---

## 6. VERIFIKASI PENGHAPUSAN METRIK HARDCODED PADA API

Telah dilakukan audit dan perbaikan kode pada layanan backend:
- `backend/services/sna_service.py`: Menghapus baris statis `communities = 342` dan `modularity = 0.9837`, digantikan oleh pembacaan dinamis dari `mbg_network_nodes_final.csv` dan `macro_topology_metrics.json`.
- `backend/services/community_service.py`: Menghapus konstanta statis `total_communities = 342`, digantikan oleh `len(community_counts)` dan pemuatan modularitas dari berkas artefak terversi.
