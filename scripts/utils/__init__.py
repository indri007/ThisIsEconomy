"""
scripts/utils/__init__.py
=========================
Shared utility package for data processing, metrics, and document styling.
"""
from .docx_utils import (
    set_cell_background,
    set_cell_margins,
    set_cell_border,
    set_cell_properties,
)

__all__ = [
    "set_cell_background",
    "set_cell_margins",
    "set_cell_border",
    "set_cell_properties",
]
