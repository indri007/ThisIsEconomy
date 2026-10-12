#!/usr/bin/env python3
"""
Revisi klaim validasi (12 Okt 2026) pada manuskrip ICS (Taylor & Francis) dan
JCMC (Oxford): menghapus klaim reliabilitas antarpenilai / gold standard yang
dihasilkan oleh label skrip, membatasi klaim ke 6 kelas emosi aktif, dan
menyatakan bahwa label acuan adalah silver-standard. Mengubah .md dan .docx.
Skrip ini idempoten: gagal keras bila teks sumber tidak ditemukan.
"""
import copy
import sys
from pathlib import Path

import docx

MS = Path(__file__).resolve().parent.parent / "manuscript"

# ───────────────────────── teks pengganti ─────────────────────────
LABELS_NOTE = ("The classification head was configured with nine output labels derived from Ekman (1992) and "
               "Plutchik (1980); however, only six of these classes occur in the labelled corpus (Joy and Surprise "
               "have no samples, and Fear has two samples and none in the test set), so all performance claims are "
               "restricted to the six active classes. Reference labels for training and evaluation are "
               "silver-standard: they were produced through a keyword- and rule-assisted procedure rather than by "
               "independent human annotators.")

REF_STATUS_BODY = ("All reported metrics are computed against silver-standard labels produced by a keyword- and "
                   "rule-assisted procedure. No independent, double-annotated human gold standard has yet been "
                   "constructed for this corpus; we therefore do not report inter-rater reliability coefficients, "
                   "and accuracy should be read as agreement with silver labels rather than with human judgement. "
                   "Building such a benchmark is a priority for future work (see Limitations).")

SARCASM_BODY = ("Qualitative inspection of sampled posts shows cases in which keyword-based silver labels assign "
                "positive emotions to sarcastic posts because of literal laudatory words (terima kasih, mantap, "
                "mewah), whereas IndoBERT predicts Disgust, in line with paralinguistic emoji inversions "
                "(e.g., 🤡, 🤮, 🤣). These examples are illustrative and have not been verified through systematic "
                "human annotation.")

ICS_MINORITY_OLD = ("revealed that 12 of the 14 Anger posts were non-Indonesian noise/spam correctly filtered by "
                    "IndoBERT as Neutral, while Sadness posts reflected")
ICS_MINORITY_NEW = ("revealed that 12 of the 14 Anger-labelled posts were non-Indonesian noise or spam that IndoBERT "
                    "predicted as Neutral (indicating silver-label noise; these predictions are still counted as "
                    "errors), while Sadness posts reflected")
ROBUST_OLD_ICS = "proving the structural robustness of its contextual representations."
ROBUST_NEW = ("suggesting that the model captures coarse affective valence more reliably than granular emotion "
              "categories; because this three-tier grouping was defined after the granular evaluation, it is "
              "reported as a supplementary, post-hoc analysis.")

LIMIT4_TITLE = "4. Silver-Standard Emotion Labels"
LIMIT4_BODY = (": Emotion labels are silver-standard and have not yet been validated against an independent, "
               "double-annotated human benchmark. Macro-F1 on the six active classes remains modest (0.4535), the "
               "model does not recognise Anger or Sadness (F1 = 0.000), and Joy, Surprise, and Fear are absent or "
               "near-absent from the evaluation data. Future work should construct a human-annotated benchmark with "
               "reported inter-rater reliability (Cohen's kappa, Krippendorff's alpha) before granular emotion "
               "proportions are interpreted as population-level estimates.")

DATA_OLD = "multi-annotator gold-standard adjudicated corpora,"
DATA_NEW = "silver-standard labelled corpora,"

JCMC_33_TITLE_OLD = "3.3 Multi-Annotator Inter-Rater Reliability Gold Standard Protocol"
JCMC_33_TITLE_NEW = "3.3 Reference-Label Status and Validation Scope"
JCMC_33_BODY_START = "To rigorously validate model classification against human ground truth"
JCMC_33_BODY_NEW = REF_STATUS_BODY

JCMC_32_ANCHOR = "with a mean softmax confidence of 95.01% (median: 96.95%)."
JCMC_MIN_OLD = "consisted of multi-lingual noise (Catalan, Turkish, Spanish spam) correctly filtered as Neutral by IndoBERT,"
JCMC_MIN_NEW = ("consisted of multi-lingual noise (Catalan, Turkish, Spanish spam) that IndoBERT predicted as Neutral "
                "(indicating silver-label noise; these predictions are still counted as errors),")
