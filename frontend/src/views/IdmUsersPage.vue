<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listIdmUsers } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'

const route = useRoute()

const users = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('username')
const sortDir = ref('asc')

const columns = [
  { key: 'username', label: 'Username', sortable: true },
  { key: 'account_status', label: 'Account Status', sortable: true },
  { key: 'person_id', label: 'Person ID', sortable: true },
  { key: 'id', label: 'User ID', sortable: false },
]

async function loadUsers() {
  loading.value = true
  error.value = ''
  try {
    users.value = await listIdmUsers()
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
      `${user.username || ''} ${user.account_status || ''} ${user.person_id || ''} ${user.id || ''}`.toLowerCase().includes(query),
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

onMounted(loadUsers)

watch(
  [visibleUsers, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleUsers.value.length,
      selected: selectedIds.value.length,
      noun: 'users',
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
    loadUsers()
  },
)
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
      >
        <template #row-actions>
          <span class="meta">—</span>
        </template>
      </DataTable>
    </div>
  </section>
</template>
