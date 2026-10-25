import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import { analyzeResume, generateResume } from '../resume.api'
import { useResumeResult } from './useResumeResult'
import { useResumeWizard } from './useResumeWizard'

export function useResumeGenerate(onSuccess?: () => void | Promise<void>) {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()
  const { getPayload } = useResumeWizard()
  const { setResult, clearResult } = useResumeResult()

  const pending = ref(false)
  const error = ref<string | null>(null)

  async function generate(): Promise<boolean> {
    if (!auth.requireAuth()) return false

    pending.value = true
    error.value = null
    try {
      const payload = getPayload()
      const gen = await generateResume(payload)
      const analysis = gen.analysis ?? await analyzeResume(payload)
      setResult({
        gen: {
          id: gen.id,
          resume_text: gen.resume_text,
          generated_by: gen.generated_by,
          format: gen.format
        },
        analysis
      })
      await onSuccess?.()
      return true
    } catch (err) {
      if (isAppError(err) && err.status === 401) {
        auth.logout()
        clearResult()
        auth.openModal('login')
        return false
      }
      const message = err instanceof Error ? err.message : t('generate_failed')
      error.value = message
      toast.add({
        title: t('generate_failed'),
        description: message,
        color: 'error'
      })
      return false
    } finally {
      pending.value = false
    }
  }

  return {
    pending,
    error,
    generate
  }
}
