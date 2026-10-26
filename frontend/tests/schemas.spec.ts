import { describe, expect, it } from 'vitest'
import {
  personalInfoSchema,
  resumeRequestSchema,
  generateResponseSchema,
  analysisResponseSchema
} from '../app/shared/schemas/resume'
import {
  userLoginSchema,
  userRegisterSchema,
  tokenResponseSchema,
  userOutSchema
} from '../app/shared/schemas/auth'
import {
  companyOutSchema,
  vacancyOutSchema,
  hrApplicationSchema
} from '../app/shared/schemas/hr'
import { jobOutSchema, seekerApplicationSchema } from '../app/shared/schemas/jobs'
import { dashboardOutSchema } from '../app/shared/schemas/dashboard'
import { formatMatchScore } from '../app/shared/utils/score'
import { applicantName } from '../app/features/hr/lib/applicantName'

describe('auth schemas', () => {
  it('parses login payload', () => {
    const parsed = userLoginSchema.parse({
      email: 'test@mail.kz',
      password: 'password1'
    })
    expect(parsed.email).toBe('test@mail.kz')
  })

  it('rejects short register password', () => {
    expect(() =>
      userRegisterSchema.parse({
        email: 'test@mail.kz',
        password: 'short',
        full_name: 'Test'
      })
    ).toThrow()
  })

  it('defaults register role to seeker', () => {
    const parsed = userRegisterSchema.parse({
      email: 'test@mail.kz',
      password: 'password1',
      full_name: 'Test'
    })
    expect(parsed.role).toBe('seeker')
  })

  it('accepts hr role on register', () => {
    const parsed = userRegisterSchema.parse({
      email: 'hr@mail.kz',
      password: 'password1',
      full_name: 'HR',
      role: 'hr'
    })
    expect(parsed.role).toBe('hr')
  })

  it('parses token and user responses', () => {
    const token = tokenResponseSchema.parse({
      access_token: 'abc',
      token_type: 'bearer'
    })
    expect(token.access_token).toBe('abc')

    const user = userOutSchema.parse({
      id: 1,
      email: 'test@mail.kz',
      full_name: 'Test User',
      role: 'hr',
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(user.id).toBe(1)
    expect(user.role).toBe('hr')
  })

  it('defaults missing user role to seeker', () => {
    const user = userOutSchema.parse({
      id: 1,
      email: 'test@mail.kz',
      full_name: 'Test User',
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(user.role).toBe('seeker')
  })
})

describe('resume schemas', () => {
  it('parses a resume request', () => {
    const parsed = resumeRequestSchema.parse({
      personal: {
        full_name: 'Test User',
        email: 'test@mail.kz',
        phone: '+7 777',
        position: 'Dev'
      },
      skills: ['React'],
      experience: [],
      education: 'Uni',
      target_job: 'frontend'
    })
    expect(parsed.skills).toEqual(['React'])
    expect(parsed.language).toBe('kk')
    expect(parsed.template).toBe('classic')
    expect(personalInfoSchema.parse(parsed.personal).full_name).toBe('Test User')
  })

  it('parses generate + analysis responses', () => {
    const analysis = analysisResponseSchema.parse({
      completeness_score: 80,
      match_score: 70,
      precision: 0.9,
      recall: 0.8,
      issues: [],
      keywords_found: ['react'],
      keywords_missing: ['vue']
    })
    expect(analysis.completeness_score).toBe(80)

    const gen = generateResponseSchema.parse({
      id: 42,
      resume_text: 'Hello',
      generated_by: 'groq',
      analysis
    })
    expect(gen.id).toBe(42)
  })
})

describe('hr jobs dashboard schemas', () => {
  it('parses company and vacancy', () => {
    const company = companyOutSchema.parse({
      id: 1,
      user_id: 4,
      name: 'Acme',
      description: 'Studio',
      website: null,
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(company.name).toBe('Acme')
    expect(company.created_at).toBe('2026-01-01T00:00:00Z')

    const vacancy = vacancyOutSchema.parse({
      id: 9,
      company_id: 1,
      title: 'Frontend',
      description: 'Vue',
      status: 'open',
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(vacancy.status).toBe('open')
    expect(vacancy.company_id).toBe(1)
  })

  it('parses HR application with nullable resume_id', () => {
    const application = hrApplicationSchema.parse({
      id: 3,
      vacancy_id: 9,
      seeker_id: 2,
      resume_id: null,
      resume_text: 'Test User\nSkills',
      match_score: 0.8,
      ranked_by: 'heuristic-keywords',
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(application.resume_id).toBeNull()
    expect(application.match_score).toBe(0.8)
  })

  it('parses JobOut with company_id and company_name', () => {
    const job = jobOutSchema.parse({
      id: 9,
      title: 'Frontend',
      description: 'Vue',
      company_id: 1,
      company_name: 'Acme'
    })
    expect(job.company_id).toBe(1)
    expect(job.company_name).toBe('Acme')
  })

  it('parses seeker application and role-discriminated dashboards', () => {
    const application = seekerApplicationSchema.parse({
      id: 1,
      vacancy_id: 9,
      vacancy_title: 'Frontend',
      resume_id: 4,
      match_score: 0.5,
      ranked_by: 'heuristic-keywords',
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(application.vacancy_title).toBe('Frontend')
    expect(application.resume_id).toBe(4)

    const hrDash = dashboardOutSchema.parse({
      role: 'hr',
      companies: 2,
      open_vacancies: 3,
      applications: 10,
      average_match_score: 72
    })
    expect(hrDash.role).toBe('hr')
    if (hrDash.role === 'hr') {
      expect(hrDash.average_match_score).toBe(72)
    }

    const seekerDash = dashboardOutSchema.parse({
      role: 'seeker',
      saved_resumes: 1,
      applications_sent: 4,
      best_match_score: 0.91,
      open_jobs: 8
    })
    expect(seekerDash.role).toBe('seeker')
    if (seekerDash.role === 'seeker') {
      expect(seekerDash.open_jobs).toBe(8)
      expect(seekerDash.best_match_score).toBe(0.91)
    }
  })

  it('formats match scores as percents', () => {
    expect(formatMatchScore(null)).toBe('—')
    expect(formatMatchScore(0.8)).toBe('80%')
    expect(formatMatchScore(72)).toBe('72%')
  })

  it('reads applicant name from resume_text snapshot', () => {
    expect(applicantName(hrApplicationSchema.parse({
      id: 3,
      vacancy_id: 9,
      seeker_id: 2,
      resume_id: null,
      resume_text: 'Test User\nSkills',
      match_score: 0.8,
      ranked_by: 'heuristic-keywords',
      created_at: '2026-01-01T00:00:00Z'
    }))).toBe('Test User')
  })
})
