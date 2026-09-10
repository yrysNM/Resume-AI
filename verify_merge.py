# -*- coding: utf-8 -*-
from pathlib import Path
paths = [
    Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\supplement_ch4_only.docx"),
    Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.docx"),
    Path(r"C:\Users\janap\Downloads\НИРМ Ырысбек_толық.pdf"),
]
Path(r"C:\Users\janap\Downloads\resume-ai-demo\merged\verify.txt").write_text(
    "\n".join(f"{p.name}|{p.stat().st_size}" for p in paths if p.exists()),
    encoding="utf-8",
)
