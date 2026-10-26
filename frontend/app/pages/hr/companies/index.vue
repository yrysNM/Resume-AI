<script setup lang="ts">
import { CompanyBoard } from '~/features/hr'

const { t } = useI18n()

useSeoMeta({
  title: () => t('companies_title')
})
</script>

<template>
  <main>
    <CompanyBoard />
  </main>
</template>
