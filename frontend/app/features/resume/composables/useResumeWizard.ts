import { computed } from 'vue'
import type { ExperienceItem, ResumeRequest } from '~/shared/schemas/resume'

export const WIZARD_STEPS = 4 as const

const DEFAULT_EXPERIENCE: ExperienceItem = {
  company: 'Tech Solutions KZ',
  role: 'Junior Frontend Developer',
  period: '2024 — present',
  description:
    'Built web interfaces with React, TypeScript, and REST APIs. Reduced delivery time by 30% through reusable UI components.'
}

export function useResumeWizard() {
  const step = useState<number>('resume-wizard-step', () => 1)

  const form = useState('resume-wizard-form', () => ({
    full_name: 'Test User',
    email: 'test@mail.kz',
    phone: '+7 777 123 4567',
    position: 'Test Position',
    target_job: 'frontend developer',
    education: 'Test Education',
    skillsText: 'React, TypeScript, JavaScript, HTML, CSS, REST API',
    experience: [{ ...DEFAULT_EXPERIENCE }] as ExperienceItem[]
  }))

  const progress = computed(() => `${step.value * 25}%`)

  function showStep(n: number) {
    step.value = Math.min(WIZARD_STEPS, Math.max(1, n))
  }

  function next() {
    showStep(step.value + 1)
  }

  function prev() {
    showStep(step.value - 1)
  }

  function addExperience(values: Partial<ExperienceItem> = {}) {
    form.value.experience.push({
      company: values.company || '',
      role: values.role || '',
      period: values.period || '',
      description: values.description || ''
    })
  }

  function removeExperience(index: number) {
    if (form.value.experience.length <= 1) {
      form.value.experience[0] = {
        company: '',
        role: '',
        period: '',
        description: ''
      }
      return
    }
    form.value.experience.splice(index, 1)
  }

  const skillTags = computed(() =>
    form.value.skillsText
      .split(',')
      .map(s => s.trim())
      .filter(Boolean)
  )

  function getPayload(): ResumeRequest {
    const skills = skillTags.value
    const experience = form.value.experience
      .map(item => ({
        company: item.company.trim(),
        role: item.role.trim(),
        period: item.period.trim(),
        description: item.description.trim()
      }))
      .filter(item => item.company || item.role || item.period || item.description)

    return {
      personal: {
        full_name: form.value.full_name.trim(),
        email: form.value.email.trim(),
        phone: form.value.phone.trim(),
        position: form.value.position.trim()
      },
      skills,
      experience,
      education: form.value.education.trim(),
      target_job: form.value.target_job.trim()
    }
  }

  return {
    step,
    form,
    progress,
    skillTags,
    showStep,
    next,
    prev,
    addExperience,
    removeExperience,
    getPayload
  }
}
