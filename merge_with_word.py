# -*- coding: utf-8 -*-
from pathlib import Path
import win32com.client

MAIN_DOCX = Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\main_from_pdf.docx")
SUPPLEMENT_DOCX = Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\supplement_ch4_only.docx")
OUT_DOCX = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.docx")
OUT_PDF = Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.pdf")

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
doc = word.Documents.Open(str(MAIN_DOCX.resolve()))

rng = doc.Content
rng.Collapse(0)
f = rng.Find
f.ClearFormatting()
f.Text = "ҚОРЫТЫНДЫ"
f.MatchCase = True
f.Forward = False
f.Wrap = 0
if f.Execute():
    doc.Range(rng.Start, rng.Start).InsertFile(str(SUPPLEMENT_DOCX.resolve()))

doc.SaveAs2(str(OUT_DOCX.resolve()), FileFormat=16)
doc.ExportAsFixedFormat(str(OUT_PDF.resolve()), ExportFormat=17)
doc.Close(False)
word.Quit()
