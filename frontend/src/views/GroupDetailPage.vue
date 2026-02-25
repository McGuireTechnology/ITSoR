<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteGroup, getGroupById, updateGroup } from '../lib/api'

const route = useRoute()
const router = useRouter()

const group = ref(null)
const name = ref('')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')

async function loadGroup() {
  loading.value = true
  error.value = ''
  try {
    const loaded = await getGroupById(route.params.id)
    group.value = loaded
    name.value = loaded.name
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!group.value) {
    return
  }

  saving.value = true
  error.value = ''
  try {
    group.value = await updateGroup(group.value.id, { name: name.value.trim() })
    name.value = group.value.name
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!group.value) {
    return
  }

  deleting.value = true
  error.value = ''
  try {
    await deleteGroup(group.value.id)
    await router.push('/groups')
  } catch (deleteError) {
    error.value = deleteError.message
  } finally {
    deleting.value = false
  }
}

function startDeleteConfirmation() {
  confirmingDelete.value = true
}

function cancelDeleteConfirmation() {
  confirmingDelete.value = false
}

onMounted(loadGroup)

watch(
  () => route.params.id,
  () => {
    loadGroup()
  },
)
</script>

<template>
  <section class="panel">
    <h2>Group Detail</h2>
    <p v-if="loading">Loading group...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <form class="form" @submit.prevent="handleSave">
        <label>
          Name
          <input v-model="name" type="text" required />
        </label>
        <button type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ group.id }}</dd>
      </dl>

      <div class="section-gap">
        <button
          v-if="!confirmingDelete"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete Group
        </button>

        <div v-else class="confirm-row">
          <p class="error">Delete group "{{ group.name }}"?</p>
          <button type="button" :disabled="deleting" @click="handleDelete">
            {{ deleting ? 'Deleting...' : 'Confirm Delete' }}
          </button>
          <button type="button" :disabled="deleting" @click="cancelDeleteConfirmation">
            Cancel
          </button>
        </div>
      </div>
    </template>
  </section>
</template>
