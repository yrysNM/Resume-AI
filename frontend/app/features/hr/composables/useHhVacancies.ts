import { useAuth } from '~/features/auth/composables/useAuth'
import type { HhVacancyList } from '~/shared/schemas/hh'
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

export function useHhVacancies() {
  const auth = useAuth()
  const page = ref(0)

  const {
    data: list,
    pending,
    error,
    refresh
  } = useAsyncData(
    'hh-hr-vacancies',
    async () => {
      if (!auth.isAuthenticated.value || !auth.isHr.value) return emptyList()
      return listHhVacancies(page.value)
    },
    {
      default: emptyList,
      watch: [page, () => auth.isAuthenticated.value, () => auth.isHr.value]
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

  return {
    list,
    pending,
    error,
    refresh,
    page,
    canPrev,
    canNext,
    prevPage,
    nextPage
  }
}
