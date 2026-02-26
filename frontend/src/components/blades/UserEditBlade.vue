<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { getUserById, updateUser } from '../../lib/api'
import { useBladeStack } from '../../lib/blades'

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
  bladeId: {
    type: String,
    required: true,
  },
  onSaved: {
    type: Function,
    default: null,
  },
})

const bladeStack = useBladeStack()

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')
const original = ref({ username: '', email: '' })
const form = ref({ username: '', email: '', password: '' })

const isDirty = computed(() => {
  return (
    form.value.username !== original.value.username ||
    form.value.email !== original.value.email ||
    Boolean(form.value.password)
  )
})

watch(isDirty, (dirty) => {
  bladeStack?.updateBladeState(props.bladeId, { dirty })
})

async function loadUser() {
  loading.value = true
  error.value = ''
  success.value = ''
  try {
    const user = await getUserById(props.userId)
    original.value = {
      username: user.username || '',
      email: user.email || '',
    }
    form.value = {
      username: user.username || '',
      email: user.email || '',
      password: '',
    }
    bladeStack?.updateBladeState(props.bladeId, { dirty: false })
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true
  error.value = ''
  success.value = ''
  try {
    await updateUser(props.userId, {
      username: form.value.username,
      email: form.value.email,
      ...(form.value.password ? { password: form.value.password } : {}),
    })
    original.value = {
      username: form.value.username,
      email: form.value.email,
    }
    form.value.password = ''
    bladeStack?.updateBladeState(props.bladeId, { dirty: false })
    success.value = 'User updated.'
    await props.onSaved?.()
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

function cancel() {
  bladeStack?.closeTopBlade()
}

onMounted(loadUser)
</script>

<template>
  <form class="blade-form" @submit.prevent="save">
    <p v-if="loading">Loading editor...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <label class="blade-field">
        <span>Username</span>
        <input v-model="form.username" type="text" required />
      </label>

      <label class="blade-field">
        <span>Email</span>
        <input v-model="form.email" type="email" required />
      </label>

      <label class="blade-field">
        <span>New Password</span>
        <input v-model="form.password" type="password" autocomplete="new-password" />
      </label>

      <p v-if="success" class="text-success small mb-0">{{ success }}</p>

      <div class="blade-inline-actions">
        <button class="btn btn-sm btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving || !isDirty">
          {{ saving ? 'Saving…' : 'Save' }}
        </button>
        <button class="btn btn-sm btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" @click="cancel">Cancel</button>
      </div>
    </template>
  </form>
</template>
