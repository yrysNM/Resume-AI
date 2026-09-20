const API = "http://127.0.0.1:8000";
let currentStep = 1;

/* ---------- i18n ---------- */
const I18N = {
  kk: {
    doc_title: "Resume AI — Түйіндеме платформасы",
    nav_resume: "Түйіндеме",
    nav_analysis: "Талдау",
    steps_title: "Қадамдар",
    step1: "Жеке ақпарат",
    step2: "Тәжірибе",
    step3: "Дағдылар",
    step4: "Алдын ала қарау",
    title: "Түйіндеме құру",
    subtitle: "Жасанды интеллект арқылы мақсатты лауазымға бейімделген CV",
    panel1: "1. Жеке ақпарат",
    full_name: "Аты-жөні",
    email: "Email",
    phone: "Телефон",
    position: "Лауазым",
    target_job: "Мақсатты жұмыс",
    education: "Білім",
    panel2: "2. Жұмыс тәжірибесі",
    company: "Компания",
    role: "Лауазым",
    period: "Кезең",
    description: "Сипаттама",
    panel3: "3. Дағдылар",
    panel4: "4. Алдын ала қарау және AI талдау",
    resume_box: "Түйіндеме",
    analysis_box: "AI талдау нәтижелері",
    completeness: "Толықтығы",
    match: "Сәйкестік",
    placeholder: "Толтыруды аяқтаңыз...",
    no_issues: "Түйіндеме жақсы сапада — ескерту жоқ",
    prev: "Артқа",
    next: "Келесі",
    generate: "AI генерациялау",
  },
  ru: {
    doc_title: "Resume AI — Платформа для резюме",
    nav_resume: "Резюме",
    nav_analysis: "Анализ",
    steps_title: "Шаги",
    step1: "Личные данные",
    step2: "Опыт",
    step3: "Навыки",
    step4: "Предпросмотр",
    title: "Создание резюме",
    subtitle: "Резюме, адаптированное под целевую должность с помощью искусственного интеллекта",
    panel1: "1. Личные данные",
    full_name: "ФИО",
    email: "Email",
    phone: "Телефон",
    position: "Должность",
    target_job: "Целевая работа",
    education: "Образование",
    panel2: "2. Опыт работы",
    company: "Компания",
    role: "Должность",
    period: "Период",
    description: "Описание",
    panel3: "3. Навыки",
    panel4: "4. Предпросмотр и ИИ-анализ",
    resume_box: "Резюме",
    analysis_box: "Результаты ИИ-анализа",
    completeness: "Полнота",
    match: "Соответствие",
    placeholder: "Завершите заполнение...",
    no_issues: "Резюме хорошего качества — замечаний нет",
    prev: "Назад",
    next: "Далее",
    generate: "Сгенерировать с ИИ",
  },
  en: {
    doc_title: "Resume AI — Resume Platform",
    nav_resume: "Resume",
    nav_analysis: "Analysis",
    steps_title: "Steps",
    step1: "Personal info",
    step2: "Experience",
    step3: "Skills",
    step4: "Preview",
    title: "Create a resume",
    subtitle: "A CV tailored to your target position with the help of artificial intelligence",
    panel1: "1. Personal info",
    full_name: "Full name",
    email: "Email",
    phone: "Phone",
    position: "Position",
    target_job: "Target job",
    education: "Education",
    panel2: "2. Work experience",
    company: "Company",
    role: "Role",
    period: "Period",
    description: "Description",
    panel3: "3. Skills",
    panel4: "4. Preview and AI analysis",
    resume_box: "Resume",
    analysis_box: "AI analysis results",
    completeness: "Completeness",
    match: "Match",
    placeholder: "Finish filling in the form...",
    no_issues: "The resume is in good shape — no warnings",
    prev: "Back",
    next: "Next",
    generate: "Generate with AI",
  },
};

const SUPPORTED_LANGS = Object.keys(I18N);
let lang = "kk";
try {
  const saved = localStorage.getItem("lang");
  if (SUPPORTED_LANGS.includes(saved)) lang = saved;
} catch (e) { /* storage unavailable */ }

const t = (key) => I18N[lang][key] ?? I18N.kk[key] ?? key;

let lastResult = null; // { gen, analysis } after the first successful generation

function applyLang() {
  document.documentElement.lang = lang;
  document.title = t("doc_title");
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll(".lang-btn").forEach((b) => {
    const active = b.dataset.lang === lang;
    b.classList.toggle("active", active);
    b.setAttribute("aria-pressed", String(active));
  });
  renderResults();
}

function setLang(next) {
  if (!SUPPORTED_LANGS.includes(next)) return;
  lang = next;
  try { localStorage.setItem("lang", lang); } catch (e) { /* ignore */ }
  applyLang();
}

/* ---------- Wizard ---------- */
const panels = ["panel-personal", "panel-experience", "panel-skills", "panel-preview"];
const steps = document.querySelectorAll(".step");
const progressFill = document.querySelector(".progress-fill");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const generateBtn = document.getElementById("generateBtn");

function showStep(n) {
  currentStep = n;
  panels.forEach((id, i) => {
    document.getElementById(id).classList.toggle("hidden", i !== n - 1);
  });
  steps.forEach((s, i) => s.classList.toggle("active", i === n - 1));
  progressFill.style.width = `${n * 25}%`;
  prevBtn.disabled = n === 1;
  nextBtn.classList.toggle("hidden", n === 4);
  generateBtn.classList.toggle("hidden", n !== 4);
}

function getPayload() {
  const f = document.getElementById("resumeForm");
  const skills = f.skills.value.split(",").map((s) => s.trim()).filter(Boolean);
  return {
    personal: {
      full_name: f.full_name.value,
      email: f.email.value,
      phone: f.phone.value,
      position: f.position.value,
    },
    skills,
    experience: [
      {
        company: f.company.value,
        role: f.role.value,
        period: f.period.value,
        description: f.description.value,
      },
    ],
    education: f.education.value,
    target_job: f.target_job.value,
  };
}

function renderResults() {
  const preview = document.getElementById("resumePreview");
  const list = document.getElementById("issuesList");

  if (!lastResult) {
    preview.textContent = t("placeholder");
    return;
  }

  const { gen, analysis } = lastResult;
  preview.textContent = gen.resume_text;
  document.getElementById("scoreComplete").textContent = `${analysis.completeness_score}%`;
  document.getElementById("scoreMatch").textContent = `${analysis.match_score}%`;

  list.innerHTML = "";
  if (analysis.issues.length === 0) {
    const li = document.createElement("li");
    li.style.borderColor = "#22c55e";
    li.textContent = t("no_issues");
    list.appendChild(li);
  } else {
    analysis.issues.forEach((issue) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${issue.section}:</strong> ${issue.message}<br><em>${issue.suggestion}</em>`;
      list.appendChild(li);
    });
  }
}

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

  lastResult = { gen, analysis };
  renderResults();
}

prevBtn.addEventListener("click", () => showStep(Math.max(1, currentStep - 1)));
nextBtn.addEventListener("click", () => showStep(Math.min(4, currentStep + 1)));
generateBtn.addEventListener("click", generate);
steps.forEach((s) => s.addEventListener("click", () => showStep(Number(s.dataset.step))));
document.querySelectorAll(".lang-btn").forEach((b) =>
  b.addEventListener("click", () => setLang(b.dataset.lang))
);

showStep(1);
applyLang();