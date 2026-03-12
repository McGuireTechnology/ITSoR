<template>
  <section class="dashboard-page bg-brand-surface rounded-3xl p-4 md:p-5">
    <h2 class="text-brand-deep">Governance Risk and Compliance</h2>
    <p class="meta">Top-level GRC workspace organized by Control, Assessment, and Implementation.</p>

    <h3 class="section-gap">Control</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/control/catalogs/list">Catalogs</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/control/profiles/list">Profiles</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/control/mappings/list">Mappings</RouterLink>
    </div>

    <h3 class="section-gap">Assessment</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/assessment/plans/list">Plans</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/assessment/results/list">Results</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/assessment/poams/list">POA&amp;M</RouterLink>
    </div>

    <h3 class="section-gap">Implementation</h3>
    <div class="shortcut-row">
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/implementation/component-definitions/list">Component Definitions</RouterLink>
      <RouterLink class="shortcut-chip border-brand-purple/30 hover:border-brand-pink hover:text-brand-pink" to="/grc/implementation/system-security-plans/list">System Security Plans</RouterLink>
    </div>
  </section>
</template>
