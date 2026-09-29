#!/usr/bin/env python3
"""
Perbaikan Pipeline Literatur Telegram (tesis MBG)
=================================================

Memperbaiki 3 masalah pada run_telegram_paper_pipeline.py (lihat pipeline_errors.log):
  1. cleaning()          -> KeyError: 'publication_year'  (kolom tahun tidak ada/beda nama)
  2. generate_review()   -> ValueError: int('UNVERIFIED')
  3. generate_summary()  -> ValueError: int('UNVERIFIED')
Sekaligus:
  4. Melengkapi metadata dari Crossref berdasarkan DOI (penulis, tahun, jurnal, ISSN, jumlah sitasi)
  5. Verifikasi kuartil via file SCImago (sumber data Scopus) berdasarkan ISSN
  6. Menerapkan filter 2024–2026 dengan benar dan memisahkan rekaman yang tahunnya tidak diketahui

Contoh
------
  # tanpa internet (hanya perbaiki tahun + filter + laporan)
  python fix_telegram_pipeline.py --master telegram_literature_master.csv --out hasil_fix

  # lengkap: Crossref + SCImago
  python fix_telegram_pipeline.py --master telegram_literature_master.csv --out hasil_fix \
      --crossref --email emailanda@domain.ac.id --scimago scimagojr_2025.csv

File SCImago: unduh dari https://www.scimagojr.com/journalrank.php  (tombol "Download data"),
format CSV dengan pemisah titik koma.

Output (folder --out)
  master_fixed.csv          seluruh rekaman + kolom baru (publication_year, quartile, dll.)
  filtered_2024_2026.csv    rekaman dengan tahun 2024–2026
  unknown_year.csv          rekaman tanpa tahun (cek manual)
  q1_verified.csv           rekaman dengan kuartil Q1 terverifikasi SCImago
  TELEGRAM_BOT_LITERATURE_REVIEW.md   daftar pustaka ringkas (tanpa crash)
  telegram_literature_summary.txt     ringkasan angka
  crossref_cache.json       cache agar tidak memanggil ulang API
"""
import argparse
import json
import os
import re
import time

import pandas as pd

YEAR_CANDIDATES = ["publication_year", "year", "pub_year", "publicationyear", "published_year",
                   "publication_date", "published_date", "published", "pub_date", "date",
                   "issued", "created", "cover_date", "coverdate"]
MISSING = {"", "nan", "none", "null", "unverified", "unknown", "n/a", "na", "-"}


# ---------------------------------------------------------------- utilitas aman
def safe_year(v):
    """Ambil tahun 4 digit dari nilai apa pun; kembalikan None jika tidak ada. Tidak pernah crash."""
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    s = str(v).strip()
    if s.lower() in MISSING:
        return None
    m = re.search(r"(19|20)\d{2}", s)
    return int(m.group(0)) if m else None


def year_label(v):
    y = safe_year(v)
    return str(y) if y else "tahun tidak diketahui"


def norm_doi(d):
    if not isinstance(d, str):
        return None
    d = d.strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", d)
    return d if re.match(r"^10\.\d{4,9}/\S+$", d) else None


def norm_issn(s):
    if not isinstance(s, str):
        return []
    return [re.sub(r"[^0-9x]", "", x.lower()) for x in re.split(r"[,;\s]+", s) if x.strip()]


# ---------------------------------------------------------------- tahun
def ensure_year(df):
    cols = {c.lower().strip(): c for c in df.columns}
    found = [cols[c] for c in YEAR_CANDIDATES if c in cols]
    print(f"[tahun] kolom kandidat ditemukan: {found or 'TIDAK ADA'}")
    yr = pd.Series([None] * len(df), index=df.index, dtype="object")
    src = pd.Series([None] * len(df), index=df.index, dtype="object")
    for c in found:
        vals = df[c].map(safe_year)
        fill = yr.isna() & vals.notna()
        yr[fill] = vals[fill]
        src[fill] = c
    df["publication_year"] = pd.to_numeric(yr, errors="coerce").astype("Int64")
    df["year_source"] = src
    return df


