from docx import Document
import re

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V19.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V20.docx"

doc = Document(src)
changed = []

for i, p in enumerate(doc.paragraphs, 1):
    old = p.text
    new = old

    # Exact spacing repairs
    new = new.replace("account,his", "account, his")
    new = new.replace("thecommunicative", "the communicative")
    new = new.replace("theobserved", "the observed")

    # Repair malformed LaTeX caused by earlier DOCX text replacement
    new = re.sub(
        r'C_\{\s*ext\{in\}\}',
        r'C_{\\text{in}}',
        new
    )

    new = re.sub(
        r'C_\{\s*ext\{out\}\}',
        r'C_{\\text{out}}',
        new
    )

    if new != old:
        p.text = new
        changed.append((i, old, new))

doc.save(out)

print("HMC V20 CREATED")
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
