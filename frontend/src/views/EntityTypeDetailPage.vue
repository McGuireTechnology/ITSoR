<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteEntityType, getEntityTypeById, updateEntityType } from '../lib/api'

const route = useRoute()
const router = useRouter()

const entityType = ref(null)
const name = ref('')
const attributesJsonText = ref('{}')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')

function parseAttributesJson() {
  try {
    const parsed = JSON.parse(attributesJsonText.value)
    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
      return parsed
    }
    throw new Error('Attributes JSON must be an object')
  } catch {
    throw new Error('Attributes JSON must be valid JSON object')
  }
}

async function loadEntityType() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getEntityTypeById(route.params.id)
    entityType.value = loaded
    name.value = loaded.name
    attributesJsonText.value = JSON.stringify(loaded.attributes_json ?? {}, null, 2)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!entityType.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    entityType.value = await updateEntityType(entityType.value.id, {
      name: name.value.trim(),
      attributes_json: parseAttributesJson(),
    })
    name.value = entityType.value.name
    attributesJsonText.value = JSON.stringify(entityType.value.attributes_json ?? {}, null, 2)
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!entityType.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteEntityType(entityType.value.id)
    await router.push('/entity-types')
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

onMounted(loadEntityType)

watch(
  () => route.params.id,
  () => {
    loadEntityType()
  },
)
</script>

<template>
  <section class="panel">
    <h2>Entity Type Detail</h2>
    <p v-if="loading">Loading entity type...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" required />
        </label>
        <label>
          Attributes JSON
          <textarea v-model="attributesJsonText" rows="8" required />
        </label>
        <button type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ entityType.id }}</dd>
        <dt>Namespace ID</dt>
        <dd>{{ entityType.namespace_id }}</dd>
      </dl>

      <div class="section-gap">
        <button
          v-if="!confirmingDelete"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Entity Type
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete entity type "{{ entityType.name }}"?</p>
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
