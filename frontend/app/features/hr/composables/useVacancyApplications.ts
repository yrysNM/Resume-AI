import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import { getVacancy, listVacancyApplications, rankVacancyApplications } from '../hr.api'

export function useVacancyApplications(vacancyId: Ref<number>) {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()
  const ranking = ref(false)

  const {
    data: vacancy,
    pending: vacancyPending,
    refresh: refreshVacancy
  } = useAsyncData(
    () => `hr-vacancy-${vacancyId.value}`,
    async () => {
      if (!auth.isAuthenticated.value || !auth.isHr.value || !Number.isFinite(vacancyId.value)) {
        return null
      }
      return getVacancy(vacancyId.value)
    },
    {
      default: () => null,
      watch: [vacancyId, () => auth.isAuthenticated.value, () => auth.isHr.value]
    }
  )

  const {
    data: items,
    pending,
    error,
    refresh
  } = useAsyncData(
    () => `hr-applications-${vacancyId.value}`,
    async () => {
      if (!auth.isAuthenticated.value || !auth.isHr.value || !Number.isFinite(vacancyId.value)) {
        return []
      }
      return listVacancyApplications(vacancyId.value)
    },
    {
      default: () => [],
      watch: [vacancyId, () => auth.isAuthenticated.value, () => auth.isHr.value]
    }
  )

  async function rank(): Promise<void> {
    ranking.value = true
    try {
      await rankVacancyApplications(vacancyId.value)
      await refresh()
    } catch (err) {
      if (isAppError(err) && err.status === 401) {
        auth.logout()
        auth.openModal('login')
        return
      }
      const message = err instanceof Error ? err.message : t('rank_failed')
      toast.add({
        title: t('rank_failed'),
        description: message,
        color: 'error'
      })
    } finally {
      ranking.value = false
    }
  }

  return {
    vacancy,
    vacancyPending,
    refreshVacancy,
    items,
    pending,
    error,
    refresh,
    ranking,
    rank
  }
}
