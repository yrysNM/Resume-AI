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
      created_at: '2026-01-01T00:00:00Z'
    })
    expect(user.id).toBe(1)
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
