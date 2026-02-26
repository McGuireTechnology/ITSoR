<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { activeWorkspace, workspaceConfig, syncWorkspaceFromDomain } from '../lib/workspaceNav'

const route = useRoute()

watch(
  () => route.meta.domain,
  (domain) => {
    syncWorkspaceFromDomain(domain)
  },
  { immediate: true },
)

const activeWorkspaceModel = computed(() => workspaceConfig[activeWorkspace.value])
</script>

<template>
  <div class="section-nav-body">
    <h3>{{ activeWorkspaceModel.label }} Namespaces</h3>

    <ul class="section-list">
      <li v-for="item in activeWorkspaceModel.namespaces" :key="item.to">
        <RouterLink :to="item.to">{{ item.label }}</RouterLink>
      </li>
    </ul>
  </div>
</template>
