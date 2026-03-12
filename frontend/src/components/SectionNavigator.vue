<script setup>
import { Tooltip } from 'bootstrap'
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { activeWorkspace, workspaceConfig, syncWorkspaceFromDomain } from '../lib/workspaceNav'

const props = defineProps({
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

const activeWorkspaceModel = computed(() => workspaceConfig[activeWorkspace.value] || { namespaces: [] })
const normalizedNamespaces = computed(() => {
  return (activeWorkspaceModel.value.namespaces || [])
    .map((item, index) => {
      const to = String(item?.to || item?.resources?.[0]?.to || '')
      if (!to) {
        return null
      }

      return {
        key: item?.key || `${item?.label || 'namespace'}-${index}`,
        label: String(item?.label || 'Workspace'),
        icon: String(item?.icon || '🧭'),
        to,
      }
    })
    .filter(Boolean)
})
const sectionNavRef = ref(null)
let tooltipInstances = []

function disposeTooltips() {
  tooltipInstances.forEach((instance) => instance.dispose())
  tooltipInstances = []
}

function syncTooltips() {
  disposeTooltips()

  if (!props.collapsed || !sectionNavRef.value) {
    return
  }

  const tooltipElements = sectionNavRef.value.querySelectorAll('[data-bs-toggle="tooltip"]')
  tooltipInstances = Array.from(tooltipElements).map(
    (element) => Tooltip.getOrCreateInstance(element, { container: 'body', trigger: 'hover focus' }),
  )
}

watch(
  () => props.collapsed,
  () => {
    nextTick(syncTooltips)
  },
  { immediate: true },
)

watch(
  () => route.fullPath,
  () => {
    nextTick(syncTooltips)
  },
)

onBeforeUnmount(() => {
  disposeTooltips()
})
</script>

<template>
  <div ref="sectionNavRef" class="section-nav-body pane-body">
    <ul class="section-list pane-list pane-scroll-body">
      <li v-for="item in normalizedNamespaces" :key="item.key">
        <RouterLink
          class="section-link pane-link"
          :to="item.to"
          :data-bs-toggle="collapsed ? 'tooltip' : null"
          :data-bs-title="collapsed ? item.label : null"
          :data-bs-placement="collapsed ? 'right' : null"
        >
          <span class="section-icon pane-icon" aria-hidden="true">{{ item.icon }}</span>
          <span v-if="!collapsed">{{ item.label }}</span>
        </RouterLink>
      </li>
    </ul>

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
      <span v-if="!collapsed">Navigation</span>
    </button>
  </div>
</template>
