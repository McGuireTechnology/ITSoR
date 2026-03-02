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

const appResources = [
  { label: 'Users', to: '/platform/users' },
  { label: 'Groups', to: '/platform/groups' },
  { label: 'Tenants', to: '/platform/tenants' },
  { label: 'Workspaces', to: '/customization/workspaces' },
]

const query = ref('')
const searching = ref(false)
const error = ref('')
const results = ref([])
const appLauncherWrapRef = ref(null)
const userMenuWrapRef = ref(null)
const appLauncherOpen = ref(false)
const userMenuOpen = ref(false)

function closeMenus() {
  appLauncherOpen.value = false
  userMenuOpen.value = false
}

function openAppLauncher() {
  appLauncherOpen.value = true
  userMenuOpen.value = false
}

function closeAppLauncher() {
  appLauncherOpen.value = false
}

function openUserMenu() {
  userMenuOpen.value = true
  appLauncherOpen.value = false
}

function closeUserMenu() {
  userMenuOpen.value = false
}

function handleDocumentClick(event) {
  const appWrap = appLauncherWrapRef.value
  const userWrap = userMenuWrapRef.value
  const target = event.target

  if (appWrap && appWrap.contains(target)) {
    return
  }

  if (userWrap && userWrap.contains(target)) {
    return
  }

  closeMenus()
}

function handleEscape(event) {
  if (event.key === 'Escape') {
    closeMenus()
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

    pushResults(users, 'User', (item) => formatNameId(item.username || item.email, item.id, '(unnamed user)'), (item) => `/platform/users/${item.id}`, term)
    pushResults(tenants, 'Tenant', (item) => formatNameId(item.name, item.id, '(unnamed tenant)'), (item) => `/platform/tenants/${item.id}`, term)
    pushResults(groups, 'Group', (item) => formatNameId(item.name, item.id, '(unnamed group)'), (item) => `/platform/groups/${item.id}`, term)
    pushResults(workspaces, 'Workspace', (item) => formatNameId(item.name, item.id, '(unnamed workspace)'), (item) => `/customization/workspaces/${item.id}`, term)
    pushResults(namespaces, 'Namespace', (item) => formatNameId(item.name, item.id, '(unnamed namespace)'), (item) => `/customization/namespaces/${item.id}`, term)
    pushResults(entityTypes, 'Entity Type', (item) => formatNameId(item.name, item.id, '(unnamed entity type)'), (item) => `/customization/entity-types/${item.id}`, term)
    pushResults(entityRecords, 'Entity Record', (item) => formatNameId(item.name, item.id, '(unnamed)'), (item) => `/customization/entity-records/${item.id}`, term)

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
  closeMenus()
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick)
  document.removeEventListener('keydown', handleEscape)
})

</script>

<template>
  <header class="top-bar bg-brand-deep text-primary-foreground border-brand-purple">
    <div class="topbar-left">
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
        >
          <svg class="app-drawer-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
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
        <div class="app-menu dropdown-menu" :class="{ show: appLauncherOpen }" aria-label="App launcher menu">
          <p class="app-menu-title">Apps</p>
          <ul class="app-menu-list">
            <li v-for="resource in appResources" :key="resource.to">
              <RouterLink class="app-menu-link dropdown-item" :to="resource.to" @click="closeMenus">{{ resource.label }}</RouterLink>
            </li>
          </ul>
          <div class="app-menu-favorites">
            <p class="app-menu-title">Favorites</p>
            <p class="meta">No favorites yet.</p>
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
        <span class="tenant-pill bg-brand-purple text-primary-foreground">{{ tenantLabel }}</span>
      </div>
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
          :aria-expanded="userMenuOpen ? 'true' : 'false'"
        >
          <span class="profile-name">{{ userDisplayName }}</span>
          <span class="profile-org">{{ userOrg }}</span>
        </button>
        <div class="user-menu dropdown-menu dropdown-menu-end" :class="{ show: userMenuOpen }" aria-label="User account menu">
          <RouterLink class="user-menu-link dropdown-item" to="/platform/users/me" @click="closeMenus">My Account</RouterLink>
          <RouterLink class="user-menu-link dropdown-item" to="/logout" @click="closeMenus">Sign out</RouterLink>
        </div>
      </div>
    </div>
  </header>
</template>
