import os
import re
import time
import requests
import pandas as pd
from pathlib import Path
from urllib.parse import quote

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "telegram_literature_output"

INPUT_FILE = BASE_DIR / "telegram_papers_latest.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "TelegramLiteratureResearch/1.0"
}

QUERIES = [
    '"Telegram bot"',
    '"Telegram bots"',
    '"Telegram bot" artificial intelligence',
    '"Telegram bot" chatbot',
    '"Telegram bot" NLP',
    '"Telegram bot" "network analysis"',
    '"Telegram bot" disinformation',
    '"Telegram bot" misinformation',
    '"Telegram bot" "large language model"',
    '"Telegram" bots "social network"'
]

START_YEAR = 2024
END_YEAR = 2026


# ============================================================
# HELPERS
# ============================================================

def normalize_title(title):
    if pd.isna(title):
        return ""

    title = str(title).lower().strip()
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"[^\w\s]", "", title)

    return title


def normalize_doi(doi):
    if pd.isna(doi):
        return ""

    doi = str(doi).strip()

    doi = re.sub(
        r"^https?://(dx\.)?doi\.org/",
        "",
        doi,
        flags=re.I
    )

    doi = re.sub(
        r"^doi:\s*",
        "",
        doi,
        flags=re.I
    )

    return doi.strip()


def classify_relevance(title):

    text = str(title).lower()

    direct_terms = [
        "telegram bot",
        "telegram bots",
        "telegram chatbot",
        "telegram chat bot"
    ]

    related_terms = [
        "telegram",
        "chatbot",
        "social network",
        "network analysis",
        "disinformation",
        "misinformation",
        "natural language processing",
        "nlp",
        "large language model",
        "llm",
        "artificial intelligence"
    ]

    if any(term in text for term in direct_terms):
        return "DIRECT"

    if any(term in text for term in related_terms):
        return "RELATED"

    return "INDIRECT"


def relevance_score(title):

    text = str(title).lower()

    weights = {
        "telegram bot": 10,
        "telegram bots": 10,
        "telegram chatbot": 10,
        "chatbot": 4,
        "telegram": 5,
        "network analysis": 6,
        "social network": 5,
        "disinformation": 5,
        "misinformation": 5,
        "artificial intelligence": 4,
        "natural language processing": 4,
        "nlp": 4,
        "large language model": 4,
        "llm": 4
    }

    score = 0

    for keyword, weight in weights.items():

        if keyword in text:
            score += weight

    return score


def validate_doi_format(doi):

    if not doi:
        return "MISSING"

    pattern = r"^10\.\d{4,9}/\S+$"

    if re.match(pattern, doi):
        return "FORMAT_VALID"

    return "INVALID"


def classify_document_type(doc_type):

    if not doc_type:
        return "UNVERIFIED"

    doc_type = str(doc_type).lower()

    if doc_type in ["article", "journal-article"]:
        return "JOURNAL"

    if "book" in doc_type:
        return "BOOK"

    if "chapter" in doc_type:
        return "CHAPTER"

    if "proceedings" in doc_type or "conference" in doc_type:
        return "CONFERENCE"

    return doc_type.upper()


# ============================================================
# STEP 1 — DISCOVERY
# ============================================================

