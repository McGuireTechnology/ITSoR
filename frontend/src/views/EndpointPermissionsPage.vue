<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { createEndpointPermission, listEndpointPermissions } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'
import { markPermissionsDirty, useDomainPermissions } from '../lib/permissions'

const route = useRoute()
const router = useRouter()
const domain = ref('endpoint-permissions')
const { canWrite } = useDomainPermissions(domain)

const endpointPermissions = ref([])
const loading = ref(true)
const error = ref('')
const creating = ref(false)
const principalType = ref('user')
const principalId = ref('')
const endpointName = ref('')
const action = ref('read')
const selectedIds = ref([])
const sortKey = ref('endpoint_name')
const sortDir = ref('asc')

const columns = [
  { key: 'endpoint_name', label: 'Endpoint', sortable: true },
  { key: 'action', label: 'Action', sortable: true },
  { key: 'principal_type', label: 'Principal Type', sortable: true },
  { key: 'principal_id', label: 'Principal ID', sortable: true },
  { key: 'id', label: 'Permission ID', sortable: false },
]

async function loadEndpointPermissions() {
  loading.value = true
  error.value = ''
  try {
    endpointPermissions.value = await listEndpointPermissions()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateEndpointPermission() {
  if (!canWrite.value) {
    return
  }

  creating.value = true
  error.value = ''
  try {
    const created = await createEndpointPermission({
      principal_type: principalType.value,
      principal_id: principalId.value.trim(),
      endpoint_name: endpointName.value.trim(),
      action: action.value.trim(),
    })
    endpointPermissions.value = [...endpointPermissions.value, created]
    principalId.value = ''
    endpointName.value = ''
    action.value = 'read'
    markPermissionsDirty()
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

const visibleEndpointPermissions = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = endpointPermissions.value

  if (query) {
    filtered = endpointPermissions.value.filter((permission) =>
      `${permission.endpoint_name || ''} ${permission.action || ''} ${permission.principal_type || ''} ${permission.principal_id || ''} ${permission.id || ''}`
        .toLowerCase()
        .includes(query),
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

function navigateToEndpointPermission(permission) {
  router.push(`/auth/endpoint-permissions/${permission.id}`)
}

onMounted(loadEndpointPermissions)

watch(
  [visibleEndpointPermissions, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleEndpointPermissions.value.length,
      selected: selectedIds.value.length,
      noun: 'endpoint permissions',
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
    loadEndpointPermissions()
  },
)
</script>

<template>
  <section class="users-page">
    <form v-if="canWrite" class="form section-gap" @submit.prevent="handleCreateEndpointPermission">
      <label>
        Principal Type
        <select v-model="principalType" required>
          <option value="user">user</option>
          <option value="group">group</option>
        </select>
      </label>
      <label>
        Principal ID
        <input v-model="principalId" type="text" required />
      </label>
      <label>
        Endpoint Name
        <input v-model="endpointName" type="text" required />
      </label>
      <label>
        Action
        <input v-model="action" type="text" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Endpoint Permission' }}
      </button>
    </form>

    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleEndpointPermissions"
        :loading="loading"
        :error="error"
        :sort-key="sortKey"
        :sort-dir="sortDir"
        :selected-ids="selectedIds"
        @sort-change="handleSortChange"
        @selection-change="selectedIds = $event"
        @row-open="navigateToEndpointPermission"
      >
        <template #row-actions="{ row }">
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-primary" type="button" @click="navigateToEndpointPermission(row)">Open</button>
          </div>
        </template>
      </DataTable>
    </div>
  </section>
</template>
