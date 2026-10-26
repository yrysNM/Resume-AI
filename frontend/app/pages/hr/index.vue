<script setup lang="ts">
import { DashboardView } from '~/features/dashboard'
import { HrHome } from '~/features/hr'

const { t } = useI18n()

useSeoMeta({
  title: () => t('hr_title')
})
</script>

<template>
  <main class="flex flex-col gap-6">
    <HrHome />
    <DashboardView :heading="false" />
  </main>
</template>
