<script setup>
import { onMounted, ref } from 'vue'
import { createNamespace, listNamespaces } from '../lib/api'
import { formatNameId } from '../lib/formatters'

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
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Namespaces</h2>

    <form class="form" @submit.prevent="handleCreateNamespace">
      <label>
        Namespace Name
        <input v-model="name" type="text" required />
      </label>
      <label>
        Workspace ID
        <input v-model="workspaceId" type="text" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Namespace' }}
      </button>
    </form>

    <p v-if="loading">Loading namespaces...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="namespace in namespaces" :key="namespace.id">
        <RouterLink :to="`/namespaces/${namespace.id}`">{{ formatNameId(namespace.name, namespace.id, '(unnamed namespace)') }}</RouterLink>
        <span class="meta">{{ namespace.id }} · owner: {{ namespace.owner_id || '-' }} · group: {{ namespace.group_id || '-' }} · perms: {{ namespace.permissions ?? '-' }}</span>
      </li>
    </ul>
  </section>
</template>
