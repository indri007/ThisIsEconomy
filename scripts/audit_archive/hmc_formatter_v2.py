from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re

SOURCE = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT.docx")
OUT = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V2.docx")
AUDIT = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_MANUSCRIPT_AUDIT_V2.txt")

# ============================================================
# HMC V2
# ============================================================

doc = Document(SOURCE)

# ------------------------------------------------------------
# 1. GLOBAL DOCUMENT FORMAT
# ------------------------------------------------------------

section = doc.sections[0]
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin = Inches(1)
section.right_margin = Inches(1)

for p in doc.paragraphs:
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

# ------------------------------------------------------------
# 2. CLEAN MARKDOWN
# ------------------------------------------------------------

for p in doc.paragraphs:
    for r in p.runs:
        r.text = re.sub(r"\*\*(.*?)\*\*", r"\1", r.text)
        r.text = re.sub(r"__(.*?)__", r"\1", r.text)
        r.text = re.sub(r"`([^`]*)`", r"\1", r.text)

# ------------------------------------------------------------
# 3. EVIDENCE-BOUNDED REVISIONS
# ------------------------------------------------------------

replacements = {
    "absolute breakdown": "substantial fragmentation",
    "empirical proof": "empirical evidence",
    "destroys democratic legitimacy": "may undermine perceptions of democratic legitimacy",
    "textbook manifestation": "clear empirical instance",
    "sociologically profound": "sociologically significant",
    "functionally dead": "structurally constrained",
    "historic paradigm shift": "potential shift in communication dynamics",
    "cannot cure": "is unlikely to resolve",
    "must abandon": "may need to reconsider",
    "obsolete": "less adequate for explaining",
}

changed_claims = []

for p in doc.paragraphs:
    old = p.text
    new = old

    for old_phrase, new_phrase in replacements.items():
        if old_phrase in new:
            new = new.replace(old_phrase, new_phrase)
            changed_claims.append(
                f"{old_phrase} -> {new_phrase}"
            )

    if new != old:
        p.text = new

# ------------------------------------------------------------
# 4. ABSTRACT
# ------------------------------------------------------------

# Evidence-bounded abstract based only on the manuscript's reported
# dataset, methods and findings.

abstract_text = (
    "This study examines public discourse surrounding Indonesia's "
    "Free Nutritious Meal (MBG) program on Platform X through a "
    "tri-layer computational communication framework. The analysis "
    "integrates granular emotion classification, pragmatic sarcasm "
    "validation, directed social network analysis, and aspect-based "
    "sentiment analysis to examine affective, structural, and policy "
    "dimensions of the observed discourse. The corpus comprised 5,310 "
    "raw posts, with 5,263 retained after preprocessing and quality "
    "control. A fine-tuned IndoBERT model was used to classify nine "
    "Plutchik-derived emotion categories. Sarcasm was examined in a "
    "dedicated corpus of 3,395 posts using lexical contradiction and "
    "text-emoji incongruence indicators. The interaction network "
    "contained 971 nodes and 666 unique edges, with Louvain community "
    "detection identifying 332 communities and a modularity value of "
    "0.9837. Aspect-based analysis covered logistics, budgeting, and "
    "food nutritional quality. The results indicate strong class "
    "imbalance in emotion classification and substantial fragmentation "
    "in the observed interaction network. Across the three policy "
    "aspects, negative affect was concentrated around logistics, "
    "budgeting, and nutritional quality. These findings illustrate how "
    "computational analysis can connect affective expression, network "
    "structure, and operational policy themes in digital public-policy "
    "discourse."
)

abstract_words = abstract_text.split()

if not (150 <= len(abstract_words) <= 250):
    raise ValueError(
        f"Abstract V2 has {len(abstract_words)} words; "
        "must be between 150 and 250."
    )

# Find ABSTRACT heading and replace following text until next major
# numbered heading.
paragraphs = doc.paragraphs
abstract_index = None

for i, p in enumerate(paragraphs):
    if p.text.strip().upper() == "ABSTRACT":
        abstract_index = i
        break

if abstract_index is None:
    raise RuntimeError("ABSTRACT heading not found.")

