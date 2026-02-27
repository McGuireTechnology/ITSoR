<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteEndpointPermission, getEndpointPermissionById, patchEndpointPermission } from '../lib/api'
import { markPermissionsDirty, useDomainPermissions } from '../lib/permissions'

const route = useRoute()
const router = useRouter()
const domain = ref('endpoint-permissions')
const { canWrite } = useDomainPermissions(domain)

const endpointPermission = ref(null)
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')
const principalType = ref('user')
const principalId = ref('')
const endpointName = ref('')
const action = ref('read')

async function loadEndpointPermission() {
  loading.value = true
  error.value = ''
  endpointPermission.value = null

  try {
    const loaded = await getEndpointPermissionById(route.params.id)
    endpointPermission.value = loaded
    principalType.value = loaded.principal_type
    principalId.value = loaded.principal_id
    endpointName.value = loaded.endpoint_name
    action.value = loaded.action
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!endpointPermission.value || !canWrite.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    endpointPermission.value = await patchEndpointPermission(endpointPermission.value.id, {
      principal_type: principalType.value,
      principal_id: principalId.value.trim(),
      endpoint_name: endpointName.value.trim(),
      action: action.value.trim(),
    })
    markPermissionsDirty()
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!endpointPermission.value || !canWrite.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteEndpointPermission(endpointPermission.value.id)
    markPermissionsDirty()
    await router.push('/platform/endpoint-permissions')
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

onMounted(loadEndpointPermission)

watch(
  () => route.params.id,
  () => {
    loadEndpointPermission()
  },
)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Endpoint Permission Detail</h2>
    <p v-if="loading">Loading endpoint permission...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Principal Type
          <select v-model="principalType" required :disabled="!canWrite || saving">
            <option value="user">user</option>
            <option value="group">group</option>
          </select>
        </label>
        <label>
          Principal ID
          <input v-model="principalId" type="text" required :disabled="!canWrite || saving" />
        </label>
        <label>
          Endpoint Name
          <input v-model="endpointName" type="text" required :disabled="!canWrite || saving" />
        </label>
        <label>
          Action
          <input v-model="action" type="text" required :disabled="!canWrite || saving" />
        </label>
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="!canWrite || saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ endpointPermission.id }}</dd>
      </dl>

      <div v-if="canWrite" class="section-gap">
        <button
          v-if="!confirmingDelete"
          class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Endpoint Permission
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete endpoint permission #{{ endpointPermission.id }}?</p>
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
