"""
PATCH untuk run_telegram_paper_pipeline.py (salin-tempel)
=========================================================
Gunakan jika Anda ingin memperbaiki pipeline asli, bukan memakai fix_telegram_pipeline.py.

LANGKAH 1 — tambahkan fungsi bantu ini di bagian atas file (setelah import):
"""
import re
import pandas as pd

YEAR_CANDIDATES = ["publication_year", "year", "pub_year", "publication_date",
                   "published_date", "published", "pub_date", "date", "issued"]


def safe_year(v):
    """Tahun 4 digit atau None. Aman untuk 'UNVERIFIED', NaN, '2025-03-01', dll."""
    try:
        if v is None or pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    m = re.search(r"(19|20)\d{2}", str(v))
    return int(m.group(0)) if m else None


def ensure_publication_year(df):
    """Buat kolom publication_year numerik dari kolom kandidat mana pun yang tersedia."""
    cols = {c.lower(): c for c in df.columns}
    yr = pd.Series([None] * len(df), index=df.index, dtype="object")
    for c in YEAR_CANDIDATES:
        if c in cols:
            vals = df[cols[c]].map(safe_year)
            yr = yr.where(yr.notna(), vals)
    df["publication_year"] = pd.to_numeric(yr, errors="coerce").astype("Int64")
    return df


"""
LANGKAH 2 — di fungsi cleaning() (baris ~181), GANTI:

    df = df[(df["publication_year"] >= 2024) & (df["publication_year"] <= 2026)]

DENGAN:

    df = ensure_publication_year(df)
    unknown = df[df["publication_year"].isna()]
    unknown.to_csv(OUTPUT_DIR / "unknown_year.csv", index=False)   # sesuaikan nama variabel folder output
    df = df[(df["publication_year"] >= 2024) & (df["publication_year"] <= 2026)]
    logger.info(f"Filter tahun: {len(df)} lolos, {len(unknown)} tanpa tahun dipisahkan")

PENTING: jika kolom tahun memang tidak pernah diambil pada tahap discovery, tambahkan pada
tahap discovery/DOI validation pengambilan tahun dari metadata (Crossref: message.published.date-parts[0][0];
OpenAlex: publication_year). Tanpa itu, semua rekaman akan masuk unknown_year.csv.


LANGKAH 3 — di generate_review() (baris ~540), GANTI:

    lines.append(f"- **{row['title']}** ({int(row['publication_year'])}) – DOI: ...")

DENGAN:

    y = safe_year(row.get('publication_year'))
    lines.append(f"- **{row['title']}** ({y if y else 'tahun tidak diketahui'}) – DOI: {row.get('doi', 'N/A')} – "
                 f"Citations: {row.get('cited_by_count', '0')} – Category: {row.get('relevance_category')}")


LANGKAH 4 — di generate_summary() (baris ~580), GANTI:

    lines.append(f"- {row['title']} ({int(row['publication_year'])}) – Score: {row['composite_score']:.2f}")

DENGAN:

    y = safe_year(row.get('publication_year'))
    sc = pd.to_numeric(row.get('composite_score'), errors='coerce')
    lines.append(f"- {row['title']} ({y if y else 'tahun tidak diketahui'}) – "
                 f"Score: {'—' if pd.isna(sc) else f'{sc:.2f}'}")


LANGKAH 5 — status Scopus/Q1:
Jangan mengisi quartile dari tebakan. Isi hanya dari sumber yang dapat diverifikasi:
  - SCImago (gratis, berbasis Scopus): cocokkan ISSN -> 'SJR Best Quartile'  (lihat fix_telegram_pipeline.py --scimago)
  - atau Scopus Serial Title API (butuh API key Elsevier institusi).
Rekaman yang tidak cocok tetap 'UNVERIFIED'.
"""
