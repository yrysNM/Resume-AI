import { isAppError } from '~/shared/types/errors'
import { useAuth } from '~/features/auth/composables/useAuth'
import type { CompanyCreate, CompanyUpdate } from '~/shared/schemas/hr'
import {
  createCompany,
  deleteCompany,
  listCompanies,
  updateCompany
} from '../hr.api'

export function useCompanies() {
  const { t } = useI18n()
  const toast = useToast()
  const auth = useAuth()

  const {
    data: items,
    pending,
    error,
    refresh
  } = useAsyncData(
    'hr-companies',
    async () => {
      if (!auth.isAuthenticated.value || !auth.isHr.value) return []
      return listCompanies()
    },
    {
      default: () => [],
      watch: [() => auth.isAuthenticated.value, () => auth.isHr.value]
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

  async function create(payload: CompanyCreate): Promise<boolean> {
    try {
      await createCompany(payload)
      await refresh()
      return true
    } catch (err) {
      notifyError(err, 'save_failed')
      return false
    }
  }

  async function update(id: number, payload: CompanyUpdate): Promise<boolean> {
    try {
      await updateCompany(id, payload)
      await refresh()
      return true
    } catch (err) {
      notifyError(err, 'save_failed')
      return false
    }
  }

  async function remove(id: number): Promise<boolean> {
    try {
      await deleteCompany(id)
      await refresh()
      return true
    } catch (err) {
      notifyError(err, 'delete_failed')
      return false
    }
  }

  return {
    items,
    pending,
    error,
    refresh,
    create,
    update,
    remove
  }
}
