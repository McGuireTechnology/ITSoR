<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { logoutUser } from '../lib/api'
import { clearToken } from '../lib/auth'
import itsorCubeLogo from '../assets/itsor-cube-logo.svg'

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
  <section class="container min-vh-100 d-flex align-items-center justify-content-center py-5 px-3">
    <div class="card shadow-sm border-0 w-100 max-w-md rounded-4 bg-brand-surface/70">
      <div class="card-body p-4 p-md-5 text-center">
        <img :src="itsorCubeLogo" alt="ITSoR logo" class="d-block mx-auto mb-3" width="80" height="80" />
        <p class="h3 text-brand-deep fw-bold mb-1">ITSoR</p>
        <p class="text-body-secondary mb-4">IT System of Record</p>
        <p>{{ message }}</p>
        <RouterLink class="text-brand-purple hover:text-brand-pink" to="/login">Go to login</RouterLink>
      </div>
    </div>
  </section>
</template>
