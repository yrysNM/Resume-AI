// Same-origin when UI is served by FastAPI; override for a split frontend host.
const API = window.location.origin.includes("8000")
  ? ""
  : "http://127.0.0.1:8000";
const TOKEN_KEY = "resume_ai_token";
let currentStep = 1;
let authMode = "login"; // login | register
let currentUser = null;

/* ---------- i18n ---------- */
const I18N = {
  kk: {
    doc_title: "Resume AI — Түйіндеме платформасы",
    nav_resume: "Түйіндеме",
    nav_analysis: "Талдау",
    nav_saved: "Сақталған",
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
    add_experience: "+ Тәжірибе қосу",
    remove_experience: "Жою",
    experience_n: "Тәжірибе",
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
    export_pdf: "PDF жүктеу",
    export_docx: "DOCX жүктеу",
    export_failed: "Экспорт сәтсіз",
    login: "Кіру",
    register: "Тіркелу",
    logout: "Шығу",
    password: "Құпия сөз",
    cancel: "Болдырмау",
    auth_required: "Генерация үшін кіріңіз немесе тіркеліңіз.",
    saved_title: "Сақталған",
    saved_empty: "Кіріңіз — түйіндемелер осында",
    saved_none: "Әлі сақталған түйіндеме жоқ",
    load_failed: "Жүктеу сәтсіз",
    auth_failed: "Кіру сәтсіз",
    generate_failed: "Генерация сәтсіз",
    delete: "Жою",
    delete_failed: "Жою сәтсіз",
  },
  ru: {
    doc_title: "Resume AI — Платформа для резюме",
    nav_resume: "Резюме",
    nav_analysis: "Анализ",
    nav_saved: "Сохранённые",
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
    add_experience: "+ Добавить опыт",
    remove_experience: "Удалить",
    experience_n: "Опыт",
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
    export_pdf: "Скачать PDF",
    export_docx: "Скачать DOCX",
    export_failed: "Ошибка экспорта",
    login: "Войти",
    register: "Регистрация",
    logout: "Выйти",
    password: "Пароль",
    cancel: "Отмена",
    auth_required: "Чтобы генерировать, войдите или зарегистрируйтесь.",
    saved_title: "Сохранённые",
    saved_empty: "Войдите — резюме появятся здесь",
    saved_none: "Пока нет сохранённых резюме",
    load_failed: "Не удалось загрузить",
    auth_failed: "Ошибка входа",
    generate_failed: "Ошибка генерации",
    delete: "Удалить",
    delete_failed: "Не удалось удалить",
  },
  en: {
    doc_title: "Resume AI — Resume Platform",
    nav_resume: "Resume",
    nav_analysis: "Analysis",
    nav_saved: "Saved",
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
    add_experience: "+ Add experience",
    remove_experience: "Remove",
    experience_n: "Experience",
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
    export_pdf: "Download PDF",
    export_docx: "Download DOCX",
    export_failed: "Export failed",
    login: "Log in",
    register: "Sign up",
    logout: "Log out",
    password: "Password",
    cancel: "Cancel",
    auth_required: "Log in or sign up to generate and save resumes.",
    saved_title: "Saved",
    saved_empty: "Log in — resumes appear here",
    saved_none: "No saved resumes yet",
    load_failed: "Failed to load",
    auth_failed: "Authentication failed",
    generate_failed: "Generation failed",
    delete: "Delete",
    delete_failed: "Delete failed",
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

function getToken() {
  try { return localStorage.getItem(TOKEN_KEY); } catch (e) { return null; }
}

function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch (e) { /* ignore */ }
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${API}${path}`, { ...options, headers });
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = { detail: text }; }
  if (!res.ok) {
    const detail = data?.detail;
    const message = typeof detail === "string"
      ? detail
      : Array.isArray(detail)
        ? detail.map((d) => d.msg || JSON.stringify(d)).join("; ")
        : res.statusText;
    const err = new Error(message || `HTTP ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}

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
  syncAuthModalLabels();
  refreshExperienceLabels();
  renderResults();
}

function setLang(next) {
  if (!SUPPORTED_LANGS.includes(next)) return;
  lang = next;
  try { localStorage.setItem("lang", lang); } catch (e) { /* ignore */ }
  applyLang();
}

