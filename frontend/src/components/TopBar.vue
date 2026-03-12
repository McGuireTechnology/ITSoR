<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  createTenant,
  listEntityRecords,
  listEntityTypes,
  listGroups,
  listNamespaces,
  listTenants,
  listUsers,
  listWorkspaces,
} from '../lib/api'
import { formatNameId } from '../lib/formatters'
import { favoriteEntries, recentEntries, trackRouteVisit } from '../lib/navigationState'
import { activeWorkspace, setActiveWorkspace, workspaceConfig } from '../lib/workspaceNav'
import brandLogo from '../assets/itsor-cube-logo.svg'

const router = useRouter()
const route = useRoute()
const TENANT_STORAGE_KEY = 'itsor.activeTenantId'
const TENANT_HISTORY_STORAGE_KEY = 'itsor.tenantHistory'
const SEARCH_RECENTS_STORAGE_KEY = 'itsor.searchRecents'
const TENANT_CONTEXT_CHANGED_EVENT = 'itsor:tenant-context-changed'
const GLOBAL_TENANT_ID = '__all__'
const GLOBAL_TENANT_LABEL = 'All Tenants'
const fallbackTenantLabel = import.meta.env.VITE_TENANT_NAME || 'Default Tenant'
const userDisplayName = import.meta.env.VITE_USER_DISPLAY_NAME || 'Signed-in user'
const userOrg = import.meta.env.VITE_USER_ORG || 'ITSoR Tenant'
const appWorkspaceIcons = {
  admin: '🖥️',
  idm: '🪪',
  customization: '⚙️',
  grc: '📚',
}

function getNamespaceRoute(namespace) {
  return String(namespace?.to || namespace?.resources?.[0]?.to || '/home')
}

function getWorkspaceDefaultRoute(workspace) {
  const firstNamespace = workspace?.namespaces?.[0]
  return getNamespaceRoute(firstNamespace)
}

const appResources = computed(() => {
  return Object.entries(workspaceConfig).map(([key, workspace]) => ({
    key,
    label: workspace.label,
    to: getWorkspaceDefaultRoute(workspace),
    icon: appWorkspaceIcons[key] || '🧭',
  }))
})

const searchSources = [
  {
    key: 'user',
    label: 'Users',
    type: 'User',
    iconClass: 'pi-user',
    list: listUsers,
    getText: (item) => formatNameId(item.username || item.email, item.id, '(unnamed user)'),
    getRoute: (item) => `/auth/users/${item.id}`,
  },
  {
    key: 'tenant',
    label: 'Tenants',
    type: 'Tenant',
    iconClass: 'pi-building',
    list: listTenants,
    getText: (item) => formatNameId(item.name, item.id, '(unnamed tenant)'),
    getRoute: (item) => `/auth/tenants/${item.id}`,
  },
  {
    key: 'group',
    label: 'Groups',
    type: 'Group',
    iconClass: 'pi-users',
    list: listGroups,
    getText: (item) => formatNameId(item.name, item.id, '(unnamed group)'),
    getRoute: (item) => `/auth/groups/${item.id}`,
  },
  {
    key: 'workspace',
    label: 'Workspaces',
    type: 'Workspace',
    iconClass: 'pi-briefcase',
    list: listWorkspaces,
    getText: (item) => formatNameId(item.name, item.id, '(unnamed workspace)'),
    getRoute: (item) => `/customization/workspaces/${item.id}`,
  },
  {
    key: 'namespace',
    label: 'Namespaces',
    type: 'Namespace',
    iconClass: 'pi-sitemap',
    list: listNamespaces,
    getText: (item) => formatNameId(item.name, item.id, '(unnamed namespace)'),
    getRoute: (item) => `/customization/namespaces/${item.id}`,
  },
  {
    key: 'entity-type',
    label: 'Entity Types',
    type: 'Entity Type',
    iconClass: 'pi-tags',
    list: listEntityTypes,
    getText: (item) => formatNameId(item.name, item.id, '(unnamed entity type)'),
    getRoute: (item) => `/customization/entity-types/${item.id}`,
  },
  {
    key: 'entity-record',
    label: 'Entity Records',
    type: 'Entity Record',
    iconClass: 'pi-database',
    list: listEntityRecords,
    getText: (item) => formatNameId(item.name, item.id, '(unnamed)'),
    getRoute: (item) => `/customization/entity-records/${item.id}`,
  },
]

