import { z } from 'zod'

export const jobOutSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string(),
  company_id: z.number(),
  company_name: z.string()
})

export const applyRequestSchema = z.object({
  resume_id: z.number()
})

export const seekerApplicationSchema = z.object({
  id: z.number(),
  vacancy_id: z.number(),
  vacancy_title: z.string(),
  resume_id: z.number().nullable(),
  match_score: z.number(),
  ranked_by: z.string(),
  created_at: z.string()
})

export type JobOut = z.infer<typeof jobOutSchema>
export type ApplyRequest = z.infer<typeof applyRequestSchema>
export type SeekerApplication = z.infer<typeof seekerApplicationSchema>
