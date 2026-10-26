import { useAuth } from '~/features/auth/composables/useAuth'
import { fetchDashboard } from '../dashboard.api'

export function useDashboard() {
  const auth = useAuth()

  const {
    data: stats,
    pending,
    error,
    refresh
  } = useAsyncData(
    'dashboard-stats',
    async () => {
      if (!auth.isAuthenticated.value) return null
      return fetchDashboard()
    },
    {
      default: () => null,
      watch: [() => auth.isAuthenticated.value, () => auth.isHr.value]
    }
  )

  return {
    stats,
    pending,
    error,
    refresh
  }
}
