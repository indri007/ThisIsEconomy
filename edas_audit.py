from docx import Document
from pathlib import Path
import re

SOURCE = Path(
    "/Users/jevin/Documents/tesis_mbg/hmc_submission/"
    "HMC_REVIEW_MANUSCRIPT.docx"
)

REPORT = SOURCE.parent / "EDAS_AUDIT.txt"

if not SOURCE.exists():
    raise FileNotFoundError(f"File tidak ditemukan: {SOURCE}")

doc = Document(SOURCE)
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
text = "\n".join(paragraphs)

results = []

def check(name, condition, ok, fail):
    if condition:
        results.append(("PASS", name, ok))
    else:
        results.append(("REVIEW", name, fail))

# Double-blind
identity_terms = [
    "Indri Anjar Kartika Sari",
    "25067020011",
    "student.upnjatim",
    "Universitas Pembangunan Nasional",
]

found_identity = [
    x for x in identity_terms
    if x.lower() in text.lower()
]

check(
    "DOUBLE-BLIND IDENTIFICATION",
    not found_identity,
    "Tidak ditemukan identitas penulis.",
    f"Ditemukan: {found_identity}"
)

# Abstract
abstract_idx = None
keywords_idx = None

for i, p in enumerate(paragraphs):
    u = p.upper()
    if u == "ABSTRACT":
        abstract_idx = i
    elif u.startswith("KEYWORDS"):
        keywords_idx = i

abstract_text = ""

if abstract_idx is not None and keywords_idx is not None:
    abstract_text = " ".join(
        paragraphs[abstract_idx + 1:keywords_idx]
    )

abstract_words = len(abstract_text.split())

check(
    "ABSTRACT 150-250 WORDS",
    150 <= abstract_words <= 250,
    f"{abstract_words} words",
    f"{abstract_words} words"
)

# Keywords
keywords = []

for p in paragraphs:
    if p.upper().startswith("KEYWORDS"):
        value = p.split(":", 1)[-1]
        keywords = [
            x.strip().rstrip(".")
            for x in re.split(r"[;,]", value)
            if x.strip()
        ]
        break

check(
    "KEYWORDS 4-6",
    4 <= len(keywords) <= 6,
    f"{len(keywords)}: {keywords}",
    f"{len(keywords)}: {keywords}"
)

# Sections
required_sections = [
    "INTRODUCTION",
    "THEORETICAL FRAMEWORK AND LITERATURE REVIEW",
    "METHODOLOGY AND RESEARCH DESIGN",
    "EMPIRICAL RESULTS",
    "DISCUSSION",
    "THEORETICAL AND PRACTICAL CONTRIBUTIONS",
    "RESEARCH LIMITATIONS AND FUTURE RESEARCH AGENDA",
    "CONCLUSION",
    "REFERENCES",
]

missing_sections = [
    s for s in required_sections
    if not any(
        p.upper() == s or p.upper().startswith(s + " ")
        for p in paragraphs
    )
]

check(
    "MAIN SECTION STRUCTURE",
    not missing_sections,
    "Configured main sections detected.",
    f"Missing: {missing_sections}"
)

# Research questions
rq_found = [
    f"RQ{i}"
    for i in range(1, 7)
    if f"RQ{i}" in text
]

check(
    "RESEARCH QUESTIONS RQ1-RQ6",
    len(rq_found) == 6,
    f"Detected: {rq_found}",
    f"Detected: {rq_found}"
)

# Dataset
dataset_values = [
    "5,310",
    "5,263",
    "3,395",
    "315",
    "9.28%",
]

missing = [x for x in dataset_values if x not in text]

check(
    "DATASET CORE VALUES",
    not missing,
    "All configured dataset values detected.",
    f"Missing: {missing}"
)

# Model
model_values = [
    "57.45%",
    "0.1444",
    "0.4563",
    "indobenchmark/indobert-base-p2",
]

