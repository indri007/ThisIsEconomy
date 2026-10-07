from docx import Document

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V18.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V19.docx"

doc = Document(src)
changed = []

replacements = {
    "thispattern": "this pattern",
    "byrecorded": "by recorded",
    "inthe observed": "in the observed",
    "crisiscommunication": "crisis communication",
    "verifiedinvestigative": "verified investigative",
    "network,however": "network, however",
    "involvinginstitutional": "involving institutional",
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

print("HMC V19 CREATED")
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
