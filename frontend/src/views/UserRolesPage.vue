<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { createUserRole, deleteUserRole, listUserRoles } from '../lib/api'

const route = useRoute()
const rows = ref([])
const loading = ref(true)
const creating = ref(false)
const deletingId = ref('')
const error = ref('')
const roleId = ref('')
const selectedIds = ref([])
const sortKey = ref('role_id')
const sortDir = ref('asc')

const columns = [
  { key: 'role_id', label: 'Role ID', sortable: true },
  { key: 'id', label: 'Link ID', sortable: false },
]

const visibleRows = computed(() => {
  const userId = String(route.params.id || '')
  return [...rows.value]
    .filter((row) => String(row.user_id) === userId)
    .sort((left, right) => {
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
    rows.value = await listUserRoles()
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
    const created = await createUserRole({
      user_id: String(route.params.id || ''),
      role_id: roleId.value.trim(),
    })
    rows.value = [...rows.value, created]
    roleId.value = ''
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

async function handleDelete(row) {
  deletingId.value = String(row.id)
  error.value = ''
  try {
    await deleteUserRole(row.id)
    rows.value = rows.value.filter((item) => String(item.id) !== String(row.id))
  } catch (deleteError) {
    error.value = deleteError.message
  } finally {
    deletingId.value = ''
  }
}

onMounted(loadRows)
watch(() => route.params.id, loadRows)
</script>

<template>
  <section class="users-page">
    <form class="form section-gap" @submit.prevent="handleCreate">
      <label>
        Role ID
        <input v-model="roleId" type="text" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Adding...' : 'Add User Role' }}
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
      >
        <template #row-actions="{ row }">
          <button class="btn btn-sm btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="deletingId === String(row.id)" @click="handleDelete(row)">
            {{ deletingId === String(row.id) ? 'Removing...' : 'Remove' }}
          </button>
        </template>
      </DataTable>
    </div>
  </section>
</template>