const routeDomainToSearchType = {
  users: 'user',
  groups: 'group',
  tenants: 'tenant',
  workspaces: 'workspace',
  namespaces: 'namespace',
  'entity-types': 'entity-type',
  'entity-records': 'entity-record',
}

function inferSearchTypeFromRoute(activeRoute) {
  const domain = String(activeRoute?.meta?.domain || '')
  return routeDomainToSearchType[domain] || 'all'
}

const query = ref('')
const searching = ref(false)
const error = ref('')
const results = ref([])
const recentSearchTerms = ref([])
const searchTypeFilter = ref('all')
const searchWrapRef = ref(null)
const appLauncherWrapRef = ref(null)
const favoritesWrapRef = ref(null)
const recentsWrapRef = ref(null)
const userMenuWrapRef = ref(null)
const tenantContextWrapRef = ref(null)
const appLauncherOpen = ref(false)
const favoritesOpen = ref(false)
const recentsOpen = ref(false)
const userMenuOpen = ref(false)
const tenantContextOpen = ref(false)
const appLauncherPinned = ref(false)
const favoritesPinned = ref(false)
const recentsPinned = ref(false)
const userMenuPinned = ref(false)
const tenantContextPinned = ref(false)
const searchPinned = ref(false)
const searchDropdownOpen = ref(false)
const appLauncherQuery = ref('')
const hasSearched = ref(false)
const tenantOptions = ref([])
const activeTenantId = ref('')
const tenantLoading = ref(false)
const tenantError = ref('')
const tenantSearchQuery = ref('')
const tenantCreating = ref(false)
let searchDebounceHandle = null
let searchRequestId = 0
let skipNextQueryWatch = false

const globalTenantOption = Object.freeze({ id: GLOBAL_TENANT_ID, name: GLOBAL_TENANT_LABEL })

function matchesTenantSearch(tenant, term) {
  return `${tenant.name || ''} ${tenant.id || ''}`.toLowerCase().includes(term)
}

function readSearchRecents() {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const raw = window.localStorage.getItem(SEARCH_RECENTS_STORAGE_KEY)
    const parsed = JSON.parse(raw || '[]')
    if (!Array.isArray(parsed)) {
      return []
    }
    return parsed.map((value) => String(value).trim()).filter(Boolean).slice(0, 8)
  } catch {
    return []
  }
}

function persistSearchRecent(term) {
  const normalizedTerm = String(term || '').trim()
  if (!normalizedTerm || typeof window === 'undefined') {
    return
  }

  const next = [normalizedTerm, ...readSearchRecents().filter((value) => value !== normalizedTerm)].slice(0, 8)
  recentSearchTerms.value = next
  window.localStorage.setItem(SEARCH_RECENTS_STORAGE_KEY, JSON.stringify(next))
}

function loadSearchRecents() {
  recentSearchTerms.value = readSearchRecents()
}

function readTenantHistory() {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const raw = window.localStorage.getItem(TENANT_HISTORY_STORAGE_KEY)
    const parsed = JSON.parse(raw || '[]')
    return Array.isArray(parsed) ? parsed.map((value) => String(value)) : []
  } catch {
    return []
  }
}

const activeTenantName = computed(() => {
  if (String(activeTenantId.value) === GLOBAL_TENANT_ID) {
    return GLOBAL_TENANT_LABEL
  }

  const selected = tenantOptions.value.find((tenant) => String(tenant.id) === String(activeTenantId.value))
  return selected?.name || fallbackTenantLabel
})

const recentTenantOptions = computed(() => {
  const history = readTenantHistory()
  const byId = new Map(tenantOptions.value.map((tenant) => [String(tenant.id), tenant]))
  const resolved = []

  for (const historyId of history) {
    const resolvedTenant = byId.get(String(historyId))
    if (resolvedTenant) {
      resolved.push(resolvedTenant)
    }
    if (resolved.length >= 10) {
      break
    }
  }

  return resolved
})

const filteredRecentTenantOptions = computed(() => {
  const term = tenantSearchQuery.value.trim().toLowerCase()
  if (!term) {
    return recentTenantOptions.value
  }
  return recentTenantOptions.value.filter((tenant) => matchesTenantSearch(tenant, term))
})

const tenantSearchResults = computed(() => {
  const term = tenantSearchQuery.value.trim().toLowerCase()
  const includeGlobal = !term || matchesTenantSearch(globalTenantOption, term)
  const prefix = includeGlobal ? [globalTenantOption] : []

  if (!term) {
    return [...prefix, ...filteredRecentTenantOptions.value]
  }

  const filteredTenants = tenantOptions.value.filter((tenant) => matchesTenantSearch(tenant, term))
  return [...prefix, ...filteredTenants]
})

