// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@pinia/nuxt',
    '@nuxtjs/i18n'
  ],

  ssr: false,

  components: [
    { path: '~/components' },
    { path: '~/features/auth/components', pathPrefix: false },
    { path: '~/features/resume/components', pathPrefix: false },
    { path: '~/features/library/components', pathPrefix: false }
  ],

  imports: {
    dirs: [
      'features/**/composables',
      'shared/utils',
      'shared/constants'
    ]
  },

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  colorMode: {
    preference: 'dark',
    fallback: 'dark'
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000'
    }
  },

  routeRules: {
    '/**': { ssr: false }
  },

  compatibilityDate: '2026-06-30',

  typescript: {
    strict: true,
    typeCheck: false
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  i18n: {
    locales: [
      { code: 'kk', language: 'kk-KZ', name: 'KK', file: 'kk.json' },
      { code: 'ru', language: 'ru-RU', name: 'RU', file: 'ru.json' },
      { code: 'en', language: 'en-US', name: 'EN', file: 'en.json' }
    ],
    langDir: 'locales',
    defaultLocale: 'kk',
    strategy: 'no_prefix',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'lang',
      fallbackLocale: 'kk'
    }
  }
})
