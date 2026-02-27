<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getGroupById, getUserById } from '../lib/api'

const route = useRoute()

const user = ref(null)
const group = ref(null)
const loading = ref(true)
const error = ref('')

async function loadMembership() {
  loading.value = true
  error.value = ''
  user.value = null
  group.value = null

  try {
    const loadedUser = await getUserById(route.params.id)
    user.value = loadedUser

    if (loadedUser.group_id) {
      group.value = await getGroupById(loadedUser.group_id)
    }
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadMembership)
watch(() => route.params.id, loadMembership)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <p v-if="loading">Loading group membership...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <dl class="user-detail">
        <dt>User ID</dt>
        <dd>{{ user?.id }}</dd>
        <dt>Username</dt>
        <dd>{{ user?.username || '-' }}</dd>
        <dt>Group ID</dt>
        <dd>{{ user?.group_id || 'No group assigned' }}</dd>
      </dl>

      <dl v-if="group" class="user-detail section-gap">
        <dt>Group Name</dt>
        <dd>
          <RouterLink :to="`/platform/groups/${group.id}`">{{ group.name }}</RouterLink>
        </dd>
        <dt>Tenant ID</dt>
        <dd>{{ group.tenant_id || '-' }}</dd>
      </dl>
    </template>
  </section>
</template>