const canCreateFromSearch = computed(() => {
  const term = tenantSearchQuery.value.trim().toLowerCase()
  if (!term) {
    return false
  }
  return !tenantOptions.value.some((tenant) => matchesTenantSearch(tenant, term))
})
const topBarFavorites = computed(() => favoriteEntries.value.slice(0, 20))
const topBarRecents = computed(() => recentEntries.value.slice(0, 20))
const searchTypeOptions = computed(() => [{ key: 'all', label: 'All Objects' }, ...searchSources.map((source) => ({ key: source.key, label: source.label }))])
const searchPlaceholder = computed(() => {
  if (searchTypeFilter.value === 'all') {
    return 'Search users, groups, tenants...'
  }

  const selectedType = searchTypeOptions.value.find((option) => option.key === searchTypeFilter.value)
  if (!selectedType) {
    return 'Search users, groups, tenants...'
  }

  return `Search ${String(selectedType.label || '').toLowerCase()}...`
})
const showSearchDropdown = computed(() => {
  if (!searchDropdownOpen.value) {
    return false
  }

  if (!query.value.trim().length) {
    return true
  }

  return searching.value || !!error.value || results.value.length > 0 || hasSearched.value
})
const filteredAppResources = computed(() => {
  const term = appLauncherQuery.value.trim().toLowerCase()
  if (!term) {
    return appResources.value
  }

  return appResources.value.filter((resource) => String(resource.label || '').toLowerCase().includes(term))
})

function closeMenus() {
  appLauncherOpen.value = false
  favoritesOpen.value = false
  recentsOpen.value = false
  userMenuOpen.value = false
  tenantContextOpen.value = false
  appLauncherPinned.value = false
  favoritesPinned.value = false
  recentsPinned.value = false
  userMenuPinned.value = false
  tenantContextPinned.value = false
  appLauncherQuery.value = ''
}

function openAppLauncher() {
  appLauncherOpen.value = true
  favoritesOpen.value = false
  recentsOpen.value = false
  userMenuOpen.value = false
}

function closeAppLauncher() {
  if (!appLauncherPinned.value) {
    appLauncherOpen.value = false
  }
}

async function selectAppWorkspace(workspace) {
  setActiveWorkspace(workspace.key)
  const targetRoute = String(workspace.to || '/home')

  if (targetRoute && targetRoute !== route.path) {
    await router.push(targetRoute)
  }

  closeMenus()
}

function toggleAppLauncherPin() {
  if (appLauncherPinned.value) {
    appLauncherPinned.value = false
    appLauncherOpen.value = false
    return
  }

  appLauncherPinned.value = true
  favoritesPinned.value = false
  recentsPinned.value = false
  userMenuPinned.value = false
  tenantContextPinned.value = false
  appLauncherOpen.value = true
  favoritesOpen.value = false
  recentsOpen.value = false
  userMenuOpen.value = false
  tenantContextOpen.value = false
}

function openFavoritesMenu() {
  favoritesOpen.value = true
  appLauncherOpen.value = false
  recentsOpen.value = false
  userMenuOpen.value = false
}

function closeFavoritesMenu() {
  if (!favoritesPinned.value) {
    favoritesOpen.value = false
  }
}

function toggleFavoritesPin() {
  if (favoritesPinned.value) {
    favoritesPinned.value = false
    favoritesOpen.value = false
    return
  }

  favoritesPinned.value = true
  appLauncherPinned.value = false
  recentsPinned.value = false
  userMenuPinned.value = false
  tenantContextPinned.value = false
  favoritesOpen.value = true
  appLauncherOpen.value = false
  recentsOpen.value = false
  userMenuOpen.value = false
  tenantContextOpen.value = false
}

function openRecentsMenu() {
  recentsOpen.value = true
  appLauncherOpen.value = false
  favoritesOpen.value = false
  userMenuOpen.value = false
}

function closeRecentsMenu() {
  if (!recentsPinned.value) {
    recentsOpen.value = false
  }
}

function toggleRecentsPin() {
  if (recentsPinned.value) {
    recentsPinned.value = false
    recentsOpen.value = false
    return
  }

  recentsPinned.value = true
  appLauncherPinned.value = false
  favoritesPinned.value = false
  userMenuPinned.value = false
  tenantContextPinned.value = false
  recentsOpen.value = true
  appLauncherOpen.value = false
  favoritesOpen.value = false
  userMenuOpen.value = false
  tenantContextOpen.value = false
}

