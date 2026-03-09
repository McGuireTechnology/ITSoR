<script setup>
import { Tooltip } from 'bootstrap'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import WorkspaceResourcesBlade from './blades/WorkspaceResourcesBlade.vue'
import { useBladeStack } from '../lib/blades'
import { groupedNavigation, isFavorite, toggleFavorite, getRecentItemsForResource } from '../lib/navigationState'
import { activeWorkspace, setActiveWorkspace, syncWorkspaceFromDomain } from '../lib/workspaceNav'

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle'])

const route = useRoute()
const router = useRouter()
const bladeStack = useBladeStack()
const hasWorkspaceDomain = computed(() => Boolean(route.meta?.domain))

watch(
  () => route.meta.domain,
  (domain) => {
    syncWorkspaceFromDomain(domain)
  },
  { immediate: true },
)

const expandedWorkspace = ref(activeWorkspace.value)
const expandedResource = ref(String(route.meta?.domain || ''))
const popupWorkspace = ref(null)
const workspaceGroups = computed(() => groupedNavigation.value)
const navRef = ref(null)
let tooltipInstances = []
let popupCloseTimer = null

watch(
  () => [activeWorkspace.value, hasWorkspaceDomain.value],
  ([workspace, hasDomain]) => {
    expandedWorkspace.value = hasDomain ? workspace : null
    expandedResource.value = hasDomain ? String(route.meta?.domain || '') : ''
  },
  { immediate: true },
)

function toggleWorkspaceGroup(group) {
  setActiveWorkspace(group.key)
  openWorkspaceBlade(group)

  const firstItem = group.resources?.[0]
  if (firstItem?.to && route.path !== firstItem.to) {
    router.push(firstItem.to)
  }

  if (props.collapsed) {
    return
  }

  popupWorkspace.value = null

  if (expandedWorkspace.value === group.key) {
    expandedWorkspace.value = null
    expandedResource.value = ''
    return
  }

  expandedWorkspace.value = group.key
  expandedResource.value = String(firstItem?.key || '')
}

function openWorkspaceBlade(group) {
  if (!bladeStack) {
    return
  }

  const bladeId = `workspace-${group.key}`
  bladeStack.closeBlade(bladeId)
  bladeStack.openBlade({
    id: bladeId,
    type: 'resource',
    title: `${group.label} Resources`,
    subtitle: 'Open resources without losing context',
    component: WorkspaceResourcesBlade,
    props: {
      workspaceKey: group.key,
      bladeId,
    },
  })
}

function toggleResource(resource) {
  expandedResource.value = expandedResource.value === resource.key ? '' : resource.key

  if (resource?.to && route.path !== resource.to) {
    router.push(resource.to)
  }
}

function isResourceActive(resource) {
  if (!resource?.to) {
    return false
  }

  return route.path === resource.to || route.path.startsWith(`${resource.to}/`) || String(route.meta?.domain || '') === resource.key
}

function listEntries(resource) {
  const recentItems = getRecentItemsForResource(resource.key, 5).map((item) => ({
    level: 'list',
    key: `recent:${item.key}`,
    label: item.label,
    to: item.to,
    domainKey: item.domainKey,
    resourceKey: item.resourceKey,
    isRecentItem: true,
    itemKey: item.key,
  }))

  return [...resource.lists, ...recentItems]
}

function domainFavoriteEntry(group) {
  const firstRoute = group.resources?.[0]?.to || '/home'
  return {
    level: 'domain',
    key: group.key,
    label: group.label,
    to: firstRoute,
    domainKey: group.key,
    resourceKey: '',
  }
}

function resourceFavoriteEntry(group, resource) {
  return {
    level: 'resource',
    key: resource.key,
    label: `${group.label} · ${resource.label}`,
    to: resource.to,
    domainKey: group.key,
    resourceKey: resource.key,
  }
}

