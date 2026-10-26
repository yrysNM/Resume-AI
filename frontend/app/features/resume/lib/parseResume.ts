import type { ResumeLanguage } from '~/shared/schemas/resume'

export interface SectionHeadings {
  experience: string
  skills: string
  education: string
  target: string
}

export const SECTION_HEADINGS: Record<ResumeLanguage, SectionHeadings> = {
  kk: {
    experience: 'ҚЫЗМЕТ ТӘЖІРИБЕСІ',
    skills: 'ДАҒДЫЛАР',
    education: 'БІЛІМ',
    target: 'Мақсатты лауазым'
  },
  ru: {
    experience: 'ОПЫТ РАБОТЫ',
    skills: 'НАВЫКИ',
    education: 'ОБРАЗОВАНИЕ',
    target: 'Целевая должность'
  },
  en: {
    experience: 'EXPERIENCE',
    skills: 'SKILLS',
    education: 'EDUCATION',
    target: 'Target role'
  }
}

export interface ParsedResume {
  name: string
  headline: string
  experience: string
  skills: string
  education: string
  target: string
  raw: string
  hasSections: boolean
}

type SectionKey = 'experience' | 'skills' | 'education' | 'target'

function norm(value: string): string {
  return value.trim().replace(/:+$/, '').toLocaleLowerCase()
}

function headingIndex(): Record<string, SectionKey> {
  const index: Record<string, SectionKey> = {}
  for (const headings of Object.values(SECTION_HEADINGS)) {
    index[norm(headings.experience)] = 'experience'
    index[norm(headings.skills)] = 'skills'
    index[norm(headings.education)] = 'education'
    index[norm(headings.target)] = 'target'
  }
  return index
}

const HEADING_INDEX = headingIndex()

function matchHeading(line: string): { key: SectionKey, inline: string } | null {
  const stripped = line.trim()
  if (!stripped) return null
  const exact = HEADING_INDEX[norm(stripped)]
  if (exact) return { key: exact, inline: '' }
  const colon = stripped.indexOf(':')
  if (colon > 0) {
    const key = HEADING_INDEX[norm(stripped.slice(0, colon))]
    if (key) return { key, inline: stripped.slice(colon + 1).trim() }
  }
  return null
}

export function headingsFor(language: string): SectionHeadings {
  if (language === 'kk' || language === 'ru' || language === 'en') {
    return SECTION_HEADINGS[language]
  }
  return SECTION_HEADINGS.kk
}

export function parseResumeText(resumeText: string): ParsedResume {
  const raw = resumeText.trim()
  const parsed: ParsedResume = {
    name: '',
    headline: '',
    experience: '',
    skills: '',
    education: '',
    target: '',
    raw,
    hasSections: false
  }
  if (!raw) return parsed

  let currentKey: SectionKey | null = null
  const preamble: string[] = []
  const buckets: Record<SectionKey, string[]> = {
    experience: [],
    skills: [],
    education: [],
    target: []
  }

  for (const line of raw.split('\n')) {
    const matched = matchHeading(line)
    if (matched) {
      currentKey = matched.key
      if (matched.inline) buckets[currentKey].push(matched.inline)
      continue
    }
    if (currentKey === null) {
      if (line.trim()) preamble.push(line.trim())
      continue
    }
    buckets[currentKey].push(line)
  }

  if (preamble.length > 0) {
    parsed.name = preamble[0] ?? ''
    parsed.headline = preamble.slice(1).join(' | ')
  }
  parsed.experience = buckets.experience.join('\n').trim()
  parsed.skills = buckets.skills.join('\n').trim()
  parsed.education = buckets.education.join('\n').trim()
  parsed.target = buckets.target.join('\n').trim()
  parsed.hasSections = Boolean(
    parsed.experience || parsed.skills || parsed.education || parsed.target
  )
  return parsed
}
