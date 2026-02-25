import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './views/LoginPage.vue'
import LogoutPage from './views/LogoutPage.vue'
import SignupPage from './views/SignupPage.vue'
import GroupsPage from './views/GroupsPage.vue'
import GroupDetailPage from './views/GroupDetailPage.vue'
import TenantsPage from './views/TenantsPage.vue'
import TenantDetailPage from './views/TenantDetailPage.vue'
import UsersPage from './views/UsersPage.vue'
import UserDetailPage from './views/UserDetailPage.vue'
import UserMePage from './views/UserMePage.vue'
import WorkspacesPage from './views/WorkspacesPage.vue'
import WorkspaceDetailPage from './views/WorkspaceDetailPage.vue'
import NamespacesPage from './views/NamespacesPage.vue'
import NamespaceDetailPage from './views/NamespaceDetailPage.vue'
import EntityTypesPage from './views/EntityTypesPage.vue'
import EntityTypeDetailPage from './views/EntityTypeDetailPage.vue'
import EntityRecordsPage from './views/EntityRecordsPage.vue'
import EntityRecordDetailPage from './views/EntityRecordDetailPage.vue'
import DashboardPage from './views/DashboardPage.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: DashboardPage, meta: { title: 'Home' } },
  { path: '/login', component: LoginPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/logout', component: LogoutPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/signup', component: SignupPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/groups', component: GroupsPage, meta: { domain: 'groups', title: 'Groups' } },
  { path: '/groups/:id', component: GroupDetailPage, props: true, meta: { domain: 'groups', title: 'Group Detail' } },
  { path: '/tenants', component: TenantsPage, meta: { domain: 'tenants', title: 'Tenants' } },
  { path: '/tenants/:id', component: TenantDetailPage, props: true, meta: { domain: 'tenants', title: 'Tenant Detail' } },
  { path: '/workspaces', component: WorkspacesPage, meta: { domain: 'workspaces', title: 'Workspaces' } },
  { path: '/workspaces/:id', component: WorkspaceDetailPage, props: true, meta: { domain: 'workspaces', title: 'Workspace Detail' } },
  { path: '/namespaces', component: NamespacesPage, meta: { domain: 'namespaces', title: 'Namespaces' } },
  { path: '/namespaces/:id', component: NamespaceDetailPage, props: true, meta: { domain: 'namespaces', title: 'Namespace Detail' } },
  { path: '/entity-types', component: EntityTypesPage, meta: { domain: 'entity-types', title: 'Entity Types' } },
  { path: '/entity-types/:id', component: EntityTypeDetailPage, props: true, meta: { domain: 'entity-types', title: 'Entity Type Detail' } },
  { path: '/entity-records', component: EntityRecordsPage, meta: { domain: 'entity-records', title: 'Entity Records' } },
  { path: '/entity-records/:id', component: EntityRecordDetailPage, props: true, meta: { domain: 'entity-records', title: 'Entity Record Detail' } },
  { path: '/users', component: UsersPage, meta: { domain: 'users', title: 'Users' } },
  { path: '/users/me', component: UserMePage, meta: { domain: 'users', title: 'My Account' } },
  { path: '/users/:id', component: UserDetailPage, props: true, meta: { domain: 'users', title: 'User Detail' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
