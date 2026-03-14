export function formatNameId(name, id, fallback = '(unnamed)') {
  const normalizedName = typeof name === 'string' ? name.trim() : ''
  const displayName = normalizedName || fallback

  if (!id) {
    return displayName
  }

  return `${displayName} (${id})`
}
