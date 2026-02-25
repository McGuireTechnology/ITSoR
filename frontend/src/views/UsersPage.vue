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

const visibleUsers = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = users.value

  if (query) {
    filtered = users.value.filter((user) =>
      `${user.username || ''} ${user.email || ''} ${user.id || ''}`.toLowerCase().includes(query),
    )
  }

  const sorted = [...filtered].sort((left, right) => {
    const a = String(left[sortKey.value] || '').toLowerCase()
    const b = String(right[sortKey.value] || '').toLowerCase()
    if (a === b) {
      return 0
    }
    const result = a > b ? 1 : -1
    return sortDir.value === 'asc' ? result : -result
  })

  return sorted
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
  router.push(`/users/${user.id}`)
}

onMounted(loadUsers)

watch(
  () => route.query._refresh,
  () => {
    loadUsers()
  },
)
</script>

<template>
  <section class="panel">
    <h2>Users</h2>
    <p class="meta section-gap">{{ visibleUsers.length }} users</p>
    <p class="meta">{{ selectedIds.length }} selected</p>

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
        <button type="button" @click="openUser(row)">View</button>
      </template>
    </DataTable>
  </section>
</template>
