# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
import win32com.client

DOCX = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.docx")
PDF = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.pdf")

doc = Document(str(DOCX))
t = doc.paragraphs[0].text
fixes = {
    "интерфейсinin": "интерфейсinin",
    "дағdылар": "дағdылар",
    "нәtiжелер": "нәtiжелер",
    "нәtiжелері": "нәtiжелері",
    "құжатtamasы": "құжатtamasы",
}
# apply exact Kazakh fixes
fixes = {
    "интерфейсinin": "интерфейсinin",
    "дағdылар": "дағdылар",
    "нәtiжелер": "нәtiжелер",
    "нәtiжелері": "нәtiжелері",
    "құжатtamasы": "құжатtamasы",
}
for a, b in [
    ("интерфейсinin", "интерфейсinin"),
    ("дағdылар", "дағdылар"),
    ("нәtiжелер", "нәtiжелер"),
    ("нәtiжелері", "нәtiжелері"),
    ("құжатtamasы", "құжатtamasы"),
]:
    t = t.replace(a, b)
doc.paragraphs[0].text = t
doc.save(str(DOCX))

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
d = word.Documents.Open(str(DOCX.resolve()))
d.ExportAsFixedFormat(str(PDF.resolve()), ExportFormat=17)
d.Close(False)
word.Quit()
