<script setup>
import { onMounted, ref } from 'vue'
import { createGroup, listGroups } from '../lib/api'
import { formatNameId } from '../lib/formatters'

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
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Groups</h2>

    <form class="form" @submit.prevent="handleCreateGroup">
      <label>
        Group Name
        <input v-model="name" type="text" required />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Group' }}
      </button>
    </form>

    <p v-if="loading">Loading groups...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="group in groups" :key="group.id">
        <RouterLink :to="`/groups/${group.id}`">{{ formatNameId(group.name, group.id, '(unnamed group)') }}</RouterLink>
        <span class="meta">{{ group.id }} · owner: {{ group.owner_id || '-' }} · group: {{ group.group_id || '-' }} · perms: {{ group.permissions ?? '-' }}</span>
      </li>
    </ul>
  </section>
</template>
