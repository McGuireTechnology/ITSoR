<script setup>
import { onMounted, ref } from 'vue'
import { createWorkspace, listWorkspaces } from '../lib/api'
import { formatNameId } from '../lib/formatters'

const workspaces = ref([])
const name = ref('')
const tenantId = ref('')
const loading = ref(true)
const creating = ref(false)
const error = ref('')

async function loadWorkspaces() {
  loading.value = true
  error.value = ''
  try {
    workspaces.value = await listWorkspaces()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateWorkspace() {
  creating.value = true
  error.value = ''
  try {
    const created = await createWorkspace({
      name: name.value.trim(),
      tenant_id: tenantId.value.trim() || null,
    })
    workspaces.value = [...workspaces.value, created]
    name.value = ''
    tenantId.value = ''
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

onMounted(loadWorkspaces)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Workspaces</h2>

    <form class="form" @submit.prevent="handleCreateWorkspace">
      <label>
        Workspace Name
        <input v-model="name" type="text" required />
      </label>
      <label>
        Tenant ID (optional)
        <input v-model="tenantId" type="text" />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Workspace' }}
      </button>
    </form>

    <p v-if="loading">Loading workspaces...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="workspace in workspaces" :key="workspace.id">
        <RouterLink :to="`/workspaces/${workspace.id}`">{{ formatNameId(workspace.name, workspace.id, '(unnamed workspace)') }}</RouterLink>
        <span class="meta">{{ workspace.id }} · owner: {{ workspace.owner_id || '-' }} · group: {{ workspace.group_id || '-' }} · perms: {{ workspace.permissions ?? '-' }}</span>
      </li>
    </ul>
  </section>
</template>
