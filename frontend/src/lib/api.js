import { getToken, getTokenSubject } from './auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request(path, { method = 'GET', body, requiresAuth = true } = {}) {
  const headers = {}
  if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
  }

  if (requiresAuth) {
    const token = getToken()
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    credentials: 'include',
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  if (response.status === 204) {
    return null
  }

  const contentType = response.headers.get('content-type') || ''
  const payload = contentType.includes('application/json')
    ? await response.json()
    : await response.text()

  if (!response.ok) {
    if (payload && typeof payload === 'object' && 'detail' in payload) {
      throw new Error(String(payload.detail))
    }
    throw new Error(typeof payload === 'string' && payload ? payload : `Request failed (${response.status})`)
  }

  return payload
}

export function signupUser({ username, email, password }) {
  return request('/signup', {
    method: 'POST',
    body: { username, email, password },
    requiresAuth: false,
  })
}

export function loginUser({ identifier, password }) {
  return request('/login', {
    method: 'POST',
    body: { identifier, password },
    requiresAuth: false,
  })
}

export function logoutUser() {
  return request('/logout', { method: 'POST' })
}

export function listUsers() {
  return request('/users')
}

export function listTenants() {
  return request('/tenants')
}

export function createTenant({ name }) {
  return request('/tenants', {
    method: 'POST',
    body: { name },
  })
}

export function getTenantById(tenantId) {
  return request(`/tenants/${tenantId}`)
}

export function updateTenant(tenantId, { name }) {
  return request(`/tenants/${tenantId}`, {
    method: 'PATCH',
    body: { name },
  })
}

export function deleteTenant(tenantId) {
  return request(`/tenants/${tenantId}`, {
    method: 'DELETE',
  })
}

export function getUserById(userId) {
  return request(`/users/${userId}`)
}

export async function getCurrentUser() {
  const userId = getTokenSubject(getToken())
  if (!userId) {
    throw new Error('No logged-in user token found')
  }
  return getUserById(userId)
}

function withQuery(path, query) {
  const params = new URLSearchParams()

  for (const [key, value] of Object.entries(query || {})) {
    if (value === undefined || value === null || value === '') {
      continue
    }
    params.set(key, String(value))
  }

  const queryString = params.toString()
  return queryString ? `${path}?${queryString}` : path
}

