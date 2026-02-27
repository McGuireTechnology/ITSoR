<script setup>
import { computed, onMounted, ref } from 'vue'
import { deleteTenant, getTenantById } from '../../lib/api'
import { closeInspectorAction, notifyTenantsChanged } from '../../lib/inspectorActions'

const props = defineProps({
  tenantIds: {
    type: Array,
    required: true,
  },
})

const deleting = ref(false)
const error = ref('')
const previewRows = ref([])
const count = computed(() => props.tenantIds.length)

async function loadPreview() {
  previewRows.value = []
  const loaded = await Promise.all(
    props.tenantIds.map(async (tenantId) => {
      try {
        const tenant = await getTenantById(String(tenantId))
        return {
          id: String(tenantId),
          label: tenant.name || String(tenantId),
        }
      } catch {
        return {
          id: String(tenantId),
          label: String(tenantId),
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
    for (const tenantId of props.tenantIds) {
      await deleteTenant(String(tenantId))
    }
    notifyTenantsChanged()
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
    <h3>Delete Tenants</h3>
    <p class="error">Delete {{ count }} selected tenant(s)? This cannot be undone.</p>
    <ul v-if="previewRows.length" class="user-list">
      <li v-for="row in previewRows" :key="row.id">
        <span>{{ row.label }}</span>
        <span class="meta">{{ row.id }}</span>
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
