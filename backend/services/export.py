"""Export resume text to PDF and DOCX."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from docx import Document
from docx.shared import Pt
from fpdf import FPDF

_FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
_DEJAVU = _FONTS_DIR / "DejaVuSans.ttf"
_DEJAVU_BOLD = _FONTS_DIR / "DejaVuSans-Bold.ttf"


def _safe_filename(title: str, ext: str) -> str:
    base = "".join(c if c.isalnum() or c in " -_" else "_" for c in (title or "resume"))
    base = base.strip() or "resume"
    return f"{base[:80]}.{ext}"


def resume_to_pdf(resume_text: str) -> bytes:
    """Render plain resume text as a Unicode PDF (DejaVu)."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.add_font("DejaVu", fname=str(_DEJAVU))
    pdf.add_font("DejaVu", style="B", fname=str(_DEJAVU_BOLD))
    pdf.set_font("DejaVu", size=11)
    # Reset X each line — multi_cell(w=0) leaves the cursor at the right margin.
    for line in resume_text.splitlines() or [""]:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 6, line if line else " ")
    out = BytesIO()
    pdf.output(out)
    return out.getvalue()


def resume_to_docx(resume_text: str) -> bytes:
    """Render plain resume text as a DOCX document."""
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    for line in resume_text.splitlines():
        doc.add_paragraph(line)
    out = BytesIO()
    doc.save(out)
    return out.getvalue()


def export_bytes(resume_text: str, fmt: str) -> tuple[bytes, str, str]:
    """Return (body, media_type, filename) for pdf|docx."""
    fmt = fmt.lower().strip()
    if fmt == "pdf":
        return resume_to_pdf(resume_text), "application/pdf", _safe_filename("resume", "pdf")
    if fmt == "docx":
        return (
            resume_to_docx(resume_text),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            _safe_filename("resume", "docx"),
        )
    raise ValueError(f"Unsupported export format: {fmt}")
