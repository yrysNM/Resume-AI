import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import { exportResume } from '../resume.api'
import { useResumeResult } from './useResumeResult'
import { useResumeWizard } from './useResumeWizard'

export function useResumeExport() {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()
  const { result, hasExportable } = useResumeResult()
  const { form } = useResumeWizard()

  const pending = ref(false)

  async function exportFormat(format: 'pdf' | 'docx'): Promise<void> {
    const id = result.value?.gen?.id
    if (!id) return
    if (!auth.requireAuth()) return

    pending.value = true
    try {
      await exportResume(id, format, form.value.template)
    } catch (err) {
      if (isAppError(err) && err.status === 401) {
        auth.logout()
        auth.openModal('login')
        return
      }
      const message = err instanceof Error ? err.message : t('export_failed')
      toast.add({
        title: t('export_failed'),
        description: message,
        color: 'error'
      })
    } finally {
      pending.value = false
    }
  }

  return {
    pending,
    hasExportable,
    exportFormat
  }
}
