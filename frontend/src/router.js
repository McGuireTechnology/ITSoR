import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './views/LoginPage.vue'
import LogoutPage from './views/LogoutPage.vue'
import SignupPage from './views/SignupPage.vue'
import TenantsPage from './views/TenantsPage.vue'
import TenantDetailPage from './views/TenantDetailPage.vue'
import UsersPage from './views/UsersPage.vue'
import UserDetailPage from './views/UserDetailPage.vue'
import UserMePage from './views/UserMePage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/logout', component: LogoutPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/signup', component: SignupPage, meta: { hideNavigation: true, layout: 'auth' } },
  { path: '/tenants', component: TenantsPage },
  { path: '/tenants/:id', component: TenantDetailPage, props: true },
  { path: '/users', component: UsersPage },
  { path: '/users/me', component: UserMePage },
  { path: '/users/:id', component: UserDetailPage, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
