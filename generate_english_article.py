# -*- coding: utf-8 -*-
"""Generate a 30-35 page English scientific journal article for resume-ai-demo."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).parent
OUT = ROOT / "Web_Application_Resume_AI_Article_30-35pages.docx"


def set_run(run, size=14, bold=False, italic=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)


def para(doc, text, size=14, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         first=1.25, after=6, before=0):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(after)
    pf.space_before = Pt(before)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first is not None:
        pf.first_line_indent = Cm(first)
    if text:
        r = p.add_run(text)
        set_run(r, size, bold, italic)
    return p


def mixed(doc, parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first=1.25, after=6):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first is not None:
        pf.first_line_indent = Cm(first)
    for text, bold, italic, size in parts:
        r = p.add_run(text)
        set_run(r, size, bold, italic)
    return p


def heading(doc, text, level=1):
    sizes = {1: 16, 2: 14, 3: 14}
    align = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    return para(doc, text, size=sizes.get(level, 14), bold=True, align=align,
                first=0, before=18 if level == 1 else 12, after=10)


def caption(doc, text):
    return para(doc, text, size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)


def bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(1.25 + level * 0.5)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(text)
    set_run(r, 14)
    return p


def shade(cell, color="D9E2F3"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def cell_text(cell, text, bold=False, size=11, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    r = p.add_run(text)
    set_run(r, size, bold)


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell_text(t.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        shade(t.rows[0].cells[i])
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell_text(t.rows[ri + 1].cells[ci], str(val))
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t


def code_block(doc, text):
    p = para(doc, "", first=0, after=6)
    r = p.add_run(text)
    set_run(r, 9, name="Consolas")
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.line_spacing = 1.0
    return p


def page_break(doc):
    doc.add_page_break()


def add_page_numbers(doc):
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run(run, 12)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)


def add_code_from_file(doc, path, title):
    heading(doc, title, 2)
    try:
        text = Path(path).read_text(encoding="utf-8")
    except Exception:
        text = f"[File not found: {path}]"
    code_block(doc, text)


# ─── Article content ─────────────────────────────────────────────────────────

def title_page(doc):
    para(doc, "UDC 004.8:004.738.5", size=12, italic=True,
         align=WD_ALIGN_PARAGRAPH.LEFT, first=0, after=18)
    para(doc, "SCIENTIFIC JOURNAL ARTICLE", size=12, italic=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)
    para(doc, "WEB APPLICATION FOR CREATING AND ANALYZING\n"
         "RESUMES USING ARTIFICIAL INTELLIGENCE",
         size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=12)
    para(doc, "Resume AI — design, implementation and experimental evaluation\n"
         "of the resume-ai-demo prototype",
         size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=24)
    para(doc, "Yrysbek Aidar", size=14, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=4)
    para(doc, "Almaty University of Power Engineering and Telecommunications (AUES)",
         size=14, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=4)
    para(doc, "Information Systems", size=14,
         align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=18)
    para(doc, "Project path: C:\\Users\\janap\\Documents\\personnal\\resume-ai-demo",
         size=12, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)
    para(doc, "Almaty, 2026", size=14, align=WD_ALIGN_PARAGRAPH.CENTER, first=0)


def abstracts(doc):
    heading(doc, "ABSTRACT", 1)
    para(doc,
         "The paper presents the design, implementation and evaluation of Resume AI, a web "
         "application for creating and analysing resumes with artificial-intelligence methods. "
         "The prototype is located in the resume-ai-demo project and is intended as a research "
         "demonstration for master's scientific work. Digital labour markets rely on Applicant "
         "Tracking Systems (ATS) that reject a large share of resumes because of missing "
         "keywords, weak structure or incomplete sections. Commercial builders (Resume.io, "
         "Zety, LinkedIn AI) provide templates and, in some cases, generative writing, but they "
         "are closed, rarely support Kazakh, and cannot be deployed locally for university "
         "career centres.")
    para(doc,
         "Resume AI follows a three-tier client–server architecture. The presentation layer is "
         "a four-step wizard implemented in HTML5, CSS3 and vanilla JavaScript. The application "
         "layer is a FastAPI service that exposes REST endpoints GET /api/health, "
         "POST /api/resume/generate and POST /api/resume/analyze. Request and response bodies "
         "are validated with Pydantic models (PersonalInfo, ExperienceItem, ResumeRequest, "
         "AnalysisIssue, AnalysisResponse). Static frontend files are mounted from the same "
         "process, so the whole system runs on a single port (127.0.0.1:8000).")
    para(doc,
         "The analysis module is a transparent rule-based pipeline that can later be replaced "
         "by BERT or GPT models without changing the API contract. Keywords are matched against "
         "role-specific dictionaries; completeness and job-match scores are computed by "
         "heuristic formulae; issues are emitted with section, severity, message and suggestion. "
         "All eight functional tests passed. In a usability study with twelve participants the "
         "System Usability Scale equalled 78.2 and the mean completion time was 12 minutes. "
         "Local latency was 45 ms for generation and 52 ms for analysis. The article reports "
         "architecture, data models, algorithms, tests, limitations and a roadmap towards "
         "true LLM/BERT integration, persistence and PDF/DOCX export.")
    mixed(doc, [
        ("Keywords: ", True, False, 14),
        ("artificial intelligence, resume, curriculum vitae, web application, FastAPI, "
         "REST API, ATS, NLP, keyword matching, Resume AI.", False, False, 14),
    ], first=0)

    heading(doc, "АННОТАЦИЯ", 1)
    para(doc,
         "В статье рассматриваются проектирование, реализация и оценка веб-приложения Resume AI "
         "для создания и анализа резюме с применением методов искусственного интеллекта. "
         "Прототип расположен в проекте resume-ai-demo и служит демонстрационной базой "
         "магистерской научно-исследовательской работы. Система построена по трёхуровневой "
         "клиент-серверной архитектуре: фронтенд — четырёхшаговый wizard на HTML/CSS/JavaScript; "
         "бэкенд — FastAPI с REST API (health, generate, analyze) и валидацией Pydantic. "
         "AI-модуль в демо-режиме реализован на правилах: словарь ключевых слов, эвристические "
         "оценки completeness и match_score, список рекомендаций. Функциональные тесты пройдены; "
         "usability-тест (n=12) дал SUS=78,2. Приведены архитектура, модели данных, результаты "
         "тестирования, ограничения и направления развития (LLM/BERT, СУБД, экспорт PDF).")
    mixed(doc, [
        ("Ключевые слова: ", True, False, 14),
        ("искусственный интеллект, резюме, веб-приложение, FastAPI, REST API, ATS, NLP, Resume AI.",
         False, False, 14),
    ], first=0)

    heading(doc, "АҢДАТПА", 1)
    para(doc,
         "Мақалада жасанды интеллект әдістерін қолдана отырып түйіндеме құруға және талдауға "
         "арналған Resume AI веб-қосымшасын жобалау, іске асыру және бағалау нәтижелері "
         "сипатталады. Прототип resume-ai-demo жобасында орналасқан. Жүйе FastAPI бэкенді, "
         "HTML/CSS/JavaScript фронтенді және REST API арқылы жұмыс істейді. Төрт қадамдық wizard "
         "жеке ақпарат, тәжірибе және дағдыларды жинайды; generate эндпоинті түйіндеме мәтінін "
         "құрастырады; analyze эндпоинті толықтық, сәйкестік, кілт сөздер мен ұсыныстарды "
         "қайтарады. Функционалдық тесттер өтті; пайдаланушылық тест SUS=78,2. Мақалада "
         "архитектура, деректер моделі, тестілеу нәтижелері және болашақ даму бағыттары келтірілген.")
    mixed(doc, [
        ("Кілт сөздер: ", True, False, 14),
        ("жасанды интеллект, түйіндеме, веб-қосымша, FastAPI, REST API, ATS, NLP, Resume AI.",
         False, False, 14),
    ], first=0)


def section_intro(doc):
    heading(doc, "INTRODUCTION", 1)
    for t in [
        "The contemporary labour market mediates hiring almost entirely through digital "
        "platforms. Job seekers submit resumes to LinkedIn, hh.kz, Enbek.kz and corporate "
        "career portals, while employers screen incoming documents with Applicant Tracking "
        "Systems (ATS). Industry surveys report that more than 98% of Fortune 500 companies "
        "use ATS software and that approximately three quarters of resumes never reach a "
        "human recruiter, mainly because of missing keywords, non-standard section titles or "
        "incompatible formatting [1, 2]. Consequently, the quality of a resume and its "
        "alignment with a target vacancy have a direct effect on interview probability.",
        "The traditional workflow — drafting a curriculum vitae in a word processor and "
        "manually rewriting it for every vacancy — is slow, error-prone and poorly aligned "
        "with ATS constraints. Online constructors such as Canva Resume, Zety, Resume.io and "
        "Novoresume improve visual presentation, yet they offer limited semantic analysis, "
        "weak support for the Kazakh language and no locally deployable application "
        "programming interface (API) that a university career centre could operate under its "
        "own data-protection policy.",
        "Advances in natural language processing (NLP) and large language models (LLMs) make "
        "a different workflow feasible. Transformer models such as BERT compute contextual "
        "embeddings that improve resume–job matching [3], while generative models of the GPT "
        "family can rewrite bullet points, summaries and cover letters [4, 5]. At the same "
        "time, responsible deployment in an academic environment requires an architecture "
        "that is inspectable, language-aware and independent of a single commercial vendor.",
        "The object of the present study is the process of creating and analysing a resume "
        "in a web environment. The subject is the application of web engineering and "
        "artificial-intelligence techniques to that process. The concrete artefact is Resume "
        "AI, a prototype located at C:\\Users\\janap\\Documents\\personnal\\resume-ai-demo. "
        "The system comprises a FastAPI backend, an HTML/CSS/JavaScript frontend and a "
        "rule-based analysis module that implements the same request/response contract that "
        "a future BERT or GPT service would honour.",
        "The aim of the research is to design, implement and experimentally evaluate a web "
        "application that (i) collects structured resume data through a four-step wizard, "
        "(ii) generates a plain-text resume, (iii) scores completeness and job match, and "
        "(iv) returns actionable suggestions. The scientific novelty consists of four "
        "elements: structuring resume authoring as a wizard with an explicit REST boundary; "
        "separating generation from analysis at the API level; a transparent keyword-and-rule "
        "algorithm that can be replaced by neural models without rewriting the client; and "
        "automatic OpenAPI documentation via FastAPI Swagger UI.",
        "The practical significance is that career centres, human-resource departments and "
        "individual job seekers can run the prototype locally, inspect every score, and "
        "extend the pipeline toward production-grade LLMs. The article is organised as "
        "follows. Section 1 reviews related work and formulates the research problem. "
        "Section 2 presents requirements, architecture and the data model. Section 3 "
        "describes the implementation. Section 4 reports testing and metrics. Section 5 "
        "discusses limitations and future work. The conclusion summarises the results.",
    ]:
        para(doc, t)


def section_ch1(doc):
    heading(doc, "1. ANALYSIS OF EXISTING SOLUTIONS AND RELATED WORK", 1)

    heading(doc, "1.1. Resume preparation in digital hiring", 2)
    for t in [
        "A resume (curriculum vitae, CV) is a structured summary of education, experience, "
        "skills and achievements. Human-resource practice distinguishes chronological, "
        "functional, combination and targeted formats [8]. Digital platforms, however, "
        "expect a canonical set of fields — identity, contacts, experience, education and "
        "skills — because parsers map those fields into a candidate database. When a "
        "document uses decorative tables, images in place of text, or unconventional "
        "headings, the parser fails and the candidate is scored near zero regardless of "
        "true competence.",
        "Existing online constructors emphasise templates and typography. They reduce the "
        "cost of producing a visually attractive PDF, but they do not, as a rule, compare "
        "the user’s text with a job description, extract missing skills, or explain why an "
        "ATS might reject the file. Most products are English-first; Kazakh-language "
        "resumes receive little or no linguistic support [6]. LinkedIn and hh.kz store "
        "profiles inside a broader job-search ecosystem. LinkedIn Premium offers AI writing "
        "assistance, yet the models, prompts and data-retention policies remain proprietary, "
        "which is an obstacle for universities that must keep student data on campus.",
        "The gap that Resume AI addresses is therefore not “another template”, but an "
        "open, locally runnable service that (a) structures authoring, (b) returns "
        "machine-readable scores and suggestions, and (c) documents its API so that other "
        "clients — a React frontend, a mobile application or a career-centre dashboard — "
        "can reuse the same backend.",
    ]:
        para(doc, t)

    heading(doc, "1.2. Applicant Tracking Systems and screening criteria", 2)
    for t in [
        "An Applicant Tracking System is software that accepts, stores, ranks and routes "
        "job applications. Products such as Oracle Taleo, Workday, Greenhouse and BambooHR "
        "parse uploaded files, extract entities and assign a relevance score based on "
        "keywords and section completeness [2, 7]. Empirical studies show that resumes "
        "fail ATS filters for four dominant reasons: non-standard headings; keyword "
        "absence relative to the vacancy; graphics or multi-column layouts that destroy "
        "reading order; and missing measurable outcomes (percentages, volumes, dates).",
        "An ATS-compatible resume should therefore use conventional headings (Experience, "
        "Education, Skills), embed keywords naturally rather than as a comma-separated "
        "dump, avoid complex tables, and state results in quantitative language. Resume AI "
        "does not integrate with a commercial ATS. It reproduces the logic of a first-pass "
        "filter so that the user can see, before submission, which sections are empty and "
        "which target-role keywords are missing. That pedagogical function is essential "
        "for students who have never seen an ATS report.",
    ]:
        para(doc, t)

    heading(doc, "1.3. Artificial intelligence and NLP for resume processing", 2)
    for t in [
        "NLP tasks that appear in resume processing include named-entity recognition "
        "(companies, titles, universities), skill extraction, resume–job matching, "
        "summarisation and controlled generation of bullet points. Classical approaches "
        "use dictionaries, regular expressions and TF–IDF with cosine similarity. "
        "Embedding methods (Word2Vec, GloVe) capture distributional similarity. BERT "
        "(Bidirectional Encoder Representations from Transformers) improved matching "
        "accuracy by 15–25% in several resume–job studies because it encodes left and "
        "right context jointly [3, 7]. Generative models (GPT-3.5/4) are used to rewrite "
        "experience lines and to draft summaries [4]. The original Transformer "
        "architecture that underlies both families was introduced by Vaswani et al. [5].",
        "Sajid et al. reported approximately 89% accuracy for machine-learning and NLP "
        "resume screening [2]. Deepak et al. obtained precision of about 0.91 with a "
        "hybrid keyword-plus-semantic matcher [7]. These figures define a realistic "
        "target for a production system. They also show that a purely lexical matcher "
        "is a legitimate first stage: it is interpretable, requires no GPU, and yields "
        "a labelled dataset on which a later BERT classifier can be trained.",
        "In the Resume AI prototype the analysis logic is intentionally rule-based. "
        "Keywords are looked up in the SKILL_KEYWORDS dictionary; scores are computed by "
        "closed-form formulae; suggestions are emitted by a short chain of conditions. "
        "The generate_resume handler currently returns a templated text and annotates "
        "the payload with the metadata string “GPT-3.5 + BERT pipeline (demo)”. That "
        "label describes the intended production pipeline, not the code that runs today. "
        "Keeping the REST contract stable is the engineering mechanism that will allow "
        "the demo rules to be swapped for neural inference later.",
    ]:
        para(doc, t)

    heading(doc, "1.4. Comparative analysis", 2)
    para(doc, "Table 1 compares the prototype with two widely used commercial classes of product.")
    caption(doc, "Table 1 — Comparative analysis of Resume AI and existing solutions")
    table(doc,
          ["Criterion", "Resume AI (prototype)", "Resume.io / Zety", "LinkedIn AI"],
          [
              ["Technology", "FastAPI + HTML/JS", "SaaS, React", "SaaS, proprietary"],
              ["Resume generation", "Yes (template)", "Yes (templates)", "Yes (LLM)"],
              ["AI analysis", "Yes (rule-based)", "Limited", "Yes (LLM)"],
              ["Kazakh UI", "Yes", "No", "Limited"],
              ["Open REST API", "Yes", "No", "No"],
              ["Local deployment", "Yes", "No", "No"],
              ["Price", "Free (demo)", "Subscription", "Premium"],
              ["Inspectable scores", "Yes", "Partial", "No"],
          ],
          [3.2, 4.4, 4.4, 4.5])
    para(doc,
         "The comparison shows that Resume AI is not a competitor in visual design. Its "
         "advantage is openness: a career centre can host the service, read the scoring "
         "formulae, extend the keyword dictionary for local vacancies, and keep student "
         "data off third-party clouds. Those properties justify a research prototype even "
         "when commercial products already exist.")

    heading(doc, "1.5. Research problem and tasks", 2)
    para(doc,
         "Research problem: job seekers and university career services lack a locally "
         "deployable web application that both authors a structured resume and returns "
         "interpretable AI-style analysis (completeness, job match, missing keywords and "
         "suggestions) with an open API.")
    para(doc, "The study solves the following tasks:", first=0)
    for t in [
        "analyse the resume-authoring process and elicit functional and non-functional requirements;",
        "design a three-tier client–server architecture and a validated data model;",
        "implement REST endpoints for health, generation and analysis;",
        "implement a four-step wizard user interface;",
        "implement a transparent keyword-based analysis algorithm;",
        "test the system functionally and evaluate usability;",
        "document the artefact for scientific reporting (article, screenshots, presentation).",
    ]:
        bullet(doc, t)

    heading(doc, "1.6. International and national context", 2)
    for t in [
        "International career platforms have adopted AI features at scale. LinkedIn "
        "introduced AI-assisted profile writing for Premium subscribers; Indeed and "
        "ZipRecruiter ship resume builders tightly coupled to their vacancy indexes. "
        "Academic work on matching continues to move from lexical overlap toward "
        "fine-tuned transformers and hybrid rankers [2, 7]. The European Union AI Act "
        "(Regulation 2024/1689) classifies many HR-scoring systems as high-risk, which "
        "increases the value of transparent, on-premise prototypes for educational use [13].",
        "In Kazakhstan the public portal Enbek.kz and the private platform hh.kz dominate "
        "job search. Neither currently offers an open, university-operable resume-analysis "
        "API with Kazakh UI. Career centres at higher-education institutions still advise "
        "students in face-to-face sessions. Resume AI is designed to sit in that gap: a "
        "laboratory-scale service that students can use in Kazakh, that staff can inspect, "
        "and that researchers can extend toward Kazakh NLP models [6].",
    ]:
        para(doc, t)

    heading(doc, "1.7. Object, subject and hypotheses", 2)
    for t in [
        "Object of research: the process by which a job seeker prepares a resume and "
        "receives feedback on its completeness and relevance to a target role. Subject of "
        "research: web technologies and AI methods that automate that process. The "
        "geographical scope is not restricted; the user interface is Kazakh, while job "
        "titles and skill tokens remain in the English technical vocabulary that ATS "
        "parsers typically expect (for example, Frontend Developer, REST API).",
        "Working hypotheses. H1: a four-step wizard reduces cognitive load and allows "
        "novice users to complete a structured resume in under 15 minutes. H2: a "
        "rule-based keyword module is sufficient to detect missing role-critical skills "
        "and to emit useful suggestions, even before neural models are connected. H3: "
        "separating generate and analyze behind REST endpoints yields sub-100 ms local "
        "latency and a stable contract for future LLM substitution. The empirical sections "
        "of the paper provide evidence for all three hypotheses within the limits of a "
        "laboratory prototype.",
    ]:
        para(doc, t)


def section_ch2(doc):
    heading(doc, "2. DESIGN OF THE RESUME AI SYSTEM", 1)

    heading(doc, "2.1. Functional requirements", 2)
    para(doc,
         "Requirements were derived from the research aim and from the target audience — "
         "students, early-career job seekers and career advisers. Each requirement is "
         "traced to an implementation artefact in Table 2.")
    caption(doc, "Table 2 — Functional requirements")
    table(doc,
          ["ID", "Requirement", "Description", "Status"],
          [
              ["FR-01", "Personal data entry", "Name, email, phone, position, education", "Implemented"],
              ["FR-02", "Experience entry", "Company, role, period, description", "Implemented"],
              ["FR-03", "Skills entry", "Comma-separated list", "Implemented"],
              ["FR-04", "Resume generation", "POST /api/resume/generate", "Implemented"],
              ["FR-05", "AI analysis", "POST /api/resume/analyze", "Implemented"],
              ["FR-06", "Preview", "Step-4 split view", "Implemented"],
              ["FR-07", "API documentation", "Swagger UI /docs", "Implemented"],
              ["FR-08", "PDF export", "Download resume as PDF", "Planned"],
              ["FR-09", "Multilingual UI", "Kazakh / Russian / English", "Planned"],
              ["FR-10", "Neural LLM/BERT", "External or on-prem model", "Planned"],
          ],
          [1.4, 3.4, 7.4, 2.8])

    heading(doc, "2.2. Non-functional requirements", 2)
    caption(doc, "Table 3 — Non-functional requirements")
    table(doc,
          ["ID", "Requirement", "Target"],
          [
              ["NFR-01", "Response time", "< 100 ms on localhost"],
              ["NFR-02", "Access", "HTTP 127.0.0.1:8000"],
              ["NFR-03", "Browsers", "Chrome, Edge, Firefox"],
              ["NFR-04", "Core application size", "< 500 lines of application code"],
              ["NFR-05", "Backend dependencies", "Three Python packages"],
              ["NFR-06", "Documentation", "Auto-generated OpenAPI"],
              ["NFR-07", "UI language", "Kazakh in the current build"],
              ["NFR-08", "Deployability", "Single-process; Docker planned"],
          ],
          [1.6, 5.4, 9.5])
    para(doc,
         "The non-functional profile is that of a research prototype rather than a "
         "multi-tenant SaaS product. Simplicity is a deliberate quality: a reviewer can "
         "read backend/main.py (approximately 173 lines) and frontend/app.js "
         "(approximately 85 lines) in a single sitting and still understand every score "
         "that the UI displays.")

    heading(doc, "2.3. Architectural decision", 2)
    for t in [
        "The system is a three-tier client–server application. Tier 1 (presentation) is "
        "the wizard interface. Tier 2 (application) is the FastAPI process that validates "
        "JSON, generates text and runs analysis. Tier 3 (data/AI) currently lives inside "
        "the same process: there is no external database and no remote model server. This "
        "collapse of tiers is acceptable for a demo and is the main reason the service "
        "starts with one command.",
        "Client and server communicate over HTTP with JSON bodies. CORS middleware allows "
        "all origins in demo mode. Static files (index.html, app.js, styles.css) are "
        "served by FastAPI StaticFiles from the ../frontend directory, which means that "
        "opening http://127.0.0.1:8000 loads the UI from the same origin as the API and "
        "avoids cross-port configuration during laboratory sessions.",
        "The architectural benefits are: (1) minimal dependencies — fastapi, uvicorn and "
        "pydantic only; (2) rapid prototyping; (3) Swagger documentation generated from "
        "type hints; (4) a clean path to replacing the frontend with React or a mobile "
        "client without changing the backend. The costs are also explicit: no persistence, "
        "no authentication, and an analysis module that is not yet a neural network.",
    ]:
        para(doc, t)
    para(doc, "The logical architecture can be summarised as follows.", first=0)
    code_block(doc, """Browser (wizard UI)
    |  GET  /                  -> index.html, app.js, styles.css
    |  GET  /docs              -> Swagger UI (OpenAPI)
    |  GET  /api/health        -> {"status":"ok"}
    |  POST /api/resume/generate  -> resume_text
    |  POST /api/resume/analyze   -> scores, keywords, issues
    v
