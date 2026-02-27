<script setup>
import { ref } from 'vue'
import { getGroupById, updateGroup } from '../../lib/api'
import { closeInspectorAction, notifyGroupsChanged } from '../../lib/inspectorActions'

const props = defineProps({
  groupIds: {
    type: Array,
    required: true,
  },
})

const saving = ref(false)
const error = ref('')
const prefix = ref('')

async function handleSubmit() {
  if (!prefix.value.trim()) {
    error.value = 'Name prefix is required for multi-edit.'
    return
  }

  saving.value = true
  error.value = ''
  try {
    for (const groupId of props.groupIds) {
      const group = await getGroupById(String(groupId))
      await updateGroup(String(groupId), {
        name: `${prefix.value.trim()}${group.name || ''}`,
      })
    }
    notifyGroupsChanged()
    closeInspectorAction()
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="form" @submit.prevent="handleSubmit">
    <h3>Multi-Edit Groups</h3>
    <p class="meta">Applying update to {{ groupIds.length }} selected groups.</p>
    <label>
      Name Prefix
      <input v-model="prefix" type="text" required />
    </label>
    <div class="confirm-row">
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="saving || !groupIds.length">
        {{ saving ? 'Applying...' : 'Apply to Selected' }}
      </button>
      <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" :disabled="saving" @click="closeInspectorAction">Cancel</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
