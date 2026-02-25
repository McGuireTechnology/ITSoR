<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteTenant, getTenantById, updateTenant } from '../lib/api'

const route = useRoute()
const router = useRouter()

const tenant = ref(null)
const name = ref('')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')

async function loadTenant() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getTenantById(route.params.id)
    tenant.value = loaded
    name.value = loaded.name
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!tenant.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    tenant.value = await updateTenant(tenant.value.id, { name: name.value.trim() })
    name.value = tenant.value.name
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!tenant.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteTenant(tenant.value.id)
    await router.push('/tenants')
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

onMounted(loadTenant)

watch(
  () => route.params.id,
  () => {
    loadTenant()
  },
)
</script>

<template>
  <section class="panel">
    <h2>Tenant Detail</h2>
    <p v-if="loading">Loading tenant...</p>
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
        <dd>{{ tenant.id }}</dd>
      </dl>

      <div class="section-gap">
        <button
          v-if="!confirmingDelete"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Tenant
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete tenant "{{ tenant.name }}"?</p>
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
