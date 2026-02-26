<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteWorkspace, getWorkspaceById, updateWorkspace } from '../lib/api'

const route = useRoute()
const router = useRouter()

const workspace = ref(null)
const name = ref('')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')

async function loadWorkspace() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getWorkspaceById(route.params.id)
    workspace.value = loaded
    name.value = loaded.name
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!workspace.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    workspace.value = await updateWorkspace(workspace.value.id, { name: name.value.trim() })
    name.value = workspace.value.name
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!workspace.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteWorkspace(workspace.value.id)
    await router.push('/workspaces')
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

onMounted(loadWorkspace)

watch(
  () => route.params.id,
  () => {
    loadWorkspace()
  },
)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Workspace Detail</h2>
    <p v-if="loading">Loading workspace...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" required />
        </label>
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ workspace.id }}</dd>
        <dt>Tenant ID</dt>
        <dd>{{ workspace.tenant_id || '-' }}</dd>
        <dt>Owner</dt>
        <dd>{{ workspace.owner_id || '-' }}</dd>
        <dt>Group</dt>
        <dd>{{ workspace.group_id || '-' }}</dd>
        <dt>Permissions</dt>
        <dd>{{ workspace.permissions ?? '-' }}</dd>
      </dl>

      <div class="section-gap">
        <button
          v-if="!confirmingDelete"
          class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Workspace
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete workspace "{{ workspace.name }}"?</p>
          <button class="btn btn-primary bg-accent hover:bg-primary border-0" type="button" :disabled="deleting" @click="handleDelete">
            {{ deleting ? 'Deleting...' : 'Confirm Delete' }}
          </button>
          <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="deleting" @click="cancelDeleteConfirmation">
            Cancel
          </button>
        </div>
      </div>
    </template>
  </section>
</template>
