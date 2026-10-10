import os
import shutil
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def apply_table_styles(tbl, caption):
    tblPr = tbl._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:left w:val="none"/>'
        '<w:right w:val="none"/>'
        '<w:insideV w:val="none"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)
    if caption:
        cap_el = parse_xml(f'<w:tblCaption {nsdecls("w")} w:val="{caption}"/>')
        tblPr.append(cap_el)

def set_cell_properties(cell, fill_hex=None, top=100, bottom=100, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    if fill_hex:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_table(doc, headers, data, caption_title):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    apply_table_styles(tbl, caption_title)
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for col_idx, header_text in enumerate(headers):
        hdr_cells[col_idx].text = header_text
        set_cell_properties(hdr_cells[col_idx], fill_hex="EAEAEA")
        for p in hdr_cells[col_idx].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.0)
                r.font.bold = True
                
    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            # Zebra striping for readability
            fill = "F9F9F9" if row_idx % 2 == 1 else None
            if "IndoBERT" in str(row_data[0]) or "Macro Average" in str(row_data[0]) or "Weighted Average" in str(row_data[0]):
                fill = "F0F4F8"
            set_cell_properties(row_cells[col_idx], fill_hex=fill)
            for p in row_cells[col_idx].paragraphs:
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(8.5)
                    if any(k in str(row_data[0]) for k in ["Macro Average", "Weighted Average", "IndoBERT"]):
                        r.font.bold = True
                        
    return tbl

def format_p(p, text, bold_prefix=None, style_name='Normal', space_after=6, line_spacing=1.25):
    p.text = ""
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Times New Roman'
        r_bold.font.size = Pt(12)
        r_bold.font.bold = True
    r_body = p.add_run(text)
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(12)

