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

const hasWorkspaceDomain = computed(() => Boolean(route.meta?.domain))
const isPlatformActive = computed(() => hasWorkspaceDomain.value && activeWorkspace.value === 'platform')
const isIdentityActive = computed(() => hasWorkspaceDomain.value && activeWorkspace.value === 'idm')
const isCustomizationActive = computed(() => hasWorkspaceDomain.value && activeWorkspace.value === 'customization')
</script>

<template>
  <nav class="rail-nav pane-body" :class="{ collapsed }">
    <div class="rail-scroll pane-scroll-body">
      <RouterLink class="rail-link pane-link" to="/home" :title="collapsed ? 'Home' : null">
        <span class="rail-icon pane-icon">🏠</span>
        <span v-if="!collapsed">Home</span>
      </RouterLink>

      <RouterLink
        class="rail-link pane-link"
        :class="{ 'workspace-link-active': isPlatformActive }"
        to="/platform/users"
        :title="collapsed ? 'Platform' : null"
        @click="setActiveWorkspace('platform')"
      >
        <span class="rail-icon pane-icon">🖥️</span>
        <span v-if="!collapsed">Platform</span>
      </RouterLink>
      <RouterLink
        class="rail-link pane-link"
        :class="{ 'workspace-link-active': isIdentityActive }"
        to="/idm/people"
        :title="collapsed ? 'Identity' : null"
        @click="setActiveWorkspace('idm')"
      >
        <span class="rail-icon pane-icon">🪪</span>
        <span v-if="!collapsed">Identity</span>
      </RouterLink>
      <RouterLink
        class="rail-link pane-link"
        :class="{ 'workspace-link-active': isCustomizationActive }"
        to="/customization/workspaces"
        :title="collapsed ? 'Customization' : null"
        @click="setActiveWorkspace('customization')"
      >
        <span class="rail-icon pane-icon">⚙️</span>
        <span v-if="!collapsed">Customization</span>
      </RouterLink>
    </div>

    <button
      type="button"
      class="pane-bottom-toggle pane-toggle"
      :aria-label="collapsed ? 'Expand navigation pane' : 'Collapse navigation pane'"
      @click="$emit('toggle')"
    >
      <svg
        class="pane-toggle-icon"
        :class="collapsed ? 'is-expand is-left' : 'is-collapse is-left'"
        viewBox="0 0 16 16"
        aria-hidden="true"
      >
        <rect x="1.5" y="2" width="13" height="12" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.2" />
        <path d="M5 2V14" stroke="currentColor" stroke-width="1.2" />
        <path d="M10.5 5.5L7.5 8L10.5 10.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <span v-if="!collapsed">Workspaces</span>
    </button>
  </nav>
</template>