/* ---------- Auth UI ---------- */
const authModal = document.getElementById("authModal");
const authForm = document.getElementById("authForm");
const authError = document.getElementById("authError");
const authUserEl = document.getElementById("authUser");
const loginOpenBtn = document.getElementById("loginOpenBtn");
const registerOpenBtn = document.getElementById("registerOpenBtn");
const logoutBtn = document.getElementById("logoutBtn");
const authHint = document.getElementById("authHint");

function syncAuthModalLabels() {
  const title = document.getElementById("authModalTitle");
  const submit = document.getElementById("authSubmitBtn");
  const label = authMode === "register" ? t("register") : t("login");
  title.textContent = label;
  submit.textContent = label;
}

function openAuthModal(mode) {
  authMode = mode;
  authError.classList.add("hidden");
  authError.textContent = "";
  const nameField = authForm.querySelector(".auth-name-field");
  if (nameField) {
    nameField.classList.toggle("hidden", mode !== "register");
  }
  authForm.password.autocomplete = mode === "register" ? "new-password" : "current-password";
  syncAuthModalLabels();
  authModal.classList.remove("hidden");
  authForm.email.focus();
}

function closeAuthModal() {
  authModal.classList.add("hidden");
}

function renderAuthState() {
  const loggedIn = Boolean(currentUser);
  authUserEl.classList.toggle("hidden", !loggedIn);
  logoutBtn.classList.toggle("hidden", !loggedIn);
  loginOpenBtn.classList.toggle("hidden", loggedIn);
  registerOpenBtn.classList.toggle("hidden", loggedIn);
  authHint.classList.toggle("hidden", loggedIn);
  if (loggedIn) {
    authUserEl.textContent = currentUser.full_name || currentUser.email;
  }
}

async function refreshSession() {
  const token = getToken();
  if (!token) {
    currentUser = null;
    renderAuthState();
    renderSavedList([]);
    return;
  }
  try {
    currentUser = await api("/api/auth/me");
    renderAuthState();
    await loadSavedResumes();
  } catch (e) {
    setToken(null);
    currentUser = null;
    renderAuthState();
    renderSavedList([]);
  }
}

async function handleAuthSubmit(event) {
  event.preventDefault();
  authError.classList.add("hidden");
  const email = authForm.email.value.trim();
  const password = authForm.password.value;
  const full_name = authForm.full_name.value.trim();
  const path = authMode === "register" ? "/api/auth/register" : "/api/auth/login";
  const body = authMode === "register"
    ? { email, password, full_name }
    : { email, password };
  try {
    const data = await api(path, { method: "POST", body: JSON.stringify(body) });
    setToken(data.access_token);
    closeAuthModal();
    authForm.reset();
    await refreshSession();
  } catch (e) {
    authError.textContent = e.message || t("auth_failed");
    authError.classList.remove("hidden");
  }
}

function logout() {
  setToken(null);
  currentUser = null;
  lastResult = null;
  renderAuthState();
  renderSavedList([]);
  renderResults();
}

/* ---------- Saved resumes ---------- */
const savedList = document.getElementById("savedList");

function renderSavedList(items) {
  savedList.innerHTML = "";
  if (!currentUser) {
    const li = document.createElement("li");
    li.className = "saved-empty";
    li.textContent = t("saved_empty");
    savedList.appendChild(li);
    return;
  }
  if (!items.length) {
    const li = document.createElement("li");
    li.className = "saved-empty";
    li.textContent = t("saved_none");
    savedList.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.className = "saved-row";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "saved-item";
    btn.textContent = item.title || item.target_job || `#${item.id}`;
    btn.addEventListener("click", () => openSavedResume(item.id));
    const del = document.createElement("button");
    del.type = "button";
    del.className = "saved-delete";
    del.setAttribute("aria-label", t("delete"));
    del.title = t("delete");
    del.textContent = "×";
    del.addEventListener("click", (event) => {
      event.stopPropagation();
      deleteSavedResume(item.id);
    });
    li.appendChild(btn);
    li.appendChild(del);
    savedList.appendChild(li);
  });
}

async function deleteSavedResume(id) {
  try {
    await api(`/api/resumes/${id}`, { method: "DELETE" });
    if (lastResult?.gen?.id === id) {
      lastResult = null;
      renderResults();
    }
    await loadSavedResumes();
  } catch (e) {
    alert(e.message || t("delete_failed"));
  }
}