# Locate next major section.
next_section_index = None

for i in range(abstract_index + 1, len(paragraphs)):
    txt = paragraphs[i].text.strip()
    if re.match(r"^1\.\s+INTRODUCTION$", txt, re.I):
        next_section_index = i
        break

if next_section_index is None:
    raise RuntimeError("Could not locate 1. INTRODUCTION after ABSTRACT.")

# Replace first paragraph after ABSTRACT.
doc.paragraphs[abstract_index + 1].text = abstract_text

# Remove additional old abstract paragraphs before Introduction,
# but preserve the first replacement paragraph.
for i in range(next_section_index - 1, abstract_index + 1, -1):
    p = doc.paragraphs[i]
    if i != abstract_index + 1:
        p._element.getparent().remove(p._element)

# ------------------------------------------------------------
# 5. KEYWORDS
# ------------------------------------------------------------

keyword_text = (
    "Keywords: Makan Bergizi Gratis; Platform X; Social Network Analysis; "
    "IndoBERT; Phygital Gap"
)

keyword_found = False

for p in doc.paragraphs:
    if re.match(r"^\s*Keywords?\s*:", p.text, re.I):
        p.text = keyword_text
        keyword_found = True
        break

if not keyword_found:
    # Insert after abstract paragraph.
    abs_p = doc.paragraphs[abstract_index + 1]
    new_p = OxmlElement("w:p")
    abs_p._p.addnext(new_p)

    from docx.text.paragraph import Paragraph
    keyword_para = Paragraph(new_p, abs_p._parent)
    keyword_para.text = keyword_text

# ------------------------------------------------------------
# 6. HMC REQUIRED STATEMENTS
# ------------------------------------------------------------

def find_paragraph_index(text):
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().lower() == text.lower():
            return i
    return None

# Remove previous placeholder statements if V2 is rerun.
for p in list(doc.paragraphs):
    if "AUTHOR VERIFICATION REQUIRED" in p.text:
        p._element.getparent().remove(p._element)

# Find REFERENCES.
ref_index = find_paragraph_index("REFERENCES")

if ref_index is not None:
    statements = [
        ("STATEMENTS AND DECLARATIONS", ""),
        ("Funding", "AUTHOR VERIFICATION REQUIRED — state whether external funding was received."),
        ("Conflict of Interest", "AUTHOR VERIFICATION REQUIRED — state whether any conflict of interest exists."),
        ("Data Availability", "AUTHOR VERIFICATION REQUIRED — specify whether the derived data/code are available and under what access conditions."),
        ("AI / Tool Disclosure", "AUTHOR VERIFICATION REQUIRED — disclose any generative AI or computational tools used in manuscript preparation, analysis, or coding, consistent with the target journal's policy."),
    ]

    ref_p = doc.paragraphs[ref_index]

    for heading, body in reversed(statements):
        p1 = OxmlElement("w:p")
        p2 = OxmlElement("w:p")

        ref_p._p.addprevious(p1)
        ref_p._p.addprevious(p2)

        from docx.text.paragraph import Paragraph

        heading_para = Paragraph(p1, ref_p._parent)
        body_para = Paragraph(p2, ref_p._parent)

        heading_para.text = heading
        body_para.text = body

# ------------------------------------------------------------
# 7. PAGE NUMBERS
# ------------------------------------------------------------

for section in doc.sections:
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = 1

    run = p.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = " PAGE "

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

# ------------------------------------------------------------
# 8. CONTINUOUS LINE NUMBERS
# ------------------------------------------------------------

settings = doc.settings.element

existing = settings.find(qn("w:lnNumType"))
if existing is not None:
    settings.remove(existing)

ln = OxmlElement("w:lnNumType")
ln.set(qn("w:countBy"), "1")
ln.set(qn("w:start"), "1")
ln.set(qn("w:restart"), "continuous")

settings.append(ln)

# ------------------------------------------------------------
# 9. SAVE
# ------------------------------------------------------------

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)

# ------------------------------------------------------------
# 10. AUDIT
# ------------------------------------------------------------

audit_doc = Document(OUT)

all_text = "\n".join(p.text for p in audit_doc.paragraphs)

