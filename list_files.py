# -*- coding: utf-8 -*-
from pathlib import Path

downloads = Path(r"C:\Users\janap\Downloads")
out = Path(r"C:\Users\janap\Downloads\resume-ai-demo\file_list.txt")
lines = []
for p in sorted(downloads.glob("*.pdf")):
    lines.append(f"PDF|{p}|{p.stat().st_size}")
for p in sorted(downloads.glob("*.docx")):
    lines.append(f"DOCX|{p}|{p.stat().st_size}")
out.write_text("\n".join(lines), encoding="utf-8")
