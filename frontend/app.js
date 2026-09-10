const API = "http://127.0.0.1:8000";
let currentStep = 1;

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
  document.getElementById("scoreComplete").textContent = `${analysis.completeness_score}%`;
  document.getElementById("scoreMatch").textContent = `${analysis.match_score}%`;

  const list = document.getElementById("issuesList");
  list.innerHTML = "";
  if (analysis.issues.length === 0) {
    list.innerHTML = "<li style='border-color:#22c55e'>Түйіндеме жақсы сапада — ескерту жоқ</li>";
  } else {
    analysis.issues.forEach((issue) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${issue.section}:</strong> ${issue.message}<br><em>${issue.suggestion}</em>`;
      list.appendChild(li);
    });
  }
}

prevBtn.addEventListener("click", () => showStep(Math.max(1, currentStep - 1)));
nextBtn.addEventListener("click", () => showStep(Math.min(4, currentStep + 1)));
generateBtn.addEventListener("click", generate);
steps.forEach((s) => s.addEventListener("click", () => showStep(Number(s.dataset.step))));

showStep(1);
