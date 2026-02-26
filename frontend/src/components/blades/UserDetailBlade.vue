<script setup>
import { onMounted, ref, watch } from 'vue'
import { getUserById } from '../../lib/api'
import { formatNameId } from '../../lib/formatters'
import { useBladeStack } from '../../lib/blades'
import UserEditBlade from './UserEditBlade.vue'

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
  bladeId: {
    type: String,
    required: true,
  },
})

const bladeStack = useBladeStack()

const user = ref(null)
const loading = ref(true)
const error = ref('')

async function loadUser() {
  loading.value = true
  error.value = ''
  user.value = null
  try {
    user.value = await getUserById(props.userId)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

function openEditBlade() {
  if (!bladeStack || !user.value) {
    return
  }

  const editBladeId = `user-edit-${user.value.id}`
  bladeStack.closeBlade(editBladeId)
  bladeStack.openBlade({
    id: editBladeId,
    parentId: props.bladeId,
    type: 'edit',
    title: `Edit ${user.value.username || user.value.id}`,
    subtitle: user.value.email || '',
    component: UserEditBlade,
    props: {
      userId: user.value.id,
      bladeId: editBladeId,
      onSaved: loadUser,
    },
  })
}

onMounted(loadUser)

watch(
  () => props.userId,
  () => {
    loadUser()
  },
)
</script>

<template>
  <div>
    <p v-if="loading">Loading user...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <dl v-else class="user-detail">
      <dt>ID</dt>
      <dd>{{ user.id }}</dd>
      <dt>Username</dt>
      <dd>{{ formatNameId(user.username, user.id, '(unnamed user)') }}</dd>
      <dt>Email</dt>
      <dd>{{ user.email }}</dd>
    </dl>

    <div v-if="user" class="section-gap confirm-row">
      <button type="button" class="btn btn-sm btn-primary bg-primary hover:bg-accent border-0" @click="openEditBlade">Edit User</button>
    </div>
  </div>
</template>
