<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteRole, getRoleById, updateRole } from '../lib/api'

const route = useRoute()
const router = useRouter()

const row = ref(null)
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')
const name = ref('')
const tenantId = ref('')
const description = ref('')

async function loadRow() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getRoleById(route.params.id)
    row.value = loaded
    name.value = loaded.name || ''
    tenantId.value = loaded.tenant_id || ''
    description.value = loaded.description || ''
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
    row.value = await updateRole(row.value.id, {
      name: name.value.trim(),
      tenant_id: tenantId.value.trim() || null,
      description: description.value.trim(),
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
    await deleteRole(row.value.id)
    await router.push('/auth/roles')
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
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Role Detail</h2>
    <p v-if="loading">Loading role...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" required :disabled="saving" />
        </label>
        <label>
          Tenant ID
          <input v-model="tenantId" type="text" :disabled="saving" />
        </label>
        <label>
          Description
          <input v-model="description" type="text" :disabled="saving" />
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
        {{ deleting ? 'Deleting...' : 'Delete Role' }}
      </button>
    </template>
  </section>
</template>
