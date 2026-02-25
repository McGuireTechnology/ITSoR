<template>
  <nav class="rail-nav">
    <h2 class="rail-title">Navigation</h2>

    <RouterLink to="/home">Home</RouterLink>

    <p class="rail-section-label">Identity</p>
    <RouterLink to="/users">Users</RouterLink>
    <RouterLink to="/groups">Groups</RouterLink>
    <RouterLink to="/tenants">Tenants</RouterLink>

    <p class="rail-section-label">Data Model</p>
    <RouterLink to="/workspaces">Workspaces</RouterLink>
    <RouterLink to="/namespaces">Namespaces</RouterLink>
    <RouterLink to="/entity-types">Entity Types</RouterLink>
    <RouterLink to="/entity-records">Entity Records</RouterLink>

    <p class="rail-section-label">Account</p>
    <RouterLink to="/users/me">My Account</RouterLink>
    <RouterLink to="/logout">Sign out</RouterLink>
  </nav>
</template>