async function loadSavedResumes() {
  if (!currentUser) {
    renderSavedList([]);
    return;
  }
  try {
    const items = await api("/api/resumes");
    renderSavedList(items);
  } catch (e) {
    renderSavedList([]);
  }
}

async function openSavedResume(id) {
  try {
    const detail = await api(`/api/resumes/${id}`);
    lastResult = {
      gen: {
        id: detail.id,
        resume_text: detail.resume_text,
        generated_by: detail.generated_by,
      },
      analysis: detail.analysis || {
        completeness_score: "—",
        match_score: "—",
        precision: 0.92,
        recall: 0.85,
        issues: [],
      },
    };
    showStep(4);
    renderResults();
  } catch (e) {
    alert(e.message || t("load_failed"));
  }
}

/* ---------- Experience entries ---------- */
const experienceList = document.getElementById("experienceList");
const addExperienceBtn = document.getElementById("addExperienceBtn");

const DEFAULT_EXPERIENCE = [
  {
    company: "Tech Solutions KZ",
    role: "Junior Frontend Developer",
    period: "2024 — қазіргі уақыт",
    description:
      "React, TypeScript және REST API қолданып веб-интерфейстерді әзірледім. UI компоненттерін қайта пайдалану арқылы әзірлеу уақытын 30% қысқарттым.",
  },
];

function createExperienceEntry(values = {}) {
  const entry = document.createElement("div");
  entry.className = "experience-entry";
  entry.innerHTML = `
    <div class="experience-entry-header">
      <span class="experience-entry-title"></span>
      <button type="button" class="btn secondary btn-sm remove-experience" data-i18n="remove_experience"></button>
    </div>
    <div class="grid">
      <label><span data-i18n="company"></span><input class="exp-company" /></label>
      <label><span data-i18n="role"></span><input class="exp-role" /></label>
      <label class="full"><span data-i18n="period"></span><input class="exp-period" /></label>
      <label class="full"><span data-i18n="description"></span><textarea class="exp-description"></textarea></label>
    </div>
  `;
  entry.querySelector(".exp-company").value = values.company || "";
  entry.querySelector(".exp-role").value = values.role || "";
  entry.querySelector(".exp-period").value = values.period || "";
  entry.querySelector(".exp-description").value = values.description || "";
  entry.querySelector(".remove-experience").addEventListener("click", () => {
    if (experienceList.children.length <= 1) {
      entry.querySelector(".exp-company").value = "";
      entry.querySelector(".exp-role").value = "";
      entry.querySelector(".exp-period").value = "";
      entry.querySelector(".exp-description").value = "";
      return;
    }
    entry.remove();
    refreshExperienceLabels();
  });
  experienceList.appendChild(entry);
  refreshExperienceLabels();
  return entry;
}

function refreshExperienceLabels() {
  experienceList.querySelectorAll(".experience-entry").forEach((entry, i) => {
    const title = entry.querySelector(".experience-entry-title");
    if (title) title.textContent = `${t("experience_n")} ${i + 1}`;
    entry.querySelectorAll("[data-i18n]").forEach((el) => {
      el.textContent = t(el.dataset.i18n);
    });
  });
  const canRemove = experienceList.children.length > 1;
  experienceList.querySelectorAll(".remove-experience").forEach((btn) => {
    btn.disabled = !canRemove;
  });
}

function collectExperience() {
  return Array.from(experienceList.querySelectorAll(".experience-entry")).map((entry) => ({
    company: entry.querySelector(".exp-company").value.trim(),
    role: entry.querySelector(".exp-role").value.trim(),
    period: entry.querySelector(".exp-period").value.trim(),
    description: entry.querySelector(".exp-description").value.trim(),
  })).filter((item) => item.company || item.role || item.period || item.description);
}

addExperienceBtn.addEventListener("click", () => createExperienceEntry());
DEFAULT_EXPERIENCE.forEach((item) => createExperienceEntry(item));

/* ---------- Wizard ---------- */
const panels = ["panel-personal", "panel-experience", "panel-skills", "panel-preview"];
const steps = document.querySelectorAll(".step");
const progressFill = document.querySelector(".progress-fill");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const generateBtn = document.getElementById("generateBtn");
const exportPdfBtn = document.getElementById("exportPdfBtn");
const exportDocxBtn = document.getElementById("exportDocxBtn");

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
    experience: collectExperience(),
    education: f.education.value,
    target_job: f.target_job.value,
  };
}