function listFavoriteEntry(group, resource, listItem) {
  return {
    level: listItem.isRecentItem ? 'item' : 'list',
    key: listItem.isRecentItem ? listItem.itemKey : listItem.key,
    label: `${resource.label} · ${listItem.label}`,
    to: listItem.to,
    domainKey: group.key,
    resourceKey: resource.key,
  }
}

function toggleFavoriteFor(entry) {
  toggleFavorite(entry)
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
    expandedResource.value = String(route.meta?.domain || '')
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
        <div class="rail-entry-row">
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
          <button
            v-if="!collapsed"
            type="button"
            class="rail-favorite-btn"
            :aria-label="isFavorite('domain', group.key) ? `Remove ${group.label} from favorites` : `Favorite ${group.label}`"
            @click.stop="toggleFavoriteFor(domainFavoriteEntry(group))"
          >
            {{ isFavorite('domain', group.key) ? '★' : '☆' }}
          </button>
        </div>

        <div
          v-if="!collapsed && expandedWorkspace === group.key"
          class="rail-submenu"
        >
          <div v-for="resource in group.resources" :key="resource.to" class="rail-resource-group">
            <div class="rail-entry-row">
              <button
                type="button"
                class="rail-link pane-link rail-sub-link rail-resource-link"
                :class="{ 'router-link-active': isResourceActive(resource) }"
                @click="toggleResource(resource)"
              >
                <span class="rail-icon pane-icon">{{ resource.icon }}</span>
                <span class="rail-list-label">{{ resource.label }}</span>
              </button>
              <button
                type="button"
                class="rail-favorite-btn"
                :aria-label="isFavorite('resource', resource.key) ? `Remove ${resource.label} from favorites` : `Favorite ${resource.label}`"
                @click.stop="toggleFavoriteFor(resourceFavoriteEntry(group, resource))"
              >
                {{ isFavorite('resource', resource.key) ? '★' : '☆' }}
              </button>
            </div>

            <div v-if="expandedResource === resource.key" class="rail-list-blade">
              <div v-for="listItem in listEntries(resource)" :key="`${resource.key}-${listItem.key}`" class="rail-entry-row">
                <RouterLink
                  class="rail-link pane-link rail-sub-link rail-list-link"
                  :to="listItem.to"
                  @click="closePopupWorkspaceMenu"
                >
                  <span class="rail-list-label">{{ listItem.label }}</span>
                </RouterLink>
                <button
                  type="button"
                  class="rail-favorite-btn"
                  :aria-label="isFavorite(listItem.isRecentItem ? 'item' : 'list', listItem.isRecentItem ? listItem.itemKey : listItem.key) ? `Remove ${listItem.label} from favorites` : `Favorite ${listItem.label}`"
                  @click.stop="toggleFavoriteFor(listFavoriteEntry(group, resource, listItem))"
                >
                  {{ isFavorite(listItem.isRecentItem ? 'item' : 'list', listItem.isRecentItem ? listItem.itemKey : listItem.key) ? '★' : '☆' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="collapsed && popupWorkspace === group.key"
          class="rail-submenu rail-popup-submenu"
        >
          <p class="rail-popup-group-name">{{ group.label }}</p>
          <div v-for="resource in group.resources" :key="`${group.key}-${resource.key}`" class="rail-resource-group">
            <RouterLink
              class="rail-link pane-link rail-sub-link"
              :to="resource.to"
              @click="closePopupWorkspaceMenu"
            >
              <span class="rail-icon pane-icon">{{ resource.icon }}</span>
              <span>{{ resource.label }}</span>
            </RouterLink>

            <RouterLink
              v-for="listItem in listEntries(resource)"
              :key="`${resource.key}-${listItem.key}`"
              class="rail-link pane-link rail-sub-link rail-list-link"
              :to="listItem.to"
              @click="closePopupWorkspaceMenu"
            >
              <span class="rail-list-label">{{ listItem.label }}</span>
            </RouterLink>
          </div>
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
