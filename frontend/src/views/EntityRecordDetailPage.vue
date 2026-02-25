<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteEntityRecord, getEntityRecordById, updateEntityRecord } from '../lib/api'

const route = useRoute()
const router = useRouter()

const entityRecord = ref(null)
const name = ref('')
const valuesJsonText = ref('{}')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
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

async function loadEntityRecord() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getEntityRecordById(route.params.id)
    entityRecord.value = loaded
    name.value = loaded.name || ''
    valuesJsonText.value = JSON.stringify(loaded.values_json ?? {}, null, 2)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!entityRecord.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    entityRecord.value = await updateEntityRecord(entityRecord.value.id, {
      name: name.value.trim(),
      values_json: parseValuesJson(),
    })
    name.value = entityRecord.value.name || ''
    valuesJsonText.value = JSON.stringify(entityRecord.value.values_json ?? {}, null, 2)
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!entityRecord.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteEntityRecord(entityRecord.value.id)
    await router.push('/entity-records')
  } catch (deleteError) {
    error.value = deleteError.message
  } finally {
    deleting.value = false
  }
}

function startDeleteConfirmation() {
  confirmingDelete.value = true
}

function cancelDeleteConfirmation() {
  confirmingDelete.value = false
}

onMounted(loadEntityRecord)

watch(
  () => route.params.id,
  () => {
    loadEntityRecord()
  },
)
</script>

<template>
  <section class="panel">
    <h2>Entity Record Detail</h2>
    <p v-if="loading">Loading entity record...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" />
        </label>
        <label>
          Values JSON
          <textarea v-model="valuesJsonText" rows="8" required />
        </label>
        <button type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ entityRecord.id }}</dd>
        <dt>Entity Type ID</dt>
        <dd>{{ entityRecord.entity_type_id }}</dd>
      </dl>

      <div class="section-gap">
        <button
          v-if="!confirmingDelete"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Entity Record
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete entity record "{{ entityRecord.name || '(unnamed)' }}"?</p>
          <button type="button" :disabled="deleting" @click="handleDelete">
            {{ deleting ? 'Deleting...' : 'Confirm Delete' }}
          </button>
          <button type="button" :disabled="deleting" @click="cancelDeleteConfirmation">
            Cancel
          </button>
        </div>
      </div>
    </template>
  </section>
</template>
