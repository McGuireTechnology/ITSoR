<script setup>
import { onMounted, ref } from 'vue'
import { createNamespace, listNamespaces } from '../lib/api'

const namespaces = ref([])
const name = ref('')
const workspaceId = ref('')
const loading = ref(true)
const creating = ref(false)
const error = ref('')

async function loadNamespaces() {
  loading.value = true
  error.value = ''
  try {
    namespaces.value = await listNamespaces()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateNamespace() {
  creating.value = true
  error.value = ''
  try {
    const created = await createNamespace({
      name: name.value.trim(),
      workspace_id: workspaceId.value.trim(),
    })
    namespaces.value = [...namespaces.value, created]
    name.value = ''
    workspaceId.value = ''
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

onMounted(loadNamespaces)
</script>

<template>
  <section class="panel">
    <h2>Namespaces</h2>

    <form class="form" @submit.prevent="handleCreateNamespace">
      <label>
        Namespace Name
        <input v-model="name" type="text" required />
      </label>
      <label>
        Workspace ID
        <input v-model="workspaceId" type="text" required />
      </label>
      <button type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Namespace' }}
      </button>
    </form>

    <p v-if="loading">Loading namespaces...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="namespace in namespaces" :key="namespace.id">
        <RouterLink :to="`/namespaces/${namespace.id}`">{{ namespace.name }}</RouterLink>
        <span class="meta">{{ namespace.id }}</span>
      </li>
    </ul>
  </section>
</template>
