<script setup>
import { ref } from 'vue'
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

const router = useRouter()
const tenantLabel = import.meta.env.VITE_TENANT_NAME || 'Default Tenant'

const query = ref('')
const searching = ref(false)
const error = ref('')
const results = ref([])

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

    pushResults(users, 'User', (item) => item.username || item.email || item.id, (item) => `/users/${item.id}`, term)
    pushResults(tenants, 'Tenant', (item) => item.name, (item) => `/tenants/${item.id}`, term)
    pushResults(groups, 'Group', (item) => item.name, (item) => `/groups/${item.id}`, term)
    pushResults(workspaces, 'Workspace', (item) => item.name, (item) => `/workspaces/${item.id}`, term)
    pushResults(namespaces, 'Namespace', (item) => item.name, (item) => `/namespaces/${item.id}`, term)
    pushResults(entityTypes, 'Entity Type', (item) => item.name, (item) => `/entity-types/${item.id}`, term)
    pushResults(entityRecords, 'Entity Record', (item) => item.name || '(unnamed)', (item) => `/entity-records/${item.id}`, term)

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
</script>

<template>
  <header class="top-bar">
    <div class="topbar-left">
      <button type="button" class="icon-button" aria-label="App launcher">☰</button>
      <strong>ITSoR admin center</strong>
      <span class="tenant-pill">{{ tenantLabel }}</span>
    </div>

    <div class="topbar-search">
      <form class="topbar-search-form" @submit.prevent="runGlobalSearch">
        <input
          v-model="query"
          type="search"
          placeholder="Search resources, objects, and docs"
        />
        <button type="submit" :disabled="searching">{{ searching ? 'Searching…' : 'Search' }}</button>
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
      <button type="button" class="icon-button" aria-label="Notifications">🔔</button>
      <button type="button" class="icon-button" aria-label="Settings">⚙</button>
      <button type="button" class="icon-button" aria-label="Help">?</button>
      <button type="button" class="icon-button" aria-label="Feedback">✎</button>
      <RouterLink to="/users/me">Profile</RouterLink>
    </div>
  </header>
</template>
