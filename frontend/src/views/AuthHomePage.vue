<template>
  <section class="dashboard-page bg-brand-surface rounded-3xl p-4 md:p-5">
    <h2 class="text-brand-deep">Auth Overview</h2>
    <p class="meta">Overview and quick access for core auth administration.</p>

    <h3 class="section-gap">Shortcuts</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/users">Users</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/groups">Groups</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/roles">Roles</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/permissions">Permissions</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/tenants">Tenants</RouterLink>
    </div>
  </section>
</template>