JCMC_ROBUST_OLD = "demonstrating the profound robustness of its contextual representations."
JCMC_CONC_OLD = "multi-annotator gold standard validation (Fleiss' κ = 0.8442, Krippendorff's α = 0.8447),"
JCMC_CONC_NEW = "holdout evaluation against silver-standard labels (accuracy 75.99%, macro-F1 0.4535),"
JCMC_LIM_OLD = ("Third, while our multi-annotator protocol demonstrated high reliability (Fleiss' κ = 0.8442), future "
                "investigations should expand multi-annotator benchmarking across multi-thousand-sample corpora and deploy")
JCMC_LIM_NEW = ("Third, emotion labels are silver-standard and have not yet been validated against an independent, "
                "double-annotated human benchmark; macro-F1 on the six active classes remains modest (0.4535), Anger "
                "and Sadness are not recognised (F1 = 0.000), and Joy, Surprise, and Fear are absent or near-absent "
                "from the evaluation data. Future investigations should construct a human-annotated benchmark with "
                "reported inter-rater reliability and deploy")

JCMC_T3_CAPTION_OLD = "Multi-Annotator Inter-Rater Reliability and IndoBERT Gold Validation Benchmark (n = 100)"
JCMC_T3_CAPTION_NEW = "Emotion Classification Validation Scope (Group-Aware Holdout, n = 1,058)"
JCMC_T3_ROWS = [
    ("Reference labels", "Silver-standard", "—", "Keyword/rule-assisted; not human-adjudicated"),
    ("Independent human gold standard", "Not yet constructed", "—", "Inter-rater reliability not reported"),
    ("Active emotion classes (test set)", "6 of 9 output labels", "—", "Joy and Surprise absent; Fear absent from test set"),
    ("Accuracy vs silver labels", "75.99%", "—", "Agreement with silver labels, not human judgement"),
    ("Macro-F1 / Weighted-F1", "0.4535 / 0.7434", "—", "Unweighted mean across the 6 active classes"),
    ("Minority-class F1 (Anger, Sadness)", "0.000 / 0.000", "—", "Model does not recognise these classes"),
]

ICS_T2_ROWS = [  # replaces rows 6..9 of Table 2
    ("Reference Labels", "Silver-standard", "Keyword/rule-assisted; not human-adjudicated"),
    ("Independent Human Gold Standard", "Not yet constructed", "Inter-rater reliability not reported"),
    ("Active Emotion Classes (test set)", "6 of 9 output labels", "Joy and Surprise absent; Fear absent from test set"),
    ("Minority-Class F1 (Anger, Sadness)", "0.000 / 0.000", "Model does not recognise these classes"),
]
ICS_F1_INTERP_OLD = "Balanced multi-class F1 metric across 6 emotion classes"
ICS_F1_INTERP_NEW = "Unweighted mean F1 across the 6 active emotion classes"


# ───────────────────────── helper ─────────────────────────
def must_replace(text, old, new, where):
    if old not in text:
        sys.exit(f"[STOP] teks tidak ditemukan di {where}: {old[:70]!r}")
    return text.replace(old, new)


def set_par(p, segments):
    """segments: list of (text, bold). Keeps the font of the first run."""
    base = p.runs[0] if p.runs else None
    for r in list(p.runs)[1:]:
        r._r.getparent().remove(r._r)
    if base is None:
        base = p.add_run("")
    base.text = segments[0][0]
    base.bold = segments[0][1]
    for txt, bold in segments[1:]:
        nr = copy.deepcopy(base._r)
        p._p.append(nr)
        run = p.runs[-1]
        run.text = txt
        run.bold = bold


def set_cell(cell, text):
    p = cell.paragraphs[0]
    set_par(p, [(text, p.runs[0].bold if p.runs else False)])


def find_par(d, needle):
    for p in d.paragraphs:
        if needle in p.text:
            return p
    sys.exit(f"[STOP] paragraf tidak ditemukan: {needle[:70]!r}")


