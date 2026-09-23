from docx import Document
import re

p = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT.docx"
doc = Document(p)

# Kata yang secara umum sering muncul sebagai bagian dari kalimat.
# Hanya digunakan untuk diagnosis, BUKAN auto-fix.
words = [
    "the", "this", "that", "study", "raw", "network",
    "substantial", "platform", "policies", "instead",
    "millions", "dynamic", "marketing", "studies",
    "state", "artificial", "intelligence", "communication",
    "nutritious", "meal", "public", "digital",
    "social", "model", "data", "results", "research"
]

print("=" * 80)
print("PRECISE SPACING CHECK")
print("=" * 80)

count = 0

for i, para in enumerate(doc.paragraphs, 1):
    text = para.text

    for word in words:
        # contoh: Thestudy / rawposts / networkcontained
        pattern = rf"(?i)\b{word}[a-z]+\b"

        for m in re.finditer(pattern, text):
            token = m.group(0)

            # Hindari kata normal yang memang merupakan kata lengkap.
            if token.lower() == word.lower():
                continue

            # Tampilkan hanya token yang cukup mencurigakan.
            if len(token) > len(word) + 2:
                print(f"\nParagraph {i}")
                print("Possible token:", token)
                print("Context:", text[max(0,m.start()-70):m.end()+70])
                count += 1
                break

print("\n" + "=" * 80)
print("POSSIBLE ISSUES:", count)
print("=" * 80)
