<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { activeWorkspace, setActiveWorkspace, syncWorkspaceFromDomain } from '../lib/workspaceNav'

defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle'])

const route = useRoute()

watch(
  () => route.meta.domain,
  (domain) => {
    syncWorkspaceFromDomain(domain)
  },
  { immediate: true },
)

const isIdentityActive = computed(() => activeWorkspace.value === 'identity')
const isCustomizationActive = computed(() => activeWorkspace.value === 'customization')
</script>

<template>
  <nav class="rail-nav" :class="{ collapsed }">
    <div class="rail-scroll">
      <RouterLink class="rail-link" to="/home">
        <span class="rail-icon">⌂</span>
        <span v-if="!collapsed">Home</span>
      </RouterLink>

      <RouterLink
        class="rail-link"
        :class="{ 'workspace-link-active': isIdentityActive }"
        to="/users"
        @click="setActiveWorkspace('identity')"
      >
        <span class="rail-icon">🪪</span>
        <span v-if="!collapsed">Identity</span>
      </RouterLink>
      <RouterLink
        class="rail-link"
        :class="{ 'workspace-link-active': isCustomizationActive }"
        to="/workspaces"
        @click="setActiveWorkspace('customization')"
      >
        <span class="rail-icon">🧩</span>
        <span v-if="!collapsed">Customization</span>
      </RouterLink>
    </div>

    <button
      type="button"
      class="rail-collapse-toggle"
      :aria-label="collapsed ? 'Expand navigation pane' : 'Collapse navigation pane'"
      @click="$emit('toggle')"
    >
      <span>{{ collapsed ? '»' : '«' }}</span>
      <span v-if="!collapsed">Collapse</span>
    </button>
  </nav>
</template>
