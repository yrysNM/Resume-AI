<script setup lang="ts">
const { locale, locales, setLocale, t } = useI18n()

type AppLocale = 'kk' | 'ru' | 'en'

const options = computed(() =>
  locales.value.map((item) => {
    const code = (typeof item === 'string' ? item : item.code) as AppLocale
    const name = typeof item === 'string' ? item : (item.name || item.code)
    return { code, name }
  })
)

function switchTo(code: AppLocale) {
  void setLocale(code)
}
</script>

<template>
  <div
    class="inline-flex gap-0.5 rounded-[10px] border border-slate-700 bg-slate-950 p-0.5"
    role="group"
    :aria-label="t('language')"
  >
    <button
      v-for="opt in options"
      :key="opt.code"
      type="button"
      class="rounded-md px-3 py-1.5 text-xs font-semibold transition"
      :class="locale === opt.code
        ? 'bg-sky-500 text-white'
        : 'bg-transparent text-slate-400 hover:text-slate-100'"
      :aria-pressed="locale === opt.code"
      @click="switchTo(opt.code)"
    >
      {{ opt.name }}
    </button>
  </div>
</template>
