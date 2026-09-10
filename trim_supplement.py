# -*- coding: utf-8 -*-
from pathlib import Path

import win32com.client

SRC = Path(r"C:\Users\janap\Downloads\НИРМ_Қосымша_5бет.docx")
OUT = Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\supplement_ch4_only.docx")

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc = word.Documents.Open(str(SRC.resolve()))
find = word.Selection.Find
find.Text = "4 ТАРАУ ПРАКТИКАЛЫҚ"
find.Execute()
if find.Found:
    start = word.Selection.Start
    doc.Range(0, start).Delete()

doc.SaveAs2(str(OUT.resolve()), FileFormat=16)
doc.Close(False)
word.Quit()
