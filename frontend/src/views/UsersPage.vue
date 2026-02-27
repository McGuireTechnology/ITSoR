<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listUsers } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'
import { inspectorState, openUserEditInspector } from '../lib/inspectorActions'

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

function navigateToUser(user) {
  router.push(`/platform/users/${user.id}`)
}

function editUserInline(user) {
  openUserEditInspector(user.id)
}

function inspectUser(user) {
  const nextQuery = { ...route.query, inspectUserId: user.id }
  router.replace({ path: '/platform/users', query: nextQuery })
}

onMounted(loadUsers)

watch(
  [visibleUsers, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleUsers.value.length,
      selected: selectedIds.value.length,
      selectedIds: selectedIds.value,
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

watch(
  () => inspectorState.usersRefreshTick,
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
        @row-open="navigateToUser"
      >
        <template #row-actions="{ row }">
          <div class="d-flex gap-2">
            <button
              class="btn btn-sm btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white"
              type="button"
              @click="editUserInline(row)"
            >
              ✎
            </button>
            <button class="btn btn-sm btn-outline-primary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" @click="inspectUser(row)">Inspect</button>
            <button class="btn btn-sm btn-primary" type="button" @click="navigateToUser(row)">Open</button>
          </div>
        </template>
      </DataTable>
    </div>
  </section>
</template>
