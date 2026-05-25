/** Replace underscores with spaces and capitalize each word. */
export function formatLabel(value) {
  if (value == null || value === '') return ''
  return String(value)
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

/** Compact number for chart axes (e.g. 1200 → 1.2K). */
export function formatCompactNumber(value) {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`
  return String(Math.round(value))
}
