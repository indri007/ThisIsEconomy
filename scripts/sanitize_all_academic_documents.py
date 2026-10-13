#!/usr/bin/env python3
"""
scripts/sanitize_all_academic_documents.py
==========================================
Membersihkan seluruh berkas Word (.docx) dan PDF dari simbol markdown mentah:
  - Mengubah **teks tebal** menjadi Word native bold (tanpa asteris **)
  - Mengubah *teks miring* menjadi Word native italic (tanpa asteris *)
  - Menghilangkan tanda backtick (`@grok` -> @grok)
  - Menghilangkan tanda dollar LaTeX ($N = 100$ -> N = 100)
  - Menghapus artefak heading markdown (#, ##, ###)
  - Mengonversi ulang seluruh berkas ke PDF via LibreOffice headless
"""

import os
import re
import subprocess
from pathlib import Path
import docx
from docx.shared import Pt, Inches

def sanitize_paragraph(p, default_size=Pt(11)):
    full_text = p.text
    if not full_text:
        return
    if "*" not in full_text and "`" not in full_text and "$" not in full_text and not full_text.startswith("#"):
        return

    alignment = p.alignment
    line_spacing = p.paragraph_format.line_spacing
    space_before = p.paragraph_format.space_before
    space_after = p.paragraph_format.space_after
    first_line_indent = p.paragraph_format.first_line_indent
    left_indent = p.paragraph_format.left_indent
    style = p.style

    # Clean markdown headers if at start
    cleaned = full_text
    is_heading_1 = False
    is_heading_2 = False
    if cleaned.startswith("# "):
        cleaned = cleaned[2:].strip()
        is_heading_1 = True
    elif cleaned.startswith("## "):
        cleaned = cleaned[3:].strip()
        is_heading_2 = True
    elif cleaned.startswith("### "):
        cleaned = cleaned[4:].strip()
        is_heading_2 = True

    # Clean LaTeX math $...$ -> ...
    cleaned = re.sub(r"\$([A-Za-z0-9_\\ -]+)\$", r"\1", cleaned)
    # Clean backticks `...` -> ...
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)

    # Tokenize bold-italic (***...***), bold (**...**), italic (*...*)
    pattern = re.compile(r"(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*)")
    parts = pattern.split(cleaned)

    # Clear existing runs
    p.text = ""

    # Restore paragraph formatting
    p.alignment = alignment
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = space_before
    p.paragraph_format.space_after = space_after
    p.paragraph_format.first_line_indent = first_line_indent
    p.paragraph_format.left_indent = left_indent
    p.style = style

    for part in parts:
        if not part:
            continue
        if part.startswith("***") and part.endswith("***") and len(part) >= 6:
            r = p.add_run(part[3:-3])
            r.bold = True
            r.italic = True
        elif part.startswith("**") and part.endswith("**") and len(part) >= 4:
            r = p.add_run(part[2:-2])
            r.bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) >= 2:
            r = p.add_run(part[1:-1])
            r.italic = True
        else:
            clean_part = part.replace("**", "").replace("*", "")
            r = p.add_run(clean_part)

        r.font.name = "Times New Roman"
        if is_heading_1:
            r.font.size = Pt(14)
            r.bold = True
        elif is_heading_2:
            r.font.size = Pt(12)
            r.bold = True
        else:
            r.font.size = default_size

def sanitize_docx_file(file_path):
    print(f"[*] Processing {file_path.name}...")
    doc = docx.Document(file_path)

    # Determine default font size (12pt for manuscripts, 11pt for letters/declarations)
    is_manuscript = "MANUSCRIPT" in file_path.name.upper() or "JURNAL" in file_path.name.upper()
    default_size = Pt(12) if is_manuscript else Pt(11)

    for p in doc.paragraphs:
        sanitize_paragraph(p, default_size)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    sanitize_paragraph(p, default_size=Pt(10))

    doc.save(file_path)

    # Verify asterisks
    doc_reloaded = docx.Document(file_path)
    count = sum(1 for p in doc_reloaded.paragraphs if "*" in p.text)
    table_count = sum(1 for t in doc_reloaded.tables for r in t.rows for c in r.cells for p in c.paragraphs if "*" in p.text)
    total_asterisks = count + table_count
    print(f"    [VERIFIED] {file_path.name}: {total_asterisks} remaining asterisks.")
    return total_asterisks == 0

def convert_to_pdf(docx_path, out_dir):
    try:
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', str(docx_path), '--outdir', str(out_dir)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pdf_path = out_dir / (docx_path.stem + ".pdf")
        if pdf_path.exists():
            print(f"    [PDF OK] Generated {pdf_path.name} ({pdf_path.stat().st_size} bytes)")
    except Exception as e:
        print(f"    [PDF WARN] Failed to convert {docx_path.name} to PDF: {e}")

def main():
    target_dirs = [
        Path("/Users/jevin/Downloads/SUBMISI_JCMC_OXFORD_SCOPUS_Q1"),
        Path("/Users/jevin/Downloads/PAKET_JURNAL_SCOPUS_Q1_MBG_2026 2"),
        Path("/Users/jevin/Documents/tesis_mbg/manuscript")
    ]

    for d in target_dirs:
        if not d.exists():
            continue
        print("=" * 70)
        print(f"MEMBERSIHKAN DIREKTORI: {d}")
        print("=" * 70)
        for docx_file in sorted(d.glob("*.docx")):
            if docx_file.name.startswith("~$"):
                continue
            sanitize_docx_file(docx_file)
            convert_to_pdf(docx_file, d)

if __name__ == "__main__":
    main()