function openUserMenu() {
  userMenuOpen.value = true
  appLauncherOpen.value = false
  favoritesOpen.value = false
  recentsOpen.value = false
}

function closeUserMenu() {
  if (!userMenuPinned.value) {
    userMenuOpen.value = false
  }
}

function toggleUserMenuPin() {
  if (userMenuPinned.value) {
    userMenuPinned.value = false
    userMenuOpen.value = false
    return
  }

  userMenuPinned.value = true
  appLauncherPinned.value = false
  tenantContextPinned.value = false
  userMenuOpen.value = true
  appLauncherOpen.value = false
  tenantContextOpen.value = false
}

function openTenantContext() {
  tenantContextOpen.value = true
  userMenuOpen.value = false
  appLauncherOpen.value = false
}

function closeTenantContext() {
  if (!tenantContextPinned.value) {
    tenantContextOpen.value = false
  }
}

function toggleTenantContextPin() {
  if (tenantContextPinned.value) {
    tenantContextPinned.value = false
    tenantContextOpen.value = false
    return
  }

  tenantContextPinned.value = true
  appLauncherPinned.value = false
  userMenuPinned.value = false
  tenantContextOpen.value = true
  appLauncherOpen.value = false
  userMenuOpen.value = false
}

function persistTenantHistory(tenantId) {
  if (String(tenantId) === GLOBAL_TENANT_ID) {
    return
  }

  if (typeof window === 'undefined') {
    return
  }

  const current = readTenantHistory()
  const next = [String(tenantId), ...current.filter((id) => String(id) !== String(tenantId))].slice(0, 10)
  window.localStorage.setItem(TENANT_HISTORY_STORAGE_KEY, JSON.stringify(next))
}

function selectTenant(tenantId) {
  activeTenantId.value = String(tenantId)
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(TENANT_STORAGE_KEY, String(tenantId))
  }
  persistTenantHistory(tenantId)
  tenantSearchQuery.value = ''
}

async function loadTenantContext() {
  tenantLoading.value = true
  tenantError.value = ''
  try {
    const tenants = await listTenants()
    tenantOptions.value = tenants || []

    const storedTenantId = typeof window !== 'undefined' ? window.localStorage.getItem(TENANT_STORAGE_KEY) : null
    const preferredTenantId = storedTenantId || activeTenantId.value
    const preferredTenant = tenantOptions.value.find((tenant) => String(tenant.id) === String(preferredTenantId || ''))
    if (String(preferredTenantId || '') === GLOBAL_TENANT_ID) {
      activeTenantId.value = GLOBAL_TENANT_ID
    } else if (preferredTenant) {
      activeTenantId.value = String(preferredTenant.id)
    } else {
      activeTenantId.value = GLOBAL_TENANT_ID
    }

    if (typeof window !== 'undefined') {
      window.localStorage.setItem(TENANT_STORAGE_KEY, activeTenantId.value)
      if (activeTenantId.value && activeTenantId.value !== GLOBAL_TENANT_ID) {
        persistTenantHistory(activeTenantId.value)
      }
    }
  } catch (loadError) {
    tenantError.value = loadError.message
  } finally {
    tenantLoading.value = false
  }
}

async function createTenantFromSearch() {
  if (!tenantSearchQuery.value.trim()) {
    return
  }

  tenantCreating.value = true
  tenantError.value = ''
  try {
    const created = await createTenant({ name: tenantSearchQuery.value.trim() })
    await loadTenantContext()
    if (created?.id) {
      selectTenant(created.id)
    }
    closeMenus()
  } catch (saveError) {
    tenantError.value = saveError.message
  } finally {
    tenantCreating.value = false
  }
}

async function openTenantsMasterView() {
  await router.push('/auth/tenants')
  closeMenus()
}

function handleDocumentClick(event) {
  const searchWrap = searchWrapRef.value
  const appWrap = appLauncherWrapRef.value
  const favoritesWrap = favoritesWrapRef.value
  const recentsWrap = recentsWrapRef.value
  const userWrap = userMenuWrapRef.value
  const tenantWrap = tenantContextWrapRef.value
  const target = event.target

  if (searchWrap && searchWrap.contains(target)) {
    return
  }

  if (appWrap && appWrap.contains(target)) {
    return
  }

  if (favoritesWrap && favoritesWrap.contains(target)) {
    return
  }

  if (recentsWrap && recentsWrap.contains(target)) {
    return
  }

  if (userWrap && userWrap.contains(target)) {
    return
  }

  if (tenantWrap && tenantWrap.contains(target)) {
    return
  }

  searchDropdownOpen.value = false
  searchPinned.value = false
  closeMenus()
}