# ---------------------------------------------------------------- Crossref
def crossref_enrich(df, email, cache_path, sleep=0.12):
    import urllib.request
    import urllib.error
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    ua = f"telegram-lit-fix/1.0 (mailto:{email})" if email else "telegram-lit-fix/1.0"
    ok = fail = 0
    for i, r in df.iterrows():
        doi = norm_doi(r.get("doi"))
        if not doi:
            continue
        if doi not in cache:
            url = f"https://api.crossref.org/works/{urllib.request.quote(doi)}"
            if email:
                url += f"?mailto={email}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": ua})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    cache[doi] = json.load(resp)["message"]
                time.sleep(sleep)
            except Exception as e:  # jaringan terblokir / DOI tidak terdaftar di Crossref
                cache[doi] = {"_error": str(e)[:200]}
        m = cache[doi]
        if "_error" in m:
            fail += 1
            continue
        ok += 1
        auth = m.get("author", [])
        df.at[i, "cr_authors"] = "; ".join(f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in auth)
        df.at[i, "cr_container"] = (m.get("container-title") or [""])[0]
        df.at[i, "cr_issn"] = ", ".join(m.get("ISSN", []))
        df.at[i, "cr_type"] = m.get("type")
        df.at[i, "cr_publisher"] = m.get("publisher")
        df.at[i, "cr_cited_by"] = m.get("is-referenced-by-count")
        dp = (m.get("published") or m.get("issued") or {}).get("date-parts", [[None]])[0]
        if dp and dp[0] and pd.isna(df.at[i, "publication_year"]):
            df.at[i, "publication_year"] = int(dp[0])
            df.at[i, "year_source"] = "crossref"
    json.dump(cache, open(cache_path, "w"))
    print(f"[crossref] berhasil {ok}, gagal {fail} (cache: {cache_path})")
    if ok == 0 and fail:
        print("[crossref] Semua panggilan gagal — cek koneksi internet. Pipeline tetap lanjut tanpa pengayaan.")
    return df


# ---------------------------------------------------------------- SCImago
def scimago_verify(df, path):
    sj = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8", on_bad_lines="skip")
    need = {"Issn", "SJR Best Quartile", "Title"}
    if not need <= set(sj.columns):
        raise SystemExit(f"[scimago] kolom wajib {need} tidak ada; cek file unduhan SCImago")
    year_tag = re.search(r"(20\d{2})", os.path.basename(path))
    year_tag = year_tag.group(1) if year_tag else "?"
    idx = {}
    for _, r in sj.iterrows():
        for s in norm_issn(r["Issn"]):
            idx[s] = (r["SJR Best Quartile"], r["Title"], r.get("Categories", ""))
    issn_cols = [c for c in df.columns if "issn" in c.lower()]
    if not issn_cols:
        print("[scimago] tidak ada kolom ISSN (jalankan dengan --crossref). Verifikasi dilewati.")
        return df
    hit = 0
    for i, r in df.iterrows():
        issns = [x for c in issn_cols for x in norm_issn(r.get(c))]
        for s in issns:
            if s in idx:
                q, t, cat = idx[s]
                df.at[i, "quartile"] = q if q and q != "-" else "UNVERIFIED"
                df.at[i, "quartile_year"] = year_tag
                df.at[i, "quartile_source"] = f"SCImago {year_tag} (Best Quartile)"
                df.at[i, "scopus_status"] = "INDEXED (SCImago/Scopus)"
                df.at[i, "sj_title"] = t
                df.at[i, "sj_categories"] = cat
                hit += 1
                break
        else:
            if str(df.at[i, "scopus_status"]) in ("nan", "None", "UNVERIFIED", ""):
                df.at[i, "scopus_status"] = "NOT_FOUND_IN_SCIMAGO"
    print(f"[scimago] {hit} rekaman cocok dengan SCImago {year_tag}")
    return df


