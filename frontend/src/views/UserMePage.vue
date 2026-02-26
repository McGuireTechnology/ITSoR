<script setup>
import { onMounted, ref } from 'vue'
import { getCurrentUser } from '../lib/api'
import { formatNameId } from '../lib/formatters'

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
  <section class="container-fluid py-3 px-2 px-md-3">
    <div class="card shadow-sm border-0 rounded-4 bg-brand-surface/70">
      <div class="card-body p-4">
        <h2 class="h3 fw-bold mb-3 text-brand-deep">Current User</h2>

        <p v-if="loading" class="text-body-secondary mb-0">Loading current user...</p>
        <div v-else-if="error" class="alert alert-danger mb-0" role="alert">{{ error }}</div>

        <dl v-else class="row mb-0 g-2">
          <dt class="col-12 col-sm-3 text-body-secondary">ID</dt>
          <dd class="col-12 col-sm-9 mb-1">{{ user.id }}</dd>
          <dt class="col-12 col-sm-3 text-body-secondary">Username</dt>
          <dd class="col-12 col-sm-9 mb-1">{{ formatNameId(user.username, user.id, '(unnamed user)') }}</dd>
          <dt class="col-12 col-sm-3 text-body-secondary">Email</dt>
          <dd class="col-12 col-sm-9 mb-0">{{ user.email }}</dd>
        </dl>
      </div>
    </div>
  </section>
</template>