# Abstract
abstract_count = len(abstract_text.split())

# Keywords
keyword_match = re.search(
    r"Keywords:\s*(.+)",
    all_text,
    re.I
)

if keyword_match:
    keywords = [
        x.strip()
        for x in keyword_match.group(1).split(";")
        if x.strip()
    ]
else:
    keywords = []

# Strong claims remaining
remaining_claims = []

for phrase in replacements:
    if phrase in all_text:
        remaining_claims.append(phrase)

# Identifying terms
identifying_terms = [
    "Indri Anjar Kartika Sari",
    "UPN VJ",
    "Universitas Pembangunan Nasional",
]

remaining_identifying = [
    x for x in identifying_terms
    if x.lower() in all_text.lower()
]

# Required statements
required_sections = [
    "Funding",
    "Conflict of Interest",
    "Data Availability",
    "AI / Tool Disclosure",
]

missing_sections = [
    x for x in required_sections
    if x.lower() not in all_text.lower()
]

# Basic figure/table audit
figure_mentions = len(
    re.findall(r"\bFigure\s+\d+", all_text, re.I)
)

table_mentions = len(
    re.findall(r"\bTable\s+\d+", all_text, re.I)
)

audit = []

audit.append("HMC MANUSCRIPT V2 AUDIT")
audit.append("=" * 70)
audit.append("")
audit.append(f"OUTPUT: {OUT}")
audit.append("")
audit.append("ABSTRACT")
audit.append("-" * 70)
audit.append(f"Word count: {abstract_count}")
audit.append(
    "STATUS: PASS"
    if 150 <= abstract_count <= 250
    else "STATUS: FAIL"
)
audit.append("")
audit.append("KEYWORDS")
audit.append("-" * 70)
audit.append(f"Count: {len(keywords)}")
audit.append(f"Keywords: {keywords}")
audit.append(
    "STATUS: PASS"
    if 4 <= len(keywords) <= 6
    else "STATUS: FAIL"
)
audit.append("")
audit.append("STRONG CLAIM AUDIT")
audit.append("-" * 70)

if remaining_claims:
    for x in remaining_claims:
        audit.append(f"REMAINING: {x}")
    audit.append("STATUS: NEEDS REVIEW")
else:
    audit.append("No targeted strong-claim phrases remain.")
    audit.append("STATUS: PASS")

audit.append("")
audit.append("ANONYMIZATION AUDIT")
audit.append("-" * 70)

if remaining_identifying:
    for x in remaining_identifying:
        audit.append(f"FOUND: {x}")
    audit.append("STATUS: FAIL")
else:
    audit.append("No configured author-identifying terms found.")
    audit.append("STATUS: PASS")

audit.append("")
audit.append("REQUIRED HMC STATEMENTS")
audit.append("-" * 70)

for x in required_sections:
    if x.lower() in all_text.lower():
        audit.append(f"{x}: PRESENT — AUTHOR VERIFICATION REQUIRED")
    else:
        audit.append(f"{x}: MISSING")

audit.append("")
audit.append("FIGURE/TABLE AUDIT")
audit.append("-" * 70)
audit.append(f"Figure call-outs detected: {figure_mentions}")
audit.append(f"Table call-outs detected: {table_mentions}")
audit.append(
    "NOTE: This audit checks textual call-outs only; "
    "it does not verify that embedded figures/tables exist or "
    "that they are placed according to journal production requirements."
)

audit.append("")
audit.append("FORMAT")
audit.append("-" * 70)
audit.append("Target font: Times New Roman 12 pt")
audit.append("Target spacing: double")
audit.append("Target margins: 1 inch")
audit.append("Page numbers: inserted")
audit.append("Line numbering: continuous XML setting inserted")

AUDIT.write_text("\n".join(audit), encoding="utf-8")

print("=" * 70)
print("HMC V2 COMPLETE")
print("=" * 70)
print(f"OUTPUT : {OUT}")
print(f"AUDIT  : {AUDIT}")
print(f"ABSTRACT WORDS: {abstract_count}")
print(f"KEYWORDS: {len(keywords)}")
print("=" * 70)