# ---------------------------------------------------------------- laporan (pengganti generate_review/summary)
def generate_review(df, path):
    sort_col = "telegram_relevance_score" if "telegram_relevance_score" in df.columns else None
    d = df.sort_values(sort_col, ascending=False) if sort_col else df
    lines = ["# Tinjauan Literatur Bot Telegram", "",
             f"Total rekaman: {len(df)}", ""]
    for _, r in d.iterrows():
        cites = r.get("cr_cited_by", r.get("cited_by_count", 0))
        cites = 0 if pd.isna(cites) else int(float(cites)) if str(cites).replace(".", "", 1).isdigit() else cites
        q = r.get("quartile", "UNVERIFIED")
        lines.append(f"- **{r.get('title','(tanpa judul)')}** ({year_label(r.get('publication_year'))}) – "
                     f"DOI: {r.get('doi') if isinstance(r.get('doi'), str) and r.get('doi').strip() else 'N/A'} – "
                     f"Sitasi: {cites} – Kategori: {r.get('document_category', r.get('relevance_category','-'))} – "
                     f"Kuartil: {q if isinstance(q,str) else 'UNVERIFIED'}")
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def generate_summary(df, filt, unk, path):
    lines = ["RINGKASAN LITERATUR TELEGRAM (setelah perbaikan)", "",
             f"Total rekaman            : {len(df)}",
             f"Tahun 2024–2026          : {len(filt)}",
             f"Tahun di luar rentang    : {df['publication_year'].notna().sum() - len(filt)}",
             f"Tahun tidak diketahui    : {len(unk)}",
             f"DOI valid                : {df['doi'].map(norm_doi).notna().sum() if 'doi' in df else 'kolom doi tidak ada'}",
             "", "Distribusi tahun:"]
    for y, n in df["publication_year"].value_counts(dropna=False).sort_index().items():
        lines.append(f"  {year_label(y)}: {n}")
    if "quartile" in df:
        lines += ["", "Kuartil (hanya dari SCImago; selain itu UNVERIFIED):"]
        for q, n in df["quartile"].fillna("UNVERIFIED").value_counts().items():
            lines.append(f"  {q}: {n}")
    if "composite_score" in df:
        lines += ["", "10 teratas (composite_score):"]
        top = df.assign(_s=pd.to_numeric(df["composite_score"], errors="coerce")).sort_values("_s", ascending=False).head(10)
        for _, r in top.iterrows():
            sc = "—" if pd.isna(r["_s"]) else f"{r['_s']:.2f}"
            lines.append(f"  - {r.get('title')} ({year_label(r.get('publication_year'))}) – Skor: {sc}")
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--master", required=True)
    ap.add_argument("--out", default="hasil_fix")
    ap.add_argument("--year-min", type=int, default=2024)
    ap.add_argument("--year-max", type=int, default=2026)
    ap.add_argument("--crossref", action="store_true", help="lengkapi metadata via Crossref (butuh internet)")
    ap.add_argument("--email", default=None, help="email untuk 'polite pool' Crossref")
    ap.add_argument("--scimago", default=None, help="path file CSV SCImago")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    df = pd.read_csv(args.master, dtype=str)
    print(f"[load] {len(df)} rekaman, {len(df.columns)} kolom")
    for c in ["scopus_status", "quartile", "quartile_year", "quartile_source"]:
        if c not in df.columns:
            df[c] = "UNVERIFIED"
    df = ensure_year(df)
    if args.crossref:
        df = crossref_enrich(df, args.email, os.path.join(args.out, "crossref_cache.json"))
    if args.scimago:
        df = scimago_verify(df, args.scimago)

    yr = df["publication_year"]
    filt = df[(yr >= args.year_min) & (yr <= args.year_max)]
    unk = df[yr.isna()]
    df.to_csv(os.path.join(args.out, "master_fixed.csv"), index=False)
    filt.to_csv(os.path.join(args.out, f"filtered_{args.year_min}_{args.year_max}.csv"), index=False)
    unk.to_csv(os.path.join(args.out, "unknown_year.csv"), index=False)
    df[df["quartile"].astype(str).str.upper() == "Q1"].to_csv(os.path.join(args.out, "q1_verified.csv"), index=False)
    generate_review(filt, os.path.join(args.out, "TELEGRAM_BOT_LITERATURE_REVIEW.md"))
    generate_summary(df, filt, unk, os.path.join(args.out, "telegram_literature_summary.txt"))


if __name__ == "__main__":
    main()
