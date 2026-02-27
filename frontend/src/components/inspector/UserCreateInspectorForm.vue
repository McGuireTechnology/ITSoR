<script setup>
import { ref } from 'vue'
import { createUser } from '../../lib/api'
import { closeInspectorAction, notifyUsersChanged } from '../../lib/inspectorActions'

const username = ref('')
const email = ref('')
const password = ref('')
const createTenantName = ref('')
const inviteGroupId = ref('')
const saving = ref(false)
const error = ref('')

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    await createUser({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
      create_tenant_name: createTenantName.value.trim() || null,
      invite_group_id: inviteGroupId.value.trim() || null,
    })
    notifyUsersChanged()
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
    <h3>Create User</h3>
    <label>
      Username
      <input v-model="username" type="text" required />
    </label>
    <label>
      Email
      <input v-model="email" type="email" required />
    </label>
    <label>
      Password
      <input v-model="password" type="password" required />
    </label>
    <label>
      Create Tenant Name (optional)
      <input v-model="createTenantName" type="text" />
    </label>
    <label>
      Invite Group ID (optional)
      <input v-model="inviteGroupId" type="text" />
    </label>
    <div class="confirm-row">
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
        {{ saving ? 'Creating...' : 'Create User' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
