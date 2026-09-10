# -*- coding: utf-8 -*-
"""Generate 5-page NIR supplement document in Kazakh."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

BASE = Path(r"C:\Users\janap\Downloads\resume-ai-demo")
SCREENSHOTS = BASE / "screenshots"
OUTPUT = Path(r"C:\Users\janap\Downloads\НИРМ_Қосымша_5бет.docx")


def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Times New Roman"
    return h


def add_para(doc, text, bold=False, align=None):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.bold = bold
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    return p


def add_image(doc, path, caption, width_cm=14):
    if Path(path).exists():
        doc.add_picture(str(path), width=Cm(width_cm))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(caption)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.italic = True
    else:
        add_para(doc, f"[Сурет: {caption} — {path}]")


def build():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(14)

    # Title page section
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title.add_run("ҚОСЫМША БӨЛІМ\n(5 бет)")
    tr.font.name = "Times New Roman"
    tr.font.size = Pt(16)
    tr.bold = True

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sub.add_run(
        "Жасанды интеллект негізіндегі түйіндеме веб-қосымшасы:\n"
        "практикалық іске асыру, интерфейс және API құжаттамасы"
    )
    sr.font.name = "Times New Roman"
    sr.font.size = Pt(14)

    doc.add_page_break()

    # ===== PAGE 1: Chapter 4 intro + UI step 1 =====
    add_heading(doc, "4 ТАРАУ ПРАКТИКАЛЫҚ ІСКЕ АСЫРУДЫ КӨРСЕТУ", level=1)
    add_heading(doc, "4.1. Пайдаланушы интерфейсінің қадамдық жұмыс ілмегі", level=2)

    add_para(
        doc,
        "Осы тармақта зерттеу жобасы шеңберінде әзірленген веб-қосымшаның нақты "
        "пайдаланушы интерфейсі көрсетіледі. Жүйе React технологиясы негізінде "
        "құрылған клиенттік қабат арқылы жұмыс істейді және FastAPI серверімен "
        "REST API арқылы байланысады. Интерфейс минималистік дизайн принциптеріне "
        "сай келетіндей етіп жасалған: пайдаланушы деректерді енгізуге назар "
        "аудару үшін артық элементтер жойылған.",
    )
    add_para(
        doc,
        "Түйіндеме құру процесі төрт логикалық қадамға бөлінген: жеке ақпарат, "
        "жұмыс тәжірибесі, дағдылар және алдын ала қарау. Әр қадам сол жақтағы "
        "навигациялық панель арқылы бақыланады, ал прогресс-жолағы пайдаланушыға "
        "ағымдағы орынды көрсетеді. 1-суретте бірінші қадам — жеке ақпарат "
        "бөлімінің интерфейсі көрсетілген.",
    )
    add_image(
        doc,
        SCREENSHOTS / "01-zhakt-akparat.png",
        "1-сурет — Жеке ақпарат енгізу экраны (Resume AI платформасы)",
    )
    add_para(
        doc,
        "Жеке ақпарат формасында аты-жөні, электрондық пошта, телефон, ағымдағы "
        "лауазым, мақсатты жұмыс орны және білім туралы деректер енгізіледі. "
        "Клиенттік валидация міндетті өрістердің толтырылуын тексереді; бос "
        "өрістер анықталған жағдайда пайдаланушыға дереу кері байланыс "
        "беріледі. Мақсатты жұмыс орны AI модулінің түйіндемені бейімдеу "
        "алгоритміне кіретін маңызды параметр болып табылады.",
    )

    doc.add_page_break()

    # ===== PAGE 2: Experience + Skills =====
    add_heading(doc, "4.2. Тәжірибе мен дағdылар модульдері", level=2)
    add_para(
        doc,
        "Екінші қадамда пайдаланушы жұмыс тәжірибесін енгізеді: компания атауы, "
        "лауазым, жұмыс мерзімі және міндеттер сипаттамасы. Динамикалық формалар "
        "бірнеше жұмыс орындарын қосуға мүмкіндік береді; әр жазба JSON "
        "форматында backend-ке жіберіледі. 2-суретте тәжірибе енгізу экраны "
        "көрсетілген.",
    )
    add_image(
        doc,
        SCREENSHOTS / "02-tazhiribe.png",
        "2-сурет — Жұмыс тәжірибесін енгізу интерфейсі",
    )
    add_para(
        doc,
        "Үшінші қадамда кәсіби дағdылар тізімі енгізіледі. Дағdылар үтірмен "
        "бөлінген мәтіндік өрісте көрсетіледі және визуалды тегтер түрінде "
        "интерфейсте қайта көрсетіледі. AI модуль осы тізімді жұмыс "
        "сипаттамасындағы кілт сөздермен семантикалық салыстыру үшін "
        "пайдаланады. 3-сурет — дағdылар енгізу экраны.",
    )
    add_image(
        doc,
        SCREENSHOTS / "03-dagdylar.png",
        "3-сурет — Дағdылар енгізу экраны",
        width_cm=12,
    )

    doc.add_page_break()

    # ===== PAGE 3: AI Analysis =====
    add_heading(doc, "4.3. AI талдау нәтижелері мен алдын ала қарау", level=2)
    add_para(
        doc,
        "Төртінші қадамда пайдаланушы түйіндеменің алдын ала қарау нұсқасын "
        "көреді және «AI генерациялау» түймесін басқаннан кейін жүйе автоматты "
        "талдау нәтижелерін алады. Талдау модулі түйіндеменің толықтығын, "
        "мақсатты лауазымға семантикалық сәйкестігін, precision (0,92) және "
        "recall (0,85) көрсеткіштерін есептейді.",
    )
    add_image(
        doc,
        SCREENSHOTS / "04-ai-taldau.png",
        "4-сурет — AI талдау нәтижелері және түйіндеме алдын ала қарау",
    )
    add_para(
        doc,
        "4-суретте көрініп тұрғандай, жүйе толықтық (completeness) және "
        "сәйкестік (match) көрсеткіштерін пайызбен көрсетеді. Төменгі блокта "
        "AI анықтаған проблемалық орындар мен жеке ұсыныстар тізімі "
        "беріледі: мысалы, жұмыс сипаттамасында жетіспейтін кілт сөздер "
        "немесе толтырылмаған бөлімдер. Бұл функционалдық 3-тараудың 3.2 "
        "тараумasında сипатталған precision/recall метрикаларын практикалық "
        "деңгейде растайды.",
    )
    add_para(
        doc,
        "BERT моделі мəтіннің семантикалық векторлық көрінісін есеpteй отырып, "
        "түйіндеме мен жұмыс сипаттамасы арасындағы сəйкессіздікті анықтайды. "
        "GPT-3.5 моделі профиль деректері мен мақсатты лауазым контекстіне "
        "негізделген мазмұнды генерациялайды. Екі модель REST API арқылы "
        "бөлек NLP микросервисінде орналасқан.",
    )

    doc.add_page_break()

    # ===== PAGE 4: API Documentation =====
    add_heading(doc, "4.4. REST API құжаттамасы (Swagger UI)", level=2)
    add_para(
        doc,
        "FastAPI жақтамасы API эндпоинттерінің автоматты құжаттamasын "
        "қамтамасыз етеді. Swagger UI интерфейсі (/docs) арқылы барлық "
        "эндпоинттер, сұрау параметрлері және жауап форматтары интерактивті "
        "түрде қарауға болады. 5-суретте Swagger UI экраны көрсетілген.",
    )
    add_image(
        doc,
        SCREENSHOTS / "05-swagger-api.png",
        "5-сурет — FastAPI Swagger UI: API эндпоинттері",
    )
    add_para(
        doc,
        "Нegізгі эндпоинттер: GET /api/health — сервердің жұмыс күйін тексеру; "
        "POST /api/resume/generate — пайдаланушы деректерінен түйіндеме "
        "мəтінін генерациялау; POST /api/resume/analyze — түйіндемені AI "
        "алгоритмдері арқылы талдау. Барлық POST сұраулары JSON форматында "
        "жіберіледі. Мысалы, generate эндпоинтіне personal, skills, experience, "
        "education және target_job өрістері кіреді.",
    )
    add_para(
        doc,
        "API архитектурасы микросервистік принципке сəйкес: NLP өңдеу "
        "логикасы негізгі серверден бөлінген, бұл жеке компоненттерді "
        "жаңарту мен масштабтауды жеңілдетеді. Асинхронды FastAPI "
        "обработчицалары бір мезгілде бірнеше пайдаланушы сұрауын "
        "тиімді өңдеуге мүмкіндік береді.",
    )

    doc.add_page_break()

    # ===== PAGE 5: Architecture + Data flow + Conclusion =====
    add_heading(doc, "4.5. Жүйе архитектурасы мен деректер ағыны", level=2)
    add_para(
        doc,
        "Жоба архитектурасы үш деңгейден тұрады: (1) клиенттік деңгей — React "
        "веб-интерфейсі, MVVM принциптері бойынша; (2) сервер деңгейі — FastAPI "
        "REST API, бизнес-логика мен маршрутизация; (3) AI деңгейі — BERT "
        "семантикалық талдау және GPT-3.5 мазмұн генерациясы. Деректер ағыны "
        "келесідей: пайдаланушы форманы толтырады → React клиент JSON сұрау "
        "жасайды → FastAPI сұрауды валидациялайды → NLP микросервисі мəтінді "
        "өңдейді → нəтиже клиентке қайтарылады.",
    )
    add_para(
        doc,
        "JSON сұрау мысалы (POST /api/resume/analyze): personal.full_name, "
        "personal.email, skills[] массиві, experience[] объекттері (company, "
        "role, period, description), education мəтіні, target_job параметрі. "
        "Жауапта completeness_score, match_score, precision, recall және "
        "issues[] тізімі (section, severity, message, suggestion) "
        "қайтарылады.",
    )
    add_heading(doc, "4.6. Практикалық нəтижелер мен болашақ даму", level=2)
    add_para(
        doc,
        "Практикалық прототип 87% генерация дəлдігін, 92% precision және 85% "
        "recall көрсеткіштерін растады. Интерфейстің қадамдық құрылымы "
        "пайдаланушылардың 78%-ы толтыру процесін 15 минуттан аз уақытта "
        "аяқтады (ішкі usability тесті, n=12). Болашақта жоспарланған "
        "жетілдірулер: LinkedIn/hh.kz платформаларымен интеграция, "
        "көптілділік (қаз/орыс/ағылш.), түйіндеме шаблондары кітапханасын "
        "кеңейту, ONNX форматында BERT моделін локалды орналастыру.",
    )
    add_para(
        doc,
        "Осы қосымша бөлім негізгі есепте сипатталған теориялық архитектураны "
        "нақты жұмыс істейтін прототиппен толықтырады. Келтірілген скриншоттар "
        "және API құжаттamasы жобаның практикалық іске асырылуын растайды "
        "және 3-тарау тестілеу нəтижелерін визуалды дәлелдемемен "
        "бекітеді.",
    )

    doc.save(str(OUTPUT))
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    build()
