import { createRouter, createWebHistory } from 'vue-router'
import { clearToken, hasValidToken } from './lib/auth'
import LoginPage from './views/LoginPage.vue'
import LogoutPage from './views/LogoutPage.vue'
import SignupPage from './views/SignupPage.vue'
import GroupsPage from './views/GroupsPage.vue'
import GroupDetailPage from './views/GroupDetailPage.vue'
import GroupMembersPage from './views/GroupMembersPage.vue'
import GroupEndpointPermissionsPage from './views/GroupEndpointPermissionsPage.vue'
import TenantsPage from './views/TenantsPage.vue'
import TenantDetailPage from './views/TenantDetailPage.vue'
import EndpointPermissionsPage from './views/EndpointPermissionsPage.vue'
import EndpointPermissionDetailPage from './views/EndpointPermissionDetailPage.vue'
import UsersPage from './views/UsersPage.vue'
import UserDetailPage from './views/UserDetailPage.vue'
import UserEndpointPermissionsPage from './views/UserEndpointPermissionsPage.vue'
import UserGroupMembershipPage from './views/UserGroupMembershipPage.vue'
import UserMePage from './views/UserMePage.vue'
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
import PlatformHomePage from './views/PlatformHomePage.vue'
import IdentityHomePage from './views/IdentityHomePage.vue'
import CustomizationHomePage from './views/CustomizationHomePage.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: DashboardPage, meta: { title: 'Home' } },
  { path: '/login', component: LoginPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/logout', component: LogoutPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/signup', component: SignupPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/platform/overview', component: PlatformHomePage, meta: { domain: 'platform_home', title: 'Platform Overview', showCommandBar: false } },
  { path: '/platform/home', redirect: '/platform/overview' },
  { path: '/platform/users', component: UsersPage, meta: { domain: 'users', title: 'Users' } },
  { path: '/platform/users/me', component: UserMePage, meta: { domain: 'users', title: 'My Account' } },
  { path: '/platform/users/:id', component: UserDetailPage, props: true, meta: { domain: 'users', title: 'User Detail' } },
  { path: '/platform/users/:id/endpoint-permissions', component: UserEndpointPermissionsPage, props: true, meta: { domain: 'users', title: 'User Endpoint Permissions' } },
  { path: '/platform/users/:id/group-membership', component: UserGroupMembershipPage, props: true, meta: { domain: 'users', title: 'User Group Membership' } },
  { path: '/platform/groups', component: GroupsPage, meta: { domain: 'groups', title: 'Groups' } },
  { path: '/platform/groups/:id', component: GroupDetailPage, props: true, meta: { domain: 'groups', title: 'Group Detail' } },
  { path: '/platform/groups/:id/members', component: GroupMembersPage, props: true, meta: { domain: 'groups', title: 'Group Members' } },
  { path: '/platform/groups/:id/endpoint-permissions', component: GroupEndpointPermissionsPage, props: true, meta: { domain: 'groups', title: 'Group Endpoint Permissions' } },
  { path: '/platform/tenants', component: TenantsPage, meta: { domain: 'tenants', title: 'Tenants' } },
  { path: '/platform/tenants/:id', component: TenantDetailPage, props: true, meta: { domain: 'tenants', title: 'Tenant Detail' } },
  { path: '/platform/endpoint-permissions', component: EndpointPermissionsPage, meta: { domain: 'endpoint-permissions', title: 'Endpoint Permissions' } },
  { path: '/platform/endpoint-permissions/:id', component: EndpointPermissionDetailPage, props: true, meta: { domain: 'endpoint-permissions', title: 'Endpoint Permission Detail' } },
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
  { path: '/users', redirect: '/platform/users' },
  { path: '/users/me', redirect: '/platform/users/me' },
  { path: '/users/:id', redirect: (to) => `/platform/users/${to.params.id}` },
  { path: '/user/:id', redirect: (to) => `/platform/users/${to.params.id}` },
  { path: '/groups', redirect: '/platform/groups' },
  { path: '/groups/:id', redirect: (to) => `/platform/groups/${to.params.id}` },
  { path: '/tenants', redirect: '/platform/tenants' },
  { path: '/tenants/:id', redirect: (to) => `/platform/tenants/${to.params.id}` },
  { path: '/endpoint-permissions', redirect: '/platform/endpoint-permissions' },
  { path: '/endpoint-permissions/:id', redirect: (to) => `/platform/endpoint-permissions/${to.params.id}` },
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
