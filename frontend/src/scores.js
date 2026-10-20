// Helpers for showing scores. Used by the result view, the comparison and the PDF.

// Turn a 0-100 score into a band (label + color class). Matches the rubric in the prompt.
export function scoreBand(score) {
  if (score >= 90) return { label: 'Excellent', cls: 'good' }
  if (score >= 75) return { label: 'Strong', cls: 'good' }
  if (score >= 50) return { label: 'Average', cls: 'ok' }
  if (score >= 25) return { label: 'Weak', cls: 'bad' }
  return { label: 'Very poor', cls: 'bad' }
}

// 5 -> "+5", -5 -> "-5", 0 -> "0", null -> "-"
export function formatDelta(delta) {
  if (delta === null || delta === undefined) return '-'
  return delta > 0 ? `+${delta}` : `${delta}`
}

// Color class for a change: green if better, pink if worse
export function deltaClass(delta) {
  if (delta > 0) return 'good'
  if (delta < 0) return 'bad'
  return ''
}
