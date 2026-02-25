<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  listEntityRecords,
  listEntityTypes,
  listGroups,
  listNamespaces,
  listTenants,
  listUsers,
  listWorkspaces,
} from '../lib/api'

const route = useRoute()

const items = ref([])
const loading = ref(false)
const error = ref('')
const filterText = ref('')
const page = ref(1)
const pageSize = 12

const domainConfig = {
  users: {
    label: 'Users',
    list: () => listUsers(),
    to: (item) => `/users/${item.id}`,
    text: (item) => item.username || item.email || item.id,
  },
  tenants: {
    label: 'Tenants',
    list: () => listTenants(),
    to: (item) => `/tenants/${item.id}`,
    text: (item) => item.name,
  },
  groups: {
    label: 'Groups',
    list: () => listGroups(),
    to: (item) => `/groups/${item.id}`,
    text: (item) => item.name,
  },
  workspaces: {
    label: 'Workspaces',
    list: () => listWorkspaces(),
    to: (item) => `/workspaces/${item.id}`,
    text: (item) => item.name,
  },
  namespaces: {
    label: 'Namespaces',
    list: () => listNamespaces(),
    to: (item) => `/namespaces/${item.id}`,
    text: (item) => item.name,
  },
  'entity-types': {
    label: 'Entity Types',
    list: () => listEntityTypes(),
    to: (item) => `/entity-types/${item.id}`,
    text: (item) => item.name,
  },
  'entity-records': {
    label: 'Entity Records',
    list: () => listEntityRecords(),
    to: (item) => `/entity-records/${item.id}`,
    text: (item) => item.name || '(unnamed)',
  },
}

const currentDomain = computed(() => route.meta.domain)
const currentConfig = computed(() => domainConfig[currentDomain.value] || null)
const routeQueryFilter = computed(() => String(route.query.q || '').trim().toLowerCase())

const filteredItems = computed(() => {
  const term = (filterText.value || routeQueryFilter.value || '').toLowerCase()
  if (!term) {
    return items.value
  }
  return items.value.filter((item) =>
    String(currentConfig.value?.text(item) || '')
      .toLowerCase()
      .includes(term),
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredItems.value.length / pageSize)))

const pagedItems = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredItems.value.slice(start, start + pageSize)
})

async function loadItems() {
  if (!currentConfig.value) {
    items.value = []
    error.value = ''
    return
  }

  loading.value = true
  error.value = ''
  try {
    const data = await currentConfig.value.list()
    items.value = Array.isArray(data) ? data : []
    page.value = 1
  } catch (loadError) {
    items.value = []
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadItems)

watch(
  () => currentDomain.value,
  () => {
    loadItems()
  },
)

watch(routeQueryFilter, (value) => {
  filterText.value = value
  page.value = 1
})

function previousPage() {
  page.value = Math.max(1, page.value - 1)
}

function nextPage() {
  page.value = Math.min(totalPages.value, page.value + 1)
}
</script>

<template>
  <div class="section-nav-body">
    <h3>{{ currentConfig?.label || 'Section' }}</h3>
    <div class="section-toolbar">
      <input v-model="filterText" type="search" placeholder="Filter list" />
      <button type="button" @click="loadItems">Refresh</button>
    </div>
    <p v-if="loading" class="meta">Loading…</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="!filteredItems.length" class="meta">No items</p>

    <ul v-else class="section-list">
      <li v-for="item in pagedItems" :key="item.id">
        <RouterLink :to="currentConfig.to(item)">{{ currentConfig.text(item) }}</RouterLink>
      </li>
    </ul>

    <div v-if="filteredItems.length" class="section-pagination">
      <button type="button" :disabled="page <= 1" @click="previousPage">Prev</button>
      <span class="meta">Page {{ page }} / {{ totalPages }}</span>
      <button type="button" :disabled="page >= totalPages" @click="nextPage">Next</button>
    </div>
  </div>
</template>
