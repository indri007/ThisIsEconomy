from docx import Document

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V4.docx"

doc = Document(src)

old_phrase = "historic paradigm shift"

new_paragraph = """When state actors provide limited responses to operational queries, some users may redirect information-seeking activities toward AI-mediated accounts. In the observed network, users tagged @grok in attempts to verify contract values, calculate vendor margins, and cross-reference nutritional standards. The AI agent therefore occupied a distinct information-seeking position within the observed interaction network. This pattern is relevant to human-machine communication because an AI-mediated account can become part of the communicative infrastructure through which users seek, interpret, and validate policy-related information. Rather than establishing a historical paradigm shift, the finding provides an empirical instance of how algorithmic actors may participate in public-policy discourse alongside human institutional and non-institutional actors."""

changed = False

for para in doc.paragraphs:
    if old_phrase.lower() in para.text.lower():
        for run in para.runs:
            run.text = ""
        if para.runs:
            para.runs[0].text = new_paragraph
        else:
            para.add_run(new_paragraph)
        changed = True
        print("Paragraph 169 updated.")

if not changed:
    raise RuntimeError("Target phrase not found.")

doc.save(out)

print("OUTPUT:", out)
