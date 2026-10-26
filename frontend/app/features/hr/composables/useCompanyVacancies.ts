import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import type { VacancyCreate, VacancyUpdate } from '~/shared/schemas/hr'
import {
  createVacancy,
  deleteVacancy,
  getCompany,
  listVacancies,
  updateVacancy
} from '../hr.api'

export function useCompanyVacancies(companyId: Ref<number>) {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()

  const {
    data: company,
    pending: companyPending,
    error: companyError,
    refresh: refreshCompany
  } = useAsyncData(
    () => `hr-company-${companyId.value}`,
    async () => {
      if (!auth.isAuthenticated.value || !auth.isHr.value || !Number.isFinite(companyId.value)) {
        return null
      }
      return getCompany(companyId.value)
    },
    {
      default: () => null,
      watch: [companyId, () => auth.isAuthenticated.value, () => auth.isHr.value]
    }
  )

  const {
    data: items,
    pending,
    error,
    refresh
  } = useAsyncData(
    () => `hr-vacancies-${companyId.value}`,
    async () => {
      if (!auth.isAuthenticated.value || !auth.isHr.value || !Number.isFinite(companyId.value)) {
        return []
      }
      return listVacancies(companyId.value)
    },
    {
      default: () => [],
      watch: [companyId, () => auth.isAuthenticated.value, () => auth.isHr.value]
    }
  )

  function notifyError(err: unknown, fallbackKey: string): void {
    if (isAppError(err) && err.status === 401) {
      auth.logout()
      auth.openModal('login')
      return
    }
    const message = err instanceof Error ? err.message : t(fallbackKey)
    toast.add({
      title: t(fallbackKey),
      description: message,
      color: 'error'
    })
  }

  async function create(payload: VacancyCreate): Promise<boolean> {
    try {
      await createVacancy(companyId.value, payload)
      await refresh()
      return true
    } catch (err) {
      notifyError(err, 'save_failed')
      return false
    }
  }

  async function update(vacancyId: number, payload: VacancyUpdate): Promise<boolean> {
    try {
      await updateVacancy(companyId.value, vacancyId, payload)
      await refresh()
      return true
    } catch (err) {
      notifyError(err, 'save_failed')
      return false
    }
  }

  async function remove(vacancyId: number): Promise<boolean> {
    try {
      await deleteVacancy(companyId.value, vacancyId)
      await refresh()
      return true
    } catch (err) {
      notifyError(err, 'delete_failed')
      return false
    }
  }

  return {
    company,
    companyPending,
    companyError,
    refreshCompany,
    items,
    pending,
    error,
    refresh,
    create,
    update,
    remove
  }
}
