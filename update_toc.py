# -*- coding: utf-8 -*-
"""Patch mazmun paragraph directly in merged DOCX."""

from pathlib import Path

from docx import Document

DOCX = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.docx")

doc = Document(str(DOCX))
p = doc.paragraphs[0]
text = p.text

insert = (
    "\r4 ТАРАУ ПРАКТИКАЛЫҚ ІСКЕ АСЫРУДЫ КӨРСЕТУ ……………………………… 19\r"
    "4.1. Пайдаланушы интерфейсinin қадамдық жұмыс ілмегі ………………… 19\r"
    "4.2. Тәжірибе мен дағdылар модульдері ……………………………………… 20\r"
    "4.3. AI талдау нәtiжелері мен алдын ала қарау ………………………… 21\r"
    "4.4. REST API құжатtamasы (Swagger UI) …………………………………… 22\r"
    "4.5. Жүйе архитектурасы мен деректер ағыны …………………………… 23\r"
    "4.6. Практикалық нәtiжелер мен болашақ даму ………………………… 24\r"
)

markers = [
    "………………………………………...16",
    "………………………………………...16 ",
    "…...16",
]

for m in markers:
    if m in text:
        text = text.replace(m, m + insert, 1)
        break
else:
    if "Қорытынды" in text:
        text = text.replace("Қорытынды", insert + "Қорытынды", 1)

text = text.replace("……........18", "……........25")
text = text.replace("………...20", "………...27")

p.text = text
doc.save(str(DOCX))

# Re-export PDF via Word
import win32com.client

PDF = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.pdf")
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
d = word.Documents.Open(str(DOCX.resolve()))
d.ExportAsFixedFormat(str(PDF.resolve()), ExportFormat=17)
d.Close(False)
word.Quit()

Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\toc_log.txt").write_text("patched", encoding="utf-8")
