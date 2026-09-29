import requests
import pandas as pd

QUERIES = [
    '"Telegram bot" AND "social network analysis"',
    '"Telegram bot" AND "network analysis"',
    '"Telegram bots" AND disinformation',
    '"Telegram bots" AND misinformation',
    '"Telegram bot" AND NLP',
    '"Telegram bot" AND "artificial intelligence"',
    '"Telegram bot" AND chatbot',
    '"Telegram" AND bots AND "large language model"',
]

results = []

for query in QUERIES:
    print(f"Searching: {query}")

    params = {
        "search": query,
        "filter": "from_publication_date:2024-01-01",
        "per-page": 50,
        "sort": "publication_date:desc",
    }

    r = requests.get(
        "https://api.openalex.org/works",
        params=params,
        timeout=30
    )

    r.raise_for_status()

    for w in r.json().get("results", []):
        location = w.get("primary_location") or {}
        source = location.get("source") or {}

        results.append({
            "year": w.get("publication_year"),
            "title": w.get("title"),
            "journal": source.get("display_name"),
            "type": w.get("type"),
            "doi": w.get("doi"),
            "cited_by": w.get("cited_by_count"),
            "openalex": w.get("id"),
            "query": query
        })

df = pd.DataFrame(results)

# Remove duplicates
df = df.drop_duplicates(
    subset=["doi", "title"],
    keep="first"
)

# Telegram relevance scoring
def relevance(row):
    text = (
        str(row["title"]) + " " +
        str(row["journal"])
    ).lower()

    score = 0

    keywords = {
        "telegram": 5,
        "telegram bot": 8,
        "telegram bots": 8,
        "chatbot": 3,
        "social network": 4,
        "network analysis": 4,
        "disinformation": 4,
        "misinformation": 4,
        "artificial intelligence": 3,
        "nlp": 3,
        "large language": 3,
    }

    for keyword, points in keywords.items():
        if keyword in text:
            score += points

    return score


df["relevance_score"] = df.apply(relevance, axis=1)

df = df.sort_values(
    ["relevance_score", "year", "cited_by"],
    ascending=[False, False, False]
)

output = "telegram_papers_2024_2026.csv"

df.to_csv(output, index=False)

print("\n" + "=" * 80)
print("TELEGRAM BOT RESEARCH SEARCH")
print("=" * 80)

print(f"Total unique papers : {len(df)}")
print(f"Output              : {output}")

print("\nTOP 30:")

for i, (_, row) in enumerate(df.head(30).iterrows(), 1):
    print(f"\n{i}. {row['title']}")
    print(f"   Year       : {row['year']}")
    print(f"   Journal    : {row['journal']}")
    print(f"   Relevance  : {row['relevance_score']}")
    print(f"   Citations  : {row['cited_by']}")
    print(f"   DOI        : {row['doi']}")
