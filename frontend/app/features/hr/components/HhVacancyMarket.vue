<script setup lang="ts">
import type { HhVacancyOut } from '~/shared/schemas/hh'
import { useHhVacancies } from '../composables/useHhVacancies'

const { t } = useI18n()
const {
  list,
  pending,
  error,
  refresh,
  canPrev,
  canNext,
  prevPage,
  nextPage
} = useHhVacancies()

function salaryAmount(item: HhVacancyOut): string | null {
  if (item.salary_from == null && item.salary_to == null) return null
  const currency = item.salary_currency?.trim() ?? ''
  let amount: string
  if (item.salary_from != null && item.salary_to != null) {
    amount = `${item.salary_from} – ${item.salary_to}`
  } else if (item.salary_from != null) {
    amount = `${item.salary_from}+`
  } else {
    amount = String(item.salary_to)
  }
  return currency ? `${amount} ${currency}` : amount
}

function metaLine(item: HhVacancyOut): string {
  return [item.experience, item.schedule]
    .filter((value): value is string => Boolean(value))
    .join(' · ')
}

const cards = computed(() =>
  (list.value?.items ?? []).map(item => ({
    item,
    salaryAmount: salaryAmount(item),
    meta: metaLine(item)
  }))
)
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <h2 class="mb-2 text-2xl font-bold text-slate-100">
      {{ t('hh_title') }}
    </h2>
    <p class="mb-2 text-slate-400">
      {{ t('hh_subtitle') }}
    </p>
    <p class="mb-7 text-sm text-slate-500">
      {{ t('hh_source') }}
    </p>

    <p
      v-if="pending"
      class="text-sm text-slate-500"
    >
      {{ t('hh_loading') }}
    </p>
    <div
      v-else-if="error"
      class="flex flex-col gap-3"
    >
      <UAlert
        color="error"
        variant="subtle"
        :title="t('hh_error')"
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
      v-else-if="!cards.length"
      class="text-sm text-slate-500"
    >
      {{ t('hh_empty') }}
    </p>
    <ul
      v-else
      class="flex list-none flex-col gap-3"
    >
      <li
        v-for="card in cards"
        :key="card.item.id"
        class="flex flex-col gap-3 rounded-2xl border border-white/10 bg-slate-950/40 p-4 sm:flex-row sm:items-start sm:justify-between"
      >
        <div>
          <p class="font-semibold text-slate-100">
            {{ card.item.title }}
          </p>
          <p class="mt-1 text-sm text-sky-400">
            {{ card.item.employer_name }}
          </p>
          <p
            v-if="card.item.area_name"
            class="mt-1 text-sm text-slate-400"
          >
            {{ card.item.area_name }}
          </p>
          <p
            v-if="card.salaryAmount"
            class="mt-2 text-sm text-slate-300"
          >
            {{ t('hh_salary', { amount: card.salaryAmount }) }}
          </p>
          <p
            v-if="card.item.requirement"
            class="mt-2 text-sm text-slate-400"
          >
            {{ card.item.requirement }}
          </p>
          <p
            v-if="card.item.responsibility"
            class="mt-2 text-sm text-slate-400"
          >
            {{ card.item.responsibility }}
          </p>
          <p
            v-if="card.meta"
            class="mt-2 text-xs tracking-wide text-slate-500 uppercase"
          >
            {{ card.meta }}
          </p>
        </div>
        <UButton
          :to="card.item.url"
          target="_blank"
          rel="noopener noreferrer"
          external
          color="primary"
          variant="subtle"
          size="sm"
          class="shrink-0"
          :label="t('hh_open')"
        />
      </li>
    </ul>

    <div
      v-if="!pending && !error"
      class="mt-6 flex flex-wrap items-center justify-between gap-3"
    >
      <p class="text-sm text-slate-500">
        {{ t('hh_found', { count: list?.found ?? 0 }) }}
      </p>
      <div class="flex gap-2">
        <UButton
          color="neutral"
          variant="subtle"
          size="sm"
          :label="t('hh_prev')"
          :disabled="!canPrev"
          @click="prevPage"
        />
        <UButton
          color="neutral"
          variant="subtle"
          size="sm"
          :label="t('hh_next')"
          :disabled="!canNext"
          @click="nextPage"
        />
      </div>
    </div>
  </section>
</template>
