<script setup>
import { onMounted, ref, watch } from 'vue'
import { getGroupById, updateGroup } from '../../lib/api'
import { closeInspectorAction, notifyGroupsChanged } from '../../lib/inspectorActions'

const props = defineProps({
  groupId: {
    type: String,
    required: true,
  },
})

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const name = ref('')

async function loadGroup() {
  loading.value = true
  error.value = ''
  try {
    const group = await getGroupById(props.groupId)
    name.value = group.name || ''
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    await updateGroup(props.groupId, { name: name.value.trim() })
    notifyGroupsChanged()
    closeInspectorAction()
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    saving.value = false
  }
}

onMounted(loadGroup)
watch(() => props.groupId, loadGroup)
</script>

<template>
  <div>
    <p v-if="loading">Loading group...</p>
    <form v-else class="form" @submit.prevent="handleSubmit">
      <h3>Edit Group</h3>
      <label>
        Group Name
        <input v-model="name" type="text" required />
      </label>
      <div class="confirm-row">
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Group' }}
        </button>
        <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p v-if="error && loading" class="error">{{ error }}</p>
  </div>
</template>
