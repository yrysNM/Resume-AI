<script setup lang="ts">
import { useResumeWizard } from '~/features/resume/composables/useResumeWizard'

const { t } = useI18n()
const { step, progress, showStep } = useResumeWizard()

const steps = computed(() => [
  { n: 1, label: t('step1') },
  { n: 2, label: t('step2') },
  { n: 3, label: t('step3') },
  { n: 4, label: t('step4') }
])
</script>

<template>
  <div>
    <h2 class="mb-4 text-xs font-semibold tracking-wide text-slate-500 uppercase">
      {{ t('steps_title') }}
    </h2>
    <ol class="list-none">
      <li
        v-for="item in steps"
        :key="item.n"
      >
        <button
          type="button"
          class="mb-2 w-full rounded-[10px] px-4 py-3 text-left text-sm transition"
          :class="step === item.n
            ? 'bg-sky-500 font-semibold text-white'
            : 'text-slate-500 hover:bg-white/5 hover:text-slate-300'"
          @click="showStep(item.n)"
        >
          {{ item.label }}
        </button>
      </li>
    </ol>
    <div class="mt-6 h-1 overflow-hidden rounded-sm bg-slate-700">
      <div
        class="h-full bg-sky-400 transition-[width] duration-300"
        :style="{ width: progress }"
      />
    </div>
  </div>
</template>
