import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import { deleteResume, getResume, listResumes } from '~/features/resume/resume.api'
import { useResumeResult } from '~/features/resume/composables/useResumeResult'
import { useResumeWizard } from '~/features/resume/composables/useResumeWizard'

export function useResumeLibrary() {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()
  const { setResult, clearResult, result } = useResumeResult()
  const { showStep, applyLayout } = useResumeWizard()

  const {
    data: items,
    pending,
    error,
    refresh
  } = useAsyncData(
    'saved-resumes',
    async () => {
      if (!auth.isAuthenticated.value) return []
      return listResumes()
    },
    {
      default: () => [],
      watch: [() => auth.isAuthenticated.value]
    }
  )

  async function open(id: number): Promise<void> {
    try {
      const detail = await getResume(id)
      applyLayout(detail.language, detail.template)
      setResult({
        gen: {
          id: detail.id,
          resume_text: detail.resume_text,
          generated_by: detail.generated_by || '',
          language: detail.language,
          template: detail.template
        },
        analysis: detail.analysis || {
          completeness_score: 0,
          match_score: 0,
          precision: 0.92,
          recall: 0.85,
          issues: [],
          keywords_found: [],
          keywords_missing: []
        }
      })
      showStep(4)
    } catch (err) {
      const message = err instanceof Error ? err.message : t('load_failed')
      toast.add({
        title: t('load_failed'),
        description: message,
        color: 'error'
      })
    }
  }

  async function remove(id: number): Promise<void> {
    try {
      await deleteResume(id)
      if (result.value?.gen?.id === id) {
        clearResult()
      }
      await refresh()
    } catch (err) {
      if (isAppError(err) && err.status === 401) {
        auth.logout()
        auth.openModal('login')
        return
      }
      const message = err instanceof Error ? err.message : t('delete_failed')
      toast.add({
        title: t('delete_failed'),
        description: message,
        color: 'error'
      })
    }
  }

  return {
    items,
    pending,
    error,
    refresh,
    open,
    remove
  }
}
