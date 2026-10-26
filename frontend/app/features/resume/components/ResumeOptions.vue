<script setup lang="ts">
import type { ResumeLanguage, ResumeTemplate } from '~/shared/schemas/resume'

defineProps<{
  language: ResumeLanguage
  template: ResumeTemplate
}>()

const emit = defineEmits<{
  'update:language': [value: ResumeLanguage]
  'update:template': [value: ResumeTemplate]
}>()

const { t } = useI18n()

const languages: Array<{ code: ResumeLanguage, label: string }> = [
  { code: 'kk', label: 'KK' },
  { code: 'ru', label: 'RU' },
  { code: 'en', label: 'EN' }
]

const templates = computed(() => [
  { id: 'classic' as const, label: t('template_classic') },
  { id: 'modern' as const, label: t('template_modern') },
  { id: 'minimal' as const, label: t('template_minimal') }
])
</script>

<template>
  <div class="mb-5 flex flex-col gap-4">
    <div>
      <p class="mb-2 text-xs font-semibold tracking-wide text-slate-500 uppercase">
        {{ t('gen_language') }}
      </p>
      <div
        class="inline-flex gap-0.5 rounded-[10px] border border-slate-700 bg-slate-950 p-0.5"
        role="radiogroup"
        :aria-label="t('gen_language')"
      >
        <button
          v-for="opt in languages"
          :key="opt.code"
          type="button"
          role="radio"
          class="rounded-md px-3 py-1.5 text-xs font-semibold transition"
          :class="language === opt.code
            ? 'bg-sky-500 text-white'
            : 'bg-transparent text-slate-400 hover:text-slate-100'"
          :aria-checked="language === opt.code"
          @click="emit('update:language', opt.code)"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div>
      <p class="mb-2 text-xs font-semibold tracking-wide text-slate-500 uppercase">
        {{ t('template_label') }}
      </p>
      <div
        class="grid grid-cols-3 gap-2"
        role="radiogroup"
        :aria-label="t('template_label')"
      >
        <button
          v-for="opt in templates"
          :key="opt.id"
          type="button"
          role="radio"
          class="rounded-xl border p-3 text-left transition"
          :class="template === opt.id
            ? 'border-sky-400 bg-sky-500/10'
            : 'border-slate-700 bg-slate-950 hover:border-slate-500'"
          :aria-checked="template === opt.id"
          @click="emit('update:template', opt.id)"
        >
          <span class="block text-xs font-semibold text-slate-100">
            {{ opt.label }}
          </span>
          <span
            class="mt-2 block h-8 overflow-hidden rounded"
            :class="{
              'bg-[#faf8f5] ring-1 ring-slate-600': opt.id === 'classic',
              'bg-sky-700': opt.id === 'modern',
              'bg-white/90': opt.id === 'minimal'
            }"
          >
            <span
              v-if="opt.id === 'classic'"
              class="mx-1 mt-1.5 block h-0.5 w-8 bg-slate-700"
            />
            <span
              v-else-if="opt.id === 'modern'"
              class="flex h-full"
            >
              <span class="w-1/3 bg-sky-900" />
              <span class="flex-1 bg-white/20" />
            </span>
            <span
              v-else
              class="mx-2 mt-3 block h-px bg-slate-400"
            />
          </span>
        </button>
      </div>
    </div>
  </div>
</template>
