import { apiBlob, apiRequest, downloadBlob } from '~/shared/api/http'
import {
  analysisResponseSchema,
  generateResponseSchema,
  resumeDetailSchema,
  resumeSummarySchema,
  type AnalysisResponse,
  type GenerateResponse,
  type ResumeDetail,
  type ResumeRequest,
  type ResumeSummary
} from '~/shared/schemas/resume'

export async function generateResume(payload: ResumeRequest): Promise<GenerateResponse> {
  const data = await apiRequest<unknown>('/api/resume/generate', {
    method: 'POST',
    body: payload
  })
  return generateResponseSchema.parse(data)
}

export async function analyzeResume(payload: ResumeRequest): Promise<AnalysisResponse> {
  const data = await apiRequest<unknown>('/api/resume/analyze', {
    method: 'POST',
    body: payload
  })
  return analysisResponseSchema.parse(data)
}

export async function listResumes(): Promise<ResumeSummary[]> {
  const data = await apiRequest<unknown>('/api/resumes')
  return resumeSummarySchema.array().parse(data)
}

export async function getResume(id: number): Promise<ResumeDetail> {
  const data = await apiRequest<unknown>(`/api/resumes/${id}`)
  return resumeDetailSchema.parse(data)
}

export async function deleteResume(id: number): Promise<void> {
  await apiRequest<unknown>(`/api/resumes/${id}`, { method: 'DELETE' })
}

export async function exportResume(
  id: number,
  format: 'pdf' | 'docx',
  template?: string
): Promise<void> {
  const { blob, filename } = await apiBlob(`/api/resumes/${id}/export`, {
    method: 'GET',
    query: { format, template }
  })
  downloadBlob(blob, filename || `resume.${format}`)
}
