from docx import Document

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V5.docx"

doc = Document(src)

replacements = {
    "NutritiousMeal": "Nutritious Meal",
    "Thestudy": "The study",
    "rawposts": "raw posts",
    "networkcontained": "network contained",
    "substantialclass": "substantial class",
    "PlatformX": "Platform X",
    "policiesare": "policies are",
    "instead,policies": "instead, policies",
    "millionsof": "millions of",
    "thisdynamic": "this dynamic",
    "marketingand": "marketing and",
    "studiesthat": "studies that",
    "statesurveillance": "state surveillance",
    "artificial intelligenceagents": "artificial intelligence agents",

    "NetworkAnalysis": "Network Analysis",
    "meso-thematicdecomposition": "meso-thematic decomposition",
    "SituationalCrisis Communication": "Situational Crisis Communication",
    "According toClark": "According to Clark",
    "modeling(indobert_9_emosi_fixed.csv": "modeling (indobert_9_emosi_fixed.csv",
    "SentimentAnalysis": "Sentiment Analysis",
    "theoriesof": "theories of",
    "Journalof": "Journal of",
    "dataset.In": "dataset. In",
    "411–426.https://": "411–426. https://",
    "241–248).https://": "241–248). https://",
    "770).https://": "770). https://",
    "wikis": "wikis",
}

changed = 0

for para in doc.paragraphs:
    original = para.text
    updated = original

    for old, new in replacements.items():
        updated = updated.replace(old, new)

    if updated != original:
        # Preserve paragraph formatting while replacing text.
        if para.runs:
            para.runs[0].text = updated
            for run in para.runs[1:]:
                run.text = ""
        else:
            para.add_run(updated)

        changed += 1

print("CHANGED PARAGRAPHS:", changed)

doc.save(out)

print("OUTPUT:", out)
