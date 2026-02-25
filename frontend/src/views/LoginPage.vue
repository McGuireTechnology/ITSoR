<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser } from '../lib/api'
import { setToken } from '../lib/auth'

const router = useRouter()

const identifier = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    const response = await loginUser({
      identifier: identifier.value,
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
    <h2>Login</h2>
    <form class="form" @submit.prevent="handleSubmit">
      <label>
        Username or Email
        <input v-model="identifier" type="text" required autocomplete="username" />
      </label>

      <label>
        Password
        <input v-model="password" type="password" required autocomplete="current-password" />
      </label>

      <button type="submit" :disabled="loading">{{ loading ? 'Signing in...' : 'Login' }}</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </section>
</template>
