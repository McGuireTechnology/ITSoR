<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listTenants } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'
import { inspectorState, openTenantEditInspector } from '../lib/inspectorActions'

const route = useRoute()
const router = useRouter()

const tenants = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('name')
const sortDir = ref('asc')

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
  router.push(`/platform/tenants/${tenant.id}`)
}

function editTenantInline(tenant) {
  openTenantEditInspector(tenant.id)
}

onMounted(loadTenants)

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
            <button class="btn btn-sm btn-primary" type="button" @click="navigateToTenant(row)">Open</button>
          </div>
        </template>
      </DataTable>
    </div>
  </section>
</template>
