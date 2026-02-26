<script setup>
import { onMounted, ref } from 'vue'
import { createEntityType, listEntityTypes } from '../lib/api'
import { formatNameId } from '../lib/formatters'

const entityTypes = ref([])
const name = ref('')
const namespaceId = ref('')
const attributesJsonText = ref('{}')
const loading = ref(true)
const creating = ref(false)
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

async function loadEntityTypes() {
  loading.value = true
  error.value = ''
  try {
    entityTypes.value = await listEntityTypes()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateEntityType() {
  creating.value = true
  error.value = ''
  try {
    const created = await createEntityType({
      name: name.value.trim(),
      namespace_id: namespaceId.value.trim(),
      attributes_json: parseAttributesJson(),
    })
    entityTypes.value = [...entityTypes.value, created]
    name.value = ''
    namespaceId.value = ''
    attributesJsonText.value = '{}'
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

onMounted(loadEntityTypes)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Entity Types</h2>

    <form class="form" @submit.prevent="handleCreateEntityType">
      <label>
        Entity Type Name
        <input v-model="name" type="text" required />
      </label>
      <label>
        Namespace ID
        <input v-model="namespaceId" type="text" required />
      </label>
      <label>
        Attributes JSON
        <textarea v-model="attributesJsonText" rows="6" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Entity Type' }}
      </button>
    </form>

    <p v-if="loading">Loading entity types...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="entityType in entityTypes" :key="entityType.id">
        <RouterLink :to="`/entity-types/${entityType.id}`">{{ formatNameId(entityType.name, entityType.id, '(unnamed entity type)') }}</RouterLink>
        <span class="meta">{{ entityType.id }} · owner: {{ entityType.owner_id || '-' }} · group: {{ entityType.group_id || '-' }} · perms: {{ entityType.permissions ?? '-' }}</span>
      </li>
    </ul>
  </section>
</template>
