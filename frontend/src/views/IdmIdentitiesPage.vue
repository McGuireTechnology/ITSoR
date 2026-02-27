<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from '../components/DataTable.vue'
import { listIdmIdentities } from '../lib/api'
import { clearCommandSurfaceMetrics, setCommandSurfaceMetrics } from '../lib/commandSurface'

const route = useRoute()

const identities = ref([])
const loading = ref(true)
const error = ref('')
const selectedIds = ref([])
const sortKey = ref('source_system')
const sortDir = ref('asc')

const columns = [
  { key: 'source_system', label: 'Source System', sortable: true },
  { key: 'source_record_id', label: 'Source Record ID', sortable: true },
  { key: 'person_id', label: 'Person ID', sortable: true },
  { key: 'id', label: 'Identity ID', sortable: false },
]

async function loadIdentities() {
  loading.value = true
  error.value = ''
  try {
    identities.value = await listIdmIdentities()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

const visibleIdentities = computed(() => {
  const query = String(route.query.q || '').trim().toLowerCase()
  let filtered = identities.value

  if (query) {
    filtered = identities.value.filter((identity) =>
      `${identity.source_system || ''} ${identity.source_record_id || ''} ${identity.person_id || ''} ${identity.id || ''}`
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

onMounted(loadIdentities)

watch(
  [visibleIdentities, selectedIds],
  () => {
    setCommandSurfaceMetrics({
      total: visibleIdentities.value.length,
      selected: selectedIds.value.length,
      noun: 'identities',
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
    loadIdentities()
  },
)
</script>

<template>
  <section class="users-page">
    <div class="users-table-fill">
      <DataTable
        :columns="columns"
        :rows="visibleIdentities"
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