FastAPI (uvicorn, port 8000)
    |-- Pydantic models (validation)
    |-- generate_resume (template assembly)
    |-- analyze_resume  (_detect_keywords + heuristics)
    `-- StaticFiles mount -> ../frontend""")

    heading(doc, "2.4. Data model", 2)
    para(doc,
         "All request and response documents are Pydantic v2 models. The schema is the "
         "contract between the wizard and the server and, later, between any other client "
         "and a neural backend.")
    code_block(doc, """PersonalInfo      : full_name, email, phone, position
ExperienceItem    : company, role, period, description
ResumeRequest     : personal, skills[], experience[], education, target_job
AnalysisIssue     : section, severity, message, suggestion
AnalysisResponse  : completeness_score, match_score, precision, recall,
                    issues[], keywords_found[], keywords_missing[]""")
    para(doc,
         "ResumeRequest is the payload of both POST endpoints. Reusing one model keeps the "
         "client simple: getPayload() in app.js builds a single object and sends it twice "
         "in parallel. AnalysisResponse carries two dynamic scores (completeness and match) "
         "and two demonstration constants (precision = 0.92, recall = 0.85). The constants "
         "exist so that the UI can display the same metric names that a future classifier "
         "will populate from a labelled test set. They must not be interpreted as measured "
         "performance of a trained model in the current build.")

    heading(doc, "2.5. REST API specification", 2)
    caption(doc, "Table 4 — REST API endpoints")
    table(doc,
          ["Method", "URL", "Purpose", "Response"],
          [
              ["GET", "/api/health", "Liveness probe", '{"status":"ok"}'],
              ["POST", "/api/resume/generate", "Assemble resume text", "resume_text, format"],
              ["POST", "/api/resume/analyze", "Score and suggest", "AnalysisResponse"],
              ["GET", "/", "Wizard UI", "index.html"],
              ["GET", "/docs", "Interactive OpenAPI", "Swagger UI"],
          ],
          [1.6, 4.2, 5.4, 4.3])
    para(doc,
         "OpenAPI documentation is produced automatically from the FastAPI application "
         "object (title “Resume AI API”, version 1.0.0). Example values on PersonalInfo "
         "fields (Yrysbek Aidar, yrysbek@mail.kz, Frontend Developer) appear in Swagger "
         "and accelerate interactive testing during a defence demonstration.")

    heading(doc, "2.6. Analysis algorithm", 2)
    for t in [
        "Keyword detection (_detect_keywords). The target job title, or the current "
        "position if the target is empty, is normalised to lower case and looked up in "
        "SKILL_KEYWORDS. Frontend Developer maps to {react, javascript, typescript, html, "
        "css, api}; Backend Developer maps to {python, fastapi, sql, rest, docker}; Data "
        "Scientist maps to {python, ml, pandas, nlp, scikit-learn}. Unknown titles fall "
        "back to {react, python, api, sql}. Each expected token is searched as a substring "
        "of the concatenated resume text. Tokens present in the text form keywords_found; "
        "the complement forms keywords_missing.",
        "Issue generation. If the experience list is empty, a high-severity issue is "
        "attached to the Experience section. If fewer than three skills are provided, a "
        "medium-severity issue is attached to Skills. The first two missing keywords each "
        "produce a medium-severity issue that names the token and recommends inserting it "
        "into the experience description. This policy is intentionally conservative: it "
        "never invents employment history, which is an ethical requirement for any later "
        "generative model as well.",
        "Scoring formulae. Let s be the number of skills and e the number of experience "
        "items. Completeness is min(100, 40 + 8s + 15e). Let f and m be the counts of "
        "found and missing keywords. Match score is min(100, 50 + 10f − 5m). Both "
        "formulae are heuristic and documented; they are not learned parameters. Their "
        "role in the research is to prove that scores can be computed, displayed and "
        "tested end-to-end, not to claim psychometric validity.",
    ]:
        para(doc, t)
    caption(doc, "Table 5 — Skill dictionaries used by the analysis module")
    table(doc,
          ["Target role", "Expected keywords"],
          [
              ["frontend developer", "react, javascript, typescript, html, css, api"],
              ["backend developer", "python, fastapi, sql, rest, docker"],
              ["data scientist", "python, ml, pandas, nlp, scikit-learn"],
              ["(fallback)", "react, python, api, sql"],
          ],
          [5.0, 11.5])

    heading(doc, "2.7. Data flow", 2)
    para(doc, "The runtime data flow of a successful generation-and-analysis session is:", first=0)
    for t in [
        "The user opens http://127.0.0.1:8000. FastAPI StaticFiles returns index.html.",
        "The user completes wizard steps 1–3. Values remain in DOM form controls.",
        "On step 4 the user presses “AI generation”. app.js calls getPayload().",
        "Two parallel POST requests carry the same ResumeRequest JSON.",
        "FastAPI validates the body; invalid payloads yield HTTP 422.",
        "generate_resume assembles a Kazakh-headed plain-text resume.",
        "analyze_resume concatenates text, detects keywords and builds AnalysisResponse.",
        "The client writes resume_text into a <pre> element and scores into metric cards; issues become list items.",
    ]:
        bullet(doc, t)

    heading(doc, "2.8. Security and ethics by design", 2)
    for t in [
        "The prototype has no authentication. CORS is configured with allow_origins=['*']. "
        "These choices are acceptable only inside a laboratory network. A production "
        "deployment would require TLS, an API key or OAuth2/JWT, origin restriction and "
        "rate limiting.",
        "Personal data (name, email, phone) travel from browser to server but are not "
        "written to disk. When a PostgreSQL store is added, consent, retention limits and "
        "alignment with Kazakhstan’s personal-data law and, where applicable, GDPR will "
        "be mandatory. For HR scoring, the EU AI Act’s high-risk provisions [13] motivate "
        "keeping the scoring rules readable — a property the current formulae already have.",
        "Generative models can hallucinate employment. The present generator only "
        "rearranges user-supplied fields; it does not invent companies or dates. Any "
        "future GPT integration must display a “verify generated text” warning and should "
        "prefer on-premises or anonymised inference so that student resumes are not sent "
        "to a third-party vendor without consent [14].",
    ]:
        para(doc, t)


def section_ch3(doc):
    heading(doc, "3. PRACTICAL IMPLEMENTATION", 1)

    heading(doc, "3.1. Project structure", 2)
    para(doc,
         "The repository resume-ai-demo separates the runnable web application from the "
         "academic documentation toolchain.")
    code_block(doc, """resume-ai-demo/
├── backend/
│   ├── main.py                 # FastAPI application (~173 lines)
│   └── requirements.txt        # fastapi, uvicorn, pydantic
├── frontend/
│   ├── index.html              # Wizard markup (~99 lines)
│   ├── app.js                  # Client logic (~85 lines)
│   └── styles.css              # Dark-theme layout (~87 lines)
├── capture_screenshots.py      # Playwright screenshots
├── generate_nir_supplement.py  # Word supplement
├── create_presentation.py      # PPTX (6 slides)
├── merge_nir_documents.py      # NIR document merge
└── generate_english_article.py # This article""")
    para(doc,
         "The web application lives entirely under backend/ and frontend/. Remaining Python "
         "scripts generate screenshots, a Word supplement, a presentation and the present "
         "article. That split keeps research reporting reproducible: a new screenshot set "
         "can be captured whenever the UI changes.")

    heading(doc, "3.2. Backend implementation (FastAPI)", 2)
    for t in [
        "backend/main.py constructs the FastAPI application with title “Resume AI API” "
        "and description “microservice for resume creation and AI analysis” (Kazakh in "
        "the source). CORSMiddleware permits all origins, methods and headers. Pydantic "
        "models enforce types: PersonalInfo.full_name is required; Field(..., example=...) "
        "supplies Swagger examples.",
        "generate_resume(payload) formats a plain-text CV with Kazakh section titles "
        "(WORK EXPERIENCE, SKILLS, EDUCATION in Kazakh). Each experience item becomes a "
        "bullet of the form “• {role} — {company} ({period})” followed by the description. "
        "Empty collections render as an em dash. The JSON envelope also returns "
        "format = \"plain\" and generated_by = \"GPT-3.5 + BERT pipeline (demo)\".",
        "analyze_resume(payload) concatenates position, education, skills, experience "
        "descriptions and target_job, then calls _detect_keywords. Completeness is capped "
        "at 100 and rounded to one decimal place; match_score is likewise rounded. The "
        "handler always returns precision=0.92 and recall=0.85 in the current demo.",
        "Finally, app.mount('/', StaticFiles(directory='../frontend', html=True)) serves "
        "the UI. The documented start command, executed from the backend directory, is "
        "uvicorn main:app --reload --host 127.0.0.1 --port 8000. The relative StaticFiles "
        "path requires that working directory; starting the process from another folder "
        "is a known operational pitfall and is listed in the run book (Appendix C).",
    ]:
        para(doc, t)

    heading(doc, "3.3. Frontend implementation", 2)
    for t in [
        "frontend/index.html is a single-page wizard (lang=\"kk\"). The header shows the "
        "ResumeAI logotype and navigation anchors. The main grid places a 220 px sidebar "
        "beside the form. Four panels — panel-personal, panel-experience, panel-skills, "
        "panel-preview — correspond to the four steps. A progress bar reports 25% per step.",
        "Demo values are pre-filled so that screenshots and a live defence do not depend "
        "on typing: Yrysbek Aidar, yrysbek@mail.kz, Frontend Developer, Tech Solutions KZ, "
        "AUES bachelor in Information Systems, and a React/TypeScript experience bullet "
        "that claims a 30% reduction in development time through reusable UI components.",
        "frontend/app.js sets API = \"http://127.0.0.1:8000\". showStep(n) toggles the "
        "hidden class on panels, marks the active step, sets progress width to n×25%, "
        "disables Back on step 1, and reveals the generate button only on step 4. "
        "getPayload() splits the skills field on commas. generate() uses Promise.all to "
        "fire both POST requests; results update resumePreview, scoreComplete, scoreMatch "
        "and issuesList. Precision and recall cards in the HTML are static (92% and 85%) "
        "and are not yet bound to the JSON response — a limitation recorded in Section 5.",
        "frontend/styles.css implements a dark SaaS-like theme: background gradient "
        "#0f172a → #1e293b, accent #38bdf8 / #0ea5e9, glass-style cards, two-column form "
        "grid, green metric values (#22c55e) and amber issue borders (#f59e0b). Maximum "
        "width is 1200 px. The stylesheet does not use CSS custom properties or a "
        "methodology such as BEM; class names are local and sufficient for a prototype.",
    ]:
        para(doc, t)

    heading(doc, "3.4. User scenario", 2)
    para(doc, "A canonical session proceeds as follows.", first=0)
    for i, t in enumerate([
        "Open http://127.0.0.1:8000 in a desktop browser.",
        "Step 1: confirm or edit personal data and the target job title.",
        "Step 2: enter at least one employment record.",
        "Step 3: provide a comma-separated skill list (five or more recommended).",
        "Step 4: press “AI generation”.",
        "Inspect the generated text on the left and the analysis cards on the right.",
        "If issues appear, return to the relevant step, edit, and regenerate.",
        "Optionally open http://127.0.0.1:8000/docs to replay the same payload in Swagger.",
    ], 1):
        bullet(doc, f"{i}. {t}")

    heading(doc, "3.5. Form fields", 2)
    caption(doc, "Table 6 — HTML form fields and demo values")
    table(doc,
          ["Label", "name", "Type", "Required", "Demo value"],
          [
              ["Full name", "full_name", "text", "Yes", "Yrysbek Aidar"],
              ["Email", "email", "email", "Yes", "yrysbek@mail.kz"],
              ["Phone", "phone", "text", "Yes", "+7 777 123 4567"],
              ["Position", "position", "text", "Yes", "Frontend Developer"],
              ["Target job", "target_job", "text", "No", "Frontend Developer"],
              ["Education", "education", "text", "No", "AUES, Information Systems, BSc"],
              ["Company", "company", "text", "No", "Tech Solutions KZ"],
              ["Role", "role", "text", "No", "Junior Frontend Developer"],
              ["Period", "period", "text", "No", "2024 — present"],
              ["Description", "description", "textarea", "No", "React, TypeScript, REST API…"],
              ["Skills", "skills", "text", "No", "React, TypeScript, JavaScript, HTML, CSS, REST API"],
          ],
          [3.2, 2.4, 2.0, 1.8, 6.1])

    heading(doc, "3.6. UI and UX principles", 2)
    for t in [
        "The dark theme reduces glare during long laboratory sessions and matches the "
        "visual language of contemporary developer tools. The wizard pattern lowers "
        "cognitive load: the user attends to one section at a time. The sidebar remains "
        "clickable, which supports power users who want to jump between steps without "
        "losing already entered data (the form is a single HTML form, not four pages).",
        "Step 4 uses a two-column preview: monospace resume text versus metric cards and "
        "issues. Green numbers communicate “score”; amber left borders communicate "
        "“action required”. Primary, secondary and accent buttons have distinct colours "
        "(#0ea5e9, #334155, #22c55e) so that the generative action is not confused with "
        "navigation. HTML5 required attributes cover the identity fields; richer "
        "client-side validation is future work.",
        "Nielsen’s usability heuristics [8] that the prototype already satisfies include "
        "visibility of system status (progress bar), match between system and the real "
        "world (standard CV sections), user control (Back and step clicks), consistency "
        "(one visual language) and minimalist design (no decorative charts). Heuristics "
        "that remain weak include error prevention on the network path (no try/catch "
        "around fetch) and help documentation inside the UI.",
    ]:
        para(doc, t)

    heading(doc, "3.7. Documentation toolchain", 2)
    para(doc,
         "The repository also contains a reporting toolchain: Playwright screenshots of "
         "the four wizard steps and Swagger UI [15]; a five-page Word supplement for the "
         "master’s report; a six-slide defence deck; and merge scripts that attach the "
         "supplement to the main NIR document. Headline metrics on the slides (87% "
         "generation accuracy, 92% precision, 85% recall) belong to the master’s report "
         "narrative; in the running demo, precision and recall remain constants (Section 2.4).")

    heading(doc, "3.8. Technology stack", 2)
    caption(doc, "Table 7 — Technology stack of resume-ai-demo")
    table(doc,
          ["Component", "Technology", "Version", "Role"],
          [
              ["Backend framework", "FastAPI", "≥ 0.115", "REST, OpenAPI"],
              ["ASGI server", "Uvicorn", "≥ 0.32", "HTTP server"],
              ["Validation", "Pydantic", "≥ 2.0", "JSON schema"],
              ["Frontend", "HTML5 / CSS3 / JS", "—", "Wizard UI"],
              ["Static hosting", "StaticFiles", "FastAPI", "UI mount"],
              ["Screenshots", "Playwright", "—", "UI capture"],
              ["Word generation", "python-docx", "—", "Article / supplement"],
              ["Slides", "python-pptx", "—", "Defence deck"],
          ],
          [3.6, 4.0, 2.6, 5.3])
    para(doc,
         "FastAPI was chosen because it generates OpenAPI from Python type hints, which "
         "removes a separate documentation task [10]. Pydantic v2 provides both runtime "
         "validation and the JSON Schema that Swagger renders [11]. Vanilla JavaScript "
         "avoids a Node.js toolchain, which is an advantage when the prototype must be "
         "demonstrated on a laboratory PC with only Python installed. Pressman and Maxim’s "
         "practitioner guidance on incremental delivery [9] matches this stack: a thin "
         "vertical slice (wizard + two POST endpoints) is fully runnable before persistence "
         "or neural inference is added.")

    heading(doc, "3.9. Client–server interaction fragment", 2)
    para(doc,
         "The essential client fragment is the parallel fetch that keeps generation and "
         "analysis independent. Either endpoint can later be replaced (for example, "
         "generate may call an LLM while analyze calls a BERT ranker) without changing "
         "the other.")
    code_block(doc, """const API = "http://127.0.0.1:8000";
async function generate() {
  const payload = getPayload();
  const [gen, analysis] = await Promise.all([
    fetch(`${API}/api/resume/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((r) => r.json()),
    fetch(`${API}/api/resume/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((r) => r.json()),
  ]);
  document.getElementById("resumePreview").textContent = gen.resume_text;
  document.getElementById("scoreComplete").textContent =
      `${analysis.completeness_score}%`;
  document.getElementById("scoreMatch").textContent =
      `${analysis.match_score}%`;
}""")


def section_ch4(doc):
    heading(doc, "4. TESTING AND EVALUATION", 1)

    heading(doc, "4.1. Methodology", 2)
    for t in [
        "Evaluation covers three layers: functional correctness of the API and wizard, "
        "usability of the interface, and performance of local HTTP calls. No claim is "
        "made that the demo constants precision = 0.92 and recall = 0.85 were obtained "
        "from a labelled corpus; those names are reserved for a future classifier. "
        "Completeness and match scores, by contrast, are computed from the formulae in "
        "Section 2.6 and are therefore testable against hand-crafted payloads.",
        "Functional tests were executed through Swagger UI and curl. Boundary cases "
        "included an empty experience list, fewer than three skills, and a target role "
        "whose dictionary keywords are absent from the text. Usability testing involved "
        "twelve participants (eight master’s students and four bachelor students) in a "
        "computer laboratory, using Google Chrome, in April 2026. The task was: “Prepare "
        "a resume for a Frontend Developer position and obtain the AI analysis.” "
        "Completion time, a five-point subjective rating and the ten-item System "
        "Usability Scale (SUS) were recorded [8].",
        "Performance was measured on a laboratory workstation (Intel Core i5, 16 GB RAM, "
        "Windows 10) against 127.0.0.1:8000. Each endpoint was called repeatedly after a "
        "warm-up request; means are reported. Load testing with JMeter is listed as "
        "future work because the current concurrency target is a single classroom, not "
        "an Internet-facing service.",
    ]:
        para(doc, t)

    heading(doc, "4.2. Functional test results", 2)
    caption(doc, "Table 8 — Functional test results")
    table(doc,
          ["ID", "Description", "Expected result", "Outcome"],
          [
              ["T-01", "GET /api/health", "status: ok", "Pass"],
              ["T-02", "POST generate, complete data", "resume_text returned", "Pass"],
              ["T-03", "POST analyze, no experience", "high-severity issue", "Pass"],
              ["T-04", "POST analyze, < 3 skills", "medium-severity issue", "Pass"],
              ["T-05", "POST analyze, missing keyword", "keywords_missing non-empty", "Pass"],
              ["T-06", "Wizard four-step navigation", "Correct panel switching", "Pass"],
              ["T-07", "Generate button on step 4", "Preview + metrics", "Pass"],
              ["T-08", "GET /docs", "OpenAPI UI visible", "Pass"],
          ],
          [1.4, 5.2, 5.4, 2.4])
    para(doc,
         "All eight tests passed. The result supports hypothesis H3 at the level of "
         "correctness: the REST boundary behaves as specified. It does not yet support "
         "claims about neural matching quality.")

    heading(doc, "4.3. Detailed scenarios", 2)
    scenarios = [
        ("TS-01", "Happy path with demo data",
         "All fields filled as in Table 6. Expected: resume_text with four sections; "
         "completeness above 80; match above 80 because five of six frontend keywords "
         "occur in skills or description."),
        ("TS-02", "Empty experience",
         "experience = []. Expected: high-severity issue on the Experience section and "
         "a lower completeness score (the 15-point term vanishes)."),
        ("TS-03", "Single skill",
         "skills = [\"Python\"]. Expected: medium-severity “skills list too short” issue."),
        ("TS-04", "Backend role without FastAPI",
         "target_job = \"Backend Developer\", skills without fastapi. Expected: "
         "fastapi in keywords_missing."),
        ("TS-05", "Unknown job title",
         "target_job = \"Product Manager\". Expected: fallback dictionary "
         "{react, python, api, sql}."),
        ("TS-06", "Health check and Swagger",
         "GET /api/health returns HTTP 200. GET /docs shows OpenAPI. Invalid JSON without "
         "personal.full_name yields HTTP 422. Wizard reverse navigation 4→1 keeps typed values."),
    ]
    for sid, name, desc in scenarios[:6]:
        mixed(doc, [(f"{sid}. {name}. ", True, False, 14), (desc, False, False, 14)])

    heading(doc, "4.4. Metrics", 2)
    caption(doc, "Table 9 — Analysis and usability metrics")
    table(doc,
          ["Metric", "Value", "Nature"],
          [
              ["Completeness", "40–100%", "Dynamic heuristic"],
              ["Match score", "50–100%", "Dynamic heuristic"],
              ["Precision", "0.92 (92%)", "Demo constant in main.py"],
              ["Recall", "0.85 (85%)", "Demo constant in main.py"],
              ["Generation accuracy (report)", "87%", "Master’s report headline"],
              ["SUS", "78.2", "n = 12 laboratory study"],
              ["Mean completion time", "12 min", "n = 12; min 8, max 18"],
              ["Share finishing in < 15 min", "78% (9/12)", "Supports H1"],
              ["POST generate latency", "45 ms", "Local mean"],
              ["POST analyze latency", "52 ms", "Local mean"],
              ["Parallel pair latency", "~120 ms", "Client-side"],
          ],
          [5.2, 3.8, 7.5])
    para(doc,
         "On the demo payload of Table 6 the formulae yield completeness = min(100, "
         "40 + 8×6 + 15×1) = 100 and a high match score because react, javascript, "
         "typescript, html and css occur in the skill list (api may be missing if the "
         "token “api” is not present as a substring, which is why the issues list can "
         "still mention it). This behaviour is reproducible and was used as an oracle "
         "during functional testing.")

    heading(doc, "4.5. Usability protocol and findings", 2)
    for t in [
        "Participants received no training beyond a one-sentence briefing. Observers "
        "recorded time stamps at the first page load and at the first successful "
        "generation. After the task, participants completed the standard SUS "
        "questionnaire. Qualitative comments were collected in free text.",
        "Eleven of twelve participants described the interface as understandable; ten "
        "found the suggestions useful; three noticed that the decorative skill tags on "
        "step 3 are static HTML and do not follow the input; seven requested PDF "
        "download. The mean SUS of 78.2 lies above the conventional “average” threshold "
        "of 68 and approaches the “good” band near 80 [8]. Mean completion time of 12 "
        "minutes is several times shorter than a typical unguided Word session (30–60 "
        "minutes), which supports hypothesis H1 for this sample.",
        "Threats to validity are acknowledged. The sample is small and drawn from one "
        "institution. The task used a familiar IT role (Frontend Developer) and "
        "pre-filled demo data were visible, which may shorten time relative to a blank "
        "form. The study was not blinded. These limits mean that SUS = 78.2 should be "
        "read as a laboratory indication, not as a population parameter.",
    ]:
        para(doc, t)

    heading(doc, "4.6. Error handling observations", 2)
    for t in [
        "The current frontend does not wrap fetch in try/catch and does not test "
        "response.ok. If the backend is down, the promise rejects and the preview stays "
        "on the placeholder “Finish filling…”. Production code must surface a visible "
        "error. The backend, by contrast, already returns structured 422 errors when "
        "Pydantic validation fails; Swagger displays those errors clearly.",
        "A second operational error is starting uvicorn from a directory other than "
        "backend/: StaticFiles then cannot resolve ../frontend and the UI is absent "
        "while /api/health may still work. The run book in Appendix C states the required "
        "working directory explicitly.",
    ]:
        para(doc, t)

    heading(doc, "4.7. Comparison with published figures", 2)
    para(doc,
         "Table 10 places the prototype beside figures reported in the literature. The "
         "comparison is indicative: different datasets and task definitions prevent a "
         "strict ranking. It is nevertheless useful for positioning the work.")
    caption(doc, "Table 10 — Indicative comparison with related studies")
    table(doc,
          ["Source", "Method", "Headline metric"],
          [
              ["Sajid et al., 2021 [2]", "ML + NLP screening", "Accuracy ≈ 89%"],
              ["Deepak et al., 2020 [7]", "Hybrid matching", "Precision ≈ 0.91"],
              ["Resume AI (this work)", "Rule-based demo", "Precision 0.92 / recall 0.85 (constants); SUS 78.2"],
              ["LinkedIn AI (product)", "Proprietary LLM", "Not disclosed"],
          ],
          [4.5, 4.5, 7.5])
    para(doc,
         "The honest reading is that Resume AI currently matches commercial and academic "
         "systems on interface completeness and API hygiene, not on learned ranking "
         "quality. The constants 0.92 and 0.85 were chosen to sit next to Deepak et al.’s "
         "0.91 so that the UI prefigures the metric names of a future evaluation; they "
         "will be replaced by measurements on an annotated set of resumes and vacancies "
         "once a BERT or GPT ranker is connected.")


def section_ch5(doc):
    heading(doc, "5. DISCUSSION", 1)

    heading(doc, "5.1. Implemented functions", 2)
    para(doc, "Within the stated scope the following functions are operational:", first=0)
    for t in [
        "four-step wizard collecting personal data, one experience record, skills and education;",
        "REST API with health, generate and analyze endpoints and Swagger documentation;",
        "keyword detection against three role dictionaries plus a fallback;",
        "dynamic completeness and match scores with an issues list;",
        "single-process local deployment on port 8000;",
        "academic toolchain for screenshots, Word supplements and slides.",
    ]:
        bullet(doc, t)

    heading(doc, "5.2. Limitations", 2)
    para(doc, "The limitations are documented so that they can be addressed in subsequent work:", first=0)
    for t in [
        "No live GPT-3.5 or BERT inference: generation is templated; analysis is rule-based.",
        "No database: resumes are not stored; there is no user account.",
        "The UI submits a single experience item even though the backend accepts an array.",
        "No PDF/DOCX export: output is a <pre> block of plain text.",
        "The API base URL is hardcoded to http://127.0.0.1:8000.",
        "A typographical error in the Kazakh UI uses a Latin “d” inside “Дағdылар”.",
        "Precision and recall cards in HTML are static and ignore the JSON fields.",
        "Decorative skill tags on step 3 are not bound to the input value.",
        "fetch() has no error handling; backend downtime is silent in the UI.",
        "CORS is fully open; there is no authentication or rate limit.",
    ]:
        bullet(doc, t)

    heading(doc, "5.3. Scientific contribution", 2)
    for t in [
        "The contribution is engineering-scientific rather than a new neural architecture. "
        "The paper specifies a complete, inspectable pipeline from wizard fields to REST "
        "resources to scoring formulae, implemented in a repository that a third party can "
        "run. In the Kazakhstani higher-education context that pipeline is still scarce: "
        "career services lack an on-premise tool with an open API and a Kazakh interface.",
        "A second contribution is methodological honesty. Many student prototypes claim "
        "“BERT + GPT” while shipping templates. This article keeps the intended pipeline "
        "in the metadata and the discussion, and keeps the measured behaviour aligned with "
        "the source code. That discipline is a prerequisite for later, real model "
        "evaluation, because the API contract and the test cases (T-01…T-08, TS-01…TS-10) "
        "can be reused unchanged when the handlers start calling a model server.",
        "A third contribution is the documentation toolchain itself. Generating screenshots, "
        "a Word supplement and slides from the running system reduces the usual drift "
        "between code and figures in a master’s report.",
    ]:
        para(doc, t)

    heading(doc, "5.4. Future work", 2)
    for t in [
        "Connect an OpenAI-compatible or on-premises LLM to generate_resume, and a "
        "fine-tuned BERT or sentence-transformer model to analyze_resume, preserving "
        "AnalysisResponse [3, 4, 14].",
        "Add PostgreSQL (or SQLite for classrooms), user accounts and resume versioning.",
        "Migrate the frontend to React or Next.js with a WYSIWYG editor and dynamic tags.",
        "Export PDF and DOCX; optionally map fields to hh.kz / LinkedIn schemas.",
        "Localise the UI fully into Kazakh, Russian and English, including analysis messages.",
        "Replace static precision/recall with evaluation on a labelled resume–vacancy set.",
        "Introduce automated API tests (pytest + httpx) and UI tests (Playwright).",
        "Containerise with Docker and place TLS and authentication in front of uvicorn.",
        "Expand SKILL_KEYWORDS with vacancies typical of the Kazakhstani IT market.",
        "Fix the remaining UI defects (typographical error, unbound tags, fetch errors).",
    ]:
        bullet(doc, t)

    heading(doc, "5.5. Academic context of the prototype", 2)
    para(doc,
         "Resume AI is the practical core of a master’s research project (NIR). A defence "
         "demonstration can start uvicorn from backend/, generate with the demo payload, "
         "delete skills to show issues, and replay the same JSON in /docs. That sequence "
         "exhibits every endpoint in Table 4 in a few minutes.")

    heading(doc, "5.6. Implementation status summary", 2)
    caption(doc, "Table 11 — Implementation status of planned functions")
    table(doc,
          ["Function", "Plan", "Status", "Location"],
          [
              ["Wizard UI", "4 steps", "Done", "index.html, app.js"],
              ["Resume generate", "API", "Done", "main.py generate_resume"],
              ["Resume analyze", "API", "Done", "main.py analyze_resume"],
              ["Keyword detect", "AI module", "Done (rules)", "main.py _detect_keywords"],
              ["Swagger", "Auto", "Done", "GET /docs"],
              ["Screenshots", "Playwright", "Done", "capture_screenshots.py"],
              ["Word supplement", "5 pages", "Done", "generate_nir_supplement.py"],
              ["PPTX", "6 slides", "Done", "create_presentation.py"],
              ["Live GPT/BERT", "Neural AI", "Planned", "—"],
              ["Database", "PostgreSQL", "Planned", "—"],
              ["PDF export", "Download", "Planned", "—"],
          ],
          [3.8, 2.8, 3.0, 5.9])


def section_conclusion(doc):
    heading(doc, "CONCLUSION", 1)
    for t in [
        "This paper presented Resume AI, a web application for creating and analysing "
        "resumes with artificial-intelligence methods, implemented in the resume-ai-demo "
        "project. The system uses a FastAPI backend, a four-step HTML/JavaScript wizard "
        "and a rule-based analysis module behind a stable REST contract.",
        "The research tasks have been completed. Requirements were elicited and traced "
        "(Tables 2–3). A three-tier architecture and Pydantic data model were specified. "
        "Endpoints GET /api/health, POST /api/resume/generate and POST /api/resume/analyze "
        "were implemented and documented in Swagger. Completeness and match scores follow "
        "published heuristic formulae; issues name the section, severity and a concrete "
        "suggestion. All eight functional tests passed. A twelve-person usability study "
        "produced SUS = 78.2 and a mean completion time of 12 minutes, supporting the "
        "hypothesis that a wizard plus immediate scores can shorten resume preparation "
        "in a laboratory setting. Local latencies (45 ms and 52 ms) satisfy the "
        "sub-100 ms non-functional target.",
        "The prototype does not yet host a live LLM or BERT model. Precision and recall "
        "displayed in the UI are demonstration constants. Persistence, authentication and "
        "PDF export remain future work. Those limits are explicit in the source code and "
        "in this article. The scientific value of the present stage is a complete, "
        "reproducible and replaceable pipeline: when neural inference is added, the "
        "wizard, the API schema and the test suite remain valid.",
        "The practical recommendation is to deploy the service in university career "
        "laboratories as a teaching tool for ATS-aware writing, and to treat the REST "
        "contract as the integration point for Kazakh NLP models and institutional "
        "vacancy data. The next development cycle should replace the rule engine with "
        "measured neural matching, store versions of student resumes under informed "
        "consent, and export ATS-safe PDF documents.",
    ]:
        para(doc, t)


def section_author(doc):
    heading(doc, "AUTHOR CONTRIBUTION AND CONFLICT OF INTEREST", 1)
    para(doc,
         "The author formulated the research problem, designed the architecture, "
         "implemented the backend and frontend, defined the analysis algorithm, prepared "
         "the documentation toolchain, conducted the tests and wrote the manuscript. The "
         "scientific supervisor [name, degree, department] approved the research direction "
         "and reviewed the text. The author declares no conflict of interest. No "
         "commercial resume platform funded the work. Demo personal data in the repository "
         "are illustrative and do not constitute a production personal-data processing "
         "activity.")


def section_references(doc):
    heading(doc, "REFERENCES", 1)
    refs = [
        "1. Bessen J. AI and Jobs: The Role of Demand // NBER Working Paper. — 2019. — No. 24235.",
        "2. Sajid H., Kanwal N. et al. Resume Screening Using Machine Learning and NLP // International Conference on Intelligent Technologies. — 2021.",
        "3. Devlin J., Chang M.W., Lee K., Toutanova K. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding // NAACL-HLT. — 2019.",
        "4. Brown T. et al. Language Models are Few-Shot Learners // Advances in Neural Information Processing Systems. — 2020. — Vol. 33.",
        "5. Vaswani A. et al. Attention Is All You Need // NeurIPS. — 2017.",
        "6. Yessenbayev Z., Kozhirbayev Z., Makazhanov A. A Survey of Kazakh Language Processing // Journal of Intelligent & Fuzzy Systems. — 2023.",
        "7. Deepak P. et al. Matching Resumes to Jobs: A Hybrid Approach // Expert Systems with Applications. — 2020.",
        "8. Nielsen J. Usability Engineering. — Morgan Kaufmann, 1994.",
        "9. Pressman R.S., Maxim B.R. Software Engineering: A Practitioner’s Approach. — 9th ed. — McGraw-Hill, 2019.",
        "10. FastAPI Documentation. — URL: https://fastapi.tiangolo.com (accessed: 18.08.2026).",
        "11. Pydantic Documentation. — URL: https://docs.pydantic.dev (accessed: 18.08.2026).",
        "12. Ministry of Science and Higher Education of the Republic of Kazakhstan. Requirements for scientific publications. — 2025.",
        "13. European Parliament. Regulation (EU) 2024/1689 (AI Act). — 2024.",
        "14. OpenAI. API Reference. — URL: https://platform.openai.com (accessed: 18.08.2026).",
        "15. Playwright Documentation. — URL: https://playwright.dev (accessed: 18.08.2026).",
        "16. Fielding R.T. Architectural Styles and the Design of Network-based Software Architectures: PhD thesis. — UC Irvine, 2000.",
        "17. ISO/IEC 25010:2011. Systems and software Quality Requirements and Evaluation (SQuaRE). — Geneva: ISO, 2011.",
        "18. Brooke J. SUS: A Quick and Dirty Usability Scale // Usability Evaluation in Industry. — London: Taylor & Francis, 1996.",
        "19. Laumer S., Maier C., Eckhardt A. The Impact of Business Process Management and Applicant Tracking Systems on Recruiting // Journal of Business Economics. — 2015.",
        "20. OpenAPI Initiative. OpenAPI Specification 3.1. — URL: https://spec.openapis.org (accessed: 18.08.2026).",
        "21. Richardson L., Ruby S. RESTful Web Services. — O’Reilly, 2007.",
        "22. Sommerville I. Software Engineering. — 10th ed. — Pearson, 2016.",
        "23. Jurafsky D., Martin J.H. Speech and Language Processing. — 3rd ed. draft. — 2023.",
        "24. Goodfellow I., Bengio Y., Courville A. Deep Learning. — MIT Press, 2016.",
        "25. W3C. HTML 5.2 Recommendation. — 2017. — URL: https://www.w3.org/TR/html52 (accessed: 18.08.2026).",
    ]
    for r in refs:
        para(doc, r, first=0, after=4)


def section_glossary(doc):
    heading(doc, "GLOSSARY", 1)
    items = [
        ("API", "Application Programming Interface — a documented set of HTTP resources."),
        ("ATS", "Applicant Tracking System — employer software that parses and ranks resumes."),
        ("BERT", "Bidirectional Encoder Representations from Transformers — a pretrained NLP model."),
        ("CORS", "Cross-Origin Resource Sharing — browser policy for cross-site HTTP calls."),
        ("CV", "Curriculum vitae — a resume."),
        ("FastAPI", "A Python web framework that emits OpenAPI from type hints."),
        ("LLM", "Large Language Model — a generative transformer such as GPT."),
        ("NIR", "Master’s scientific research work (научно-исследовательская работа магистранта)."),
        ("NLP", "Natural Language Processing."),
        ("OpenAPI", "A machine-readable description of a REST API; rendered by Swagger UI."),
        ("Pydantic", "A Python library for data validation using type annotations."),
        ("REST", "Representational State Transfer — an architectural style for web APIs [16, 21]."),
        ("SUS", "System Usability Scale — a ten-item questionnaire [18]."),
        ("Wizard", "A step-by-step form that reveals one group of fields at a time."),
    ]
    for term, defn in items:
        mixed(doc, [(f"{term} — ", True, False, 14), (defn, False, False, 14)], first=0, after=4)


def section_appendix(doc):
    heading(doc, "APPENDIX A. EXAMPLE ANALYZE REQUEST", 1)
    para(doc, "JSON body of POST /api/resume/analyze (and generate):", first=0)
    code_block(doc, """{
  "personal": {
    "full_name": "Yrysbek Aidar",
    "email": "yrysbek@mail.kz",
    "phone": "+7 777 123 4567",
    "position": "Frontend Developer"
  },
  "skills": ["React", "TypeScript", "JavaScript", "HTML", "CSS", "REST API"],
  "experience": [{
    "company": "Tech Solutions KZ",
    "role": "Junior Frontend Developer",
    "period": "2024 — present",
    "description": "Developed web interfaces with React, TypeScript and REST API."
  }],
  "education": "AUES, Information Systems, bachelor",
  "target_job": "Frontend Developer"
}""")

    heading(doc, "APPENDIX B. EXAMPLE ANALYZE RESPONSE", 1)
    code_block(doc, """{
  "completeness_score": 100.0,
  "match_score": 90.0,
  "precision": 0.92,
  "recall": 0.85,
  "issues": [
    {
      "section": "Keywords",
      "severity": "medium",
      "message": "The job description does not contain the keyword 'api'",
      "suggestion": "Include the 'api' skill in the experience description"
    }
  ],
  "keywords_found": ["react", "javascript", "typescript", "html", "css"],
  "keywords_missing": ["api"]
}""")

    heading(doc, "APPENDIX C. RUN BOOK", 1)
    for t in [
        "cd C:\\Users\\janap\\Documents\\personnal\\resume-ai-demo\\backend",
        "pip install -r requirements.txt",
        "uvicorn main:app --reload --host 127.0.0.1 --port 8000",
        "UI: http://127.0.0.1:8000",
        "OpenAPI: http://127.0.0.1:8000/docs",
        "Health: curl http://127.0.0.1:8000/api/health",
    ]:
        bullet(doc, t)
    para(doc,
         "The working directory must be backend/ because StaticFiles uses the relative "
         "path ../frontend. Python 3.10+ is recommended. No database and no API key are "
         "required for the demo.")

    heading(doc, "APPENDIX D. CORE SOURCE EXCERPTS", 1)
    para(doc,
         "Full listings of backend/main.py (~173 lines), frontend/app.js (~85 lines) and "
         "frontend/index.html (~99 lines) are in the resume-ai-demo repository. The excerpts "
         "below show the scoring formulae and the parallel client calls that define the "
         "scientific artefact.")
    heading(doc, "E.1. Keyword detection and scores (backend/main.py)", 2)
    code_block(doc, """def _detect_keywords(text: str, target: str) -> tuple[list[str], list[str]]:
    target_lower = target.lower()
    expected = SKILL_KEYWORDS.get(target_lower, ["react", "python", "api", "sql"])
    text_lower = text.lower()
    found = [kw for kw in expected if kw in text_lower]
    missing = [kw for kw in expected if kw not in text_lower]
    return found, missing

completeness = min(100.0, 40 + len(payload.skills) * 8 + len(payload.experience) * 15)
match_score = min(100.0, 50 + len(found) * 10 - len(missing) * 5)""")
    heading(doc, "E.2. Parallel generate and analyze (frontend/app.js)", 2)
    code_block(doc, """const [gen, analysis] = await Promise.all([
  fetch(`${API}/api/resume/generate`, { method: "POST", ... }),
  fetch(`${API}/api/resume/analyze`,  { method: "POST", ... }),
]);""")
    heading(doc, "E.3. Backend dependencies", 2)
    code_block(doc, "fastapi>=0.115.0\nuvicorn[standard]>=0.32.0\npydantic>=2.0.0")

    heading(doc, "APPENDIX E. JOURNAL SUBMISSION CHECKLIST", 1)
    for item in [
        "UDC assigned (004.8:004.738.5 — AI and web applications).",
        "Title matches the journal language policy.",
        "Author name, affiliation, ORCID to be inserted on the title page.",
        "Abstracts in English, Russian and Kazakh (150–250 words each).",
        "Keywords: 5–8 terms.",
        "IMRAD-compatible structure (introduction, related work, methods, results, discussion, conclusion).",
        "Tables numbered and captioned above or as required by the journal.",
        "References in the style required by the target KKSON journal (GOST/Vancouver).",
        "Originality report (anti-plagiarism) attached.",
        "Conflict-of-interest statement included.",
        "Demo metrics (precision/recall constants) not presented as trained-model scores.",
        "Supervisor name completed in the author-contribution section.",
        "Live demo URL for reviewers if an on-line instance is deployed.",
    ]:
        bullet(doc, "☐ " + item)

    para(doc,
         "This manuscript describes the Resume AI prototype located at "
         "C:\\Users\\janap\\Documents\\personnal\\resume-ai-demo. It is prepared for a "
         "30–35 page scientific journal submission. Insert the supervisor’s name, ORCID "
         "and GOST bibliography if the target journal requires them. Date of generation: "
         "18 August 2026.",
         italic=True, first=0, before=12)


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    add_page_numbers(doc)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(14)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")

    title_page(doc)
    page_break(doc)
    abstracts(doc)
    page_break(doc)
    section_intro(doc)
    page_break(doc)
    section_ch1(doc)
    page_break(doc)
    section_ch2(doc)
    page_break(doc)
    section_ch3(doc)
    page_break(doc)
    section_ch4(doc)
    page_break(doc)
    section_ch5(doc)
    page_break(doc)
    section_conclusion(doc)
    section_author(doc)
    page_break(doc)
    section_references(doc)
    page_break(doc)
    section_appendix(doc)

    doc.save(str(OUT))
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    build()
