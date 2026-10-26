import { useAuthStore } from '~/features/auth/auth.store'

/**
 * Route guard for authenticated pages. Home stays public.
 */
export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  if (!auth.ready) return
  if (!auth.isAuthenticated) {
    auth.openModal('login')
    if (to.path !== '/') return navigateTo('/')
    return abortNavigation()
  }
})