missing = [
    x for x in model_values
    if x.lower() not in text.lower()
]

check(
    "MODEL / EVALUATION VALUES",
    not missing,
    "Configured model values detected.",
    f"Missing: {missing}"
)

# SNA
sna_values = [
    "971",
    "666",
    "692",
    "0.0011",
    "1.21%",
    "332",
    "0.9837",
    "@grok",
]

missing = [
    x for x in sna_values
    if x.lower() not in text.lower()
]

check(
    "SNA EMPIRICAL VALUES",
    not missing,
    "Configured SNA values detected.",
    f"Missing: {missing}"
)

# ABSA
absa_values = [
    "403",
    "535",
    "1,344",
    "78.91%",
    "77.01%",
    "71.13%",
]

missing = [x for x in absa_values if x not in text]

check(
    "ABSA EMPIRICAL VALUES",
    not missing,
    "Configured ABSA values detected.",
    f"Missing: {missing}"
)

# Emotions
emotion_classes = [
    "Disgust",
    "Trust",
    "Neutral",
    "Anticipation",
    "Anger",
    "Sadness",
    "Joy",
    "Surprise",
    "Fear",
]

missing = [
    x for x in emotion_classes
    if x.lower() not in text.lower()
]

check(
    "NINE EMOTION CLASSES",
    not missing,
    "All 9 emotion classes detected.",
    f"Missing: {missing}"
)

# Sarcasm
sarcasm_terms = [
    "sarcasm",
    "lexical",
    "emoji",
    "3,395",
]

missing = [
    x for x in sarcasm_terms
    if x.lower() not in text.lower()
]

check(
    "SARCASM ANALYSIS",
    not missing,
    "Sarcasm methodology and corpus indicators detected.",
    f"Missing: {missing}"
)

# References
check(
    "REFERENCES SECTION",
    "REFERENCES" in [p.upper() for p in paragraphs],
    "REFERENCES section detected.",
    "REFERENCES section not detected."
)

# Markdown
markdown = [x for x in ["**", "__", "```"] if x in text]

check(
    "MARKDOWN RESIDUE",
    not markdown,
    "No obvious Markdown residue.",
    f"Detected: {markdown}"
)

# Strong claims
strong_claims = [
    "absolute breakdown",
    "empirical proof",
    "destroys democratic legitimacy",
    "textbook manifestation",
    "sociologically profound",
    "functionally dead",
    "historic paradigm shift",
    "cannot cure",
    "must abandon",
    "obsolete",
]

found = [
    x for x in strong_claims
    if x.lower() in text.lower()
]

check(
    "EVIDENCE-BOUNDED LANGUAGE",
    not found,
    "Configured strong-claim expressions not detected.",
    f"Review: {found}"
)

# HMC relevance
hmc_terms = [
    "human-machine communication",
    "@grok",
    "AI-mediated",
]

missing = [
    x for x in hmc_terms
    if x.lower() not in text.lower()
]

check(
    "HMC COMMUNICATIVE RELEVANCE",
    not missing,
    "HMC-relevant elements detected.",
    f"Missing/review: {missing}"
)

# Summary
pass_count = sum(1 for x in results if x[0] == "PASS")
review_count = sum(1 for x in results if x[0] == "REVIEW")

with REPORT.open("w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("EDAS / CONFERENCE MANUSCRIPT AUDIT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"SOURCE : {SOURCE}\n")
    f.write(f"PASS   : {pass_count}\n")
    f.write(f"REVIEW : {review_count}\n\n")

    for status, name, detail in results:
        f.write(f"[{status}] {name}\n")
        f.write(f"    {detail}\n\n")

print("=" * 80)
print("EDAS / CONFERENCE AUDIT COMPLETE")
print("=" * 80)
print(f"SOURCE : {SOURCE}")
print(f"REPORT : {REPORT}")
print(f"PASS   : {pass_count}")
print(f"REVIEW : {review_count}")
print("=" * 80)
