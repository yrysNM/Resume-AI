import { useAuthStore } from '~/features/auth/auth.store'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  await auth.refreshSession()
})
