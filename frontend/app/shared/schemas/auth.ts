import { z } from 'zod'

export const userRegisterSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(128),
  full_name: z.string().max(255).default('')
})

export const userLoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
})

export const tokenResponseSchema = z.object({
  access_token: z.string(),
  token_type: z.string().default('bearer')
})

export const userOutSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  full_name: z.string(),
  created_at: z.string()
})

export type UserRegister = z.infer<typeof userRegisterSchema>
export type UserLogin = z.infer<typeof userLoginSchema>
export type TokenResponse = z.infer<typeof tokenResponseSchema>
export type UserOut = z.infer<typeof userOutSchema>
