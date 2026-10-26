export function formatMatchScore(score: number | null | undefined): string {
  if (score === null || score === undefined || Number.isNaN(score)) return '—'
  const percent = score >= 0 && score <= 1 ? score * 100 : score
  return `${Math.round(percent)}%`
}
