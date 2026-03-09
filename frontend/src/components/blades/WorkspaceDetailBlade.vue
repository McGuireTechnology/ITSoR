<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { deleteWorkspace, getWorkspaceById, updateWorkspace } from '../../lib/api'
import { useBladeStack } from '../../lib/blades'
import { useDomainPermissions } from '../../lib/permissions'

const props = defineProps({
  workspaceId: {
    type: String,
    required: true,
  },
  bladeId: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const bladeStack = useBladeStack()
const domain = ref('workspaces')
const { canWrite } = useDomainPermissions(domain)

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
    const loaded = await getWorkspaceById(props.workspaceId)
    workspace.value = loaded
    name.value = loaded.name
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!workspace.value || !canWrite.value) {
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
  if (!workspace.value || !canWrite.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteWorkspace(workspace.value.id)
    bladeStack?.closeBlade(props.bladeId)
    await router.push('/customization/workspaces')
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
  () => props.workspaceId,
  () => {
    loadWorkspace()
  },
)
</script>

<template>
  <section>
    <p v-if="loading">Loading workspace...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="blade-form" @submit.prevent="handleSave">
        <label class="blade-field">
          <span>Name</span>
          <input v-model="name" type="text" required :disabled="!canWrite || saving" />
        </label>
        <button class="btn btn-sm btn-primary" type="submit" :disabled="!canWrite || saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
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

      <div v-if="canWrite" class="section-gap">
        <button
          v-if="!confirmingDelete"
          class="btn btn-sm btn-outline-secondary"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Workspace
        </button>

        <div v-else class="confirm-row">
          <p class="error mb-0">Delete workspace "{{ workspace.name }}"?</p>
          <button class="btn btn-sm btn-primary" type="button" :disabled="deleting" @click="handleDelete">
            {{ deleting ? 'Deleting...' : 'Confirm Delete' }}
          </button>
          <button class="btn btn-sm btn-outline-secondary" type="button" :disabled="deleting" @click="cancelDeleteConfirmation">
            Cancel
          </button>
        </div>
      </div>
    </template>
  </section>
</template>