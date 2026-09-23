from pathlib import Path
import shutil

# ============================================================
# CONFIG
# ============================================================

PROJECT_DIR = Path("/Users/jevin/Documents/tesis_mbg/mbg-sna-github")

PDF_SOURCE = Path(
    "/Users/jevin/jurnal/Manuscript_SNAM_Final_Revised.pdf"
)

# ============================================================
# CREATE FOLDERS
# ============================================================

folders = [
    "manuscript",
    "data",
    "src",
    "figures",
    "results",
    "docs",
]

for folder in folders:
    (PROJECT_DIR / folder).mkdir(
        parents=True,
        exist_ok=True
    )

print("Project dibuat:")
print(PROJECT_DIR)

# ============================================================
# COPY PDF
# ============================================================

if PDF_SOURCE.exists():

    destination = (
        PROJECT_DIR
        / "manuscript"
        / "Manuscript_SNAM_Final_Revised.pdf"
    )

    shutil.copy2(
        PDF_SOURCE,
        destination
    )

    print("PDF berhasil dicopy:")
    print(destination)

else:

    print("WARNING: PDF tidak ditemukan:")
    print(PDF_SOURCE)

# ============================================================
# README
# ============================================================

readme = """# MBG Social Network Analysis Research

Research repository for:

Mapping the 'Phygital Gap' in Public Policy Crisis:
A Tri-Layer Computational Communication Study of Indonesia's
Free Nutritious Meal (MBG) Program on Platform X

## Research Components

- Natural Language Processing
- IndoBERT
- 9-class emotion classification
- Pragmatic sarcasm analysis
- Social Network Analysis
- Louvain community detection
- Aspect-Based Sentiment Analysis
- Phygital Gap framework

## Manuscript

The manuscript is located in:

manuscript/Manuscript_SNAM_Final_Revised.pdf

## Repository Structure

mbg-sna-github/

    manuscript/
    data/
    src/
    figures/
    results/
    docs/

## Dataset

Initial corpus: 5,310 posts

Final high-integrity corpus: 5,263 posts

Sarcasm validation corpus: 3,395 posts

Validated sarcastic posts: 315

Sarcasm proportion: 9.28 percent

## Model

IndoBERT:

indobenchmark/indobert-base-p2

## Reproducibility

Analysis scripts should be placed in src/.

Figures should be placed in figures/.

Results should be placed in results/.

Raw or private social-media data should not be uploaded unless
redistribution is legally and ethically permitted.
"""

(PROJECT_DIR / "README.md").write_text(
    readme,
    encoding="utf-8"
)

# ============================================================
# REQUIREMENTS
# ============================================================

requirements = """python-docx
pandas
numpy
matplotlib
networkx
transformers
torch
scikit-learn
"""

(PROJECT_DIR / "requirements.txt").write_text(
    requirements,
    encoding="utf-8"
)

# ============================================================
# GITIGNORE
# ============================================================

gitignore = """__pycache__/
*.pyc
.venv/
venv/
.env
.DS_Store
.ipynb_checkpoints/

data/raw/
data/private/

checkpoints/
*.bin
*.safetensors

*.tmp
*.log
"""

(PROJECT_DIR / ".gitignore").write_text(
    gitignore,
    encoding="utf-8"
)

# ============================================================
# DOCUMENTATION
# ============================================================

research_info = """# Research Information

## Dataset

Initial corpus: 5,310 posts

Final high-integrity corpus: 5,263 posts

Sarcasm validation corpus: 3,395 posts

Validated sarcastic posts: 315

Sarcasm proportion: 9.28 percent

## Emotion Classification

Nine emotion categories:

- Disgust
- Trust
- Neutral
- Anticipation
- Anger
- Sadness
- Joy
- Surprise
- Fear

## Model

indobenchmark/indobert-base-p2

## Social Network Analysis

Nodes: 971

Unique edges: 666

Raw interactions: 692

Density: 0.0011

Reciprocity: 1.21 percent

Giant component: 89 nodes

Giant component share: 9.17 percent

Communities: 332

Modularity: 0.9837

## ABSA

Logistics: 403

Budget: 535

Nutrition: 1,344

Logistics Disgust: 78.91 percent

Budget Disgust: 77.01 percent

Nutrition Disgust: 71.13 percent
"""

(PROJECT_DIR / "docs" / "research_info.md").write_text(
    research_info,
    encoding="utf-8"
)

# ============================================================
# PLACEHOLDER FILES
# ============================================================

(PROJECT_DIR / "src" / "README.md").write_text(
    "# Analysis Scripts\n\nPlace Python analysis scripts here.\n",
    encoding="utf-8"
)

(PROJECT_DIR / "figures" / "README.md").write_text(
    "# Figures\n\nPlace research figures here.\n",
    encoding="utf-8"
)

(PROJECT_DIR / "results" / "README.md").write_text(
    "# Results\n\nPlace research results here.\n",
    encoding="utf-8"
)

# ============================================================
# DONE
# ============================================================

print()
print("=" * 60)
print("PROJECT SIAP")
print("=" * 60)

print()
print("Lokasi:")
print(PROJECT_DIR)

print()
print("Isi project:")

for path in sorted(PROJECT_DIR.rglob("*")):
    if path.is_file():
        print("-", path.relative_to(PROJECT_DIR))

print()
print("NEXT COMMAND:")
print("cd", PROJECT_DIR)
print("git init")
print("git add .")
print('git commit -m "Initial MBG SNA research repository"')
