import { z } from 'zod'

export const hrDashboardSchema = z.object({
  role: z.literal('hr'),
  companies: z.number(),
  open_vacancies: z.number(),
  applications: z.number(),
  average_match_score: z.number().nullable()
})

export const seekerDashboardSchema = z.object({
  role: z.literal('seeker'),
  saved_resumes: z.number(),
  applications_sent: z.number(),
  best_match_score: z.number().nullable(),
  open_jobs: z.number()
})

export const dashboardOutSchema = z.discriminatedUnion('role', [
  hrDashboardSchema,
  seekerDashboardSchema
])

export type HrDashboard = z.infer<typeof hrDashboardSchema>
export type SeekerDashboard = z.infer<typeof seekerDashboardSchema>
export type DashboardOut = z.infer<typeof dashboardOutSchema>
