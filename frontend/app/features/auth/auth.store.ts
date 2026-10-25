import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { readToken, writeToken } from '~/shared/utils/token'
import type { UserOut } from '~/shared/schemas/auth'
import { fetchCurrentUser, loginUser, registerUser } from './auth.api'

export type AuthMode = 'login' | 'register'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserOut | null>(null)
  const token = ref<string | null>(null)
  const ready = ref(false)
  const pending = ref(false)
  const modalOpen = ref(false)
  const authMode = ref<AuthMode>('login')
  const authError = ref<string | null>(null)

  const isAuthenticated = computed(() => Boolean(user.value && token.value))
  const displayName = computed(() => user.value?.full_name || user.value?.email || '')

  function openModal(mode: AuthMode = 'login') {
    authMode.value = mode
    authError.value = null
    modalOpen.value = true
  }

  function closeModal() {
    modalOpen.value = false
    authError.value = null
  }

  async function refreshSession(): Promise<void> {
    const existing = readToken()
    token.value = existing
    if (!existing) {
      user.value = null
      ready.value = true
      return
    }
    try {
      user.value = await fetchCurrentUser()
    } catch {
      writeToken(null)
      token.value = null
      user.value = null
    } finally {
      ready.value = true
    }
  }

  async function submitAuth(input: {
    email: string
    password: string
    full_name?: string
  }): Promise<boolean> {
    pending.value = true
    authError.value = null
    try {
      const result = authMode.value === 'register'
        ? await registerUser({
            email: input.email,
            password: input.password,
            full_name: input.full_name || ''
          })
        : await loginUser({
            email: input.email,
            password: input.password
          })
      writeToken(result.access_token)
      token.value = result.access_token
      user.value = await fetchCurrentUser()
      closeModal()
      return true
    } catch (error) {
      authError.value = error instanceof Error ? error.message : 'Authentication failed'
      return false
    } finally {
      pending.value = false
    }
  }

  function logout() {
    writeToken(null)
    token.value = null
    user.value = null
  }

  function requireAuth(): boolean {
    if (isAuthenticated.value) return true
    openModal('login')
    return false
  }

  return {
    user,
    token,
    ready,
    pending,
    modalOpen,
    authMode,
    authError,
    isAuthenticated,
    displayName,
    openModal,
    closeModal,
    refreshSession,
    submitAuth,
    logout,
    requireAuth
  }
})
