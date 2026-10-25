import { describe, expect, it, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../app/features/auth/auth.store'
import { TOKEN_KEY } from '../app/shared/constants/auth'

vi.mock('../app/features/auth/auth.api', () => ({
  fetchCurrentUser: vi.fn(async () => ({
    id: 1,
    email: 'test@mail.kz',
    full_name: 'Test User',
    created_at: '2026-01-01T00:00:00Z'
  })),
  loginUser: vi.fn(async () => ({
    access_token: 'token-123',
    token_type: 'bearer'
  })),
  registerUser: vi.fn(async () => ({
    access_token: 'token-456',
    token_type: 'bearer'
  }))
}))

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.removeItem(TOKEN_KEY)
  })

  it('starts logged out', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBeNull()
  })

  it('opens login modal via requireAuth when logged out', () => {
    const store = useAuthStore()
    const ok = store.requireAuth()
    expect(ok).toBe(false)
    expect(store.modalOpen).toBe(true)
    expect(store.authMode).toBe('login')
  })

  it('logs in and exposes display name', async () => {
    const store = useAuthStore()
    store.openModal('login')
    const ok = await store.submitAuth({
      email: 'test@mail.kz',
      password: 'password1'
    })
    expect(ok).toBe(true)
    expect(store.isAuthenticated).toBe(true)
    expect(store.displayName).toBe('Test User')
    expect(localStorage.getItem(TOKEN_KEY)).toBe('token-123')
  })

  it('clears session on logout', async () => {
    const store = useAuthStore()
    await store.submitAuth({
      email: 'test@mail.kz',
      password: 'password1'
    })
    store.logout()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem(TOKEN_KEY)).toBeNull()
  })
})
