import { describe, expect, it, beforeEach, vi } from 'vitest'
import { ref } from 'vue'

const state = new Map<string, ReturnType<typeof ref>>()

vi.stubGlobal('useState', <T>(key: string, init: () => T) => {
  if (!state.has(key)) {
    state.set(key, ref(init()) as ReturnType<typeof ref>)
  }
  return state.get(key)!
})

describe('useResumeWizard', () => {
  beforeEach(() => {
    state.clear()
  })

  it('moves between steps and clamps bounds', async () => {
    const { useResumeWizard } = await import('../app/features/resume/composables/useResumeWizard')
    const wizard = useResumeWizard()
    expect(wizard.step.value).toBe(1)
    expect(wizard.progress.value).toBe('25%')

    wizard.next()
    expect(wizard.step.value).toBe(2)

    wizard.showStep(99)
    expect(wizard.step.value).toBe(4)

    wizard.prev()
    expect(wizard.step.value).toBe(3)

    wizard.showStep(0)
    expect(wizard.step.value).toBe(1)
  })

  it('builds a resume payload from form state', async () => {
    const { useResumeWizard } = await import('../app/features/resume/composables/useResumeWizard')
    const wizard = useResumeWizard()
    const payload = wizard.getPayload()
    expect(payload.personal.email).toBe('test@mail.kz')
    expect(payload.skills).toContain('React')
    expect(payload.experience.length).toBeGreaterThan(0)
    expect(payload.language).toBe('kk')
    expect(payload.template).toBe('classic')
  })

  it('updates generation language and template', async () => {
    const { useResumeWizard } = await import('../app/features/resume/composables/useResumeWizard')
    const wizard = useResumeWizard()
    wizard.setLanguage('ru')
    wizard.setTemplate('modern')
    const payload = wizard.getPayload()
    expect(payload.language).toBe('ru')
    expect(payload.template).toBe('modern')
  })
})
