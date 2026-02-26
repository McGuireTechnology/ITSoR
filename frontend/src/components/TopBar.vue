<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  listEntityRecords,
  listEntityTypes,
  listGroups,
  listNamespaces,
  listTenants,
  listUsers,
  listWorkspaces,
} from '../lib/api'
import { formatNameId } from '../lib/formatters'
import brandLogo from '../assets/itsor-cube-logo.svg'

const router = useRouter()
const tenantLabel = import.meta.env.VITE_TENANT_NAME || 'Default Tenant'
const userDisplayName = import.meta.env.VITE_USER_DISPLAY_NAME || 'Signed-in user'
const userOrg = import.meta.env.VITE_USER_ORG || 'ITSoR Tenant'
const appMenuOpen = ref(false)
const userMenuOpen = ref(false)

const appResources = [
  { label: 'Users', to: '/users' },
  { label: 'Groups', to: '/groups' },
  { label: 'Tenants', to: '/tenants' },
  { label: 'Workspaces', to: '/workspaces' },
]

const query = ref('')
const searching = ref(false)
const error = ref('')
const results = ref([])
const appLauncherButtonRef = ref(null)
const appMenuRef = ref(null)
const userMenuButtonRef = ref(null)
const userMenuRef = ref(null)

function getFocusableElements(container) {
  if (!(container instanceof HTMLElement)) {
    return []
  }

  return Array.from(
    container.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'),
  ).filter((element) => element instanceof HTMLElement && !element.hasAttribute('disabled'))
}

function focusFirstInMenu(menuRef) {
  const focusable = getFocusableElements(menuRef?.value)
  if (focusable.length > 0) {
    focusable[0].focus()
  }
}

function closeAppMenu(returnFocus = false) {
  appMenuOpen.value = false
  if (returnFocus) {
    appLauncherButtonRef.value?.focus()
  }
}

function closeUserMenu(returnFocus = false) {
  userMenuOpen.value = false
  if (returnFocus) {
    userMenuButtonRef.value?.focus()
  }
}

function toggleAppMenu() {
  const next = !appMenuOpen.value
  appMenuOpen.value = next

  if (next) {
    userMenuOpen.value = false
    requestAnimationFrame(() => {
      focusFirstInMenu(appMenuRef)
    })
  }
}

function handleDocumentClick(event) {
  if (!(event.target instanceof Element)) {
    return
  }
  if (!event.target.closest('.app-launcher-wrap')) {
    closeAppMenu()
  }
  if (!event.target.closest('.user-menu-wrap')) {
    closeUserMenu()
  }
}

function toggleUserMenu() {
  const next = !userMenuOpen.value
  userMenuOpen.value = next

  if (next) {
    appMenuOpen.value = false
    requestAnimationFrame(() => {
      focusFirstInMenu(userMenuRef)
    })
  }
}

function trapTabWithinMenu(event, menuRef) {
  if (event.key !== 'Tab') {
    return false
  }

  const focusable = getFocusableElements(menuRef?.value)
  if (focusable.length === 0) {
    return false
  }

  const first = focusable[0]
  const last = focusable[focusable.length - 1]
  const active = document.activeElement

  if (event.shiftKey && active === first) {
    event.preventDefault()
    last.focus()
    return true
  }

  if (!event.shiftKey && active === last) {
    event.preventDefault()
    first.focus()
    return true
  }

  return false
}

function handleArrowNavigationWithinMenu(event, menuRef) {
  const key = event.key
  if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(key)) {
    return false
  }

  const focusable = getFocusableElements(menuRef?.value)
  if (focusable.length === 0) {
    return false
  }

  const currentIndex = focusable.findIndex((element) => element === document.activeElement)
  let nextIndex = currentIndex

  if (key === 'Home') {
    nextIndex = 0
  } else if (key === 'End') {
    nextIndex = focusable.length - 1
  } else if (key === 'ArrowDown') {
    nextIndex = currentIndex < 0 ? 0 : (currentIndex + 1) % focusable.length
  } else if (key === 'ArrowUp') {
    nextIndex = currentIndex < 0 ? focusable.length - 1 : (currentIndex - 1 + focusable.length) % focusable.length
  }

  event.preventDefault()
  focusable[nextIndex].focus()
  return true
}

function handleDocumentKeydown(event) {
  if (event.key === 'Escape') {
    if (userMenuOpen.value) {
      event.preventDefault()
      closeUserMenu(true)
      return
    }

    if (appMenuOpen.value) {
      event.preventDefault()
      closeAppMenu(true)
      return
    }
  }

  if (userMenuOpen.value) {
    if (handleArrowNavigationWithinMenu(event, userMenuRef)) {
      return
    }
    trapTabWithinMenu(event, userMenuRef)
    return
  }

  if (appMenuOpen.value) {
    if (handleArrowNavigationWithinMenu(event, appMenuRef)) {
      return
    }
    trapTabWithinMenu(event, appMenuRef)
  }
}

function matches(value, term) {
  return String(value || '').toLowerCase().includes(term)
}

function pushResults(collection, type, getText, getRoute, term) {
  for (const item of collection || []) {
    const text = getText(item)
    if (matches(text, term)) {
      results.value.push({
        key: `${type}:${item.id}`,
        type,
        text,
        to: getRoute(item),
      })
    }
  }
}

