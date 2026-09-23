from docx import Document
from pathlib import Path

src = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V11.docx")
out = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V12.docx")

doc = Document(str(src))

# Only confirmed missing-space concatenations.
replacements = {
    # Main manuscript
    "withpublic": "with public",
    "ofnetworked": "of networked",
    "networkedgatekeeping": "networked gatekeeping",
    "launchingpromotional": "launching promotional",
    "promotionaldigital": "promotional digital",
    "practicesin": "practices in",
    "fromcomplementing": "from complementing",
    "finalcorpus": "final corpus",
    "inthis": "in this",
    "MBG)program": "MBG) program",
    "theanalyzed": "the analyzed",
    "haveinappropriately": "have inappropriately",
    "FAIRdata": "FAIR data",
    "intothe": "into the",
    "separateTitle": "separate Title",
    "providedin": "provided in",
    "forDouble": "for Double",
    "comply": "comply",
    
    # References
    "CorporateReputation": "Corporate Reputation",
    "ofdeep": "of deep",
    "inquiryinto": "inquiry into",
    "ofthe": "of the",
    "the28th": "the 28th",
    "ofSciences": "of Sciences",
    "103(23),8577": "103(23), 8577",
    "In2018": "In 2018",
    "the28th": "the 28th",
    "InProceedings": "In Proceedings",
    
    # Other confirmed forms from audit
    "bridging marketing theory withpublic": "bridging marketing theory with public",
    "functioning as a central communicativeauthority": "functioning as a central communicative authority",
    "launchingpromotional": "launching promotional",
    "MBG)program": "MBG) program",
    "within theanalyzed": "within the analyzed",
    "the finalcorpus": "the final corpus",
}

changed_paragraphs = 0
changes = []

for para in doc.paragraphs:
    old = para.text
    new = old

    for a, b in replacements.items():
        new = new.replace(a, b)

    if new != old:
        # Preserve paragraph-level formatting.
        if para.runs:
            para.runs[0].text = new
            for run in para.runs[1:]:
                run.text = ""
        else:
            para.add_run(new)

        changed_paragraphs += 1
        changes.append((old, new))

doc.save(str(out))

print("=" * 80)
print("HMC V12 CREATED")
print("=" * 80)
print("INPUT :", src)
print("OUTPUT:", out)
print("CHANGED PARAGRAPHS:", changed_paragraphs)
print()
print("CHANGES:")
for old, new in changes:
    print("- OLD:", old[:180])
    print("  NEW:", new[:180])
print("=" * 80)