function syncExportButtons() {
  const ready = Boolean(lastResult?.gen?.id);
  exportPdfBtn.disabled = !ready;
  exportDocxBtn.disabled = !ready;
}

async function exportResume(fmt) {
  const id = lastResult?.gen?.id;
  if (!id) return;
  if (!currentUser) {
    openAuthModal("login");
    return;
  }
  try {
    const token = getToken();
    const res = await fetch(`${API}/api/resumes/${id}/export?format=${fmt}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) {
      const text = await res.text();
      let message = res.statusText;
      try {
        const data = JSON.parse(text);
        message = typeof data.detail === "string" ? data.detail : message;
      } catch (e) { /* ignore */ }
      throw Object.assign(new Error(message), { status: res.status });
    }
    const blob = await res.blob();
    const disposition = res.headers.get("Content-Disposition") || "";
    const match = /filename="?([^"]+)"?/i.exec(disposition);
    const filename = match ? match[1] : `resume.${fmt}`;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (e) {
    if (e.status === 401) {
      logout();
      openAuthModal("login");
      return;
    }
    alert(e.message || t("export_failed"));
  }
}

function renderResults() {
  const preview = document.getElementById("resumePreview");
  const list = document.getElementById("issuesList");

  if (!lastResult) {
    preview.textContent = t("placeholder");
    syncExportButtons();
    return;
  }

  const { gen, analysis } = lastResult;
  preview.textContent = gen.resume_text;
  document.getElementById("scoreComplete").textContent =
    analysis.completeness_score === "—" ? "—" : `${analysis.completeness_score}%`;
  document.getElementById("scoreMatch").textContent =
    analysis.match_score === "—" ? "—" : `${analysis.match_score}%`;
  if (analysis.precision != null) {
    document.getElementById("scorePrecision").textContent =
      `${Math.round(analysis.precision * 100)}%`;
  }
  if (analysis.recall != null) {
    document.getElementById("scoreRecall").textContent =
      `${Math.round(analysis.recall * 100)}%`;
  }

  list.innerHTML = "";
  const issues = analysis.issues || [];
  if (issues.length === 0) {
    const li = document.createElement("li");
    li.style.borderColor = "#22c55e";
    li.textContent = t("no_issues");
    list.appendChild(li);
  } else {
    issues.forEach((issue) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${issue.section}:</strong> ${issue.message}<br><em>${issue.suggestion}</em>`;
      list.appendChild(li);
    });
  }
  syncExportButtons();
}

async function generate() {
  if (!currentUser) {
    openAuthModal("login");
    return;
  }
  const payload = getPayload();
  try {
    const gen = await api("/api/resume/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    const analysis = gen.analysis || await api("/api/resume/analyze", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    lastResult = { gen, analysis };
    renderResults();
    await loadSavedResumes();
  } catch (e) {
    if (e.status === 401) {
      logout();
      openAuthModal("login");
      return;
    }
    alert(e.message || t("generate_failed"));
  }
}

prevBtn.addEventListener("click", () => showStep(Math.max(1, currentStep - 1)));
nextBtn.addEventListener("click", () => showStep(Math.min(4, currentStep + 1)));
generateBtn.addEventListener("click", generate);
exportPdfBtn.addEventListener("click", () => exportResume("pdf"));
exportDocxBtn.addEventListener("click", () => exportResume("docx"));
steps.forEach((s) => s.addEventListener("click", () => showStep(Number(s.dataset.step))));
document.querySelectorAll(".lang-btn").forEach((b) =>
  b.addEventListener("click", () => setLang(b.dataset.lang))
);

loginOpenBtn.addEventListener("click", () => openAuthModal("login"));
registerOpenBtn.addEventListener("click", () => openAuthModal("register"));
logoutBtn.addEventListener("click", logout);
document.getElementById("authCancelBtn").addEventListener("click", closeAuthModal);
document.getElementById("authModalBackdrop").addEventListener("click", closeAuthModal);
authForm.addEventListener("submit", handleAuthSubmit);

showStep(1);
applyLang();
refreshSession();
