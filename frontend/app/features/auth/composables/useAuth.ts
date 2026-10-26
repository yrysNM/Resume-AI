import { useAuthStore } from '../auth.store'

export function useAuth() {
  const store = useAuthStore()

  return {
    user: computed(() => store.user),
    ready: computed(() => store.ready),
    pending: computed(() => store.pending),
    isAuthenticated: computed(() => store.isAuthenticated),
    displayName: computed(() => store.displayName),
    isHr: computed(() => store.isHr),
    isSeeker: computed(() => store.isSeeker),
    modalOpen: computed({
      get: () => store.modalOpen,
      set: (value: boolean) => {
        if (!value) store.closeModal()
        else store.openModal(store.authMode)
      }
    }),
    authMode: computed(() => store.authMode),
    authError: computed(() => store.authError),
    openModal: store.openModal,
    closeModal: store.closeModal,
    refreshSession: store.refreshSession,
    submitAuth: store.submitAuth,
    logout: store.logout,
    requireAuth: store.requireAuth
  }
}
