<script setup lang="ts">
import { CompanyVacancies } from '~/features/hr'

const { t } = useI18n()
const route = useRoute()

const companyId = computed(() => {
  const raw = route.params.id
  const value = Array.isArray(raw) ? raw[0] : raw
  return Number(value)
})

useSeoMeta({
  title: () => t('vacancies_title')
})
</script>

<template>
  <main>
    <CompanyVacancies
      v-if="Number.isFinite(companyId) && companyId > 0"
      :company-id="companyId"
    />
    <UAlert
      v-else
      color="error"
      variant="subtle"
      :title="t('company_not_found')"
    />
  </main>
</template>
