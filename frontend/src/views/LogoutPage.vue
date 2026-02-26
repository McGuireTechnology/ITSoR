<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { logoutUser } from '../lib/api'
import { clearToken } from '../lib/auth'

const router = useRouter()
const message = ref('Signing out...')

onMounted(async () => {
  try {
    await logoutUser()
    message.value = 'You are logged out.'
  } catch (logoutError) {
    message.value = logoutError.message
  } finally {
    clearToken()
    await router.replace('/login')
  }
})
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Logout</h2>
    <p>{{ message }}</p>
    <RouterLink class="text-brand-purple hover:text-brand-pink" to="/login">Go to login</RouterLink>
  </section>
</template>
