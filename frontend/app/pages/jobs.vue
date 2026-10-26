<script setup lang="ts">
import { JobBoard } from '~/features/jobs'
import { useAuth } from '~/features/auth/composables/useAuth'

definePageMeta({
  middleware: 'auth',
  layout: 'default'
})

const { t } = useI18n()
const { ready, isHr } = useAuth()

watch(
  [ready, isHr],
  ([isReady, hr]) => {
    if (isReady && hr) {
      void navigateTo('/hr')
    }
  },
  { immediate: true }
)

useSeoMeta({
  title: () => t('jobs_title')
})
</script>

<template>
  <main>
    <JobBoard />
  </main>
</template>