function handleEscape(event) {
  if (event.key === 'Escape') {
    searchDropdownOpen.value = false
    searchPinned.value = false
    closeMenus()
  }
}

function handleTenantContextChanged(event) {
  const tenantId = String(event?.detail?.tenantId || '').trim()
  if (!tenantId) {
    return
  }

  selectTenant(tenantId)
}

function openSearchDropdown() {
  searchDropdownOpen.value = true
  if (!query.value.trim().length) {
    results.value = []
    error.value = ''
    hasSearched.value = false
    searching.value = false
  }
}

function pinSearchDropdown() {
  searchPinned.value = true
  openSearchDropdown()
}

function closeSearchDropdown() {
  if (searchPinned.value) {
    return
  }
  searchDropdownOpen.value = false
}

function applySearchType(typeKey) {
  searchTypeFilter.value = typeKey
  searchDropdownOpen.value = true
  if (query.value.trim()) {
    triggerSearchNow(false)
  }
}

function useRecentSearch(term) {
  skipNextQueryWatch = true
  query.value = String(term || '').trim()
  searchDropdownOpen.value = true
  triggerSearchNow(true)
}

async function handleSearchSubmit() {
  const term = query.value.trim()

  await router.replace({
    path: route.path,
    query: {
      ...route.query,
      q: term || undefined,
    },
  })

  triggerSearchNow(true, false)
}

function triggerSearchNow(recordRecent = false, keepDropdownOpen = true) {
  if (searchDebounceHandle) {
    clearTimeout(searchDebounceHandle)
    searchDebounceHandle = null
  }
  runGlobalSearch(recordRecent, keepDropdownOpen)
}

function matches(value, term) {
  return String(value || '').toLowerCase().includes(term)
}

function pushResults(collection, source, term) {
  for (const item of collection || []) {
    const text = source.getText(item)
    if (matches(text, term)) {
      results.value.push({
        key: `${source.type}:${item.id}`,
        type: source.type,
        iconClass: source.iconClass,
        text,
        to: source.getRoute(item),
      })
    }
  }
}

async function runGlobalSearch(recordRecent = false, keepDropdownOpen = true) {
  const term = query.value.trim().toLowerCase()
  const requestId = ++searchRequestId

  if (!term) {
    results.value = []
    error.value = ''
    hasSearched.value = false
    searching.value = false
    if (!keepDropdownOpen) {
      searchDropdownOpen.value = false
      searchPinned.value = false
    }
    return
  }

  results.value = []
  error.value = ''
  hasSearched.value = false
  searchDropdownOpen.value = keepDropdownOpen
  if (!keepDropdownOpen) {
    searchPinned.value = false
  }
  if (recordRecent) {
    persistSearchRecent(query.value.trim())
  }
  searching.value = true
  try {
    const selectedSources = searchTypeFilter.value === 'all'
      ? searchSources
      : searchSources.filter((source) => source.key === searchTypeFilter.value)

    const settled = await Promise.allSettled(selectedSources.map((source) => source.list()))

    if (requestId !== searchRequestId) {
      return
    }

    selectedSources.forEach((source, index) => {
      const settledValue = settled[index]
      const collection = settledValue?.status === 'fulfilled' ? (settledValue.value || []) : []
      pushResults(collection, source, term)
    })

    results.value = results.value.slice(0, 12)
    hasSearched.value = true
  } catch (searchError) {
    if (requestId !== searchRequestId) {
      return
    }
    error.value = searchError.message
    hasSearched.value = true
  } finally {
    if (requestId === searchRequestId) {
      searching.value = false
    }
  }
}

async function navigateTo(item) {
  persistSearchRecent(query.value.trim())
  await router.push(item.to)
  query.value = ''
  results.value = []
  error.value = ''
  hasSearched.value = false
  searchDropdownOpen.value = false
  searchPinned.value = false
  closeMenus()
}

watch(query, (value) => {
  if (skipNextQueryWatch) {
    skipNextQueryWatch = false
    return
  }

  const term = value.trim()

  if (searchDebounceHandle) {
    clearTimeout(searchDebounceHandle)
  }

  if (!term) {
    results.value = []
    error.value = ''
    hasSearched.value = false
    searching.value = false
    return
  }

  searchDropdownOpen.value = true
  searchDebounceHandle = setTimeout(() => {
    runGlobalSearch(false)
  }, 180)
})

