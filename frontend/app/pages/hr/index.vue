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
    <HhVacancyMarket
      default-category="hr"
      cache-key="hh-hr-vacancies"
    />
    <DashboardView :heading="false" />
  </main>
</template>
