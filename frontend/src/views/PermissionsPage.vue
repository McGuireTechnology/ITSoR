<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { createPermission, listPermissions } from '../lib/api'

const route = useRoute()
const router = useRouter()

const rows = ref([])
const loading = ref(true)
const creating = ref(false)
const error = ref('')
const sortKey = ref('name')
const sortDir = ref('asc')
const selectedIds = ref([])
const name = ref('')
const resource = ref('')
const action = ref('read')

const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'resource', label: 'Resource', sortable: true },
  { key: 'action', label: 'Action', sortable: true },
  { key: 'id', label: 'Permission ID', sortable: false },
]

async function loadRows() {
  loading.value = true
  error.value = ''
  try {
    rows.value = await listPermissions()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  creating.value = true
  error.value = ''
  try {
    const created = await createPermission({
      name: name.value.trim(),
      resource: resource.value.trim(),
      action: action.value.trim(),
    })
    rows.value = [...rows.value, created]
    name.value = ''
    resource.value = ''
    action.value = 'read'
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

const visibleRows = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = rows.value
  if (query) {
    filtered = rows.value.filter((row) => `${row.name || ''} ${row.resource || ''} ${row.action || ''} ${row.id || ''}`.toLowerCase().includes(query))
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

function openRow(row) {
  router.push(`/auth/permissions/${row.id}`)
}

onMounted(loadRows)
</script>

<template>
  <section class="users-page">
    <form class="form section-gap" @submit.prevent="handleCreate">
      <label>
        Name
        <input v-model="name" type="text" required />
      </label>
      <label>
        Resource
        <input v-model="resource" type="text" required />
      </label>
      <label>
        Action
        <input v-model="action" type="text" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Permission' }}
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
        @row-open="openRow"
      >
        <template #row-actions="{ row }">
          <button class="btn btn-sm btn-primary" type="button" @click="openRow(row)">Open</button>
        </template>
      </DataTable>
    </div>
  </section>
</template>
