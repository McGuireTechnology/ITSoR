<script setup>
import { computed, onMounted, ref } from 'vue'
import { deleteUser, getUserById } from '../../lib/api'
import { closeInspectorAction, notifyUsersChanged } from '../../lib/inspectorActions'

const props = defineProps({
  userIds: {
    type: Array,
    required: true,
  },
})

const deleting = ref(false)
const error = ref('')
const previewRows = ref([])
const count = computed(() => props.userIds.length)

async function loadPreview() {
  previewRows.value = []
  const loaded = await Promise.all(
    props.userIds.map(async (userId) => {
      try {
        const user = await getUserById(String(userId))
        return {
          id: String(userId),
          label: user.username || user.email || String(userId),
          detail: user.email || '',
        }
      } catch {
        return {
          id: String(userId),
          label: String(userId),
          detail: '',
        }
      }
    }),
  )
  previewRows.value = loaded
}

async function handleDelete() {
  deleting.value = true
  error.value = ''
  try {
    for (const userId of props.userIds) {
      await deleteUser(String(userId))
    }
    notifyUsersChanged()
    closeInspectorAction()
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    deleting.value = false
  }
}

onMounted(loadPreview)
</script>

<template>
  <div class="form">
    <h3>Delete Users</h3>
    <p class="error">Delete {{ count }} selected user(s)? This cannot be undone.</p>
    <ul v-if="previewRows.length" class="user-list">
      <li v-for="row in previewRows" :key="row.id">
        <span>{{ row.label }}</span>
        <span class="meta">{{ row.id }}<template v-if="row.detail"> · {{ row.detail }}</template></span>
      </li>
    </ul>
    <div class="confirm-row">
      <button class="btn btn-primary bg-accent hover:bg-primary border-0" type="button" :disabled="deleting || !count" @click="handleDelete">
        {{ deleting ? 'Deleting...' : 'Confirm Delete' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="deleting" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>
