from docx import Document
import re

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V14.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V15.docx"

doc = Document(src)
changed = []

for i, p in enumerate(doc.paragraphs, 1):
    old = p.text
    new = old

    # Fix malformed LaTeX C_out regardless of number of spaces
    new = re.sub(
        r'C_\{\s*ext\{out\}\}',
        r'C_{\\text{out}}',
        new
    )

    if new != old:
        p.text = new
        changed.append((i, old, new))

doc.save(out)

print("HMC V15 CREATED")
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
