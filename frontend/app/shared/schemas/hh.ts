import { z } from 'zod'

export const hhVacancyOutSchema = z.object({
  id: z.string(),
  title: z.string(),
  employer_name: z.string(),
  area_name: z.string().nullable().optional(),
  salary_from: z.number().nullable().optional(),
  salary_to: z.number().nullable().optional(),
  salary_currency: z.string().nullable().optional(),
  published_at: z.string(),
  requirement: z.string().nullable().optional(),
  responsibility: z.string().nullable().optional(),
  experience: z.string().nullable().optional(),
  schedule: z.string().nullable().optional(),
  url: z.string()
})

export const hhVacancyListSchema = z.object({
  found: z.number(),
  page: z.number(),
  pages: z.number(),
  per_page: z.number(),
  items: z.array(hhVacancyOutSchema)
})

/** Mirrors backend `HH_CATEGORIES` keys. */
export const HH_CATEGORIES = [
  'all',
  'hr',
  'it',
  'sales',
  'marketing',
  'finance'
] as const

export const hhCategorySchema = z.enum(HH_CATEGORIES)

export type HhVacancyOut = z.infer<typeof hhVacancyOutSchema>
export type HhVacancyList = z.infer<typeof hhVacancyListSchema>
export type HhCategory = z.infer<typeof hhCategorySchema>
