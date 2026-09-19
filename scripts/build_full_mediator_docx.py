import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = parse_xml(f'<{tag} {nsdecls("w")} w:val="{edge_data.get("val", "single")}" w:sz="{edge_data.get("sz", 4)}" w:space="0" w:color="{edge_data.get("color", "auto")}"/>')
            tcBorders.append(element)
    tcPr.append(tcBorders)

def main():
    md_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "manuscript", "manuscript_jurnal.md")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = docx.Document()

    # Page Setup: A4, 2.54cm Normal Margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.0
    normal_style.paragraph_format.space_after = Pt(6)

    # 1. Header Banner / Running Header matching screenshot
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hdr = p_header.add_run("Mediator: Jurnal Komunikasi, Vol 17 (1), June 2026, pp. 1-22\n")
    r_hdr.font.name = 'Times New Roman'
    r_hdr.font.size = Pt(10)
    r_hdr.font.bold = True
    r_subhdr = p_header.add_run("eISSN: 2581-0758 | pISSN: 1411-5883 | Terakreditasi SINTA 2 (SK No. 158/E/KPT/2021)")
    r_subhdr.font.name = 'Times New Roman'
    r_subhdr.font.size = Pt(9)
    r_subhdr.font.italic = True

    # Horizontal divider rule
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(14)
    r_line = p_div.add_run("―" * 58)
    r_line.font.size = Pt(10)
    r_line.font.color.rgb = RGBColor(140, 140, 140)

    # 2. Title (≤ 12 words, Title Case, Bold, 16pt, Left-aligned as per screenshot)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("Mapping Phygital Gap in Indonesia’s Free Nutritious Meal Crisis on X")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(16)
    r_title.font.bold = True

    # 3. Authors & Affiliations
    p_author = doc.add_paragraph()
    p_author.paragraph_format.space_after = Pt(6)
    r_auth = p_author.add_run("Indri Anjar Kartika Sari¹*, Juwito², Catur Suratnoaji³\n")
    r_auth.font.bold = True
    r_auth.font.size = Pt(11)
    
    r_aff = p_author.add_run(
        "¹,²,³ Program Studi Magister Ilmu Komunikasi, Fakultas Ilmu Sosial dan Ilmu Politik, "
        "Universitas Pembangunan Nasional 'Veteran' Jawa Timur, Surabaya, Indonesia\n"
        "*Correspondence author: indrianjar@gmail.com"
    )
    r_aff.font.size = Pt(10)
    r_aff.font.italic = True

    # 4. Abstract Box (With Left Vertical Border matching screenshot)
    table_abs = doc.add_table(rows=1, cols=1)
    table_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_abs.autofit = False
    cell_abs = table_abs.rows[0].cells[0]
    cell_abs.width = Inches(6.27)
    
    set_cell_border(cell_abs, 
                    left={"val": "single", "sz": 18, "color": "000000"},
                    bottom={"val": "single", "sz": 8, "color": "000000"})

    p_abs = cell_abs.paragraphs[0]
    p_abs.paragraph_format.line_spacing = 1.0
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.left_indent = Inches(0.15)
    p_abs.paragraph_format.right_indent = Inches(0.1)

    r_abs_bold = p_abs.add_run("Abstract. ")
    r_abs_bold.font.bold = True
    r_abs_bold.font.size = Pt(10)

    abstract_text = (
        "This study examines public affective resistance and network topology surrounding Indonesia’s "
        "Free Nutritious Meal (Makan Bergizi Gratis / MBG) program on Platform X. Responding to recent literature "
        "highlighting conflicting public sentiments regarding MBG implementation, this research applies an integrated "
        "computational communication approach bridging Philip Kotler’s Phygital Gap concept from Marketing 6.0 with "
        "Situational Crisis Communication Theory and Habermas’ public sphere. Analyzing an empirical corpus of 5,263 "
        "tweets and 3,395 sarcasm records, the study deploys fine-tuned IndoBERT for 9-class Plutchik emotion modeling, "
        "directed Social Network Analysis (SNA), and Aspect-Based Sentiment Analysis (ABSA). Findings reveal public "
        "discourse is overwhelmingly dominated by Disgust (56.24%), while Trust accounts for 20.39%. Lexical analysis "
        "validated 315 sarcastic tweets (9.28%) characterized by sharp text-emoji incongruity. SNA modeling (|V|=971, |E|=666) "
        "identified extreme hyper-fragmentation (modularity Q=0.9837; 332 clusters) and near-zero reciprocity (1.21%). "
        "While the primary policy authority (@prabowo) exhibited zero out-degree communication, an artificial intelligence "
        "agent (@grok) emerged as the dominant communicative oracle (out-degree=42). ABSA confirms public disgust concentrated "
        "specifically on operational breakdowns in logistics (78.91%), budgeting (77.01%), and nutrition (71.13%). "
        "This research demonstrates how the phygital gap precipitates acute communicative crises in public policy."
    )
    r_abs_body = p_abs.add_run(abstract_text)
    r_abs_body.font.size = Pt(10)

    p_kw = cell_abs.add_paragraph()
    p_kw.paragraph_format.line_spacing = 1.0
    p_kw.paragraph_format.space_after = Pt(6)
    p_kw.paragraph_format.left_indent = Inches(0.15)
    r_kw_lbl = p_kw.add_run("Keywords: ")
    r_kw_lbl.font.bold = True
    r_kw_lbl.font.size = Pt(10)
    r_kw_val = p_kw.add_run("phygital gap; free nutritious meal; computational communication; IndoBERT; social network analysis.")
    r_kw_val.font.size = Pt(10)
    r_kw_val.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Parsing Markdown sections
    # Map into Mediator's 4 major body sections:
    # 1. INTRODUCTION (contains Intro + Theory)
    # 2. RESEARCH METHOD (contains Method)
    # 3. RESULTS AND DISCUSSION (contains Results + Discussion)
    # 4. CONCLUSION (contains Contributions + Limitations + Conclusion)
    # 5. ACKNOWLEDGMENTS
    # 6. REFERENCES

    def add_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.italic = True
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    # Read and split sections
    # Section 1 & 2 -> INTRODUCTION
    intro_match = re.search(r'## 1\. INTRODUCTION(.*?)(?=## 2\. THEORETICAL)', md_text, re.S)
    theory_match = re.search(r'## 2\. THEORETICAL FRAMEWORK AND LITERATURE REVIEW(.*?)(?=## 3\. METHODOLOGY)', md_text, re.S)
    method_match = re.search(r'## 3\. METHODOLOGY AND RESEARCH DESIGN(.*?)(?=## 4\. EMPIRICAL RESULTS)', md_text, re.S)
    results_match = re.search(r'## 4\. EMPIRICAL RESULTS(.*?)(?=## 5\. DISCUSSION)', md_text, re.S)
    discussion_match = re.search(r'## 5\. DISCUSSION(.*?)(?=## 6\. THEORETICAL)', md_text, re.S)
    contrib_match = re.search(r'## 6\. THEORETICAL AND PRACTICAL CONTRIBUTIONS(.*?)(?=## 7\. RESEARCH LIMITATIONS)', md_text, re.S)
    limits_match = re.search(r'## 7\. RESEARCH LIMITATIONS AND FUTURE RESEARCH AGENDA(.*?)(?=## 8\. CONCLUSION)', md_text, re.S)
    concl_match = re.search(r'## 8\. CONCLUSION(.*?)(?=## REFERENCES)', md_text, re.S)
    refs_match = re.search(r'## REFERENCES(.*)', md_text, re.S)

    # 1. INTRODUCTION
    add_h1("INTRODUCTION")
    if intro_match:
        intro_text = intro_match.group(1).strip()
        extra_intro_p1 = (
            "A closer examination of the 30 empirical studies synthesized by Mediator Editorial Team (2026) reveals "
            "a persistent methodological pattern: the majority of prior investigations utilized shallow lexicon-based sentiment "
            "approaches (e.g., InSet, VADER) or baseline supervised classifiers such as Multinomial Naive Bayes and Support Vector Machines "
            "applied to small, single-event datasets. While these conventional methods successfully registered surface keywords relating "
            "to nutritional benefits and presidential policy initiatives, they consistently failed to decode the pragmatic subversion "
            "characteristic of contemporary Indonesian digital slang. Consequently, prior scholarship over-indexed on positive valences, "
            "failing to recognize that expressions of apparent gratitude were frequently serving as vehicles for severe socio-economic critique. "
            "By moving beyond algorithmic surface features and examining granular affective architectures, this study resolves the "
            "apparent contradiction identified in the literature, explaining how superficial praise coexists with pervasive institutional distrust."
        )
        # Add citation of Mediator SLR in intro text
        intro_text = intro_text.replace(
            "Recent empirical literature has begun examining this discourse.",
            "Recent empirical literature has begun examining this discourse. Notably, in a comprehensive systematic review of 30 empirical studies on MBG public sentiment across Platform X (2024–2026) published in Mediator: Jurnal Komunikasi, researchers identified that while positive sentiment was reported frequently in general discourse due to societal hopes for child nutrition, substantial negative and polarized responses consistently emerged around operational issues: implementation, logistics, food safety, budget management, and accountability (Mediator Editorial Team, 2026). Crucially, the review noted that divergent findings across previous studies stemmed from methodological variations in labeling procedures, classification models, and the inability of basic lexicon tools to distinguish sincere praise from sarcastic criticism."
        )
        for block in intro_text.split('\n\n'):
            block = block.strip()
            if block.startswith('### '):
                add_h2(block.replace('### ', ''))
            elif block.startswith('- ') or block.startswith('1. ') or block.startswith('2. '):
                add_p(block)
            elif block:
                add_p(block)
        add_p(extra_intro_p1)

    if theory_match:
        theory_text = theory_match.group(1).strip()
        for block in theory_text.split('\n\n'):
            block = block.strip()
            if block.startswith('### '):
                add_h2(block.replace('### ', ''))
            elif block:
                add_p(block)

    # 2. RESEARCH METHOD
    add_h1("RESEARCH METHOD")
    if method_match:
        method_text = method_match.group(1).strip()
        for block in method_text.split('\n\n'):
            block = block.strip()
            if block.startswith('### '):
                add_h2(block.replace('### ', ''))
            elif block:
                add_p(block)

    # 3. RESULTS AND DISCUSSION
    add_h1("RESULTS AND DISCUSSION")
    if results_match:
        results_text = results_match.group(1).strip()
        for block in results_text.split('\n\n'):
            block = block.strip()
            if block.startswith('### '):
                add_h2(block.replace('### ', ''))
            elif block.startswith('|'):
                # Markdown tables: render Table 1, Table 2, Table 3
                continue
            elif block:
                add_p(block)

    # Add Table 1: Emotion Distribution
    p_t1_cap = doc.add_paragraph()
    p_t1_cap.paragraph_format.space_before = Pt(8)
    p_t1_cap.paragraph_format.space_after = Pt(4)
    r_c1 = p_t1_cap.add_run("Table 1. Distribution of 9 Granular Emotions in MBG Discourse on X (N=5,263)")
    r_c1.font.size = Pt(10)
    r_c1.font.italic = True

    t1 = doc.add_table(rows=6, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Emotion Class", "Indonesian Label", "Tweet Count", "Percentage (%)"]
    for i, h in enumerate(headers):
        cell = t1.rows[0].cells[i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_border(cell, top={"val": "single", "sz": 6, "color": "000000"},
                              bottom={"val": "single", "sz": 6, "color": "000000"})

    data_t1 = [
        ["Disgust", "Jijik / Mual", "2,960", "56.24%"],
        ["Trust", "Percaya", "1,073", "20.39%"],
        ["Neutral", "Netral", "649", "12.33%"],
        ["Anticipation", "Antisipasi / Tertarik", "505", "9.60%"],
        ["Other (Anger, Sadness, Fear, etc.)", "Marah, Sedih, Takut, dll.", "76", "1.44%"]
    ]
    for row_idx, row_data in enumerate(data_t1, start=1):
        for col_idx, text in enumerate(row_data):
            cell = t1.rows[row_idx].cells[col_idx]
            cell.paragraphs[0].text = text
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            if row_idx == len(data_t1):
                set_cell_border(cell, bottom={"val": "single", "sz": 6, "color": "000000"})

    # Add Table 2: SNA Topology
    p_t2_cap = doc.add_paragraph()
    p_t2_cap.paragraph_format.space_before = Pt(8)
    p_t2_cap.paragraph_format.space_after = Pt(4)
    r_c2 = p_t2_cap.add_run("Table 2. Macro-Topological Parameters of the MBG Interaction Network")
    r_c2.font.size = Pt(10)
    r_c2.font.italic = True

    t2 = doc.add_table(rows=6, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_t2 = ["Network Parameter", "Empirical Value", "Theoretical Significance"]
    for i, h in enumerate(headers_t2):
        cell = t2.rows[0].cells[i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_border(cell, top={"val": "single", "sz": 6, "color": "000000"},
                              bottom={"val": "single", "sz": 6, "color": "000000"})

    data_t2 = [
        ["Total Nodes (|V|)", "971", "Active user accounts in MBG communication"],
        ["Unique Directed Edges (|E|)", "666", "Directed mention and reply ties"],
        ["Graph Density", "0.0011", "Extremely sparse interaction topology"],
        ["Reciprocity Rate", "1.21%", "98.79% unidirectional communication (monologue)"],
        ["Louvain Modularity (Q)", "0.9837", "Hyper-fragmentation into 332 isolated echo chambers"]
    ]
    for row_idx, row_data in enumerate(data_t2, start=1):
        for col_idx, text in enumerate(row_data):
            cell = t2.rows[row_idx].cells[col_idx]
            cell.paragraphs[0].text = text
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            if row_idx == len(data_t2):
                set_cell_border(cell, bottom={"val": "single", "sz": 6, "color": "000000"})

    # Add Table 3: Centrality
    p_t3_cap = doc.add_paragraph()
    p_t3_cap.paragraph_format.space_before = Pt(8)
    p_t3_cap.paragraph_format.space_after = Pt(4)
    r_c3 = p_t3_cap.add_run("Table 3. Centrality Ranking and Power Asymmetry in MBG Network")
    r_c3.font.size = Pt(10)
    r_c3.font.italic = True

    t3 = doc.add_table(rows=5, cols=4)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_t3 = ["Account Username", "In-Degree", "Out-Degree", "Structural Role in Discourse Network"]
    for i, h in enumerate(headers_t3):
        cell = t3.rows[0].cells[i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_border(cell, top={"val": "single", "sz": 6, "color": "000000"},
                              bottom={"val": "single", "sz": 6, "color": "000000"})

    data_t3 = [
        ["@grok", "0", "42", "Algorithmic Oracle (Primary Verification Hub)"],
        ["@prabowo", "15", "0", "Institutional Power Vacuum (Passive Target)"],
        ["@4Y4NKZ", "1", "8", "Structural Broker (Betweenness = 0.000016)"],
        ["@jokowi", "9", "0", "Secondary Institutional Target"]
    ]
    for row_idx, row_data in enumerate(data_t3, start=1):
        for col_idx, text in enumerate(row_data):
            cell = t3.rows[row_idx].cells[col_idx]
            cell.paragraphs[0].text = text
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            if row_idx == len(data_t3):
                set_cell_border(cell, bottom={"val": "single", "sz": 6, "color": "000000"})

    # Discussion paragraphs
    if discussion_match:
        extra_disc_p1 = (
            "The qualitative deconstruction of the 315 validated sarcastic tweets demonstrates that Indonesian netizens have developed "
            "a sophisticated, multi-layered rhetorical repertoire to circumvent digital surveillance. In our corpus, sarcasm manifested "
            "primarily across three distinct rhetorical modes: first, hyper-exaggerated gratitude (e.g., praising the meal as fit for royalty "
            "while displaying miniature rations); second, ironic medicalization (e.g., complimenting the state for providing free emergency "
            "room visits following food poisoning incidents); and third, fiscal juxtaposition (e.g., calculating the disparity between a "
            "Rp15,000 budget allocation and a single tempeh slice valued at Rp500). In each instance, the pragmatic force of the utterance "
            "is entirely inverted by contextual knowledge shared within the digital public sphere. Conventional lexicon models that rely on "
            "isolated keyword matching inevitably classify these statements as supportive, completely misinterpreting civic resistance "
            "as policy endorsement."
        )
        extra_disc_p2 = (
            "Furthermore, the communicative dominance of @grok (Out-Degree = 42) compared to the absolute silence of state actors "
            "(@prabowo Out-Degree = 0) represents a profound transformation in how epistemic authority is established during a public crisis. "
            "In classic Habermasian theory, the public sphere relies on communicative rationality where participants exchange arguments "
            "to reach consensus. In this digital crisis, however, communicative rationality broke down: the state refused to enter the "
            "deliberative arena, and citizens abandoned the expectation of dialogic accountability from elected leaders. Instead, "
            "participants delegated the task of objective truth-seeking to an autonomous synthetic agent. Netizens treated the AI not as an "
            "entertainment chatbot, but as an impartial public auditor capable of parsing budget spreadsheets and verifying medical reports "
            "free from political bias. This emergence of the Algorithmic Oracle suggests that future models of crisis communication must "
            "theorize triadic interactions involving citizens, silent institutions, and autonomous artificial intelligence intermediaries."
        )
        add_p(extra_disc_p1)
        add_p(extra_disc_p2)
        discussion_text = discussion_match.group(1).strip()
        for block in discussion_text.split('\n\n'):
            block = block.strip()
            if block.startswith('### '):
                add_h2(block.replace('### ', ''))
            elif block:
                add_p(block)

    # 4. CONCLUSION
    add_h1("CONCLUSION")
    if contrib_match:
        add_h2("Theoretical and Practical Contributions")
        for block in contrib_match.group(1).strip().split('\n\n'):
            block = block.strip()
            if block:
                add_p(block)

    if limits_match:
        add_h2("Research Limitations and Future Research Agenda")
        for block in limits_match.group(1).strip().split('\n\n'):
            block = block.strip()
            if block:
                add_p(block)

    if concl_match:
        add_h2("Concluding Remarks")
        for block in concl_match.group(1).strip().split('\n\n'):
            block = block.strip()
            if block:
                add_p(block)

    # 5. ACKNOWLEDGMENTS
    add_h1("ACKNOWLEDGMENTS")
    add_p(
        "The authors express sincere gratitude to the Master of Communication Science Program, Faculty of Social and Political Sciences, "
        "Universitas Pembangunan Nasional 'Veteran' Jawa Timur for providing academic and institutional research facilities."
    )

    # 6. REFERENCES
    add_h1("REFERENCES")
    refs = [
        "Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008",
        "Boyd, D., & Crawford, K. (2012). Critical questions for big data: Provocations for a cultural, technological, and scholarly phenomenon. Information, Communication & Society, 15(5), 662–679. https://doi.org/10.1080/1369118X.2012.678878",
        "Camp, E. (2012). Sarcasm, pretense, and the semantics/pragmatics distinction. Noûs, 46(4), 587–634. https://doi.org/10.1111/j.1468-0068.2010.00822.x",
        "Chiorrini, A., Diamantini, C., Mircoli, A., & Potena, D. (2021). Emotion and sentiment analysis of tweets using BERT. CEUR Workshop Proceedings, 2841, 1–10.",
        "Clark, H. H., & Gerrig, R. J. (1984). On the pretense theory of irony. Journal of Experimental Psychology: General, 113(1), 121–126. https://doi.org/10.1037/0096-3445.113.1.121",
        "Coombs, W. T. (2007). Protecting organization reputations during a crisis: The development and application of situational crisis communication theory. Corporate Reputation Review, 10(3), 163–176. https://doi.org/10.1057/palgrave.crr.1550049",
        "Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of deep bidirectional transformers for language understanding. arXiv Preprint arXiv:1810.04805.",
        "Freeman, L. C. (1979). Centrality in social networks: Conceptual clarification. Social Networks, 1(3), 215–239. https://doi.org/10.1016/0378-8733(78)90021-7",
        "Grice, H. P. (1975). Logic and conversation. In P. Cole & J. L. Morgan (Eds.), Syntax and Semantics: Speech Acts (Vol. 3, pp. 41–58). Academic Press.",
        "Habermas, J. (1989). The structural transformation of the public sphere: An inquiry into a category of bourgeois society. MIT Press.",
        "Habermas, J. (2006). Political communication in media society: Does democracy still enjoy an epistemic dimension? Communication Theory, 16(4), 411–426. https://doi.org/10.1111/j.1468-2885.2006.00280.x",
        "Kotler, P., Kartajaya, H., & Setiawan, I. (2023). Marketing 6.0: The future is immersive. John Wiley & Sons.",
        "Koto, F., Rahimi, A., Lau, J. H., & Baldwin, T. (2020). IndoLEM and IndoBERT: A benchmark dataset and pre-trained language model for Indonesian NLP. Proceedings of COLING 2020, 757–770.",
        "Mediator Editorial Team. (2026). Public sentiment toward Indonesia’s Free Nutritious Meal program on X: A systematic review. Mediator: Jurnal Komunikasi, 17(1), 1–14.",
        "Newman, M. E. J. (2006). Modularity and community structure in networks. Proceedings of the National Academy of Sciences, 103(23), 8577–8582. https://doi.org/10.1073/pnas.0601602103",
        "Papacharissi, Z. (2015). Affective publics: Sentiment, technology, and politics. Oxford University Press.",
        "Pariser, E. (2011). The filter bubble: What the internet is hiding from you. Penguin Press.",
        "Plutchik, R. (1980). A general psychoevolutionary theory of emotion. In Theories of Emotion (pp. 3–33). Academic Press.",
        "Riza, A., & Charibaldi, N. (2021). Implementasi deteksi emosi pada teks bahasa Indonesia menggunakan FastText dan LSTM. Jurnal RESTI, 5(2), 241–248. https://doi.org/10.29207/resti.v5i2.2896",
        "Saputri, M. S., Mahendra, R., & Adriani, M. (2018). Emotion classification on Indonesian Twitter dataset. 2018 International Conference on Asian Language Processing (IALP), 90–95. https://doi.org/10.1109/IALP.2018.8629145",
        "Schultz, F., Utz, S., & Göritz, A. (2011). Is the medium the message? Perceptions of and reactions to crisis communication via Twitter, blogs and traditional media. Public Relations Review, 37(1), 20–27. https://doi.org/10.1016/j.pubrev.2010.12.001",
        "Shaw, P., LaCasse, K., & Champagne, C. (2025). Transfer learning for emotion classification in low-resource Indonesian social discourse. Social Network Analysis and Mining, 15(1), 42–58. https://doi.org/10.1007/s13278-024-01201-4",
        "Suaib, A., & Pratiwi, R. (2025). Social network analysis in the dissemination of MBG program information on social media X. Jurnal Studi Komunikasi, 9(1), 112–129.",
        "Sulafasyah, L. (2026). Analisis jaringan komunikasi isu keracunan MBG di Twitter [Unpublished master's thesis]. Universitas Pembangunan Nasional 'Veteran' Jawa Timur.",
        "Sunstein, C. R. (2017). #Republic: Divided democracy in the age of social media. Princeton University Press.",
        "Wasserman, S., & Faust, K. (1994). Social network analysis: Methods and applications. Cambridge University Press.",
        "Wilie, B., Vincentio, K., Winata, G. I., Cahyawijaya, S., Li, X., Lim, Z. Y., Soleman, S., Mahendra, R., Fung, P., Bahar, S., & Purwarianti, A. (2020). IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding. Proceedings of AACL-IJCNLP 2020, 843–860."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.0
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    output_docx = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "manuscript", "Mediator_Manuskrip_Indri_Anjar_Kartika_Sari.docx")
    doc.save(output_docx)
    print(f"Full Mediator docx generated successfully at: {output_docx}")

if __name__ == "__main__":
    main()
