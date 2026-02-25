<script setup>
defineProps({
  isAuthenticated: {
    type: Boolean,
    required: true,
  },
})
</script>

<template>
  <header class="app-header">
    <h1>ITSoR Frontend</h1>
    <nav class="app-nav">
      <RouterLink v-if="!isAuthenticated" to="/login">Login</RouterLink>
      <RouterLink v-if="!isAuthenticated" to="/signup">Signup</RouterLink>
      <RouterLink to="/tenants">Tenants</RouterLink>
      <RouterLink to="/users">Users</RouterLink>
      <RouterLink to="/users/me">Users Me</RouterLink>
      <RouterLink v-if="isAuthenticated" to="/logout">Logout</RouterLink>
    </nav>
    <p class="auth-state">Auth: {{ isAuthenticated ? 'signed in' : 'signed out' }}</p>
  </header>

  <main class="page-body">
    <slot />
  </main>
</template>
