<script setup>
import { onMounted, ref } from 'vue'
import { createTenant, listTenants } from '../lib/api'

const tenants = ref([])
const name = ref('')
const loading = ref(true)
const creating = ref(false)
const error = ref('')

async function loadTenants() {
  loading.value = true
  error.value = ''
  try {
    tenants.value = await listTenants()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateTenant() {
  creating.value = true
  error.value = ''
  try {
    const created = await createTenant({ name: name.value.trim() })
    tenants.value = [...tenants.value, created]
    name.value = ''
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

onMounted(loadTenants)
</script>

<template>
  <section class="panel">
    <h2>Tenants</h2>

    <form class="form" @submit.prevent="handleCreateTenant">
      <label>
        Tenant Name
        <input v-model="name" type="text" required />
      </label>
      <button type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Tenant' }}
      </button>
    </form>

    <p v-if="loading">Loading tenants...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="tenant in tenants" :key="tenant.id">
        <RouterLink :to="`/tenants/${tenant.id}`">{{ tenant.name }}</RouterLink>
        <span class="meta">{{ tenant.id }}</span>
      </li>
    </ul>
  </section>
</template>
