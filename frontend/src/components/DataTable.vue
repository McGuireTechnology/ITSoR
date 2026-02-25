<script setup>
import { computed } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true,
  },
  rows: {
    type: Array,
    required: true,
  },
  rowKey: {
    type: String,
    default: 'id',
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
  sortKey: {
    type: String,
    default: '',
  },
  sortDir: {
    type: String,
    default: 'asc',
  },
  selectedIds: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['sort-change', 'selection-change', 'row-open'])

const allVisibleSelected = computed(() => {
  if (!props.rows.length) {
    return false
  }
  return props.rows.every((row) => props.selectedIds.includes(row[props.rowKey]))
})

function toggleAll(event) {
  if (event.target.checked) {
    emit(
      'selection-change',
      props.rows.map((row) => row[props.rowKey]),
    )
    return
  }
  emit('selection-change', [])
}

function toggleRow(rowId, checked) {
  if (checked) {
    emit('selection-change', [...props.selectedIds, rowId])
    return
  }
  emit(
    'selection-change',
    props.selectedIds.filter((id) => id !== rowId),
  )
}

function headerLabel(column) {
  if (props.sortKey !== column.key) {
    return column.label
  }
  return `${column.label} ${props.sortDir === 'asc' ? '↑' : '↓'}`
}
</script>

<template>
  <div class="data-table-wrap">
    <p v-if="loading">Loading…</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="!rows.length" class="meta">No records found.</p>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th class="col-checkbox">
            <input type="checkbox" :checked="allVisibleSelected" @change="toggleAll" />
          </th>
          <th v-for="column in columns" :key="column.key">
            <button
              v-if="column.sortable"
              type="button"
              class="th-button"
              @click="emit('sort-change', column.key)"
            >
              {{ headerLabel(column) }}
            </button>
            <span v-else>{{ column.label }}</span>
          </th>
          <th class="col-actions">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row[rowKey]">
          <td class="col-checkbox">
            <input
              type="checkbox"
              :checked="selectedIds.includes(row[rowKey])"
              @change="toggleRow(row[rowKey], $event.target.checked)"
            />
          </td>
          <td v-for="column in columns" :key="`${row[rowKey]}:${column.key}`">
            {{ row[column.key] }}
          </td>
          <td class="col-actions">
            <slot name="row-actions" :row="row">
              <button type="button" @click="emit('row-open', row)">Open</button>
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
