import { z } from 'zod'

export const vacancyStatusSchema = z.enum(['open', 'closed'])

export const companyCreateSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().default(''),
  website: z.string().max(512).nullable().optional()
})

export const companyUpdateSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().optional(),
  website: z.string().max(512).nullable().optional()
})

export const companyOutSchema = z.object({
  id: z.number(),
  user_id: z.number(),
  name: z.string(),
  description: z.string(),
  website: z.string().nullable(),
  created_at: z.string()
})

export const vacancyCreateSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().default(''),
  status: vacancyStatusSchema.default('open')
})

export const vacancyUpdateSchema = z.object({
  title: z.string().min(1).max(255).optional(),
  description: z.string().optional(),
  status: vacancyStatusSchema.optional()
})

export const vacancyOutSchema = z.object({
  id: z.number(),
  company_id: z.number(),
  title: z.string(),
  description: z.string(),
  status: vacancyStatusSchema,
  created_at: z.string()
})

export const hrApplicationSchema = z.object({
  id: z.number(),
  vacancy_id: z.number(),
  seeker_id: z.number(),
  resume_id: z.number().nullable(),
  resume_text: z.string(),
  match_score: z.number(),
  ranked_by: z.string(),
  created_at: z.string()
})

export type VacancyStatus = z.infer<typeof vacancyStatusSchema>
export type CompanyCreate = z.infer<typeof companyCreateSchema>
export type CompanyUpdate = z.infer<typeof companyUpdateSchema>
export type CompanyOut = z.infer<typeof companyOutSchema>
export type VacancyCreate = z.infer<typeof vacancyCreateSchema>
export type VacancyUpdate = z.infer<typeof vacancyUpdateSchema>
export type VacancyOut = z.infer<typeof vacancyOutSchema>
export type HrApplication = z.infer<typeof hrApplicationSchema>
