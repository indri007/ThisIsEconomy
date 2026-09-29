#!/usr/bin/env python3
"""Master Telegram Bot Literature Pipeline (2024‑2026)

This script performs the full end‑to‑end workflow requested:
1️⃣ Discovery via OpenAlex (uses cached `telegram_papers_latest.csv` if present)
2️⃣ Cleaning & deduplication (year filter, DOI validation)
3️⃣ Simple relevance screening (keyword match & citation count)
4️⃣ Placeholder Scopus/Q1 verification (marked UNVERIFIED)
5️⃣ Generates:
   - `telegram_papers_clean.csv` (cleaned dataset)
   - `telegram_paper_review.md` (markdown literature review)
   - `telegram_paper_review.docx` (Word document)

All steps are automated; missing Python dependencies are installed on‑the‑fly.
"""

import sys
import subprocess
import importlib.util
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Helper: ensure required packages are installed
# ---------------------------------------------------------------------------
REQUIRED_PKGS = ["pandas", "requests", "tqdm", "python-docx"]

def install_missing():
    missing = []
    for pkg in REQUIRED_PKGS:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    if missing:
        print(f"[pipeline] Installing missing packages: {missing}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

install_missing()

import pandas as pd
import requests
from tqdm import tqdm
from docx import Document
from docx.shared import Pt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WORKDIR = Path(__file__).parent
RAW_CSV = WORKDIR / "telegram_papers_latest.csv"
CLEAN_CSV = WORKDIR / "telegram_papers_clean.csv"
REPORT_MD = WORKDIR / "telegram_paper_review.md"
REPORT_DOCX = WORKDIR / "telegram_paper_review.docx"

# OpenAlex queries (titles) – these are the exact strings used in the original spec
QUERIES = [
    "Telegram bot",
    "Telegram bots",
    "Telegram bot artificial intelligence",
    "Telegram bot chatbot",
    "Telegram bot NLP",
    "Telegram bot network analysis",
    "Telegram bot misinformation",
    "Telegram bot disinformation",
    "Telegram bot LLM",
    "Telegram bot social network analysis",
]

# ---------------------------------------------------------------------------
# Step 1 – Discovery (cached or fresh)
# ---------------------------------------------------------------------------
def fetch_openalex(query: str, year_from: int = 2024, year_to: int = 2026) -> list[dict]:
    """Fetch works from OpenAlex matching *query* and publication year range.
    Returns a list of dicts with selected fields.
    """
    base_url = "https://api.openalex.org/works"
    # Build filter: title.search & year range
    params = {
        "filter": f"title.search:{query},from_publication_date:{year_from}-01-01,to_publication_date:{year_to}-12-31",
        "per-page": 200,  # max per page
    }
    results = []
    cursor = None
    while True:
        if cursor:
            params["cursor"] = cursor
        resp = requests.get(base_url, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"[pipeline] OpenAlex request failed for '{query}': {resp.status_code}")
            break
        data = resp.json()
        results.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break
    return results

def discovery():
    if RAW_CSV.exists():
        print(f"[pipeline] Using cached discovery file: {RAW_CSV.name}")
        return pd.read_csv(RAW_CSV)
    print("[pipeline] No cached discovery file – querying OpenAlex …")
    all_records = []
    for q in tqdm(QUERIES, desc="OpenAlex queries"):
        works = fetch_openalex(q)
        for w in works:
            # Extract fields – many may be missing, so use .get with defaults
            rec = {
                "title": w.get("title", "").strip(),
                "year": w.get("publication_year"),
                "journal": w.get("host_venue", {}).get("display_name", ""),
                "doi": w.get("doi", "").replace("https://doi.org/", "").strip(),
                "cited_by": w.get("cited_by_count", 0),
                "openalex_id": w.get("id", ""),
                "abstract": w.get("abstract", ""),
            }
            all_records.append(rec)
    df = pd.DataFrame(all_records)
    # Save raw file for reproducibility
    df.to_csv(RAW_CSV, index=False)
    print(f"[pipeline] Saved raw discovery data to {RAW_CSV.name} ({len(df)} rows)")
    return df

# ---------------------------------------------------------------------------
# Step 2 – Cleaning & DOI validation
# ---------------------------------------------------------------------------
def validate_doi(doi: str) -> bool:
    if not doi:
        return False
    url = f"https://doi.org/{doi}"
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        return r.status_code == 200
    except Exception:
        return False

def cleaning(df: pd.DataFrame) -> pd.DataFrame:
    # Drop exact duplicates across all columns
    df = df.drop_duplicates().reset_index(drop=True)
    # Keep only years 2024‑2026
    df = df[df["year"].between(2024, 2026)].reset_index(drop=True)
    # DOI validation (slow – show progress bar)
    doi_vals = []
    for doi in tqdm(df["doi"].fillna(""), desc="Validating DOIs"):
        doi_vals.append(validate_doi(doi))
    df["doi_valid"] = doi_vals
    # Placeholder Scopus status & quartile (UNVERIFIED)
    df["scopus_status"] = "UNVERIFIED"
    df["scopus_quartile"] = "UNVERIFIED"
    return df

# ---------------------------------------------------------------------------
# Step 3 – Relevance screening
# ---------------------------------------------------------------------------
RELEVANT_KEYWORDS = [
    "telegram bot",
    "telegram bots",
    "chatbot",
    "nlp",
    "artificial intelligence",
    "ai",
    "llm",
    "large language model",
    "network analysis",
    "social network analysis",
    "misinformation",
    "disinformation",
]

def compute_relevance(row) -> str:
    title = str(row["title"]).lower()
    abstract = str(row.get("abstract", "")).lower()
    text = f"{title} {abstract}"
    matches = sum(kw in text for kw in RELEVANT_KEYWORDS)
    # Simple rule‑based categories
    if matches >= 4:
        return "DIRECT"
    if matches == 3:
        return "RELATED"
    if matches == 2:
        return "INDIRECT"
    return "IRRELEVANT"

def relevance_screening(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["relevance_category"] = df.apply(compute_relevance, axis=1)
    # Sort by relevance then citations
    order = {"DIRECT": 0, "RELATED": 1, "INDIRECT": 2, "IRRELEVANT": 3}
    df["rel_order"] = df["relevance_category"].map(order)
    df = df.sort_values(["rel_order", "cited_by"], ascending=[True, False])
    df = df.drop(columns=["rel_order"]).reset_index(drop=True)
    return df

# ---------------------------------------------------------------------------
# Step 4 – Report generation (Markdown & Word)
# ---------------------------------------------------------------------------
def generate_markdown(df: pd.DataFrame, path: Path):
    with path.open("w", encoding="utf-8") as md:
        md.write("# Telegram Bot Literature Review (2024‑2026)\n\n")
        md.write("## Overview\n")
        md.write(f"Total records after cleaning: {len(df)}\\n\\n")
        md.write("### Relevance breakdown\n")
        for cat in ["DIRECT", "RELATED", "INDIRECT", "IRRELEVANT"]:
            cnt = (df["relevance_category"] == cat).sum()
            md.write(f"- {cat}: {cnt} papers\\n")
        md.write("\n---\n\n")
        md.write("## Top 20 Papers (by relevance & citations)\n\n")
        md.write("| Title | Year | Journal | DOI | Citations | DOI Valid | Scopus | Q1 |\n")
        md.write("|---|---|---|---|---|---|---|---|\n")
        top = df.head(20)
        for _, r in top.iterrows():
            md.write(f"| {r['title']} | {int(r['year'])} | {r['journal']} | {r['doi']} | {int(r['cited_by'])} | {r['doi_valid']} | {r['scopus_status']} | {r['scopus_quartile']} |\n")
        md.write("\n*Scopus status and quartile are marked UNVERIFIED until manually checked.*\n")

def generate_word(df: pd.DataFrame, path: Path):
    doc = Document()
    doc.add_heading('Telegram Bot Literature Review (2024‑2026)', level=0)
    doc.add_paragraph(f"Total records after cleaning: {len(df)}")
    doc.add_paragraph('Relevance breakdown:')
    for cat in ["DIRECT", "RELATED", "INDIRECT", "IRRELEVANT"]:
        cnt = (df["relevance_category"] == cat).sum()
        doc.add_paragraph(f"- {cat}: {cnt} papers")
    doc.add_paragraph('Top 20 Papers (by relevance & citations):')
    table = doc.add_table(rows=1, cols=8)
    hdr_cells = table.rows[0].cells
    headers = ['Title', 'Year', 'Journal', 'DOI', 'Citations', 'DOI Valid', 'Scopus', 'Q1']
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
    for _, r in df.head(20).iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = r['title']
        row_cells[1].text = str(int(r['year']))
        row_cells[2].text = r['journal']
        row_cells[3].text = r['doi']
        row_cells[4].text = str(int(r['cited_by']))
        row_cells[5].text = str(r['doi_valid'])
        row_cells[6].text = r['scopus_status']
        row_cells[7].text = r['scopus_quartile']
    doc.add_paragraph('*Scopus status and quartile are marked UNVERIFIED until manually checked.*')
    doc.save(path)

# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------
def main():
    # 1. Discovery
    raw_df = discovery()
    # 2. Cleaning
    cleaned_df = cleaning(raw_df)
    cleaned_df.to_csv(CLEAN_CSV, index=False)
    print(f"[pipeline] Cleaned data saved to {CLEAN_CSV.name} ({len(cleaned_df)} rows)")
    # 3. Relevance screening
    relevance_df = relevance_screening(cleaned_df)
    # 4. Reports
    generate_markdown(relevance_df, REPORT_MD)
    generate_word(relevance_df, REPORT_DOCX)
    print("[pipeline] Markdown report generated:", REPORT_MD.name)
    print("[pipeline] Word report generated:", REPORT_DOCX.name)
    # Summary output
    print("--- Summary ---")
    print(f"Cleaned records: {len(cleaned_df)}")
    for cat in ["DIRECT", "RELATED", "INDIRECT", "IRRELEVANT"]:
        count = (relevance_df['relevance_category'] == cat).sum()
        print(f"{cat}: {count}")
    print("Top 5 papers (title only):")
    for t in relevance_df['title'].head(5):
        print(f" - {t}")

if __name__ == "__main__":
    main()
