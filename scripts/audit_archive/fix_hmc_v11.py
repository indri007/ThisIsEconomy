from docx import Document
from pathlib import Path

src = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V10.docx")
out = Path("/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V11.docx")

doc = Document(str(src))

# Exact spacing repairs identified in V10
replacements = {
    "aspect-basedsentiment": "aspect-based sentiment",
    "adedicated": "a dedicated",
    "incongruenceindicators": "incongruence indicators",
    "amodularity": "a modularity",
    "categories.The": "categories. The",
    "networkstructure": "network structure",
    "policiesare": "policies are",
    "instead,policies": "instead, policies",
    "millionsof": "millions of",
    "thisdynamic": "this dynamic",
    "Meal(Makan": "Meal (Makan",
    "civicdissent": "civic dissent",
    "publicsentiment": "public sentiment",
    "linguisticchallenges": "linguistic challenges",
    "humor,dark": "humor, dark",
    "hours of a policy's physical rollout": "hours of a policy's physical rollout",
}

changed = 0

for para in doc.paragraphs:
    old_text = para.text
    new_text = old_text

    for old, new in replacements.items():
        new_text = new_text.replace(old, new)

    if new_text != old_text:
        # Preserve paragraph formatting while replacing runs safely.
        # Rebuild paragraph text in a single run.
        for run in para.runs:
            run.text = ""

        if para.runs:
            para.runs[0].text = new_text
        else:
            para.add_run(new_text)

        changed += 1

# Remove separator-only paragraphs.
removed = 0

for para in list(doc.paragraphs):
    if para.text.strip() == "---":
        parent = para._element.getparent()
        parent.remove(para._element)
        removed += 1

doc.save(str(out))

print("=" * 70)
print("HMC V11 CREATED")
print("=" * 70)
print("INPUT :", src)
print("OUTPUT:", out)
print("CHANGED PARAGRAPHS:", changed)
print("REMOVED SEPARATORS:", removed)
print("=" * 70)
