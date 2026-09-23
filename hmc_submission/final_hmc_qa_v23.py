from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_LINE_SPACING
from zipfile import ZipFile
import re
import os

FILE = "HMC_REVIEW_MANUSCRIPT_V22.docx"
REPORT = "HMC_FINAL_QA_V23.txt"

doc = Document(FILE)

results = []
issues = []

def check(name, condition, detail=""):
    status = "PASS" if condition else "REVIEW"
    results.append((status, name, detail))
    if not condition:
        issues.append((name, detail))

# ============================================================
# 1. BASIC FILE
# ============================================================

check(
    "FILE EXISTS",
    os.path.exists(FILE),
    FILE
)

check(
    "PARAGRAPH COUNT",
    len(doc.paragraphs) > 50,
    f"{len(doc.paragraphs)} paragraphs"
)

# ============================================================
# 2. DOUBLE-BLIND CONTENT
# ============================================================

full_text = "\n".join(p.text for p in doc.paragraphs)

identity_patterns = [
    r"\bIndri Anjar Kartika Sari\b",
    r"\bUPN\b",
    r"Universitas Pembangunan Nasional",
    r"Veteran Jawa Timur",
    r"ORCID",
    r"25067020011@student",
    r"@student\.upnjatim",
]

identity_hits = []

for pattern in identity_patterns:
    if re.search(pattern, full_text, re.I):
        identity_hits.append(pattern)

check(
    "DOUBLE-BLIND IDENTITY",
    not identity_hits,
    "No author/affiliation/ORCID/contact identity found"
    if not identity_hits else str(identity_hits)
)

# ============================================================
# 3. HIGH-RISK TERMS
# ============================================================

high_risk = [
    "Algorithmic Oracle",
    "rancid physical meals",
    "severe trauma",
    "paralyze institutional legitimacy",
    "dismantle the conditions",
    "passive receptacles",
    "absolute zero",
    "most transformative",
    "dominating the graph",
    "remained silent",
]

high_hits = []

for i, p in enumerate(doc.paragraphs, 1):
    for term in high_risk:
        if term.lower() in p.text.lower():
            high_hits.append(f"P{i}: {term}")

check(
    "HIGH-RISK LANGUAGE",
    not high_hits,
    "All targeted high-risk wording removed"
    if not high_hits else "\n".join(high_hits)
)

# ============================================================
# 4. SPACING / TYPO ERRORS
# ============================================================

spacing_patterns = [
    r"\bandconsumer\b",
    r"\bpoliticalcommunication\b",
    r"\bwelfaremegaprojects\b",
    r"\bcommunicatedexpectations\b",
    r"\bofan\b",
    r"\binthe\b",
    r"\bof the\b",  # informational only, filtered below
    r"GovernanceGap",
]

spacing_hits = []

for i, p in enumerate(doc.paragraphs, 1):
    text = p.text
    for pattern in spacing_patterns:
        if pattern == r"\bof the\b":
            continue
        if re.search(pattern, text, re.I):
            spacing_hits.append(f"P{i}: {pattern}")

check(
    "SPACING / CONCATENATION",
    not spacing_hits,
    "No targeted concatenation errors"
    if not spacing_hits else "\n".join(spacing_hits)
)

# ============================================================
# 5. DOCUMENT FORMAT
# ============================================================

font_issues = []
size_issues = []

for i, p in enumerate(doc.paragraphs, 1):
    for run in p.runs:
        if not run.text.strip():
            continue

        if run.font.name and run.font.name.lower() not in [
            "times new roman",
            "timesnewroman"
        ]:
            font_issues.append(
                f"P{i}: {run.font.name}"
            )

        if run.font.size and abs(run.font.size.pt - 12) > 0.2:
            size_issues.append(
                f"P{i}: {run.font.size.pt} pt"
            )

check(
    "FONT",
    not font_issues,
    "Times New Roman"
    if not font_issues else "\n".join(font_issues[:20])
)

check(
    "FONT SIZE",
    not size_issues,
    "12 pt"
    if not size_issues else "\n".join(size_issues[:20])
)

# ============================================================
# 6. LINE SPACING
# ============================================================

line_issues = []

for i, p in enumerate(doc.paragraphs, 1):
    if not p.text.strip():
        continue

    fmt = p.paragraph_format

    # HMC requires double spacing.
    if fmt.line_spacing is not None:
        if isinstance(fmt.line_spacing, float):
            # 2.0 = double
            if abs(fmt.line_spacing - 2.0) > 0.05:
                line_issues.append(
                    f"P{i}: line_spacing={fmt.line_spacing}"
                )

check(
    "DOUBLE SPACING",
    not line_issues,
    "No explicit non-double spacing detected"
    if not line_issues else "\n".join(line_issues[:20])
)

# ============================================================
# 7. MARGINS
# ============================================================

section_issues = []

for i, sec in enumerate(doc.sections, 1):
    margins = {
        "top": sec.top_margin.inches,
        "bottom": sec.bottom_margin.inches,
        "left": sec.left_margin.inches,
        "right": sec.right_margin.inches,
    }

    for side, value in margins.items():
        if abs(value - 1.0) > 0.05:
            section_issues.append(
                f"Section {i} {side}={value:.3f} inch"
            )

