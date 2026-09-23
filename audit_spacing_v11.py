from docx import Document
import re

p = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V11.docx"
doc = Document(p)

patterns = [
    (r"[a-zA-Z]{2,}(?:are|is|of|by|the|and|in|to|on|for|with)[a-zA-Z]{2,}",
     "possible missing space"),
    (r"[a-zA-Z]{2,},[a-zA-Z]{2,}",
     "missing space after comma"),
    (r"[.!?][A-Za-z]{2,}",
     "missing space after punctuation"),
    (r"\)[A-Za-z]{2,}",
     "missing space after closing parenthesis"),
    (r"[A-Za-z]{2,}\([A-Za-z]{2,}",
     "possible missing space before parenthesis"),
]

print("=" * 80)
print("HMC V11 SPACING AUDIT")
print("=" * 80)

count = 0

for i, para in enumerate(doc.paragraphs, 1):
    text = para.text

    for pattern, label in patterns:
        matches = list(re.finditer(pattern, text))

        for m in matches:
            snippet = text[max(0, m.start()-45):min(len(text), m.end()+45)]
            print(f"P{i} | {label}")
            print("   ", snippet)
            print()
            count += 1

print("=" * 80)
print("POSSIBLE ISSUES:", count)
print("=" * 80)