# ───────────────────────── ICS ─────────────────────────
def ics_md():
    f = MS / "ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.md"
    t = f.read_text(encoding="utf-8")
    t = must_replace(t, "The model was trained to classify 9 granular affective states (Ekman, 1992; Plutchik, 1980) and detect sarcasm via text-emoji incongruence.",
                     "The model was also used to flag sarcasm via text-emoji incongruence. " + LABELS_NOTE, "ICS md 3.2")
    t = must_replace(t, ICS_F1_INTERP_OLD, ICS_F1_INTERP_NEW, "ICS md T2")
    lines = t.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("| **Inter-Human Reliability"))
    assert lines[start + 3].startswith("| **IndoBERT vs Gold Consensus Accuracy")
    lines[start:start + 4] = [f"| **{a}** | **{b}** | {c} |" for a, b, c in ICS_T2_ROWS]
    t = "\n".join(lines)
    i2 = t.index("2. **Multi-Annotator Inter-Rater Reliability ($n = 100$)**")
    i3 = t.index("3. **Disambiguation of Sarcasm**")
    i4 = t.index("4. **Hierarchical Taxonomy")
    t = (t[:i2] + "2. **Reference-Label Status ($n = 1,058$)**: " + REF_STATUS_BODY + "\n"
         + "3. **Illustrative Sarcasm Cases**: " + SARCASM_BODY + "\n" + t[i4:])
    t = must_replace(t, ICS_MINORITY_OLD, ICS_MINORITY_NEW, "ICS md 4.2(4)")
    t = must_replace(t, ROBUST_OLD_ICS, ROBUST_NEW, "ICS md 4.2(4)")
    t = must_replace(t, "three foundational ecological boundary conditions must be specified:",
                     "four foundational boundary conditions must be specified:", "ICS md 6.1")
    anchor = "Shorts.\n"
    k = t.index("3. **Cross-Platform Multi-Modal Trajectory**")
    k_end = t.index("\n", k) + 1
    t = t[:k_end] + f"4. **Silver-Standard Emotion Labels**{LIMIT4_BODY}\n" + t[k_end:]
    t = must_replace(t, DATA_OLD, DATA_NEW, "ICS md data availability")
    f.write_text(t, encoding="utf-8")


def ics_docx():
    f = MS / "ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx"
    d = docx.Document(str(f))
    p = find_par(d, "The model was trained to classify 9 granular affective states")
    txt = p.text.replace("The model was trained to classify 9 granular affective states (Ekman, 1992; Plutchik, 1980) and detect sarcasm via text-emoji incongruence.",
                         "The model was also used to flag sarcasm via text-emoji incongruence. " + LABELS_NOTE)
    set_par(p, [(txt, False)])
    tbl = d.tables[1]
    for r in tbl.rows:
        if r.cells[0].text.startswith("Holdout Macro / Weighted F1"):
            set_cell(r.cells[2], ICS_F1_INTERP_NEW)
    rows = [r for r in tbl.rows if r.cells[0].text.startswith(("Inter-Human Reliability", "Multi-Rater Fleiss", "Krippendorff's Alpha", "IndoBERT vs Gold"))]
    assert len(rows) == 4, len(rows)
    for r, vals in zip(rows, ICS_T2_ROWS):
        for c, v in zip(r.cells, vals):
            set_cell(c, v)
    set_par(find_par(d, "2. Multi-Annotator Inter-Rater Reliability"),
            [("2. Reference-Label Status (n = 1,058)", True), (": " + REF_STATUS_BODY, False)])
    set_par(find_par(d, "3. Disambiguation of Sarcasm"),
            [("3. Illustrative Sarcasm Cases", True), (": " + SARCASM_BODY, False)])
    p = find_par(d, "4. Hierarchical Taxonomy & Minority Error Dissection")
    txt = p.text.replace(ICS_MINORITY_OLD, ICS_MINORITY_NEW).replace(ROBUST_OLD_ICS, ROBUST_NEW)
    head = "4. Hierarchical Taxonomy & Minority Error Dissection"
    set_par(p, [(head, True), (txt[len(head):], False)])
    p = find_par(d, "three foundational ecological boundary conditions")
    set_par(p, [(p.text.replace("three foundational ecological boundary conditions must be specified:",
                                "four foundational boundary conditions must be specified:"), False)])
    p3 = find_par(d, "3. Cross-Platform Multi-Modal Trajectory")
    new = copy.deepcopy(p3._p)
    p3._p.addnext(new)
    p4 = docx.text.paragraph.Paragraph(new, p3._parent)
    set_par(p4, [(LIMIT4_TITLE, True), (LIMIT4_BODY, False)])
    p = find_par(d, DATA_OLD)
    lead = "Data Availability Statement"
    set_par(p, [(lead, True), (p.text[len(lead):].replace(DATA_OLD, DATA_NEW), False)])
    d.save(str(f))


