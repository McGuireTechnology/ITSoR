<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import WorkspaceDetailBlade from '../components/blades/WorkspaceDetailBlade.vue'
import { createWorkspace, listWorkspaces } from '../lib/api'
import { useBladeStack } from '../lib/blades'
import { formatNameId } from '../lib/formatters'
import { useDomainPermissions } from '../lib/permissions'

const router = useRouter()
const bladeStack = useBladeStack()
const workspaces = ref([])
const domain = ref('workspaces')
const { canWrite } = useDomainPermissions(domain)
const name = ref('')
const tenantId = ref('')
const loading = ref(true)
const creating = ref(false)
const error = ref('')

async function loadWorkspaces() {
  loading.value = true
  error.value = ''
  try {
    workspaces.value = await listWorkspaces()
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreateWorkspace() {
  if (!canWrite.value) {
    return
  }

  creating.value = true
  error.value = ''
  try {
    const created = await createWorkspace({
      name: name.value.trim(),
      tenant_id: tenantId.value.trim() || null,
    })
    workspaces.value = [...workspaces.value, created]
    name.value = ''
    tenantId.value = ''
  } catch (createError) {
    error.value = createError.message
  } finally {
    creating.value = false
  }
}

function openWorkspace(workspace) {
  if (!workspace?.id) {
    return
  }

  const workspaceId = String(workspace.id)
  const bladeId = `workspace-detail-${workspaceId}`

  router.push(`/customization/workspaces/${workspaceId}`)

  if (!bladeStack) {
    return
  }

  bladeStack.closeBlade(bladeId)
  bladeStack.openBlade({
    id: bladeId,
    type: 'detail',
    title: formatNameId(workspace.name, workspace.id, '(unnamed workspace)'),
    subtitle: workspace.id,
    component: WorkspaceDetailBlade,
    props: {
      workspaceId,
      bladeId,
    },
  })
}

onMounted(loadWorkspaces)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">Workspaces</h2>

    <form v-if="canWrite" class="form" @submit.prevent="handleCreateWorkspace">
      <label>
        Workspace Name
        <input v-model="name" type="text" required />
      </label>
      <label>
        Tenant ID (optional)
        <input v-model="tenantId" type="text" />
      </label>
      <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
        {{ creating ? 'Creating...' : 'Create Workspace' }}
      </button>
    </form>

    <p v-if="loading">Loading workspaces...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <ul v-else class="user-list">
      <li v-for="workspace in workspaces" :key="workspace.id">
        <button class="btn btn-link p-0" type="button" @click="openWorkspace(workspace)">
          {{ formatNameId(workspace.name, workspace.id, '(unnamed workspace)') }}
        </button>
        <span class="meta">{{ workspace.id }} · owner: {{ workspace.owner_id || '-' }} · group: {{ workspace.group_id || '-' }} · perms: {{ workspace.permissions ?? '-' }}</span>
      </li>
    </ul>
  </section>
</template>
