from docx import Document
from pathlib import Path

src = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V9.docx")
out = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V10.docx")

doc = Document(str(src))

remove_exact = {
    "Authors: [Names and Affiliations Anonymized for Double-Blind Peer Review]",
    "Target Publication: Social Network Analysis and Mining (Springer Nature Switzerland, Scopus Q1, SJR 0.76)",
    "Scopus ASJC Classification: 3315 (Communication), 1702 (Artificial Intelligence), 3312 (Sociology and Political Science)",
    "Scopus Subject Area: Social Sciences (Communication) · Computer Science (Artificial Intelligence)",
    "---",
}

removed = []

# Remove only metadata paragraphs BEFORE the Introduction.
# Keep the title, abstract, keywords, and all manuscript content.
for para in list(doc.paragraphs):
    text = para.text.strip()

    if text in remove_exact:
        # Do not remove separator if it somehow occurs later in the manuscript.
        # Only remove separators appearing before Introduction.
        intro_seen = any(
            p.text.strip().upper() == "1. INTRODUCTION"
            for p in doc.paragraphs
        )

        if text != "---" or not intro_seen:
            parent = para._element.getparent()
            parent.remove(para._element)
            removed.append(text)

doc.save(str(out))

print("=" * 70)
print("HMC V10 CREATED")
print("=" * 70)
print(f"INPUT : {src}")
print(f"OUTPUT: {out}")
print(f"REMOVED PARAGRAPHS: {len(removed)}")

for x in removed:
    print("REMOVED:", x)

print("=" * 70)
