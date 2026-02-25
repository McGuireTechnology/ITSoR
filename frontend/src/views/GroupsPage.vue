<script setup>
import { onMounted, ref } from 'vue'
import { createGroup, listGroups } from '../lib/api'

const groups = ref([])
const name = ref('')
const loading = ref(true)
const creating = ref(false)
const error = ref('')

async function loadGroups() {
  loading.value = true
  error.value = ''
  try {
    groups.value = await listGroups()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateGroup() {
  creating.value = true
  error.value = ''
  try {
    const created = await createGroup({ name: name.value.trim() })
    groups.value = [...groups.value, created]
    name.value = ''
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

onMounted(loadGroups)
</script>

<template>
  <section class="panel">
    <h2>Groups</h2>

    <form class="form" @submit.prevent="handleCreateGroup">
      <label>
        Group Name
        <input v-model="name" type="text" required />
      </label>
      <button type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Group' }}
      </button>
    </form>

    <p v-if="loading">Loading groups...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="group in groups" :key="group.id">
        <RouterLink :to="`/groups/${group.id}`">{{ group.name }}</RouterLink>
        <span class="meta">{{ group.id }}</span>
      </li>
    </ul>
  </section>
</template>
