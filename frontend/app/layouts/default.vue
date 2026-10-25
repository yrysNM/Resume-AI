<script setup lang="ts">
import AuthBar from '~/features/auth/components/AuthBar.vue'
import LoginModal from '~/features/auth/components/LoginModal.vue'
import { useResumeResult } from '~/features/resume/composables/useResumeResult'
import { useResumeLibrary } from '~/features/library/composables/useResumeLibrary'

const { t, locale } = useI18n()
const { clearResult } = useResumeResult()
const { refresh } = useResumeLibrary()

useHead({
  htmlAttrs: {
    lang: locale
  }
})

watch(locale, (code) => {
  useHead({ htmlAttrs: { lang: code } })
})

async function onLogout() {
  clearResult()
  await refresh()
}
</script>

<template>
  <div class="mx-auto max-w-[1200px] px-6 py-6">
    <header class="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-white/5 px-6 py-4 backdrop-blur-md">
      <NuxtLink
        to="/"
        class="text-2xl font-bold text-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-400"
      >
        Resume<span class="text-sky-400">AI</span>
      </NuxtLink>

      <div class="flex flex-wrap items-center gap-6">
        <nav
          class="flex items-center gap-6 text-sm"
          aria-label="Primary"
        >
          <a
            href="#"
            class="font-semibold text-sky-400"
          >{{ t('nav_resume') }}</a>
          <a
            href="#analysis"
            class="text-slate-400 transition hover:text-slate-200"
          >{{ t('nav_analysis') }}</a>
          <a
            href="#saved"
            class="text-slate-400 transition hover:text-slate-200"
          >{{ t('nav_saved') }}</a>
        </nav>

        <LangSwitch />
        <AuthBar @logout="onLogout" />
      </div>
    </header>

    <slot />

    <LoginModal />
  </div>
</template>
