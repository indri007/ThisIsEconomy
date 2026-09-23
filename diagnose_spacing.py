from docx import Document
import re

p = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT.docx"
doc = Document(p)

patterns = [
    r"[a-z][A-Z]",
    r",(?=[A-Za-z])",
    r"\.[A-Z]",
    r"\b(?:The|This|In|of|and|or|to|with|from|for|on|as|that|which|across|within|into|between|while|but|rather|than)[a-zA-Z]+",
]

print("=" * 80)
print("SPACING / TYPO DIAGNOSTIC")
print("=" * 80)

count = 0

for i, para in enumerate(doc.paragraphs, 1):
    text = para.text.strip()

    if not text:
        continue

    hits = []

    if re.search(r"[a-z][A-Z]", text):
        hits.append("missing-space camel boundary")

    if re.search(r",[A-Za-z]", text):
        hits.append("missing space after comma")

    if re.search(r"\.[A-Z]", text):
        hits.append("missing space after period")

    if hits:
        print(f"\nParagraph {i}")
        print("ISSUE:", ", ".join(hits))
        print("TEXT :", text[:500])
        count += 1

print("\n" + "=" * 80)
print("PARAGRAPHS WITH POSSIBLE SPACING ISSUES:", count)
print("=" * 80)
