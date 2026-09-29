import requests
import pandas as pd
import time

OUTPUT = "telegram_papers_latest.csv"

QUERIES = [
    "\"Telegram bot\"",
    "\"Telegram bots\"",
    "\"Telegram bot\" artificial intelligence",
    "\"Telegram bot\" chatbot",
    "\"Telegram bot\" NLP",
    "\"Telegram bot\" \"network analysis\"",
    "\"Telegram bot\" disinformation",
    "\"Telegram bot\" misinformation",
    "\"Telegram bot\" \"large language model\"",
    "\"Telegram\" bots social network"
]

HEADERS = {
    "User-Agent": "TelegramResearchBot/1.0"
}

rows = []
seen = set()

print("=" * 60)
print("SEARCH TELEGRAM BOT PAPERS")
print("=" * 60)

for query in QUERIES:
    print(f"\nQuery: {query}")
    params = {
        "search": query,
        "filter": "from_publication_date:2024-01-01,to_publication_date:2026-12-31",
        "per-page": 50
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
        print("Ditemukan:", len(results))
        for work in results:
            title = work.get("display_name") or ""
            if not title:
                continue
            title_key = title.lower().strip()
            if title_key in seen:
                continue
            seen.add(title_key)
            authors = []
            for a in work.get("authorships", []):
                author = a.get("author", {}).get("display_name")
                if author:
                    authors.append(author)
            location = work.get("primary_location") or {}
            source = location.get("source") or {}
            doi = work.get("doi") or ""
            rows.append({
                "title": title,
                "authors": "; ".join(authors),
                "year": work.get("publication_year"),
                "journal": source.get("display_name", ""),
                "doi": doi,
                "openalex_id": work.get("id", ""),
                "cited_by": work.get("cited_by_count", 0),
                "type": work.get("type", ""),
                "scopus_status": "UNVERIFIED",
                "quartile": "UNVERIFIED"
            })
        time.sleep(0.5)
    except Exception as e:
        print("ERROR:", e)

df = pd.DataFrame(rows)
if df.empty:
    print("\nTidak ada paper ditemukan.")
    raise SystemExit
# Prioritize newest year then citations
df = df.sort_values(by=["year", "cited_by"], ascending=[False, False])

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print("\n" + "=" * 60)
print("SELESAI")
print("=" * 60)
print("Total unique papers:", len(df))
print("File:", OUTPUT)

print("\nTOP 20:")
print(df[["title", "year", "journal", "doi", "cited_by"]].head(20).to_string(index=False))