check(
    "ONE-INCH MARGINS",
    not section_issues,
    "All margins approximately 1 inch"
    if not section_issues else "\n".join(section_issues)
)

# ============================================================
# 8. HEADINGS / STRUCTURE
# ============================================================

required_terms = [
    "Abstract",
    "Introduction",
    "Method",
    "Results",
    "Discussion",
    "Conclusion",
    "References",
]

missing_sections = []

for term in required_terms:
    if not re.search(rf"\b{re.escape(term)}\b", full_text, re.I):
        missing_sections.append(term)

check(
    "MANUSCRIPT STRUCTURE",
    not missing_sections,
    "Core sections detected"
    if not missing_sections else
    "Missing: " + ", ".join(missing_sections)
)

# ============================================================
# 9. AI / ALGORITHMIC ORACLE CONSISTENCY
# ============================================================

oracle_count = len(re.findall(r"Algorithmic Oracle", full_text, re.I))

check(
    "ALGORITHMIC ORACLE REMOVED",
    oracle_count == 0,
    f"Occurrences: {oracle_count}"
)

# ============================================================
# 10. CRITICAL NUMBERS
# ============================================================

critical_values = [
    ("Corpus N=5263", "5,263"),
    ("Sarcasm N=3395", "3,395"),
    ("Sarcasm rate", "9.28%"),
    ("Network nodes", "971"),
    ("Network edges", "666"),
    ("Network density", "0.0011"),
    ("Reciprocity", "1.21%"),
    ("Giant component", "9.17%"),
    ("Communities", "332"),
    ("Modularity", "0.9837"),
    ("Disgust", "56.24%"),
    ("Trust", "20.39%"),
    ("Neutral", "12.33%"),
    ("Anticipation", "9.60%"),
]

number_missing = []

for label, value in critical_values:
    if value not in full_text:
        number_missing.append(f"{label}: {value}")

check(
    "CRITICAL RESULTS PRESERVED",
    not number_missing,
    "Key reported values detected"
    if not number_missing else "\n".join(number_missing)
)

# ============================================================
# 11. TABLE PLACEHOLDER DETECTION
# ============================================================

pipe_tables = []

for i, p in enumerate(doc.paragraphs, 1):
    txt = p.text.strip()
    if txt.startswith("|") and txt.endswith("|"):
        pipe_tables.append(i)

check(
    "TABLE FORMAT REVIEW",
    len(pipe_tables) > 0,
    f"{len(pipe_tables)} pipe-style table rows detected; "
    "review before submission because HMC prefers tables at manuscript end."
)

# ============================================================
# 12. METADATA
# ============================================================

metadata_issues = []

with ZipFile(FILE, "r") as z:
    names = z.namelist()

    core_xml = z.read("docProps/core.xml").decode(
        "utf-8",
        errors="ignore"
    )

    app_xml = ""
    if "docProps/app.xml" in names:
        app_xml = z.read("docProps/app.xml").decode(
            "utf-8",
            errors="ignore"
        )

    suspicious_metadata = [
        "Indri",
        "Anjar",
        "Kartika",
        "UPN",
        "Veteran",
        "student.upnjatim",
    ]

    for term in suspicious_metadata:
        if term.lower() in core_xml.lower():
            metadata_issues.append(
                f"core.xml contains: {term}"
            )

check(
    "WORD METADATA ANONYMIZED",
    not metadata_issues,
    "No author identity detected in core metadata"
    if not metadata_issues else "\n".join(metadata_issues)
)

# ============================================================
# FINAL REPORT
# ============================================================

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("HMC FINAL SUBMISSION QA — V23\n")
    f.write("=" * 100 + "\n")
    f.write(f"FILE: {FILE}\n\n")

    for status, name, detail in results:
        f.write(f"[{status}] {name}\n")
        f.write(f"       {detail}\n")

    f.write("\n" + "=" * 100 + "\n")

    if issues:
        f.write("FINAL STATUS: REVIEW REQUIRED\n")
        f.write("=" * 100 + "\n")
        for name, detail in issues:
            f.write(f"- {name}: {detail}\n")
    else:
        f.write("FINAL STATUS: PASS\n")
        f.write("=" * 100 + "\n")
        f.write(
            "V22 passed all automated HMC submission checks.\n"
        )

print("=" * 100)
print("HMC FINAL QA V23")
print("=" * 100)

for status, name, detail in results:
    print(f"[{status}] {name}: {detail}")

print("\n" + "=" * 100)

if issues:
    print("FINAL STATUS: REVIEW REQUIRED")
    print("=" * 100)
    for name, detail in issues:
        print(f"- {name}")
        print(f"  {detail}")
else:
    print("FINAL STATUS: PASS")
    print("=" * 100)
    print("V22 PASSED ALL AUTOMATED HMC SUBMISSION CHECKS.")

print(f"\nREPORT: {REPORT}")
