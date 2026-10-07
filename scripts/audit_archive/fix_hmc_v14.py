from docx import Document

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V13.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V14.docx"

doc = Document(src)
changed = []

replacements = {
    "arescrutinized": "are scrutinized",
    "primaryarena": "primary arena",
    "darkirony": "dark irony",
    "positive'or": "positive' or",
    "communicationtopology": "communication topology",
    r"C_{      ext{out}}": r"C_{\text{out}}",
}

for i, p in enumerate(doc.paragraphs, 1):
    old = p.text
    new = old

    for a, b in replacements.items():
        new = new.replace(a, b)

    if new != old:
        p.text = new
        changed.append((i, old, new))

doc.save(out)

print("HMC V14 CREATED")
print("=" * 80)
print("INPUT :", src)
print("OUTPUT:", out)
print("CHANGED PARAGRAPHS:", len(changed))
print()

for i, old, new in changed:
    print(f"P{i} CHANGED")
    print("OLD:", old)
    print("NEW:", new)
    print("-" * 80)
