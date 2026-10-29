import { apiRequest } from '~/shared/api/http'
import {
  hhVacancyListSchema,
  type HhVacancyList
} from '~/shared/schemas/hh'

export async function listHhVacancies(page = 0): Promise<HhVacancyList> {
  const data = await apiRequest<unknown>('/api/hh/vacancies', {
    query: { page }
  })
  return hhVacancyListSchema.parse(data)
}
