<script setup>
import { ref } from 'vue'
import { createTenant } from '../../lib/api'
import { closeInspectorAction, notifyTenantsChanged } from '../../lib/inspectorActions'

const name = ref('')
const saving = ref(false)
const error = ref('')

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    await createTenant({ name: name.value.trim() })
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
    <h3>Create Tenant</h3>
    <label>
      Tenant Name
      <input v-model="name" type="text" required />
    </label>
    <div class="confirm-row">
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
        {{ saving ? 'Creating...' : 'Create Tenant' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
