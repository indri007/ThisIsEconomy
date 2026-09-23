from docx import Document

src = "HMC_REVIEW_MANUSCRIPT_V21.docx"
out = "HMC_REVIEW_MANUSCRIPT_V22.docx"

doc = Document(src)
changed = []

replacements = {
    "communicatedexpectations": "communicated expectations",
    "GovernanceGap": "Governance Gap",
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

print("HMC V22 CREATED")
print("=" * 100)
print("INPUT :", src)
print("OUTPUT:", out)
print("CHANGED PARAGRAPHS:", len(changed))

for i, old, new in changed:
    print(f"\nP{i} CHANGED")
    print("OLD:", old)
    print("NEW:", new)
