"""Build and populate the academic database for all published journals and the 30-paper systematic review corpus.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# Paths
ROOT_DIR = Path("/Users/jevin/Documents/tesis_mbg")
DB_DIR = ROOT_DIR / "data" / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_PATH = DB_DIR / "published_journals.db"

DOCX_F1 = Path(
    "/Users/jevin/Downloads/inggris_Public+Sentiment+toward+Indonesia’s+Free+Nutritious+Meal+Program+on+X+A+Systematic+Review+(1).docx"
)
DOCX_F2 = Path("/Users/jevin/Downloads/Jurnal_Indri+Anjar.docx")

# 1. Author's Published Works and Preprints
AUTHOR_PUBLICATIONS = [
    {
        "pub_id": "PUB-001",
        "title": "Public Sentiment toward Indonesia's Free Nutritious Meal Program on X: A Systematic Review",
        "authors": ["Indri Anjar Kartika Sari", "Catur Suratnoaji", "Agus Widiyarta"],
        "year": 2026,
        "journal_name": "International Journal of Contemporary Sciences (IJCS)",
        "volume": "1",
        "issue": "9",
        "pages": "2332-2352",
        "doi": "10.55927/fcdcvw62",
        "issn": "3047-4078",
        "publication_status": "PUBLISHED",
        "category": "Systematic Literature Review (PRISMA 2020)",
        "publisher": "Formosa Publisher",
        "url": "https://journal.formosapublisher.org/index.php/ijcs",
        "abstract": "This study systematically reviews research on public sentiment toward Indonesia's Free Nutritious Meal (MBG) program expressed on X/Twitter. Using the PRISMA 2020 framework, literature published between 2024 and 2026 was identified through Google Scholar and GARUDA, resulting in 30 empirical studies included in the final review.",
        "keywords": "public sentiment; free nutritious meal; social media X; digital communication; systematic literature review",
        "citation_apa": "Sari, I. A. K., Suratnoaji, C., & Widiyarta, A. (2026). Public Sentiment toward Indonesia's Free Nutritious Meal Program on X: A Systematic Review. International Journal of Contemporary Sciences (IJCS), 1(9), 2332–2352. https://doi.org/10.55927/fcdcvw62",
    },
    {
        "pub_id": "PUB-002",
        "title": "Reading Emotions Behind TikTok Text: Fine-Tuning IndoBERT for Nine-Class Emotion Classification in the Indonesian Language",
        "authors": ["Indri Anjar Kartika Sari", "Catur Suratnoaji", "Agus Widiyarta"],
        "year": 2026,
        "journal_name": "INOVASI: Jurnal Inovasi Pendidikan",
        "volume": "12",
        "issue": "3",
        "pages": "1-12",
        "doi": "10.55927/inovasi.v12i3.88",
        "issn": "2442-5923",
        "publication_status": "ACCEPTED_IN_PRESS",
        "category": "Computational Linguistics & NLP",
        "publisher": "Nus Publications",
        "url": "https://journal.nuspublications.or.id/innovasi",
        "abstract": "A computational analysis fine-tuning IndoBERT on 9 discrete emotion categories based on Robert Plutchik's psychosemiotic taxonomy for Indonesian short-text communication on TikTok.",
        "keywords": "IndoBERT; emotion classification; TikTok; NLP; Plutchik emotion taxonomy",
        "citation_apa": "Sari, I. A. K., Suratnoaji, C., & Widiyarta, A. (2026). Reading emotions behind TikTok text: Fine-tuning IndoBERT for nine-class emotion classification in the Indonesian language. INOVASI: Jurnal Inovasi Pendidikan, 12(3), 1–12. Ref No: 88 / Nus-INN/LOA/V.12/N.3/12-2026.",
    },
    {
        "pub_id": "PUB-003",
        "title": "Sentiment Analysis of the Free Nutritious Meal or Makan Bergizi Gratis (MBG) Program on Social Media X from the Perspective of the Political Economy of Development",
        "authors": ["Indri Anjar Kartika Sari"],
        "year": 2026,
        "journal_name": "Public Sector & Society Journal (PSSJ / IPSSJ)",
        "volume": "6",
        "issue": "6",
        "pages": "101-115",
        "doi": "10.55942/pssj.v6i6.2023",
        "issn": "3064-4011",
        "publication_status": "PUBLISHED",
        "category": "Political Economy & Social Media Analytics",
        "publisher": "IPSSJ Publishing",
        "url": "https://doi.org/10.55942/pssj.v6i6.2023",
        "abstract": "Investigates public perceptions of the Makan Bergizi Gratis (MBG) program through VADER sentiment analysis and qualitative economic development framing on platform X.",
        "keywords": "makan bergizi gratis; political economy; public sentiment; platform X; development communication",
        "citation_apa": "Sari, I. A. K. (2026). Sentiment Analysis of the Free Nutritious Meal or Makan Bergizi Gratis (MBG) Program on Social Media X from the Perspective of the Political Economy of Development. Public Sector & Society Journal (PSSJ), 6(6), 101–115. https://doi.org/10.55942/pssj.v6i6.2023",
    },
    {
        "pub_id": "PUB-004",
        "title": "Analisis Jaringan Sosial dalam Isu Percakapan MBG di Media Sosial X",
        "authors": ["Indri Anjar Kartika Sari", "Catur Suratnoaji", "Agus Widiyarta"],
        "year": 2026,
        "journal_name": "Integrative Perspectives of Social and Science Journal (IPSSJ)",
        "volume": "3",
        "issue": "9",
        "pages": "248-257",
        "doi": "10.55942/ipssj.v3i9.2009",
        "issn": "3064-4011",
        "publication_status": "PUBLISHED",
        "category": "Communication Network Analysis (SNA)",
        "publisher": "IPSSJ Publishing",
        "url": "https://ipssj.com/index.php/ojs/article/view/2009",
        "abstract": "Penerapan Social Network Analysis (SNA) untuk memetakan aktor sentral, struktur penyebaran informasi, dan polarisasi opini publik terkait program Makan Bergizi Gratis (MBG) di media sosial X.",
        "keywords": "social network analysis; CNA; makan bergizi gratis; platform X; polarisasi opini",
        "citation_apa": "Sari, I. A. K., Suratnoaji, C., & Widiyarta, A. (2026). Analisis Jaringan Sosial dalam Isu Percakapan MBG di Media Sosial X. Integrative Perspectives of Social and Science Journal (IPSSJ), 3(9), 248–257. LoA Ref No: 2009/IPSSJ/I/2026.",
    },
    {
        "pub_id": "PUB-005",
        "title": "JobsMatchAI: Platform Generative AI End-to-End untuk Pencocokan Kerja Semantik dan Dukungan Karier di Pasar Tenaga Kerja Indonesia",
        "authors": ["Indri Anjar Kartika Sari"],
        "year": 2026,
        "journal_name": "Integrative Perspectives of Social and Science Journal (IPSSJ)",
        "volume": "3",
        "issue": "9",
        "pages": "333-340",
        "doi": "10.55942/ipssj.v3i9.2024",
        "issn": "3064-4011",
        "publication_status": "PUBLISHED",
        "category": "Generative AI & Semantic Matching",
        "publisher": "IPSSJ Publishing",
        "url": "https://ipssj.com/index.php/ojs/article/view/2024",
        "abstract": "Arsitektur platform Generative AI untuk pencocokan semantik CV pelamar dengan deskripsi pekerjaan menggunakan embeddings transformer dan ontologi karier terstruktur.",
        "keywords": "JobsMatchAI; generative AI; semantic matching; ATS scoring; labour market",
        "citation_apa": "Sari, I. A. K. (2026). JobsMatchAI: Platform Generative AI End-to-End untuk Pencocokan Kerja Semantik dan Dukungan Karier di Pasar Tenaga Kerja Indonesia. Integrative Perspectives of Social and Science Journal (IPSSJ), 3(9), 333–340. https://ipssj.com/index.php/ojs/article/view/2024",
    },
    {
        "pub_id": "PUB-006",
        "title": "Keamanan dan Privasi Sistem Absensi Siswa Berbasis Biometrik dan Geolokasi: Tinjauan Sistematis Prisma 2020 dan Studi Kasus Audit Sistem Open-Source",
        "authors": [
            "Indri Anjar Kartika Sari",
            "Onno W. Purbo",
            "Eldiana Tri Narulita",
            "Ni Ketut Pande Sarjani",
            "Ni Ketut Rini Astuti",
        ],
        "year": 2026,
        "journal_name": "Integrative Perspectives of Social and Science Journal (IPSSJ)",
        "volume": "3",
        "issue": "9",
        "pages": "768-775",
        "doi": "10.55942/ipssj.v3i9.2060",
        "issn": "3064-4011",
        "publication_status": "PUBLISHED",
        "category": "Cybersecurity & Educational Technology",
        "publisher": "IPSSJ Publishing",
        "url": "https://ipssj.com/index.php/ojs/article/view/2060",
        "abstract": "Audit keamanan siber dan perlindungan privasi data pribadi siswa pada sistem absensi geolokasi dan biometrik di lingkungan pendidikan menengah.",
        "keywords": "cybersecurity; biometrik; absensi sekolah; geolokasi; PRISMA 2020",
        "citation_apa": "Sari, I. A. K., Purbo, O. W., Narulita, E. T., Sarjani, N. K. P., & Astuti, N. K. R. (2026). Keamanan dan Privasi Sistem Absensi Siswa Berbasis Biometrik dan Geolokasi: Tinjauan Sistematis Prisma 2020 dan Studi Kasus Audit Sistem Open-Source. Integrative Perspectives of Social and Science Journal (IPSSJ), 3(9), 768–775.",
    },
    {
        "pub_id": "PUB-007",
        "title": "Silent Authority dan Paradigma Branding Iceberg: Analisis Strategi Komunikasi Digital NVIDIA di Platform TikTok dalam Era Marketing 5.0",
        "authors": ["Indri Anjar Kartika Sari", "Agung Budi Prasetio", "Waspodo Tjipto Subroto"],
        "year": 2026,
        "journal_name": "Integrative Perspectives of Social and Science Journal (IPSSJ)",
        "volume": "3",
        "issue": "9",
        "pages": "788-799",
        "doi": "10.55942/ipssj.v3i9.2074",
        "issn": "3064-4011",
        "publication_status": "PUBLISHED",
        "category": "Digital Branding & Marketing 5.0",
        "publisher": "IPSSJ Publishing",
        "url": "https://ipssj.com/index.php/ojs/article/view/2074",
        "abstract": "Mengkaji fenomena komunikasi visual korporat dan strategi branding tacit knowledge NVIDIA di media sosial berdurasi pendek TikTok.",
        "keywords": "silent authority; iceberg branding; NVIDIA; TikTok; marketing 5.0",
        "citation_apa": "Sari, I. A. K., Prasetio, A. B., & Subroto, W. T. (2026). Silent Authority dan Paradigma Branding Iceberg: Analisis Strategi Komunikasi Digital NVIDIA di Platform TikTok dalam Era Marketing 5.0. Integrative Perspectives of Social and Science Journal (IPSSJ), 3(9), 788–799.",
    },
    {
        "pub_id": "PUB-008",
        "title": "Relevance-Gated Early Warning with Telegram Alerts for Free Nutritious Meal Discourse on X",
        "authors": ["Indri Anjar Kartika Sari", "Catur Suratnoaji", "Agus Widiyarta"],
        "year": 2026,
        "journal_name": "SSRN Electronic Journal (Elsevier)",
        "volume": "Preprint",
        "issue": "7526942",
        "pages": "1-32",
        "doi": "10.2139/ssrn.7526942",
        "issn": "1556-5068",
        "publication_status": "PREPRINT_RELEASED",
        "category": "Crisis Communication & Early Warning System",
        "publisher": "Social Science Research Network (SSRN)",
        "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7526942",
        "abstract": "Develops a zero-shot relevance-gating and threshold alerting system that streams public discourse on X, classifies negative surge and food poisoning keywords, and pushes structured Telegram alerts.",
        "keywords": "early warning system; telegram alerts; crisis communication; makan bergizi gratis; platform X",
        "citation_apa": "Sari, I. A. K., Suratnoaji, C., & Widiyarta, A. (2026). Relevance-Gated Early Warning with Telegram Alerts for Free Nutritious Meal Discourse on X. SSRN Electronic Journal, Abstract ID 7526942. https://doi.org/10.2139/ssrn.7526942",
    },
    {
        "pub_id": "PUB-009",
        "title": "Analysis of the Trillion-Rupiah Communication Network Surrounding the Free Nutritious Meal Program on X (Social Media)",
        "authors": ["Indri Anjar Kartika Sari", "Catur Suratnoaji", "Agus Widiyarta"],
        "year": 2026,
        "journal_name": "Mediator: Jurnal Komunikasi",
        "volume": "17",
        "issue": "2",
        "pages": "1-22",
        "doi": "10.29313/mediator.v17i2.14820",
        "issn": "1411-5883",
        "publication_status": "UNDER_REVIEW",
        "category": "Communication Science (SINTA 2)",
        "publisher": "Fakultas Ilmu Komunikasi Unisba",
        "url": "https://ejournal.unisba.ac.id/index.php/mediator",
        "abstract": "Investigates the tri-layer computational architecture of political economy and public discussion on Indonesia's MBG program, linking budgetary scale to modular community structures and emotion trajectories.",
        "keywords": "communication network analysis; Louvain modularity; political economy; mediator; platform X",
        "citation_apa": "Sari, I. A. K., Suratnoaji, C., & Widiyarta, A. (2026). Analysis of the Trillion-Rupiah Communication Network Surrounding the Free Nutritious Meal Program on X (Social Media). Mediator: Jurnal Komunikasi, 17(2), 1–22.",
    },
]


def extract_30_studies_from_docx() -> list[dict]:
    """Extract and parse all 30 empirical studies from the docx file."""
    doc_path = DOCX_F2 if DOCX_F2.exists() else DOCX_F1
    if not doc_path.exists():
        raise FileNotFoundError(f"Neither {DOCX_F1} nor {DOCX_F2} found.")

    with zipfile.ZipFile(doc_path) as z:
        tree = ET.fromstring(z.read("word/document.xml"))

    # Find the table with 31 rows
    target_tbl = None
    for tbl in tree.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl"):
        tr_list = tbl.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr")
        if len(tr_list) >= 30:
            target_tbl = tbl
            break

    if target_tbl is None:
        raise ValueError("Could not find 30-row table in document.")

    rows = []
    for tr in target_tbl.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr"):
        cells = [
            "".join(
                [
                    t.text
                    for t in tc.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
                    if t.text
                ]
            ).strip()
            for tc in tr.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")
        ]
        rows.append(cells)

    header = rows[0]
    # Header format: ['No.', 'Authors (Year)', 'Article Title', 'Main Method', 'DOI']

    # Extract references to cross-enrich journal names
    pars = []
    for p in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        t = "".join([node.text for node in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text])
        if t.strip():
            pars.append(t.strip())

    bib_map = {}
    for p in pars:
        match_doi = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", p)
        if match_doi:
            bib_map[match_doi.group(0).lower().rstrip(".")] = p

    studies = []
    for r in rows[1:]:
        if len(r) < 5:
            continue
        idx_str, author_year, title, method, doi = r[0], r[1], r[2], r[3], r[4]

        # Extract year
        m_year = re.search(r"\((202\d)\)", author_year)
        year = int(m_year.group(1)) if m_year else 2025

        # Clean DOI
        doi_clean = doi.strip()
        if doi_clean.startswith("http"):
            doi_clean = doi_clean.split("doi.org/")[-1]

        # Check bib reference for journal details
        bib_text = bib_map.get(doi_clean.lower().rstrip("."), "")
        journal_name = "Indonesian Journal of Computer Science / Information Systems"
        if "jitet" in doi_clean.lower():
            journal_name = "Jurnal Informatika Dan Teknik Elektro Terapan (JITET)"
        elif "journalisi" in doi_clean.lower():
            journal_name = "Journal of Information System and Informatics (Journal ISI)"
        elif "bits" in doi_clean.lower():
            journal_name = "Building of Informatics, Technology and Science (BITS)"
        elif "sitech" in doi_clean.lower():
            journal_name = "Jurnal SITECH: Sistem Informasi dan Teknologi"
        elif "piksel" in doi_clean.lower():
            journal_name = "PIKSEL : Penelitian Ilmu Komputer Sistem Embedded & Logic"
        elif "jati" in doi_clean.lower():
            journal_name = "Jurnal Mahasiswa Teknik Informatika (JATI)"
        elif "jmt" in doi_clean.lower() or "thales" in bib_text.lower():
            journal_name = "Jurnal Matematika Thales (JMT)"
        elif "pssj" in doi_clean.lower():
            journal_name = "Public Sector & Society Journal (PSSJ / IPSSJ)"
        elif "zero" in doi_clean.lower():
            journal_name = "ZERO: Jurnal Sains, Matematika dan Terapan"
        elif "jtip" in doi_clean.lower():
            journal_name = "Jurnal Teknologi Informasi dan Pendidikan (JTIP)"
        elif "siskom-kb" in doi_clean.lower():
            journal_name = "Jurnal Sistem Komputer dan Kecerdasan Buatan (SISKOM-KB)"
        elif "bulletinds" in doi_clean.lower():
            journal_name = "Bulletin of Data Science"
        elif "cauchy" in doi_clean.lower():
            journal_name = "CAUCHY: Jurnal Matematika Murni dan Aplikasi"
        elif "jurikom" in doi_clean.lower():
            journal_name = "JURIKOM (Jurnal Riset Komputer)"
        elif "joresd" in doi_clean.lower():
            journal_name = "Journal of Research in Science and Data Science (JORESD)"
        elif "riggs" in doi_clean.lower():
            journal_name = "RIGGS: Journal of Computer Science and Informatics"
        elif "jf" in doi_clean.lower():
            journal_name = "Jurnal Fasilkom"
        elif "joti" in doi_clean.lower():
            journal_name = "Jurnal Open Technology Information (JOTI)"
        elif "te" in doi_clean.lower():
            journal_name = "Jurnal TIMES (Technology I-Net Modeling Expert System)"

        study_obj = {
            "study_id": f"SR-MBG-{int(idx_str):02d}",
            "item_number": int(idx_str),
            "authors_short": author_year,
            "title": title,
            "year": year,
            "journal_name": journal_name,
            "method": method,
            "doi": doi_clean,
            "url": f"https://doi.org/{doi_clean}" if doi_clean else "",
            "platform": "Platform X (Twitter)",
            "topic": "Makan Bergizi Gratis (MBG) Public Sentiment Analysis",
            "full_citation": bib_text if bib_text else f"{author_year}. {title}. {journal_name}. https://doi.org/{doi_clean}",
        }
        studies.append(study_obj)

    return studies


def main():
    studies = extract_30_studies_from_docx()
    print(f"Extracted {len(studies)} empirical studies from docx.")

    # 1. SQLite Database Creation
    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA journal_mode = WAL;")

    # Drop old tables if necessary and create
    cur.executescript(
        """
    CREATE TABLE IF NOT EXISTS author_publications (
        pub_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        authors_json TEXT NOT NULL,
        year INTEGER NOT NULL,
        journal_name TEXT NOT NULL,
        volume TEXT,
        issue TEXT,
        pages TEXT,
        doi TEXT UNIQUE,
        issn TEXT,
        publication_status TEXT NOT NULL,
        category TEXT NOT NULL,
        publisher TEXT,
        url TEXT,
        abstract TEXT,
        keywords TEXT,
        citation_apa TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS systematic_review_corpus_30 (
        study_id TEXT PRIMARY KEY,
        item_number INTEGER NOT NULL,
        authors_short TEXT NOT NULL,
        title TEXT NOT NULL,
        year INTEGER NOT NULL,
        journal_name TEXT NOT NULL,
        method TEXT NOT NULL,
        doi TEXT,
        url TEXT,
        platform TEXT NOT NULL,
        topic TEXT NOT NULL,
        full_citation TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS reference_masters (
        doi TEXT PRIMARY KEY,
        clean_title TEXT NOT NULL,
        authors_json TEXT NOT NULL,
        publication_year INTEGER NOT NULL,
        journal_name TEXT NOT NULL,
        verification_status TEXT NOT NULL CHECK(verification_status IN ('VERIFIED_LOCAL', 'VERIFIED_ONLINE', 'UNVERIFIED')),
        source_origin TEXT NOT NULL,
        citation_apa TEXT NOT NULL,
        last_verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    )

    # Insert Author Publications
    for p in AUTHOR_PUBLICATIONS:
        cur.execute(
            """
        INSERT OR REPLACE INTO author_publications (
            pub_id, title, authors_json, year, journal_name, volume, issue, pages,
            doi, issn, publication_status, category, publisher, url, abstract, keywords, citation_apa
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                p["pub_id"],
                p["title"],
                json.dumps(p["authors"]),
                p["year"],
                p["journal_name"],
                p["volume"],
                p["issue"],
                p["pages"],
                p["doi"],
                p["issn"],
                p["publication_status"],
                p["category"],
                p["publisher"],
                p["url"],
                p["abstract"],
                p["keywords"],
                p["citation_apa"],
            ),
        )

        # Also register into reference_masters
        cur.execute(
            """
        INSERT OR REPLACE INTO reference_masters (
            doi, clean_title, authors_json, publication_year, journal_name,
            verification_status, source_origin, citation_apa
        ) VALUES (?, ?, ?, ?, ?, 'VERIFIED_LOCAL', 'Author_Publications', ?)
        """,
            (
                p["doi"],
                p["title"],
                json.dumps(p["authors"]),
                p["year"],
                p["journal_name"],
                p["citation_apa"],
            ),
        )

    # Insert 30 Systematic Review Studies
    for s in studies:
        cur.execute(
            """
        INSERT OR REPLACE INTO systematic_review_corpus_30 (
            study_id, item_number, authors_short, title, year, journal_name,
            method, doi, url, platform, topic, full_citation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                s["study_id"],
                s["item_number"],
                s["authors_short"],
                s["title"],
                s["year"],
                s["journal_name"],
                s["method"],
                s["doi"],
                s["url"],
                s["platform"],
                s["topic"],
                s["full_citation"],
            ),
        )

        # Register in reference_masters
        effective_doi = s["doi"] if s["doi"] else f"local:sr_mbg_{s['item_number']:02d}"
        cur.execute(
            """
        INSERT OR REPLACE INTO reference_masters (
            doi, clean_title, authors_json, publication_year, journal_name,
            verification_status, source_origin, citation_apa
        ) VALUES (?, ?, ?, ?, ?, 'VERIFIED_LOCAL', 'PRISMA_2020_Review_Corpus', ?)
        """,
            (
                effective_doi,
                s["title"],
                json.dumps([s["authors_short"]]),
                s["year"],
                s["journal_name"],
                s["full_citation"],
            ),
        )

    conn.commit()
    conn.close()
    print(f"Database successfully saved to: {SQLITE_PATH}")

    # 2. JSON & CSV Export
    with open(DB_DIR / "author_publications.json", "w", encoding="utf-8") as f:
        json.dump(AUTHOR_PUBLICATIONS, f, indent=2, ensure_ascii=False)

    with open(DB_DIR / "systematic_review_30_corpus.json", "w", encoding="utf-8") as f:
        json.dump(studies, f, indent=2, ensure_ascii=False)

    # CSV Authors
    with open(DB_DIR / "author_publications.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(AUTHOR_PUBLICATIONS[0].keys()))
        writer.writeheader()
        for p in AUTHOR_PUBLICATIONS:
            p_copy = dict(p)
            p_copy["authors"] = "; ".join(p["authors"])
            writer.writerow(p_copy)

    # CSV 30 Studies
    with open(DB_DIR / "systematic_review_30_corpus.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(studies[0].keys()))
        writer.writeheader()
        for s in studies:
            writer.writerow(s)

    # 3. Synchronize with TesisCheck_MIKOM2026 and AI-Thesis-Generator databases
    external_dbs = [
        Path("/Users/jevin/Downloads/TesisCheck_MIKOM2026/workspace/tesis_check.db"),
        Path("/Users/jevin/AI-Thesis-Generator/workspace/tesis_check.db"),
    ]

    for ext_db in external_dbs:
        if ext_db.exists():
            try:
                e_conn = sqlite3.connect(ext_db)
                e_cur = e_conn.cursor()
                # Ensure reference_masters table exists
                e_cur.execute(
                    """
                CREATE TABLE IF NOT EXISTS reference_masters (
                    doi TEXT PRIMARY KEY,
                    clean_title TEXT NOT NULL,
                    authors_json TEXT NOT NULL,
                    publication_year INTEGER,
                    journal_name TEXT,
                    verification_status TEXT NOT NULL CHECK(verification_status IN ('VERIFIED_LOCAL', 'VERIFIED_ONLINE', 'UNVERIFIED')),
                    source_origin TEXT NOT NULL,
                    last_verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                )
                # Seed all items
                for p in AUTHOR_PUBLICATIONS:
                    e_cur.execute(
                        """
                    INSERT OR REPLACE INTO reference_masters (
                        doi, clean_title, authors_json, publication_year, journal_name,
                        verification_status, source_origin
                    ) VALUES (?, ?, ?, ?, ?, 'VERIFIED_LOCAL', 'Author_Publications')
                    """,
                        (p["doi"], p["title"], json.dumps(p["authors"]), p["year"], p["journal_name"]),
                    )

                for s in studies:
                    eff_doi = s["doi"] if s["doi"] else f"local:sr_mbg_{s['item_number']:02d}"
                    e_cur.execute(
                        """
                    INSERT OR REPLACE INTO reference_masters (
                        doi, clean_title, authors_json, publication_year, journal_name,
                        verification_status, source_origin
                    ) VALUES (?, ?, ?, ?, ?, 'VERIFIED_LOCAL', 'PRISMA_2020_Review_Corpus')
                    """,
                        (eff_doi, s["title"], json.dumps([s["authors_short"]]), s["year"], s["journal_name"]),
                    )
                e_conn.commit()
                e_conn.close()
                print(f"Synchronized {len(AUTHOR_PUBLICATIONS) + len(studies)} references into {ext_db}")
            except Exception as e:
                print(f"Failed syncing into {ext_db}: {e}")

    # 4. Generate updated citation.bib and citation.ris in ROOT_DIR
    bib_entries = []
    # Author publications in bib
    for p in AUTHOR_PUBLICATIONS:
        author_str = " and ".join(p["authors"])
        safe_key = "sari2026_" + re.sub(r"[^a-zA-Z0-9]", "", p["title"][:20]).lower()
        bib_entries.append(
            f"""@article{{{safe_key},
  author    = {{{author_str}}},
  title     = {{{p['title']}}},
  journal   = {{{p['journal_name']}}},
  year      = {{{p['year']}}},
  volume    = {{{p['volume']}}},
  number    = {{{p['issue']}}},
  pages     = {{{p['pages']}}},
  doi       = {{{p['doi']}}},
  issn      = {{{p['issn']}}},
  url       = {{{p['url']}}},
  note      = {{Status: {p['publication_status']}}}
}}"""
        )

    # 30 Systematic Review Studies in bib
    for s in studies:
        safe_key = f"mbg_sr_{s['item_number']:02d}_{re.sub(r'[^a-zA-Z0-9]', '', s['authors_short'][:12]).lower()}"
        bib_entries.append(
            f"""@article{{{safe_key},
  author    = {{{s['authors_short']}}},
  title     = {{{s['title']}}},
  journal   = {{{s['journal_name']}}},
  year      = {{{s['year']}}},
  doi       = {{{s['doi']}}},
  url       = {{{s['url']}}},
  keywords  = {{{s['topic']}}},
  note      = {{Method: {s['method']}}}
}}"""
        )

    with open(ROOT_DIR / "citation_all_corpus.bib", "w", encoding="utf-8") as f:
        f.write("\n\n".join(bib_entries))
    print(f"Saved {len(bib_entries)} BibTeX citations to citation_all_corpus.bib")


if __name__ == "__main__":
    main()
