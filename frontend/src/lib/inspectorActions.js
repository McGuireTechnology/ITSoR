import { reactive } from 'vue'

export const inspectorState = reactive({
  mode: '',
  userId: '',
  userIds: [],
  groupId: '',
  groupIds: [],
  tenantId: '',
  tenantIds: [],
  usersRefreshTick: 0,
  groupsRefreshTick: 0,
  tenantsRefreshTick: 0,
})

function normalizeId(value) {
  return String(value || '').trim()
}

function normalizeIds(value) {
  if (!Array.isArray(value)) {
    return []
  }

  const seen = new Set()
  const normalizedIds = []

  for (const item of value) {
    const normalizedItem = normalizeId(item)
    if (!normalizedItem || seen.has(normalizedItem)) {
      continue
    }

    seen.add(normalizedItem)
    normalizedIds.push(normalizedItem)
  }

  return normalizedIds
}

function resetInspectorTargets() {
  inspectorState.userId = ''
  inspectorState.userIds = []
  inspectorState.groupId = ''
  inspectorState.groupIds = []
  inspectorState.tenantId = ''
  inspectorState.tenantIds = []
}

function setInspectorMode(mode) {
  inspectorState.mode = mode
}

export function closeInspectorAction() {
  setInspectorMode('')
  resetInspectorTargets()
}

export function openUserCreateInspector() {
  closeInspectorAction()
  setInspectorMode('user-create')
}

export function openUserEditInspector(userId) {
  const normalizedUserId = normalizeId(userId)
  if (!normalizedUserId) {
    return
  }

  closeInspectorAction()
  setInspectorMode('user-edit')
  inspectorState.userId = normalizedUserId
}

export function openUserMultiEditInspector(userIds) {
  const normalizedUserIds = normalizeIds(userIds)
  if (!normalizedUserIds.length) {
    return
  }

  closeInspectorAction()
  setInspectorMode('user-multiedit')
  inspectorState.userIds = normalizedUserIds
}

export function openUserDeleteInspector(userIds) {
  const normalizedUserIds = normalizeIds(userIds)
  if (!normalizedUserIds.length) {
    return
  }

  closeInspectorAction()
  setInspectorMode('user-delete')
  inspectorState.userIds = normalizedUserIds
}

export function openGroupCreateInspector() {
  closeInspectorAction()
  setInspectorMode('group-create')
}

export function openGroupEditInspector(groupId) {
  const normalizedGroupId = normalizeId(groupId)
  if (!normalizedGroupId) {
    return
  }

  closeInspectorAction()
  setInspectorMode('group-edit')
  inspectorState.groupId = normalizedGroupId
}

export function openGroupMultiEditInspector(groupIds) {
  const normalizedGroupIds = normalizeIds(groupIds)
  if (!normalizedGroupIds.length) {
    return
  }

  closeInspectorAction()
  setInspectorMode('group-multiedit')
  inspectorState.groupIds = normalizedGroupIds
}

export function openGroupDeleteInspector(groupIds) {
  const normalizedGroupIds = normalizeIds(groupIds)
  if (!normalizedGroupIds.length) {
    return
  }

  closeInspectorAction()
  setInspectorMode('group-delete')
  inspectorState.groupIds = normalizedGroupIds
}

export function openTenantCreateInspector() {
  closeInspectorAction()
  setInspectorMode('tenant-create')
}

export function openTenantEditInspector(tenantId) {
  const normalizedTenantId = normalizeId(tenantId)
  if (!normalizedTenantId) {
    return
  }

  closeInspectorAction()
  setInspectorMode('tenant-edit')
  inspectorState.tenantId = normalizedTenantId
}

export function openTenantMultiEditInspector(tenantIds) {
  const normalizedTenantIds = normalizeIds(tenantIds)
  if (!normalizedTenantIds.length) {
    return
  }

  closeInspectorAction()
  setInspectorMode('tenant-multiedit')
  inspectorState.tenantIds = normalizedTenantIds
}

export function openTenantDeleteInspector(tenantIds) {
  const normalizedTenantIds = normalizeIds(tenantIds)
  if (!normalizedTenantIds.length) {
    return
  }

  closeInspectorAction()
  setInspectorMode('tenant-delete')
  inspectorState.tenantIds = normalizedTenantIds
}

export function notifyUsersChanged() {
  inspectorState.usersRefreshTick += 1
}

export function notifyGroupsChanged() {
  inspectorState.groupsRefreshTick += 1
}

export function notifyTenantsChanged() {
  inspectorState.tenantsRefreshTick += 1
}
