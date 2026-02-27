<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { commandSurfaceMetrics } from '../lib/commandSurface'
import {
  openGroupDeleteInspector,
  openGroupCreateInspector,
  openGroupEditInspector,
  openGroupMultiEditInspector,
  openTenantDeleteInspector,
  openTenantCreateInspector,
  openTenantEditInspector,
  openTenantMultiEditInspector,
  openUserDeleteInspector,
  openUserCreateInspector,
  openUserEditInspector,
  openUserMultiEditInspector,
} from '../lib/inspectorActions'
import { useDomainPermissions } from '../lib/permissions'

const route = useRoute()
const router = useRouter()

const domain = computed(() => route.meta.domain)
const selectedId = computed(() => route.params.id || null)
const showMetrics = computed(() => Number.isFinite(commandSurfaceMetrics.total))
const { canWrite } = useDomainPermissions(domain)
const isUserDetailRoute = computed(() => /^\/platform\/users\/[^/]+(?:\/.*)?$/.test(route.path) && route.path !== '/platform/users/me')
const isUsersListRoute = computed(() => route.path === '/platform/users')
const isGroupsListRoute = computed(() => route.path === '/platform/groups')
const isTenantsListRoute = computed(() => route.path === '/platform/tenants')
const selectedIds = computed(() => commandSurfaceMetrics.selectedIds || [])

const listPath = computed(() => (domain.value ? `/${domain.value}` : '/'))

async function openList() {
  await router.push(listPath.value)
}

function handleCreate() {
  if (!canWrite.value) {
    return
  }
  if (isUsersListRoute.value) {
    openUserCreateInspector()
    return
  }

  if (isGroupsListRoute.value) {
    openGroupCreateInspector()
    return
  }

  if (isTenantsListRoute.value) {
    openTenantCreateInspector()
  }
}

function handleEdit() {
  if (!canWrite.value) {
    return
  }

  if (isUsersListRoute.value) {
    if (selectedIds.value.length > 1) {
      openUserMultiEditInspector(selectedIds.value)
      return
    }
    if (selectedIds.value.length === 1) {
      openUserEditInspector(selectedIds.value[0])
      return
    }
  }

  if (isGroupsListRoute.value) {
    if (selectedIds.value.length > 1) {
      openGroupMultiEditInspector(selectedIds.value)
      return
    }
    if (selectedIds.value.length === 1) {
      openGroupEditInspector(selectedIds.value[0])
      return
    }
  }

  if (isTenantsListRoute.value) {
    if (selectedIds.value.length > 1) {
      openTenantMultiEditInspector(selectedIds.value)
      return
    }
    if (selectedIds.value.length === 1) {
      openTenantEditInspector(selectedIds.value[0])
      return
    }
  }
}

function handleDelete() {
  if (!canWrite.value) {
    return
  }

  if (isUsersListRoute.value) {
    if (selectedIds.value.length > 0) {
      openUserDeleteInspector(selectedIds.value)
    }
    return
  }

  if (isGroupsListRoute.value) {
    if (selectedIds.value.length > 0) {
      openGroupDeleteInspector(selectedIds.value)
    }
    return
  }

  if (isTenantsListRoute.value) {
    if (selectedIds.value.length > 0) {
      openTenantDeleteInspector(selectedIds.value)
    }
  }
}

async function refreshPage() {
  await router.replace({
    path: route.path,
    query: {
      ...route.query,
      _refresh: String(Date.now()),
    },
  })
}
</script>

<template>
  <div class="command-surface">
    <div class="command-primary">
      <button v-if="!isUserDetailRoute && !isUsersListRoute" type="button" :disabled="!canWrite" @click="openList"><span>＋</span><span>New</span></button>
      <button v-if="!isUserDetailRoute" type="button" :disabled="!canWrite" @click="handleCreate"><span>✚</span><span>Create</span></button>
      <button
        type="button"
        :disabled="!canWrite || ((isUsersListRoute || isGroupsListRoute || isTenantsListRoute) ? selectedIds.length === 0 : !selectedId)"
        @click="handleEdit"
      ><span>✎</span><span>Edit</span></button>
      <button
        type="button"
        :disabled="!canWrite || ((isUsersListRoute || isGroupsListRoute || isTenantsListRoute) ? selectedIds.length === 0 : !selectedId)"
        @click="handleDelete"
      ><span>🗑</span><span>Delete</span></button>
      <button v-if="!isUserDetailRoute" type="button"><span>⇩</span><span>Export</span></button>
      <button type="button" @click="refreshPage"><span>↻</span><span>Refresh</span></button>
    </div>

    <div v-if="showMetrics" class="command-metrics text-body-secondary small">
      <span>{{ commandSurfaceMetrics.total }} {{ commandSurfaceMetrics.noun }}</span>
      <span>{{ commandSurfaceMetrics.selected }} selected</span>
    </div>
  </div>
</template>
