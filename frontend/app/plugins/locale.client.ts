type AppLocale = 'kk' | 'ru' | 'en'

function isAppLocale(value: string): value is AppLocale {
  return value === 'kk' || value === 'ru' || value === 'en'
}

export default defineNuxtPlugin({
  name: 'locale-client',
  dependsOn: ['i18n:plugin'],
  async setup(nuxtApp) {
    let saved: string | null
    try {
      saved = localStorage.getItem('lang')
    } catch {
      return
    }

    if (!saved || !isAppLocale(saved)) return

    const { locale, localeCodes, setLocale } = nuxtApp.$i18n
    if (!localeCodes.value.includes(saved) || saved === locale.value) return

    await setLocale(saved)
  }
})
