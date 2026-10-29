<script setup lang="ts">
import { DashboardView } from '~/features/dashboard'
import { HhVacancyMarket, HrHome } from '~/features/hr'

const { t } = useI18n()

useSeoMeta({
  title: () => t('hr_title')
})
</script>

<template>
  <main class="flex flex-col gap-6">
    <HrHome />
    <HhVacancyMarket />
    <DashboardView :heading="false" />
  </main>
</template>