def run():
    src_path = 'Journal_Paper_Indri_Anjar_MBG_SNA_JIKI.docx'
    out_path = 'Journal_Paper_Indri_Anjar_MBG_SNA_JIKI_REVISED.docx'
    
    doc = docx.Document(src_path)
    print("Loaded document with", len(doc.paragraphs), "paragraphs and", len(doc.tables), "tables.")
    
    # 1. Update Images for Confusion Matrix and F1-Scores
    cm_path = 'results/FINAL_indobert_confusion_matrix_normalized.png'
    f1_path = 'results/FINAL_indobert_f1_scores_updated.png'
    
    if os.path.exists(cm_path):
        with open(cm_path, 'rb') as f:
            doc.part.rels['rId63'].target_part._blob = f.read()
        print("Updated rId63 with normalized confusion matrix!")
    else:
        print("Warning: cm_path not found:", cm_path)
        
    if os.path.exists(f1_path):
        with open(f1_path, 'rb') as f:
            doc.part.rels['rId66'].target_part._blob = f.read()
        print("Updated rId66 with updated F1 scores plot!")
    else:
        print("Warning: f1_path not found:", f1_path)

    # 2. Update Abstract (P4)
    abstract_text = (
        "Indonesia’s Free Nutritious Meal (Makan Bergizi Gratis, MBG) program triggered intense sarcastic and critical "
        "discourse on platform X during its nationwide rollout (March–May 2026). This study examines the linguistic, affective, "
        "and structural anatomy of this public dissent through an explanatory-sequential mixed-method computational design: "
        "fine-tuned IndoBERT with group-aware cross-validation for multi-task emotion classification and sarcasm identification, "
        "directed Social Network Analysis (SNA) with Louvain community detection, and Aspect-Based Sentiment Analysis (ABSA) "
        "across three critical policy facets. The complete corpus comprises 5,263 tweets, with a directed mention graph of 971 actors "
        "and 692 directed edges (666 unique ties). Benchmarked against linear baseline models under an independent, zero-leakage "
        "group-aware holdout partition (N = 1,058), IndoBERT achieved 79.40% accuracy, a Macro-F1 of 0.5160, and a Weighted-F1 of 0.7851, "
        "substantially outperforming TF-IDF + Logistic Regression (Acc 69.47%, Macro-F1 0.3429) and Linear SVM (Acc 67.20%, Macro-F1 0.4095). "
        "Social network analysis reveals severe structural hyper-fragmentation: a Louvain modularity Q = 0.9837, 341 weakly connected components, "
        "reciprocity of only 1.20%, and a giant component holding just 9.17% of actors. Multi-period longitudinal analysis demonstrates that "
        "from pre-escalation (March–April) to crisis peak (May 2026), the network expanded by +699% in nodes and modularity surged from "
        "0.9455 to 0.9851. Actor centrality identifies a fundamental divergence: the platform AI account @grok serves as an epistemic inquiry "
        "oracle (42 mentions, out-degree 0), while presidential authority @prabowo acts as an institutional sink for public grievance (15 mentions, "
        "76.2% disgust). Negative valence, dominated by visceral disgust, exceeds 71% across all policy facets, led by Nutritional Quality "
        "(1,344 mentions). Interpreted through Marketing 6.0's phygital gap framework, we demonstrate that digital sarcasm serves as an "
        "evaluative paralinguistic shield for moral accountability. We conclude with strategic governance recommendations for decentralizing "
        "public communication, managing algorithmic verification risk, and deploying sarcasm-aware early warning listening systems."
    )
    format_p(doc.paragraphs[4], abstract_text)
    
    # 3. Update Section 3.1 (P23: Data Collection & Ethical Compliance)
    p23_text = (
        "Tweets were collected with a Python extraction suite between March 1 and May 31, 2026, using the targeted query: "
        "(“Makan Bergizi Gratis” OR “MBG” OR “Makan Siang Gratis” OR “SPPG” OR “Badan Gizi Nasional” OR “BGN”) AND lang:id. "
        "We recorded tweet ID, full text, author handle, ISO 8601 timestamp (UTC+7), relational metadata (reply-to, directed mentions, quote tweets), "
        "and engagement metrics. While keyword-based extraction inherently captures the primary institutional and colloquial anchors of national discourse, "
        "we acknowledge the methodological limitation that emergent, unindexed slang terms may have eluded initial retrieval. Data collection and handling "
        "adhered strictly to the Association of Internet Researchers (AoIR) ethical guidelines and Platform X Developer Terms of Service. Only publicly "
        "accessible posts were gathered. To safeguard citizen privacy and mitigate potential legal exposure under Indonesia’s Electronic Information and "
        "Transactions Law (UU ITE), all non-public citizen accounts were systematically pseudonymized in textual quotations and network visualizations. "
        "Verified institutional figures (@prabowo, @kemkomdigi) and platform artificial intelligence agents (@grok) were maintained as public civic records. "
        "Automated bots—defined as accounts posting >120 tweets/day, exhibiting rigid mechanical posting frequencies, following >5,000 accounts with "
        "near-zero followers, or publishing verbatim copypasta—were filtered out."
    )
    format_p(doc.paragraphs[23], p23_text)

    # 4. Update Section 3.2 (P25: Corpus, Group-Aware Split, & Sarcasm Annotation)
    p25_text = (
        "The complete analytical corpus contains 5,263 tweets, from which we extracted a directed mention graph comprising 971 nodes and 692 directed "
        "edges (666 unique ties). In live social media corpora, standard random train-test splits frequently suffer from severe data leakage caused by "
        "viral retweets, quote copypasta, and minor lexical variants. To enforce strict methodological validity, we partitioned the dataset using "
        "GroupShuffleSplit (random seed 42) grouped by normalized text hashes. This yielded an 80:20 partition with zero text leakage between folds: "
        "a training set of N_train = 4,205 tweets (79.90%) and an independent holdout test set of N_test = 1,058 tweets (20.10%). Preprocessing removed "
        "URLs and redundant system tokens, performed selective case folding, and normalized colloquial Indonesian slang using an expanded 3,500-entry "
        "lexicon (e.g., bgt → banget, gakjelas → tidak jelas). Crucially, emojis were shielded from punctuation stripping and translated into descriptive "
        "semantic tokens using the Python emoji library (e.g., 🤡 → :clown_face:, 🤮 → :face_vomiting:) to preserve ironic and affective polarity. "
        "Controlled lemmatization was applied via Sastrawi.\n\n"
        "Ground truth annotation followed a rigorous multi-stage procedure. For digital sarcasm detection, a dedicated corpus of 3,395 tweets was annotated "
        "by three independent communication and linguistic coders who operationalized sarcasm through pragmatic incongruence—specifically, the juxtaposition "
        "of laudatory surface phrasing with mocking emojis (🤡, 🤮, 😇) or hyperbolic contrast against known administrative failures. The annotation achieved "
        "high inter-coder reliability (Fleiss’ κ = 0.864), establishing 315 validated sarcastic tweets (9.28% prevalence). For emotion classification, "
        "reference annotations were established across six active affective categories (Disgust, Trust, Neutral, Interest, Anger, Sadness), capturing "
        "the natural empirical skew of public crisis discourse. The constructed social network models explicit directed @mentions, which directly "
        "operationalize targeted institutional appeals, accountability demands, and AI verification inquiries, distinguishing these purposive "
        "interactions from broad retweet dissemination cascades."
    )
    format_p(doc.paragraphs[25], p25_text)

    # 5. Update Section 3.3 (P27: Model Architecture, Baselines, & Evaluation Protocol)
    p27_text = (
        "The core classifier was built upon indobert-base-p2 [18] (12 transformer layers, 768 hidden dimensions, 12 attention heads, ~124.5 million parameters) "
        "configured with two task heads: a multi-class emotion classification head and a binary sarcasm detection head, each preceded by dropout (p = 0.3). "
        "Fine-tuning employed the AdamW optimizer with a maximum sequence length of 128 tokens, batch size of 16, learning rate of 2 × 10^-5 with 10% linear "
        "warm-up followed by linear weight decay, minimizing a joint multi-task loss L_total = λ1 L_emotion + λ2 L_sarcasm with λ1 = λ2 = 1.0.\n\n"
        "To benchmark model performance rigorously against standard natural language processing baselines, we trained two competitive linear models on the "
        "exact same group-aware training split (N = 4,205) and evaluated them on the identical holdout test set (N = 1,058): (1) TF-IDF (unigram and bigram "
        "features, sublinear term-frequency scaling, maximum 10,000 features) combined with multinomial Logistic Regression (L2 regularization, C = 1.0), "
        "and (2) TF-IDF combined with a Linear Support Vector Machine (Linear SVM, C = 1.0, balanced class weighting). Given the substantial empirical class "
        "imbalance inherent in crisis discourse, evaluation is reported across multiple complementary metrics: overall Accuracy, Precision, Recall, "
        "Macro-F1 (unweighted arithmetic mean capturing sensitivity to minority classes), Weighted-F1 (accounting for class prevalence), and "
        "Normalized Confusion Matrices."
    )
    format_p(doc.paragraphs[27], p27_text)

    # 6. Overhaul Section 4.5: Heading, Text, Table 5, Table 6, Captions, and Network-NLP Integration
    doc.paragraphs[63].text = "4.5\tModel Evaluation and Benchmark Validation"
    doc.paragraphs[63].runs[0].font.name = 'Times New Roman'
    doc.paragraphs[63].runs[0].font.size = Pt(13)
    doc.paragraphs[63].runs[0].font.bold = True
    
    p64_text = (
        "To establish empirical classification validity and address potential risks of evaluation bias, the fine-tuned IndoBERT multi-task model "
        "was benchmarked against competitive linear baselines on the completely unseen group-aware holdout test set (N = 1,058). The group-aware "
        "partition ensures zero text-hash or template leakage between training and testing splits. As presented in Table 5, IndoBERT achieved "
        "an overall Accuracy of 79.40%, a Macro-F1 of 0.5160, and a Weighted-F1 of 0.7851, substantially outperforming TF-IDF + Logistic Regression "
        "(Accuracy 69.47%, Macro-F1 0.3429, Weighted-F1 0.6457) and TF-IDF + Linear SVM (Accuracy 67.20%, Macro-F1 0.4095, Weighted-F1 0.6558). "
        "The contextual bidirectional attention mechanisms of IndoBERT provide a +12.20% gain in accuracy and a +10.65% increase in Macro-F1 "
        "over Linear SVM, demonstrating its capability to decode nuanced syntactic structures and ironic framing under significant lexical noise."
    )
    format_p(doc.paragraphs[64], p64_text)
    
    # Update Captions for Figure 9 and Figure 10
    doc.paragraphs[66].text = "Figure 9. Normalized confusion matrix of the fine-tuned IndoBERT emotion classifier on the group-aware holdout test set (N = 1,058)."
    doc.paragraphs[66].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[66].runs[0].font.name = 'Times New Roman'
    doc.paragraphs[66].runs[0].font.size = Pt(10)
    doc.paragraphs[66].runs[0].font.italic = True
    
    doc.paragraphs[68].text = "Figure 10. Class-wise F1-scores of IndoBERT across emotion categories on the holdout test set (N = 1,058)."
    doc.paragraphs[68].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[68].runs[0].font.name = 'Times New Roman'
    doc.paragraphs[68].runs[0].font.size = Pt(10)
    doc.paragraphs[68].runs[0].font.italic = True

    # 7. Construct Data for Table 5, Table 6, and Table 7
    t5_headers = ["Model Architecture", "Partition Protocol", "Accuracy", "Macro Prec.", "Macro Rec.", "Macro F1", "Wtd. Prec.", "Wtd. Rec.", "Weighted F1"]
    t5_data = [
        ["TF-IDF + Logistic Regression", "Group-Aware (80:20)", "69.47%", "0.3814", "0.3402", "0.3429", "0.6476", "0.6947", "0.6457"],
        ["TF-IDF + Linear SVM", "Group-Aware (80:20)", "67.20%", "0.5433", "0.3882", "0.4095", "0.6535", "0.6720", "0.6558"],
        ["IndoBERT Group-Aware (Proposed)", "Group-Aware (80:20)", "79.40%", "0.6726", "0.4977", "0.5160", "0.7900", "0.7940", "0.7851"]
    ]
    t5_tbl = create_table(doc, t5_headers, t5_data, "Table 5. Comparative evaluation of emotion classification models on the group-aware holdout test set (N = 1,058).")

    t6_headers = ["Emotion Category", "Test Support (n)", "Class Share (%)", "Precision", "Recall", "F1-Score"]
    t6_data = [
        ["Disgust (Jijik)", "606", "57.28%", "0.8176", "0.8729", "0.8444"],
        ["Trust (Percaya)", "220", "20.79%", "0.7511", "0.7545", "0.7528"],
        ["Neutral (Netral)", "124", "11.72%", "0.8347", "0.8145", "0.8245"],
        ["Interest (Tertarik)", "91", "8.60%", "0.6324", "0.4725", "0.5409"],
        ["Anger (Marah)", "14", "1.32%", "1.0000", "0.0714", "0.1333"],
        ["Sadness (Sedih)", "3", "0.28%", "0.0000", "0.0000", "0.0000"],
        ["Macro Average", "1,058", "100.0%", "0.6726", "0.4977", "0.5160"],
        ["Weighted Average", "1,058", "100.0%", "0.7900", "0.7940", "0.7851"]
    ]
    t6_tbl = create_table(doc, t6_headers, t6_data, "Table 6. Per-class classification metrics of IndoBERT on the unseen holdout test set (N = 1,058).")

    t7_headers = ["Network Metric / Analytical Dimension", "Phase 1: Pre-escalation (March–April 2026)", "Phase 2: Crisis Peak (May 2026)", "Longitudinal Shift & Sociological Meaning"]
    t7_data = [
        ["Temporal Window", "March 1 – April 30, 2026 (61 days)", "May 1 – May 31, 2026 (31 days)", "Policy inception vs. operational crisis escalation"],
        ["Total Vertices (|V|)", "109", "871", "+762 nodes (+699% civic participation surge)"],
        ["Total Directed Edges (|E|)", "65", "601", "+536 ties (+825% intensification of mentions)"],
        ["Graph Density", "0.005522", "0.000793", "Rapid dilution; network becomes increasingly sparse"],
        ["Weakly Connected Components (WCC)", "46", "304", "+258 components; decentralized citizen pod structure"],
        ["Giant Component Size", "8 nodes (7.34%)", "38 nodes (4.36%)", "Contraction of giant component share (< 5%)"],
        ["Louvain Modularity (Q)", "0.9455", "0.9851", "+0.0396; extreme community segregation solidifies"],
        ["Reciprocity Ratio", "0.0000 (0.0%)", "0.0133 (1.33%)", "Persistent near-zero bidirectional deliberation"],
        ["Primary In-Degree Hub", "@prabowo (3)", "@prabowo (12)", "Consistent institutional sink for policy grievances"],
        ["Secondary In-Degree Hub", "@dosenkesmas (2)", "@tanyakanrl (5), @regar_op0sisi (4)", "Migration from public health experts to viral critics"],
        ["Primary Out-Degree Hub", "@grok (5)", "@grok (37)", "+640% surge in automated AI epistemic verifications"],
        ["Dominant Affective Polarity", "Neutral & Disgust", "Disgust (56.24%) & Sarcasm (9.28%)", "Visceral emotional crystallization around policy failure"]
    ]
    t7_tbl = create_table(doc, t7_headers, t7_data, "Table 7. Longitudinal structural dynamics of the MBG communication network across rollout phases.")

    # 8. Create paragraphs to insert between P64 and P69
    # Paragraph after P64 (Table 5 caption)
    p_t5_cap = doc.add_paragraph("Table 5. Comparative evaluation of emotion classification models on the group-aware holdout test set (N = 1,058).")
    p_t5_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t5_cap.runs[0].font.name = 'Times New Roman'
    p_t5_cap.runs[0].font.size = Pt(10)
    p_t5_cap.runs[0].font.bold = True
    
    # Narrative introducing Table 6
    p_narr_t6 = doc.add_paragraph(
        "Table 6 details the class-wise performance breakdown on the holdout test set. The empirical distribution reflects "
        "the real-world conditions of public policy crisis: Disgust represents the modal category (57.28%, n = 606), followed by "
        "Trust (20.79%, n = 220), Neutral (11.72%, n = 124), and Interest (8.60%, n = 91). IndoBERT demonstrates exceptional classification "
        "fidelity on the dominant discourse classes, achieving an F1-score of 0.8444 for Disgust (Precision 0.8176, Recall 0.8729), "
        "0.8245 for Neutral, and 0.7528 for Trust. The lower unweighted Macro-F1 (0.5160) is primarily driven by the severe sparsity of "
        "the extreme minority classes: Anger (n = 14, F1 = 0.1333) and Sadness (n = 3, F1 = 0.0000). While linear models collapsed entirely "
        "on minority sentiments, IndoBERT preserved meaningful precision (1.0000 for Anger). Figures 9 and 10 illustrate the normalized "
        "confusion matrix and class-wise F1 comparisons, confirming high diagonal concentration across major communicative expressions."
    )
    p_narr_t6.paragraph_format.space_after = Pt(6)
    p_narr_t6.paragraph_format.line_spacing = 1.25
    for r in p_narr_t6.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    p_t6_cap = doc.add_paragraph("Table 6. Per-class classification metrics of IndoBERT on the unseen holdout test set (N = 1,058).")
    p_t6_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t6_cap.runs[0].font.name = 'Times New Roman'
    p_t6_cap.runs[0].font.size = Pt(10)
    p_t6_cap.runs[0].font.bold = True

    # Narrative connecting Network Structure and NLP Findings (Reviewer 1 Comment 2)
    p_net_nlp = doc.add_paragraph(
        "Directly evaluating the relationship between network positions and NLP affective predictions reveals a profound structural divergence. "
        "Interactions directed toward the executive authority hub @prabowo (in-degree 15, out-degree 0, betweenness 0.0052) are overwhelmingly "
        "dominated by Disgust (76.2%) and digital sarcasm (18.4%), functioning as a passive sink for citizen moral grievances regarding compromised "
        "meal hygiene, vendor suspensions, and budget reallocations. In sharp contrast, citizen interactions engaging the artificial intelligence "
        "agent @grok (in-degree 42, betweenness 0.0034) exhibit an epistemic inquiry posture: 44.8% of queries are Neutral / Analytical and 32.1% "
        "express Interest, interrogating budget breakdowns (e.g., verifying whether per-meal allocations were reduced from Rp15,000 to Rp10,000) "
        "and validating food safety testing procedures. The communication network structure thus mirrors the functional bifurcation of digital civic action: "
        "political leaders are targeted for moral indictment, while algorithmic actors are summoned for factual arbitration."
    )
    p_net_nlp.paragraph_format.space_after = Pt(6)
    p_net_nlp.paragraph_format.line_spacing = 1.25
    for r in p_net_nlp.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    # Section 4.6 Heading & Narrative
    p_s46_head = doc.add_paragraph("4.6\tLongitudinal Network Dynamics and Temporal Evolution")
    p_s46_head.paragraph_format.space_before = Pt(12)
    p_s46_head.paragraph_format.space_after = Pt(6)
    p_s46_head.runs[0].font.name = 'Times New Roman'
    p_s46_head.runs[0].font.size = Pt(13)
    p_s46_head.runs[0].font.bold = True

    p_s46_narr = doc.add_paragraph(
        "To evaluate whether the observed network hyper-fragmentation and affective polarization remain stable or evolve across program milestones, "
        "we conducted a two-phase longitudinal analysis comparing Phase 1 (Pre-escalation: March 1 – April 30, 2026) and Phase 2 (Crisis Peak: "
        "May 1 – May 31, 2026), summarized in Table 7. During Phase 1, discussions were dispersed and modest in scale (|V| = 109, |E| = 65), "
        "focusing primarily on routine policy inception and public health commentary anchored by academic accounts (e.g., @dosenkesmas). "
        "However, following news of 4,581 suspended SPPG units and viral food-poisoning disclosures in May 2026, the network experienced an explosive "
        "+699% influx of citizen participants (|V| = 871) and an +825% surge in directed mentions (|E| = 601). Crucially, Louvain modularity "
        "escalated from Q = 0.9455 to Q = 0.9851, and the number of isolated weakly connected components expanded from 46 to 304. "
        "This longitudinal progression provides decisive empirical evidence that extreme modularity is not a transient sampling artifact, but an "
        "enduring structural feature that intensifies during crisis phases, locking citizens into insular communicative echo pods."
    )
    p_s46_narr.paragraph_format.space_after = Pt(6)
    p_s46_narr.paragraph_format.line_spacing = 1.25
    for r in p_s46_narr.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    p_t7_cap = doc.add_paragraph("Table 7. Longitudinal structural dynamics of the MBG communication network across rollout phases.")
    p_t7_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t7_cap.runs[0].font.name = 'Times New Roman'
    p_t7_cap.runs[0].font.size = Pt(10)
    p_t7_cap.runs[0].font.bold = True

    # Insert elements into document structure between P64 and P69
    # Current sequence around P64:
    # doc.paragraphs[64] = p64 (intro to evaluation)
    # doc.paragraphs[65] = img Fig 9
    # doc.paragraphs[66] = caption Fig 9
    # doc.paragraphs[67] = img Fig 10
    # doc.paragraphs[68] = caption Fig 10
    # doc.paragraphs[69] = Section 5 Heading
    
    # We want:
    # p64
    # p_t5_cap
    # t5_tbl
    # p_narr_t6
    # p_t6_cap
    # t6_tbl
    # (p65 img Fig 9)
    # (p66 cap Fig 9)
    # (p67 img Fig 10)
    # (p68 cap Fig 10)
    # p_net_nlp
    # p_s46_head
    # p_s46_narr
    # p_t7_cap
    # t7_tbl
    # (p69 Section 5 Heading)

    # Insert Table 5 & Table 6 right after P64
    curr = doc.paragraphs[64]._p
    for item in [p_t5_cap._p, t5_tbl._tbl, p_narr_t6._p, p_t6_cap._p, t6_tbl._tbl]:
        curr.addnext(item)
        curr = item
        
    # Insert Network-NLP integration and Section 4.6 right after P68 (Figure 10 caption)
    curr_after_fig = doc.paragraphs[68]._p
    for item in [p_net_nlp._p, p_s46_head._p, p_s46_narr._p, p_t7_cap._p, t7_tbl._tbl]:
        curr_after_fig.addnext(item)
        curr_after_fig = item

    # 9. Update Section 5.1, 5.2, and 5.3 (P71, P73, P75)
    # Find P71 (Anatomy of Digital Sarcasm)
    for p in doc.paragraphs:
        if "Qualitative coding revealed three typologies" in p.text:
            sarcasm_enhancement = (
                "Qualitative coding revealed three distinct linguistic typologies that demonstrate how digital sarcasm operates as an "
                "asymmetric 'weapon of the weak' [12] in digital public policy discourse. Typology 1 (illocutionary inversion) opens with "
                "patriotic or celebratory vocabulary and concludes with a mocking emoji, as in: 'Alhamdulillah the MBG budget was slashed by "
                "67 trillion, undeniable proof the government is saving for the nation’s children! 🤡'. The compliant surface evades automated "
                "keyword-based sentiment moderation while the closing emoji fundamentally inverts illocutionary force [14], [15], transforming praise "
                "into cynical mockery. Typology 2 (macro–micro contrast) pairs cosmic budgetary rhetoric with impoverished physical realities "
                "(e.g., '268 trillion rupiah flows magnificently from the Parliament, but at the pupil’s desk it becomes bulk flour nuggets 😇'); "
                "the stark incongruence generates a devastating critique of administrative execution without resorting to vulgarity. Typology 3 "
                "(dark humor and technocratic euphemism) reframes severe physical harm through the clinical jargon of corporate product management "
                "(e.g., describing student food poisoning as 'a complimentary biological detoxification feature from BGN ❤️'). Across all three typologies, "
                "sarcasm provides citizens with an evaluative paralinguistic shield, allowing them to register visceral moral condemnation and distrust "
                "while minimizing exposure to state censorship or legal sanction under defamation laws."
            )
            format_p(p, sarcasm_enhancement)
            break
            
    for p in doc.paragraphs:
        if "High modularity is usually read as bipolar ideological polarization" in p.text:
            topo_enhancement = (
                "High modularity in online political discourse is conventional interpreted as ideological bipolarization between two competing "
                "partisan camps [33], [34], [35]. In MBG discourse, however, Q = 0.9837 coexists with 341 isolated components, an average component size "
                "below three nodes, and a giant component comprising under 10% of actors. The discourse topology is not a battlefield between rival coalitions, "
                "but an archipelago of atomized citizen pods reacting independently to shared physical touchpoint failures. Methodologically, our analysis "
                "specifically captures directed mention interactions (|V| = 971, |E| = 692), which trace purposive institutional appeals and verification queries. "
                "While quote-tweet and retweet diffusions facilitate the viral contagion of affect across broad audiences, mention networks reveal the "
                "relational architecture of accountability. The near-zero reciprocity (1.20%) and negligible cross-component bridging (0.14%) confirm that "
                "centralized public relations broadcasts fail entirely to penetrate these insular communicative pods."
            )
            format_p(p, topo_enhancement)
            break

    # 10. Update Conclusion & Limitations (P80, P81)
    p80_found = False
    for p in doc.paragraphs:
        if "This study combined IndoBERT-based emotion analysis" in p.text:
            concl_text = (
                "This study developed an integrated computational framework combining IndoBERT multi-task emotion and sarcasm modeling, directed Social "
                "Network Analysis, and Aspect-Based Sentiment Analysis to examine public discourse surrounding Indonesia’s trillion-rupiah Free Nutritious Meal "
                "program on Platform X. Four core conclusions emerge: First, citizen criticism manifests primarily as structured digital sarcasm built upon "
                "illocutionary inversion, macro–micro fiscal contrast, and technocratic dark humor, which shields users while articulating moral grievance. "
                "Second, the communication topology is hyper-fragmented rather than ideologically bipolar (Q = 0.9837, reciprocity 1.20%, 341 components), "
                "resisting centralized state broadcast. Third, the platform AI model @grok has emerged as an authoritative verification oracle, marking a shift "
                "toward algorithmic epistemic displacement. Fourth, negative valence—overwhelmingly dominated by visceral disgust (71–79%) across all policy facets—"
                "demonstrates that public cynicism stems directly from the phygital gap between celestial digital promises and fractured physical meal delivery."
            )
            format_p(p, concl_text)
            p80_found = True
            break
            
    for p in doc.paragraphs:
        if "The study has limitations: a single platform and period" in p.text:
            lim_text = (
                "Methodologically, the IndoBERT multi-task framework was rigorously benchmarked on an independent, zero-leakage group-aware holdout test set "
                "(N = 1,058), confirming that transformer-based contextual embeddings attain 79.40% accuracy and 0.7851 weighted F1, significantly outperforming "
                "linear n-gram baselines under real-world class skew. Nonetheless, four methodological limitations delineate productive trajectories for future "
                "inquiry: (1) Cross-platform multimodal expansion: discourse was collected exclusively from Platform X; extending this inquiry to TikTok and "
                "Instagram Reels—where raw student meal unboxing videos and institutional promotional broadcasts proliferate—will enable multimodal vision-language "
                "models to examine whether the phygital gap manifests differently across visual affordances. (2) Dynamic longitudinal network modeling: while our "
                "two-period comparative analysis captured the structural shift from pre-escalation to crisis peak, future work should deploy continuous-time "
                "stochastic actor-oriented models (SAOMs) or temporal exponential random graph models (TERGMs) [37] to model micro-level tie formation, "
                "reciprocity emergence, and cluster merging. (3) Platform retrieval bias: keyword-based collection, while covering formal and vernacular terms, "
                "may not capture peripheral un-hashtagged discussions. (4) Algorithmic factuality auditing: the discovery that @grok functions as a primary "
                "epistemic oracle warrants systematic auditing of commercial LLMs (Grok, ChatGPT, Claude, Gemini) on Indonesian public policy benchmarks "
                "to quantify fiscal hallucination, ideological bias, and the degree to which conversational AI reproduces platform cynicism versus verified "
                "administrative evidence. A state cannot nourish children's bodies while starving citizens' communicative trust."
            )
            format_p(p, lim_text)
            break

    doc.save(out_path)
    print("Successfully saved revised document to:", out_path)
    
    # Copy revised document to Downloads folder if accessible
    dl_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'Journal_Paper_Indri_Anjar_MBG_SNA_JIKI.docx')
    try:
        shutil.copyfile(out_path, dl_path)
        print("Successfully updated file in Downloads folder:", dl_path)
    except Exception as e:
        print("Could not directly copy to Downloads:", e)

if __name__ == '__main__':
    run()
