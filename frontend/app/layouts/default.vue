<script setup lang="ts">
import AuthBar from '~/features/auth/components/AuthBar.vue'
import LoginModal from '~/features/auth/components/LoginModal.vue'
import { useAuth } from '~/features/auth/composables/useAuth'
import { useResumeResult } from '~/features/resume/composables/useResumeResult'
import { useResumeLibrary } from '~/features/library/composables/useResumeLibrary'

const { t, locale } = useI18n()
const { isHr } = useAuth()
const { clearResult } = useResumeResult()
const { refresh } = useResumeLibrary()
const route = useRoute()

useHead({
  htmlAttrs: {
    lang: locale
  }
})

watch(locale, (code) => {
  useHead({ htmlAttrs: { lang: code } })
})

const homeTo = computed(() => (isHr.value ? '/hr' : '/'))

const seekerLinks = computed(() => [
  { to: '/', label: t('nav_resume'), exact: true },
  { to: '/jobs', label: t('nav_jobs'), exact: false },
  { to: '/dashboard', label: t('nav_dashboard'), exact: false }
])

const hrLinks = computed(() => [
  { to: '/hr/companies', label: t('nav_companies'), exact: false },
  { to: '/dashboard', label: t('nav_dashboard'), exact: false }
])

const navLinks = computed(() => (isHr.value ? hrLinks.value : seekerLinks.value))

function linkActive(to: string, exact: boolean): boolean {
  if (exact) return route.path === to
  return route.path === to || route.path.startsWith(`${to}/`)
}

async function onLogout() {
  clearResult()
  await refresh()
  await navigateTo('/')
}
</script>

<template>
  <div class="mx-auto max-w-[1200px] px-6 py-6">
    <header class="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-white/5 px-6 py-4 backdrop-blur-md">
      <NuxtLink
        :to="homeTo"
        class="text-2xl font-bold text-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-400"
      >
        Resume<span class="text-sky-400">AI</span>
      </NuxtLink>

      <div class="flex flex-wrap items-center gap-6">
        <nav
          class="flex items-center gap-6 text-sm"
          aria-label="Primary"
        >
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="transition"
            :class="linkActive(link.to, link.exact)
              ? 'font-semibold text-sky-400'
              : 'text-slate-400 hover:text-slate-200'"
          >
            {{ link.label }}
          </NuxtLink>
        </nav>

        <LangSwitch />
        <AuthBar @logout="onLogout" />
      </div>
    </header>

    <slot />

    <LoginModal />
  </div>
</template>
