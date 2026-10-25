export class AppError extends Error {
  readonly status: number
  readonly detail: unknown

  constructor(message: string, status = 500, detail: unknown = null) {
    super(message)
    this.name = 'AppError'
    this.status = status
    this.detail = detail
  }
}

export function isAppError(error: unknown): error is AppError {
  return error instanceof AppError
}
