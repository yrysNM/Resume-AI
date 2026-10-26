<script setup lang="ts">
import { VacancyApplicants } from '~/features/hr'

const { t } = useI18n()
const route = useRoute()

const vacancyId = computed(() => {
  const raw = route.params.id
  const value = Array.isArray(raw) ? raw[0] : raw
  return Number(value)
})

useSeoMeta({
  title: () => t('applicants_title')
})
</script>

<template>
  <main>
    <VacancyApplicants
      v-if="Number.isFinite(vacancyId) && vacancyId > 0"
      :vacancy-id="vacancyId"
    />
    <UAlert
      v-else
      color="error"
      variant="subtle"
      :title="t('vacancy_not_found')"
    />
  </main>
</template>
