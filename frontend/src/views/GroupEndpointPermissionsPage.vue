<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { createEndpointPermission, deleteEndpointPermission, listEndpointPermissions } from '../lib/api'
import { markPermissionsDirty, useDomainPermissions } from '../lib/permissions'

const route = useRoute()
const router = useRouter()
const permissionDomain = ref('endpoint-permissions')
const { canWrite } = useDomainPermissions(permissionDomain)

const rows = ref([])
const loading = ref(true)
const creating = ref(false)
const deletingId = ref('')
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('endpoint_name')
const sortDir = ref('asc')
const endpointName = ref('')
const action = ref('read')

const columns = [
  { key: 'endpoint_name', label: 'Endpoint', sortable: true },
  { key: 'action', label: 'Action', sortable: true },
  { key: 'id', label: 'Permission ID', sortable: false },
]

const visibleRows = computed(() => {
  return [...rows.value].sort((left, right) => {
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

async function loadRows() {
  loading.value = true
  error.value = ''
  try {
    rows.value = await listEndpointPermissions({
      principalType: 'group',
      principalId: String(route.params.id || ''),
    })
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  if (!canWrite.value) {
    return
  }

  creating.value = true
  error.value = ''
  try {
    const created = await createEndpointPermission({
      principal_type: 'group',
      principal_id: String(route.params.id || ''),
      endpoint_name: endpointName.value.trim(),
      action: action.value.trim(),
    })
    rows.value = [...rows.value, created]
    endpointName.value = ''
    action.value = 'read'
    markPermissionsDirty()
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

async function handleDelete(row) {
  if (!canWrite.value) {
    return
  }

  deletingId.value = String(row.id)
  error.value = ''
  try {
    await deleteEndpointPermission(row.id)
    rows.value = rows.value.filter((item) => String(item.id) !== String(row.id))
    selectedIds.value = selectedIds.value.filter((id) => String(id) !== String(row.id))
    markPermissionsDirty()
  } catch (deleteError) {
    error.value = deleteError.message
  } finally {
    deletingId.value = ''
  }
}

function openPermission(row) {
  router.push(`/platform/endpoint-permissions/${row.id}`)
}

onMounted(loadRows)
watch(() => route.params.id, loadRows)
</script>

<template>
  <section class="users-page">
    <form v-if="canWrite" class="form section-gap" @submit.prevent="handleCreate">
      <label>
        Endpoint Name
        <input v-model="endpointName" type="text" required />
      </label>
      <label>
        Action
        <input v-model="action" type="text" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Adding...' : 'Add Permission' }}
      </button>
    </form>

    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleRows"
        :loading="loading"
        :error="error"
        :sort-key="sortKey"
        :sort-dir="sortDir"
        :selected-ids="selectedIds"
        @sort-change="handleSortChange"
        @selection-change="selectedIds = $event"
        @row-open="openPermission"
      >
        <template #row-actions="{ row }">
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-primary" type="button" @click="openPermission(row)">Open</button>
            <button
              v-if="canWrite"
              class="btn btn-sm btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white"
              type="button"
              :disabled="deletingId === String(row.id)"
              @click="handleDelete(row)"
            >
              {{ deletingId === String(row.id) ? 'Removing...' : 'Remove' }}
            </button>
          </div>
        </template>
      </DataTable>
    </div>
  </section>
</template>
