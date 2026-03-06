<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listUsers } from '../lib/api'

const route = useRoute()
const router = useRouter()

const users = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('username')
const sortDir = ref('asc')

const columns = [
  { key: 'username', label: 'Username', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'id', label: 'User ID', sortable: false },
]

const visibleUsers = computed(() => {
  const groupId = String(route.params.id || '')
  return users.value
    .filter((user) => String(user.group_id || '') === groupId)
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

function openUser(user) {
  router.push(`/auth/users/${user.id}`)
}

async function loadUsers() {
  loading.value = true
  error.value = ''
  try {
    users.value = await listUsers()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadUsers)
watch(() => route.params.id, loadUsers)
</script>

<template>
  <section class="users-page">
    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleUsers"
        :loading="loading"
        :error="error"
        :sort-key="sortKey"
        :sort-dir="sortDir"
        :selected-ids="selectedIds"
        @sort-change="handleSortChange"
        @selection-change="selectedIds = $event"
        @row-open="openUser"
      >
        <template #row-actions="{ row }">
          <button class="btn btn-sm btn-primary" type="button" @click="openUser(row)">Open User</button>
        </template>
      </DataTable>
    </div>
  </section>
</template>
