<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deletePermission, getPermissionById, updatePermission } from '../lib/api'

const route = useRoute()
const router = useRouter()

const row = ref(null)
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')
const name = ref('')
const resource = ref('')
const action = ref('')

async function loadRow() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getPermissionById(route.params.id)
    row.value = loaded
    name.value = loaded.name || ''
    resource.value = loaded.resource || ''
    action.value = loaded.action || ''
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!row.value) {
    return
  }
  saving.value = true
  error.value = ''
  try {
    row.value = await updatePermission(row.value.id, {
      name: name.value.trim(),
      resource: resource.value.trim(),
      action: action.value.trim(),
    })
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!row.value) {
    return
  }
  deleting.value = true
  error.value = ''
  try {
    await deletePermission(row.value.id)
    await router.push('/auth/permissions')
  } catch (deleteError) {
    error.value = deleteError.message
  } finally {
    deleting.value = false
  }
}

onMounted(loadRow)
watch(() => route.params.id, loadRow)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Permission Detail</h2>
    <p v-if="loading">Loading permission...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" required :disabled="saving" />
        </label>
        <label>
          Resource
          <input v-model="resource" type="text" required :disabled="saving" />
        </label>
        <label>
          Action
          <input v-model="action" type="text" required :disabled="saving" />
        </label>
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ row.id }}</dd>
      </dl>

      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="deleting" @click="handleDelete">
        {{ deleting ? 'Deleting...' : 'Delete Permission' }}
      </button>
    </template>
  </section>
</template>
