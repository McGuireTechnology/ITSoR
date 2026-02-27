<script setup>
import { ref } from 'vue'
import { createGroup } from '../../lib/api'
import { closeInspectorAction, notifyGroupsChanged } from '../../lib/inspectorActions'

const name = ref('')
const tenantId = ref('')
const saving = ref(false)
const error = ref('')

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    await createGroup({
      name: name.value.trim(),
      tenant_id: tenantId.value.trim() || null,
    })
    notifyGroupsChanged()
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
    <h3>Create Group</h3>
    <label>
      Group Name
      <input v-model="name" type="text" required />
    </label>
    <label>
      Tenant ID (optional)
      <input v-model="tenantId" type="text" />
    </label>
    <div class="confirm-row">
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
        {{ saving ? 'Creating...' : 'Create Group' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
