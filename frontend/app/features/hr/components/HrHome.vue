<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <h1 class="mb-2 text-3xl font-bold text-slate-100">
      {{ t('hr_title') }}
    </h1>
    <p class="mb-6 text-slate-400">
      {{ t('hr_subtitle') }}
    </p>
    <div class="flex flex-wrap gap-3">
      <UButton
        to="/hr/companies"
        color="primary"
        :label="t('hr_manage_companies')"
      />
      <UButton
        to="/dashboard"
        color="neutral"
        variant="subtle"
        :label="t('hr_view_dashboard')"
      />
    </div>
  </section>
</template>
