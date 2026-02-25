<template>
  <section class="dashboard-page">
    <h2>ITSoR Overview</h2>

    <div class="dashboard-grid">
      <article class="dash-card">
        <h3>Identity Health</h3>
        <p class="meta">No detections found in the last 30 days.</p>
      </article>
      <article class="dash-card">
        <h3>Tenant Context</h3>
        <p class="meta">Active tenant and service posture summary.</p>
      </article>
      <article class="dash-card dash-card-muted">
        <h3>Operational Alerts</h3>
        <p class="meta">No active alerts.</p>
      </article>
    </div>

    <h3 class="section-gap">Shortcuts</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip" to="/users">Users</RouterLink>
      <RouterLink class="shortcut-chip" to="/groups">Groups</RouterLink>
      <RouterLink class="shortcut-chip" to="/tenants">Tenants</RouterLink>
      <RouterLink class="shortcut-chip" to="/workspaces">Workspaces</RouterLink>
      <RouterLink class="shortcut-chip" to="/entity-types">Entity Types</RouterLink>
      <RouterLink class="shortcut-chip" to="/entity-records">Entity Records</RouterLink>
    </div>
  </section>
</template>
