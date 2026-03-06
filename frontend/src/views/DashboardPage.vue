<template>
  <section class="dashboard-page bg-brand-surface rounded-3xl p-4 md:p-5">
    <h2 class="text-brand-deep">ITSoR Overview</h2>

    <div class="dashboard-grid">
      <article class="dash-card border-brand-purple/20">
        <h3 class="text-brand-deep">Identity Health</h3>
        <p class="meta">No detections found in the last 30 days.</p>
      </article>
      <article class="dash-card border-brand-purple/20">
        <h3 class="text-brand-deep">Tenant Context</h3>
        <p class="meta">Active tenant and service posture summary.</p>
      </article>
      <article class="dash-card dash-card-muted border-brand-pink/25">
        <h3 class="text-brand-purple">Operational Alerts</h3>
        <p class="meta">No active alerts.</p>
      </article>
    </div>

    <h3 class="section-gap">Shortcuts</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/users">Users</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/groups">Groups</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/roles">Roles</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/permissions">Permissions</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/auth/tenants">Tenants</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/workspaces">Workspaces</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/entity-types">Entity Types</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/entity-records">Entity Records</RouterLink>
    </div>
  </section>
</template>
