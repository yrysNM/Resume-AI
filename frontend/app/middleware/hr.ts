import { useAuthStore } from '~/features/auth/auth.store'

/** HR-only guard. Non-HR users are sent home. */
export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()
  if (!auth.ready) return
  if (!auth.isHr) {
    return navigateTo('/')
  }
})
