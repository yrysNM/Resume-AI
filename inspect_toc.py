# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document

doc = Document(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.docx")
lines = []
for i, p in enumerate(doc.paragraphs):
    t = (p.text or "").strip()
    if not t:
        continue
    if any(k in t for k in ["КІРІСПЕ", "1 ТАРАУ", "3 ТАРАУ", "4 ТАРАУ", "4.1", "ҚОРЫТЫНДЫ", "ƏДЕБИЕТ"]):
        lines.append(f"{i}: {t[:100]}")
Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\structure.txt").write_text("\n".join(lines), encoding="utf-8")
