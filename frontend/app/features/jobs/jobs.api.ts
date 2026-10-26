import { apiRequest } from '~/shared/api/http'
import {
  jobOutSchema,
  seekerApplicationSchema,
  type JobOut,
  type SeekerApplication
} from '~/shared/schemas/jobs'

export async function listJobs(): Promise<JobOut[]> {
  const data = await apiRequest<unknown>('/api/jobs')
  return jobOutSchema.array().parse(data)
}

export async function applyToJob(jobId: number, resumeId: number): Promise<SeekerApplication> {
  const data = await apiRequest<unknown>(`/api/jobs/${jobId}/apply`, {
    method: 'POST',
    body: { resume_id: resumeId }
  })
  return seekerApplicationSchema.parse(data)
}

export async function listMyApplications(): Promise<SeekerApplication[]> {
  const data = await apiRequest<unknown>('/api/applications')
  return seekerApplicationSchema.array().parse(data)
}
