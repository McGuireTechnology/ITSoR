import { computed, ref } from 'vue'
import { getListPathForDomain, getWorkspaceForDomain, workspaceConfig } from './workspaceNav'

const FAVORITES_STORAGE_KEY = 'itsor.navigation.favorites.v1'
const RECENTS_STORAGE_KEY = 'itsor.navigation.recents.v1'
const MAX_FAVORITES = 60
const MAX_RECENTS = 60

const hiddenPaths = new Set(['/login', '/signup', '/logout'])

function normalizeString(value) {
  return String(value || '').trim()
}

function pathMatches(path, candidate) {
  if (!path || !candidate) {
    return false
  }

  if (candidate === '/') {
    return path === '/'
  }

  return path === candidate || path.startsWith(`${candidate}/`)
}

function toFavoriteId(level, key) {
  return `${normalizeString(level)}:${normalizeString(key)}`
}

function fallbackLabelFromPath(path) {
  const normalizedPath = normalizeString(path)
  if (!normalizedPath) {
    return 'Home'
  }

  if (normalizedPath === '/') {
    return 'Home'
  }

  const parts = normalizedPath
    .split('/')
    .map((item) => item.trim())
    .filter(Boolean)

  if (!parts.length) {
    return 'Home'
  }

  return parts[parts.length - 1]
    .split('-')
    .map((item) => item.charAt(0).toUpperCase() + item.slice(1))
    .join(' ')
}

function withRouteIdLabel(label, route) {
  const normalizedLabel = normalizeString(label)
  const routeId = normalizeString(route?.params?.id)
  if (!routeId || !normalizedLabel) {
    return normalizedLabel || fallbackLabelFromPath(route?.path)
  }

  if (!/detail/i.test(normalizedLabel)) {
    return normalizedLabel
  }

  return `${normalizedLabel} ${routeId}`
}

