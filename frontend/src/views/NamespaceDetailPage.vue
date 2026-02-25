<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteNamespace, getNamespaceById, updateNamespace } from '../lib/api'

const route = useRoute()
const router = useRouter()

const namespace = ref(null)
const name = ref('')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')

async function loadNamespace() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getNamespaceById(route.params.id)
    namespace.value = loaded
    name.value = loaded.name
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!namespace.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    namespace.value = await updateNamespace(namespace.value.id, { name: name.value.trim() })
    name.value = namespace.value.name
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!namespace.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteNamespace(namespace.value.id)
    await router.push('/namespaces')
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

onMounted(loadNamespace)

watch(
  () => route.params.id,
  () => {
    loadNamespace()
  },
)
</script>

<template>
  <section class="panel">
    <h2>Namespace Detail</h2>
    <p v-if="loading">Loading namespace...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" required />
        </label>
        <button type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ namespace.id }}</dd>
        <dt>Workspace ID</dt>
        <dd>{{ namespace.workspace_id }}</dd>
      </dl>

      <div class="section-gap">
        <button
          v-if="!confirmingDelete"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Namespace
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete namespace "{{ namespace.name }}"?</p>
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
