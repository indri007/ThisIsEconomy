from docx import Document

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V16.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V17.docx"

doc = Document(src)
changed = []

replacements = {
    "facts.The": "facts. The",
    "crisiscommunication": "crisis communication",
    "capability,while": "capability, while",
    "conductedindependently": "conducted independently",
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

print("HMC V17 CREATED")
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
