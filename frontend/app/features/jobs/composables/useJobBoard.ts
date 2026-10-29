import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import { applyToJob, listJobs, listMyApplications } from '../jobs.api'

export function useJobBoard() {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()
  const applying = ref(false)
  const searchInput = ref('')
  const searchQuery = ref('')
  let debounceTimer: ReturnType<typeof setTimeout> | null = null

  const {
    data: jobs,
    pending,
    error,
    refresh
  } = useAsyncData(
    'open-jobs',
    async () => {
      if (!auth.isAuthenticated.value || auth.isHr.value) return []
      return listJobs(searchQuery.value)
    },
    {
      default: () => [],
      watch: [
        searchQuery,
        () => auth.isAuthenticated.value,
        () => auth.isHr.value
      ]
    }
  )

  const {
    data: applications,
    pending: applicationsPending,
    refresh: refreshApplications
  } = useAsyncData(
    'seeker-applications',
    async () => {
      if (!auth.isAuthenticated.value || auth.isHr.value) return []
      return listMyApplications()
    },
    {
      default: () => [],
      watch: [() => auth.isAuthenticated.value, () => auth.isHr.value]
    }
  )

  const appliedVacancyIds = computed(() => {
    return new Set((applications.value || []).map(item => item.vacancy_id))
  })

  function applySearch(): void {
    const next = searchInput.value.trim()
    if (searchQuery.value === next) {
      void refresh()
      return
    }
    searchQuery.value = next
  }

  function onSearchInput(): void {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      applySearch()
    }, 350)
  }

  function clearSearch(): void {
    searchInput.value = ''
    if (searchQuery.value) searchQuery.value = ''
  }

  async function apply(jobId: number, resumeId: number): Promise<boolean> {
    applying.value = true
    try {
      await applyToJob(jobId, resumeId)
      await refreshApplications()
      toast.add({
        title: t('jobs_apply_success'),
        color: 'success'
      })
      return true
    } catch (err) {
      if (isAppError(err) && err.status === 401) {
        auth.logout()
        auth.openModal('login')
        return false
      }
      if (isAppError(err) && err.status === 409) {
        const closed = /closed/i.test(err.message)
        toast.add({
          title: closed ? t('jobs_vacancy_closed') : t('jobs_already_applied'),
          color: 'warning'
        })
        return false
      }
      const message = err instanceof Error ? err.message : t('jobs_apply_failed')
      toast.add({
        title: t('jobs_apply_failed'),
        description: message,
        color: 'error'
      })
      return false
    } finally {
      applying.value = false
    }
  }

  return {
    jobs,
    pending,
    error,
    refresh,
    applications,
    applicationsPending,
    refreshApplications,
    appliedVacancyIds,
    applying,
    apply,
    searchInput,
    applySearch,
    onSearchInput,
    clearSearch
  }
}
