<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listIdmGroupMemberships } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'

const route = useRoute()

const memberships = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('group_id')
const sortDir = ref('asc')

const columns = [
  { key: 'group_id', label: 'Group ID', sortable: true },
  { key: 'member_type', label: 'Member Type', sortable: true },
  { key: 'member_user_id', label: 'Member User ID', sortable: true },
  { key: 'member_group_id', label: 'Member Group ID', sortable: true },
  { key: 'id', label: 'Membership ID', sortable: false },
]

async function loadMemberships() {
  loading.value = true
  error.value = ''
  try {
    memberships.value = await listIdmGroupMemberships()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

const visibleMemberships = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = memberships.value

  if (query) {
    filtered = memberships.value.filter((membership) =>
      `${membership.group_id || ''} ${membership.member_type || ''} ${membership.member_user_id || ''} ${membership.member_group_id || ''} ${membership.id || ''}`
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

onMounted(loadMemberships)

watch(
  [visibleMemberships, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleMemberships.value.length,
      selected: selectedIds.value.length,
      noun: 'memberships',
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
    loadMemberships()
  },
)
</script>

<template>
  <section class="users-page">
    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleMemberships"
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
