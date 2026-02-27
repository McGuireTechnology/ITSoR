<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listIdmPeople } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'

const route = useRoute()

const people = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('display_name')
const sortDir = ref('asc')

const columns = [
  { key: 'display_name', label: 'Display Name', sortable: true },
  { key: 'current_identity_id', label: 'Current Identity ID', sortable: true },
  { key: 'id', label: 'Person ID', sortable: false },
]

async function loadPeople() {
  loading.value = true
  error.value = ''
  try {
    people.value = await listIdmPeople()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

const visiblePeople = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = people.value

  if (query) {
    filtered = people.value.filter((person) =>
      `${person.display_name || ''} ${person.current_identity_id || ''} ${person.id || ''}`.toLowerCase().includes(query),
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

onMounted(loadPeople)

watch(
  [visiblePeople, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visiblePeople.value.length,
      selected: selectedIds.value.length,
      noun: 'people',
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
    loadPeople()
  },
)
</script>

<template>
  <section class="users-page">
    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visiblePeople"
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