def discover_papers():

    print("\n" + "=" * 70)
    print("STEP 1 — OPENALEX DISCOVERY")
    print("=" * 70)

    rows = []
    seen_titles = set()
    seen_dois = set()

    for query in QUERIES:

        print(f"\nQuery: {query}")

        params = {
            "search": query,
            "filter": (
                f"from_publication_date:"
                f"{START_YEAR}-01-01,"
                f"to_publication_date:"
                f"{END_YEAR}-12-31"
            ),
            "per-page": 100
        }

        try:

            response = requests.get(
                "https://api.openalex.org/works",
                params=params,
                headers=HEADERS,
                timeout=30
            )

            response.raise_for_status()

            results = response.json().get("results", [])

            print("Results:", len(results))

            for work in results:

                title = work.get("display_name") or ""

                if not title:
                    continue

                title_key = normalize_title(title)

                doi = normalize_doi(work.get("doi") or "")

                if title_key in seen_titles:
                    continue

                if doi and doi in seen_dois:
                    continue

                seen_titles.add(title_key)

                if doi:
                    seen_dois.add(doi)

                authors = []

                for author in work.get("authorships", []):

                    name = author.get(
                        "author",
                        {}
                    ).get("display_name")

                    if name:
                        authors.append(name)

                primary_location = (
                    work.get("primary_location") or {}
                )

                source = (
                    primary_location.get("source") or {}
                )

                rows.append({

                    "title": title,

                    "authors":
                        "; ".join(authors),

                    "year":
                        work.get("publication_year"),

                    "journal":
                        source.get(
                            "display_name",
                            ""
                        ),

                    "publisher":
                        source.get(
                            "host_organization_name",
                            ""
                        ),

                    "doi":
                        doi,

                    "openalex_id":
                        work.get("id", ""),

                    "cited_by":
                        work.get(
                            "cited_by_count",
                            0
                        ),

                    "type":
                        work.get("type", ""),

                    "abstract":
                        "",

                    "scopus_status":
                        "UNVERIFIED",

                    "quartile":
                        "UNVERIFIED"
                })

            time.sleep(0.5)

        except Exception as error:

            print(
                "ERROR:",
                error
            )

    df = pd.DataFrame(rows)

    output = (
        OUTPUT_DIR /
        "01_discovery.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\nDiscovered:",
        len(df)
    )

    print(
        "Saved:",
        output
    )

    return df


# ============================================================
# STEP 2 — RELEVANCE
# ============================================================

def relevance_analysis(df):

    print("\n" + "=" * 70)
    print("STEP 2 — RELEVANCE ANALYSIS")
    print("=" * 70)

    df = df.copy()

    df["title_normalized"] = (
        df["title"].apply(
            normalize_title
        )
    )

    df["telegram_role"] = (
        df["title"].apply(
            classify_relevance
        )
    )

    df["telegram_relevance_score"] = (
        df["title"].apply(
            relevance_score
        )
    )

    df["relevance_to_thesis"] = (
        df["telegram_role"].map({

            "DIRECT":
                "HIGHLY_RELEVANT",

            "RELATED":
                "RELEVANT",

            "INDIRECT":
                "BACKGROUND_ONLY"

        }).fillna(
            "UNVERIFIED"
        )
    )

    output = (
        OUTPUT_DIR /
        "02_relevance_matrix.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        df["telegram_role"]
        .value_counts()
    )

    return df


# ============================================================
# STEP 3 — DOI VALIDATION
# ============================================================

def doi_validation(df):

    print("\n" + "=" * 70)
    print("STEP 3 — DOI VALIDATION")
    print("=" * 70)

    df = df.copy()

    df["doi"] = (
        df["doi"].apply(
            normalize_doi
        )
    )

    df["doi_status"] = (
        df["doi"].apply(
            validate_doi_format
        )
    )

    output = (
        OUTPUT_DIR /
        "03_doi_validation.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        df["doi_status"]
        .value_counts()
    )

    return df


# ============================================================
# STEP 4 — JOURNAL VALIDATION
# ============================================================

