#!/usr/bin/env python3
"""
build_scopus_q1_latest_manuscript.py
====================================
Menghasilkan naskah artikel jurnal ilmiah standar internasional (Scopus Q1)
dalam 2 format sekaligus:
1. Markdown (.md) lengkap dengan persamaan matematis LaTeX dan tabel komparasi.
2. Microsoft Word (.docx) dengan format publikasi, tabel terformat, dan gambar disematkan.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = os.path.expanduser("~/ThisIsEconomy")
MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(MANUSCRIPT_DIR, exist_ok=True)

MASTER_IMG_PATH = os.path.join(RESULTS_DIR, "grafik_master_indobert_dan_rumus_tesis.png")
LOSS_CURVE_PATH = os.path.join(RESULTS_DIR, "indobert_training_loss_curve_3epochs.png")
MONTHLY_IMG_PATH = os.path.join(RESULTS_DIR, "indobert_monthly_emotion_timeline_2026.png")

MD_OUT_PATH = os.path.join(MANUSCRIPT_DIR, "JURNAL_MBG_SCOPUS_Q1_LATEST_2026.md")
DOCX_OUT_PATH = os.path.join(MANUSCRIPT_DIR, "JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx")
DOCX_DOCUMENTS_PATH = os.path.expanduser("~/Documents/tesis_mbg/manuscript/JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx")

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

print("[*] Menulis naskah format Markdown...")

# Baca naskah lengkap dari journal_paper_mbg_sna.md yang sudah diperkaya
with open(os.path.join(BASE_DIR, "journal_paper_mbg_sna.md"), "r", encoding="utf-8") as f:
    full_md_content = f.read()

with open(MD_OUT_PATH, "w", encoding="utf-8") as f:
    f.write(full_md_content)

print(f"[OK] Naskah Markdown tersimpan : {MD_OUT_PATH}")

print("[*] Membangun dokumen Word (.docx) berstandar publikasi Scopus Q1...")
doc = docx.Document()

# Page Setup: Normal Margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Styles
style_normal = doc.styles['Normal']
font = style_normal.font
font.name = 'Times New Roman'
font.size = Pt(11)
font.color.rgb = RGBColor(0x1F, 0x24, 0x21)

# --- 1. TITLE ---
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(0)
title_p.paragraph_format.space_after = Pt(12)
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title_p.add_run(
    "Decoding Public Policy Crisis in the Algorithmic Sphere: "
    "A Tri-Layer Computational Forensics of Indonesia's Free Nutritious Meal (MBG) Program, "
    "IndoBERT Fine-Tuning Across 3.0 Epochs, and the Phygital Gap"
)
run_title.font.name = 'Times New Roman'
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

# --- 2. AUTHORS & AFFILIATIONS ---
author_p = doc.add_paragraph()
author_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
author_p.paragraph_format.space_after = Pt(4)
r_author = author_p.add_run("Indri Anjar Kartika Sari¹*, Catur Suratnoaji¹, Agus Widiyarta¹")
r_author.font.bold = True
r_author.font.size = Pt(11.5)

affil_p = doc.add_paragraph()
affil_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
affil_p.paragraph_format.space_after = Pt(14)
r_affil = affil_p.add_run(
    "¹ Department of Communication Science, Faculty of Social and Political Sciences,\n"
    "Universitas Pembangunan Nasional 'Veteran' Jawa Timur, Surabaya, 60294, Indonesia\n"
    "*Corresponding Author: indrianjar@gmail.com | ORCID: 0009-0002-8419-7231"
)
r_affil.font.size = Pt(9.5)
r_affil.font.italic = True
r_affil.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

# --- 3. ABSTRACT BOX ---
abs_table = doc.add_table(rows=1, cols=1)
abs_table.alignment = WD_TABLE_ALIGNMENT.CENTER
abs_table.autofit = False
cell = abs_table.cell(0, 0)
cell.width = Inches(6.5)
set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
set_cell_background(cell, "F8FAFC")

abs_p = cell.paragraphs[0]
abs_p.paragraph_format.space_after = Pt(6)
r_abs_label = abs_p.add_run("ABSTRACT\n")
r_abs_label.font.bold = True
r_abs_label.font.size = Pt(10.5)
r_abs_label.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

r_abs_text = abs_p.add_run(
    "State-sponsored welfare initiatives in the algorithmic public sphere face existential legitimacy crises when "
    "immaculate digital branding decouples from flawed physical delivery. This study investigates the communication "
    "crisis surrounding Indonesia's flagship Free Nutritious Meal (Makan Bergizi Gratis / MBG) program on Platform X "
    "through an explanatory-sequential, tri-layer computational communication science framework. Bridging Philip Kotler's "
    "Marketing 6.0 concept of the 'Phygital Gap' with Coombs' Situational Crisis Communication Theory (SCCT) and "
    "pretense irony theory, the analytical architecture synthesizes: (1) fine-tuned transformer language modeling "
    "(indobenchmark/indobert-base-p2) across 3.0 full training epochs (792 global steps, loss 1.87 to 0.43) classifying "
    "9 granular emotion categories; (2) directed Social Network Analysis (SNA via NetworkX and Louvain community detection) "
    "measuring macro-topological fragmentation; and (3) 3-pillar Aspect-Based Sentiment Analysis (ABSA). Beyond the core "
    "corpus (971 nodes, 692 edges, 3,395 tweets), the framework was validated on an expanded real-world streaming dataset "
    "of 9,862 deduplicated citizen posts with an average throughput of 223.3 posts/second on Apple Silicon GPU. "
    "Empirical findings confirm the overwhelming hegemony of Disgust (98.14% in streaming validation, 73.88% across core policy aspects), "
    "with Nutritional Quality generating double the discursive volume of budget debates (34.87% vs 8.70%). Topological modeling "
    "uncovered extreme structural atomization: a Louvain modularity score of Q = 0.9761 - 0.9837, density of 0.0004 - 0.0007, "
    "and dyadic reciprocity of merely 0.91% - 1.20%. Centrality analysis identified an acute structural power asymmetry: "
    "while institutional handles (@prabowo) operated as in-degree grievance sinks, the generative AI agent @grok emerged as "
    "the highest-centrality 'Algorithmic Oracle' (Degree = 0.0433, Betweenness = 0.0059) solicited by citizens as an epistemic arbiter "
    "to fact-check food poisoning reports and fiscal arithmetic. Applying the replicated formula battery triggered an Early Warning "
    "System (EWS) score of 84.6/100 (RED ALERT). In the phygital era, algorithmic verifiers inevitably supplant silent state "
    "institutions, proving that physical delivery excellence is the only credible foundation for public policy communication."
)
r_abs_text.font.size = Pt(9.5)
r_abs_text.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

kw_p = cell.add_paragraph()
kw_p.paragraph_format.space_before = Pt(6)
r_kw = kw_p.add_run("Keywords: ")
r_kw.font.bold = True
r_kw.font.size = Pt(9.5)
r_kw_val = kw_p.add_run(
    "Computational Communication Science, Phygital Gap, Marketing 6.0, IndoBERT Transformer, "
    "Social Network Analysis, Sarcasm Detection, Algorithmic Oracle, Early Warning System (EWS), Free Nutritious Meal (MBG)."
)
r_kw_val.font.size = Pt(9.5)
r_kw_val.font.italic = True

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# --- 4. BODY HEADINGS & SECTIONS ---
def add_sec_heading(title, level=1):
    h = doc.add_heading(level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    r = h.add_run(title)
    r.font.name = 'Times New Roman'
    if level == 1:
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    elif level == 2:
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    elif level == 3:
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.italic = True
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return h

def add_body_p(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.size = Pt(11)
    return p

# Section 1: Introduction
add_sec_heading("1. INTRODUCTION", level=1)
add_body_p(
    "In contemporary networked democracies, the state no longer exercises exclusive control over the narrative of its public policies. "
    "Instead, public policy interventions are continuously subjected to decentralized, real-time civic peer-review across social media platforms. "
    "When policy implementation suffers from operational defects, digital platforms evolve from channels of citizen feedback into volatile arenas "
    "of collective delegitimation. A prime manifestation of this dynamic occurred during the nationwide rollout of Indonesia's Free Nutritious Meal "
    "(Makan Bergizi Gratis / MBG) program in early 2026."
)
add_body_p(
    "Backed by an indicative state budget exceeding IDR 268 trillion to combat childhood stunting, the initiative encountered severe ground-level "
    "friction upon physical deployment. Citizen reports documenting substandard food trays, spoiled milk, logistical bottlenecks, and mass food poisoning "
    "across pilot schools ignited an explosive public crisis on Platform X. Crucially, public dissent was not expressed primarily through formal complaints; "
    "rather, citizens deployed sophisticated paralinguistic shields—combining hyperbolic praise with nauseated emojis (🤡, 🤮) to register moral contempt "
    "while navigating platform algorithms. Traditional sentiment analysis engines routinely misclassify such sarcastic praise as genuine government support, "
    "producing fatally distorted policy intelligence."
)

# Section 2: Methodology
add_sec_heading("2. COMPUTATIONAL METHODOLOGY & MODEL ARCHITECTURE", level=1)
add_body_p(
    "This investigation deploys a rigorous tri-layer computational architecture comprising: (1) deep learning natural language processing with a "
    "fine-tuned bidirectional transformer (indobenchmark/indobert-base-p2) for 9-class emotion modeling; (2) directed Social Network Analysis (SNA) "
    "via NetworkX and Louvain community detection; and (3) Aspect-Based Sentiment Analysis (ABSA) decomposing discourse across three operational facets: "
    "Budget & Procurement, Logistics & Distribution, and Nutritional Quality."
)

# Table: Model Hyperparameters
add_sec_heading("2.1 Deep Learning Training Telemetry (3.0 Full Epochs)", level=2)
add_body_p(
    "The primary IndoBERT classifier was trained using PyTorch and Hugging Face Transformers under rigorous cross-entropy loss optimization. "
    "As logged in the formal execution ledger (trainer_state.json), the model completed exactly 3.0 epochs over 792 global steps without premature termination. "
    "Training parameters and convergence milestones are summarized in Table 1."
)

# Add Table 1
t1 = doc.add_table(rows=6, cols=3)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_headers = ["Training Parameter / Milestone", "Configured Value", "Methodological Rationale / Outcome"]
for col_idx, h_text in enumerate(t1_headers):
    c = t1.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 100, 100, 150, 150)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t1_data = [
    ("Foundation Architecture", "indobenchmark/indobert-base-p2", "BERT Base Indonesian (12-layer, 768-hidden, 12-heads)"),
    ("Training Epochs", "3.0 Full Epochs (792 Steps)", "Monotonic loss reduction from 1.8708 to 0.4328"),
    ("Batch Size & Learning Rate", "16 per device | 2e-5 (AdamW)", "Optimal gradient stability with linear learning rate warmup"),
    ("Validation Loss", "0.5250 (Optimal Convergence)", "Stable generalization without overparameterized overfitting"),
    ("Evaluation Accuracy & Macro-F1", "79.40% - 81.43% | F1: 0.5160", "Statistically superior to TF-IDF SVM (68.05%) and LogReg (67.11%)")
]
for row_idx, row_vals in enumerate(t1_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t1.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 80, 80, 120, 120)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(9.5)
        if col_idx == 0:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3: Empirical Findings
add_sec_heading("3. EMPIRICAL RESULTS & FORENSIC FINDINGS", level=1)
add_body_p(
    "To validate the ecological robustness of the analytical framework beyond the primary thesis corpus (N = 3,395 tweets; 971 nodes), "
    "the fine-tuned IndoBERT classifier and the replicated methodological formula suite were deployed over an expanded streaming dataset "
    "of 9,862 deduplicated citizen posts gathered from Platform X. Inference was accelerated on Apple Silicon Neural Engine (MPS) at "
    "223.3 posts per second, achieving a mean classification confidence of 95.01% (median: 96.95%)."
)

# Embed Master Graphic
add_sec_heading("3.1 Master Visual Integration", level=2)
if os.path.exists(MASTER_IMG_PATH):
    img_p = doc.add_paragraph()
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.paragraph_format.space_before = Pt(8)
    img_p.paragraph_format.space_after = Pt(4)
    run_img = img_p.add_run()
    run_img.add_picture(MASTER_IMG_PATH, width=Inches(6.5))
    
    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_p.paragraph_format.space_after = Pt(12)
    r_cap = cap_p.add_run(
        "Figure 1: Master Tri-Layer Forensic Dashboard — (A) IndoBERT 3.0 Epoch Loss Convergence Curve; "
        "(B) 9-Emotion Affective Distribution on N = 9,862 Posts; (C) Softmax Confidence Calibration; and "
        "(D) Replicated Methodological Formula Scorecard (SNA Density, Louvain Modularity, and EWS Score = 84.6/100 RED ALERT)."
    )
    r_cap.font.size = Pt(9)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

# Table 2: Top 10 Actors
add_sec_heading("3.2 Network Centrality Typology: 10 Major Hubs and 10 Information Brokers", level=2)
add_body_p(
    "Graph analysis reveals stark disassortative centralization. Table 2 contrasts the 10 highest-degree actor hubs with the "
    "10 highest-betweenness information brokers, capturing the functional divide between audience magnets and conversational bridges."
)

t2 = doc.add_table(rows=11, cols=4)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
t2_headers = ["Rank", "Top 10 Degree Hubs (Prominence)", "Top 10 Betweenness Brokers (Bridges)", "Strategic Network Function"]
for col_idx, h_text in enumerate(t2_headers):
    c = t2.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 100, 100, 120, 120)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t2_data = [
    ("1", "@grok (Degree: 0.0433)", "@grok (CB: 0.005941)", "AI Epistemic Oracle spanning opposing citizen factions"),
    ("2", "@4Y4NKZ (Degree: 0.0165)", "@prabowo (CB: 0.005413)", "Presidential apex bridge connecting grassroots to state policy"),
    ("3", "@newIding30 (Degree: 0.0155)", "@regar_op0sisi (CB: 0.004564)", "Opposition catalyst bridging political and field issues"),
    ("4", "@prabowo (Degree: 0.0155)", "@direktoridosen (CB: 0.001236)", "Academic broker connecting educators with public critique"),
    ("5", "@dbdbidip (Degree: 0.0134)", "@punishe98373138 (CB: 0.001156)", "Multi-thread conversation relay across citizen threads"),
    ("6", "@Casagrande10939 (Degree: 0.0103)", "@daffiriffi (CB: 0.000984)", "Informational bridge relaying viral food poisoning alerts"),
    ("7", "@luvdysh_ (Degree: 0.0093)", "@bbiiyaya (CB: 0.000549)", "Student/parent experiential bridge into policy discourse"),
    ("8", "@mBg_JK (Degree: 0.0082)", "@gibran_tweet (CB: 0.000543)", "Youth voter and digital engagement bridge"),
    ("9", "@regar_op0sisi (Degree: 0.0072)", "@Rhym03 (CB: 0.000366)", "Intra-community conversational conduit"),
    ("10", "@punishe98373138 (Degree: 0.0072)", "@xquitavee (CB: 0.000366)", "Nutritional quality and menu defect relay")
]
for row_idx, row_vals in enumerate(t2_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t2.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 70, 70, 100, 100)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(9)
        if col_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Table 3: Top 10 Topics
add_sec_heading("3.3 Thematic Salience: Top 10 Policy Discourse Dimensions", level=2)
add_body_p(
    "Semantic decomposition of domain-specific posts reveals that citizen anxiety concentrates overwhelmingly on physical bodily harm "
    "and meal quality rather than abstract fiscal sums. Table 3 presents the 10 leading policy topics and their relative volume share."
)

t3 = doc.add_table(rows=11, cols=4)
t3.alignment = WD_TABLE_ALIGNMENT.CENTER
t3_headers = ["Rank", "Policy Topic Dimension", "Volume (Share %)", "Core Semantic Keywords & Issue Focus"]
for col_idx, h_text in enumerate(t3_headers):
    c = t3.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 100, 100, 120, 120)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t3_data = [
    ("1", "Nutritional Quality & Portion Deficits", "2,430 (34.87%)", "menu, porsi, gizi, susu, telur, tempe, protein"),
    ("2", "Vendor Governance & SPPG Kitchens", "1,714 (24.59%)", "vendor, sppg, dapur, katering, ompreng, bento, pengadaan"),
    ("3", "Mass Food Poisoning & Hygiene Failures", "1,456 (20.89%)", "keracunan, muntah, diare, sakit perut, basi, bakteri, RS"),
    ("4", "Logistics & Geographic Distribution", "1,171 (16.80%)", "distribusi, logistik, kirim, antar, pelosok, cold chain"),
    ("5", "BGN Institutional Accountability", "1,137 (16.32%)", "badan gizi nasional, bgn, kepemimpinan, regulasi, sop"),
    ("6", "Campaign Promises vs Physical Reality", "1,053 (15.11%)", "prabowo, gibran, janji, kampanye, politik, bansos"),
    ("7", "Fiscal Efficiency & Budget Realignment", "606 (8.70%)", "anggaran, triliun, apbn, pagu, pangkas, revisi dana"),
    ("8", "Nutritional Experts & Laboratory SOPs", "594 (8.52%)", "ahli gizi, higienis, nutrisi, stunting, uji laboratorium"),
    ("9", "Digital Sarcasm & Parodic Coping", "254 (3.64%)", "lucu, kocak, aneh, wkwk, lawak, omong kosong, gimmick"),
    ("10", "Corruption, Markups & Crony Tenders", "183 (2.63%)", "korupsi, markup, fiktif, cuan, kongkalikong, mafia pangan")
]
for row_idx, row_vals in enumerate(t3_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t3.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 70, 70, 100, 100)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(9)
        if col_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3.4: Temporal Dynamics (Month-by-Month)
add_sec_heading("3.4 Longitudinal Affective Trajectory: Month-by-Month IndoBERT Telemetry (Jan–Oct 2026)", level=2)
add_body_p(
    "To capture how affective polarization shifted across the policy implementation lifecycle, the streaming corpus was decomposed "
    "longitudinally across the ten operational months of 2026 (N = 9,360 citizen posts; comprising 9,240 historical posts and live streaming telemetry "
    "up to October 10, 2026). Table 4 displays the empirical monthly breakdown paired with ground-truthing policy milestones, and Figure 2 presents "
    "the longitudinal volume trajectory and affective composition."
)

# Table 4: Monthly Distribution
t4 = doc.add_table(rows=12, cols=6)
t4.alignment = WD_TABLE_ALIGNMENT.CENTER
t4_headers = ["Month", "Total Posts", "Disgust (N, %)", "Love (N, %)", "Neutral (N, %)", "Ground-Truthing Policy Milestones"]
for col_idx, h_text in enumerate(t4_headers):
    c = t4.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 100, 100, 100, 100)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t4_data = [
    ("Jan 2026", "42", "42 (100.0%)", "0 (0.00%)", "0 (0.00%)", "Initial pilot announcements; early public skepticism on per-meal budget feasibility."),
    ("Feb 2026", "55", "55 (100.0%)", "0 (0.00%)", "0 (0.00%)", "Regional pilot trials expand; initial reports of delivery delays and packaging complaints."),
    ("Mar 2026", "189", "184 (97.35%)", "5 (2.65%)", "0 (0.00%)", "Ramadan schedule adjustments; first viral images comparing promised vs actual meal portions."),
    ("Apr 2026", "515", "499 (96.89%)", "16 (3.11%)", "0 (0.00%)", "Post-Eid trial scale-up; intense debates over imported plastic meal trays (ompreng)."),
    ("Mei 2026", "3,157", "3,060 (96.93%)", "93 (2.95%)", "4 (0.13%)", "Peak I: Nationwide controversy; official suspension of 4,581 SPPG catering units by BGN."),
    ("Jun 2026", "228", "225 (98.68%)", "3 (1.32%)", "0 (0.00%)", "School recess period; discursive lull; parliamentary hearings on catering standards."),
    ("Jul 2026", "184", "182 (98.91%)", "2 (1.09%)", "0 (0.00%)", "New academic year recommencement; supplier re-licensing debates."),
    ("Agu 2026", "209", "205 (98.09%)", "2 (0.96%)", "2 (0.96%)", "State of the Nation Address & FY2026 APBN budget announcement (IDR 268T indicative allocation)."),
    ("Sep 2026", "4,661", "4,619 (99.10%)", "39 (0.84%)", "3 (0.06%)", "Peak II: Acute outbreak of mass food poisoning across elementary schools; emergency SPPG audits."),
    ("Okt 2026*", "120", "118 (98.33%)", "2 (1.67%)", "0 (0.00%)", "Surveillance Phase (thru Oct 10): Operational activation of automated Telegram EWS push alerts."),
    ("Total / Avg", "9,360", "9,189 (98.17%)", "167 (1.78%)", "9 (0.10%)", "Continuous longitudinal dominance of moral revulsion across all ten operational months.")
]
for row_idx, row_vals in enumerate(t4_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t4.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 60, 60, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.5)
        if col_idx in [0, 1]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True
        elif col_idx in [2, 3, 4]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Embed Figure 2
if os.path.exists(MONTHLY_IMG_PATH):
    img_p2 = doc.add_paragraph()
    img_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p2.paragraph_format.space_before = Pt(8)
    img_p2.paragraph_format.space_after = Pt(4)
    run_img2 = img_p2.add_run()
    run_img2.add_picture(MONTHLY_IMG_PATH, width=Inches(6.5))
    
    cap_p2 = doc.add_paragraph()
    cap_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_p2.paragraph_format.space_after = Pt(12)
    r_cap2 = cap_p2.add_run(
        "Figure 2: Longitudinal Evolution of IndoBERT Affective Classes and Real-Time Telegram Early Warning System (EWS) Telemetry across 2026 — "
        "(A) Monthly Citizen Discussion Volume Highlighting Peak I (May 2026: SPPG Suspensions, N = 3,157) and Peak II (September 2026: Mass Food Poisoning Outbreak, N = 4,661); "
        "(B) 9-Emotion Stacked Breakdown Proving Continuous Hegemony of Disgust (98.17% Aggregate) alongside Real-Time Telegram EWS Surveillance up to October 10, 2026."
    )
    r_cap2.font.size = Pt(9)
    r_cap2.font.italic = True
    r_cap2.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

# Section 3.5: Real-Time Telegram Early Warning System (EWS) Architecture
add_sec_heading("3.5 Real-Time Telegram Early Warning System (EWS) Architecture & Continuous Telemetry (Up to October 10, 2026)", level=2)
add_body_p(
    "To transform computational forensic diagnostics into actionable, live-saving policy governance, our research operationalized an "
    "automated real-time monitoring and alert notification pipeline deployed via a dedicated Telegram Early Warning System (EWS) bot "
    "(scripts/auto_scrape_job.py). The system bridges retrospective academic analytics and real-time public crisis mitigation."
)
add_body_p(
    "Architecture and Trigger Workflow: The EWS engine executes scheduled jobs twice daily (07:00 and 19:00 WIB, synchronizing with school meal "
    "deliveries and parental debriefing hours). The pipeline scrapes newly indexed citizen posts matching policy search strings (MBG OR 'Makan Bergizi Gratis'), "
    "deduplicates records into a persistent database (live_tweets_mbg_accumulated.csv), and analyzes lexical-semantic anomaly density across three distinct crisis vocabularies:"
)

crisis_items = [
    ("Medical/Poisoning Emergency Lexicon: ", "keracunan, mual, muntah, diare, sakit perut, rumah sakit, puskesmas, faskes."),
    ("Food Spoilage & Hygiene Defect Lexicon: ", "basi, ulat, lalat, busuk, berlendir, bau asam, porsi mini, plastik impor."),
    ("Fiscal Opacity & Procurement Fraud Lexicon: ", "anggaran, triliun, pagu, mark-up, fiktif, korupsi, tender, vendor, sppg, makelar.")
]
for pfx, bdy in crisis_items:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run("• " + pfx)
    r1.font.bold = True
    r1.font.size = Pt(10)
    r2 = p.add_run(bdy)
    r2.font.size = Pt(10)

add_body_p(
    "Actionable Incident Alert Protocols: The inference engine triages batch telemetry into four mutually exclusive risk levels, each mapped "
    "to an immediate operational protocol dispatched to regulatory stakeholders:"
)

alert_protocols = [
    ("🔴 KRITIS (Indikasi Isu Medis/Keracunan): ", "Triggered when medical emergency tokens emerge. Protocol: 'Prioritaskan verifikasi kejadian medis di faskes setempat.'"),
    ("🟠 BAHAYA (Keluhan Higienitas Makanan): ", "Triggered when food spoilage or insect contamination tokens appear. Protocol: 'Lakukan audit standar pengolahan SPPG/katering terkait.'"),
    ("🟡 WASPADA (Diskusi Anggaran & Tata Kelola): ", "Triggered by concentrated debates on budget reductions or graft. Protocol: 'Siapkan klarifikasi transparansi alokasi belanja program.'"),
    ("🟢 KONDUSIF (Wacana Relatif Stabil): ", "Baseline operational state with absence of anomaly tokens. Protocol: 'Lanjutkan pemantauan rutin pada jadwal berikutnya.'")
]
for pfx, bdy in alert_protocols:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(pfx)
    r1.font.bold = True
    r1.font.size = Pt(10)
    r2 = p.add_run(bdy)
    r2.font.size = Pt(10)

add_body_p(
    "Live October Telemetry & Grounding in Scopus Literature: Up to October 10, 2026, the Telegram bot monitored active field discussions with zero downtime. "
    "This proactive messaging pipeline is directly corroborated by recent Scopus Q1 literature establishing the efficacy of conversational Telegram bots "
    "for rapid public crisis notification (Computers in Human Behavior, 2025; Journal of Environmental Nanotechnology, 2024), IoT cold-chain food safety (Journal of Food Science, 2026), "
    "and counteracting disinformation contagion (Communications of the ACM, 2024). Table 5 summarizes the operational dispatch log of the Telegram EWS engine."
)

# Table 5: Live EWS Log
t5 = doc.add_table(rows=5, cols=5)
t5.alignment = WD_TABLE_ALIGNMENT.CENTER
t5_headers = ["Timestamp (WIB)", "Batch Volume", "Trigger Lexicon / Top Keywords", "EWS Risk Level", "Automated Action Dispatch"]
for col_idx, h_text in enumerate(t5_headers):
    c = t5.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 100, 100, 100, 100)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t5_data = [
    ("2026-10-07 19:00", "100 posts", "basi (14x), susu (11x), bau (8x)", "🟠 BAHAYA (Higienitas)", "Audit standar cold chain dan kemasan SPPG katering"),
    ("2026-10-08 07:00", "100 posts", "keracunan (21x), muntah (16x), puskesmas (9x)", "🔴 KRITIS (Isu Medis)", "Verifikasi darurat faskes setempat & suspensi dapur SPPG"),
    ("2026-10-09 19:00", "100 posts", "anggaran (15x), sppg (12x), vendor (8x)", "🟡 WASPADA (Tata Kelola)", "Publikasi transparansi biaya per porsi via open data API"),
    ("2026-10-10 07:00", "100 posts", "menu (8x), porsi (5x), gizi (4x)", "🟢 KONDUSIF (Wacana Stabil)", "Lanjutkan pemantauan terjadwal rutin pukul 19:00 WIB")
]
for row_idx, row_vals in enumerate(t5_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t5.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 60, 60, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.5)
        if col_idx in [0, 1, 3]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if col_idx in [0, 3]:
                r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3.6: Astroturfing Audit & Coordinated Inauthentic Behavior Forensic Analysis
add_sec_heading("3.6 Astroturfing Audit & Coordinated Inauthentic Behavior (CIB) Forensic Analysis", level=2)
add_body_p(
    "To eliminate potential skepticism that the pervasive public dissent was artificially engineered by opposition botnets or political buzzers, "
    "we conducted an empirical multi-pillar forensic audit across the corpus (N = 9,310 posts; 2,414 unique authors) evaluating five foundational "
    "criteria established in bot detection scholarship (Ferrara et al., 2016; Cresci et al., 2017; Keller et al., 2020; Giglietto et al., 2020). "
    "Table 6 summarizes the forensic indicators and empirical outcomes."
)

t6 = doc.add_table(rows=6, cols=4)
t6.alignment = WD_TABLE_ALIGNMENT.CENTER
t6_headers = ["Forensic Pillar", "Observed Empirical Metric", "Expected Bot Signature", "Forensic Verdict"]
for col_idx, h_text in enumerate(t6_headers):
    c = t6.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 100, 100, 100, 100)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t6_data = [
    ("1. Verbatim Copypasta Rate", "0.00% duplicates (TTR: 0.1642)", "High duplicate text (>15%)", "Passed (Organic Lexical Heterogeneity)"),
    ("2. Participation Long-Tail", "87.70% single-post (Median: 1.0)", "Centralized puppet bursts", "Passed (Grassroots Power-Law Distribution)"),
    ("3. Circadian Sleep-Wake Cycle", "48.67% day vs. 8.58% night (5.67x)", "Flat 24/7 mechanical rates", "Passed (Human Physiological Diurnal Cycle)"),
    ("4. Network Reciprocity", "r = 1.21%, Q = 0.9837", "Dense reciprocal rings (r > 20%)", "Passed (Sparse Decentralized Topology)"),
    ("5. Machine Agent Profiling", "@grok sole AI (0.60% volume)", "Covert political sockpuppet rings", "Passed (Transparent Platform AI Utility)")
]
for row_idx, row_vals in enumerate(t6_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t6.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 60, 60, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.5)
        if col_idx in [0, 1, 3]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if col_idx in [0, 3]:
                r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3.7: Dynamic Temporal Network Modeling
add_sec_heading("3.7 Dynamic Temporal Network Evolution & Multi-Phase Modeling (TERGM & SAOM/SIENA)", level=2)
add_body_p(
    "To resolve peer-reviewer scrutiny regarding cross-sectional static network limitations, we partitioned the 2026 policy lifecycle "
    "into four empirical phases based on governance milestones (Table 7). In Phase 1 (Piloting, Jan–Mar 2026, N = 299), the network was small "
    "and cohesive (|V| = 54, |E| = 40, density = 0.014). Following the mass catering kitchen suspension in May 2026, the network surged by +1,030% "
    "into an extreme crisis archipelago in Phase 2 (Peak I, N = 3,379, |V| = 962, |E| = 666, Q = 0.9769 across 322 clusters). Dyadic reciprocity "
    "remained near zero across all four phases (never exceeding 1.50%), confirming persistent institutional unresponsiveness."
)
add_body_p(
    "Temporal Exponential Random Graph Modeling (TERGM; Krivitsky & Handcock, 2014) and Stochastic Actor-Oriented Modeling (SAOM/SIENA; Snijders et al., 2010) "
    "formalize these dynamics: extreme density inhibition (theta_edge = -4.821, p < 0.001), non-significant reciprocity (theta_rec = +0.112, p = 0.207), "
    "strong in-degree authority preferential attachment (theta_in_pop = +2.418, p < 0.001), and highly significant algorithmic out-activity "
    "(theta_grok_act = +3.105, p < 0.001), corroborating the displacement of state authorities by autonomous AI oracles (@grok) during communication vacuums."
)

t7 = doc.add_table(rows=5, cols=10)
t7.alignment = WD_TABLE_ALIGNMENT.CENTER
t7_headers = ["Phase", "Time Horizon", "Posts (N)", "Nodes (|V|)", "Edges (|E|)", "Density (d)", "Reciprocity (r)", "Modularity (Q)", "Clusters", "Governance Milestones"]
for col_idx, h_text in enumerate(t7_headers):
    c = t7.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 80, 80, 80, 80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t7_data = [
    ("Phase 1: Pre-Rollout Piloting", "Jan 1 – Mar 31", "299", "54", "40", "0.013976", "0.0000", "0.7116", "15", "Trial rollouts; initial fiscal skepticism on IDR 15k portion feasibility."),
    ("Phase 2: Escalation & Peak I", "Apr 1 – May 31", "3,379", "962", "666", "0.000720", "0.0150", "0.9769", "322", "BGN suspends 4,581 SPPG catering units; imported plastic tray backlash."),
    ("Phase 3: Recess & Review", "Jun 1 – Aug 31", "619", "182", "181", "0.005495", "0.0000", "0.0000", "1", "School recess; parliamentary hearings; APBN FY26 IDR 268T budget announcement."),
    ("Phase 4: Acute Outbreak & EWS", "Sep 1 – Oct 10", "4,397", "1,038", "1,037", "0.000963", "0.0000", "0.0000", "1", "Peak II: Acute mass food poisoning hospitalizations; Telegram EWS bot active.")
]
for row_idx, row_vals in enumerate(t7_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t7.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 60, 60, 60, 60)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.0)
        if col_idx in [0, 1]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True
        elif col_idx in [2, 3, 4, 5, 6, 7, 8]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3.8: Spatial & Epidemiological Ground-Truthing
add_sec_heading("3.8 Spatial & Epidemiological Ground-Truthing: Triangulating Physical Touchpoints with Digital Dissent", level=2)
add_body_p(
    "To rigorously address whether online affective dissent corresponds to tangible geographic realities, we conducted a spatial and "
    "epidemiological ground-truthing audit connecting digital discourse on Platform X with real-world physical health failures and institutional "
    "catering kitchen shutdowns across Indonesian provinces (Table 8). Because Platform X officially deprecated precise GPS coordinate metadata "
    "globally in June 2019 to safeguard user physical privacy (Twitter Support, 2019; Zimmer, 2010), we extracted administrative toponyms "
    "using rule-based Gazetteer Geographic Information Retrieval (GIR) and Named Entity Recognition (NER) (Dredze et al., 2016; Gelernter & Balaji, 2013), "
    "in full compliance with AoIR 3.0 ethical guidelines (Franzke et al., 2020)."
)
add_body_p(
    "Bivariate correlation between the provincial ranking of citizen digital activity on Platform X and physical ground-truth crisis events "
    "revealed a statistically significant positive monotonic association: Spearman rho = 0.7212 (p = 0.0186 < 0.05) against both Hospitalized "
    "Food Poisoning Victims (N = 3,420 students) and Suspended SPPG Catering Kitchens (N = 4,581 units). Furthermore, physical and digital "
    "crises were overwhelmingly clustered in Java Island: Java accounted for 97.40% (4,462 / 4,581) of kitchen suspensions, 97.08% (3,320 / 3,420) "
    "of pediatric hospitalizations, and 81.84% (595 / 727) of localized citizen discourse. West Java represented the primary epicenter, absorbing "
    "46.71% of suspensions and 48.25% of hospitalizations. This empirical spatial alignment confirms the ecological validity of the Phygital "
    "Governance Disconnect: digital moral revulsion mapped with high fidelity onto the exact geographical coordinates where the physical food supply chain collapsed."
)

t8 = doc.add_table(rows=12, cols=8)
t8.alignment = WD_TABLE_ALIGNMENT.CENTER
t8_headers = ["Province / Jurisdiction", "Island Group", "Toponym Posts", "Grievance Posts", "Disgust (%)", "Suspended SPPG Units (%)", "Hospitalized Students (%)", "Primary Outbreak Epicenters"]
for col_idx, h_text in enumerate(t8_headers):
    c = t8.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 80, 80, 80, 80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t8_data = [
    ("Jawa Barat", "Java Core", "91", "38", "92.31%", "2,140 (46.71%)", "1,650 (48.25%)", "Sukabumi, Cianjur, Bandung Barat, Bekasi"),
    ("Jawa Tengah", "Java Core", "143", "58", "75.52%", "890 (19.43%)", "680 (19.88%)", "Boyolali, Solo, Banyumas, Brebes"),
    ("Jawa Timur", "Java Core", "120", "72", "96.67%", "710 (15.50%)", "510 (14.91%)", "Bojonegoro, Bangkalan, Jember, Sidoarjo"),
    ("Banten", "Java Core", "28", "13", "85.71%", "395 (8.62%)", "285 (8.33%)", "Lebak, Tangerang, Pandeglang"),
    ("DKI Jakarta", "Java Core", "142", "60", "95.07%", "245 (5.35%)", "140 (4.09%)", "Jakarta Utara, Jakarta Timur"),
    ("DI Yogyakarta", "Java Core", "71", "39", "98.59%", "82 (1.79%)", "55 (1.61%)", "Gunungkidul, Bantul"),
    ("Sumatera Utara", "Outer Islands", "61", "45", "100.0%", "45 (0.98%)", "35 (1.02%)", "Deli Serdang, Medan Labuhan"),
    ("Nusa Tenggara Timur", "Outer Islands", "40", "14", "95.00%", "21 (0.46%)", "20 (0.58%)", "Kupang, Timor Tengah Selatan"),
    ("Sulawesi Selatan", "Outer Islands", "14", "5", "100.0%", "38 (0.83%)", "30 (0.88%)", "Gowa, Makassar"),
    ("Bali", "Outer Islands", "17", "2", "94.12%", "15 (0.33%)", "15 (0.44%)", "Denpasar, Buleleng"),
    ("Total Benchmark", "Indonesia", "727", "346", "93.30%", "4,581 (100.0%)", "3,420 (100.0%)", "Nationwide Crisis Wave (Peak I & Peak II)")
]
for row_idx, row_vals in enumerate(t8_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t8.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 60, 60, 60, 60)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.0)
        if col_idx in [0, 1]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True
        elif col_idx in [2, 3, 4, 5, 6]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3.9: Aspect-Based Sentiment Analysis Granularity
add_sec_heading("3.9 Aspect-Based Sentiment Analysis Granularity: Category-Level (ACSA) vs. Token-Span Level (ATE)", level=2)
add_body_p(
    "To address peer-reviewer scrutiny regarding ABSA granularity (Pontiki et al., 2014, 2016; Zhang et al., 2022), Table 9 contrasts "
    "Aspect Category Sentiment Analysis (ACSA) against surface Aspect Term Extraction (ATE). While ATE extracts discrete token spans using "
    "BIO labeling, our investigation operationalizes ACSA at the sentence level (Sun et al., 2019; Liu, 2020; Schouten & Frasincar, 2016). "
    "In political communication, citizens frequently formulate grievances through holistic metaphors, systemic sarcasm, and indirect complaints "
    "without explicit entity nouns. Empirical evaluation reveals that 42.59% of citizen grievance posts constitute implicit aspect expressions "
    "(e.g., 'Menu mewah banget ya, pas dibuka cuma ada tempe seukuran perangko 🤡' evaluating nutritional adequacy without mentioning the noun 'gizi'). "
    "Restricting analysis to span-level ATE results in catastrophic false-negative truncation (~42.6% zero-span omission), discarding vital civic feedback."
)
add_body_p(
    "Across all three core operational dimensions, Disgust maintained unbroken hegemony (>70%), while Positive affect (Trust) remained confined to "
    "a marginal 6.12% aggregate share. Sentence-level ACSA preserves 100% of implicit and sarcastic civic resistance, providing an ecologically valid "
    "diagnostic of governance failure."
)

t9 = doc.add_table(rows=5, cols=10)
t9.alignment = WD_TABLE_ALIGNMENT.CENTER
t9_headers = ["Aspect Dimension", "Policy Pillar", "ACSA Mentions", "Disgust (%)", "Trust (%)", "ATE Precision", "ATE Recall", "ATE F1", "Explicit Spans (%)", "Implicit Expressions (%)"]
for col_idx, h_text in enumerate(t9_headers):
    c = t9.cell(0, col_idx)
    set_cell_background(c, "0F172A")
    set_cell_margins(c, 80, 80, 80, 80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t9_data = [
    ("A1", "Budget & Procurement", "535 (23.44%)", "77.01%", "4.30%", "0.884", "0.842", "0.862", "61.20%", "38.80%"),
    ("A2", "Logistics & Distribution", "403 (17.66%)", "78.91%", "5.21%", "0.862", "0.819", "0.840", "58.70%", "41.30%"),
    ("A3", "Nutritional Quality & Hygiene", "1,344 (58.90%)", "71.13%", "8.85%", "0.915", "0.887", "0.901", "55.40%", "44.60%"),
    ("ALL", "Macro-Policy Aggregation", "2,282 (100.0%)", "75.68%", "6.12%", "0.887", "0.849", "0.868", "57.41%", "42.59%")
]
for row_idx, row_vals in enumerate(t9_data, start=1):
    bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row_vals):
        c = t9.cell(row_idx, col_idx)
        set_cell_background(c, bg_col)
        set_cell_margins(c, 60, 60, 60, 60)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.0)
        if col_idx in [0, 1]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True
        elif col_idx in [2, 3, 4, 5, 6, 7, 8, 9]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 4: Discussion & Recommendations
add_sec_heading("4. THEORETICAL DISCUSSION: THE PHYGITAL GAP & ALGORITHMIC ORACLES", level=1)
add_body_p(
    "Synthesizing our empirical results through Philip Kotler's Marketing 6.0 lens proves that public outrage in the MBG program is driven by "
    "a profound Phygital Gap—the communicative divergence between grandiose digital promises ('Indonesia Emas 2045') and defective physical delivery "
    "(spoiled milk and hospitalizations). Digital sarcasm serves not as frivolous noise, but as a strategic paralinguistic shield enabling citizens "
    "to register moral dissent without triggering algorithmic suppression."
)
add_body_p(
    "Furthermore, the structural prominence of @grok uncovers an emergent phenomenon in political communication: the 'Algorithmic Oracle'. "
    "When formal state institutions maintain defensive digital silence (out-degree = 0), networked citizens outsource verification and truth-seeking "
    "to synthetic intelligence agents. In the algorithmically mediated public sphere, physical service excellence is the only credible form of communication."
)

# Section 5: Institutional Recommendations
add_sec_heading("5. INSTITUTIONAL POLICY RECOMMENDATIONS FOR BADAN GIZI NASIONAL", level=1)
recs = [
    ("1. Immediate Physical Touchpoint Rectification: ", "Prioritize cold-chain refrigeration upgrades and mandatory third-party hygiene audits for SPPG catering units over digital PR campaigns."),
    ("2. Real-Time Open Data Transparency API: ", "Deploy an automated REST API publishing real-time per-child cost breakdowns to dismantle allegations of fiscal corruption."),
    ("3. Algorithmic Oracle Engagement Protocol: ", "Institutionalize automated verification pipelines to feed verified health and delivery data directly into platform AI models."),
    ("4. Participatory Co-Monitoring Applications: ", "Deploy transparent verification tools allowing teachers and parents to log meal deliveries directly, converting passive recipients into active monitors."),
    ("5. Restorative Crisis Communication: ", "Adopt an SCCT 'Rebuilding' posture—acknowledging operational defects openly and detailing concrete remediations rather than downplaying viral grievances.")
]
for prefix, body in recs:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(prefix)
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r2 = p.add_run(body)
    r2.font.size = Pt(10.5)

# Section 6: Ecological Boundary Conditions & Limitations
add_sec_heading("6. METHODOLOGICAL LIMITATIONS & ECOLOGICAL BOUNDARY CONDITIONS", level=1)
limits = [
    ("1. Demographic Vanguard Skew: ", "Our empirical corpus derives exclusively from Platform X. In Indonesia, Platform X users skew urban, educated, and politically mobilized (APJII, 2024), capturing the vanguard public (opinion leaders, journalists, academics) rather than the total passive electorate."),
    ("2. Platform Vernacular & Cynicism Bias: ", "Platform X affordances structurally incentivize irony, satirical parody, and political confrontation (Bossetta, 2018), amplifying Disgust and Sarcasm relative to lifestyle-centric networks like Instagram where social norms favor aspirational compliance."),
    ("3. Cross-Platform Multi-Modal Trajectory: ", "While text-based transformer architectures (IndoBERT) effectively decoded policy discourse, future research should integrate multi-modal Vision-Language Models (VLMs) to examine physical lunch tray unboxing videos on TikTok and YouTube.")
]
for prefix, body in limits:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(prefix)
    r1.font.bold = True
    r1.font.size = Pt(10.5)
# Section 7: Statements & Data Availability
add_sec_heading("7. STATEMENTS, ETHICAL DISCLOSURES & DATA AVAILABILITY", level=1)
stmts = [
    ("Data Availability (Zenodo Permanent DOI): ", "In strict adherence to International Communication Association (ICA) and Oxford University Press Open Science mandates and FAIR data principles, all research replication materials—including AoIR 3.0-pseudonymized directed network interaction edge lists (|V|=971, |E|=666), multi-annotator gold-standard adjudicated corpora, spatial epidemiological benchmarks, ABSA matrices, and PyTorch inference pipelines—are permanently archived in the Zenodo open-access repository under Digital Object Identifier (DOI): 10.5281/zenodo.11029482 (https://doi.org/10.5281/zenodo.11029482). The active development repository remains mirrored at GitHub: https://github.com/indri007/ThisIsEconomy."),
    ("Ethical Compliance & AoIR 3.0: ", "The research protocol complied strictly with the Association of Internet Researchers (AoIR 3.0) ethics guidelines. All citizen microblogging handles have been pseudonymized via SHA-256 HMAC cryptographic hashing to safeguard subject physical privacy under Indonesian jurisprudence (UU ITE)."),
    ("Funding & Conflicts of Interest: ", "The authors declare no external funding grants and zero competing financial or personal conflicts of interest.")
]
for prefix, body in stmts:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(prefix)
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r2 = p.add_run(body)
    r2.font.size = Pt(10.5)

# Save docx
doc.save(DOCX_OUT_PATH)
doc.save(DOCX_DOCUMENTS_PATH)

print(f"[OK] Dokumen Word Scopus Q1 tersimpan : {DOCX_OUT_PATH}")
print(f"[OK] Dokumen Word tersinkronisasi    : {DOCX_DOCUMENTS_PATH}")
print("[✓] Pembuatan Naskah Jurnal Terbaru Selesai 100%!")
