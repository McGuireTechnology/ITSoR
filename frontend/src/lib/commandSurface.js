import { reactive } from 'vue'

const defaultMetrics = Object.freeze({
  total: Number.NaN,
  selected: 0,
  selectedIds: [],
  noun: 'items',
})

export const commandSurfaceMetrics = reactive({
  total: defaultMetrics.total,
  selected: defaultMetrics.selected,
  selectedIds: [...defaultMetrics.selectedIds],
  noun: defaultMetrics.noun,
})

function normalizeNumber(value, fallback) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue : fallback
}

function normalizeSelectedIds(value) {
  if (!Array.isArray(value)) {
    return []
  }

  return value
    .map((item) => String(item || '').trim())
    .filter(Boolean)
}

export function setCommandSurfaceMetrics(metrics = {}) {
  commandSurfaceMetrics.total = normalizeNumber(metrics.total, 0)
  commandSurfaceMetrics.selected = normalizeNumber(metrics.selected, 0)
  commandSurfaceMetrics.selectedIds = normalizeSelectedIds(metrics.selectedIds)
  commandSurfaceMetrics.noun = String(metrics.noun || 'items')
}

export function clearCommandSurfaceMetrics() {
  commandSurfaceMetrics.total = defaultMetrics.total
  commandSurfaceMetrics.selected = defaultMetrics.selected
  commandSurfaceMetrics.selectedIds = [...defaultMetrics.selectedIds]
  commandSurfaceMetrics.noun = defaultMetrics.noun
}
