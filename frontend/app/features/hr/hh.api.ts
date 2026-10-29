import { apiRequest } from '~/shared/api/http'
import {
  hhVacancyListSchema,
  type HhCategory,
  type HhVacancyList
} from '~/shared/schemas/hh'

export interface ListHhVacanciesParams {
  page?: number
  text?: string
  category?: HhCategory
}

export async function listHhVacancies(
  params: ListHhVacanciesParams = {}
): Promise<HhVacancyList> {
  const data = await apiRequest<unknown>('/api/hh/vacancies', {
    query: {
      page: params.page ?? 0,
      text: params.text?.trim() || undefined,
      category: params.category
    }
  })
  return hhVacancyListSchema.parse(data)
}
