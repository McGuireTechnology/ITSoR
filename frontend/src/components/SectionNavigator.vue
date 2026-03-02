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

const route = useRoute()

watch(
  () => route.meta.domain,
  (domain) => {
    syncWorkspaceFromDomain(domain)
  },
  { immediate: true },
)

const activeWorkspaceModel = computed(() => workspaceConfig[activeWorkspace.value])
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
    <ul class="section-list pane-list">
      <li v-for="item in activeWorkspaceModel.namespaces" :key="item.to">
        <RouterLink
          class="section-link pane-link"
          :to="item.to"
          :data-bs-toggle="collapsed ? 'tooltip' : null"
          :data-bs-title="collapsed ? item.label : null"
          :data-bs-placement="collapsed ? 'right' : null"
        >
          <span class="section-icon pane-icon" aria-hidden="true">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
