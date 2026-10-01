# Validation Status — MBG Thesis

## Dimension 1: Automated Verification Coverage

> 28/28 checks PASS = 100% automated verification coverage.
> Ini mengukur: apakah semua pipeline, file, metrik, dan prosedur telah berjalan
> dan menghasilkan output yang konsisten secara komputasional.

| Area | Status | Score |
|------|--------|-------|
| Data & pipeline | ✅ | 15/15 |
| Split & leakage control | ✅ | 10/10 |
| IndoBERT evaluation | ✅ | 10/10 |
| Baseline comparison (4 model + CI) | ✅ | 10/10 |
| CI & uncertainty (Bootstrap n=2000) | ✅ | 10/10 |
| Effect size (Cohen's d + Δ) | ✅ | 5/5 |
| Statistical testing (McNemar + Wilcoxon) | ✅ | 5/5 |
| Provenance/reproducibility (SHA-256) | ✅ | 10/10 |
| Automated audit | ✅ | 10/10 |
| Independent ground truth (IndoNLU EmoT) | ✅ | 10/10 |
| Reference-label/model agreement (κ=0.6492) | ✅ | 5/5 |
| External/generalization (JS=0.4705) | ✅ | 5/5 |

**Automated coverage: 105/105 = 100%**

---

## Dimension 2: Scientific Validation Maturity

> Ini mengukur: apakah klaim ilmiah dalam tesis didukung oleh bukti
> yang memenuhi standar peer-review NLP/computational linguistics.

| Area | Status | Catatan |
|------|--------|---------|
| Model performance metrics | ✅ Verified | Acc=0.794, F1=0.516, 95% CI |
| Leakage-free split | ✅ Verified | NO_LEAKAGE, overlap=0 |
| Statistical significance | ✅ Verified | McNemar p<10⁻¹⁵, Wilcoxon p<10⁻¹⁵ |
| Effect size | ✅ Verified | Δacc +0.099–+0.122 vs baseline |
| Provenance | ✅ Verified | SHA-256 + reproducibility audit |
| Independent external GT | ✅ Verified | IndoNLU EmoT (human-annotated, Koto et al. 2020) |
| Reference-label/model agreement | ✅ Terukur | κ=0.6492 (Substantial) — bukan IAA |
| Domain shift quantification | ✅ Verified | JS-divergence=0.4705 |
| **Human-human IAA** | ⚠️ Belum ada | Memerlukan ≥2 anotator manusia independen |

**Scientific maturity: STRONG untuk automated + external metrics;**
**PARTIAL untuk label quality (silver-standard, bukan human-adjudicated).**

---

## Catatan Metodologis Penting

> **κ = 0,6492 adalah *reference-label/model agreement*, bukan IAA.**
>
> Kategori *substantial* mengikuti klasifikasi Landis & Koch (1977),
> tetapi klasifikasi tersebut tidak mengubah jenis pasangan yang dibandingkan
> menjadi IAA. Threshold κ ≥ 0,60 digunakan sebagai **threshold operasional
> penelitian ini** — bukan "IAA threshold yang secara umum diterima" tanpa
> kualifikasi, karena standar agreement bergantung pada desain anotasi, task,
> label distribution, dan bidang penelitian (Artstein & Poesio, 2008).

**Referensi:**
- Landis, J.R., & Koch, G.G. (1977). Biometrics, 33(1), 159–174.
- Artstein, R., & Poesio, M. (2008). Computational Linguistics, 34(4), 555–596.
