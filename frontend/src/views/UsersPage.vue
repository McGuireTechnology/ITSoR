<script setup>
import { onMounted, ref } from 'vue'
import { listUsers } from '../lib/api'

const users = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    users.value = await listUsers()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="panel">
    <h2>Users</h2>
    <p v-if="loading">Loading users...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="user in users" :key="user.id">
        <RouterLink :to="`/users/${user.id}`">{{ user.username }}</RouterLink>
        <span class="meta">{{ user.email }}</span>
      </li>
    </ul>
  </section>
</template>
