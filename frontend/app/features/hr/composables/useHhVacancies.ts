import { useAuth } from '~/features/auth/composables/useAuth'
import type { HhCategory, HhVacancyList } from '~/shared/schemas/hh'
import { listHhVacancies } from '../hh.api'

function emptyList(): HhVacancyList {
  return {
    found: 0,
    page: 0,
    pages: 0,
    per_page: 20,
    items: []
  }
}

export interface UseHhVacanciesOptions {
  /** Initial category tab. */
  defaultCategory?: HhCategory
  /** AsyncData cache key suffix so HR and jobs pages do not clash. */
  cacheKey?: string
}

export function useHhVacancies(options: UseHhVacanciesOptions = {}) {
  const auth = useAuth()
  const page = ref(0)
  const category = ref<HhCategory>(options.defaultCategory ?? 'hr')
  const searchInput = ref('')
  const searchText = ref('')
  let debounceTimer: ReturnType<typeof setTimeout> | null = null

  const cacheKey = options.cacheKey ?? 'hh-vacancies'

  const {
    data: list,
    pending,
    error,
    refresh
  } = useAsyncData(
    cacheKey,
    async () => {
      if (!auth.isAuthenticated.value) return emptyList()
      return listHhVacancies({
        page: page.value,
        text: searchText.value,
        category: category.value
      })
    },
    {
      default: emptyList,
      watch: [
        page,
        category,
        searchText,
        () => auth.isAuthenticated.value
      ]
    }
  )

  const canPrev = computed(() => page.value > 0)
  const canNext = computed(() => page.value + 1 < (list.value?.pages ?? 0))

  function prevPage(): void {
    if (!canPrev.value) return
    page.value -= 1
  }

  function nextPage(): void {
    if (!canNext.value) return
    page.value += 1
  }

  function setCategory(next: HhCategory): void {
    if (category.value === next) return
    category.value = next
    page.value = 0
  }

  function applySearch(): void {
    const next = searchInput.value.trim()
    if (searchText.value === next) {
      void refresh()
      return
    }
    searchText.value = next
    page.value = 0
  }

  function onSearchInput(): void {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      applySearch()
    }, 350)
  }

  function clearSearch(): void {
    searchInput.value = ''
    if (searchText.value) {
      searchText.value = ''
      page.value = 0
    }
  }

  return {
    list,
    pending,
    error,
    refresh,
    page,
    category,
    searchInput,
    searchText,
    canPrev,
    canNext,
    prevPage,
    nextPage,
    setCategory,
    applySearch,
    onSearchInput,
    clearSearch
  }
}
