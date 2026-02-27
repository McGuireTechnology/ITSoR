<script setup>
import { computed, ref } from 'vue'
import { updateUser } from '../../lib/api'
import { closeInspectorAction, notifyUsersChanged } from '../../lib/inspectorActions'

const props = defineProps({
  userIds: {
    type: Array,
    required: true,
  },
})

const saving = ref(false)
const error = ref('')
const password = ref('')

const count = computed(() => props.userIds.length)

async function handleSubmit() {
  if (!password.value) {
    error.value = 'Password is required for multi-edit.'
    return
  }

  saving.value = true
  error.value = ''
  try {
    for (const userId of props.userIds) {
      await updateUser(String(userId), { password: password.value })
    }
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
    <h3>Multi-Edit Users</h3>
    <p class="meta">Applying update to {{ count }} selected users.</p>
    <label>
      New Password
      <input v-model="password" type="password" required />
    </label>
    <div class="confirm-row">
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving || !count">
        {{ saving ? 'Applying...' : 'Apply to Selected' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
