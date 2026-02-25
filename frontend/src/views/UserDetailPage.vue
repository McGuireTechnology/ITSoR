<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getUserById } from '../lib/api'

const route = useRoute()

const user = ref(null)
const loading = ref(true)
const error = ref('')

async function loadUser() {
  loading.value = true
  error.value = ''
  user.value = null

  try {
    user.value = await getUserById(route.params.id)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadUser)

watch(
  () => route.params.id,
  () => {
    loadUser()
  },
)
</script>

<template>
  <section class="panel">
    <h2>User Detail</h2>
    <p v-if="loading">Loading user...</p>
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
