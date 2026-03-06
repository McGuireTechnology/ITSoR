<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getUserById } from '../lib/api'
import UserCreateInspectorForm from './inspector/UserCreateInspectorForm.vue'
import UserDeleteInspectorForm from './inspector/UserDeleteInspectorForm.vue'
import UserEditInspectorForm from './inspector/UserEditInspectorForm.vue'
import UserMultiEditInspectorForm from './inspector/UserMultiEditInspectorForm.vue'
import GroupCreateInspectorForm from './inspector/GroupCreateInspectorForm.vue'
import GroupDeleteInspectorForm from './inspector/GroupDeleteInspectorForm.vue'
import GroupEditInspectorForm from './inspector/GroupEditInspectorForm.vue'
import GroupMultiEditInspectorForm from './inspector/GroupMultiEditInspectorForm.vue'
import TenantCreateInspectorForm from './inspector/TenantCreateInspectorForm.vue'
import TenantDeleteInspectorForm from './inspector/TenantDeleteInspectorForm.vue'
import TenantEditInspectorForm from './inspector/TenantEditInspectorForm.vue'
import TenantMultiEditInspectorForm from './inspector/TenantMultiEditInspectorForm.vue'
import { inspectorState } from '../lib/inspectorActions'
import { getListPathForDomain } from '../lib/workspaceNav'

const route = useRoute()

const sectionTitle = computed(() => route.meta.title || 'Details')
const selectedId = computed(() => route.params.id || null)
const inspectedUserId = computed(() => String(route.query.inspectUserId || ''))
const domain = computed(() => route.meta.domain || '')
const listPath = computed(() => getListPathForDomain(domain.value) || '/')
const inspectedUserName = ref('')

async function loadInspectedUserName() {
  inspectedUserName.value = ''

  if (domain.value !== 'users' || !inspectedUserId.value) {
    return
  }

  try {
    const user = await getUserById(inspectedUserId.value)
    inspectedUserName.value = user?.username || user?.email || inspectedUserId.value
  } catch {
    inspectedUserName.value = inspectedUserId.value
  }
}

onMounted(loadInspectedUserName)

watch(
  () => [domain.value, inspectedUserId.value],
  () => {
    loadInspectedUserName()
  },
)

const inspectedUserRoute = computed(() => {
  if (domain.value !== 'users' || !inspectedUserId.value) {
    return null
  }
  return `/auth/users/${inspectedUserId.value}`
})

const isUsersListRoute = computed(() => route.path === '/auth/users')
const isGroupsListRoute = computed(() => route.path === '/auth/groups')
const isTenantsListRoute = computed(() => route.path === '/auth/tenants')

const inspectorComponent = computed(() => {
  if (isUsersListRoute.value) {
    if (inspectorState.mode === 'user-create') {
      return UserCreateInspectorForm
    }
    if (inspectorState.mode === 'user-edit' && inspectorState.userId) {
      return UserEditInspectorForm
    }
    if (inspectorState.mode === 'user-multiedit' && inspectorState.userIds.length > 0) {
      return UserMultiEditInspectorForm
    }
    if (inspectorState.mode === 'user-delete' && inspectorState.userIds.length > 0) {
      return UserDeleteInspectorForm
    }
  }

  if (isGroupsListRoute.value) {
    if (inspectorState.mode === 'group-create') {
      return GroupCreateInspectorForm
    }
    if (inspectorState.mode === 'group-edit' && inspectorState.groupId) {
      return GroupEditInspectorForm
    }
    if (inspectorState.mode === 'group-multiedit' && inspectorState.groupIds.length > 0) {
      return GroupMultiEditInspectorForm
    }
    if (inspectorState.mode === 'group-delete' && inspectorState.groupIds.length > 0) {
      return GroupDeleteInspectorForm
    }
  }

  if (isTenantsListRoute.value) {
    if (inspectorState.mode === 'tenant-create') {
      return TenantCreateInspectorForm
    }
    if (inspectorState.mode === 'tenant-edit' && inspectorState.tenantId) {
      return TenantEditInspectorForm
    }
    if (inspectorState.mode === 'tenant-multiedit' && inspectorState.tenantIds.length > 0) {
      return TenantMultiEditInspectorForm
    }
    if (inspectorState.mode === 'tenant-delete' && inspectorState.tenantIds.length > 0) {
      return TenantDeleteInspectorForm
    }
  }

  return null
})

const inspectorProps = computed(() => {
  if (inspectorState.mode === 'user-edit') {
    return { userId: inspectorState.userId }
  }
  if (inspectorState.mode === 'user-multiedit') {
    return { userIds: inspectorState.userIds }
  }
  if (inspectorState.mode === 'group-edit') {
    return { groupId: inspectorState.groupId }
  }
  if (inspectorState.mode === 'group-multiedit') {
    return { groupIds: inspectorState.groupIds }
  }
  if (inspectorState.mode === 'tenant-edit') {
    return { tenantId: inspectorState.tenantId }
  }
  if (inspectorState.mode === 'tenant-multiedit') {
    return { tenantIds: inspectorState.tenantIds }
  }
  return {}
})
</script>

<template>
  <div class="inspector-body pane-body">
    <component :is="inspectorComponent" v-if="inspectorComponent" v-bind="inspectorProps" />

    <template v-else>
    <dl class="inspector-detail">
      <dt>Section</dt>
      <dd>{{ sectionTitle }}</dd>
      <dt>Route</dt>
      <dd>{{ route.path }}</dd>
      <dt>Selected ID</dt>
      <dd>{{ selectedId || 'None selected' }}</dd>
      <template v-if="inspectedUserId">
        <dt>Inspected User</dt>
        <dd>{{ inspectedUserName || inspectedUserId }}</dd>
      </template>
    </dl>

    <div class="section-gap">
      <RouterLink class="pane-link" :to="listPath">Open section list</RouterLink>
      <RouterLink v-if="inspectedUserRoute" class="pane-link" :to="inspectedUserRoute">Open inspected user</RouterLink>
    </div>
    </template>
  </div>
</template>
