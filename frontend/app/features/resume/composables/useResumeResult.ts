import { computed } from 'vue'
import type { AnalysisResponse, GenerateResponse } from '~/shared/schemas/resume'

export interface ResumeResult {
  gen: Pick<GenerateResponse, 'id' | 'resume_text' | 'generated_by' | 'language' | 'template'> & {
    format?: string
  }
  analysis: AnalysisResponse | {
    completeness_score: number | string
    match_score: number | string
    precision: number
    recall: number
    issues: AnalysisResponse['issues']
    keywords_found?: string[]
    keywords_missing?: string[]
  }
}

export function useResumeResult() {
  const result = useState<ResumeResult | null>('resume-result', () => null)

  function clearResult() {
    result.value = null
  }

  function setResult(next: ResumeResult | null) {
    result.value = next
  }

  const hasExportable = computed(() => Boolean(result.value?.gen?.id))

  return {
    result,
    hasExportable,
    clearResult,
    setResult
  }
}
