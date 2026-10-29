import { z } from 'zod'

export const hhVacancyOutSchema = z.object({
  id: z.string(),
  title: z.string(),
  employer_name: z.string(),
  area_name: z.string().nullable(),
  salary_from: z.number().nullable(),
  salary_to: z.number().nullable(),
  salary_currency: z.string().nullable(),
  published_at: z.string(),
  requirement: z.string().nullable(),
  responsibility: z.string().nullable(),
  experience: z.string().nullable(),
  schedule: z.string().nullable(),
  url: z.string()
})

export const hhVacancyListSchema = z.object({
  found: z.number(),
  page: z.number(),
  pages: z.number(),
  per_page: z.number(),
  items: z.array(hhVacancyOutSchema)
})

export type HhVacancyOut = z.infer<typeof hhVacancyOutSchema>
export type HhVacancyList = z.infer<typeof hhVacancyListSchema>
