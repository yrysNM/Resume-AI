import type { HrApplication } from '~/shared/schemas/hr'

export function applicantName(application: HrApplication): string {
  const line = application.resume_text
    .split('\n')
    .map(part => part.trim())
    .find(Boolean)
  if (line) return line.replace(/^#+\s*/, '').slice(0, 80)
  return `#${application.id}`
}
