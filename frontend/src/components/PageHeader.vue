<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const pageTitle = computed(() => route.meta.title || 'Workspace')

const breadcrumbs = computed(() => {
  const chain = [{ label: 'Home', to: '/' }]
  for (const matched of route.matched) {
    if (!matched.path || matched.path === '/') {
      continue
    }
    const label = matched.meta?.title || matched.path.replace('/', '')
    const path = matched.path.replace(':id', route.params.id || '')
    chain.push({ label, to: path })
  }
  return chain
})
</script>

<template>
  <header class="page-header">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <span v-for="(crumb, index) in breadcrumbs" :key="`${crumb.to}-${index}`">
        <RouterLink :to="crumb.to">{{ crumb.label }}</RouterLink>
        <span v-if="index < breadcrumbs.length - 1" class="crumb-sep">›</span>
      </span>
    </nav>
    <h1>{{ pageTitle }}</h1>
  </header>
</template>