export function updateUser(userId, payload) {
  return request(`/users/${userId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function listGroups() {
  return request('/groups')
}

export function createGroup(payload) {
  return request('/groups', {
    method: 'POST',
    body: payload,
  })
}

export function getGroupById(groupId) {
  return request(`/groups/${groupId}`)
}

export function updateGroup(groupId, payload) {
  return request(`/groups/${groupId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteGroup(groupId) {
  return request(`/groups/${groupId}`, {
    method: 'DELETE',
  })
}

export function listWorkspaces(filters = {}) {
  return request(withQuery('/workspaces', {
    tenant_id: filters.tenantId,
  }))
}

export function createWorkspace(payload) {
  return request('/workspaces', {
    method: 'POST',
    body: payload,
  })
}

export function getWorkspaceById(workspaceId) {
  return request(`/workspaces/${workspaceId}`)
}

export function updateWorkspace(workspaceId, payload) {
  return request(`/workspaces/${workspaceId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteWorkspace(workspaceId) {
  return request(`/workspaces/${workspaceId}`, {
    method: 'DELETE',
  })
}

export function listNamespaces(filters = {}) {
  return request(withQuery('/namespaces', {
    workspace_id: filters.workspaceId,
  }))
}

export function createNamespace(payload) {
  return request('/namespaces', {
    method: 'POST',
    body: payload,
  })
}

export function getNamespaceById(namespaceId) {
  return request(`/namespaces/${namespaceId}`)
}

export function updateNamespace(namespaceId, payload) {
  return request(`/namespaces/${namespaceId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteNamespace(namespaceId) {
  return request(`/namespaces/${namespaceId}`, {
    method: 'DELETE',
  })
}

export function listEntityTypes(filters = {}) {
  return request(withQuery('/entity-types', {
    namespace_id: filters.namespaceId,
  }))
}

export function createEntityType(payload) {
  return request('/entity-types', {
    method: 'POST',
    body: payload,
  })
}

export function getEntityTypeById(entityTypeId) {
  return request(`/entity-types/${entityTypeId}`)
}

export function updateEntityType(entityTypeId, payload) {
  return request(`/entity-types/${entityTypeId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteEntityType(entityTypeId) {
  return request(`/entity-types/${entityTypeId}`, {
    method: 'DELETE',
  })
}

export function listEntityRecords(filters = {}) {
  return request(withQuery('/entity-records', {
    entity_type_id: filters.entityTypeId,
    field: filters.field,
    value: filters.value,
    operator: filters.operator,
  }))
}

export function createEntityRecord(payload) {
  return request('/entity-records', {
    method: 'POST',
    body: payload,
  })
}

export function getEntityRecordById(entityRecordId) {
  return request(`/entity-records/${entityRecordId}`)
}

export function updateEntityRecord(entityRecordId, payload) {
  return request(`/entity-records/${entityRecordId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteEntityRecord(entityRecordId) {
  return request(`/entity-records/${entityRecordId}`, {
    method: 'DELETE',
  })
}

export function createUser(payload) {
  return request('/users', {
    method: 'POST',
    body: payload,
  })
}

export function deleteUser(userId) {
  return request(`/users/${userId}`, {
    method: 'DELETE',
  })
}

export function listRoles() {
  return request('/roles')
}

export function createRole(payload) {
  return request('/roles', {
    method: 'POST',
    body: payload,
  })
}

export function getRoleById(roleId) {
  return request(`/roles/${roleId}`)
}

export function updateRole(roleId, payload) {
  return request(`/roles/${roleId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteRole(roleId) {
  return request(`/roles/${roleId}`, {
    method: 'DELETE',
  })
}

export function listPermissions() {
  return request('/permissions')
}

export function createPermission(payload) {
  return request('/permissions', {
    method: 'POST',
    body: payload,
  })
}

export function getPermissionById(permissionId) {
  return request(`/permissions/${permissionId}`)
}

export function updatePermission(permissionId, payload) {
  return request(`/permissions/${permissionId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deletePermission(permissionId) {
  return request(`/permissions/${permissionId}`, {
    method: 'DELETE',
  })
}

export function listGroupMemberships(filters = {}) {
  return request(withQuery('/group_memberships', {
    group_id: filters.groupId,
    member_type: filters.memberType,
    member_user_id: filters.memberUserId,
    member_group_id: filters.memberGroupId,
  }))
}

export function createGroupMembership(payload) {
  return request('/group_memberships', {
    method: 'POST',
    body: payload,
  })
}

export function deleteGroupMembership(groupMembershipId) {
  return request(`/group_memberships/${groupMembershipId}`, {
    method: 'DELETE',
  })
}

export function listGroupRoles(filters = {}) {
  return request(withQuery('/group_roles', {
    group_id: filters.groupId,
    role_id: filters.roleId,
  }))
}

export function createGroupRole(payload) {
  return request('/group_roles', {
    method: 'POST',
    body: payload,
  })
}

export function deleteGroupRole(groupRoleId) {
  return request(`/group_roles/${groupRoleId}`, {
    method: 'DELETE',
  })
}

export function listRolePermissions(filters = {}) {
  return request(withQuery('/role_permissions', {
    role_id: filters.roleId,
    permission_id: filters.permissionId,
  }))
}

export function createRolePermission(payload) {
  return request('/role_permissions', {
    method: 'POST',
    body: payload,
  })
}

export function deleteRolePermission(rolePermissionId) {
  return request(`/role_permissions/${rolePermissionId}`, {
    method: 'DELETE',
  })
}

export function listUserRoles(filters = {}) {
  return request(withQuery('/user_roles', {
    user_id: filters.userId,
    role_id: filters.roleId,
  }))
}

export function createUserRole(payload) {
  return request('/user_roles', {
    method: 'POST',
    body: payload,
  })
}

export function deleteUserRole(userRoleId) {
  return request(`/user_roles/${userRoleId}`, {
    method: 'DELETE',
  })
}

export function listUserTenants(filters = {}) {
  return request(withQuery('/user_tenants', {
    user_id: filters.userId,
    tenant_id: filters.tenantId,
  }))
}

export function createUserTenant(payload) {
  return request('/user_tenants', {
    method: 'POST',
    body: payload,
  })
}

export function deleteUserTenant(userTenantId) {
  return request(`/user_tenants/${userTenantId}`, {
    method: 'DELETE',
  })
}

export function listEndpointPermissions(filters = {}) {
  return request(withQuery('/endpoint-permissions', {
    principal_type: filters.principalType ?? filters.principal_type,
    principal_id: filters.principalId ?? filters.principal_id,
    endpoint_name: filters.endpointName ?? filters.endpoint_name,
    action: filters.action,
  }))
}

export function createEndpointPermission(payload) {
  return request('/endpoint-permissions', {
    method: 'POST',
    body: payload,
  })
}

export function getEndpointPermissionById(endpointPermissionId) {
  return request(`/endpoint-permissions/${endpointPermissionId}`)
}

export function patchEndpointPermission(endpointPermissionId, payload) {
  return request(`/endpoint-permissions/${endpointPermissionId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteEndpointPermission(endpointPermissionId) {
  return request(`/endpoint-permissions/${endpointPermissionId}`, {
    method: 'DELETE',
  })
}

export function listIdmPeople() {
  return request('/idm/people')
}

export function listIdmIdentities() {
  return request('/idm/identities')
}

export function listIdmUsers() {
  return request('/idm/users')
}

export function listIdmGroups() {
  return request('/idm/groups')
}

export function listIdmGroupMemberships() {
  return request('/idm/group-memberships')
}

export function listNavigationTree(filters = {}) {
  return request(withQuery('/admin/navigation', {
    tenant_id: filters.tenantId,
    include_disabled: filters.includeDisabled,
  }))
}

export function loadNavigationDefaults(tenantId) {
  return request('/admin/navigation/load-defaults', {
    method: 'POST',
    body: {
      tenant_id: tenantId || null,
    },
  })
}

export function setNavigationDefault(payload) {
  return request('/admin/navigation/set-default', {
    method: 'POST',
    body: payload,
  })
}

export function createNavigationModule(payload) {
  return request('/admin/navigation/modules', {
    method: 'POST',
    body: payload,
  })
}

export function patchNavigationModule(moduleId, payload) {
  return request(`/admin/navigation/modules/${moduleId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteNavigationModule(moduleId, tenantId = null) {
  return request(withQuery(`/admin/navigation/modules/${moduleId}`, {
    tenant_id: tenantId,
  }), {
    method: 'DELETE',
  })
}

export function createNavigationResource(payload) {
  return request('/admin/navigation/resources', {
    method: 'POST',
    body: payload,
  })
}

export function patchNavigationResource(resourceId, payload) {
  return request(`/admin/navigation/resources/${resourceId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteNavigationResource(resourceId, tenantId = null) {
  return request(withQuery(`/admin/navigation/resources/${resourceId}`, {
    tenant_id: tenantId,
  }), {
    method: 'DELETE',
  })
}

export function createNavigationView(payload) {
  return request('/admin/navigation/views', {
    method: 'POST',
    body: payload,
  })
}

export function patchNavigationView(viewId, payload) {
  return request(`/admin/navigation/views/${viewId}`, {
    method: 'PATCH',
    body: payload,
  })
}

export function deleteNavigationView(viewId, tenantId = null) {
  return request(withQuery(`/admin/navigation/views/${viewId}`, {
    tenant_id: tenantId,
  }), {
    method: 'DELETE',
  })
}

const oscalSubmodulePathByType = {
  catalog: 'catalogs',
  profile: 'profiles',
  mapping: 'mappings',
  'assessment-plan': 'assessment-plans',
  'assessment-results': 'assessment-results',
  poam: 'poams',
  'component-definition': 'component-definitions',
  'system-security-plan': 'system-security-plans',
}

function getOscalSubmodulePath(documentType, documentId = '') {
  const normalizedType = String(documentType || '').trim()
  const submodulePath = oscalSubmodulePathByType[normalizedType]

  const basePath = submodulePath
    ? `/oscal/${submodulePath}`
    : '/oscal/documents'

  if (!documentId) {
    return basePath
  }

  return `${basePath}/${documentId}`
}

export function listOscalSubmoduleDocuments(documentType) {
  return request(getOscalSubmodulePath(documentType))
}

export function getOscalSubmoduleDocument(documentType, documentId) {
  return request(getOscalSubmodulePath(documentType, documentId))
}

export function createOscalSubmoduleDocument(documentType, payload) {
  return request(getOscalSubmodulePath(documentType), {
    method: 'POST',
    body: {
      title: payload?.title ?? null,
      content_json: payload?.content ?? {},
    },
  })
}

export function replaceOscalSubmoduleDocument(documentType, documentId, payload) {
  return request(getOscalSubmodulePath(documentType, documentId), {
    method: 'PUT',
    body: {
      title: payload?.title ?? null,
      content_json: payload?.content ?? {},
    },
  })
}

export function deleteOscalSubmoduleDocument(documentType, documentId) {
  return request(getOscalSubmodulePath(documentType, documentId), {
    method: 'DELETE',
  })
}
