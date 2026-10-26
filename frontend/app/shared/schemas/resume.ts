import { z } from 'zod'

export const resumeLanguageSchema = z.enum(['kk', 'ru', 'en'])
export const resumeTemplateSchema = z.enum(['classic', 'modern', 'minimal'])

export const personalInfoSchema = z.object({
  full_name: z.string().min(1),
  email: z.string().email(),
  phone: z.string().min(1),
  position: z.string().min(1)
})

export const experienceItemSchema = z.object({
  company: z.string(),
  role: z.string(),
  period: z.string(),
  description: z.string()
})

export const resumeRequestSchema = z.object({
  personal: personalInfoSchema,
  skills: z.array(z.string()).default([]),
  experience: z.array(experienceItemSchema).default([]),
  education: z.string().default(''),
  target_job: z.string().default(''),
  language: resumeLanguageSchema.default('kk'),
  template: resumeTemplateSchema.default('classic')
})

export const analysisIssueSchema = z.object({
  section: z.string(),
  severity: z.string(),
  message: z.string(),
  suggestion: z.string()
})

export const analysisResponseSchema = z.object({
  completeness_score: z.number(),
  match_score: z.number(),
  precision: z.number(),
  recall: z.number(),
  issues: z.array(analysisIssueSchema),
  keywords_found: z.array(z.string()),
  keywords_missing: z.array(z.string())
})

export const generateResponseSchema = z.object({
  id: z.number(),
  resume_text: z.string(),
  format: z.string().default('plain'),
  generated_by: z.string(),
  language: resumeLanguageSchema.default('kk'),
  template: resumeTemplateSchema.default('classic'),
  analysis: analysisResponseSchema.nullable().optional()
})

export const resumeSummarySchema = z.object({
  id: z.number(),
  title: z.string(),
  target_job: z.string(),
  generated_by: z.string(),
  created_at: z.string(),
  updated_at: z.string()
})

export const resumeDetailSchema = resumeSummarySchema.extend({
  resume_text: z.string(),
  language: resumeLanguageSchema.default('kk'),
  template: resumeTemplateSchema.default('classic'),
  analysis: analysisResponseSchema.nullable().optional()
})

export type ResumeLanguage = z.infer<typeof resumeLanguageSchema>
export type ResumeTemplate = z.infer<typeof resumeTemplateSchema>
export type PersonalInfo = z.infer<typeof personalInfoSchema>
export type ExperienceItem = z.infer<typeof experienceItemSchema>
export type ResumeRequest = z.infer<typeof resumeRequestSchema>
export type AnalysisIssue = z.infer<typeof analysisIssueSchema>
export type AnalysisResponse = z.infer<typeof analysisResponseSchema>
export type GenerateResponse = z.infer<typeof generateResponseSchema>
export type ResumeSummary = z.infer<typeof resumeSummarySchema>
export type ResumeDetail = z.infer<typeof resumeDetailSchema>
