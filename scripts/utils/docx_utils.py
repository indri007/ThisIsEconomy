"""
scripts/utils/docx_utils.py
===========================
Shared Microsoft Word (.docx) document formatting utilities for table styling,
cell backgrounds, padding margins, border styles, and combined cell properties.
"""

from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set custom internal padding margins on a table cell in dxa units."""
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
    """Set cell shading background color using a hexadecimal color code."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex.lstrip('#'))
    tcPr.append(shd)


def set_cell_border(cell, **kwargs):
    """Set custom cell borders (top, left, bottom, right, insideH, insideV)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = parse_xml(
                f'<{tag} {nsdecls("w")} '
                f'w:val="{edge_data.get("val", "single")}" '
                f'w:sz="{edge_data.get("sz", 4)}" '
                f'w:space="0" '
                f'w:color="{edge_data.get("color", "auto")}"/>'
            )
            tcBorders.append(element)
    tcPr.append(tcBorders)


def set_cell_properties(cell, fill_hex=None, top=100, bottom=100, left=120, right=120):
    """Set cell padding margins and optional background shading in a single call."""
    if fill_hex:
        set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=top, bottom=bottom, left=left, right=right)
