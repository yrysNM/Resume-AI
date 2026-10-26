import { apiRequest } from '~/shared/api/http'
import { dashboardOutSchema, type DashboardOut } from '~/shared/schemas/dashboard'

export async function fetchDashboard(): Promise<DashboardOut> {
  const data = await apiRequest<unknown>('/api/dashboard')
  return dashboardOutSchema.parse(data)
}
