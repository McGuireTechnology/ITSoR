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
import IdentityHomePage from './views/IdentityHomePage.vue'
import CustomizationHomePage from './views/CustomizationHomePage.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: DashboardPage, meta: { title: 'Home' } },
  { path: '/login', component: LoginPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/logout', component: LogoutPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/signup', component: SignupPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/auth/overview', component: AuthHomePage, meta: { domain: 'auth_home', title: 'Auth Overview', showCommandBar: false } },
  { path: '/auth/home', redirect: '/auth/overview' },
  { path: '/auth/users', component: UsersPage, meta: { domain: 'users', title: 'Users' } },
  { path: '/auth/users/me', component: UserMePage, meta: { domain: 'users', title: 'My Account' } },
  { path: '/auth/users/:id', component: UserDetailPage, props: true, meta: { domain: 'users', title: 'User Detail' } },
  { path: '/auth/users/:id/group-membership', component: UserGroupMembershipPage, props: true, meta: { domain: 'users', title: 'User Group Membership' } },
  { path: '/auth/users/:id/user-roles', component: UserRolesPage, props: true, meta: { domain: 'users', title: 'User Roles' } },
  { path: '/auth/users/:id/user-tenants', component: UserTenantsPage, props: true, meta: { domain: 'users', title: 'User Tenants' } },
  { path: '/auth/groups', component: GroupsPage, meta: { domain: 'groups', title: 'Groups' } },
  { path: '/auth/groups/:id', component: GroupDetailPage, props: true, meta: { domain: 'groups', title: 'Group Detail' } },
  { path: '/auth/groups/:id/group-memberships', component: GroupMembershipsPage, props: true, meta: { domain: 'groups', title: 'Group Memberships' } },
  { path: '/auth/groups/:id/group-roles', component: GroupRolesPage, props: true, meta: { domain: 'groups', title: 'Group Roles' } },
  { path: '/auth/tenants', component: TenantsPage, meta: { domain: 'tenants', title: 'Tenants' } },
  { path: '/auth/tenants/:id', component: TenantDetailPage, props: true, meta: { domain: 'tenants', title: 'Tenant Detail' } },
  { path: '/auth/roles', component: RolesPage, meta: { domain: 'roles', title: 'Roles' } },
  { path: '/auth/roles/:id', component: RoleDetailPage, props: true, meta: { domain: 'roles', title: 'Role Detail' } },
  { path: '/auth/roles/:id/role-permissions', component: RolePermissionsPage, props: true, meta: { domain: 'roles', title: 'Role Permissions' } },
  { path: '/auth/permissions', component: PermissionsPage, meta: { domain: 'permissions', title: 'Permissions' } },
  { path: '/auth/permissions/:id', component: PermissionDetailPage, props: true, meta: { domain: 'permissions', title: 'Permission Detail' } },
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
  { path: '/users', redirect: '/auth/users' },
  { path: '/users/me', redirect: '/auth/users/me' },
  { path: '/users/:id', redirect: (to) => `/auth/users/${to.params.id}` },
  { path: '/user/:id', redirect: (to) => `/auth/users/${to.params.id}` },
  { path: '/groups', redirect: '/auth/groups' },
  { path: '/groups/:id', redirect: (to) => `/auth/groups/${to.params.id}` },
  { path: '/tenants', redirect: '/auth/tenants' },
  { path: '/tenants/:id', redirect: (to) => `/auth/tenants/${to.params.id}` },
  { path: '/roles', redirect: '/auth/roles' },
  { path: '/roles/:id', redirect: (to) => `/auth/roles/${to.params.id}` },
  { path: '/permissions', redirect: '/auth/permissions' },
  { path: '/permissions/:id', redirect: (to) => `/auth/permissions/${to.params.id}` },
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
