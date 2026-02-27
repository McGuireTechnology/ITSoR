<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listIdmGroups } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'

const route = useRoute()

const groups = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('name')
const sortDir = ref('asc')

const columns = [
  { key: 'name', label: 'Group Name', sortable: true },
  { key: 'description', label: 'Description', sortable: true },
  { key: 'id', label: 'Group ID', sortable: false },
]

async function loadGroups() {
  loading.value = true
  error.value = ''
  try {
    groups.value = await listIdmGroups()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

const visibleGroups = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = groups.value

  if (query) {
    filtered = groups.value.filter((group) => `${group.name || ''} ${group.description || ''} ${group.id || ''}`.toLowerCase().includes(query))
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

onMounted(loadGroups)

watch(
  [visibleGroups, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleGroups.value.length,
      selected: selectedIds.value.length,
      noun: 'groups',
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
    loadGroups()
  },
)
</script>

<template>
  <section class="users-page">
    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleGroups"
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
