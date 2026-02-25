<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { signupUser } from '../lib/api'
import { setToken } from '../lib/auth'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    const response = await signupUser({
      username: username.value,
      email: email.value,
      password: password.value,
    })
    setToken(response.access_token)
    await router.push('/users')
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="panel">
    <h2>Signup</h2>
    <form class="form" @submit.prevent="handleSubmit">
      <label>
        Username
        <input v-model="username" type="text" required autocomplete="username" />
      </label>

      <label>
        Email
        <input v-model="email" type="email" required autocomplete="email" />
      </label>

      <label>
        Password
        <input v-model="password" type="password" required autocomplete="new-password" />
      </label>

      <button type="submit" :disabled="loading">{{ loading ? 'Creating...' : 'Signup' }}</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </section>
</template>
