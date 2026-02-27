<script setup>
import { ref } from 'vue'
import { getTenantById, updateTenant } from '../../lib/api'
import { closeInspectorAction, notifyTenantsChanged } from '../../lib/inspectorActions'

const props = defineProps({
  tenantIds: {
    type: Array,
    required: true,
  },
})

const saving = ref(false)
const error = ref('')
const prefix = ref('')

async function handleSubmit() {
  if (!prefix.value.trim()) {
    error.value = 'Name prefix is required for multi-edit.'
    return
  }

  saving.value = true
  error.value = ''
  try {
    for (const tenantId of props.tenantIds) {
      const tenant = await getTenantById(String(tenantId))
      await updateTenant(String(tenantId), {
        name: `${prefix.value.trim()}${tenant.name || ''}`,
      })
    }
    notifyTenantsChanged()
    closeInspectorAction()
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="form" @submit.prevent="handleSubmit">
    <h3>Multi-Edit Tenants</h3>
    <p class="meta">Applying update to {{ tenantIds.length }} selected tenants.</p>
    <label>
      Name Prefix
      <input v-model="prefix" type="text" required />
    </label>
    <div class="confirm-row">
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving || !tenantIds.length">
        {{ saving ? 'Applying...' : 'Apply to Selected' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
