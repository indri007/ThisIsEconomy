from docx import Document

src = "HMC_REVIEW_MANUSCRIPT_V22.docx"
out = "HMC_REVIEW_MANUSCRIPT_V23.docx"

doc = Document(src)

replacements = {
    "Public SectorGovernance": "Public Sector Governance",
    "Data andCode Availability": "Data and Code Availability",
}

changed = []

for i, p in enumerate(doc.paragraphs, 1):
    old = p.text
    new = old

    for a, b in replacements.items():
        new = new.replace(a, b)

    if new != old:
        p.text = new
        changed.append((i, old, new))

doc.save(out)

print("=" * 100)
print("HMC V23 CREATED")
print("=" * 100)
print("INPUT :", src)
print("OUTPUT:", out)
print("CHANGED PARAGRAPHS:", len(changed))

for i, old, new in changed:
    print(f"\nP{i} CHANGED")
    print("OLD:", old)
    print("NEW:", new)
