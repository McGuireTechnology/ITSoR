import { ref } from 'vue'

export const workspaceConfig = {
  admin: {
    label: 'Administration',
    icon: '🖥️',
    namespaces: [
      { key: 'auth_home', label: 'Overview', icon: '🏠', to: '/admin/overview' },
      { key: 'users', label: 'Users', icon: '👤', to: '/admin/users' },
      { key: 'groups', label: 'Groups', icon: '👥', to: '/admin/groups' },
      { key: 'tenants', label: 'Tenants', icon: '🏢', to: '/admin/tenants' },
      { key: 'roles', label: 'Roles', icon: '🎭', to: '/admin/roles' },
      { key: 'permissions', label: 'Permissions', icon: '🔐', to: '/admin/permissions' },
      { key: 'navigation', label: 'Navigation', icon: '🧭', to: '/admin/navigation' },
    ],
  },
  idm: {
    label: 'Identity',
    icon: '🪪',
    namespaces: [
      { key: 'idm_home', label: 'Overview', icon: '🏠', to: '/idm/overview' },
      { key: 'idm_people', label: 'People', icon: '🧑', to: '/idm/people' },
      { key: 'idm_identities', label: 'Identities', icon: '🪪', to: '/idm/identities' },
      { key: 'idm_users', label: 'Users', icon: '👤', to: '/idm/users' },
      { key: 'idm_groups', label: 'Groups', icon: '👥', to: '/idm/groups' },
      { key: 'idm_group_memberships', label: 'Group Memberships', icon: '🫱‍🫲', to: '/idm/group-memberships' },
    ],
  },
  customization: {
    label: 'Customization',
    icon: '⚙️',
    namespaces: [
      { key: 'customization_home', label: 'Overview', icon: '🏠', to: '/customization/overview' },
      { key: 'workspaces', label: 'Workspaces', icon: '🗂️', to: '/customization/workspaces' },
      { key: 'namespaces', label: 'Namespaces', icon: '📦', to: '/customization/namespaces' },
      { key: 'entity-types', label: 'Entity Types', icon: '🧩', to: '/customization/entity-types' },
      { key: 'entity-records', label: 'Entity Records', icon: '🗃️', to: '/customization/entity-records' },
    ],
  },
  grc: {
    label: 'GRC',
    icon: '📚',
    namespaces: [
      { key: 'grc_home', label: 'Overview', icon: '🏠', to: '/grc/overview' },
      { key: 'grc_control_catalogs', label: 'Control Catalogs', icon: '📘', to: '/grc/control/catalogs' },
      { key: 'grc_control_profiles', label: 'Control Profiles', icon: '📙', to: '/grc/control/profiles' },
      { key: 'grc_control_mappings', label: 'Control Mappings', icon: '🗺️', to: '/grc/control/mappings' },
      { key: 'grc_assessment_plans', label: 'Assessment Plans', icon: '📝', to: '/grc/assessment/plans' },
      { key: 'grc_assessment_results', label: 'Assessment Results', icon: '📊', to: '/grc/assessment/results' },
      { key: 'grc_assessment_poams', label: 'Assessment POA&M', icon: '📌', to: '/grc/assessment/poams' },
      {
        key: 'grc_implementation_component_definitions',
        label: 'Component Definitions',
        icon: '🧱',
        to: '/grc/implementation/component-definitions',
      },
      {
        key: 'grc_implementation_system_security_plans',
        label: 'System Security Plans',
        icon: '🛡️',
        to: '/grc/implementation/system-security-plans',
      },
    ],
  },
}

const workspaceByDomain = {
  auth_home: 'admin',
  users: 'admin',
  groups: 'admin',
  tenants: 'admin',
  roles: 'admin',
  permissions: 'admin',
  navigation: 'admin',
  'endpoint-permissions': 'admin',

  idm_home: 'idm',
  idm_people: 'idm',
  idm_identities: 'idm',
  idm_users: 'idm',
  idm_groups: 'idm',
  idm_group_memberships: 'idm',

  customization_home: 'customization',
  workspaces: 'customization',
  namespaces: 'customization',
  'entity-types': 'customization',
  'entity-records': 'customization',

  grc_home: 'grc',
  oscal_documents: 'grc',
}

const listPathByDomain = {
  auth_home: '/admin/overview',
  users: '/admin/users',
  groups: '/admin/groups',
  tenants: '/admin/tenants',
  roles: '/admin/roles',
  permissions: '/admin/permissions',
  navigation: '/admin/navigation',
  'endpoint-permissions': '/auth/endpoint-permissions',

  idm_home: '/idm/overview',
  idm_people: '/idm/people',
  idm_identities: '/idm/identities',
  idm_users: '/idm/users',
  idm_groups: '/idm/groups',
  idm_group_memberships: '/idm/group-memberships',

  customization_home: '/customization/overview',
  workspaces: '/customization/workspaces',
  namespaces: '/customization/namespaces',
  'entity-types': '/customization/entity-types',
  'entity-records': '/customization/entity-records',

  grc_home: '/grc/overview',
  grc_control_catalogs_list: '/grc/control/catalogs/list',
  grc_control_catalogs_create: '/grc/control/catalogs/list',
  grc_control_profiles_list: '/grc/control/profiles/list',
  grc_control_profiles_create: '/grc/control/profiles/list',
  grc_control_mappings_list: '/grc/control/mappings/list',
  grc_control_mappings_create: '/grc/control/mappings/list',
  grc_assessment_plans_list: '/grc/assessment/plans/list',
  grc_assessment_plans_create: '/grc/assessment/plans/list',
  grc_assessment_results_list: '/grc/assessment/results/list',
  grc_assessment_results_create: '/grc/assessment/results/list',
  grc_assessment_poams_list: '/grc/assessment/poams/list',
  grc_assessment_poams_create: '/grc/assessment/poams/list',
  grc_implementation_component_definitions_list: '/grc/implementation/component-definitions/list',
  grc_implementation_component_definitions_create: '/grc/implementation/component-definitions/list',
  grc_implementation_system_security_plans_list: '/grc/implementation/system-security-plans/list',
  grc_implementation_system_security_plans_create: '/grc/implementation/system-security-plans/list',
}

export const activeWorkspace = ref('admin')

function normalizeDomain(domain) {
  return String(domain || '').trim()
}

export function getWorkspaceForDomain(domain) {
  const normalizedDomain = normalizeDomain(domain)
  if (!normalizedDomain) {
    return null
  }

  const explicitWorkspace = workspaceByDomain[normalizedDomain]
  if (explicitWorkspace) {
    return explicitWorkspace
  }

  if (normalizedDomain.startsWith('grc_')) {
    return 'grc'
  }

  return null
}

export function getListPathForDomain(domain) {
  const normalizedDomain = normalizeDomain(domain)
  if (!normalizedDomain) {
    return ''
  }

  const explicitPath = listPathByDomain[normalizedDomain]
  if (explicitPath) {
    return explicitPath
  }

  return ''
}

export function setActiveWorkspace(workspaceKey) {
  if (!workspaceConfig[workspaceKey]) {
    return
  }

  activeWorkspace.value = workspaceKey
}

export function syncWorkspaceFromDomain(domain) {
  const workspaceKey = getWorkspaceForDomain(domain)
  if (!workspaceKey) {
    return
  }

  setActiveWorkspace(workspaceKey)
}
