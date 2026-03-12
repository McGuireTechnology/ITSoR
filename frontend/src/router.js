import { createRouter, createWebHistory } from 'vue-router'
import { clearToken, hasValidToken } from './lib/auth'
import LoginPage from './views/LoginPage.vue'
import LogoutPage from './views/LogoutPage.vue'
import SignupPage from './views/SignupPage.vue'
import GroupsPage from './views/GroupsPage.vue'
import GroupDetailPage from './views/GroupDetailPage.vue'
import GroupMembershipsPage from './views/GroupMembershipsPage.vue'
import GroupRolesPage from './views/GroupRolesPage.vue'
import TenantsPage from './views/TenantsPage.vue'
import TenantDetailPage from './views/TenantDetailPage.vue'
import UsersPage from './views/UsersPage.vue'
import UserDetailPage from './views/UserDetailPage.vue'
import UserGroupMembershipPage from './views/UserGroupMembershipPage.vue'
import UserRolesPage from './views/UserRolesPage.vue'
import UserTenantsPage from './views/UserTenantsPage.vue'
import UserMePage from './views/UserMePage.vue'
import RolesPage from './views/RolesPage.vue'
import RoleDetailPage from './views/RoleDetailPage.vue'
import RolePermissionsPage from './views/RolePermissionsPage.vue'
import PermissionsPage from './views/PermissionsPage.vue'
import PermissionDetailPage from './views/PermissionDetailPage.vue'
import WorkspacesPage from './views/WorkspacesPage.vue'
import WorkspaceDetailPage from './views/WorkspaceDetailPage.vue'
import NamespacesPage from './views/NamespacesPage.vue'
import NamespaceDetailPage from './views/NamespaceDetailPage.vue'
import EntityTypesPage from './views/EntityTypesPage.vue'
import EntityTypeDetailPage from './views/EntityTypeDetailPage.vue'
import EntityRecordsPage from './views/EntityRecordsPage.vue'
import EntityRecordDetailPage from './views/EntityRecordDetailPage.vue'
import IdmGroupsPage from './views/IdmGroupsPage.vue'
import IdmIdentitiesPage from './views/IdmIdentitiesPage.vue'
import IdmPeoplePage from './views/IdmPeoplePage.vue'
import IdmUsersPage from './views/IdmUsersPage.vue'
import IdmGroupMembershipsPage from './views/IdmGroupMembershipsPage.vue'
import DashboardPage from './views/DashboardPage.vue'
import AuthHomePage from './views/AuthHomePage.vue'
import AdminNavigationPage from './views/AdminNavigationPage.vue'
import IdentityHomePage from './views/IdentityHomePage.vue'
import CustomizationHomePage from './views/CustomizationHomePage.vue'
import OscalDocumentsPage from './views/OscalDocumentsPage.vue'
import GrcHomePage from './views/GrcHomePage.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: DashboardPage, meta: { title: 'Home' } },
  { path: '/login', component: LoginPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/logout', component: LogoutPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/signup', component: SignupPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/admin/overview', component: AuthHomePage, meta: { domain: 'auth_home', title: 'Auth Overview', showCommandBar: false } },
  { path: '/admin/home', redirect: '/admin/overview' },
  { path: '/admin/users', component: UsersPage, meta: { domain: 'users', title: 'Users' } },
  { path: '/admin/users/me', component: UserMePage, meta: { domain: 'users', title: 'My Account' } },
  { path: '/admin/users/:id', component: UserDetailPage, props: true, meta: { domain: 'users', title: 'User Detail' } },
  { path: '/admin/users/:id/group-membership', component: UserGroupMembershipPage, props: true, meta: { domain: 'users', title: 'User Group Membership' } },
  { path: '/admin/users/:id/user-roles', component: UserRolesPage, props: true, meta: { domain: 'users', title: 'User Roles' } },
  { path: '/admin/users/:id/user-tenants', component: UserTenantsPage, props: true, meta: { domain: 'users', title: 'User Tenants' } },
  { path: '/admin/groups', component: GroupsPage, meta: { domain: 'groups', title: 'Groups' } },
  { path: '/admin/groups/:id', component: GroupDetailPage, props: true, meta: { domain: 'groups', title: 'Group Detail' } },
  { path: '/admin/groups/:id/group-memberships', component: GroupMembershipsPage, props: true, meta: { domain: 'groups', title: 'Group Memberships' } },
  { path: '/admin/groups/:id/group-roles', component: GroupRolesPage, props: true, meta: { domain: 'groups', title: 'Group Roles' } },
  { path: '/admin/tenants', component: TenantsPage, meta: { domain: 'tenants', title: 'Tenants' } },
  { path: '/admin/tenants/:id', component: TenantDetailPage, props: true, meta: { domain: 'tenants', title: 'Tenant Detail' } },
  { path: '/admin/roles', component: RolesPage, meta: { domain: 'roles', title: 'Roles' } },
  { path: '/admin/roles/:id', component: RoleDetailPage, props: true, meta: { domain: 'roles', title: 'Role Detail' } },
  { path: '/admin/roles/:id/role-permissions', component: RolePermissionsPage, props: true, meta: { domain: 'roles', title: 'Role Permissions' } },
  { path: '/admin/permissions', component: PermissionsPage, meta: { domain: 'permissions', title: 'Permissions' } },
  { path: '/admin/permissions/:id', component: PermissionDetailPage, props: true, meta: { domain: 'permissions', title: 'Permission Detail' } },
  { path: '/admin/navigation', component: AdminNavigationPage, meta: { domain: 'navigation', title: 'Navigation' } },
  { path: '/idm/overview', component: IdentityHomePage, meta: { domain: 'idm_home', title: 'Identity Overview', showCommandBar: false } },
  { path: '/idm/home', redirect: '/idm/overview' },
  { path: '/idm/people', component: IdmPeoplePage, meta: { domain: 'idm_people', title: 'People' } },
  { path: '/idm/identities', component: IdmIdentitiesPage, meta: { domain: 'idm_identities', title: 'Identities' } },
  { path: '/idm/users', component: IdmUsersPage, meta: { domain: 'idm_users', title: 'Users' } },
  { path: '/idm/groups', component: IdmGroupsPage, meta: { domain: 'idm_groups', title: 'Groups' } },
  { path: '/idm/group-memberships', component: IdmGroupMembershipsPage, meta: { domain: 'idm_group_memberships', title: 'Group Memberships' } },
  { path: '/customization/overview', component: CustomizationHomePage, meta: { domain: 'customization_home', title: 'Customization Overview', showCommandBar: false } },
  { path: '/customization/home', redirect: '/customization/overview' },
  { path: '/customization/workspaces', component: WorkspacesPage, meta: { domain: 'workspaces', title: 'Workspaces' } },
  { path: '/customization/workspaces/:id', component: WorkspaceDetailPage, props: true, meta: { domain: 'workspaces', title: 'Workspace Detail' } },
  { path: '/customization/namespaces', component: NamespacesPage, meta: { domain: 'namespaces', title: 'Namespaces' } },
  { path: '/customization/namespaces/:id', component: NamespaceDetailPage, props: true, meta: { domain: 'namespaces', title: 'Namespace Detail' } },
  { path: '/customization/entity-types', component: EntityTypesPage, meta: { domain: 'entity-types', title: 'Entity Types' } },
  { path: '/customization/entity-types/:id', component: EntityTypeDetailPage, props: true, meta: { domain: 'entity-types', title: 'Entity Type Detail' } },
  { path: '/customization/entity-records', component: EntityRecordsPage, meta: { domain: 'entity-records', title: 'Entity Records' } },
  { path: '/customization/entity-records/:id', component: EntityRecordDetailPage, props: true, meta: { domain: 'entity-records', title: 'Entity Record Detail' } },
  { path: '/grc/overview', component: GrcHomePage, meta: { domain: 'grc_home', title: 'GRC Overview', showCommandBar: false } },
  { path: '/grc/home', redirect: '/grc/overview' },
  { path: '/grc/control', redirect: '/grc/control/catalogs' },
  { path: '/grc/control/catalogs', redirect: '/grc/control/catalogs/list' },
  { path: '/grc/control/catalogs/list', component: OscalDocumentsPage, props: { fixedType: 'catalog', titleOverride: 'Control · Catalogs · List', viewMode: 'list' }, meta: { domain: 'grc_control_catalogs_list', title: 'Control Catalogs List' } },
  { path: '/grc/control/catalogs/create', component: OscalDocumentsPage, props: { fixedType: 'catalog', titleOverride: 'Control · Catalogs · Create', viewMode: 'create' }, meta: { domain: 'grc_control_catalogs_create', title: 'Control Catalogs Create' } },
  { path: '/grc/control/profiles', redirect: '/grc/control/profiles/list' },
  { path: '/grc/control/profiles/list', component: OscalDocumentsPage, props: { fixedType: 'profile', titleOverride: 'Control · Profiles · List', viewMode: 'list' }, meta: { domain: 'grc_control_profiles_list', title: 'Control Profiles List' } },
  { path: '/grc/control/profiles/create', component: OscalDocumentsPage, props: { fixedType: 'profile', titleOverride: 'Control · Profiles · Create', viewMode: 'create' }, meta: { domain: 'grc_control_profiles_create', title: 'Control Profiles Create' } },
  { path: '/grc/control/mappings', redirect: '/grc/control/mappings/list' },
  { path: '/grc/control/mappings/list', component: OscalDocumentsPage, props: { fixedType: 'mapping', titleOverride: 'Control · Mappings · List', viewMode: 'list' }, meta: { domain: 'grc_control_mappings_list', title: 'Control Mappings List' } },
  { path: '/grc/control/mappings/create', component: OscalDocumentsPage, props: { fixedType: 'mapping', titleOverride: 'Control · Mappings · Create', viewMode: 'create' }, meta: { domain: 'grc_control_mappings_create', title: 'Control Mappings Create' } },
  { path: '/grc/assessment', redirect: '/grc/assessment/plans' },
  { path: '/grc/assessment/plans', redirect: '/grc/assessment/plans/list' },
  { path: '/grc/assessment/plans/list', component: OscalDocumentsPage, props: { fixedType: 'assessment-plan', titleOverride: 'Assessment · Plans · List', viewMode: 'list' }, meta: { domain: 'grc_assessment_plans_list', title: 'Assessment Plans List' } },
  { path: '/grc/assessment/plans/create', component: OscalDocumentsPage, props: { fixedType: 'assessment-plan', titleOverride: 'Assessment · Plans · Create', viewMode: 'create' }, meta: { domain: 'grc_assessment_plans_create', title: 'Assessment Plans Create' } },
  { path: '/grc/assessment/results', redirect: '/grc/assessment/results/list' },
  { path: '/grc/assessment/results/list', component: OscalDocumentsPage, props: { fixedType: 'assessment-results', titleOverride: 'Assessment · Results · List', viewMode: 'list' }, meta: { domain: 'grc_assessment_results_list', title: 'Assessment Results List' } },
  { path: '/grc/assessment/results/create', component: OscalDocumentsPage, props: { fixedType: 'assessment-results', titleOverride: 'Assessment · Results · Create', viewMode: 'create' }, meta: { domain: 'grc_assessment_results_create', title: 'Assessment Results Create' } },
  { path: '/grc/assessment/poams', redirect: '/grc/assessment/poams/list' },
  { path: '/grc/assessment/poams/list', component: OscalDocumentsPage, props: { fixedType: 'poam', titleOverride: 'Assessment · POA&M · List', viewMode: 'list' }, meta: { domain: 'grc_assessment_poams_list', title: 'Assessment POA&M List' } },
  { path: '/grc/assessment/poams/create', component: OscalDocumentsPage, props: { fixedType: 'poam', titleOverride: 'Assessment · POA&M · Create', viewMode: 'create' }, meta: { domain: 'grc_assessment_poams_create', title: 'Assessment POA&M Create' } },
  { path: '/grc/implementation', redirect: '/grc/implementation/component-definitions' },
  { path: '/grc/implementation/component-definitions', redirect: '/grc/implementation/component-definitions/list' },
  { path: '/grc/implementation/component-definitions/list', component: OscalDocumentsPage, props: { fixedType: 'component-definition', titleOverride: 'Implementation · Component Definitions · List', viewMode: 'list' }, meta: { domain: 'grc_implementation_component_definitions_list', title: 'Implementation Component Definitions List' } },
  { path: '/grc/implementation/component-definitions/create', component: OscalDocumentsPage, props: { fixedType: 'component-definition', titleOverride: 'Implementation · Component Definitions · Create', viewMode: 'create' }, meta: { domain: 'grc_implementation_component_definitions_create', title: 'Implementation Component Definitions Create' } },
  { path: '/grc/implementation/system-security-plans', redirect: '/grc/implementation/system-security-plans/list' },
  { path: '/grc/implementation/system-security-plans/list', component: OscalDocumentsPage, props: { fixedType: 'system-security-plan', titleOverride: 'Implementation · System Security Plans · List', viewMode: 'list' }, meta: { domain: 'grc_implementation_system_security_plans_list', title: 'Implementation System Security Plans List' } },
  { path: '/grc/implementation/system-security-plans/create', component: OscalDocumentsPage, props: { fixedType: 'system-security-plan', titleOverride: 'Implementation · System Security Plans · Create', viewMode: 'create' }, meta: { domain: 'grc_implementation_system_security_plans_create', title: 'Implementation System Security Plans Create' } },
  { path: '/oscal/overview', redirect: '/grc/overview' },
  { path: '/oscal/home', redirect: '/grc/overview' },
  { path: '/oscal/documents', redirect: '/grc/control/catalogs/list' },
  { path: '/customization/oscal', redirect: '/oscal/documents' },
  { path: '/users', redirect: '/admin/users' },
  { path: '/users/me', redirect: '/admin/users/me' },
  { path: '/users/:id', redirect: (to) => `/admin/users/${to.params.id}` },
  { path: '/user/:id', redirect: (to) => `/admin/users/${to.params.id}` },
  { path: '/groups', redirect: '/admin/groups' },
  { path: '/groups/:id', redirect: (to) => `/admin/groups/${to.params.id}` },
  { path: '/tenants', redirect: '/admin/tenants' },
  { path: '/tenants/:id', redirect: (to) => `/admin/tenants/${to.params.id}` },
  { path: '/roles', redirect: '/admin/roles' },
  { path: '/roles/:id', redirect: (to) => `/admin/roles/${to.params.id}` },
  { path: '/permissions', redirect: '/admin/permissions' },
  { path: '/permissions/:id', redirect: (to) => `/admin/permissions/${to.params.id}` },
  { path: '/auth', redirect: '/admin/overview' },
  { path: '/auth/home', redirect: '/admin/overview' },
  { path: '/auth/:rest(.*)', redirect: (to) => `/admin/${String(to.params.rest || '')}` },
  { path: '/idm_people', redirect: '/idm/people' },
  { path: '/idm_identities', redirect: '/idm/identities' },
  { path: '/idm_users', redirect: '/idm/users' },
  { path: '/idm_groups', redirect: '/idm/groups' },
  { path: '/idm_group_memberships', redirect: '/idm/group-memberships' },
  { path: '/workspaces', redirect: '/customization/workspaces' },
  { path: '/workspaces/:id', redirect: (to) => `/customization/workspaces/${to.params.id}` },
  { path: '/namespaces', redirect: '/customization/namespaces' },
  { path: '/namespaces/:id', redirect: (to) => `/customization/namespaces/${to.params.id}` },
  { path: '/entity-types', redirect: '/customization/entity-types' },
  { path: '/entity-types/:id', redirect: (to) => `/customization/entity-types/${to.params.id}` },
  { path: '/entity-records', redirect: '/customization/entity-records' },
  { path: '/entity-records/:id', redirect: (to) => `/customization/entity-records/${to.params.id}` },
  { path: '/oscal', redirect: '/grc/overview' },
  { path: '/grc', redirect: '/grc/overview' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const authOnlyPaths = new Set(['/login', '/signup'])
const publicPaths = new Set(['/login', '/signup', '/logout'])

router.beforeEach((to) => {
  const isAuthenticated = hasValidToken()

  if (!isAuthenticated) {
    clearToken()
  }

  if (isAuthenticated && authOnlyPaths.has(to.path)) {
    return '/home'
  }

  if (!isAuthenticated && !publicPaths.has(to.path)) {
    return '/logout'
  }

  return true
})

export default router
