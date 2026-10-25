import { useAuthStore } from '~/features/auth/auth.store'

/**
 * Optional route guard. Home stays public; generate/export gate via useAuth.requireAuth.
 */
export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()
  if (!auth.ready) return
  if (!auth.isAuthenticated) {
    auth.openModal('login')
    return abortNavigation()
  }
})
