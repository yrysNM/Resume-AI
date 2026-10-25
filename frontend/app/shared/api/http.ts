import { AppError } from '../types/errors'
import { readToken } from '../utils/token'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

export interface HttpOptions {
  method?: HttpMethod
  body?: unknown
  headers?: Record<string, string>
  query?: Record<string, string | number | boolean | undefined>
  auth?: boolean
}

function getApiBase(): string {
  const config = useRuntimeConfig()
  return String(config.public.apiBase || 'http://127.0.0.1:8000').replace(/\/$/, '')
}

function buildUrl(path: string, query?: HttpOptions['query']): string {
  const base = getApiBase()
  const url = new URL(path.startsWith('http') ? path : `${base}${path}`)
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined) url.searchParams.set(key, String(value))
    }
  }
  return url.toString()
}

function messageFromDetail(detail: unknown, fallback: string): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === 'object' && 'msg' in item) {
          return String((item as { msg: unknown }).msg)
        }
        return JSON.stringify(item)
      })
      .join('; ')
  }
  return fallback
}

async function parseError(response: Response): Promise<AppError> {
  const text = await response.text()
  let data: unknown
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = { detail: text }
  }
  const detail = data && typeof data === 'object' && 'detail' in data
    ? (data as { detail: unknown }).detail
    : data
  const message = messageFromDetail(detail, response.statusText || `HTTP ${response.status}`)
  return new AppError(message, response.status, detail)
}

export async function apiRequest<T>(path: string, options: HttpOptions = {}): Promise<T> {
  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...(options.headers || {})
  }

  if (options.body !== undefined) {
    headers['Content-Type'] = 'application/json'
  }

  if (options.auth !== false) {
    const token = readToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(buildUrl(path, options.query), {
    method: options.method || (options.body !== undefined ? 'POST' : 'GET'),
    headers,
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined
  })

  if (!response.ok) {
    throw await parseError(response)
  }

  if (response.status === 204) {
    return undefined as T
  }

  const text = await response.text()
  if (!text) return undefined as T
  return JSON.parse(text) as T
}

export interface BlobDownload {
  blob: Blob
  filename: string
}

export async function apiBlob(path: string, options: HttpOptions = {}): Promise<BlobDownload> {
  const headers: Record<string, string> = { ...(options.headers || {}) }

  if (options.auth !== false) {
    const token = readToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(buildUrl(path, options.query), {
    method: options.method || 'GET',
    headers
  })

  if (!response.ok) {
    throw await parseError(response)
  }

  const blob = await response.blob()
  const disposition = response.headers.get('Content-Disposition') || ''
  const match = /filename="?([^"]+)"?/i.exec(disposition)
  const filename = match?.[1] || 'download'
  return { blob, filename }
}

export function downloadBlob(blob: Blob, filename: string): void {
  if (!import.meta.client) return
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}
