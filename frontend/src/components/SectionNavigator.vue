<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { activeWorkspace, workspaceConfig, syncWorkspaceFromDomain } from '../lib/workspaceNav'

defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
})

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
  <div class="section-nav-body pane-body">
    <ul class="section-list pane-list">
      <li v-for="item in activeWorkspaceModel.namespaces" :key="item.to">
        <RouterLink class="section-link pane-link" :to="item.to" :title="collapsed ? item.label : null">
          <span class="section-icon pane-icon" aria-hidden="true">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
