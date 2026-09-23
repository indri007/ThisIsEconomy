from docx import Document
from pathlib import Path

DOC = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V9.docx")

if not DOC.exists():
    print(f"ERROR: File tidak ditemukan: {DOC}")
    raise SystemExit(1)

doc = Document(str(DOC))

print("=" * 70)
print("HMC AUDIT V8")
print("=" * 70)
print(f"FILE: {DOC}")
print(f"SIZE: {DOC.stat().st_size / 1024:.1f} KB")
print(f"PARAGRAPHS: {len(doc.paragraphs)}")
print(f"TABLES: {len(doc.tables)}")
print(f"SECTIONS: {len(doc.sections)}")

# ------------------------------------------------------------
# 1. MARGINS
# ------------------------------------------------------------
print("\n[1] MARGINS")

for i, sec in enumerate(doc.sections, 1):
    print(
        f"Section {i}: "
        f"top={sec.top_margin.inches:.2f}, "
        f"bottom={sec.bottom_margin.inches:.2f}, "
        f"left={sec.left_margin.inches:.2f}, "
        f"right={sec.right_margin.inches:.2f}"
    )

# ------------------------------------------------------------
# 2. FONT / SPACING SAMPLE
# ------------------------------------------------------------
print("\n[2] FONT / SPACING SAMPLE")

for i, para in enumerate(doc.paragraphs[:20], 1):
    if not para.runs:
        continue

    r = para.runs[0]
    pf = para.paragraph_format

    print(
        f"P{i}: "
        f"font={r.font.name}, "
        f"size={r.font.size.pt if r.font.size else None}, "
        f"line_spacing={pf.line_spacing}, "
        f"before={pf.space_before.pt if pf.space_before else 0}, "
        f"after={pf.space_after.pt if pf.space_after else 0}"
    )

# ------------------------------------------------------------
# 3. FIRST 20 PARAGRAPHS
# ------------------------------------------------------------
print("\n[3] FIRST 20 PARAGRAPHS")

for i, para in enumerate(doc.paragraphs[:20], 1):
    print(f"P{i}: {para.text[:200]}")

# ------------------------------------------------------------
# 4. ANONYMIZATION CHECK
# ------------------------------------------------------------
print("\n[4] ANONYMIZATION CHECK")

full_text = "\n".join(p.text for p in doc.paragraphs)

identity_terms = [
    "Indri Anjar Kartika Sari",
    "25067020011@student.upnjatim.ac.id",
    "Universitas Pembangunan Nasional",
    "UPN Veteran Jawa Timur",
]

for term in identity_terms:
    if term.lower() in full_text.lower():
        print(f"REVIEW: identity term found -> {term}")
    else:
        print(f"PASS: {term}")

# ------------------------------------------------------------
# 5. TARGETED TYPO / SPACING CHECK
# ------------------------------------------------------------
print("\n[5] TARGETED TYPO CHECK")

bad = [
    "communicationtopology",
    "orformalize",
    "crisiscommunication",
    "capability,while",
    "responsesto",
    "TheAI",
    "observedinteraction",
    "anAI-mediated",
    "asubstantial",
    "accountssuch",
    "facts.The",
    "historic paradigm shift",
    "historical paradigm shift",
    "macro-topologicalstructure",
    "influenceasymmetry",
    "budgeting,and",
    "substantiatethe",
]

found = 0

for i, para in enumerate(doc.paragraphs, 1):
    hits = [x for x in bad if x.lower() in para.text.lower()]

    if hits:
        found += len(hits)
        print(f"REVIEW P{i}: {hits}")
        print(para.text)

print(f"TARGETED TYPO ISSUES: {found}")

# ------------------------------------------------------------
# 6. MALFORMED LATEX CHECK
# ------------------------------------------------------------
print("\n[6] LATEX CHECK")

latex_bad = [
    "ext{out}",
    "ext{in}",
    "$C_{      ext",
    "$C_{ ext",
]

latex_found = 0

for i, para in enumerate(doc.paragraphs, 1):
    hits = [x for x in latex_bad if x in para.text]

    if hits:
        latex_found += len(hits)
        print(f"REVIEW P{i}: {hits}")
        print(para.text)

print(f"LATEX ISSUES: {latex_found}")

# ------------------------------------------------------------
# 7. STRONG CLAIM CHECK
# ------------------------------------------------------------
print("\n[7] STRONG CLAIM CHECK")

strong_terms = [
    "textbook manifestation",
    "sociologically profound",
    "functionally dead",
    "historic paradigm shift",
    "historical paradigm shift",
    "must abandon",
    "cannot cure",
    "obsolete",
    "empirical proof",
    "destroys democratic legitimacy",
    "absolute breakdown",
]

strong_found = 0

for i, para in enumerate(doc.paragraphs, 1):
    hits = [x for x in strong_terms if x.lower() in para.text.lower()]

    if hits:
        strong_found += len(hits)
        print(f"REVIEW P{i}: {hits}")
        print(para.text)

print(f"STRONG CLAIM ISSUES: {strong_found}")

# ------------------------------------------------------------
# 8. REQUIRED DECLARATION TERMS
# ------------------------------------------------------------
print("\n[8] DECLARATIONS CHECK")

declarations = [
    "Funding",
    "Competing Interests",
    "Conflict of Interest",
    "Data and Code Availability",
    "Author Contributions",
    "CRediT",
    "Ethics Approval",
    "AI",
]

for term in declarations:
    if term.lower() in full_text.lower():
        print(f"PASS: {term}")
    else:
        print(f"REVIEW: missing {term}")

# ------------------------------------------------------------
# 9. KEY STRUCTURE
# ------------------------------------------------------------
print("\n[9] MAIN STRUCTURE CHECK")

required_headings = [
    "ABSTRACT",
    "1. INTRODUCTION",
    "2. THEORETICAL FRAMEWORK AND LITERATURE REVIEW",
    "3. METHODOLOGY AND RESEARCH DESIGN",
    "4. EMPIRICAL RESULTS",
    "5. DISCUSSION",
    "6. THEORETICAL AND PRACTICAL CONTRIBUTIONS",
    "7. RESEARCH LIMITATIONS AND FUTURE RESEARCH AGENDA",
    "8. CONCLUSION",
    "STATEMENTS AND DECLARATIONS",
    "REFERENCES",
]

for h in required_headings:
    if h.lower() in full_text.lower():
        print(f"PASS: {h}")
    else:
        print(f"REVIEW: missing {h}")

print("\n" + "=" * 70)
print("HMC AUDIT V8 COMPLETE")
print("=" * 70)
