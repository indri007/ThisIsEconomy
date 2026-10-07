from docx import Document

src = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT.docx"
out = "/Users/jevin/Documents/tesis_mbg/hmc_submission/HMC_REVIEW_MANUSCRIPT_V2.docx"

doc = Document(src)

abstract = """This study examines public discourse surrounding Indonesia’s Free Nutritious Meal (MBG) program on Platform X through a tri-layer computational communication framework. The study integrates granular emotion classification, pragmatic sarcasm validation, directed social network analysis, and aspect-based sentiment analysis to examine affective, structural, and policy dimensions of the observed discourse. The corpus comprised 5,310 raw posts, with 5,263 retained after preprocessing and quality control. A fine-tuned IndoBERT model classified nine Plutchik-derived emotion categories. Sarcasm was examined in a dedicated corpus of 3,395 posts using lexical contradiction and text-emoji incongruence indicators. The directed interaction network contained 971 nodes and 666 unique edges from 692 raw interactions; Louvain community detection identified 332 communities, with a modularity value of 0.9837. Aspect-based analysis covered logistics and distribution, budget and vendor allocation, and food nutritional quality. Model evaluation produced an accuracy of 57.45%, macro F1 of 0.1444, and weighted F1 of 0.4563, indicating substantial class imbalance across emotion categories. The findings show strong concentration of negative affect across the three policy aspects and a highly fragmented interaction structure in the observed corpus. The study contributes an integrated computational approach for connecting affective expression, network structure, sarcasm, and operational policy themes in digital public-policy discourse."""

keywords = "Makan Bergizi Gratis; Platform X; IndoBERT; Social Network Analysis; Phygital Gap"

# Cari heading ABSTRACT
paras = doc.paragraphs

abstract_idx = None
keywords_idx = None

for i, p in enumerate(paras):
    t = p.text.strip().upper()
    if t == "ABSTRACT":
        abstract_idx = i
    elif t.startswith("KEYWORDS"):
        keywords_idx = i

if abstract_idx is None:
    raise RuntimeError("Heading ABSTRACT tidak ditemukan.")

# Abstract biasanya berada setelah heading ABSTRACT dan sebelum KEYWORDS
if keywords_idx is None:
    raise RuntimeError("KEYWORDS tidak ditemukan.")

# Isi seluruh paragraf antara ABSTRACT dan KEYWORDS dengan abstract baru
for i in range(abstract_idx + 1, keywords_idx):
    paras[i].text = ""

paras[abstract_idx + 1].text = abstract

# Ganti keywords
paras[keywords_idx].text = "Keywords: " + keywords

doc.save(out)

print("BERHASIL")
print("OUTPUT:", out)
print("ABSTRACT WORDS:", len(abstract.split()))
print("KEYWORDS: 5")
