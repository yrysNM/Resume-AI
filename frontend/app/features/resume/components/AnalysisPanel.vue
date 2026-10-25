<script setup lang="ts">
import { useResumeResult } from '../composables/useResumeResult'

const { t } = useI18n()
const { result } = useResumeResult()

function formatScore(value: number | string | undefined): string {
  if (value === undefined || value === null || value === '—') return '—'
  if (typeof value === 'string') return value
  return `${Math.round(value)}%`
}

function formatRatio(value: number | undefined): string {
  if (value === undefined || value === null) return '—'
  return `${Math.round(value * 100)}%`
}

const completeness = computed(() => formatScore(result.value?.analysis?.completeness_score))
const match = computed(() => formatScore(result.value?.analysis?.match_score))
const precision = computed(() => formatRatio(result.value?.analysis?.precision))
const recall = computed(() => formatRatio(result.value?.analysis?.recall))
const issues = computed(() => result.value?.analysis?.issues ?? [])
</script>

<template>
  <div class="flex min-h-70 flex-col rounded-xl border border-slate-700 bg-slate-950 p-5">
    <h4 class="mb-3 text-xs font-semibold tracking-wide text-slate-500 uppercase">
      {{ t('analysis_box') }}
    </h4>

    <div class="mb-4 grid grid-cols-2 gap-3">
      <div class="rounded-lg bg-slate-800 p-3.5 text-center">
        <span class="block text-2xl font-bold text-green-500">{{ completeness }}</span>
        <span class="text-xs text-slate-500">{{ t('completeness') }}</span>
      </div>
      <div class="rounded-lg bg-slate-800 p-3.5 text-center">
        <span class="block text-2xl font-bold text-green-500">{{ match }}</span>
        <span class="text-xs text-slate-500">{{ t('match') }}</span>
      </div>
      <div class="rounded-lg bg-slate-800 p-3.5 text-center">
        <span class="block text-2xl font-bold text-green-500">{{ precision }}</span>
        <span class="text-xs text-slate-500">{{ t('precision') }}</span>
      </div>
      <div class="rounded-lg bg-slate-800 p-3.5 text-center">
        <span class="block text-2xl font-bold text-green-500">{{ recall }}</span>
        <span class="text-xs text-slate-500">{{ t('recall') }}</span>
      </div>
    </div>

    <ul
      v-if="result"
      class="list-none space-y-2 text-sm"
    >
      <li
        v-if="issues.length === 0"
        class="rounded-lg border-l-3 border-green-500 bg-slate-800 p-2.5"
      >
        {{ t('no_issues') }}
      </li>
      <li
        v-for="(issue, index) in issues"
        :key="index"
        class="rounded-lg border-l-3 border-amber-500 bg-slate-800 p-2.5"
      >
        <strong>{{ issue.section }}:</strong> {{ issue.message }}
        <br>
        <em class="text-slate-400">{{ issue.suggestion }}</em>
      </li>
    </ul>
  </div>
</template>
