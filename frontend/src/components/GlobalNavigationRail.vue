<script setup>
import { Tooltip } from 'bootstrap'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { activeWorkspace, setActiveWorkspace, syncWorkspaceFromDomain, workspaceConfig } from '../lib/workspaceNav'

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle'])

const route = useRoute()
const router = useRouter()
const hasWorkspaceDomain = computed(() => Boolean(route.meta?.domain))

watch(
  () => route.meta.domain,
  (domain) => {
    syncWorkspaceFromDomain(domain)
  },
  { immediate: true },
)

const expandedWorkspace = ref(activeWorkspace.value)
const popupWorkspace = ref(null)
const workspaceGroups = computed(() => [
  {
    key: 'auth',
    label: 'Auth',
    icon: '🖥️',
    items: workspaceConfig.auth.namespaces,
  },
  {
    key: 'idm',
    label: 'Identity',
    icon: '🪪',
    items: workspaceConfig.idm.namespaces,
  },
  {
    key: 'customization',
    label: 'Customization',
    icon: '⚙️',
    items: workspaceConfig.customization.namespaces,
  },
])
const navRef = ref(null)
let tooltipInstances = []
let popupCloseTimer = null

watch(
  () => [activeWorkspace.value, hasWorkspaceDomain.value],
  ([workspace, hasDomain]) => {
    expandedWorkspace.value = hasDomain ? workspace : null
  },
  { immediate: true },
)

function toggleWorkspaceGroup(group) {
  setActiveWorkspace(group.key)

  if (props.collapsed) {
    return
  }

  popupWorkspace.value = null

  if (expandedWorkspace.value === group.key) {
    expandedWorkspace.value = null
    return
  }

  expandedWorkspace.value = group.key

  const firstItem = group.items?.[0]
  if (firstItem && route.path !== firstItem.to) {
    router.push(firstItem.to)
  }
}

function openPopupWorkspaceMenu(group) {
  if (!props.collapsed) {
    return
  }
  if (popupCloseTimer) {
    window.clearTimeout(popupCloseTimer)
    popupCloseTimer = null
  }
  setActiveWorkspace(group.key)
  popupWorkspace.value = group.key
}

function closePopupWorkspaceMenuOnLeave(group) {
  if (!props.collapsed) {
    return
  }
  if (popupWorkspace.value !== group.key) {
    return
  }

  if (popupCloseTimer) {
    window.clearTimeout(popupCloseTimer)
  }

  popupCloseTimer = window.setTimeout(() => {
    popupWorkspace.value = null
    popupCloseTimer = null
  }, 250)
}

function closePopupWorkspaceMenu() {
  if (popupCloseTimer) {
    window.clearTimeout(popupCloseTimer)
    popupCloseTimer = null
  }
  popupWorkspace.value = null
}

function handleDocumentClick(event) {
  if (!props.collapsed || !navRef.value) {
    return
  }

  if (!navRef.value.contains(event.target)) {
    closePopupWorkspaceMenu()
  }
}

function disposeTooltips() {
  tooltipInstances.forEach((instance) => instance.dispose())
  tooltipInstances = []
}

function syncTooltips() {
  disposeTooltips()

  if (!props.collapsed || !navRef.value) {
    return
  }

  const tooltipElements = navRef.value.querySelectorAll('.rail-tooltip[data-bs-toggle="tooltip"]')
  tooltipInstances = Array.from(tooltipElements).map(
    (element) => Tooltip.getOrCreateInstance(element, { container: 'body', trigger: 'hover focus' }),
  )
}

watch(
  () => props.collapsed,
  () => {
    if (!props.collapsed) {
      closePopupWorkspaceMenu()
    }
    nextTick(syncTooltips)
  },
  { immediate: true },
)

watch(
  () => route.fullPath,
  () => {
    if (!hasWorkspaceDomain.value) {
      expandedWorkspace.value = null
      closePopupWorkspaceMenu()
    }
    nextTick(syncTooltips)
  },
)

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
  if (popupCloseTimer) {
    window.clearTimeout(popupCloseTimer)
    popupCloseTimer = null
  }
  disposeTooltips()
})
</script>

<template>
  <nav ref="navRef" class="rail-nav pane-body" :class="{ collapsed }">
    <div class="rail-scroll pane-scroll-body">
      <RouterLink
        class="rail-link pane-link rail-tooltip"
        to="/home"
        :data-bs-toggle="collapsed ? 'tooltip' : null"
        :data-bs-title="collapsed ? 'Home' : null"
        :data-bs-placement="collapsed ? 'right' : null"
      >
        <span class="rail-icon pane-icon">🏠</span>
        <span v-if="!collapsed">Home</span>
      </RouterLink>

      <div
        v-for="group in workspaceGroups"
        :key="group.key"
        class="rail-group"
        @mouseenter="openPopupWorkspaceMenu(group)"
        @mouseleave="closePopupWorkspaceMenuOnLeave(group)"
      >
        <button
          type="button"
          class="rail-link pane-link rail-primary-link"
          :class="{ 'workspace-link-active': hasWorkspaceDomain && activeWorkspace === group.key }"
          :aria-expanded="String(!collapsed && expandedWorkspace === group.key)"
          @click="toggleWorkspaceGroup(group)"
        >
          <span class="rail-icon pane-icon">{{ group.icon }}</span>
          <span v-if="!collapsed" class="rail-primary-label">
            <span>{{ group.label }}</span>
          </span>
        </button>

        <div
          v-if="!collapsed && expandedWorkspace === group.key"
          class="rail-submenu"
        >
          <RouterLink
            v-for="item in group.items"
            :key="item.to"
            class="rail-link pane-link rail-sub-link"
            :to="item.to"
            @click="closePopupWorkspaceMenu"
          >
            <span class="rail-icon pane-icon">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </RouterLink>
        </div>

        <div
          v-if="collapsed && popupWorkspace === group.key"
          class="rail-submenu rail-popup-submenu"
        >
          <p class="rail-popup-group-name">{{ group.label }}</p>
          <RouterLink
            v-for="item in group.items"
            :key="`${group.key}-${item.to}`"
            class="rail-link pane-link rail-sub-link"
            :to="item.to"
            @click="closePopupWorkspaceMenu"
          >
            <span class="rail-icon pane-icon">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </RouterLink>
        </div>
      </div>
    </div>

    <button
      type="button"
      class="pane-bottom-toggle pane-toggle rail-tooltip"
      :aria-label="collapsed ? 'Expand navigation pane' : 'Collapse navigation pane'"
      :data-bs-toggle="collapsed ? 'tooltip' : null"
      :data-bs-title="collapsed ? 'Navigation' : null"
      :data-bs-placement="collapsed ? 'right' : null"
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
  </nav>
</template>
