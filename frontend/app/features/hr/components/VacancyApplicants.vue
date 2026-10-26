<script setup lang="ts">
import { formatMatchScore } from '~/shared/utils/score'
import { useVacancyApplications } from '../composables/useVacancyApplications'
import { applicantName } from '../lib/applicantName'

const props = defineProps<{
  vacancyId: number
}>()

const { t } = useI18n()
const vacancyId = computed(() => props.vacancyId)
const {
  vacancy,
  items,
  pending,
  error,
  refresh,
  ranking,
  rank
} = useVacancyApplications(vacancyId)

const backTo = computed(() => {
  const companyId = vacancy.value?.company_id
  return companyId ? `/hr/companies/${companyId}` : '/hr/companies'
})
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <UButton
      :to="backTo"
      color="neutral"
      variant="ghost"
      class="mb-3 px-0"
      :label="t('back')"
    />
    <div class="mb-6 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-slate-100">
          {{ vacancy?.title || t('applicants_title') }}
        </h1>
        <p class="mt-2 text-slate-400">
          {{ t('applicants_title') }}
        </p>
      </div>
      <UButton
        color="primary"
        :label="ranking ? t('applicants_ranking') : t('applicants_rank')"
        :loading="ranking"
        @click="rank()"
      />
    </div>

    <p
      v-if="pending"
      class="text-sm text-slate-500"
    >
      {{ t('applicants_loading') }}
    </p>
    <div
      v-else-if="error"
      class="flex flex-col gap-3"
    >
      <UAlert
        color="error"
        variant="subtle"
        :title="t('load_failed')"
      />
      <UButton
        color="neutral"
        variant="subtle"
        class="self-start"
        :label="t('retry')"
        @click="refresh()"
      />
    </div>
    <p
      v-else-if="!items?.length"
      class="text-sm text-slate-500"
    >
      {{ t('applicants_empty') }}
    </p>
    <ol
      v-else
      class="flex list-none flex-col gap-3"
    >
      <li
        v-for="(application, index) in items"
        :key="application.id"
        class="rounded-2xl border border-white/10 bg-slate-950/40 p-4"
      >
        <div class="flex flex-wrap items-baseline justify-between gap-2">
          <p class="font-semibold text-slate-100">
            {{ index + 1 }}. {{ applicantName(application) }}
          </p>
          <p class="text-lg font-bold text-sky-400">
            {{ formatMatchScore(application.match_score) }}
          </p>
        </div>
        <p class="mt-1 text-xs text-slate-500">
          {{ t('generated_by') }}: {{ application.ranked_by }}
        </p>
        <pre
          v-if="application.resume_text"
          class="mt-3 max-h-40 overflow-auto whitespace-pre-wrap text-xs text-slate-400"
        >{{ application.resume_text }}</pre>
      </li>
    </ol>
  </section>
</template>
