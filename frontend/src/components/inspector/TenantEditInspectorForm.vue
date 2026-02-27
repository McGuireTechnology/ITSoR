<script setup>
import { onMounted, ref, watch } from 'vue'
import { getTenantById, updateTenant } from '../../lib/api'
import { closeInspectorAction, notifyTenantsChanged } from '../../lib/inspectorActions'

const props = defineProps({
  tenantId: {
    type: String,
    required: true,
  },
})

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const name = ref('')

async function loadTenant() {
  loading.value = true
  error.value = ''
  try {
    const tenant = await getTenantById(props.tenantId)
    name.value = tenant.name || ''
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    await updateTenant(props.tenantId, { name: name.value.trim() })
    notifyTenantsChanged()
    closeInspectorAction()
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    saving.value = false
  }
}

onMounted(loadTenant)
watch(() => props.tenantId, loadTenant)
</script>

<template>
  <div>
    <p v-if="loading">Loading tenant...</p>
    <form v-else class="form" @submit.prevent="handleSubmit">
      <h3>Edit Tenant</h3>
      <label>
        Tenant Name
        <input v-model="name" type="text" required />
      </label>
      <div class="confirm-row">
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Tenant' }}
        </button>
        <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p v-if="error && loading" class="error">{{ error }}</p>
  </div>
</template>
