<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AuthLayout from './layouts/AuthLayout.vue'
import DefaultLayout from './layouts/DefaultLayout.vue'
import { getToken } from './lib/auth'

const route = useRoute()
const isAuthenticated = ref(Boolean(getToken()))
const showNavigation = computed(() => route.meta.hideNavigation !== true)
const isAuthLayout = computed(() => route.meta.layout === 'auth')

function syncAuthState() {
  isAuthenticated.value = Boolean(getToken())
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
    <DefaultLayout v-if="showNavigation" :is-authenticated="isAuthenticated">
      <RouterView />
    </DefaultLayout>
    <AuthLayout v-else-if="isAuthLayout">
      <RouterView />
    </AuthLayout>
    <main v-else class="page-body">
      <RouterView />
    </main>
  </div>
</template>
