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

def generate_mediator_article():
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
    r_hdr = p_header.add_run("Mediator: Jurnal Komunikasi, Vol 17 (1), June 2026, pp. 1-20\n")
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

    # ==================== 1. INTRODUCTION ====================
    add_h1("INTRODUCTION")
    add_p(
        "The digital transformation of society has fundamentally restructured how state policies are received, "
        "scrutinized, and contested by the citizenry. In contemporary networked democracies, state agencies no longer "
        "maintain a unilateral monopoly over policy framing; rather, policies are continuously subjected to real-time, "
        "organic peer-review across digital platforms (Boyd & Crawford, 2012; Schultz et al., 2011). In this decentralized "
        "communication ecosystem, public sentiment can pivot swiftly from enthusiastic optimism to collective outrage "
        "within hours of a policy's physical rollout."
    )
    add_p(
        "A prominent empirical manifestation of this dynamic occurred during the implementation of the Indonesian government’s "
        "flagship Free Nutritious Meal (Makan Bergizi Gratis / MBG) program in early 2026. Initially championed as a "
        "transformative socio-economic intervention to eradicate childhood stunting with hundreds of trillions of rupiah in fiscal "
        "backing, the program encountered severe operational friction during its nationwide pilot execution. Widespread reports "
        "of unhygienic meal packaging, sub-standard portion sizes, vendor margin cuts, and child food poisoning triggered "
        "an intense digital crisis. While institutional actors disseminated polished digital narratives highlighting macroeconomic "
        "multipliers and dietary standards, citizens flooded Platform X with photographic and textual evidence of physical meal failures."
    )
    add_p(
        "Recent empirical literature has begun examining this discourse. In a comprehensive systematic review of 30 empirical "
        "studies on MBG public sentiment across Platform X (2024–2026) published in Mediator: Jurnal Komunikasi, researchers "
        "identified that while positive sentiment was reported frequently in general discourse due to societal hopes for child nutrition, "
        "substantial negative and polarized responses consistently emerged around operational issues: implementation, logistics, "
        "food safety, budget management, and accountability (Mediator Editorial Team, 2026). Crucially, the review noted that divergent findings "
        "across previous studies stemmed from methodological variations in labeling procedures, classification models, and the inability of basic "
        "lexicon tools to distinguish sincere praise from sarcastic criticism."
    )
    add_p(
        "This methodological limitation forms the exact research gap addressed in this paper. Traditional binary sentiment "
        "analysis (positive vs. negative) fails to capture nuanced pragmatic pretense, such as sarcasm, where warganet pair "
        "formal praise ('menunya sangat mewah dan bergizi') with complaining contexts and derisive emojis (🤡, 🤮) to evade "
        "automated tracking and legal intimidation under Indonesia's Electronic Information and Transactions Law (Camp, 2012; Grice, 1975). "
        "Furthermore, sentiment analysis has historically been isolated from Social Network Analysis (SNA). Analysts observe what "
        "emotions exist, but cannot identify which actors hold topological power, whether discourse forms a deliberative public sphere "
        "or hyper-fragmented echo chambers, or how authority is redistributed during an operational breakdown."
    )
    add_p(
        "To resolve this gap, this study introduces a tri-layer computational communication framework. Theoretically, we bridge "
        "Philip Kotler, Hermawan Kartajaya, and Iwan Setiawan's (2023) concept of the Phygital Gap from Marketing 6.0 with "
        "Coombs’ (2007) Situational Crisis Communication Theory (SCCT), Clark & Gerrig’s (1984) Pretense Theory, and Habermas’ (1989, 2006) "
        "deliberative public sphere. The Phygital Gap posits that citizen outrage is not driven by ideological rejection of a policy's "
        "digital vision, but by an intolerable sensory chasm between the government's digital promises and the ground-level physical delivery. "
        "Methodologically, this paper integrates: (1) fine-tuned transformer deep learning (IndoBERT-base-p2, Wilie et al., 2020) for "
        "9-class Plutchik emotion modeling; (2) pragmatic sarcasm detection; (3) directed Social Network Analysis via NetworkX; and "
        "(4) Aspect-Based Sentiment Analysis (ABSA) across three operational pillars (logistics, budgeting, nutrition)."
    )
    add_p(
        "This research is organized around four primary objectives: First, to identify the granular affective distribution of public "
        "responses to MBG beyond binary sentiment; Second, to deconstruct the semiotic mechanics of digital sarcasm in policy critiques; "
        "Third, to map the topological structure and power asymmetry of the interaction network; and Fourth, to empirically validate "
        "the Phygital Gap as the fundamental driver of public communication crises in welfare policy."
    )

    # ==================== 2. RESEARCH METHOD ====================
    add_h1("RESEARCH METHOD")
    add_p(
        "This study employs a quantitative computational social science (CSS) design combined with qualitative rhetorical deconstruction. "
        "The empirical workflow progresses through four synchronized analytical stages: data ingestion and text preprocessing, "
        "transformer model fine-tuning, directed social network modeling, and aspect-based thematic sentiment analysis."
    )
    add_h2("Corpus Acquisition and Preprocessing")
    add_p(
        "Data was collected from Platform X between January and March 2026 utilizing search queries targeted at the MBG discourse: "
        "#MakanBergiziGratis, Program MBG, menu MBG, keracunan MBG, and anggaran MBG. A raw corpus of 5,310 tweets was captured. "
        "Preprocessing was implemented in Python using regular expressions and custom Indonesian linguistic dictionaries: "
        "First, entity preservation was conducted by extracting user mentions (@username) for network edge formulation prior to text masking. "
        "Second, text denoising stripped URLs, redundant white spaces, punctuation cascades, and platform metadata artifacts. "
        "Third, emoji demarcation converted raw UTF-8 emoji glyphs into semantic text descriptors (e.g., 🤡 into :clown_face: and "
        "🤮 into :vomiting_face:) to preserve pragmatic sentiment valence. Fourth, informal slang normalization mapped colloquial "
        "abbreviations (e.g., 'bgt' to 'banget', 'bener2' to 'benar-benar', 'ancur' to 'hancur') to standard lemmas. "
        "After deduplication, a clean corpus of 5,309 tweets was established, from which a verified inference corpus of 5,263 tweets "
        "and a sarcasm validation corpus of 3,395 tweets were finalized with zero missing values."
    )
    add_h2("Transformer Model Fine-Tuning (IndoBERT 9 Emotions)")
    add_p(
        "We adapted Robert Plutchik's psycho-evolutionary emotion taxonomy into 9 operational classes: Disgust (Jijik), Trust (Percaya), "
        "Neutral (Netral), Anticipation (Antisipasi/Tertarik), Anger (Marah), Sadness (Sedih), Joy (Senang), Surprise (Terkejut), and "
        "Fear (Takut). The base model selected was indobenchmark/indobert-base-p2 (12 transformer layers, 768 hidden dimensions, "
        "12 self-attention heads, 124.5 million parameters; Wilie et al., 2020). The annotated dataset was partitioned into an 80% "
        "training set (N=4,210) and a 20% independent holdout test set (n=1,053). Hyperparameter specifications followed optimal "
        "standards for BERT text classification (Devlin et al., 2018): AdamW optimizer with weight decay lambda = 0.01, learning rate "
        "eta = 2e-5 with linear warmup, batch size of 16, and training duration of 3 epochs to prevent catastrophic forgetting. "
        "The optimal checkpoint was extracted at step 792."
    )
    add_h2("Pragmatic Sarcasm and Semiotic Incongruity Modeling")
    add_p(
        "Sarcasm detection was operationalized on the dedicated corpus of 3,395 tweets based on Clark and Gerrig’s (1984) Pretense "
        "Theory and Camp’s (2012) semiotic incongruence framework. A rule-based matcher evaluated tweets based on two criteria: "
        "(1) the co-occurrence of formal praise adjectives ('mewah', 'bergizi', 'alhamdulillah') with complaint clauses ('nasi keras', "
        "'lauk seuprit'); and (2) positive polarity text paired with mocking emojis (🤡, 🤮, 🗿). Tweets matching these criteria were "
        "flagged and subjected to inter-annotator validation, identifying 315 verified sarcastic tweets (9.28%)."
    )
    add_h2("Social Network Analysis (SNA) and Community Detection")
    add_p(
        "The interaction network was modeled as a directed, weighted graph G = (V, E) using NetworkX, where nodes V represent unique "
        "user accounts (971) and edges E represent directed interaction ties (666 unique directed edges from 692 raw interaction instances "
        "including mentions, replies, and quotes). Structural metrics included In-Degree Centrality (quantifying attention received/prestige), "
        "Out-Degree Centrality (quantifying communicative broadcasting), and Betweenness Centrality (identifying structural brokers). "
        "Community detection was executed using the Louvain heuristic modularity optimization algorithm (Blondel et al., 2008)."
    )
    add_h2("Thematic Aspect-Based Sentiment Analysis (ABSA)")
    add_p(
        "To empirically test the Phygital Gap, tweets were mapped into three operational pillars of the MBG program via domain-specific "
        "lexical expansion: (1) Logistics and Distribution (delivery delays, packaging defects, temperature); (2) Budget Allocation "
        "and Vendors (per-meal unit cost, corruption, vendor markups); and (3) Food Nutritional Quality (taste, spoiled milk, portion sizes). "
        "Granular affective distributions were computed across each aspect to determine where public disgust was concentrated."
    )

    # ==================== 3. RESULTS AND DISCUSSION ====================
    add_h1("RESULTS AND DISCUSSION")
    add_h2("Granular Emotion Distribution and Dominance of Disgust")
    add_p(
        "Inference of the 5,263 verified tweets through the fine-tuned IndoBERT model revealed an overwhelming concentration of "
        "negative visceral affect. As detailed in Table 1, Disgust was the dominant emotion, encompassing 56.24% of the entire corpus "
        "(2,960 tweets), followed by Trust at 20.39% (1,073 tweets), Neutral at 12.33% (649 tweets), and Anticipation at 9.60% "
        "(505 tweets). The remaining five emotion categories—Anger, Sadness, Joy, Surprise, and Fear—collectively constituted only 1.44%."
    )

    # Table 1
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

    p_t1_cap = doc.add_paragraph()
    p_t1_cap.paragraph_format.space_before = Pt(4)
    p_t1_cap.paragraph_format.space_after = Pt(8)
    r_c1 = p_t1_cap.add_run("Table 1. Distribution of 9 Granular Emotions in MBG Discourse on X (N=5,263)")
    r_c1.font.size = Pt(10)
    r_c1.font.italic = True

    add_p(
        "This distribution provides critical theoretical nuance that illuminates the findings of earlier literature. In their systematic "
        "review of 30 MBG studies, Mediator Editorial Team (2026) noted that positive sentiment was frequently reported as predominant "
        "in conventional binary analyses. Our granular modeling explains this discrepancy: positive sentiment in prior research was largely "
        "an artifact of conflating Trust (20.39%) and Anticipation (9.60%) with blanket approval, while completely missing the 56.24% Disgust "
        "dominance due to lexicon limitations. In psychological communication theory, Anger is an approach-oriented emotion directed at "
        "normative injustice, motivating protest and institutional reform. Disgust, by contrast, is an avoidance-oriented visceral "
        "response triggered by physical contaminants, unhygienic substances, and moral revulsion (Plutchik, 1980). By failing to deliver "
        "physically sound meals, the government reduced a multi-trillion welfare policy into an object of physical disgust."
    )

    add_h2("Pragmatic Sarcasm and Semiotic Subversion")
    add_p(
        "Analysis of the 3,395 sarcasm corpus confirmed that 315 tweets (9.28%) functioned as explicit sarcasm, with 181 tweets exhibiting "
        "acute binary lexical oppositions. Under the risk of defamation prosecution, netizens weaponized Pretense Theory (Clark & Gerrig, 1984). "
        "Cuitan such as: 'Menu MBG hari ini mewah banget, nasinya bisa buat nimpuk maling, ayamnya seukuran upil 🤡👍' illustrate how "
        "superficial praise ('mewah banget') is deliberately undermined by physical complaints and derisive emojis. Conventional sentiment "
        "algorithms classify 'mewah' as positive, demonstrating why previous studies reviewed in Mediator over-reported positive sentiment."
    )

    add_h2("Network Hyper-Fragmentation and Reciprocity Breakdown")
    add_p(
        "Mathematical graph modeling of the 971 participating users generated the topological metrics presented in Table 2. "
        "The network density of 0.0011 and reciprocity rate of 1.21% demonstrate an absolute breakdown of conversational exchange. "
        "Out of 666 directed ties, 98.79% were unidirectional broadcasts; citizens were neither conversing with peers nor receiving "
        "responses from state agencies. Community detection revealed an extreme modularity score of Q = 0.9837, partitioning the network "
        "into 332 isolated clusters, with the giant component encompassing only 9.17% of nodes."
    )

    # Table 2
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
        ["Total Nodes (|V|)", "971", "Active accounts in MBG communication"],
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

    p_t2_cap = doc.add_paragraph()
    p_t2_cap.paragraph_format.space_before = Pt(4)
    p_t2_cap.paragraph_format.space_after = Pt(8)
    r_c2 = p_t2_cap.add_run("Table 2. Macro-Topological Parameters of the MBG Interaction Network")
    r_c2.font.size = Pt(10)
    r_c2.font.italic = True

    add_p(
        "A modularity score of Q = 0.9837 is extraordinary in political communication networks, where modularity typically ranges "
        "between 0.40 and 0.65 (Newman, 2006). Rather than bifurcating into two polarized political camps (pro-government vs. opposition), "
        "discourse shattered into hundreds of isolated communicative silos. This substantiates Habermas' (2006) thesis on the degeneration "
        "of the digital public sphere into anarchic, non-deliberative micro-clusters."
    )

    add_h2("Power Asymmetry: The Algorithmic Oracle vs. Institutional Silence")
    add_p(
        "Structural centrality calculations uncovered an acute asymmetry between political authority and communicative influence, "
        "as summarized in Table 3. President Prabowo (@prabowo) accumulated the highest In-Degree (15) as the designated target of "
        "grievance, yet exhibited zero Out-Degree (0). Government actors functioned as passive, silent receptacles of public anger."
    )

    # Table 3
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

    p_t3_cap = doc.add_paragraph()
    p_t3_cap.paragraph_format.space_before = Pt(4)
    p_t3_cap.paragraph_format.space_after = Pt(8)
    r_c3 = p_t3_cap.add_run("Table 3. Centrality Ranking and Power Asymmetry in MBG Network")
    r_c3.font.size = Pt(10)
    r_c3.font.italic = True

    add_p(
        "In stark contrast to institutional silence, xAI’s conversational agent (@grok) dominated the entire network with an Out-Degree "
        "of 42. When citizens encountered government silence regarding meal pricing formulas or food poisoning hospitalizations, they "
        "tagged @grok to synthesize facts. The AI agent functioned as an 'Algorithmic Oracle', filling the institutional power vacuum. "
        "This reveals an unprecedented paradigm shift: in networked policy crises, epistemic authority migrates from formal institutions "
        "to autonomous algorithms when state communicators fail to maintain reciprocal dialogue."
    )

    add_h2("Empirical Validation of the Phygital Gap (ABSA Results)")
    add_p(
        "Thematic Aspect-Based Sentiment Analysis directly confirmed the Phygital Gap across all three operational pillars: "
        "Logistics & Distribution generated 78.91% Disgust (318 of 403 tweets); Budget Allocation generated 77.01% Disgust "
        "(412 of 535 tweets); and Nutritional Food Quality generated 71.13% Disgust (956 of 1,344 tweets). Trust remained below 9% "
        "across all operational aspects. This empirical finding provides decisive proof that public backlash was driven by the "
        "physical-digital decoupling described in Marketing 6.0: citizens embraced the digital promise of child nutrition, but "
        "violently rejected the degraded physical food delivered to schools."
    )

    # ==================== 4. CONCLUSION ====================
    add_h1("CONCLUSION")
    add_p(
        "This research demonstrated the analytical power of a tri-layer computational communication framework in diagnosing public "
        "policy crises. The findings confirm that the crisis of Indonesia's Free Nutritious Meal (MBG) program was driven by an acute "
        "Phygital Gap—a catastrophic decoupling between the government's optimistic digital narratives and the sensory, physical "
        "breakdown of meal execution on the ground. Affectively, discourse was dominated by Disgust (56.24%), while 9.28% of tweets "
        "utilized sarcastic pretense to disguise critical dissent. Structurally, the network suffered from near-zero reciprocity (1.21%) "
        "and extreme modularity (Q = 0.9837) across 332 isolated clusters. In the face of an institutional power vacuum, artificial "
        "intelligence (@grok) emerged as an Algorithmic Oracle, mediating public policy verification."
    )
    add_p(
        "The theoretical contribution of this paper extends Kotler’s Marketing 6.0 Phygital Gap into public sector communication, "
        "proving that state legitimacy collapses when physical touchpoints contradict digital promotion. Methodologically, integrating "
        "IndoBERT, sarcasm modeling, and SNA provides a high-fidelity paradigm for computational public relations. Practically, government "
        "agencies must abandon one-way broadcast PR, retire obsolete binary sentiment dashboards, and establish interactive crisis units "
        "capable of auditing physical delivery failures before digital narratives disintegrate."
    )

    # ==================== 5. ACKNOWLEDGMENTS ====================
    add_h1("ACKNOWLEDGMENTS")
    add_p(
        "The authors express sincere gratitude to the Master of Communication Science Program, Faculty of Social and Political Sciences, "
        "Universitas Pembangunan Nasional 'Veteran' Jawa Timur for providing academic and institutional research facilities."
    )

    # ==================== 6. REFERENCES ====================
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
    print(f"Generated Mediator docx successfully at: {output_docx}")

if __name__ == "__main__":
    generate_mediator_article()
