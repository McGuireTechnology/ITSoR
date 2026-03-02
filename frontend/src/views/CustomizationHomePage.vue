<template>
  <section class="dashboard-page bg-brand-surface rounded-3xl p-4 md:p-5">
    <h2 class="text-brand-deep">Customization Overview</h2>
    <p class="meta">Overview and quick access for schema and workspace customization.</p>

    <h3 class="section-gap">Shortcuts</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/workspaces">Workspaces</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/namespaces">Namespaces</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/entity-types">Entity Types</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/customization/entity-records">Entity Records</RouterLink>
    </div>
  </section>
</template>
