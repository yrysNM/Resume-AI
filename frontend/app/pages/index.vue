<script setup lang="ts">
import ResumeWizard from '~/features/resume/components/ResumeWizard.vue'
import SavedList from '~/features/library/components/SavedList.vue'
import { useAuth } from '~/features/auth/composables/useAuth'
import { useResumeLibrary } from '~/features/library/composables/useResumeLibrary'

definePageMeta({
  layout: 'default'
})

const { t } = useI18n()
const { isAuthenticated, isHr, ready } = useAuth()
const { refresh } = useResumeLibrary()

watch(
  [ready, isAuthenticated, isHr],
  ([isReady, authed, hr]) => {
    if (isReady && authed && hr) {
      void navigateTo('/hr')
    }
  },
  { immediate: true }
)

useSeoMeta({
  title: () => t('doc_title'),
  description: () => t('subtitle'),
  ogTitle: () => t('doc_title'),
  ogDescription: () => t('subtitle')
})
</script>

<template>
  <main class="grid grid-cols-1 gap-6 lg:grid-cols-[220px_1fr]">
    <aside class="h-fit rounded-2xl border border-white/10 bg-white/5 p-6">
      <WizardSteps />
      <SavedList />
    </aside>

    <ResumeWizard @generated="refresh">
      <template #auth-hint>
        <p
          v-if="!isAuthenticated"
          class="mb-5 rounded-[10px] border border-amber-500/35 bg-amber-500/12 px-3.5 py-2.5 text-sm text-amber-400"
          role="status"
        >
          {{ t('auth_required') }}
        </p>
      </template>
    </ResumeWizard>
  </main>
</template>