# ───────────────────────── JCMC ─────────────────────────
def jcmc_md():
    f = MS / "JCMC_OXFORD_MBG_COMMUNICATION_2026.md"
    t = f.read_text(encoding="utf-8")
    t = must_replace(t, JCMC_32_ANCHOR, JCMC_32_ANCHOR + " " + LABELS_NOTE, "JCMC md 3.2")
    t = must_replace(t, JCMC_33_TITLE_OLD, JCMC_33_TITLE_NEW, "JCMC md 3.3 title")
    s = t.index(JCMC_33_BODY_START)
    e = t.index("\n", s)
    t = t[:s] + JCMC_33_BODY_NEW + t[e:]
    t = must_replace(t, JCMC_MIN_OLD, JCMC_MIN_NEW, "JCMC md 4.5")
    t = must_replace(t, JCMC_ROBUST_OLD, ROBUST_NEW, "JCMC md 4.5")
    t = must_replace(t, JCMC_CONC_OLD, JCMC_CONC_NEW, "JCMC md 6")
    t = must_replace(t, JCMC_LIM_OLD, JCMC_LIM_NEW, "JCMC md 6 limitations")
    t = must_replace(t, DATA_OLD, DATA_NEW, "JCMC md data availability")
    t = must_replace(t, JCMC_T3_CAPTION_OLD, JCMC_T3_CAPTION_NEW, "JCMC md T3 caption")
    s = t.index("Inter-Human Agreement (H1 vs H2)")
    e = t.index("Strong classification reliability on authentic citizen discourse") + len("Strong classification reliability on authentic citizen discourse")
    block = "\n\n".join("\n\n".join(r) for r in JCMC_T3_ROWS)
    t = t[:s] + block + t[e:]
    f.write_text(t, encoding="utf-8")


def jcmc_docx():
    f = MS / "JCMC_OXFORD_MBG_COMMUNICATION_2026.docx"
    d = docx.Document(str(f))
    p = find_par(d, JCMC_32_ANCHOR)
    set_par(p, [(p.text + " " + LABELS_NOTE, False)])
    p = find_par(d, JCMC_33_TITLE_OLD)
    set_par(p, [(JCMC_33_TITLE_NEW, p.runs[0].bold)])
    set_par(find_par(d, JCMC_33_BODY_START), [(JCMC_33_BODY_NEW, False)])
    p = find_par(d, JCMC_MIN_OLD)
    set_par(p, [(p.text.replace(JCMC_MIN_OLD, JCMC_MIN_NEW).replace(JCMC_ROBUST_OLD, ROBUST_NEW), False)])
    p = find_par(d, JCMC_CONC_OLD)
    set_par(p, [(p.text.replace(JCMC_CONC_OLD, JCMC_CONC_NEW), False)])
    p = find_par(d, JCMC_LIM_OLD[:60])
    set_par(p, [(p.text.replace(JCMC_LIM_OLD, JCMC_LIM_NEW), False)])
    assert JCMC_LIM_NEW[:40] in p.text
    p = find_par(d, DATA_OLD)
    set_par(p, [(p.text.replace(DATA_OLD, DATA_NEW), False)])
    p = find_par(d, JCMC_T3_CAPTION_OLD)
    for r in p.runs:
        r.text = r.text.replace(JCMC_T3_CAPTION_OLD, JCMC_T3_CAPTION_NEW)
    assert JCMC_T3_CAPTION_NEW in p.text
    tbl = next(t for t in d.tables if t.rows[1].cells[0].text.startswith("Inter-Human Agreement"))
    assert len(tbl.rows) == 7
    for r, vals in zip(tbl.rows[1:], JCMC_T3_ROWS):
        for c, v in zip(r.cells, vals):
            set_cell(c, v)
    d.save(str(f))


if __name__ == "__main__":
    ics_md(); ics_docx(); jcmc_md(); jcmc_docx()
    print("[OK] ICS & JCMC manuscripts revised (.md + .docx)")