async function runGlobalSearch() {
  const term = query.value.trim().toLowerCase()
  results.value = []
  error.value = ''

  if (!term) {
    return
  }

  searching.value = true
  try {
    const [users, tenants, groups, workspaces, namespaces, entityTypes, entityRecords] = await Promise.all([
      listUsers(),
      listTenants(),
      listGroups(),
      listWorkspaces(),
      listNamespaces(),
      listEntityTypes(),
      listEntityRecords(),
    ])

    pushResults(users, 'User', (item) => formatNameId(item.username || item.email, item.id, '(unnamed user)'), (item) => `/users/${item.id}`, term)
    pushResults(tenants, 'Tenant', (item) => formatNameId(item.name, item.id, '(unnamed tenant)'), (item) => `/tenants/${item.id}`, term)
    pushResults(groups, 'Group', (item) => formatNameId(item.name, item.id, '(unnamed group)'), (item) => `/groups/${item.id}`, term)
    pushResults(workspaces, 'Workspace', (item) => formatNameId(item.name, item.id, '(unnamed workspace)'), (item) => `/workspaces/${item.id}`, term)
    pushResults(namespaces, 'Namespace', (item) => formatNameId(item.name, item.id, '(unnamed namespace)'), (item) => `/namespaces/${item.id}`, term)
    pushResults(entityTypes, 'Entity Type', (item) => formatNameId(item.name, item.id, '(unnamed entity type)'), (item) => `/entity-types/${item.id}`, term)
    pushResults(entityRecords, 'Entity Record', (item) => formatNameId(item.name, item.id, '(unnamed)'), (item) => `/entity-records/${item.id}`, term)

    results.value = results.value.slice(0, 12)
  } catch (searchError) {
    error.value = searchError.message
  } finally {
    searching.value = false
  }
}

async function navigateTo(item) {
  await router.push(item.to)
  results.value = []
}

async function openAppResource(resource) {
  closeAppMenu()
  await router.push(resource.to)
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
  document.addEventListener('keydown', handleDocumentKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick)
  document.removeEventListener('keydown', handleDocumentKeydown)
})
</script>

<template>
  <header class="top-bar bg-brand-deep text-primary-foreground border-brand-purple">
    <div class="topbar-left">
      <div class="app-launcher-wrap">
        <button
          ref="appLauncherButtonRef"
          type="button"
          class="icon-button app-launcher"
          aria-label="App launcher"
          aria-haspopup="menu"
          :aria-expanded="appMenuOpen"
          aria-controls="topbar-app-menu"
          @click="toggleAppMenu"
        >
          <span class="waffle-icon" aria-hidden="true">
            <span v-for="dot in 9" :key="dot" class="waffle-dot" />
          </span>
        </button>
        <div v-if="appMenuOpen" id="topbar-app-menu" ref="appMenuRef" class="app-menu" role="menu">
          <p class="app-menu-title">Apps</p>
          <ul class="app-menu-list">
            <li v-for="resource in appResources" :key="resource.to">
              <button type="button" class="app-menu-link" role="menuitem" @click="openAppResource(resource)">{{ resource.label }}</button>
            </li>
          </ul>
          <div class="app-menu-favorites">
            <p class="app-menu-title">Favorites</p>
            <p class="meta">No favorites yet.</p>
          </div>
        </div>
      </div>
      <img class="brand-logo" :src="brandLogo" alt="IT-SoR logo" />
      <div class="brand-block">
        <strong class="brand-title">IT-SoR</strong>
        <span class="brand-subtitle">IT System of Record</span>
      </div>
      <span class="tenant-pill bg-brand-purple text-primary-foreground">{{ tenantLabel }}</span>
    </div>

    <div class="topbar-search">
      <form class="topbar-search-form" @submit.prevent="runGlobalSearch">
        <input
          v-model="query"
          type="search"
          placeholder="Search resources, services, and docs"
        />
        <button
          type="submit"
          class="bg-primary text-primary-foreground border-0 hover:bg-accent"
          :disabled="searching"
        >
          {{ searching ? 'Searching…' : 'Search' }}
        </button>
      </form>
      <p v-if="error" class="error topbar-error">{{ error }}</p>
      <ul v-if="results.length" class="search-results">
        <li v-for="item in results" :key="item.key">
          <button type="button" class="search-result-btn" @click="navigateTo(item)">
            <span class="meta">{{ item.type }}</span>
            <span>{{ item.text }}</span>
          </button>
        </li>
      </ul>
    </div>

    <div class="topbar-actions">
      <button type="button" class="icon-button border-brand-purple/50" aria-label="Notifications">🔔</button>
      <button type="button" class="icon-button border-brand-purple/50" aria-label="Settings">⚙</button>
      <button type="button" class="icon-button border-brand-purple/50" aria-label="Help">?</button>

      <div class="user-menu-wrap">
        <button
          ref="userMenuButtonRef"
          type="button"
          class="user-menu-trigger"
          aria-haspopup="menu"
          :aria-expanded="userMenuOpen"
          aria-controls="topbar-user-menu"
          @click="toggleUserMenu"
        >
          <span class="profile-name">{{ userDisplayName }}</span>
          <span class="profile-org">{{ userOrg }}</span>
          <span aria-hidden="true">▾</span>
        </button>
        <div v-if="userMenuOpen" id="topbar-user-menu" ref="userMenuRef" class="user-menu" role="menu">
          <RouterLink class="user-menu-link" role="menuitem" to="/users/me" @click="closeUserMenu()">My Account</RouterLink>
          <RouterLink class="user-menu-link" role="menuitem" to="/logout" @click="closeUserMenu()">Sign out</RouterLink>
        </div>
      </div>
    </div>
  </header>
</template>
