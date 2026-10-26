<script setup lang="ts">
import { formatMatchScore } from '~/shared/utils/score'
import { useDashboard } from '../composables/useDashboard'

const props = withDefaults(defineProps<{
  heading?: boolean
}>(), {
  heading: true
})

const { t } = useI18n()
const { stats, pending, error, refresh } = useDashboard()

const isHrDashboard = computed(() => stats.value?.role === 'hr')

const cards = computed(() => {
  const data = stats.value
  if (!data) return []
  if (data.role === 'hr') {
    return [
      { key: 'dash_companies' as const, value: formatCount(data.companies) },
      { key: 'dash_open_vacancies' as const, value: formatCount(data.open_vacancies) },
      { key: 'dash_applications' as const, value: formatCount(data.applications) },
      { key: 'dash_average_match' as const, value: formatMatchScore(data.average_match_score) }
    ]
  }
  return [
    { key: 'dash_saved_resumes' as const, value: formatCount(data.saved_resumes) },
    { key: 'dash_applications_sent' as const, value: formatCount(data.applications_sent) },
    { key: 'dash_best_match' as const, value: formatMatchScore(data.best_match_score) },
    { key: 'dash_open_jobs' as const, value: formatCount(data.open_jobs) }
  ]
})

function formatCount(value: number): string {
  return String(value)
}
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <h1
      v-if="props.heading"
      class="mb-2 text-3xl font-bold text-slate-100"
    >
      {{ t('dashboard_title') }}
    </h1>
    <h2
      v-else
      class="mb-2 text-lg font-semibold text-sky-400"
    >
      {{ t('dashboard_title') }}
    </h2>
    <p
      class="mb-7 text-slate-400"
      :class="{ 'sr-only': !props.heading }"
    >
      {{ isHrDashboard ? t('dashboard_hr_subtitle') : t('dashboard_seeker_subtitle') }}
    </p>

    <p
      v-if="pending"
      class="text-sm text-slate-500"
    >
      {{ t('dashboard_loading') }}
    </p>

    <div
      v-else-if="error"
      class="flex flex-col gap-3"
    >
      <UAlert
        color="error"
        variant="subtle"
        :title="t('dashboard_error')"
      />
      <UButton
        color="neutral"
        variant="subtle"
        class="self-start"
        :label="t('retry')"
        @click="refresh()"
      />
    </div>

    <div
      v-else
      class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4"
    >
      <article
        v-for="card in cards"
        :key="card.key"
        class="rounded-2xl border border-white/10 bg-slate-950/40 p-5"
      >
        <p class="text-sm text-slate-400">
          {{ t(card.key) }}
        </p>
        <p class="mt-2 text-3xl font-bold text-slate-100">
          {{ card.value }}
        </p>
      </article>
    </div>
  </section>
</template>
