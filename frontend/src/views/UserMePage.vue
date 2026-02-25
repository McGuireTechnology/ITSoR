<script setup>
import { onMounted, ref } from 'vue'
import { getCurrentUser } from '../lib/api'

const user = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    user.value = await getCurrentUser()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="panel">
    <h2>Current User</h2>
    <p v-if="loading">Loading current user...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <dl v-else class="user-detail">
      <dt>ID</dt>
      <dd>{{ user.id }}</dd>
      <dt>Username</dt>
      <dd>{{ user.username }}</dd>
      <dt>Email</dt>
      <dd>{{ user.email }}</dd>
    </dl>
  </section>
</template>