watch(
  () => route.meta?.domain,
  () => {
    searchTypeFilter.value = inferSearchTypeFromRoute(route)
  },
  { immediate: true },
)

watch(
  () => route.fullPath,
  () => {
    trackRouteVisit(route)
  },
  { immediate: true },
)

onMounted(() => {
  loadTenantContext()
  loadSearchRecents()
  document.addEventListener('click', handleDocumentClick)
  document.addEventListener('keydown', handleEscape)
  window.addEventListener(TENANT_CONTEXT_CHANGED_EVENT, handleTenantContextChanged)
})

onUnmounted(() => {
  if (searchDebounceHandle) {
    clearTimeout(searchDebounceHandle)
  }
  document.removeEventListener('click', handleDocumentClick)
  document.removeEventListener('keydown', handleEscape)
  window.removeEventListener(TENANT_CONTEXT_CHANGED_EVENT, handleTenantContextChanged)
})

</script>

<template>
  <header class="top-bar bg-brand-deep text-primary-foreground border-brand-purple">
    <div class="topbar-left">
      <div class="topbar-left-tools">
        <div
          ref="appLauncherWrapRef"
          class="app-launcher-wrap dropdown"
          :class="{ show: appLauncherOpen }"
          @mouseenter="openAppLauncher"
          @mouseleave="closeAppLauncher"
        >
          <button
            type="button"
            class="icon-button app-launcher dropdown-toggle"
            aria-label="App launcher"
            :class="{ show: appLauncherOpen }"
            :aria-expanded="appLauncherOpen ? 'true' : 'false'"
            @click.stop="toggleAppLauncherPin"
          >
            <svg class="topbar-icon-glyph app-drawer-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
              <circle cx="6" cy="6" r="1.5" />
              <circle cx="12" cy="6" r="1.5" />
              <circle cx="18" cy="6" r="1.5" />
              <circle cx="6" cy="12" r="1.5" />
              <circle cx="12" cy="12" r="1.5" />
              <circle cx="18" cy="12" r="1.5" />
              <circle cx="6" cy="18" r="1.5" />
              <circle cx="12" cy="18" r="1.5" />
              <circle cx="18" cy="18" r="1.5" />
            </svg>
          </button>
          <div class="app-menu app-menu-launcher dropdown-menu" :class="{ show: appLauncherOpen }" aria-label="App launcher menu">
            <div class="app-launcher-menu">
              <label class="app-launcher-search-wrap">
                <i class="pi pi-search app-launcher-search-icon" aria-hidden="true"></i>
                <input
                  v-model="appLauncherQuery"
                  type="search"
                  class="app-launcher-search"
                  placeholder="Find apps"
                  aria-label="Find apps"
                />
              </label>

              <ul class="app-launcher-grid" role="list">
                <li v-for="resource in filteredAppResources" :key="resource.key" class="app-launcher-grid-item">
                  <button
                    type="button"
                    class="app-launcher-tile"
                    :class="{ active: activeWorkspace === resource.key }"
                    @click="selectAppWorkspace(resource)"
                  >
                    <span class="app-launcher-tile-icon" aria-hidden="true">{{ resource.icon }}</span>
                    <span class="app-launcher-tile-label">{{ resource.label }}</span>
                  </button>
                </li>
              </ul>

              <p v-if="!filteredAppResources.length" class="meta">No apps match your search.</p>
            </div>
          </div>
        </div>

        <div
          ref="favoritesWrapRef"
          class="favorites-menu-wrap dropdown"
          :class="{ show: favoritesOpen }"
          @mouseenter="openFavoritesMenu"
          @mouseleave="closeFavoritesMenu"
        >
          <button
            type="button"
            class="topbar-mini-menu-trigger dropdown-toggle"
            :class="{ show: favoritesOpen }"
            aria-label="Favorites"
            title="Favorites"
            :aria-expanded="favoritesOpen ? 'true' : 'false'"
            @click.stop="toggleFavoritesPin"
          >
            <svg class="topbar-icon-glyph" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
              <path d="M12 3.8l2.5 5.1 5.6.8-4 3.9.9 5.5-5-2.6-5 2.6.9-5.5-4-3.9 5.6-.8z" fill="currentColor" />
            </svg>
          </button>

          <div class="topbar-mini-menu dropdown-menu" :class="{ show: favoritesOpen }" aria-label="Favorites menu">
            <p class="app-menu-title">Favorites</p>
            <ul v-if="topBarFavorites.length" class="app-menu-list">
              <li v-for="favorite in topBarFavorites" :key="favorite.id">
                <RouterLink class="app-menu-link dropdown-item" :to="favorite.to" @click="closeMenus">{{ favorite.label }}</RouterLink>
              </li>
            </ul>
            <p v-else class="meta">No favorites yet.</p>
          </div>
        </div>

        <div
          ref="recentsWrapRef"
          class="recents-menu-wrap dropdown"
          :class="{ show: recentsOpen }"
          @mouseenter="openRecentsMenu"
          @mouseleave="closeRecentsMenu"
        >
          <button
            type="button"
            class="topbar-mini-menu-trigger dropdown-toggle"
            :class="{ show: recentsOpen }"
            aria-label="Recents"
            title="Recents"
            :aria-expanded="recentsOpen ? 'true' : 'false'"
            @click.stop="toggleRecentsPin"
          >
            <svg class="topbar-icon-glyph" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
              <path d="M12 6.5a5.5 5.5 0 1 1-3.9 1.6" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" />
              <path d="M4.8 6.2h3.8v3.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M12 9v3.2l2.1 1.3" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>

          <div class="topbar-mini-menu dropdown-menu" :class="{ show: recentsOpen }" aria-label="Recents menu">
            <p class="app-menu-title">Recent Resources and Items</p>
            <ul v-if="topBarRecents.length" class="app-menu-list">
              <li v-for="recent in topBarRecents" :key="recent.id">
                <RouterLink class="app-menu-link dropdown-item" :to="recent.to" @click="closeMenus">{{ recent.label }}</RouterLink>
              </li>
            </ul>
            <p v-else class="meta">No recents yet.</p>
          </div>
        </div>
      </div>

      <div class="brand-cluster">
        <img class="brand-logo" :src="brandLogo" alt="IT-SoR logo" />
        <div class="brand-block">
          <strong class="brand-title">IT-SoR</strong>
          <span class="brand-subtitle">IT System of Record</span>
        </div>
      </div>
    </div>

    <div class="topbar-search">
      <div class="topbar-search-row">
        <form class="topbar-search-form" @submit.prevent="handleSearchSubmit">
          <div
            ref="searchWrapRef"
            class="topbar-search-input-wrap topbar-combobox"
            role="combobox"
            aria-haspopup="listbox"
            :aria-expanded="showSearchDropdown ? 'true' : 'false'"
            @mouseenter="openSearchDropdown"
            @mouseleave="closeSearchDropdown"
          >
            <div class="topbar-search-control">
              <input
                v-model="query"
                type="search"
                :placeholder="searchPlaceholder"
                @focus="pinSearchDropdown"
                @click="pinSearchDropdown"
              />
              <button
                type="submit"
                class="topbar-search-submit"
                :disabled="searching"
                :aria-label="searching ? 'Searching' : 'Search'"
              >
                <svg class="topbar-search-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                  <circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2" />
                  <path d="M16 16l4 4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" />
                </svg>
              </button>
            </div>

            <ul v-if="showSearchDropdown" class="search-dropdown" role="listbox">
              <li class="search-dropdown-section">
                <p class="search-dropdown-title">Object Types</p>
                <div class="search-type-chips">
                  <button
                    v-for="typeOption in searchTypeOptions"
                    :key="`popup-${typeOption.key}`"
                    type="button"
                    class="search-type-chip"
                    :class="{ active: searchTypeFilter === typeOption.key }"
                    @click="applySearchType(typeOption.key)"
                  >
                    {{ typeOption.label }}
                  </button>
                </div>
              </li>

              <template v-if="!query.trim().length">
                <li class="search-dropdown-section">
                  <p class="search-dropdown-title">Recent Searches</p>
                  <div v-if="recentSearchTerms.length" class="search-recents-list">
                    <button v-for="term in recentSearchTerms" :key="term" type="button" class="recent-search-btn" @click="useRecentSearch(term)">
                      {{ term }}
                    </button>
                  </div>
                  <p v-else class="search-dropdown-state">No recent searches yet.</p>
                </li>
              </template>

              <template v-else>
                <li v-if="searching" class="search-dropdown-state">Searching...</li>
                <li v-else-if="error" class="search-dropdown-state error">{{ error }}</li>
                <li v-else-if="!results.length" class="search-dropdown-state">No results found.</li>
                <li v-else v-for="item in results" :key="item.key">
                  <button type="button" class="search-result-btn" @click="navigateTo(item)">
                    <span class="search-result-leading">
                      <i class="pi" :class="item.iconClass" aria-hidden="true"></i>
                      <span class="meta search-result-type">{{ item.type }}</span>
                    </span>
                    <span class="search-result-name">{{ item.text }}</span>
                  </button>
                </li>
              </template>
            </ul>
          </div>
        </form>
      </div>
    </div>

    <div class="topbar-actions">
      <div
        ref="tenantContextWrapRef"
        class="tenant-context-wrap dropdown"
        :class="{ show: tenantContextOpen }"
        @mouseenter="openTenantContext"
        @mouseleave="closeTenantContext"
      >
        <button
          type="button"
          class="tenant-context-trigger dropdown-toggle"
          :class="{ show: tenantContextOpen }"
          aria-label="Tenant context"
          :title="activeTenantName"
          :aria-expanded="tenantContextOpen ? 'true' : 'false'"
          @click.stop="toggleTenantContextPin"
        >
          <svg class="topbar-icon-glyph tenant-context-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <path d="M5 21h14" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" />
            <path d="M6.5 21V7h11v14" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linejoin="round" />
            <path d="M10 11h1.5M12.5 11H14M10 14h1.5M12.5 14H14M11 21v-4h2v4" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" />
          </svg>
          <span class="topbar-trigger-label">{{ activeTenantName }}</span>
        </button>

        <div class="tenant-context-menu dropdown-menu dropdown-menu-end" :class="{ show: tenantContextOpen }" aria-label="Tenant context menu">
          <p class="app-menu-title">Tenant Context</p>
          <p class="meta mb-2">Active: {{ activeTenantName }}</p>

          <label class="tenant-context-search-label">
            <span class="visually-hidden">Search tenants</span>
            <input v-model="tenantSearchQuery" class="tenant-context-search" type="search" placeholder="Search recent tenants" />
          </label>

          <p v-if="tenantLoading" class="meta mb-2">Loading tenants...</p>
          <p v-else-if="!tenantSearchResults.length && !tenantSearchQuery.trim()" class="meta mb-2">No recent tenants yet.</p>

          <div v-else-if="tenantSearchResults.length" class="tenant-context-list">
            <button
              v-for="tenant in tenantSearchResults"
              :key="tenant.id"
              type="button"
              class="tenant-context-item"
              :class="{ active: String(tenant.id) === String(activeTenantId) }"
              @click="selectTenant(tenant.id)"
            >
              {{ tenant.name || tenant.id }}
            </button>
          </div>

          <div v-else-if="canCreateFromSearch" class="tenant-context-empty">
            <p class="meta mb-1">No recent tenant matched "{{ tenantSearchQuery.trim() }}".</p>
            <button type="button" class="tenant-flow-primary" :disabled="tenantCreating" @click="createTenantFromSearch">
              {{ tenantCreating ? 'Creating...' : `Create Tenant "${tenantSearchQuery.trim()}"` }}
            </button>
          </div>

          <div class="tenant-context-actions">
            <button type="button" class="tenant-action-btn" @click="openTenantsMasterView">Open Tenant Management</button>
          </div>

          <p v-if="tenantError" class="error topbar-error">{{ tenantError }}</p>
        </div>
      </div>

      <div
        ref="userMenuWrapRef"
        class="user-menu-wrap dropdown"
        :class="{ show: userMenuOpen }"
        @mouseenter="openUserMenu"
        @mouseleave="closeUserMenu"
      >
        <button
          type="button"
          class="user-menu-trigger dropdown-toggle"
          :class="{ show: userMenuOpen }"
          aria-label="User menu"
          :title="`${userDisplayName} · ${userOrg}`"
          :aria-expanded="userMenuOpen ? 'true' : 'false'"
          @click.stop="toggleUserMenuPin"
        >
          <svg class="topbar-icon-glyph user-menu-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <circle cx="12" cy="8" r="3.2" fill="none" stroke="currentColor" stroke-width="1.85" />
            <path d="M6.5 19.5a5.5 5.5 0 0 1 11 0" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" />
          </svg>
          <span class="topbar-trigger-label">{{ userDisplayName }}</span>
        </button>
        <div class="user-menu dropdown-menu dropdown-menu-end" :class="{ show: userMenuOpen }" aria-label="User account menu">
          <RouterLink class="user-menu-link dropdown-item" to="/auth/users/me" @click="closeMenus">My Profile</RouterLink>
          <RouterLink class="user-menu-link dropdown-item" to="/logout" @click="closeMenus">Sign Out</RouterLink>
        </div>
      </div>
    </div>
  </header>
</template>
