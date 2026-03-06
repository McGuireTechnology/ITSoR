<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listTenants } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'
import { inspectorState, openTenantEditInspector } from '../lib/inspectorActions'

const TENANT_STORAGE_KEY = 'itsor.activeTenantId'
const TENANT_CONTEXT_CHANGED_EVENT = 'itsor:tenant-context-changed'

const route = useRoute()
const router = useRouter()

const tenants = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('name')
const sortDir = ref('asc')
const currentTenantContextId = ref('')

const columns = [
  { key: 'name', label: 'Tenant Name', sortable: true },
  { key: 'id', label: 'Tenant ID', sortable: false },
]

async function loadTenants() {
  loading.value = true
  error.value = ''
  try {
    tenants.value = await listTenants()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

const visibleTenants = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = tenants.value

  if (query) {
    filtered = tenants.value.filter((tenant) =>
      `${tenant.name || ''} ${tenant.id || ''}`.toLowerCase().includes(query),
    )
  }
  return [...filtered].sort((left, right) => {
    const leftValue = String(left[sortKey.value] || '').toLowerCase()
    const rightValue = String(right[sortKey.value] || '').toLowerCase()
    if (leftValue === rightValue) {
      return 0
    }
    const result = leftValue > rightValue ? 1 : -1
    return sortDir.value === 'asc' ? result : -result
  })
})

function handleSortChange(nextKey) {
  if (sortKey.value === nextKey) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
    return
  }
  sortKey.value = nextKey
  sortDir.value = 'asc'
}

function navigateToTenant(tenant) {
  router.push(`/auth/tenants/${tenant.id}`)
}

function editTenantInline(tenant) {
  openTenantEditInspector(tenant.id)
}

function setTenantContext(tenant) {
  const tenantId = String(tenant?.id || '')
  if (!tenantId || typeof window === 'undefined') {
    return
  }

  currentTenantContextId.value = tenantId
  window.localStorage.setItem(TENANT_STORAGE_KEY, tenantId)
  window.dispatchEvent(new CustomEvent(TENANT_CONTEXT_CHANGED_EVENT, { detail: { tenantId } }))
}

function syncCurrentTenantContext() {
  if (typeof window === 'undefined') {
    return
  }

  currentTenantContextId.value = String(window.localStorage.getItem(TENANT_STORAGE_KEY) || '')
}

function handleTenantContextChanged(event) {
  const nextTenantId = String(event?.detail?.tenantId || '').trim()
  currentTenantContextId.value = nextTenantId
}

onMounted(() => {
  syncCurrentTenantContext()
  loadTenants()
  window.addEventListener(TENANT_CONTEXT_CHANGED_EVENT, handleTenantContextChanged)
  window.addEventListener('storage', syncCurrentTenantContext)
})

watch(
  [visibleTenants, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleTenants.value.length,
      selected: selectedIds.value.length,
      selectedIds: selectedIds.value,
      noun: 'tenants',
    })
  },
  { immediate: true },
)

onUnmounted(() => {
  clearCommandSurfaceMetrics()
  if (typeof window !== 'undefined') {
    window.removeEventListener(TENANT_CONTEXT_CHANGED_EVENT, handleTenantContextChanged)
    window.removeEventListener('storage', syncCurrentTenantContext)
  }
})

watch(
  () => route.query._refresh,
  () => {
    loadTenants()
  },
)

watch(
  () => inspectorState.tenantsRefreshTick,
  () => {
    loadTenants()
  },
)
</script>

<template>
  <section class="users-page">
    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleTenants"
        :loading="loading"
        :error="error"
        :sort-key="sortKey"
        :sort-dir="sortDir"
        :selected-ids="selectedIds"
        @sort-change="handleSortChange"
        @selection-change="selectedIds = $event"
        @row-open="navigateToTenant"
      >
        <template #row-actions="{ row }">
          <div class="d-flex gap-2">
            <button
              class="btn btn-sm btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white"
              type="button"
              @click="editTenantInline(row)"
            >
              ✎
            </button>
            <button
              v-if="String(row.id) === currentTenantContextId"
              class="btn btn-sm btn-outline-secondary"
              type="button"
              title="Current Tenant Context"
              aria-label="Current Tenant Context"
              disabled
            >
              <i class="pi pi-crown" aria-hidden="true"></i>
            </button>
            <button
              v-else
              class="btn btn-sm btn-outline-secondary"
              type="button"
              title="Set Tenant Context"
              aria-label="Set Tenant Context"
              @click="setTenantContext(row)"
            >
              <i class="pi pi-sign-in" aria-hidden="true"></i>
            </button>
            <button
              class="btn btn-sm btn-primary"
              type="button"
              title="Open Tenant Details"
              aria-label="Open Tenant Details"
              @click="navigateToTenant(row)"
            >
              <i class="pi pi-external-link" aria-hidden="true"></i>
            </button>
          </div>
        </template>
      </DataTable>
    </div>
  </section>
</template>
