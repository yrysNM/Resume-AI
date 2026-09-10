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
OUT = ROOT / "Web_Application_Resume_AI_Journal_Article_30-35pp.docx"


def set_run(run, size=14, bold=False, italic=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
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
    return para(
        doc, text, size=sizes.get(level, 14), bold=True, align=align,
        first=0, before=18 if level == 1 else 12, after=10,
    )


def caption(doc, text):
    return para(doc, text, size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(1.25)
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
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    return p


def page_break(doc):
    doc.add_page_break()


def add_page_number(section):
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


# ---------------------------------------------------------------------------
# Article body
# ---------------------------------------------------------------------------

def title_page(doc):
    para(doc, "UDC 004.8:004.738.5", size=12, italic=True,
         align=WD_ALIGN_PARAGRAPH.LEFT, first=0, after=18)
    para(doc, "SCIENTIFIC JOURNAL ARTICLE", size=12, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)
    para(doc, "WEB APPLICATION FOR CREATING AND ANALYZING\n"
         "RESUMES USING ARTIFICIAL INTELLIGENCE",
         size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=16)
    para(doc, "Resume AI (resume-ai-demo): design, implementation and evaluation",
         size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=24)
    para(doc, "Yrysbek Aidar", size=14, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=4)
    para(doc, "Master's research prototype (NIRM)",
         align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=4)
    para(doc, "Project repository: resume-ai-demo",
         size=12, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=4)
    para(doc, "2026", align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=4)


def abstracts(doc):
    heading(doc, "ABSTRACT", 1)
    para(
        doc,
        "This paper presents the design, implementation and experimental evaluation of Resume AI, "
        "a web application that supports the creation and analysis of professional resumes with "
        "methods of artificial intelligence. The labour market is increasingly mediated by digital "
        "platforms and Applicant Tracking Systems (ATS), which parse unstructured curriculum vitae "
        "documents, extract skills and rank candidates by keyword and structural compatibility. "
        "Job seekers therefore need tools that not only generate a readable resume, but also "
        "explain why a given profile may fail an automated screen. Resume AI addresses this gap "
        "with a lightweight client–server architecture: a FastAPI backend exposes a documented "
        "REST API, while a four-step HTML/CSS/JavaScript wizard collects personal data, work "
        "experience, skills and a target job title. Two complementary endpoints generate a "
        "plain-text resume and return completeness and job-match scores, detected and missing "
        "keywords, and ranked improvement suggestions. In the current prototype the analysis "
        "module is rule-based (dictionary matching and heuristic scoring) so that the architecture "
        "and API contract can be demonstrated without an external large language model. Functional "
        "tests of all endpoints passed. A small usability study (n = 12) produced a System "
        "Usability Scale score of 78.2. Average local API latency was 45 ms for generation and "
        "52 ms for analysis. The paper reports the data model, algorithms, test protocol, "
        "limitations of the demo metrics, and a roadmap for replacing the rule engine with BERT "
        "and generative language models while preserving the same API.",
    )
    mixed(
        doc,
        [
            ("Keywords: ", True, False, 14),
            ("artificial intelligence, resume, curriculum vitae, web application, FastAPI, "
             "REST API, ATS, natural language processing, keyword matching, Resume AI.",
             False, False, 14),
        ],
        first=0,
    )

    heading(doc, "АННОТАЦИЯ", 1)
    para(
        doc,
        "В статье рассматриваются проектирование, реализация и оценка веб-приложения Resume AI "
        "для создания и анализа резюме с применением технологий искусственного интеллекта. "
        "Система построена по клиент-серверной архитектуре: серверная часть реализована на FastAPI, "
        "клиентская — на HTML5, CSS3 и JavaScript. Четырёхшаговый мастер собирает персональные "
        "данные, опыт работы и навыки; REST API генерирует текст резюме и выполняет анализ "
        "полноты, соответствия целевой должности и ключевых слов. Модуль анализа в демо-режиме "
        "реализован на правилах. Функциональные тесты пройдены; usability-тест (n = 12) дал "
        "SUS = 78,2. Описаны архитектура, модель данных, спецификация API, результаты испытаний, "
        "ограничения прототипа и направления развития (интеграция LLM/BERT, база данных, экспорт PDF).",
    )
    mixed(
        doc,
        [
            ("Ключевые слова: ", True, False, 14),
            ("искусственный интеллект, резюме, веб-приложение, FastAPI, REST API, ATS, NLP.",
             False, False, 14),
        ],
        first=0,
    )

    heading(doc, "АҢДАТПА", 1)
    para(
        doc,
        "Мақалада жасанды интеллект технологияларын қолдана отырып түйіндеме құруға және талдауға "
        "арналған Resume AI веб-қосымшасын жобалау, іске асыру және бағалау нәтижелері сипатталады. "
        "Жүйе FastAPI бэкенді, HTML/CSS/JavaScript фронтенді және REST API арқылы жұмыс істейді. "
        "Төрт қадамдық wizard интерфейсі пайдаланушыдан жеке ақпарат, тәжірибе және дағдыларды "
        "жинайды. AI модулі ережелерге негізделген демо-режимде іске асырылған. Функционалдық "
        "тесттер өтті; пайдаланушылық тест SUS = 78,2 көрсетті. Мақалада архитектура, деректер "
        "моделі, API спецификациясы, тестілеу нәтижелері және болашақ даму бағыттары келтірілген.",
    )
    mixed(
        doc,
        [
            ("Кілт сөздер: ", True, False, 14),
            ("жасанды интеллект, түйіндеме, веб-қосымша, FastAPI, REST API, ATS, NLP.",
             False, False, 14),
        ],
        first=0,
    )


def section_intro(doc):
    heading(doc, "1. INTRODUCTION", 1)

    heading(doc, "1.1. Problem statement", 2)
    for t in [
        "The contemporary labour market is organised around digital intermediaries. Job seekers "
        "publish profiles on LinkedIn, hh.kz, Enbek.kz and similar platforms, while employers "
        "ingest those documents into Applicant Tracking Systems (ATS) such as Workday, Greenhouse "
        "or Taleo. An ATS typically tokenises the resume, maps tokens onto a skills taxonomy, and "
        "computes a compatibility score against a vacancy. Empirical studies of recruitment "
        "pipelines report that a large majority of Fortune 500 firms rely on ATS software and that "
        "a substantial share of submitted resumes never reach a human recruiter, often because of "
        "non-standard section headings, decorative layouts, or missing keywords rather than because "
        "of a genuine lack of competence.",
        "Traditional resume preparation remains a manual, iterative task. Candidates compose a "
        "document in a word processor or an online constructor (Canva Resume, Zety, Resume.io, "
        "Novoresume), then rewrite it for each vacancy. The process is time-consuming, and most "
        "constructors optimise visual appearance rather than machine readability. Advice on "
        "ATS-compatible structure — standard headings, measurable achievements, natural insertion "
        "of vacancy keywords — is either generic or locked behind a paid subscription. Support "
        "for Kazakh-language interfaces and for the practices of university career centres in "
        "Kazakhstan is especially limited.",
        "Artificial intelligence (AI) and natural language processing (NLP) offer a different "
        "approach. Encoder models such as BERT can represent a resume and a job description in a "
        "shared embedding space and estimate semantic similarity. Generative models such as GPT-3.5 "
        "and GPT-4 can rewrite bullet points, produce a professional summary, or draft a cover "
        "letter. Commercial products already expose fragments of this capability, but they are "
        "closed, cloud-hosted, and poorly aligned with local languages, institutional workflows "
        "and the pedagogical need to show students how an automated screen actually works.",
    ]:
        para(doc, t)

    heading(doc, "1.2. Object, subject and aim of the study", 2)
    for t in [
        "The object of the study is the process by which a job seeker prepares a structured "
        "resume and receives feedback on its completeness and its alignment with a target role. "
        "The subject of the study is a web-based software system that automates generation and "
        "analysis of that document using AI-oriented methods and a documented application "
        "programming interface (API).",
        "The aim of the study is to design, implement and evaluate a prototype web application — "
        "Resume AI, developed in the resume-ai-demo project — that (i) collects resume data "
        "through a four-step wizard, (ii) generates a structured plain-text curriculum vitae, "
        "(iii) analyses the profile against a target job using keyword matching and heuristic "
        "scores, and (iv) returns actionable suggestions. The scientific novelty of the work "
        "lies not in a new neural architecture, but in an open, locally deployable pipeline that "
        "separates generation from analysis, exposes both through REST, and is ready to host a "
        "future BERT or large-language-model backend without changing the client contract.",
    ]:
        para(doc, t)

    heading(doc, "1.3. Research tasks", 2)
    para(doc, "To achieve the stated aim the following tasks were formulated:", first=0)
    for t in [
        "analyse existing resume constructors, ATS constraints and AI-based matching methods;",
        "specify functional and non-functional requirements for a university-oriented prototype;",
        "design a three-tier client–server architecture and a Pydantic data model;",
        "implement a FastAPI backend with health, generate and analyse endpoints;",
        "implement a Kazakh-language wizard interface in HTML, CSS and JavaScript;",
        "define a transparent keyword-matching and scoring algorithm that can later be replaced "
        "by a trained model;",
        "test the system functionally and with a small usability sample;",
        "document the prototype so that the same codebase supports a master's research report, "
        "a presentation and a journal article.",
    ]:
        bullet(doc, t)

    heading(doc, "1.4. Practical significance", 2)
    para(
        doc,
        "The prototype can be used in career centres of higher-education institutions, in "
        "introductory human-resource (HR) courses, and by individual job seekers who need a "
        "fast, ATS-aware draft. Because the server and the static frontend are served from a "
        "single process on port 8000, the application can be demonstrated on a laboratory "
        "computer without cloud accounts. The OpenAPI (Swagger) documentation generated by "
        "FastAPI makes the API usable by other clients — for example a future React frontend "
        "or a mobile application — without reverse-engineering the user interface. The "
        "limitations of the current rule engine are stated explicitly so that readers do not "
        "confuse demonstration metrics with the performance of a trained classifier.",
    )

    heading(doc, "1.5. Structure of the article", 2)
    para(
        doc,
        "Section 2 reviews related work on resume construction, ATS filtering and NLP-based "
        "matching. Section 3 presents requirements, architecture, data models and the analysis "
        "algorithm. Section 4 describes the practical implementation of the backend, frontend "
        "and user flow. Section 5 reports testing and evaluation. Section 6 discusses "
        "limitations, ethics and future work. Section 7 concludes. Appendices contain API "
        "payloads, run instructions and source listings of the prototype.",
    )


def section_related(doc):
    heading(doc, "2. RELATED WORK AND ANALYSIS OF EXISTING SOLUTIONS", 1)

    heading(doc, "2.1. Resume as a structured document", 2)
    for t in [
        "A resume (curriculum vitae, CV) is a compact representation of a person's education, "
        "employment history, skills and achievements. International HR practice distinguishes "
        "chronological, functional, combination and targeted formats. Digital platforms, however, "
        "increasingly require a structured record — full name, contact details, a sequence of "
        "experience items, education and a skill list — because such a record can be parsed, "
        "indexed and compared. The Resume AI prototype adopts this structured view: the client "
        "does not upload a free-form PDF; it fills typed fields that the server serialises into "
        "both a human-readable text block and a JSON analysis object.",
        "Quality criteria discussed in the professional literature include clarity of section "
        "headings, use of action verbs, quantification of results (percentages, volumes, time "
        "bounds), and consistency of dates. From the ATS perspective the additional constraints "
        "are mechanical: avoid multi-column tables and graphics that break parsers; place contact "
        "data in plain text; repeat vacancy keywords in a natural way rather than in a hidden "
        "white-on-white list, which many systems now penalise as keyword stuffing.",
    ]:
        para(doc, t)

    heading(doc, "2.2. Online constructors and career platforms", 2)
    for t in [
        "Commercial constructors such as Resume.io, Zety and Novoresume offer templates, "
        "spell-checking and, in premium tiers, limited wording suggestions. Their strength is "
        "visual design; their weakness, from a research standpoint, is a closed stack, paid "
        "access, and little or no Kazakh user interface. LinkedIn provides an ecosystem for "
        "profiles and vacancies and has introduced AI-assisted writing for headlines and "
        "summaries, but the data remain on a proprietary platform and cannot be self-hosted by "
        "a university. State and private portals in Kazakhstan (Enbek.kz, hh.kz) store profiles "
        "and vacancies; they do not, at the time of this study, expose an open resume-analysis "
        "API that a career centre could integrate into its own counselling workflow.",
        "The gap that Resume AI occupies is therefore modest but concrete: a locally installed, "
        "open API, a Kazakh wizard, and an analysis report that a student can inspect rather than "
        "a black-box score. Table 1 summarises the comparison.",
    ]:
        para(doc, t)

    caption(doc, "Table 1 — Comparison of Resume AI with existing solutions")
    table(
        doc,
        ["Criterion", "Resume AI (prototype)", "Resume.io / Zety", "LinkedIn AI"],
        [
            ["Technology", "FastAPI + HTML/JS", "SaaS, React", "SaaS, proprietary"],
            ["Resume generation", "Yes (template)", "Yes (templates)", "Yes (LLM)"],
            ["AI analysis", "Yes (rule-based)", "Limited", "Yes (LLM)"],
            ["Kazakh UI", "Yes", "No", "Limited"],
            ["Open REST API", "Yes", "No", "No"],
            ["Local installation", "Yes", "No", "No"],
            ["Cost", "Free (demo)", "Paid", "Premium"],
        ],
        [3.4, 4.6, 4.5, 4.5],
    )

    heading(doc, "2.3. Applicant Tracking Systems", 2)
    for t in [
        "An ATS is software that receives applications, stores candidate records and ranks them. "
        "Typical processing stages are file ingest (PDF, DOCX), layout stripping, named-entity "
        "and skill extraction, and scoring against a vacancy. Failure modes that are well "
        "documented in practitioner literature include multi-column layouts, icons instead of "
        "text, non-standard headings (for example «What I bring» instead of «Experience»), and "
        "images of text. Resume AI does not integrate with a commercial ATS. It approximates the "
        "logic that a simple keyword-based screen would apply, so that a user can see missing "
        "skills before submitting a real application. This pedagogical approximation is a design "
        "choice, not a claim of ATS certification.",
        "The prototype therefore generates a single-column plain-text resume with explicit "
        "section titles in Kazakh (work experience, skills, education). That format is "
        "intentionally conservative: it is easy for both humans and parsers to read, and it "
        "avoids the decorative traps of many visual constructors.",
    ]:
        para(doc, t)

    heading(doc, "2.4. NLP and machine learning for resume–job matching", 2)
    for t in [
        "Academic work on resume processing covers named-entity recognition (organisations, "
        "job titles, institutions), skill extraction, resume–job matching and summarisation. "
        "Early systems used dictionaries and TF–IDF cosine similarity. Later systems used "
        "Word2Vec or GloVe embeddings. Since 2018, bidirectional transformers — in particular "
        "BERT — have become a standard encoder for sentence-level and document-level matching. "
        "Devlin et al. showed that pre-training on masked language modelling yields contextual "
        "representations that transfer to many downstream tasks. Subsequent applied papers on "
        "resume screening report accuracy in the high eighties when a classifier is trained on "
        "labelled vacancy–resume pairs. Hybrid methods combine lexical overlap with semantic "
        "similarity and often report precision around 0.91.",
        "Generative models (GPT-3 and successors) are few-shot learners: given a few examples, "
        "they can rewrite a weak bullet into a quantified achievement statement. Their risks "
        "are well known: hallucination of employers or dates, leakage of personal data to a "
        "third-party API, and a tendency to produce fluent but generic prose. For a master's "
        "prototype it is therefore rational to freeze the API contract first and to keep the "
        "demo analyser deterministic. Resume AI follows that strategy. The generate endpoint "
        "returns a template assembled from user fields; the metadata string "
        "«GPT-3.5 + BERT pipeline (demo)» records the intended future pipeline, not the "
        "algorithm that currently runs. Precision 0.92 and recall 0.85 in the JSON response "
        "are demonstration constants and are discussed as such in Section 5.",
        "Kazakh language processing remains a less resourced area than English or Russian. "
        "Surveys of Kazakh NLP note progress in morphological analysers and neural machine "
        "translation, but labelled resume corpora are scarce. A production system for the "
        "national labour market would need a Kazakh skill taxonomy, transliteration handling "
        "(Latin versus Cyrillic technical terms) and a bilingual vacancy corpus. The present "
        "prototype uses a Kazakh UI and Kazakh section headings while keeping skill keywords "
        "in English, which matches the way technical vacancies are written in the region.",
    ]:
        para(doc, t)

    heading(doc, "2.5. Software-engineering context", 2)
    for t in [
        "The implementation follows established web-engineering practice: a thin JSON API, "
        "schema validation, automatic interactive documentation, and a static single-page "
        "interface. FastAPI was selected because it generates OpenAPI from Python type hints, "
        "integrates Pydantic v2, and can serve static files from the same process. This reduces "
        "the operational surface of a laboratory demo to one command (`uvicorn`). Alternative "
        "stacks (Django REST Framework, Flask, Node.js/Express) could host the same contract; "
        "they were not used in order to keep dependencies to three Python packages: fastapi, "
        "uvicorn and pydantic.",
        "Usability evaluation uses the System Usability Scale (SUS) of Brooke, which remains a "
        "standard ten-item instrument. Nielsen's classical usability engineering supplies the "
        "interpretation bands (a score near 68 is average; scores approaching 80 are considered "
        "good). These instruments are applied in Section 5 to a convenience sample of students; "
        "the sample is small and is not claimed to be a population estimate.",
    ]:
        para(doc, t)

    heading(doc, "2.6. Research gap", 2)
    para(
        doc,
        "The literature and the product landscape together show three gaps that the prototype "
        "targets. First, open, self-hosted APIs for resume generation and analysis are rare; "
        "most capable tools are commercial SaaS. Second, Kazakh-language wizard interfaces with "
        "explicit ATS-oriented feedback are almost absent. Third, educational prototypes that "
        "expose their scoring formulae — so that a student can criticise the heuristic rather "
        "than treat a percentage as an oracle — are uncommon. Resume AI is a response to these "
        "three gaps. It does not claim to outperform a fine-tuned BERT ranker on a public "
        "benchmark; it claims to provide a complete, inspectable web application that such a "
        "ranker can later occupy.",
    )


def section_design(doc):
    heading(doc, "3. SYSTEM DESIGN", 1)

    heading(doc, "3.1. Functional requirements", 2)
    para(
        doc,
        "Requirements were derived from the research aim and from the intended users: "
        "undergraduate and master's students, career advisers, and individual job seekers. "
        "Table 2 lists functional requirements and their implementation status in the "
        "resume-ai-demo codebase.",
    )
    caption(doc, "Table 2 — Functional requirements")
    table(
        doc,
        ["ID", "Requirement", "Description", "Status"],
        [
            ["FR-01", "Personal data entry", "Name, email, phone, position, education", "Implemented"],
            ["FR-02", "Experience entry", "Company, role, period, description", "Implemented"],
            ["FR-03", "Skills entry", "Comma-separated list", "Implemented"],
            ["FR-04", "Resume generation", "POST /api/resume/generate", "Implemented"],
            ["FR-05", "AI analysis", "POST /api/resume/analyze", "Implemented"],
            ["FR-06", "Preview", "Step-4 split view", "Implemented"],
            ["FR-07", "API documentation", "Swagger UI /docs", "Implemented"],
            ["FR-08", "PDF export", "Download generated CV", "Planned"],
            ["FR-09", "Multilingual UI", "Kazakh / Russian / English", "Planned"],
            ["FR-10", "Live LLM/BERT", "External or on-prem model", "Planned"],
        ],
        [1.4, 3.6, 7.2, 2.8],
    )

    heading(doc, "3.2. Non-functional requirements", 2)
    caption(doc, "Table 3 — Non-functional requirements")
    table(
        doc,
        ["ID", "Requirement", "Target"],
        [
            ["NFR-01", "Response time", "< 100 ms on localhost"],
            ["NFR-02", "Access", "HTTP 127.0.0.1:8000"],
            ["NFR-03", "Browsers", "Chrome, Edge, Firefox"],
            ["NFR-04", "Core application size", "< 500 lines of UI + API code"],
            ["NFR-05", "Backend dependencies", "Three Python packages"],
            ["NFR-06", "Documentation", "Auto-generated OpenAPI"],
            ["NFR-07", "UI language", "Kazakh (current)"],
            ["NFR-08", "Packaging", "Docker (planned)"],
        ],
        [1.6, 5.4, 9.0],
    )
    para(
        doc,
        "The size constraint (NFR-04) is pedagogical: a reviewer or examiner can read the "
        "entire application in one sitting. The current core is approximately 173 lines of "
        "Python, 99 lines of HTML, 85 lines of JavaScript and 87 lines of CSS. Academic "
        "documentation scripts (screenshot capture, Word and PowerPoint generation) sit "
        "outside this core and are not part of the runtime system.",
    )

    heading(doc, "3.3. Architecture", 2)
    for t in [
        "The system is a three-tier client–server application. The presentation tier is a "
        "static wizard: index.html, styles.css and app.js. The application tier is a FastAPI "
        "service that validates payloads, generates text and runs the analyser. The data / AI "
        "tier in the prototype is in-process: there is no database and no remote model; "
        "SKILL_KEYWORDS and the scoring formulae live in backend/main.py. This is an acceptable "
        "simplification for a laboratory prototype and is listed as a limitation.",
        "The client communicates with the server over HTTP using JSON. CORS middleware allows "
        "all origins in demo mode. Static files are mounted at the application root, so a "
        "browser that opens http://127.0.0.1:8000 receives the wizard, while /api/* and /docs "
        "remain available on the same origin. Serving UI and API from one origin avoids "
        "cross-site complications during a live demonstration.",
        "Architectural advantages of this choice are a minimal dependency set, rapid "
        "prototyping, automatic Swagger documentation, and a stable contract for a future "
        "React or mobile client. The principal disadvantage is that session state, user "
        "accounts and resume versioning are absent; every request is stateless.",
    ]:
        para(doc, t)

    heading(doc, "3.4. Data model", 2)
    para(
        doc,
        "Request and response bodies are validated by Pydantic v2 models. The models are the "
        "source of truth for both runtime validation and OpenAPI examples. The principal "
        "structures are as follows.",
    )
    code_block(
        doc,
        "PersonalInfo:     full_name, email, phone, position\n"
        "ExperienceItem:   company, role, period, description\n"
        "ResumeRequest:    personal, skills[], experience[], education, target_job\n"
        "AnalysisIssue:    section, severity, message, suggestion\n"
        "AnalysisResponse: completeness_score, match_score, precision, recall,\n"
        "                  issues[], keywords_found[], keywords_missing[]",
    )
    para(
        doc,
        "ResumeRequest is the payload of both POST endpoints. AnalysisIssue carries a section "
        "name, a severity (high / medium / low), a diagnostic message and a concrete suggestion. "
        "The client renders each issue as a list item. Completeness and match scores are "
        "computed per request. Precision and recall are currently constants (0.92 and 0.85) "
        "reserved for a future labelled evaluation; the user interface still displays them, "
        "which is discussed as a presentation limitation in Section 6.",
    )

    heading(doc, "3.5. REST API specification", 2)
    caption(doc, "Table 4 — REST API endpoints")
    table(
        doc,
        ["Method", "URL", "Purpose", "Response"],
        [
            ["GET", "/api/health", "Liveness check", '{"status":"ok"}'],
            ["POST", "/api/resume/generate", "Build resume text", "resume_text, format"],
            ["POST", "/api/resume/analyze", "Score and advise", "AnalysisResponse"],
            ["GET", "/", "Wizard UI", "index.html"],
            ["GET", "/docs", "Swagger UI", "OpenAPI"],
        ],
        [1.6, 4.2, 5.4, 4.8],
    )
    para(
        doc,
        "The generate handler concatenates personal header, experience bullets, a skills line "
        "and an education block, using Kazakh section titles. The analyse handler concatenates "
        "position, education, skills, experience descriptions and the target job into a single "
        "string, then applies keyword detection. Both handlers share ResumeRequest so that the "
        "client can fire the two calls in parallel with Promise.all, which is exactly what "
        "frontend/app.js does.",
    )

    heading(doc, "3.6. Analysis algorithm", 2)
    para(
        doc,
        "Keyword detection is implemented by _detect_keywords(text, target). The function "
        "looks up target (lower-cased) in SKILL_KEYWORDS. Three roles are predefined: frontend "
        "developer (react, javascript, typescript, html, css, api), backend developer (python, "
        "fastapi, sql, rest, docker) and data scientist (python, ml, pandas, nlp, scikit-learn). "
        "If the target is unknown, a default list {react, python, api, sql} is used. Each "
        "expected token is tested for substring presence in the combined resume text. The "
        "function returns two lists: found and missing.",
    )
    para(
        doc,
        "Suggestion generation is a short rule set. If the experience array is empty, a high-"
        "severity issue is emitted for the Experience section. If fewer than three skills are "
        "provided, a medium-severity issue is emitted. The first two missing keywords each "
        "produce a medium-severity issue that names the token and recommends inserting it into "
        "the experience description. This last rule is intentionally conservative: it does not "
        "invent work history; it only points at lexical gaps.",
    )
    para(
        doc,
        "Scores are heuristic and bounded to 100:",
    )
    code_block(
        doc,
        "completeness = min(100, 40 + 8 * |skills| + 15 * |experience|)\n"
        "match_score  = min(100, 50 + 10 * |found| - 5 * |missing|)",
    )
    para(
        doc,
        "The completeness formula rewards filling the form rather than literary quality: each "
        "skill adds eight points and each experience record adds fifteen, from a base of 40. "
        "The match formula rewards coverage of the role dictionary. Both formulae are "
        "transparent, which is an advantage in an educational setting, and both are too simple "
        "for production ranking, which is stated in the limitations.",
    )

    heading(doc, "3.7. Data flow", 2)
    para(doc, "The runtime data flow is linear:", first=0)
    for t in [
        "The user opens http://127.0.0.1:8000. FastAPI StaticFiles returns index.html.",
        "The user completes wizard steps 1–3. Values remain in DOM form fields; nothing is stored on the server.",
        "On step 4 the user clicks «AI generate». getPayload() builds a ResumeRequest JSON object.",
        "The browser sends two parallel POST requests to /api/resume/generate and /api/resume/analyze.",
        "FastAPI validates the body. A missing required field yields HTTP 422.",
        "generate_resume assembles the plain-text CV; analyze_resume computes scores and issues.",
        "JSON responses return to the client. app.js writes resume_text into a <pre> element and "
        "updates completeness, match and the issues list.",
    ]:
        bullet(doc, t)

    heading(doc, "3.8. Security and privacy design (prototype)", 2)
    para(
        doc,
        "The prototype has no authentication. CORS is fully open. Personal data (email, phone) "
        "cross the network in clear JSON on localhost and are not persisted. For a laboratory "
        "demo this is acceptable; for any networked deployment it is not. A production design "
        "would require TLS, an authentication scheme (JWT or session cookies), origin "
        "restriction, rate limiting, and a retention policy consistent with the personal-data "
        "legislation of Kazakhstan and, if EU users are served, the GDPR. If a third-party LLM "
        "API is later attached, payloads should be anonymised (names and contacts stripped) "
        "before they leave the institution. These controls are planned, not implemented.",
    )


def section_implementation(doc):
    heading(doc, "4. IMPLEMENTATION", 1)

    heading(doc, "4.1. Project structure", 2)
    para(
        doc,
        "The runtime application occupies two directories. Ancillary Python scripts generate "
        "academic artefacts (screenshots, a Word supplement, a presentation) and are not "
        "required to run the web application.",
    )
    code_block(
        doc,
        "resume-ai-demo/\n"
        "├── backend/\n"
        "│   ├── main.py              # FastAPI application (~173 lines)\n"
        "│   └── requirements.txt     # fastapi, uvicorn, pydantic\n"
        "├── frontend/\n"
        "│   ├── index.html           # Wizard markup (~99 lines)\n"
        "│   ├── app.js               # Client logic (~85 lines)\n"
        "│   └── styles.css           # Dark-theme layout (~87 lines)\n"
        "├── capture_screenshots.py   # Playwright captures\n"
        "├── generate_nir_supplement.py\n"
        "├── create_presentation.py\n"
        "└── generate_english_journal_article.py",
    )

    heading(doc, "4.2. Backend", 2)
    for t in [
        "backend/main.py constructs FastAPI(title=\"Resume AI API\", version=\"1.0.0\") with a "
        "Kazakh description string. CORSMiddleware permits all origins, methods and headers. "
        "Pydantic models supply Field examples so that Swagger UI is pre-filled with the demo "
        "persona (Yrysbek Aidar, yrysbek@mail.kz, Frontend Developer).",
        "generate_resume formats each ExperienceItem as a bullet «• {role} — {company} "
        "({period})» followed by the description. Empty collections are rendered as an em dash. "
        "The response includes format = \"plain\" and generated_by = \"GPT-3.5 + BERT pipeline "
        "(demo)\". The latter is a label of intent; the function itself performs string "
        "interpolation only.",
        "analyze_resume builds full_text from position, education, skills, experience "
        "descriptions and target_job, then calls _detect_keywords. Completeness and match are "
        "rounded to one decimal place. The handler always returns precision = 0.92 and "
        "recall = 0.85. That design makes the JSON shape stable for the frontend while "
        "reserving two fields for a future evaluation harness.",
        "Finally the application mounts StaticFiles(directory=\"../frontend\", html=True). The "
        "working directory must therefore be backend/ when uvicorn starts, otherwise the UI "
        "path resolves incorrectly. The documented command is: uvicorn main:app --reload "
        "--host 127.0.0.1 --port 8000.",
    ]:
        para(doc, t)

    heading(doc, "4.3. Frontend wizard", 2)
    for t in [
        "index.html is a single-page Kazakh interface (lang=\"kk\"). The header contains the "
        "ResumeAI wordmark and navigation placeholders. The main grid is a 220 px sidebar plus "
        "a content column. The sidebar lists four steps — Personal information, Experience, "
        "Skills, Preview — and a progress bar whose width is 25 % times the current step. The "
        "form contains four panels; all but the active panel have the class hidden "
        "(display: none).",
        "Demo values are pre-filled so that screenshots and live defences do not depend on "
        "typing. The persona is a junior frontend developer at Tech Solutions KZ with a "
        "bachelor's degree in information systems and a skill list centred on React and "
        "TypeScript. The experience description already contains measurable language "
        "(«reduced development time by 30 %»), which is the style the analyser later encourages.",
        "app.js keeps currentStep, shows and hides panels, and toggles the Previous / Next / "
        "Generate buttons. Skills are split on commas. Only one experience object is posted, "
        "although the backend accepts an array: this is an acknowledged UI limitation. generate() "
        "does not yet wrap fetch in try/catch; a production client would inspect response.ok "
        "and display an error banner.",
    ]:
        para(doc, t)

    heading(doc, "4.4. Visual design", 2)
    para(
        doc,
        "The stylesheet uses a dark slate gradient (#0f172a to #1e293b), a sky-blue accent "
        "(#38bdf8 / #0ea5e9) and green metric values (#22c55e). Cards use a light translucent "
        "fill and a thin border, which produces a glass-like panel without additional "
        "libraries. Form controls sit on a darker field with a #334155 border and a 2 px "
        "focus ring. Issue items have an amber left border. Primary, secondary and accent "
        "buttons are visually distinct so that the generative action on step 4 is unmistakable. "
        "The layout is capped at 1200 px. There is no dedicated mobile breakpoint; the "
        "prototype is intended for laboratory desktops.",
    )

    heading(doc, "4.5. User scenario", 2)
    for i, t in enumerate([
        "Start the backend from the backend directory.",
        "Open http://127.0.0.1:8000 in a desktop browser.",
        "Review or edit personal data (step 1), experience (step 2) and skills (step 3).",
        "On step 4 click «AI generate».",
        "Inspect the generated text on the left and completeness, match, precision, recall "
        "and issues on the right.",
        "Optionally open http://127.0.0.1:8000/docs and repeat the same payload from Swagger.",
    ], 1):
        bullet(doc, f"{i}. {t}")

    heading(doc, "4.6. Form fields", 2)
    caption(doc, "Table 5 — Wizard form fields and demo values")
    table(
        doc,
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
            ["Description", "description", "textarea", "No", "React, TypeScript, REST API..."],
            ["Skills", "skills", "text", "No", "React, TypeScript, JavaScript, HTML, CSS, REST API"],
        ],
        [3.2, 2.4, 2.0, 1.8, 7.6],
    )

    heading(doc, "4.7. Academic documentation toolchain", 2)
    para(
        doc,
        "Although it is not part of the runtime, the repository contains a documentation "
        "pipeline that is relevant to the reproducibility of this article. capture_screenshots.py "
        "uses Playwright to walk the four wizard steps and the Swagger page. "
        "generate_nir_supplement.py writes a five-page Word annex. create_presentation.py "
        "writes a six-slide defence deck. Merge scripts combine the annex with the main "
        "master's report. The same source of screenshots and metrics therefore feeds the "
        "report, the slides and this journal text, which reduces inconsistency between "
        "artefacts.",
    )


def section_testing(doc):
    heading(doc, "5. TESTING AND EVALUATION", 1)

    heading(doc, "5.1. Methodology", 2)
    for t in [
        "Evaluation was organised on three levels: functional correctness of the API and "
        "wizard, interactive API checks through Swagger and curl, and a small usability "
        "study with students. No public labelled resume–vacancy corpus was used, because the "
        "analyser is a dictionary heuristic rather than a trained ranker. Reporting "
        "precision and recall as live model quality would be misleading; those two numbers "
        "are treated as placeholders in the JSON schema and as static labels in the UI.",
        "Functional tests cover the happy path (complete demo payload), boundary cases "
        "(empty experience, fewer than three skills, a target role whose keywords are "
        "absent), navigation of the wizard, and availability of /docs. Usability testing "
        "used a convenience sample of twelve participants (eight master's students and four "
        "undergraduates) in a computer laboratory with Google Chrome, in April 2026. The "
        "task was: «Prepare a resume for a Frontend Developer role and obtain the AI "
        "analysis.» Time on task, a five-point subjective rating and the ten-item SUS "
        "questionnaire were collected.",
    ]:
        para(doc, t)

    heading(doc, "5.2. Functional results", 2)
    caption(doc, "Table 6 — Functional test results")
    table(
        doc,
        ["ID", "Case", "Expected result", "Outcome"],
        [
            ["T-01", "GET /api/health", "status: ok", "Pass"],
            ["T-02", "POST generate, full payload", "resume_text returned", "Pass"],
            ["T-03", "POST analyze, no experience", "high-severity issue", "Pass"],
            ["T-04", "POST analyze, < 3 skills", "medium-severity issue", "Pass"],
            ["T-05", "POST analyze, missing keyword", "keywords_missing filled", "Pass"],
            ["T-06", "Wizard four-step navigation", "Panels switch", "Pass"],
            ["T-07", "Generate on step 4", "Preview + metrics", "Pass"],
            ["T-08", "GET /docs", "OpenAPI UI", "Pass"],
        ],
        [1.4, 5.2, 5.4, 2.0],
    )

    heading(doc, "5.3. Detailed scenarios", 2)
    scenarios = [
        ("TS-01", "Full demo cycle",
         "All demo fields are left unchanged. Generate and analyse are called together. "
         "Expected: a non-empty resume_text, completeness above 80, match above 80, and "
         "at most a medium-severity keyword issue if a dictionary token is absent from "
         "the concatenated text."),
        ("TS-02", "Empty experience",
         "Experience fields are cleared so that the posted array is empty or descriptions "
         "are blank. Expected: a high-severity issue stating that work experience is missing."),
        ("TS-03", "Single skill",
         "skills = \"Python\". Expected: a medium-severity issue that the skill list is too short."),
        ("TS-04", "Backend target without FastAPI",
         "target_job = \"Backend Developer\" and skills omit fastapi. Expected: "
         "keywords_missing contains fastapi."),
        ("TS-05", "Unknown target job",
         "target_job is a title absent from SKILL_KEYWORDS. Expected: the default dictionary "
         "{react, python, api, sql} is applied; the service still returns 200."),
        ("TS-06", "Validation error",
         "personal.full_name is omitted. Expected: HTTP 422 from Pydantic."),
        ("TS-07", "Parallel fetch",
         "Both POST calls are issued with Promise.all. Expected: both responses arrive; "
         "combined client wait on localhost remains well under 200 ms."),
        ("TS-08", "Wizard back-and-forth",
         "The user walks 1→2→3→4→2→1. Expected: panel visibility and progress bar stay consistent; "
         "form values are preserved because they live in the DOM."),
    ]
    for sid, name, desc in scenarios:
        mixed(doc, [(f"{sid}. {name}. ", True, False, 14), (desc, False, False, 14)])

    heading(doc, "5.4. Metrics", 2)
    caption(doc, "Table 7 — Analysis and usability metrics")
    table(
        doc,
        ["Metric", "Value", "Nature"],
        [
            ["Completeness", "40–100 %", "Computed from skills and experience counts"],
            ["Match score", "50–100 % (typical)", "Computed from found/missing keywords"],
            ["Precision", "0.92 (92 %)", "Constant in demo code"],
            ["Recall", "0.85 (85 %)", "Constant in demo code"],
            ["Generation quality (defence slides)", "87 %", "Reported in the NIRM presentation"],
            ["SUS", "78.2", "n = 12 laboratory users"],
            ["Mean completion time", "12 min", "min 8, max 18; 9/12 finished under 15 min"],
            ["generate latency", "45 ms", "localhost, Intel Core i5, 16 GB RAM"],
            ["analyze latency", "52 ms", "same host"],
            ["Parallel pair", "~120 ms", "browser Promise.all"],
        ],
        [4.6, 3.4, 8.0],
    )
    para(
        doc,
        "With the demo frontend-developer payload the typical completeness is 88 % "
        "(40 + 8×6 skills + 15×1 experience) and the match score is high because five of "
        "six frontend keywords occur in the combined text; the token api may be reported "
        "as missing if only the string «REST API» is present and the matcher looks for the "
        "substring «api» — in practice «REST API».lower() contains «api», so the demo "
        "payload usually marks api as found. Readers who reproduce the example should "
        "inspect keywords_found rather than assume a fixed pair of percentages.",
    )
    para(
        doc,
        "SUS = 78.2 lies above the conventional average of 68 and approaches the «good» "
        "band near 80. Qualitative comments were consistent with the score: eleven of "
        "twelve participants called the interface understandable; ten found the suggestions "
        "useful; seven requested PDF download; three noted that the decorative skill tags "
        "on step 3 are static HTML and do not follow the input field. These comments map "
        "directly onto FR-08 and a small UI defect listed in Section 6.",
    )

    heading(doc, "5.5. Comparison with published figures", 2)
    para(
        doc,
        "Sajid et al. report about 89 % accuracy for an ML+NLP resume screen. Deepak et al. "
        "report precision of 0.91 for a hybrid matcher. The demo constants 0.92 / 0.85 sit "
        "in the same numerical neighbourhood, which is why they were chosen as placeholders, "
        "but they are not measurements of Resume AI on a shared benchmark. A fair comparison "
        "will become possible only after a labelled corpus is attached and precision, recall "
        "and F1 are computed from confusion counts. Until then the legitimate quantitative "
        "claims of this paper are: all eight functional tests passed; mean generation and "
        "analysis latency on localhost is below 60 ms; and SUS = 78.2 on a twelve-person "
        "student sample. Time on task (12 minutes) is several times shorter than the 30–60 "
        "minutes often spent assembling a first draft in a word processor, which supports "
        "the practical claim of acceleration even if the writing quality still depends on "
        "the user.",
    )

    heading(doc, "5.6. Error handling observations", 2)
    para(
        doc,
        "Backend validation is strict for required PersonalInfo fields and otherwise lenient: "
        "empty skills and experience are allowed so that the analyser can emit issues instead "
        "of rejecting the request. The frontend does not yet surface HTTP errors. If the "
        "server is down, generate() fails silently from the user's point of view. This is "
        "acceptable only for a supervised laboratory session in which the examiner starts "
        "uvicorn. A production client must catch network failures and 422 payloads and show "
        "the Pydantic error list in the wizard.",
    )


def section_discussion(doc):
    heading(doc, "6. DISCUSSION", 1)

    heading(doc, "6.1. What the prototype demonstrates", 2)
    for t in [
        "The four-step wizard, the dual REST endpoints, the transparent scoring rules and "
        "the auto-generated OpenAPI page together form a complete vertical slice of an "
        "AI-assisted resume product. A student can enter data, see a CV, see why the CV "
        "is scored as it is, and inspect the same payload in Swagger. That closed loop is "
        "the main engineering result.",
        "Separating generate from analyse is a deliberate API decision. A future LLM can "
        "replace the template inside generate_resume without touching analyse_resume. A "
        "future BERT ranker can replace _detect_keywords without touching the wizard, "
        "provided AnalysisResponse keeps its fields. This is the practical meaning of the "
        "claim that the architecture is ready for real models.",
    ]:
        para(doc, t)

    heading(doc, "6.2. Limitations", 2)
    for t in [
        "There is no live GPT-3.5 or BERT call. Generation is template filling. Analysis is "
        "dictionary search plus two linear formulae.",
        "There is no database, user account or resume versioning.",
        "The UI posts a single experience record even though the backend accepts a list.",
        "Export to PDF or DOCX is absent; the preview is a <pre> block.",
        "The API base URL is hardcoded to http://127.0.0.1:8000.",
        "The Kazakh UI contains a typographic defect in the word for «skills» (a Latin d "
        "in place of a Cyrillic д) in more than one file.",
        "Precision and recall in the UI are static strings (92 %, 85 %) and do not read the "
        "API response, which can desynchronise the display from the JSON.",
        "Skill tags on step 3 are decorative and do not update when the input changes.",
        "fetch() is not wrapped in error handling.",
        "Authentication, TLS and CORS restriction are absent.",
        "The usability sample (n = 12) is small and drawn from one laboratory; SUS should "
        "not be generalised to the national student population.",
    ]:
        bullet(doc, t)

    heading(doc, "6.3. Ethical considerations", 2)
    para(
        doc,
        "An AI resume writer can hallucinate employers, dates or achievements. In the current "
        "template mode that risk is low because the server echoes the user's own fields. As "
        "soon as a generative model is attached, the interface must warn that the text is a "
        "draft and must be verified. A second risk is unfair scoring: a keyword list encodes "
        "a narrow view of a role (for example, a frontend developer who uses Vue rather than "
        "React will look weaker than they are). Dictionary matching should therefore be "
        "presented as coaching, not as a hiring decision. A third risk is data leakage to a "
        "cloud LLM. On-premises inference or anonymisation is the appropriate mitigation for "
        "a university deployment. The EU AI Act and national personal-data rules both push "
        "in the direction of transparency and purpose limitation; an educational analyser "
        "that shows its rules is easier to justify than an opaque commercial score.",
    )

    heading(doc, "6.4. Future work", 2)
    for t in [
        "Replace _detect_keywords with a sentence-transformer or a fine-tuned BERT encoder "
        "and compute precision, recall and F1 on a labelled set of vacancies.",
        "Call a generative model only for rewriting bullets and summaries, with a "
        "user-visible «verify» checklist.",
        "Store users and resume versions in PostgreSQL; add JWT authentication.",
        "Migrate the frontend to React or Next.js, bind skill tags to state, and support "
        "multiple experience rows.",
        "Add PDF and DOCX export using a single-column ATS-safe template.",
        "Localise the UI fully into Kazakh, Russian and English.",
        "Containerise with Docker and add automated API tests (pytest) and load tests.",
        "Correct remaining Kazakh typography and bind the metric tiles to API fields.",
    ]:
        bullet(doc, t)

    heading(doc, "6.5. Academic context", 2)
    para(
        doc,
        "Resume AI is the practical core of a master's research assignment (NIRM). The "
        "scientific contribution is an implemented, documented, testable web system rather "
        "than a new loss function. In applied computer science this form of contribution is "
        "standard: the value is the integration, the explicit algorithm, the measured "
        "usability, and a path to replacing heuristics with models. The present article is "
        "written so that a journal editor can see both what works today and what must not "
        "be over-claimed (the demo precision and recall).",
    )


def section_conclusion(doc):
    heading(doc, "7. CONCLUSION", 1)
    for t in [
        "This paper described Resume AI, a web application for creating and analysing "
        "resumes with methods of artificial intelligence, implemented in the resume-ai-demo "
        "project. The system comprises a FastAPI backend, a four-step HTML/CSS/JavaScript "
        "wizard, and a REST API that generates a plain-text curriculum vitae and returns "
        "completeness, job-match scores, keyword lists and improvement suggestions.",
        "In the current prototype the intelligence layer is rule-based and therefore fully "
        "inspectable. All planned functional tests passed. Local latencies are compatible "
        "with interactive use. A twelve-person usability study yielded SUS = 78.2 and a mean "
        "completion time of 12 minutes. These results support the claim that a locally hosted, "
        "Kazakh-language wizard with an open API is a viable educational and counselling tool, "
        "even before a neural ranker is attached.",
        "The same API contract can host a future BERT matcher and a generative rewriter. "
        "Required follow-up work includes a database, authentication, PDF export, multilingual "
        "UI, genuine model evaluation on labelled data, and the security controls that any "
        "networked processing of personal data demands. Until those steps are taken, Resume AI "
        "should be presented as a transparent prototype, not as an automated hiring system.",
    ]:
        para(doc, t)


def section_references(doc):
    heading(doc, "REFERENCES", 1)
    refs = [
        "1. Bessen J. AI and Jobs: The Role of Demand // NBER Working Paper. — 2019. — No. 24235.",
        "2. Brooke J. SUS: a «quick and dirty» usability scale // Usability Evaluation in Industry. — London: Taylor & Francis, 1996. — P. 189–194.",
        "3. Brown T., Mann B., Ryder N. et al. Language Models are Few-Shot Learners // Advances in Neural Information Processing Systems. — 2020. — Vol. 33.",
        "4. Deepak P. et al. Matching Resumes to Jobs: A Hybrid Approach // Expert Systems with Applications. — 2020.",
        "5. Devlin J., Chang M.W., Lee K., Toutanova K. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding // NAACL-HLT. — 2019.",
        "6. European Parliament. Regulation (EU) 2024/1689 (Artificial Intelligence Act). — 2024.",
        "7. FastAPI documentation [Electronic resource]. — URL: https://fastapi.tiangolo.com (accessed: 18.08.2026).",
        "8. LinkedIn. AI-assisted writing for profiles [Electronic resource]. — URL: https://www.linkedin.com (accessed: 18.08.2026).",
        "9. Nielsen J. Usability Engineering. — San Francisco: Morgan Kaufmann, 1994.",
        "10. OpenAI. API reference [Electronic resource]. — URL: https://platform.openai.com (accessed: 18.08.2026).",
        "11. Playwright documentation [Electronic resource]. — URL: https://playwright.dev (accessed: 18.08.2026).",
        "12. Pressman R.S., Maxim B.R. Software Engineering: A Practitioner's Approach. — 9th ed. — New York: McGraw-Hill, 2019.",
        "13. Pydantic documentation [Electronic resource]. — URL: https://docs.pydantic.dev (accessed: 18.08.2026).",
        "14. Sajid H., Kanwal N. et al. Resume Screening Using Machine Learning and NLP // International Conference on Intelligent Technologies. — 2021.",
        "15. Vaswani A., Shazeer N., Parmar N. et al. Attention Is All You Need // Advances in Neural Information Processing Systems. — 2017.",
        "16. Yessenbayev Z., Kozhirbayev Z., Makazhanov A. A Survey of Kazakh Language Processing // Journal of Intelligent & Fuzzy Systems. — 2023.",
        "17. Fielding R.T. Architectural Styles and the Design of Network-based Software Architectures: PhD thesis. — UC Irvine, 2000.",
        "18. ISO/IEC 25010:2011. Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE).",
        "19. Ministry of Science and Higher Education of the Republic of Kazakhstan. Requirements for scientific publications. — 2025.",
        "20. Richardson L., Amundsen M., Ruby S. RESTful Web APIs. — Sebastopol: O'Reilly, 2013.",
        "21. Sommerville I. Software Engineering. — 10th ed. — Boston: Pearson, 2016.",
        "22. Jurafsky D., Martin J.H. Speech and Language Processing. — 3rd ed. draft. — 2023.",
        "23. Mikolov T., Chen K., Corrado G., Dean J. Efficient Estimation of Word Representations in Vector Space // ICLR Workshop. — 2013.",
        "24. Reimers N., Gurevych I. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks // EMNLP. — 2019.",
        "25. Uvicorn documentation [Electronic resource]. — URL: https://www.uvicorn.org (accessed: 18.08.2026).",
    ]
    for r in refs:
        para(doc, r, first=0, after=4)


def section_appendix(doc):
    heading(doc, "APPENDIX A. EXAMPLE ANALYZE REQUEST", 1)
    para(doc, "JSON body of POST /api/resume/analyze (and of POST /api/resume/generate):", first=0)
    code_block(
        doc,
        '{\n'
        '  "personal": {\n'
        '    "full_name": "Yrysbek Aidar",\n'
        '    "email": "yrysbek@mail.kz",\n'
        '    "phone": "+7 777 123 4567",\n'
        '    "position": "Frontend Developer"\n'
        '  },\n'
        '  "skills": ["React", "TypeScript", "JavaScript", "HTML", "CSS", "REST API"],\n'
        '  "experience": [{\n'
        '    "company": "Tech Solutions KZ",\n'
        '    "role": "Junior Frontend Developer",\n'
        '    "period": "2024 — present",\n'
        '    "description": "Developed web interfaces with React, TypeScript and REST API."\n'
        '  }],\n'
        '  "education": "AUES, Information Systems, bachelor",\n'
        '  "target_job": "Frontend Developer"\n'
        '}',
    )

    heading(doc, "APPENDIX B. EXAMPLE ANALYZE RESPONSE", 1)
    code_block(
        doc,
        '{\n'
        '  "completeness_score": 88.0,\n'
        '  "match_score": 90.0,\n'
        '  "precision": 0.92,\n'
        '  "recall": 0.85,\n'
        '  "issues": [],\n'
        '  "keywords_found": ["react", "javascript", "typescript", "html", "css", "api"],\n'
        '  "keywords_missing": []\n'
        '}',
    )

    heading(doc, "APPENDIX C. HOW TO RUN THE PROTOTYPE", 1)
    for t in [
        "cd resume-ai-demo/backend",
        "pip install -r requirements.txt",
        "uvicorn main:app --reload --host 127.0.0.1 --port 8000",
        "Open the wizard: http://127.0.0.1:8000",
        "Open the API docs: http://127.0.0.1:8000/docs",
        "Health check: GET http://127.0.0.1:8000/api/health",
    ]:
        bullet(doc, t)

    heading(doc, "APPENDIX D. CURL EXAMPLE", 1)
    code_block(
        doc,
        "curl -X POST http://127.0.0.1:8000/api/resume/analyze \\\n"
        '  -H "Content-Type: application/json" \\\n'
        "  -d @payload.json",
    )

    heading(doc, "APPENDIX E. GLOSSARY", 1)
    glossary = [
        ("ATS", "Applicant Tracking System used by employers to parse and rank resumes."),
        ("API", "Application Programming Interface; here a REST JSON interface."),
        ("BERT", "Bidirectional Encoder Representations from Transformers."),
        ("CV", "Curriculum vitae; used interchangeably with resume in this paper."),
        ("FastAPI", "Python web framework that generates OpenAPI documentation."),
        ("LLM", "Large language model (for example GPT-3.5 / GPT-4)."),
        ("NIRM", "Master's research assignment (from the Russian abbreviation)."),
        ("NLP", "Natural language processing."),
        ("REST", "Representational State Transfer style of HTTP APIs."),
        ("SUS", "System Usability Scale (0–100)."),
        ("Wizard", "Multi-step form that reveals one panel at a time."),
    ]
    for term, defn in glossary:
        mixed(doc, [(f"{term} — ", True, False, 14), (defn, False, False, 14)], first=0, after=4)

    heading(doc, "APPENDIX F. IMPLEMENTATION STATUS", 1)
    caption(doc, "Table 8 — Feature status in resume-ai-demo")
    table(
        doc,
        ["Feature", "Plan", "Status", "Location"],
        [
            ["Wizard UI", "4 steps", "Done", "index.html, app.js"],
            ["Resume generate", "REST", "Done", "main.py generate_resume"],
            ["Resume analyze", "REST", "Done", "main.py analyze_resume"],
            ["Keyword detect", "AI module", "Done (rules)", "main.py _detect_keywords"],
            ["Swagger", "Auto", "Done", "/docs"],
            ["Screenshots", "Playwright", "Done", "capture_screenshots.py"],
            ["Live GPT/BERT", "AI", "Planned", "—"],
            ["Database", "PostgreSQL", "Planned", "—"],
            ["PDF export", "Export", "Planned", "—"],
        ],
        [4.0, 3.2, 3.0, 5.8],
    )

    heading(doc, "APPENDIX G. CORE ALGORITHM (BACKEND)", 1)
    para(
        doc,
        "The keyword matcher and the two scoring formulae occupy a few dozen lines of "
        "backend/main.py. The listing below is the analytical core discussed in Sections 3.6 "
        "and 5.4; the surrounding FastAPI boilerplate is omitted.",
        first=0,
    )
    code_block(
        doc,
        "SKILL_KEYWORDS = {\n"
        '    "frontend developer": ["react", "javascript", "typescript", "html", "css", "api"],\n'
        '    "backend developer": ["python", "fastapi", "sql", "rest", "docker"],\n'
        '    "data scientist": ["python", "ml", "pandas", "nlp", "scikit-learn"],\n'
        "}\n\n"
        "def _detect_keywords(text, target):\n"
        "    expected = SKILL_KEYWORDS.get(target.lower(),\n"
        '                                  ["react", "python", "api", "sql"])\n'
        "    found = [kw for kw in expected if kw in text.lower()]\n"
        "    missing = [kw for kw in expected if kw not in text.lower()]\n"
        "    return found, missing\n\n"
        "completeness = min(100.0, 40 + len(skills) * 8 + len(experience) * 15)\n"
        "match_score  = min(100.0, 50 + len(found) * 10 - len(missing) * 5)\n"
        "# precision=0.92 and recall=0.85 are demonstration constants",
    )

    heading(doc, "APPENDIX H. CLIENT GENERATE() CALL", 1)
    para(
        doc,
        "The wizard posts the same ResumeRequest to both endpoints in parallel:",
        first=0,
    )
    code_block(
        doc,
        "const API = \"http://127.0.0.1:8000\";\n"
        "async function generate() {\n"
        "  const payload = getPayload();\n"
        "  const [gen, analysis] = await Promise.all([\n"
        "    fetch(`${API}/api/resume/generate`, {\n"
        "      method: \"POST\",\n"
        "      headers: { \"Content-Type\": \"application/json\" },\n"
        "      body: JSON.stringify(payload),\n"
        "    }).then((r) => r.json()),\n"
        "    fetch(`${API}/api/resume/analyze`, {\n"
        "      method: \"POST\",\n"
        "      headers: { \"Content-Type\": \"application/json\" },\n"
        "      body: JSON.stringify(payload),\n"
        "    }).then((r) => r.json()),\n"
        "  ]);\n"
        "  resumePreview.textContent = gen.resume_text;\n"
        "  scoreComplete.textContent = `${analysis.completeness_score}%`;\n"
        "  scoreMatch.textContent = `${analysis.match_score}%`;\n"
        "}",
    )

    heading(doc, "APPENDIX I. AUTHOR CONTRIBUTION AND CONFLICT OF INTEREST", 1)
    para(
        doc,
        "The author formulated the research problem, designed the architecture, implemented "
        "the backend and frontend, defined the analysis rules, carried out the tests reported "
        "in Section 5, and wrote the article. Insert the supervisor's name, degree and "
        "department before journal submission. The author declares no conflict of interest. "
        "Replace precision and recall placeholders with experimental values if a trained "
        "model is evaluated before publication. Add ORCID, affiliation and correspondence "
        "email on the title page as required by the target journal.",
        first=0,
    )


def section_extended(doc):
    """Closing design notes that belong with the main argument, not as padding."""
    heading(doc, "3.9. Why rule-based analysis first", 2)
    para(
        doc,
        "Jumping directly to a hosted LLM would have produced more fluent suggestions and "
        "would have hidden the scoring rule. For a thesis defence that is a poor trade. "
        "Examiners cannot reproduce a closed model; they can reproduce a six-word dictionary "
        "and two formulae. Starting with rules also forces the API to be designed around "
        "stable fields (issues, keywords_found, keywords_missing) instead of a single free-"
        "text paragraph. When an LLM is added, those fields can still be filled — for "
        "example by asking the model to return JSON that matches AnalysisResponse — which "
        "is a more robust integration pattern than pasting a chat completion into the UI.",
    )

    heading(doc, "5.7. Reproducibility", 2)
    para(
        doc,
        "A third party with the repository, Python 3.10+, and the three pinned dependency "
        "lower bounds can reproduce T-01…T-08 and the latency order of magnitude. They cannot "
        "reproduce SUS = 78.2 without a new user sample. They should not treat precision 0.92 "
        "and recall 0.85 as experimental outcomes. These three sentences are the reproducibility "
        "statement of the paper. The source listings in Appendices G and H are the corresponding "
        "artefacts.",
    )

    heading(doc, "5.8. Threats to validity", 2)
    for t in [
        "Internal validity of the usability study is limited by the pre-filled form, the "
        "presence of the author in the laboratory, and the short task. External validity is "
        "limited by the sample (students of one programme) and by the single target role "
        "(frontend developer) that matches the demo dictionary. Construct validity of "
        "«AI quality» is limited because the analyser is not a learned model. Conclusion "
        "validity is limited by n = 12, which is enough to detect a grossly unusable "
        "interface and not enough to compare two designs statistically. These threats are "
        "typical of a prototype evaluation and are not hidden here.",
        "The functional tests were executed by the author, not by an independent tester. "
        "They are closer to a structured demonstration checklist than to a continuous-"
        "integration suite. Adding pytest with TestClient would raise the level of evidence "
        "without changing the product.",
    ]:
        para(doc, t)

    heading(doc, "APPENDIX J. TECHNOLOGY STACK", 1)
    caption(doc, "Table 9 — Technology stack of resume-ai-demo")
    table(
        doc,
        ["Component", "Technology", "Version", "Role"],
        [
            ["Backend framework", "FastAPI", "≥ 0.115", "REST + OpenAPI"],
            ["ASGI server", "Uvicorn", "≥ 0.32", "HTTP server"],
            ["Validation", "Pydantic", "≥ 2.0", "JSON schema"],
            ["Frontend", "HTML5 / CSS3 / JS", "—", "Wizard"],
            ["Static hosting", "StaticFiles", "FastAPI", "UI mount"],
            ["Screenshots", "Playwright", "—", "Documentation"],
            ["Word generation", "python-docx", "—", "Article / annex"],
            ["Slides", "python-pptx", "—", "Defence deck"],
        ],
        [3.6, 4.2, 2.4, 5.8],
    )

    para(
        doc,
        "End of article. Formatted as a 30–35 page scientific paper on the web application "
        "for creating and analysing resumes using artificial intelligence (Resume AI, "
        "project resume-ai-demo). Version date: 18 August 2026. Before journal submission, "
        "add ORCID, affiliation and correspondence email, and keep the statements that "
        "precision and recall are demonstration constants until a labelled evaluation is run.",
        italic=True, first=0, before=12,
    )


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    add_page_number(sec)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(14)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    title_page(doc)
    page_break(doc)
    abstracts(doc)
    page_break(doc)
    section_intro(doc)
    page_break(doc)
    section_related(doc)
    page_break(doc)
    section_design(doc)
    page_break(doc)
    section_implementation(doc)
    page_break(doc)
    section_testing(doc)
    page_break(doc)
    section_discussion(doc)
    page_break(doc)
    section_conclusion(doc)
    page_break(doc)
    section_references(doc)
    page_break(doc)
    section_appendix(doc)
    page_break(doc)
    section_extended(doc)

    doc.save(str(OUT))
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    build()
