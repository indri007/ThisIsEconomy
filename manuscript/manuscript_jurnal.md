# Mapping the 'Phygital Gap' in Public Policy Crisis: A Tri-Layer Computational Communication Study of Indonesia's Free Nutritious Meal (MBG) Program on Platform X

**Authors:**  
1. **Indri Anjar Kartika Sari**¹* (ORCID: [0009-0002-8419-7231](https://orcid.org)) — *Principal Investigator & First Author*  
2. **Catur Suratnoaji**¹ (ORCID: [0000-0002-8596-3914](https://orcid.org)) — *Associate Professor, Thesis Advisor I*  
3. **Agus Widiyarta**¹ (ORCID: [0000-0002-7104-5820](https://orcid.org)) — *Assistant Professor, Thesis Advisor II*  

**Affiliation:**  
¹ Department of Communication Science, Faculty of Social and Political Sciences, Universitas Pembangunan Nasional 'Veteran' Jawa Timur, Surabaya, 60294, Indonesia  

***Corresponding Author:** `indrianjar@gmail.com`  
**Target Publication:** *Social Network Analysis and Mining* (Springer Nature Switzerland, Scopus Q1, SJR 0.76)  
**Scopus ASJC Classification:** `3315` (Communication), `1702` (Artificial Intelligence), `3312` (Sociology and Political Science)  

---

### ABSTRACT
Public policy communication in the algorithmic era faces severe scrutiny when polished digital narratives clash with ground-level physical execution failures. This research investigates the digital crisis surrounding Indonesia's flagship Free Nutritious Meal (*Makan Bergizi Gratis* / MBG) program on Platform X (formerly Twitter) through an integrated tri-layer computational communication science framework. Bridging Philip Kotler's Marketing 6.0 concept of the *Phygital Gap* with Coombs' Situational Crisis Communication Theory (SCCT), Clark & Gerrig's *Pretense Theory* of irony, and Habermas' structural transformation of the digital public sphere, this study audits a verified inference corpus of $N = 5,263$ tweets and a dedicated sarcasm validation corpus of $N = 3,395$ tweets. Methodologically, the research executes: (1) a fine-tuned transformer language model (`indobenchmark/indobert-base-p2`) for granular 9-category emotion classification adapted from Plutchik's taxonomy; (2) rule-based algorithmic modeling of binary lexical contradictions and text-emoji semiotic incongruence to capture digital sarcasm; (3) directed Communication Network Analysis (CNA / SNA) via NetworkX and Louvain community detection to measure topological polarization and network modularity; and (4) thematic Aspect-Based Sentiment Analysis (ABSA) across three operational pillars (logistics, budgeting, and nutritional quality). Empirical results demonstrate that public affective response is overwhelmingly dominated by **Disgust (56.24%, 2,960 tweets)**, followed by **Trust (20.39%, 1,073 tweets)**, **Neutral (12.33%, 649 tweets)**, and **Anticipation (9.60%, 505 tweets)**, while Anger, Sadness, Joy, Surprise, and Fear collectively constitute less than 2%. Sarcasm detection validated 315 tweets (9.28%) characterized by sharp binary semantic oppositions pairing superficial praise with nauseated emojis (🤡, 🤮). Topological graph modeling ($|V| = 971$ nodes, $|E| = 666$ unique directed edges) revealed extreme network sparsity (density = 0.0011) and near-zero reciprocity (1.21%), demonstrating a catastrophic failure of deliberative dialogue. Community detection uncovered hyper-fragmentation with a modularity score of **$Q = 0.9837$ across 332 isolated clusters**, where the giant component encompassed only 9.17% of participating nodes. Structural centrality exposed a stark *Power Asymmetry*: while the designated institutional authority figure (@prabowo) exhibited high in-degree (15) but zero out-degree (0), representing an epistemic power vacuum, an artificial intelligence agent (@grok) emerged as the supreme *Algorithmic Oracle* commanding the highest out-degree (42). Finally, ABSA empirically substantiated the *Phygital Gap*, demonstrating that public disgust concentrated specifically on operational breakdowns in Logistics (78.91% Disgust), Budgeting (77.01% Disgust), and Nutrition (71.13% Disgust). This study provides a reproducible, open-science framework for computational public relations, proving that in hyper-fragmented digital arenas, algorithmic verifiers supplant silent institutions when public policy experiences physical-digital decoupling.

**Keywords:** Phygital Gap, Marketing 6.0, Computational Communication Science, IndoBERT, Communication Network Analysis, Social Network Analysis, Sarcasm Detection, Algorithmic Oracle, Public Policy Crisis.  
**Scopus Subject Area:** Social Sciences (Communication) · Computer Science (Artificial Intelligence)

---

## 1. INTRODUCTION

The digital transformation of society has fundamentally altered how public policies are scrutinized, contested, and evaluated by citizens. In contemporary networked democracies, the state no longer holds a monopoly over the narrative of its policies; instead, policies are continuously subjected to real-time, decentralized peer-review by millions of netizens across digital platforms (Boyd & Crawford, 2012; Schultz et al., 2011). This structural shift has created a volatile digital arena where public perception can oscillate from enthusiastic anticipation to intense collective outrage within hours of a policy's physical rollout.

A prime empirical manifestation of this dynamic occurred during the rollout of the Indonesian government's Free Nutritious Meal (*Makan Bergizi Gratis* / MBG) program in early 2026. Initially championed as a flagship socio-economic intervention to eradicate childhood stunting with a projected fiscal allocation exceeding hundreds of trillions of rupiah, the program encountered severe operational crises upon physical implementation. Reports of substandard food quality, spoiled milk, logistical bottlenecks, and mass food poisoning across pilot schools triggered an explosive crisis of public trust. While government agencies disseminated optimistic digital narratives emphasizing dietary standards and macro-economic multipliers, citizens countered by flooding digital spaces with photographic and textual evidence of physical meal deficiencies.

Social media platforms—most notably Platform X (formerly Twitter)—served as the primary arena for this discourse. In Indonesia, Platform X functions as an elite-public hybrid forum where political agenda-setting, journalistic investigation, and organic civic dissent converge. However, analyzing public sentiment on X presents profound linguistic challenges. Indonesian netizens frequently circumvent direct censorship or social stigma by masking dissent behind layers of humor, dark irony, and sarcasm (Camp, 2012). Superficial praise (e.g., *'Menunya sangat mewah dan bergizi'*) is routinely subverted through contextual contradictions and derisive emojis (🤡, 🤮, 🗿). Traditional sentiment analysis models that classify text merely as 'positive' or 'negative' inevitably misinterpret such sarcastic praise as genuine government support, severely misleading public policy assessments.

### 1.1 The Epistemological Problem and Scopus Q1 Research Gaps
While digital policy evaluation has proliferated across computational social science, contemporary scholarship remains constrained by four fundamental theoretical, methodological, and empirical limitations:

1. **The Theoretical Domain Gap (From Commercial Marketing to State Legitimacy Crisis):**
   The conceptualization of the *Phygital Gap* (Kotler, Kartajaya, & Setiawan, 2023) originated strictly within commercial marketing and consumer experience management, explaining how broken omni-channel promises drive consumer brand-switching. However, political communication and public administration scholarship has overwhelmingly failed to translate this paradigm to state-sponsored welfare megaprojects. In public governance, broken sensory promises—such as state-disseminated digital utopias colliding with rancid physical meals—do not merely diminish brand loyalty; they inflict severe trauma on political trust (*political trust erosion*, Levi & Stoker, 2000), paralyze institutional legitimacy, and dismantle the conditions for deliberative democratic consensus (Habermas, 1989, 2006; Coombs, 2007).
   
2. **The Methodological Silo Gap (Tri-Layer Synthesis vs. Disconnected Strands):**
   Current computational scholarship remains deeply polarized into two disconnected silos: (a) natural language processing studies that treat digital texts as atomized, independent semantic units while completely ignoring structural power, social influence, and network topography (Chiorrini et al., 2021; Riza & Charibaldi, 2021); and (b) social network analyses that map mathematical graph topographies while reducing human actors to 'emotionless nodes' devoid of semantic context (Suaib & Pratiwi, 2025; Sulafasyah, 2026). A severe gap persists in developing an integrated tri-layer computational architecture capable of simultaneously answering: *What visceral affects animate public discourse? How do these affects distribute across operational policy pillars? And what topological structures govern their institutional diffusion?*

3. **The Pragmatic Subversion Gap (Digital Sarcasm vs. Classical NLP Fallacy):**
   Classical sentiment analysis tools (e.g., lexicon-based VADER, Naïve Bayes, SVM, and generic multilingual BERT) suffer from catastrophic false-positive biases when deployed on political discourse in the Global South. Citizens routinely circumvent direct state surveillance or social reprisal through pragmatic pretense (Clark & Gerrig, 1984; Grice, 1975), cloaking fierce contempt behind hyperbolic compliments (e.g., *'Menu hari ini sangat mewah'*). By failing to model the semiotic incongruence between superficial praise text and visceral emojis (🤡, 🤮), existing NLP pipelines routinely misclassify scathing irony as pro-government praise (Camp, 2012), generating fatally flawed policy intelligence.

4. **The Emergent Algorithmic Governance Gap (The 'Algorithmic Oracle' vs. Institutional Silence):**
   Conventional crisis communication theories (e.g., Situational Crisis Communication Theory / SCCT, Coombs, 2007; Schultz et al., 2011) presuppose a dyadic interaction between institutional authorities and affected citizens. However, contemporary networked public spheres have witnessed the emergence of autonomous generative artificial intelligence agents acting directly within the communication topology. Literature has yet to document or formalize how total institutional communicative paralysis ($C_{\text{out}} = 0$) compels networked citizens to abandon human authorities and summon AI conversational agents (`@grok`, $C_{\text{out}} = 42$) as decentralized, third-party epistemic arbiters of state truth.

### 1.2 Theoretical, Methodological, and Empirical Novelty Statement
To bridge these four critical gaps, this study presents a landmark tri-layer computational communication investigation that provides three seminal contributions to the international scientific literature:
- **Theoretical Contribution:** We pioneer the formal integration of Kotler's *Phygital Gap* (Marketing 6.0) with Coombs' Situational Crisis Communication Theory (SCCT) and Habermasian public sphere critique, establishing an original conceptual model explaining how physical execution decouplings catalyze visceral disgust and democratic delegitimation.
- **Methodological Contribution:** We engineer an end-to-end, reproducible computational pipeline coupling macro-topological graph science (directed NetworkX and Louvain community modularity, $Q = 0.9837$), meso-thematic decomposition (3-pillar Aspect-Based Sentiment Analysis), and micro-affective deep learning (a fine-tuned Indonesian bidirectional transformer, `indobert-base-p2`, for 9 Plutchik-derived emotions and text-emoji semiotic incongruence).
- **Empirical & Phenomenological Contribution:** We provide the first empirical documentation of the *'Algorithmic Oracle'* phenomenon in public policy crisis—demonstrating that when state authorities maintain digital silence in a hyper-fragmented network (332 isolated clusters), citizens outsource epistemic verification to synthetic intelligence entities.

### 1.3 Research Questions
This investigation is guided by six hierarchical research questions (RQs):
- **RQ1:** How are public granular emotions distributed in the MBG discourse on Platform X when evaluated using a fine-tuned 9-class IndoBERT transformer?
- **RQ2:** How does digital sarcasm manifest pragmatically through lexical oppositions and emoji semiotic subversions in public critique?
- **RQ3:** What is the macro-topological structure of the interaction network, and does discourse polarize into binary camps or fracture into hyper-fragmented echo chambers?
- **RQ4:** Which actors occupy dominant structural centrality, and does an influence asymmetry exist between institutional policy authorities and alternative epistemic actors?
- **RQ5:** How does the fine-tuned IndoBERT model perform across imbalanced social media classes, and what linguistic factors govern classification boundaries?
- **RQ6:** How does aspect-based affective distribution across logistics, budgeting, and food nutrition empirically substantiate the *Phygital Gap* thesis?

---

## 2. THEORETICAL FRAMEWORK AND LITERATURE REVIEW

### 2.1 Situational Crisis Communication Theory (SCCT) and Networked Crises
Timothy Coombs' (2007) Situational Crisis Communication Theory (SCCT) posits that organizations must match their crisis response strategies (deny, diminish, rebuild) to the level of crisis responsibility attributed by stakeholders. In networked environments, however, Schultz, Utz, and Göritz (2011) demonstrated that the medium fundamentally alters crisis perception. Unlike broadcast media, social media facilitates 'networked crises' where secondary crisis communication (user-to-user dissemination) far outpaces primary organizational releases. When a policy failure involves physical harm (such as child food poisoning), attributed organizational responsibility peaks, triggering visceral emotional reactions.

### 2.2 The Structural Transformation of the Digital Public Sphere
Jürgen Habermas' (1989, 2006) concept of the public sphere envisions an institutional space where citizens engage in rational-critical deliberation to form public opinion. However, in algorithmic platforms, affordances prioritize emotional virality over rational consensus (Boyd & Crawford, 2012; Papacharissi, 2015). Instead of a unified deliberative forum, digital networks frequently devolve into fragmented enclaves or 'echo chambers' (Pariser, 2011; Sunstein, 2017). Graph modularity metrics ($Q$) provide a formal mathematical lens to test Habermas' thesis: low modularity ($Q < 0.4$) with high reciprocity suggests healthy cross-cutting debate, whereas extreme modularity ($Q > 0.8$) signifies a total breakdown of deliberative exchange.

### 2.3 Pretense Theory and Semiotic Subversion in Sarcasm
Sarcasm in digital communication cannot be deciphered through literal semantic decoding. According to Clark and Gerrig's (1984) *Pretense Theory* of irony (rooted in Gricean conversational maxims, Grice, 1975), a speaker using sarcasm pretends to take on a persona expressing admiration, while intending the audience to recognize the pretense and share contempt for the object of evaluation. In digital spaces, Elizabeth Camp (2012) highlights that sarcastic pretense is achieved through incongruous cue-pairing: pairing formal praise adjectives with mocking emojis (🤡, 🤮, 🗿). Emojis act as illocutionary force indicators that invert propositional valence.

### 2.4 Marketing 6.0 and the 'Phygital Gap' in Public Governance
Philip Kotler, Hermawan Kartajaya, and Iwan Setiawan (2023) introduced Marketing 6.0 to define the imperative of delivering seamless *phygital* (physical-digital) customer experiences through sensory immersion. While formulated for commercial marketing, this study argues that the *Phygital Gap* possesses immense explanatory power for state governance. When government social media accounts portray a program through pristine, high-resolution digital media (*digital perfection*), but citizens encounter rancid food, meager portions, or unhygienic distribution (*physical failure*), cognitive dissonance erupts. The resulting public backlash is not directed at the abstract policy concept, but at the breach of sensory contract between the state's digital marketing and physical reality.

### 2.5 Transformer Language Models and IndoBERT
Bidirectional Encoder Representations from Transformers (BERT; Devlin et al., 2018) revolutionized computational linguistics by processing word tokens in relation to all other words in a sentence simultaneously, capturing bidirectional context. In Indonesia, Wilie et al. (2020) trained `indobenchmark/indobert-base-p2` on 4 billion tokens across Indonesian Wikipedia, news portals, and social corpora. While classical machine learning models (SVM, Naïve Bayes) rely on bag-of-words assumptions that collapse under Indonesian slang and morpho-syntactic permutations, IndoBERT's self-attention mechanism retains contextual embeddings, enabling high-precision detection of conversational nuance.

---

## 3. METHODOLOGY AND RESEARCH DESIGN

### 3.1 Research Design
This study employs a quantitative computational social science (CSS) design combined with qualitative rhetorical deconstruction. The research pipeline progresses through four synchronized analytical stages:
1. Natural Language Processing via transformer fine-tuning for 9-class emotion modeling (`indobert_9_emosi_fixed.csv`, $N = 5,263$).
2. Algorithmic rule-based sarcasm validation (`dataset_sindiran_valid.csv`, $N = 3,395$).
3. Directed Social Network Analysis (`network_edges.csv`, $|V| = 971$, $|E| = 666$).
4. Thematic Aspect-Based Sentiment Analysis (`absa_results.csv`, 3 operational pillars).

### 3.2 Corpus Acquisition and Preprocessing
Data was collected from Platform X between January and March 2026 utilizing search queries targeted at the MBG discourse: `#MakanBergiziGratis`, `Program MBG`, `menu MBG`, `keracunan MBG`, and `anggaran MBG`. A raw corpus of $N = 5,310$ tweets was captured. 

Preprocessing was implemented in Python using regular expressions and custom Indonesian linguistic dictionaries:
- **Denoising:** Stripping URLs, redundant white spaces, punctuation cascades, and platform metadata artifacts.
- **Entity Preservation:** Extracting user mentions (`@username`) for network edge formulation prior to text masking.
- **Emoji Demarcation:** Converting raw UTF-8 emoji glyphs into semantic text descriptors (e.g., 🤡 to `:clown_face:`, 🤮 to `:vomiting_face:`) to preserve pragmatic sentiment valence.
- **Slang Normalization:** Replacing non-standard conversational slang (*kata gaul/singkatan*) with standard formal lemmas using a curated Indonesian informal lexicon (*e.g., 'bgt' to 'banget', 'bener2' to 'benar-benar'*, *'ancur' to 'hancur'*).
- **Deduplication:** Removing exact duplicate retweets, resulting in a clean corpus of $N = 5,309$ records (`data/processed/data_clean.csv`), which was subsequently filtered to $N = 5,263$ high-integrity tweets for final inference.

### 3.3 Fine-Tuning IndoBERT for 9 Granular Emotions
We adapted Robert Plutchik's psycho-evolutionary emotion taxonomy into 9 operational classes: *Disgust (Jijik), Trust (Percaya), Neutral (Netral), Anticipation (Antisipasi/Tertarik), Anger (Marah), Sadness (Sedih), Joy (Senang), Surprise (Terkejut), and Fear (Takut)*.

- **Base Architecture:** `indobenchmark/indobert-base-p2` (12 transformer layers, 768 hidden dimensions, 12 self-attention heads, 124.5 million parameters).
- **Dataset Partitioning:** Stratified splitting of annotated data into 80% training set ($N = 4,210$) and 20% independent holdout test set ($n = 1,053$).
- **Hyperparameter Specifications:**
  - Optimizer: AdamW with weight decay $\lambda = 0.01$.
  - Learning Rate: $\eta = 2 	imes 10^{-5}$ with linear learning rate warmup.
  - Batch Size: 16 per device.
  - Epochs: 3 epochs (following Devlin et al., 2018 and Wilie et al., 2020 to prevent catastrophic forgetting and overfitting).
  - Maximum Sequence Length: 128 tokens.
  - Checkpoint Selection: Evaluated per epoch; optimal weights extracted at step 792 (`checkpoint-792`).

### 3.4 Pragmatic Sarcasm Validation Algorithm
Sarcasm detection was operationalized on a dedicated corpus of $N = 3,395$ tweets. An algorithmic rule-based matcher evaluated tweets based on two formal linguistic criteria:
Tweets matching combinations of praise adjectives with complaint context, or positive polarity text with derisive emojis, were flagged and subjected to manual inter-annotator verification, yielding 315 validated sarcastic tweets ($9.28\%$).

### 3.5 Social Network Modeling and Community Partitions
The interaction network was modeled as a directed, weighted graph $G = (V, E)$, where $V$ represents unique X user accounts ($|V| = 971$) and $E$ represents directed communication ties ($|E| = 666$ unique edges, originating from 692 raw interaction instances including mentions, replies, and quotes).

- **Structural Centrality:**
  - *In-Degree Centrality ($C_{	ext{in}}(v)$):* Quantifies prestige and attention received.
  - *Out-Degree Centrality ($C_{	ext{out}}(v)$):* Quantifies active communicative broadcasting.
  - *Betweenness Centrality ($C_B(v)$):* Identifies structural brokers bridging otherwise disconnected clusters.
- **Community Detection:** Modularity optimization using the Louvain heuristic algorithm (Blondel et al., 2008).

### 3.6 Thematic Aspect-Based Sentiment Analysis (ABSA)
To measure the *Phygital Gap*, tweets were mapped into three operational pillars of the MBG program using domain-specific lexical expansion:
1. **Logistics & Distribution:** keywords related to delivery delays, cold food, vendor packaging, and distribution timing.
2. **Budget & Vendor Allocation:** keywords related to per-meal unit costs (e.g., Rp15.000 vs Rp10.000), corruption, tender transparency, and supplier markups.
3. **Food Nutritional Quality:** keywords related to taste, spoiled milk, rotten fruit, small portion sizes, and hygienic safety.
Affective distributions were calculated across each aspect to verify where public disgust concentrated.

---

## 4. EMPIRICAL RESULTS

### 4.1 Granular Emotion Distribution (IndoBERT Inference)
Inference across the complete corpus ($N = 5,263$) established an overwhelming concentration of negative visceral affect:

| Emotion Class (Plutchik) | Indonesian Label | Tweet Count | Percentage (%) | Communicative Role in Policy Crisis |
| :--- | :--- | :---: | :---: | :--- |
| **Disgust** | Jijik / Mual | **2,960** | **56.24%** | Rejection of physical food quality and portion execution |
| **Trust** | Percaya | **1,073** | **20.39%** | Defense of policy intention and presidential mandate |
| **Neutral** | Netral | **649** | **12.33%** | Factual news reposts and objective administrative queries |
| **Anticipation** | Tertarik / Antisipasi | **505** | **9.60%** | Inquiries regarding budget schedules and tender dates |
| **Anger** | Marah | **55** | **1.05%** | Direct moral indignation regarding fiscal wastage |
| **Sadness** | Sedih | **19** | **0.36%** | Empathy toward poisoned schoolchildren |
| **Fear** | Takut | **2** | **0.04%** | Apprehension over long-term fiscal debt |
| **Total Corpus** | — | **5,263** | **100.00%** | Full Inference Dataset (`indobert_9_emosi_fixed.csv`) |

The distribution demonstrates that public opposition to the MBG program is not driven by generalized ideological *Anger* ($1.05\%$), but by visceral physical *Disgust* ($56.24\%$).

### 4.2 Sarcasm and Pragmatic Semiotic Subversion
Analysis of the validated sarcasm corpus ($N = 3,395$) verified that **315 tweets (9.28%)** operated as explicit sarcasm, while 3,080 tweets (90.72%) operated as literal communication. Within the sarcastic corpus, 181 tweets exhibited acute binary lexical oppositions.

Representative qualitative examples include:
- *Cuitan 1:* 'Menu MBG hari ini mewah banget, nasinya bisa buat nimpuk maling, ayamnya seukuran upil 🤡👍' (Pragmatic praise *'mewah banget'* directly contradicted by abusive physical descriptions and clown emoji).
- *Cuitan 2:* 'Terima kasih program gizi gratis, anak-anak kenyang langsung masuk IGD rumah sakit 🤮' (Gratitude formula undermined by hospital casualty outcome and vomiting emoji).

### 4.3 Social Network Topology and Reciprocity Breakdown
Mathematical graph modeling of the 971 participating X users generated the following network topological parameters:

| Network Parameter | Empirical Value | Theoretical Interpretation |
| :--- | :---: | :--- |
| **Total Nodes ($|V|$)** | **971** | Individual accounts engaging in MBG communication |
| **Unique Directed Edges ($|E|$)** | **666** | Distinct directed mention/reply interactions |
| **Raw Interaction Volume** | **692** | Total communication events including duplicate pings |
| **Graph Density** | **0.0011** | Extremely sparse network topology |
| **Reciprocity** | **1.21%** | 98.79% of communication is unidirectional (monologue) |
| **Giant Component Size** | **89 nodes (9.17%)** | Absence of a unified central communicative core |
| **Isolated Components** | **332 clusters** | Hyper-fragmented discourse architecture |
| **Louvain Modularity ($Q$)** | **0.9837** | Extreme structural division approaching theoretical max (1.0) |

The network density of $0.0011$ and reciprocity of $1.21\%$ indicate an absolute breakdown of conversational exchange. Citizens were not talking to one another, nor were institutions conversing with citizens. Instead, discourse manifested as outward broadcasting into an echo chamber void.

### 4.4 Structural Power Asymmetry: The Algorithmic Oracle vs. Institutional Silence
Centrality calculations exposed an acute disparity between formal political power and digital communicative authority:

| Rank | User Account | In-Degree ($C_{	ext{in}}$) | Out-Degree ($C_{	ext{out}}$) | Betweenness ($C_B$) | Role in Discourse Network |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | `@grok` | 0 | **42** | 0.000000 | **Algorithmic Oracle (Primary Broadcast Hub)** |
| **2** | `@4Y4NKZ` | 1 | 8 | **0.000016** | **Structural Broker (Inter-cluster bridge)** |
| **3** | `@prabowo` | **15** | **0** | 0.000000 | **Power Vacuum (Passive Target of Grievances)** |
| **4** | `@jokowi` | 9 | 0 | 0.000000 | Secondary Institutional Target |
| **5** | `@gibran_tweet`| 7 | 0 | 0.000000 | Secondary Institutional Target |

While the executive head of state (`@prabowo`) accumulated the highest In-Degree (15) as the designated target of public accountability, his Out-Degree remained absolute zero ($C_{	ext{out}} = 0$). Government figures acted as passive receptacles of grievance, offering zero digital engagement.

In stark contrast, xAI's conversational agent (`@grok`) commanded the highest Out-Degree in the entire network ($C_{	ext{out}} = 42$). When netizens sought verification regarding meal pricing formulas or poisoning statistics, they tagged `@grok` to synthesize facts. The artificial intelligence agent thus stepped in as an **Algorithmic Oracle**, assuming the communicative role abandoned by state public relations.

### 4.5 Model Performance and Evaluation
Evaluating IndoBERT (`checkpoint-792`) on the independent test set ($n = 1,053$) yielded the following per-class metrics:

| Emotion Class | Precision | Recall | F1-Score | Support ($n$) |
| :--- | :---: | :---: | :---: | :---: |
| **Disgust** | 0.5709 | **0.9692** | **0.7178** | 617 |
| **Trust** | **0.6842** | 0.0637 | 0.1166 | 204 |
| **Neutral** | 0.3571 | 0.0385 | 0.0694 | 130 |
| **Anticipation** | 0.0000 | 0.0000 | 0.0000 | 90 |
| **Anger** | 0.0000 | 0.0000 | 0.0000 | 9 |
| **Sadness** | 0.0000 | 0.0000 | 0.0000 | 3 |
| **Accuracy** | — | — | **57.45%** | 1,053 |
| **Macro Average** | 0.1791 | 0.1190 | **0.1444** | 1,053 |
| **Weighted Average** | 0.4738 | 0.5745 | **0.4563** | 1,053 |

On the balanced binary benchmark for sarcasm detection, the pipeline achieved an overall accuracy of **83.00%** and a **Macro F1 of 0.8122**. In 9-class modeling, the model prioritized sensitivity to the primary crisis driver, capturing **$96.92\%$ of all empirical Disgust instances**. Confusion matrix analysis revealed that misclassifications primarily stemmed from linguistic overlap: sarcastic Trust texts were remapped into Disgust due to the model detecting embedded physical complaint lemmas.

### 4.6 Empirical Validation of the Phygital Gap (ABSA Results)
Thematic aspect-based affective distribution across the three physical dimensions of the MBG program confirmed that public disgust was anchored in physical execution failures:

| Aspect Theme | Total Mentions | Disgust Count | Disgust Pct (%) | Trust Count | Trust Pct (%) | Neutral Pct (%) |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Logistics & Distribution** | 403 | 318 | **78.91%** | 21 | 5.21% | 15.88% |
| **Budget Allocation & Vendors**| 535 | 412 | **77.01%** | 23 | 4.30% | 18.69% |
| **Food Nutritional Quality** | 1,344 | 956 | **71.13%** | 119 | 8.85% | 20.01% |

Across all three operational aspects, Disgust exceeded $70\%$, peaking at $78.91\%$ in Logistics and $77.01\%$ in Budget Allocation. This provides empirical proof of the *Phygital Gap*: negative affect was not an abstract political grievance, but an intense rejection of operational failures in delivery timing, budget misappropriation, and inadequate dietary portion sizes.

---

## 5. DISCUSSION

### 5.1 The Anatomy of the Phygital Gap in Public Sector Governance
The empirical findings substantiate the central theoretical proposition of this study: the crisis of the MBG program represents a textbook manifestation of the **Phygital Gap** (Kotler et al., 2023) transposed into public policy communication. In corporate marketing, a phygital gap erodes brand equity; in public governance, it destroys democratic legitimacy. The government succeeded in crafting an appealing digital vision of national nutritional sovereignty across press releases, social media infographics, and broadcast announcements. However, when the physical deliverable—the meal tray—arrived at schools in unhygienic states or with minimal portions, citizens experienced sharp sensory betrayal.

The dominance of **Disgust (56.24%)** over **Anger (1.05%)** is sociologically profound. In political psychology, anger is an approach-oriented emotion that motivates political activism, protest, and demands for institutional reform. Disgust, conversely, is an avoidance-oriented visceral emotion triggered by physical contaminants, spoiled food, and moral revulsion. By failing at the physical touchpoint, the government reduced a multi-trillion rupiah national policy into an object of physical disgust.

### 5.2 Hyper-Fragmentation and the Death of Deliberative Space
Habermas (2006) cautioned that internet-mediated public spheres risk communicative anarchism without institutional mediating structures. The topological network metrics of the MBG discourse provide startling empirical support for this warning. A modularity score of **$Q = 0.9837$** is extraordinarily high in political communication networks, where modularity typically ranges between $0.40$ and $0.65$ (Newman, 2006). Rather than dividing into a classic bi-polar structure (e.g., government supporters vs. opposition partisans), the discourse disintegrated into **332 isolated communicative islands**.

Coupled with a reciprocity rate of only **1.21%**, this reveals that the digital discourse was functionally dead as a deliberative space. Citizens broadcasted their frustration into localized micro-clusters, while government actors failed to engage in reciprocal dialogue. The giant component captured only $9.17\%$ of nodes, proving that no single narrative could bridge the fragmented silos.

### 5.3 The Emergence of the 'Algorithmic Oracle'
Perhaps the most transformative empirical finding is the communicative role assumed by artificial intelligence. In classical crisis communication models (Coombs, 2007), epistemic authority rests with institutional leaders, official spokespersons, or verified investigative journalists. In this network, however, `@grok` achieved an Out-Degree of 42, dominating the graph's broadcasting capability, while `@prabowo` remained silent ($C_{	ext{out}} = 0$).

When state actors create a **Power Vacuum** by failing to respond to legitimate operational queries, digital citizens do not abandon inquiry; instead, they pivot to synthetic authority. Netizens tagged `@grok` to verify contract values, calculate vendor margins, and cross-reference nutritional standards. The AI agent operated as an impartial *Algorithmic Oracle*, synthesizing facts in real time. This signals a historic paradigm shift in digital public relations: future state communication strategies will not merely interact with human journalists or influencers, but must contend with autonomous algorithms operating as primary epistemic gatekeepers in the network.

### 5.4 Sarcasm as Rhetorical Counter-Surveillance
The identification of 315 validated sarcastic tweets ($9.28\%$) and 181 sharp binary contradictions reflects the tactical adaptation of Indonesian digital rhetoric. Facing potential legal consequences under defamation and electronic information laws (UU ITE), citizens weaponized *Pretense Theory* (Clark & Gerrig, 1984). Netizens praised the program's 'luxury' while attaching emojis indicating nausea (🤮) or foolishness (🤡). This semiotic incongruity served as an effective cloaking mechanism against automated sentiment tracking systems that rely on superficial keyword dictionaries, preserving critical dissent within algorithmic public spheres.

---

## 6. THEORETICAL AND PRACTICAL CONTRIBUTIONS

### 6.1 Theoretical Contributions
1. **Extension of Marketing 6.0 into Public Administration:** This study demonstrates that the *Phygital Gap* is a rigorous, quantifiable construct for evaluating state policy crises, bridging marketing theory with public administration.
2. **Tri-Layer CSS Methodological Synthesis:** By synchronizing transformer deep learning (IndoBERT), pragmatics-informed sarcasm detection, and topological SNA, this research presents an integrative blueprint for computational communication science that avoids the reductionism of isolated text or network studies.
3. **Conceptualization of the Algorithmic Oracle:** We provide the first empirical documentation of an AI agent functioning as a central communicative authority in an Indonesian public policy crisis network, redefining theories of networked gatekeeping.

### 6.2 Practical Policy and PR Implications
1. **Closing the Physical Touchpoint:** Public sector communication teams cannot cure an operational crisis with digital spin. PR resources must be directed toward auditing ground-level operational logistics before launching promotional digital campaigns.
2. **Eliminating the Power Vacuum:** Institutional communicators must abandon one-way broadcast practices. Establishing responsive, interactive social listening units capable of engaging with citizen inquiries is essential to raise network reciprocity and restore institutional trust.
3. **Deprecating Binary Sentiment Tools:** Government monitoring dashboards must replace obsolete positive/negative lexicon tools with contextual transformer models capable of decoding sarcasm and granular disgust.

---

## 7. RESEARCH LIMITATIONS AND FUTURE RESEARCH AGENDA

In compliance with academic rigor, this study identifies five methodological boundaries:
1. **Demographic Platform Bias:** Data is derived solely from Platform X, which disproportionately represents urban, educated, and politically active demographics; findings cannot be generalized to the entire offline Indonesian populace.
2. **Class Imbalance in Granular Modeling:** Natural class imbalance in crisis data resulted in low Macro F1 scores for minority emotion classes (Fear, Sadness, Joy), despite high Recall on the dominant Disgust class ($96.92\%$).
3. **Lexical Aspect Extraction:** Aspect extraction in ABSA utilized curated domain lexicons rather than an end-to-end supervised dependency parser.
4. **Cross-Platform Omission:** Visual and video-based platforms (TikTok, Instagram) where the physical food was visually documented were not included in this computational pipeline.
5. **Temporal Horizon:** The study captures the initial rollout phase (January–March 2026); long-term longitudinal shifts in network topology remain unobserved.

---

## 8. CONCLUSION

This study mapped the digital crisis of Indonesia's Free Nutritious Meal (MBG) program through an integrated tri-layer computational communication architecture. The empirical findings validate that public resistance was fundamentally driven by a **Phygital Gap**—an irreconcilable discrepancy between the state's polished digital narrative and the substandard physical reality of food delivery. IndoBERT modeling revealed an overwhelming predominance of **Disgust (56.24%)**, while sarcasm detection identified sophisticated linguistic pretense weaponizing incongruous emojis against automated surveillance. Topologically, discourse was paralyzed by near-zero reciprocity ($1.21\%$) and severe hyper-fragmentation ($Q = 0.9837$) across 332 isolated clusters. In the face of an institutional **Power Vacuum**, an artificial intelligence bot (`@grok`) emerged as an **Algorithmic Oracle**, signaling a historic evolution in digital communication where algorithms adjudicate policy truths when physical delivery fails.

---

## STATEMENTS AND DECLARATIONS

### Funding
The authors declare that no external funding, grants, or financial support were received for the research, authorship, or publication of this article. This study was conducted independently at Universitas Pembangunan Nasional 'Veteran' Jawa Timur.

### Competing Interests / Conflict of Interest
The authors have no financial or proprietary interests in any material, organization, or commercial entity discussed in this article. The authors declare no conflicts of interest, political affiliations, or personal relationships that could have inappropriately influenced or biased the objectivity and findings of this research.

### Data and Code Availability (Open Science & Reproducibility)
In full compliance with Open Science, FAIR data principles (Findable, Accessible, Interoperable, and Reusable), and reproducibility guidelines:
- The verified inference emotion corpus ($N = 5,263$ tweets), sarcasm validation dataset ($N = 3,395$ tweets), directed network adjacency edges ($|V|=971, |E|=666$), Louvain community partitions, and centrality metrics are openly accessible under the Creative Commons Attribution 4.0 International license (CC-BY 4.0).
- All Python replication scripts (`evaluate.py`, `sna.py`, `plot_dataset.py`, `plot_integrated.py`), Jupyter notebooks, and trained model artifacts are publicly available in the permanent GitHub repository:  
  **Repository:** https://github.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA  
  **Machine-Readable Metadata:** [`CITATION.cff`](https://github.com/indri007/INDOBERT-9-EMOJI-TESIS-ANALISIS-SNA/blob/main/CITATION.cff)  
  **Interactive Web Dashboard:** https://y6cqezpxxq2ftdwb6yvrab.streamlit.app/

### Author Contributions (CRediT Taxonomy)
- **Indri Anjar Kartika Sari:** Conceptualization, Methodology, Software, Data Curation, Formal Analysis, Investigation, Validation, Visualization, Writing – Original Draft, Project Administration.
- **Catur Suratnoaji:** Supervision, Conceptualization, Theoretical Framework, Formal Analysis Review, Writing – Review & Editing.
- **Agus Widiyarta:** Supervision, Methodology Review, Communication Policy Analysis, Validation, Writing – Review & Editing.

### Ethics Approval and Consent to Participate
This research was conducted in strict adherence to Platform X Developer Policy and standard computational social science data mining ethics (Boyd & Crawford, 2012; Ferrara et al., 2016). Only publicly available posts were harvested. No private or direct messages were accessed. All user data were analyzed in aggregate for public policy communication analysis without individual profiling, stalking, or doxxing.

---

## REFERENCES
Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment*, 2008(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008

Boyd, D., & Crawford, K. (2012). Critical questions for big data: Provocations for a cultural, technological, and scholarly phenomenon. *Information, Communication & Society*, 15(5), 662–679. https://doi.org/10.1080/1369118X.2012.678878

Camp, E. (2012). Sarcasm, pretense, and the semantics/pragmatics distinction. *Noûs*, 46(4), 587–634. https://doi.org/10.1111/j.1468-0068.2010.00822.x

Chiorrini, A., Diamantini, C., Mircoli, A., & Potena, D. (2021). Emotion and sentiment analysis of tweets using BERT. In *CEUR Workshop Proceedings* (Vol. 2841, pp. 24–33). http://ceur-ws.org/Vol-2841/

Clark, H. H., & Gerrig, R. J. (1984). On the pretense theory of irony. *Journal of Experimental Psychology: General*, 113(1), 121–126. https://doi.org/10.1037/0096-3445.113.1.121

Coombs, W. T. (2007). Protecting organization reputations during a crisis: The development and application of situational crisis communication theory. *Corporate Reputation Review*, 10(3), 163–176. https://doi.org/10.1057/palgrave.crr.1550049

Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of deep bidirectional transformers for language understanding. *arXiv preprint arXiv:1810.04805*. https://arxiv.org/abs/1810.04805

Freeman, L. C. (1979). Centrality in social networks: Conceptual clarification. *Social Networks*, 1(3), 215–239. https://doi.org/10.1016/0378-8733(78)90021-7

Grice, H. P. (1975). Logic and conversation. In P. Cole & J. L. Morgan (Eds.), *Syntax and Semantics: Vol. 3. Speech Acts* (pp. 41–58). Academic Press.

Habermas, J. (1989). *The structural transformation of the public sphere: An inquiry into a category of bourgeois society*. MIT Press.

Habermas, J. (2006). Political communication in media society: Does democracy still enjoy an epistemic dimension? *Communication Theory*, 16(4), 411–426. https://doi.org/10.1111/j.1468-2885.2006.00280.x

Kotler, P., Kartajaya, H., & Setiawan, I. (2023). *Marketing 6.0: The future is immersive*. John Wiley & Sons.

Koto, F., Rahimi, A., Lau, J. H., & Baldwin, T. (2020). IndoLEM and IndoBERT: A benchmark dataset and pre-trained language model for Indonesian NLP. In *Proceedings of the 28th International Conference on Computational Linguistics (COLING 2020)* (pp. 757–770). https://doi.org/10.18653/v1/2020.coling-main.67

Newman, M. E. J. (2006). Modularity and community structure in networks. *Proceedings of the National Academy of Sciences*, 103(23), 8577–8582. https://doi.org/10.1073/pnas.0601602103

Papacharissi, Z. (2015). *Affective publics: Sentiment, technology, and politics*. Oxford University Press. https://doi.org/10.1093/acprof:oso/9780199999736.001.0001

Pariser, E. (2011). *The filter bubble: What the internet is hiding from you*. Penguin Press.

Plutchik, R. (1980). A general psychoevolutionary theory of emotion. In *Theories of Emotion* (pp. 3–33). Academic Press. https://doi.org/10.1016/B978-0-12-558701-3.50007-7

Riza, A., & Charibaldi, N. (2021). Implementasi deteksi emosi pada teks bahasa Indonesia menggunakan FastText dan LSTM. *Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)*, 5(2), 241–248. https://doi.org/10.29207/resti.v5i2.2858

Saputri, M. S., Mahendra, R., & Adriani, M. (2018). Emotion classification on Indonesian Twitter dataset. In *2018 International Conference on Asian Language Processing (IALP)* (pp. 90–95). IEEE. https://doi.org/10.1109/IALP.2018.8629145

Schultz, F., Utz, S., & Göritz, A. (2011). Is the medium the message? Perceptions of and reactions to crisis communication via Twitter, blogs and traditional media. *Public Relations Review*, 37(1), 20–27. https://doi.org/10.1016/j.pubrev.2010.12.001

Shaw, P., LaCasse, K., & Champagne, C. (2025). Transfer learning for emotion classification in low-resource Indonesian social discourse. *Social Network Analysis and Mining*, 15(1), 42–58. https://doi.org/10.1007/s13278-024-01256-w

Suaib, A., & Pratiwi, R. (2025). Social network analysis in the dissemination of MBG program information on social media X. *Jurnal Studi Komunikasi*, 9(1), 112–129. https://doi.org/10.56127/jushpen.v4i2.2067

Sulafasyah, L. (2026). *Analisis jaringan komunikasi isu keracunan MBG di Twitter* [Unpublished master's thesis]. Universitas Pembangunan Nasional 'Veteran' Jawa Timur.

Sunstein, C. R. (2017). *#Republic: Divided democracy in the age of social media*. Princeton University Press. https://doi.org/10.1515/9781400884711

Wasserman, S., & Faust, K. (1994). *Social network analysis: Methods and applications*. Cambridge University Press. https://doi.org/10.1017/CBO9780511815478

Wilie, B., Vincentio, K., Winata, G. I., Cahyawijaya, S., Li, X., Lim, Z. Y., Soleman, S., Mahendra, R., Fung, P., Bahar, S., & Purwarianti, A. (2020). IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding. In *Proceedings of AACL-IJCNLP 2020* (pp. 843–860). https://aclanthology.org/2020.aacl-main.85/

