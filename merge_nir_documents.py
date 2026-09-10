# -*- coding: utf-8 -*-
"""Merge NIR main PDF with 5-page supplement; update TOC and export."""

from __future__ import annotations

import re
import shutil
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt
from pdf2docx import Converter

BASE_DIR = Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged")
MAIN_PDF = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек.pdf")
SUPPLEMENT_DOCX = Path(r"C:\Users\janap\Downloads\НИРМ_Қосымша_5бет.docx")
OUT_DOCX = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.docx")
OUT_PDF = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.pdf")
LOG = BASE_DIR / "merge_log.txt"

CH4_TOC = (
    "4 ТАРАУ ПРАКТИКАЛЫҚ ІСКЕ АСЫРУДЫ КӨРСЕТУ ……………………………… 19\n"
    "4.1. Пайдаланушы интерфейсінің қадамдық жұмыс ілмегі ………………… 19\n"
    "4.2. Тәжірибе мен дағдылар модульдері ……………………………………… 20\n"
    "4.3. AI талдау нәтижелері мен алдын ала қарау ………………………… 21\n"
    "4.4. REST API құжаттамасы (Swagger UI) …………………………………… 22\n"
    "4.5. Жүйе архитектурасы мен деректер ағыны …………………………… 23\n"
    "4.6. Практикалық нәтижелер мен болашақ даму ………………………… 24"
)


def log(msg: str) -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")


def pdf_to_docx(pdf_path: Path, docx_path: Path) -> None:
    cv = Converter(str(pdf_path))
    cv.convert(str(docx_path), start=0, end=None)
    cv.close()


def paragraph_text(p) -> str:
    return (p.text or "").strip()


def find_conclusion_index(doc: Document) -> int:
    for i, p in enumerate(doc.paragraphs):
        t = paragraph_text(p).upper()
        if "ҚОРЫТЫНДЫ" in t or "КОРЫТЫНДЫ" in t:
            if len(t) < 40:
                return i
    for i, p in enumerate(doc.paragraphs):
        t = paragraph_text(p).upper()
        if "ҚОРЫТЫНДЫ" in t:
            return i
    raise RuntimeError("Қорытынды бөлімі табылмады")


def update_toc(doc: Document) -> None:
    for p in doc.paragraphs:
        t = paragraph_text(p)
        if "3 ТАРАУ" in t and "ТЕСТІЛЕУ" in t:
            # update following conclusion/reference page numbers in mazmun block
            pass
        if t.startswith("Қорытынды") or t.startswith("ҚОРЫТЫНДЫ"):
            p.text = re.sub(r"\d+\s*$", "25", t) if re.search(r"\d+\s*$", t) else t.replace("18", "25")
        if "ƏДЕБИЕТТЕР" in t or "ӘДЕБИЕТТЕР" in t:
            p.text = re.sub(r"\d+\s*$", "27", t) if re.search(r"\d+\s*$", t) else t.replace("20", "27")

    # Find mazmun section and inject chapter 4 lines
    for i, p in enumerate(doc.paragraphs):
        t = paragraph_text(p)
        if "3 ТАРАУ" in t and "ТЕСТІЛЕУ" in t:
            new_p = p.insert_paragraph_before(CH4_TOC)
            for run in new_p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(14)
            # update ch3 line page if present
            p.text = re.sub(r"16\s*$", "16", t)
            break


def insert_supplement_before_conclusion(main: Document, supplement: Document, skip_until_heading: str) -> None:
    idx = find_conclusion_index(main)
    conclusion_el = main.paragraphs[idx]._element
    body = main.element.body

    started = False
    for child in list(supplement.element.body):
        tag = child.tag.split("}")[-1]
        if tag == "p":
            texts = child.findall(".//" + qn("w:t"))
            line = "".join(t.text or "" for t in texts)
            if not started:
                if "4 ТАРАУ" in line:
                    started = True
                else:
                    continue
        elif not started:
            continue

        if started:
            body.insert(body.index(conclusion_el), deepcopy(child))


def set_document_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(14)
    for section in doc.sections:
        section.page_height = section.page_height
        section.page_width = section.page_width
        section.left_margin = section.left_margin
        section.right_margin = section.right_margin


def add_page_numbers(doc: Document) -> None:
    for section in doc.sections:
        footer = section.footer
        if footer.paragraphs:
            p = footer.paragraphs[0]
        else:
            p = footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        run = p.add_run()
        fld_char1 = run._r.makeelement(qn("w:fldChar"), {qn("w:fldCharType"): "begin"})
        instr = run._r.makeelement(qn("w:instrText"), {})
        instr.text = " PAGE "
        fld_char2 = run._r.makeelement(qn("w:fldChar"), {qn("w:fldCharType"): "end"})
        run._r.append(fld_char1)
        run._r.append(instr)
        run._r.append(fld_char2)


def export_pdf(docx_path: Path, pdf_path: Path) -> bool:
    try:
        from docx2pdf import convert

        convert(str(docx_path), str(pdf_path))
        return pdf_path.exists()
    except Exception as exc:
        log(f"PDF export failed: {exc}")
        return False


def main() -> None:
    if LOG.exists():
        LOG.unlink()
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    main_docx = BASE_DIR / "main_from_pdf.docx"
    log("Converting PDF to DOCX...")
    pdf_to_docx(MAIN_PDF, main_docx)

    log("Loading documents...")
    main = Document(str(main_docx))
    supplement = Document(str(SUPPLEMENT_DOCX))

    log("Updating table of contents...")
    update_toc(main)

    log("Inserting chapter 4 before conclusion...")
    insert_supplement_before_conclusion(main, supplement, "4 ТАРАУ")

    log("Applying styles...")
    set_document_styles(main)

    log("Saving merged DOCX...")
    main.save(str(OUT_DOCX))

    log("Exporting PDF...")
    ok = export_pdf(OUT_DOCX, OUT_PDF)
    log(f"PDF export: {'OK' if ok else 'FAILED'}")

    result = BASE_DIR / "result.txt"
    result.write_text(
        f"DOCX={OUT_DOCX}\nPDF={OUT_PDF if ok else 'not created'}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
