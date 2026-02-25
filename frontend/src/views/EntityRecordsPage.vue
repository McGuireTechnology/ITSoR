<script setup>
import { onMounted, ref } from 'vue'
import { createEntityRecord, listEntityRecords } from '../lib/api'

const entityRecords = ref([])
const entityTypeId = ref('')
const name = ref('')
const valuesJsonText = ref('{}')
const searchField = ref('')
const searchValue = ref('')
const searchOperator = ref('eq')
const loading = ref(true)
const creating = ref(false)
const searching = ref(false)
const error = ref('')

function parseValuesJson() {
  try {
    const parsed = JSON.parse(valuesJsonText.value)
    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
      return parsed
    }
    throw new Error('Values JSON must be an object')
  } catch {
    throw new Error('Values JSON must be valid JSON object')
  }
}

async function loadEntityRecords() {
  loading.value = true
  error.value = ''
  try {
    entityRecords.value = await listEntityRecords()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateEntityRecord() {
  creating.value = true
  error.value = ''
  try {
    const created = await createEntityRecord({
      entity_type_id: entityTypeId.value.trim(),
      name: name.value.trim(),
      values_json: parseValuesJson(),
    })
    entityRecords.value = [...entityRecords.value, created]
    name.value = ''
    valuesJsonText.value = '{}'
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

async function handleSearch() {
  searching.value = true
  error.value = ''
  try {
    entityRecords.value = await listEntityRecords({
      entityTypeId: entityTypeId.value.trim() || undefined,
      field: searchField.value.trim() || undefined,
      value: searchValue.value,
      operator: searchOperator.value,
    })
  } catch (searchError) {
    error.value = searchError.message
  } finally {
    searching.value = false
  }
}

onMounted(loadEntityRecords)
</script>

<template>
  <section class="panel">
    <h2>Entity Records</h2>

    <form class="form section-gap" @submit.prevent="handleSearch">
      <label>
        Entity Type ID (optional filter)
        <input v-model="entityTypeId" type="text" />
      </label>
      <label>
        Field (optional search)
        <input v-model="searchField" type="text" />
      </label>
      <label>
        Value (optional search)
        <input v-model="searchValue" type="text" />
      </label>
      <label>
        Operator
        <select v-model="searchOperator">
          <option value="eq">eq</option>
          <option value="neq">neq</option>
          <option value="contains">contains</option>
        </select>
      </label>
      <button type="submit" :disabled="searching">
        {{ searching ? 'Searching...' : 'Apply Filter' }}
      </button>
    </form>

    <form class="form" @submit.prevent="handleCreateEntityRecord">
      <label>
        Entity Type ID
        <input v-model="entityTypeId" type="text" required />
      </label>
      <label>
        Record Name
        <input v-model="name" type="text" />
      </label>
      <label>
        Values JSON
        <textarea v-model="valuesJsonText" rows="6" required />
      </label>
      <button type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Entity Record' }}
      </button>
    </form>

    <p v-if="loading">Loading entity records...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="entityRecord in entityRecords" :key="entityRecord.id">
        <RouterLink :to="`/entity-records/${entityRecord.id}`">{{ entityRecord.name || '(unnamed)' }}</RouterLink>
        <span class="meta">{{ entityRecord.id }}</span>
      </li>
    </ul>
  </section>
</template>
