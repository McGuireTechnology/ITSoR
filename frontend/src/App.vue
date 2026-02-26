<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AuthLayout from './layouts/AuthLayout.vue'
import DefaultLayout from './layouts/DefaultLayout.vue'
import { hasValidToken } from './lib/auth'

const route = useRoute()
const isAuthenticated = ref(hasValidToken())
const isAuthLayout = computed(() => route.meta.layout === 'auth')

function syncAuthState() {
  isAuthenticated.value = hasValidToken()
}

onMounted(() => {
  window.addEventListener('storage', syncAuthState)
  window.addEventListener('itsor-auth-changed', syncAuthState)
})

onUnmounted(() => {
  window.removeEventListener('storage', syncAuthState)
  window.removeEventListener('itsor-auth-changed', syncAuthState)
})
</script>

<template>
  <div class="app-shell">
    <AuthLayout v-if="isAuthLayout">
      <RouterView />
    </AuthLayout>
    <DefaultLayout v-else :is-authenticated="isAuthenticated">
      <RouterView />
    </DefaultLayout>
  </div>
</template>
