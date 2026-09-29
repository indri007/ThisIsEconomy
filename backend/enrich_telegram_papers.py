import pandas as pd
import requests
import re
import time

INPUT = "telegram_papers_latest.csv"
OUTPUT = "telegram_papers_enriched.csv"

print("Membaca:", INPUT)

df = pd.read_csv(INPUT)

print("Jumlah awal:", len(df))

# Pastikan kolom title tersedia
if "title" not in df.columns:
    raise ValueError("Kolom 'title' tidak ditemukan.")

def normalize_doi(doi):
    if pd.isna(doi):
        return ""
    doi = str(doi).strip()
    doi = re.sub(r"^https?://doi.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    return doi.strip()

def relevance_score(title):
    if pd.isna(title):
        return 0

    text = str(title).lower()
    score = 0

    keywords = {
        "telegram": 5,
        "telegram bot": 8,
        "telegram bots": 8,
        "bot": 2,
        "chatbot": 2,
        "social network": 4,
        "network analysis": 5,
        "disinformation": 4,
        "misinformation": 4,
        "artificial intelligence": 3,
        "natural language processing": 3,
        "nlp": 3,
        "large language model": 3,
        "llm": 3,
    }

    for keyword, weight in keywords.items():
        if keyword in text:
            score += weight

    return score

print("Menghitung relevansi...")

df["doi_normalized"] = df["doi"].apply(normalize_doi) if "doi" in df.columns else ""

df["telegram_relevance"] = df["title"].apply(relevance_score)

# Tandai DOI yang mencurigakan
def suspicious_doi(doi):
    if not doi:
        return True

    suspicious_patterns = [
        "00123",
        "00124",
        "00125",
        "00126",
        "00127",
        "00128",
        "00129",
        "00130",
        "00131",
        "00132",
        "00133",
        "00134",
        "00135",
        "00136",
        "00137",
        "00138",
        "00139",
        "00140",
        "00141",
        "00142",
        "00143",
        "00144",
        "00145",
        "00146",
        "00147",
        "00148",
        "00149",
        "00150",
        "00151",
        "00152",
        "00153",
        "00154",
    ]

    return any(x in doi for x in suspicious_patterns)

df["doi_suspicious"] = df["doi_normalized"].apply(suspicious_doi)

# Kolom hasil verifikasi
df["openalex_id"] = ""
df["openalex_title"] = ""
df["authors_openalex"] = ""
df["publication_year_openalex"] = ""
df["journal_openalex"] = ""
df["doi_openalex"] = ""
df["cited_by_openalex"] = ""
df["type_openalex"] = ""

df["scopus_status"] = "UNVERIFIED"
df["quartile"] = "UNVERIFIED"
df["telegram_role"] = "UNVERIFIED"
df["bot_type"] = "UNVERIFIED"
df["dataset_size"] = "UNVERIFIED"
df["method"] = "UNVERIFIED"
df["NLP_model"] = "UNVERIFIED"
df["network_method"] = "UNVERIFIED"
df["research_gap"] = "NEEDS_ABSTRACT_REVIEW"
df["relevance_to_your_research"] = "NEEDS_FULL_TEXT_REVIEW"

session = requests.Session()

headers = {
    "User-Agent": "TelegramPaperResearch/1.0"
}

print("\nMencari metadata OpenAlex...\n")

for i, row in df.iterrows():

    title = str(row["title"]).strip()

    if not title or title.lower() == "nan":
        continue

    print(f"[{i+1}/{len(df)}] {title[:100]}")

    try:
        url = "https://api.openalex.org/works"

        params = {
            "search": title,
            "per-page": 3
        }

        response = session.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if results:

            # Pilih hasil pertama
            work = results[0]

            df.at[i, "openalex_id"] = work.get("id", "")
            df.at[i, "openalex_title"] = work.get("display_name", "")

            authors = work.get("authorships", [])

            author_names = []

            for author in authors:
                name = author.get("author", {}).get("display_name")

                if name:
                    author_names.append(name)

            df.at[i, "authors_openalex"] = "; ".join(author_names)

            df.at[i, "publication_year_openalex"] = work.get(
                "publication_year", ""
            )

            primary_location = work.get("primary_location") or {}

            source = primary_location.get("source") or {}

            df.at[i, "journal_openalex"] = source.get(
                "display_name", ""
            )

            doi = work.get("doi") or ""

            doi = normalize_doi(doi)

            df.at[i, "doi_openalex"] = doi

            df.at[i, "cited_by_openalex"] = work.get(
                "cited_by_count", 0
            )

            df.at[i, "type_openalex"] = work.get(
                "type", ""
            )

        time.sleep(0.15)

    except Exception as e:

        print("  ERROR:", e)

print("\nMenghapus judul duplikat...")

df = df.drop_duplicates(
    subset=["title"],
    keep="first"
)

print("Jumlah setelah deduplikasi:", len(df))

print("\nMengurutkan berdasarkan relevansi...")

df = df.sort_values(
    by=[
        "telegram_relevance",
        "publication_year_openalex",
        "cited_by_openalex"
    ],
    ascending=[
        False,
        False,
        False
    ]
)

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\n======================================")
print("SELESAI")
print("======================================")
print("Output:", OUTPUT)
print("Total papers:", len(df))
print("======================================")
