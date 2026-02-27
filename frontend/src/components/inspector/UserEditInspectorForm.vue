<script setup>
import { onMounted, ref, watch } from 'vue'
import { getUserById, updateUser } from '../../lib/api'
import { closeInspectorAction, notifyUsersChanged } from '../../lib/inspectorActions'

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
})

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const username = ref('')
const email = ref('')
const password = ref('')

async function loadUser() {
  loading.value = true
  error.value = ''
  try {
    const user = await getUserById(props.userId)
    username.value = user.username || ''
    email.value = user.email || ''
    password.value = ''
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
    await updateUser(props.userId, {
      username: username.value.trim(),
      email: email.value.trim(),
      ...(password.value ? { password: password.value } : {}),
    })
    notifyUsersChanged()
    closeInspectorAction()
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    saving.value = false
  }
}

onMounted(loadUser)
watch(() => props.userId, loadUser)
</script>

<template>
  <div>
    <p v-if="loading">Loading user...</p>
    <form v-else class="form" @submit.prevent="handleSubmit">
      <h3>Edit User</h3>
      <label>
        Username
        <input v-model="username" type="text" required />
      </label>
      <label>
        Email
        <input v-model="email" type="email" required />
      </label>
      <label>
        New Password (optional)
        <input v-model="password" type="password" />
      </label>
      <div class="confirm-row">
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save User' }}
        </button>
        <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p v-if="error && loading" class="error">{{ error }}</p>
  </div>
</template>