def journal_validation(df):

    print("\n" + "=" * 70)
    print("STEP 4 — JOURNAL VALIDATION")
    print("=" * 70)

    df = df.copy()

    df["document_category"] = (
        df["type"].apply(
            classify_document_type
        )
    )

    df["journal_status"] = (
        df["journal"]
        .apply(
            lambda x:
            "IDENTIFIED"
            if str(x).strip()
            else "UNVERIFIED"
        )
    )

    output = (
        OUTPUT_DIR /
        "04_journal_validation.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    return df


# ============================================================
# STEP 5 — SCOPUS STATUS
# ============================================================

def scopus_verification(df):

    print("\n" + "=" * 70)
    print("STEP 5 — SCOPUS VERIFICATION")
    print("=" * 70)

    df = df.copy()

    # IMPORTANT:
    # OpenAlex alone does NOT establish Scopus/Q1 status.

    df["scopus_status"] = "UNVERIFIED"

    df["scopus_source"] = "REQUIRES_SCOPUS_VERIFICATION"

    df["quartile"] = "UNVERIFIED"

    df["quartile_year"] = ""

    df["subject_area"] = "UNVERIFIED"

    output = (
        OUTPUT_DIR /
        "05_scopus_verification.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "Scopus status intentionally left UNVERIFIED."
    )

    return df


# ============================================================
# STEP 6 — Q1 CANDIDATES
# ============================================================

def q1_candidates(df):

    print("\n" + "=" * 70)
    print("STEP 6 — Q1 CANDIDATES")
    print("=" * 70)

    df = df.copy()

    def classify_q1(row):

        if (
            row["telegram_role"]
            in ["DIRECT", "RELATED"]
            and row["scopus_status"]
            == "VERIFIED"
            and row["quartile"]
            == "Q1"
        ):
            return "Q1_VERIFIED"

        if (
            row["telegram_role"]
            in ["DIRECT", "RELATED"]
            and row["scopus_status"]
            == "UNVERIFIED"
        ):
            return "SCOPUS_UNVERIFIED"

        return "OTHER"

    df["q1_candidate_status"] = (
        df.apply(
            classify_q1,
            axis=1
        )
    )

    output = (
        OUTPUT_DIR /
        "06_q1_candidates.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    return df


# ============================================================
# STEP 7 — METHODOLOGY MATRIX
# ============================================================

def methodology_matrix(df):

    print("\n" + "=" * 70)
    print("STEP 7 — METHODOLOGY MATRIX")
    print("=" * 70)

    df = df.copy()

    methodology_columns = {

        "research_object":
            "UNVERIFIED",

        "platform":
            "Telegram",

        "bot_type":
            "UNVERIFIED",

        "dataset":
            "UNVERIFIED",

        "dataset_size":
            "UNVERIFIED",

        "sampling":
            "UNVERIFIED",

        "data_collection":
            "UNVERIFIED",

        "API":
            "UNVERIFIED",

        "software":
            "UNVERIFIED",

        "method":
            "UNVERIFIED",

        "NLP_model":
            "UNVERIFIED",

        "LLM":
            "UNVERIFIED",

        "classification_method":
            "UNVERIFIED",

        "network_method":
            "UNVERIFIED",

        "SNA_method":
            "UNVERIFIED",

        "community_detection":
            "UNVERIFIED",

        "sentiment_analysis":
            "UNVERIFIED",

        "emotion_analysis":
            "UNVERIFIED",

        "sarcasm_detection":
            "UNVERIFIED",

        "topic_modeling":
            "UNVERIFIED",

        "evaluation_metric":
            "UNVERIFIED"
    }

    for column, default in methodology_columns.items():

        if column not in df.columns:
            df[column] = default

    output = (
        OUTPUT_DIR /
        "07_methodology_matrix.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    return df


# ============================================================
# STEP 8 — RESEARCH GAP
# ============================================================

def research_gap(df):

    print("\n" + "=" * 70)
    print("STEP 8 — RESEARCH GAP")
    print("=" * 70)

    df = df.copy()

    df["existing_contribution"] = (
        "REQUIRES_ABSTRACT_REVIEW"
    )

    df["limitation"] = (
        "REQUIRES_FULL_TEXT_REVIEW"
    )

    df["missing_dimension"] = (
        "REQUIRES_FULL_TEXT_REVIEW"
    )

    df["potential_gap"] = (
        "REQUIRES_SYNTHESIS"
    )

    df["relevance_to_thesis"] = (
        df["telegram_role"].map({

            "DIRECT":
                "HIGHLY_RELEVANT",

            "RELATED":
                "RELEVANT",

            "INDIRECT":
                "BACKGROUND_ONLY"

        }).fillna(
            "UNVERIFIED"
        )
    )

    output = (
        OUTPUT_DIR /
        "08_research_gap_matrix.csv"
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    return df


# ============================================================
# STEP 9 — METHOD BENCHMARK
# ============================================================

def method_benchmark(df):

    print("\n" + "=" * 70)
    print("STEP 9 — METHOD BENCHMARK")
    print("=" * 70)

    columns = [

        "title",
        "year",
        "journal",
        "telegram_role",
        "dataset_size",
        "method",
        "NLP_model",
        "network_method",
        "emotion_analysis",
        "sarcasm_detection",
        "community_detection",
        "relevance_to_thesis"

    ]

    available = [
        col
        for col in columns
        if col in df.columns
    ]

    benchmark = df[
        available
    ].copy()

    output = (
        OUTPUT_DIR /
        "09_method_benchmark.csv"
    )

    benchmark.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    return benchmark


# ============================================================
# STEP 10 — MASTER LITERATURE REVIEW
# ============================================================

def final_report(df):

    print("\n" + "=" * 70)
    print("STEP 10 — FINAL LITERATURE PACKAGE")
    print("=" * 70)

    master_file = (
        OUTPUT_DIR /
        "telegram_literature_master.csv"
    )

    df.to_csv(
        master_file,
        index=False,
        encoding="utf-8-sig"
    )

    direct = (
        (df["telegram_role"] == "DIRECT")
        .sum()
    )

    related = (
        (df["telegram_role"] == "RELATED")
        .sum()
    )

    scopus_verified = (
        (df["scopus_status"] == "VERIFIED")
        .sum()
    )

    q1_verified = (
        (
            (df["scopus_status"] == "VERIFIED")
            &
            (df["quartile"] == "Q1")
        )
        .sum()
    )

    report = []

    report.append(
        "# Telegram Bot Literature Review 2024–2026\n"
    )

    report.append(
        "## 1. Search Strategy\n"
    )

    report.append(
        "Literature discovery menggunakan OpenAlex "
        "dengan keyword Telegram Bot, Telegram Bots, "
        "chatbot, NLP, AI, LLM, network analysis, "
        "misinformation dan disinformation.\n"
    )

    report.append(
        "## 2. Dataset Discovery\n"
    )

    report.append(
        f"- Total discovered: {len(df)}\n"
        f"- DIRECT: {direct}\n"
        f"- RELATED: {related}\n"
    )

    report.append(
        "## 3. Scopus Verification\n"
    )

    report.append(
        f"- Scopus verified: {scopus_verified}\n"
        f"- Q1 verified: {q1_verified}\n"
        "- Status yang belum diverifikasi tetap "
        "ditandai UNVERIFIED.\n"
    )

    report.append(
        "## 4. Research Gap\n"
    )

    report.append(
        "Analisis research gap membutuhkan "
        "review abstrak/full text. Metadata yang "
        "tidak tersedia tidak diisi dengan asumsi.\n"
    )

    report.append(
        "## 5. Relevance to Thesis\n"
    )

    report.append(
        "Relevansi dibandingkan secara deskriptif "
        "dengan Social Network Analysis, sarcasm, "
        "emotion analysis, IndoBERT, emoji, Twitter/X, "
        "MBG dan Marketing 6.0.\n"
    )

    report_file = (
        OUTPUT_DIR /
        "TELEGRAM_BOT_LITERATURE_REVIEW.md"
    )

    report_file.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    summary = f"""
========================================
FINAL TELEGRAM BOT LITERATURE AUDIT
========================================

Discovered:
{len(df)}

Direct:
{direct}

Related:
{related}

Scopus Verified:
{scopus_verified}

Q1 Verified:
{q1_verified}

Unverified:
{len(df) - scopus_verified}

Output:
{OUTPUT_DIR}

========================================
PIPELINE COMPLETED
========================================
"""

    summary_file = (
        OUTPUT_DIR /
        "telegram_literature_summary.txt"
    )

    summary_file.write_text(
        summary,
        encoding="utf-8"
    )

    print(summary)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("TELEGRAM BOT LITERATURE PIPELINE")
    print("2024–2026")
    print("=" * 70)

    # If discovery CSV already exists, use it.
    # Otherwise perform discovery.

    if INPUT_FILE.exists():

        print(
            "\nExisting discovery CSV found:"
        )

        print(INPUT_FILE)

        df = pd.read_csv(
            INPUT_FILE
        )

    else:

        df = discover_papers()

    if df.empty:

        print(
            "\nERROR: Tidak ada paper ditemukan."
        )

        return

    df = relevance_analysis(df)

    df = doi_validation(df)

    df = journal_validation(df)

    df = scopus_verification(df)

    df = q1_candidates(df)

    df = methodology_matrix(df)

    df = research_gap(df)

    method_benchmark(df)

    final_report(df)

    print(
        "\nSemua output berada di:"
    )

    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
