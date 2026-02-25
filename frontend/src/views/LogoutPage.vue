<script setup>
import { onMounted, ref } from 'vue'
import { logoutUser } from '../lib/api'
import { clearToken } from '../lib/auth'

const message = ref('Signing out...')

onMounted(async () => {
  try {
    await logoutUser()
    message.value = 'You are logged out.'
  } catch (logoutError) {
    message.value = logoutError.message
  } finally {
    clearToken()
  }
})
</script>

<template>
  <section class="panel">
    <h2>Logout</h2>
    <p>{{ message }}</p>
    <RouterLink to="/login">Go to login</RouterLink>
  </section>
</template>
