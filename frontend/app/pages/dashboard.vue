<script setup lang="ts">
import { DashboardView } from '~/features/dashboard'

definePageMeta({
  middleware: 'auth',
  layout: 'default'
})

const { t } = useI18n()

useSeoMeta({
  title: () => t('dashboard_title')
})
</script>

<template>
  <main>
    <DashboardView />
  </main>
</template>