function readStorageArray(storageKey) {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const raw = window.localStorage.getItem(storageKey)
    const parsed = JSON.parse(raw || '[]')
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

function writeStorageArray(storageKey, value) {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.setItem(storageKey, JSON.stringify(value))
}

function normalizeFavoriteEntry(entry) {
  const level = normalizeString(entry?.level || 'item')
  const key = normalizeString(entry?.key)
  const to = normalizeString(entry?.to)

  if (!key || !to) {
    return null
  }

  return {
    id: toFavoriteId(level, key),
    level,
    key,
    label: normalizeString(entry?.label || key),
    to,
    domainKey: normalizeString(entry?.domainKey),
    resourceKey: normalizeString(entry?.resourceKey),
    savedAt: Number.isFinite(Number(entry?.savedAt)) ? Number(entry.savedAt) : Date.now(),
  }
}

function normalizeRecentEntry(entry) {
  const to = normalizeString(entry?.to)
  if (!to) {
    return null
  }

  return {
    id: `route:${to}`,
    to,
    label: normalizeString(entry?.label || fallbackLabelFromPath(to)),
    visitedAt: Number.isFinite(Number(entry?.visitedAt)) ? Number(entry.visitedAt) : Date.now(),
  }
}

function removeRefreshQuery(pathOrFullPath) {
  const fullPath = normalizeString(pathOrFullPath)
  if (!fullPath || !fullPath.includes('?')) {
    return fullPath
  }

  try {
    const tempUrl = new URL(fullPath, 'https://itsor.local')
    tempUrl.searchParams.delete('_refresh')
    const query = tempUrl.searchParams.toString()
    const hash = normalizeString(tempUrl.hash)
    return `${tempUrl.pathname}${query ? `?${query}` : ''}${hash}`
  } catch {
    return fullPath
  }
}

function toResourceKey(resource, index) {
  const explicitKey = normalizeString(resource?.key)
  if (explicitKey) {
    return explicitKey
  }

  const explicitLabel = normalizeString(resource?.label)
  if (explicitLabel) {
    return explicitLabel.toLowerCase().replace(/\s+/g, '-')
  }

  return `resource-${index}`
}

function normalizeViewEntry(view, listKey, index) {
  const key = normalizeString(view?.key) || `${listKey}-view-${index}`
  const label = normalizeString(view?.label || key)
  const to = normalizeString(view?.to)

  if (!to) {
    return null
  }

  return {
    key,
    label,
    to,
  }
}

function normalizeListEntry(listItem, resourceKey, index) {
  const key = normalizeString(listItem?.key) || `${resourceKey}-list-${index}`
  const label = normalizeString(listItem?.label || key)
  const to = normalizeString(listItem?.to)

  if (!to) {
    return null
  }

  const views = Array.isArray(listItem?.views)
    ? listItem.views
      .map((view, viewIndex) => normalizeViewEntry(view, key, viewIndex))
      .filter(Boolean)
    : []

  return {
    key,
    label,
    to,
    views,
  }
}

function normalizeResourceEntry(resource, index) {
  const key = toResourceKey(resource, index)
  const label = normalizeString(resource?.label || key)
  const to = normalizeString(resource?.to || resource?.resources?.[0]?.to)

  if (!to) {
    return null
  }

  const lists = Array.isArray(resource?.lists)
    ? resource.lists
      .map((listItem, listIndex) => normalizeListEntry(listItem, key, listIndex))
      .filter(Boolean)
    : []

  return {
    key,
    label,
    to,
    icon: normalizeString(resource?.icon || '📄'),
    lists,
  }
}

const workspaceIconByKey = {
  admin: '🖥️',
  idm: '🪪',
  customization: '⚙️',
  grc: '📚',
}

export const groupedNavigation = computed(() => {
  return Object.entries(workspaceConfig).map(([workspaceKey, workspace]) => {
    const resources = (workspace?.namespaces || [])
      .map((resource, index) => normalizeResourceEntry(resource, index))
      .filter(Boolean)

    return {
      key: workspaceKey,
      label: normalizeString(workspace?.label || workspaceKey),
      icon: normalizeString(workspace?.icon || workspaceIconByKey[workspaceKey] || '🧭'),
      resources,
    }
  })
})

function findBestNavigationMatch(path) {
  let bestMatch = null
  let bestScore = -1

  for (const group of groupedNavigation.value) {
    const groupPath = normalizeString(group?.resources?.[0]?.to)
    if (pathMatches(path, groupPath) && groupPath.length > bestScore) {
      bestMatch = {
        level: 'domain',
        key: normalizeString(group.key),
        label: normalizeString(group.label),
        to: groupPath,
        domainKey: normalizeString(group.key),
        resourceKey: '',
      }
      bestScore = groupPath.length
    }

    for (const resource of group.resources || []) {
      const resourcePath = normalizeString(resource?.to)
      if (pathMatches(path, resourcePath) && resourcePath.length > bestScore) {
        bestMatch = {
          level: 'resource',
          key: normalizeString(resource.key),
          label: normalizeString(resource.label),
          to: resourcePath,
          domainKey: normalizeString(group.key),
          resourceKey: normalizeString(resource.key),
        }
        bestScore = resourcePath.length
      }

      for (const listItem of resource.lists || []) {
        const listPath = normalizeString(listItem?.to)
        if (pathMatches(path, listPath) && listPath.length > bestScore) {
          bestMatch = {
            level: 'list',
            key: normalizeString(listItem.key),
            label: normalizeString(listItem.label),
            to: listPath,
            domainKey: normalizeString(group.key),
            resourceKey: normalizeString(resource.key),
          }
          bestScore = listPath.length
        }

        for (const view of listItem.views || []) {
          const viewPath = normalizeString(view?.to)
          if (pathMatches(path, viewPath) && viewPath.length > bestScore) {
            bestMatch = {
              level: 'item',
              key: normalizeString(view.key),
              label: normalizeString(view.label),
              to: viewPath,
              domainKey: normalizeString(group.key),
              resourceKey: normalizeString(resource.key),
            }
            bestScore = viewPath.length
          }
        }
      }
    }
  }

  return bestMatch
}

function readFavoriteEntries() {
  return readStorageArray(FAVORITES_STORAGE_KEY)
    .map((entry) => normalizeFavoriteEntry(entry))
    .filter(Boolean)
    .slice(0, MAX_FAVORITES)
}

function readRecentEntries() {
  return readStorageArray(RECENTS_STORAGE_KEY)
    .map((entry) => normalizeRecentEntry(entry))
    .filter(Boolean)
    .slice(0, MAX_RECENTS)
}

export const favoriteEntries = ref(readFavoriteEntries())
export const recentEntries = ref(readRecentEntries())

function persistFavoriteEntries() {
  writeStorageArray(FAVORITES_STORAGE_KEY, favoriteEntries.value)
}

function persistRecentEntries() {
  writeStorageArray(RECENTS_STORAGE_KEY, recentEntries.value)
}

export function isFavorite(level, key) {
  const favoriteId = toFavoriteId(level, key)
  return favoriteEntries.value.some((entry) => entry.id === favoriteId)
}

export function toggleFavorite(entry) {
  const normalizedEntry = normalizeFavoriteEntry(entry)
  if (!normalizedEntry) {
    return
  }

  const existingIndex = favoriteEntries.value.findIndex(
    (favoriteEntry) => favoriteEntry.id === normalizedEntry.id,
  )

  if (existingIndex >= 0) {
    favoriteEntries.value = favoriteEntries.value.filter(
      (favoriteEntry) => favoriteEntry.id !== normalizedEntry.id,
    )
    persistFavoriteEntries()
    return
  }

  favoriteEntries.value = [normalizedEntry, ...favoriteEntries.value].slice(0, MAX_FAVORITES)
  persistFavoriteEntries()
}

export function resolveRouteFavoriteEntry(route) {
  const path = normalizeString(route?.path)
  if (!path || hiddenPaths.has(path)) {
    return null
  }

  const bestNavigationMatch = findBestNavigationMatch(path)
  if (bestNavigationMatch) {
    return bestNavigationMatch
  }

  const domain = normalizeString(route?.meta?.domain)
  const workspaceKey = getWorkspaceForDomain(domain)
  const fallbackTo = normalizeString(getListPathForDomain(domain) || path)

  return {
    level: domain ? 'resource' : 'item',
    key: normalizeString(domain || path),
    label: withRouteIdLabel(route?.meta?.title, route),
    to: fallbackTo,
    domainKey: normalizeString(workspaceKey),
    resourceKey: normalizeString(domain),
  }
}

export function trackRouteVisit(route) {
  const path = normalizeString(route?.path)
  if (!path || hiddenPaths.has(path)) {
    return
  }

  const routeTarget = removeRefreshQuery(normalizeString(route?.fullPath || path))
  const routeLabel = withRouteIdLabel(route?.meta?.title, route)
  const normalizedEntry = normalizeRecentEntry({
    to: routeTarget,
    label: routeLabel,
  })

  if (!normalizedEntry) {
    return
  }

  recentEntries.value = [
    normalizedEntry,
    ...recentEntries.value.filter((entry) => entry.id !== normalizedEntry.id),
  ].slice(0, MAX_RECENTS)

  persistRecentEntries()
}
