<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getGroupById, getUserById } from '../lib/api'
import { getListPathForDomain, getWorkspaceForDomain, workspaceConfig } from '../lib/workspaceNav'

const route = useRoute()

const userCrumbLabel = ref('')
const groupCrumbLabel = ref('')

const namespaceLabelByDomain = {
  auth_home: 'Overview',
  users: 'Users',
  groups: 'Groups',
  roles: 'Roles',
  permissions: 'Permissions',
  tenants: 'Tenants',
  idm_home: 'Overview',
  idm_people: 'People',
  idm_identities: 'Identities',
  idm_users: 'Users',
  idm_groups: 'Groups',
  idm_group_memberships: 'Group Memberships',
  customization_home: 'Overview',
  workspaces: 'Workspaces',
  namespaces: 'Namespaces',
  'entity-types': 'Entity Types',
  'entity-records': 'Entity Records',
}

const isUserDetailRoute = computed(() => /^\/auth\/users\/[^/]+(?:\/.*)?$/.test(route.path) && route.path !== '/auth/users/me')
const isGroupDetailRoute = computed(() => /^\/auth\/groups\/[^/]+(?:\/.*)?$/.test(route.path))
const isRoleDetailRoute = computed(() => /^\/auth\/roles\/[^/]+(?:\/.*)?$/.test(route.path))
const isPermissionDetailRoute = computed(() => /^\/auth\/permissions\/[^/]+(?:\/.*)?$/.test(route.path))

const pageTitle = computed(() => {
  if (isUserDetailRoute.value) {
    const label = userCrumbLabel.value || String(route.params.id || '')
    return `User: ${label}`
  }
  if (isGroupDetailRoute.value) {
    const label = groupCrumbLabel.value || String(route.params.id || '')
    return `Group: ${label}`
  }
  if (isRoleDetailRoute.value) {
    return `Role: ${String(route.params.id || '')}`
  }
  if (isPermissionDetailRoute.value) {
    return `Permission: ${String(route.params.id || '')}`
  }
  return route.meta.title || 'Workspace'
})

const tabs = computed(() => {
  if (isUserDetailRoute.value) {
    const userId = String(route.params.id || '')
    return [
      { label: 'Overview', to: `/auth/users/${userId}` },
      { label: 'Group Membership', to: `/auth/users/${userId}/group-membership` },
      { label: 'User Roles', to: `/auth/users/${userId}/user-roles` },
      { label: 'User Tenants', to: `/auth/users/${userId}/user-tenants` },
    ]
  }
  if (isGroupDetailRoute.value) {
    const groupId = String(route.params.id || '')
    return [
      { label: 'Overview', to: `/auth/groups/${groupId}` },
      { label: 'Group Memberships', to: `/auth/groups/${groupId}/group-memberships` },
      { label: 'Group Roles', to: `/auth/groups/${groupId}/group-roles` },
    ]
  }
  if (isRoleDetailRoute.value) {
    const roleId = String(route.params.id || '')
    return [
      { label: 'Overview', to: `/auth/roles/${roleId}` },
      { label: 'Role Permissions', to: `/auth/roles/${roleId}/role-permissions` },
    ]
  }
  return []
})

const showTabs = computed(() => isUserDetailRoute.value || isGroupDetailRoute.value || isRoleDetailRoute.value)

async function loadUserCrumb() {
  userCrumbLabel.value = ''
  if (!isUserDetailRoute.value || !route.params.id) {
    return
  }

  try {
    const user = await getUserById(route.params.id)
    userCrumbLabel.value = user?.username || user?.email || String(route.params.id)
  } catch {
    userCrumbLabel.value = String(route.params.id)
  }
}

async function loadGroupCrumb() {
  groupCrumbLabel.value = ''
  if (!isGroupDetailRoute.value || !route.params.id) {
    return
  }

  try {
    const group = await getGroupById(route.params.id)
    groupCrumbLabel.value = group?.name || String(route.params.id)
  } catch {
    groupCrumbLabel.value = String(route.params.id)
  }
}

onMounted(async () => {
  await loadUserCrumb()
  await loadGroupCrumb()
})

watch(
  () => route.fullPath,
  () => {
    loadUserCrumb()
    loadGroupCrumb()
  },
)

const breadcrumbs = computed(() => {
  const domain = String(route.meta?.domain || '')
  const chain = []

  if (domain) {
    const namespacePath = getListPathForDomain(domain)
    const workspaceKey = getWorkspaceForDomain(domain)
    if (workspaceKey) {
      chain.push({ label: workspaceConfig[workspaceKey].label, to: namespacePath || '/' })
    }

    const namespaceLabel = namespaceLabelByDomain[domain] || (route.meta?.title || 'Section')
    chain.push({ label: namespaceLabel, to: namespacePath || '/' })

    if (isUserDetailRoute.value) {
      chain.push({ label: userCrumbLabel.value || String(route.params.id || ''), to: route.fullPath })
    }

    if (isGroupDetailRoute.value) {
      chain.push({ label: groupCrumbLabel.value || String(route.params.id || ''), to: route.fullPath })
    }

    return chain
  }

  if (route.path === '/home' || route.path === '/') {
    return [{ label: 'Home', to: '/home' }]
  }

  chain.push({ label: 'Home', to: '/home' })
  for (const matched of route.matched) {
    if (!matched.path || matched.path === '/') {
      continue
    }
    const label = matched.meta?.title || matched.path.replace('/', '')
    const path = matched.path.replace(':id', route.params.id || '')
    chain.push({ label, to: path })
  }
  return chain
})
</script>

<template>
  <header class="page-header">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <span v-for="(crumb, index) in breadcrumbs" :key="`${crumb.to}-${index}`">
        <RouterLink :to="crumb.to">{{ crumb.label }}</RouterLink>
        <span v-if="index < breadcrumbs.length - 1" class="crumb-sep">›</span>
      </span>
    </nav>
    <div class="page-header-main">
      <h1>{{ pageTitle }}</h1>
    </div>
    <div v-if="showTabs" class="page-tabs" role="tablist" aria-label="Page tabs">
      <component
        v-for="(tab, index) in tabs"
        :key="tab.label"
        :is="tab.to ? 'RouterLink' : 'span'"
        :to="tab.to || undefined"
        class="page-tab"
        :class="{ 'page-tab-active': tab.to ? route.path === tab.to : index === 0 }"
      >
        {{ tab.label }}
      </component>
    </div>
  </header>
</template>
