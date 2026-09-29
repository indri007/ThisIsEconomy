import requests

QUERIES = [
    "Telegram bot artificial intelligence",
    "Telegram chatbot NLP",
    "Telegram bot social network analysis",
    "Telegram bots disinformation",
    "Telegram bot large language model",
]

BASE_URL = "https://api.openalex.org/works"

results = []

for query in QUERIES:
    print(f"\nSearching: {query}")

    params = {
        "search": query,
        "filter": "from_publication_date:2024-01-01",
        "per-page": 20,
        "sort": "publication_date:desc",
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    for work in data.get("results", []):
        title = work.get("title")
        year = work.get("publication_year")
        doi = work.get("doi")
        journal = (
            work.get("primary_location", {})
            .get("source", {})
        )

        journal_name = journal.get("display_name") if journal else None

        results.append({
            "query": query,
            "year": year,
            "title": title,
            "journal": journal_name,
            "doi": doi,
            "cited_by": work.get("cited_by_count"),
            "openalex_id": work.get("id"),
        })

# hapus duplikat berdasarkan DOI/judul
unique = {}

for item in results:
    key = item["doi"] or item["title"]

    if key:
        unique[key] = item

results = list(unique.values())

results.sort(
    key=lambda x: (
        x["year"] or 0,
        x["cited_by"] or 0
    ),
    reverse=True
)

print("\n" + "=" * 80)
print("TELEGRAM BOT PAPER SEARCH")
print("=" * 80)

for i, paper in enumerate(results[:50], 1):
    print(f"\n{i}. {paper['title']}")
    print(f"   Year      : {paper['year']}")
    print(f"   Journal   : {paper['journal']}")
    print(f"   Citations : {paper['cited_by']}")
    print(f"   DOI       : {paper['doi']}")

print(f"\nTotal unique papers: {len(results)}")
