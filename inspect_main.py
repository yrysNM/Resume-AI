# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document

doc = Document(r"C:\Users\janap\Downloads\resume-ai-demo\merged\main_from_pdf.docx")
hits = []
for i, p in enumerate(doc.paragraphs):
    t = (p.text or "").strip()
    if any(k in t.upper() for k in ["ҚОРЫТ", "КОРЫТ", "ƏДЕБ", "3 ТАРАУ", "4 ТАРАУ"]):
        hits.append(f"{i}: {t[:100]}")
Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\inspect.txt").write_text("\n".join(hits), encoding="utf-8")
