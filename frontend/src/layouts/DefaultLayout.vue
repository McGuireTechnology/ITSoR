<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import BladeWorkspace from '../components/BladeWorkspace.vue'
import CommandBar from '../components/CommandBar.vue'
import ContextInspectorPane from '../components/ContextInspectorPane.vue'
import GlobalNavigationRail from '../components/GlobalNavigationRail.vue'
import PageHeader from '../components/PageHeader.vue'
import TopBar from '../components/TopBar.vue'
import { createBladeStack, provideBladeStack } from '../lib/blades'

defineProps({
  isAuthenticated: {
    type: Boolean,
    required: true,
  },
})

const route = useRoute()
const title = computed(() => route.meta.title || 'Workspace')
const showCommandBar = computed(() => route.meta.showCommandBar !== false)
const manuallyCollapsed = ref(false)
const manuallyInspectorHidden = ref(false)
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1440)
const bladeStack = createBladeStack()

provideBladeStack(bladeStack)

const autoCollapsed = computed(() => viewportWidth.value <= 1200)
const railCollapsed = computed(() => autoCollapsed.value || manuallyCollapsed.value)
const autoInspectorHidden = computed(() => viewportWidth.value <= 1280)
const inspectorApplicable = computed(() => {
  return Boolean(route.meta.domain) || Boolean(route.params.id) || bladeStack.blades.value.length > 0
})
const inspectorUnavailable = computed(() => !inspectorApplicable.value)
const inspectorCollapsed = computed(() => autoInspectorHidden.value || manuallyInspectorHidden.value)
const inspectorHidden = computed(() => inspectorUnavailable.value || inspectorCollapsed.value)
const contentIsDetail = computed(() => bladeStack.blades.value.length > 0)
const useSimpleContentPane = computed(() => !route.meta.domain && bladeStack.blades.value.length === 0)

function toggleRailCollapse() {
  if (autoCollapsed.value) {
    return
  }
  manuallyCollapsed.value = !manuallyCollapsed.value
}

function toggleInspector() {
  if (!inspectorApplicable.value || autoInspectorHidden.value) {
    return
  }
  manuallyInspectorHidden.value = !manuallyInspectorHidden.value
}

function syncViewport() {
  viewportWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', syncViewport)
})

onUnmounted(() => {
  window.removeEventListener('resize', syncViewport)
})

watch(
  () => route.fullPath,
  () => {
    bladeStack.clearBlades()
    manuallyInspectorHidden.value = false
  },
)

function handleCloseTopBlade() {
  bladeStack.closeTopBlade()
}

function handleCloseToBlade(index) {
  if (index <= 0) {
    bladeStack.clearBlades()
    return
  }
  bladeStack.closeToBlade(index - 1)
}

function handleBladeUpdate(event) {
  bladeStack.updateBladeState(event.index, event.patch)
}
</script>

<template>
  <div
    class="admin-root"
    :class="{
      'rail-collapsed': railCollapsed,
      'inspector-collapsed': inspectorCollapsed,
      'inspector-unavailable': inspectorUnavailable,
      'content-is-detail': contentIsDetail,
    }"
  >
    <TopBar />

    <div class="admin-shell">
      <aside class="admin-rail admin-pane">
        <GlobalNavigationRail :collapsed="railCollapsed" @toggle="toggleRailCollapse" />
      </aside>

      <section class="admin-workspace">
        <PageHeader />
        <CommandBar v-if="showCommandBar" />
        <main v-if="useSimpleContentPane" class="page-body">
          <slot />
        </main>
        <BladeWorkspace
          v-else
          :blades="bladeStack.blades.value"
          :root-title="title"
          @close-top="handleCloseTopBlade"
          @close-to="handleCloseToBlade"
          @update-blade="handleBladeUpdate"
        >
          <slot />
        </BladeWorkspace>
      </section>

      <aside v-if="inspectorApplicable" class="admin-inspector admin-pane" :aria-hidden="inspectorHidden">
        <div v-if="!inspectorHidden" class="pane-scroll">
          <ContextInspectorPane />
        </div>
        <button
          type="button"
          class="pane-bottom-toggle pane-toggle"
          :aria-label="inspectorHidden ? 'Expand inspector pane' : 'Collapse inspector pane'"
          @click="toggleInspector"
        >
          <svg
            class="pane-toggle-icon"
            :class="inspectorHidden ? 'is-expand is-right' : 'is-collapse is-right'"
            viewBox="0 0 16 16"
            aria-hidden="true"
          >
            <rect x="1.5" y="2" width="13" height="12" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.2" />
            <path d="M11 2V14" stroke="currentColor" stroke-width="1.2" />
            <path d="M5.5 5.5L8.5 8L5.5 10.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <span v-if="!inspectorHidden">Inspector</span>
        </button>
      </aside>
    </div>
  </div>
</template>
