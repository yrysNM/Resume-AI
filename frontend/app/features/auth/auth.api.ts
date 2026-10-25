import { apiRequest } from '~/shared/api/http'
import {
  tokenResponseSchema,
  userOutSchema,
  type TokenResponse,
  type UserLogin,
  type UserOut,
  type UserRegister
} from '~/shared/schemas/auth'

export async function loginUser(payload: UserLogin): Promise<TokenResponse> {
  const data = await apiRequest<unknown>('/api/auth/login', {
    method: 'POST',
    body: payload,
    auth: false
  })
  return tokenResponseSchema.parse(data)
}

export async function registerUser(payload: UserRegister): Promise<TokenResponse> {
  const data = await apiRequest<unknown>('/api/auth/register', {
    method: 'POST',
    body: payload,
    auth: false
  })
  return tokenResponseSchema.parse(data)
}

export async function fetchCurrentUser(): Promise<UserOut> {
  const data = await apiRequest<unknown>('/api/auth/me')
  return userOutSchema.parse(data)
}
