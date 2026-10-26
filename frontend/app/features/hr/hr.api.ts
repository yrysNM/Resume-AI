import { apiRequest } from '~/shared/api/http'
import {
  companyOutSchema,
  hrApplicationSchema,
  vacancyOutSchema,
  type CompanyCreate,
  type CompanyOut,
  type CompanyUpdate,
  type HrApplication,
  type VacancyCreate,
  type VacancyOut,
  type VacancyUpdate
} from '~/shared/schemas/hr'

export async function listCompanies(): Promise<CompanyOut[]> {
  const data = await apiRequest<unknown>('/api/companies')
  return companyOutSchema.array().parse(data)
}

export async function getCompany(id: number): Promise<CompanyOut> {
  const data = await apiRequest<unknown>(`/api/companies/${id}`)
  return companyOutSchema.parse(data)
}

export async function createCompany(payload: CompanyCreate): Promise<CompanyOut> {
  const data = await apiRequest<unknown>('/api/companies', {
    method: 'POST',
    body: payload
  })
  return companyOutSchema.parse(data)
}

export async function updateCompany(id: number, payload: CompanyUpdate): Promise<CompanyOut> {
  const data = await apiRequest<unknown>(`/api/companies/${id}`, {
    method: 'PUT',
    body: payload
  })
  return companyOutSchema.parse(data)
}

export async function deleteCompany(id: number): Promise<void> {
  await apiRequest<unknown>(`/api/companies/${id}`, { method: 'DELETE' })
}

export async function listVacancies(companyId: number): Promise<VacancyOut[]> {
  const data = await apiRequest<unknown>(`/api/companies/${companyId}/vacancies`)
  return vacancyOutSchema.array().parse(data)
}

export async function getCompanyVacancy(
  companyId: number,
  vacancyId: number
): Promise<VacancyOut> {
  const data = await apiRequest<unknown>(
    `/api/companies/${companyId}/vacancies/${vacancyId}`
  )
  return vacancyOutSchema.parse(data)
}

export async function createVacancy(
  companyId: number,
  payload: VacancyCreate
): Promise<VacancyOut> {
  const data = await apiRequest<unknown>(`/api/companies/${companyId}/vacancies`, {
    method: 'POST',
    body: payload
  })
  return vacancyOutSchema.parse(data)
}

export async function updateVacancy(
  companyId: number,
  vacancyId: number,
  payload: VacancyUpdate
): Promise<VacancyOut> {
  const data = await apiRequest<unknown>(
    `/api/companies/${companyId}/vacancies/${vacancyId}`,
    { method: 'PUT', body: payload }
  )
  return vacancyOutSchema.parse(data)
}

export async function deleteVacancy(companyId: number, vacancyId: number): Promise<void> {
  await apiRequest<unknown>(`/api/companies/${companyId}/vacancies/${vacancyId}`, {
    method: 'DELETE'
  })
}

export async function getVacancy(vacancyId: number): Promise<VacancyOut> {
  const data = await apiRequest<unknown>(`/api/vacancies/${vacancyId}`)
  return vacancyOutSchema.parse(data)
}

export async function listVacancyApplications(vacancyId: number): Promise<HrApplication[]> {
  const data = await apiRequest<unknown>(`/api/vacancies/${vacancyId}/applications`)
  return hrApplicationSchema.array().parse(data)
}

export async function rankVacancyApplications(vacancyId: number): Promise<HrApplication[]> {
  const data = await apiRequest<unknown>(`/api/vacancies/${vacancyId}/rank`, {
    method: 'POST'
  })
  return hrApplicationSchema.array().parse(data)
}
