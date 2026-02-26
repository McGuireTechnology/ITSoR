<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import BladeWorkspace from '../components/BladeWorkspace.vue'
import CommandBar from '../components/CommandBar.vue'
import ContextInspectorPane from '../components/ContextInspectorPane.vue'
import GlobalNavigationRail from '../components/GlobalNavigationRail.vue'
import PageHeader from '../components/PageHeader.vue'
import SectionNavigator from '../components/SectionNavigator.vue'
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
const manuallyCollapsed = ref(false)
const manuallySectionCollapsed = ref(false)
const manuallyInspectorHidden = ref(false)
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1440)
const bladeStack = createBladeStack()

provideBladeStack(bladeStack)

const autoCollapsed = computed(() => viewportWidth.value <= 1200)
const railCollapsed = computed(() => autoCollapsed.value || manuallyCollapsed.value)
const sectionApplicable = computed(() => Boolean(route.meta.domain))
const sectionUnavailable = computed(() => !sectionApplicable.value)
const autoSectionCollapsed = computed(() => viewportWidth.value <= 1320)
const sectionCollapsed = computed(() => autoSectionCollapsed.value || manuallySectionCollapsed.value)
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

function toggleSectionCollapse() {
  if (autoSectionCollapsed.value) {
    return
  }
  manuallySectionCollapsed.value = !manuallySectionCollapsed.value
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
      'section-collapsed': sectionCollapsed,
      'section-unavailable': sectionUnavailable,
      'inspector-collapsed': inspectorCollapsed,
      'inspector-unavailable': inspectorUnavailable,
      'content-is-detail': contentIsDetail,
    }"
  >
    <TopBar />

    <div class="admin-shell">
      <aside class="admin-rail">
        <GlobalNavigationRail :collapsed="railCollapsed" @toggle="toggleRailCollapse" />
      </aside>

      <aside v-if="sectionApplicable" class="admin-section-nav">
        <div v-if="!sectionCollapsed" class="pane-scroll">
          <SectionNavigator />
        </div>
        <button
          type="button"
          class="pane-bottom-toggle"
          :aria-label="sectionCollapsed ? 'Expand namespace pane' : 'Collapse namespace pane'"
          @click="toggleSectionCollapse"
        >
          {{ sectionCollapsed ? '» Expand namespace' : '« Collapse namespace' }}
        </button>
      </aside>

      <section class="admin-workspace">
        <PageHeader />
        <CommandBar />
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

      <aside v-if="inspectorApplicable" class="admin-inspector" :aria-hidden="inspectorHidden">
        <div v-if="!inspectorHidden" class="pane-scroll">
          <ContextInspectorPane />
        </div>
        <button
          type="button"
          class="pane-bottom-toggle"
          :aria-label="inspectorHidden ? 'Expand inspector pane' : 'Collapse inspector pane'"
          @click="toggleInspector"
        >
          {{ inspectorHidden ? '« Expand inspector' : '» Collapse inspector' }}
        </button>
      </aside>
    </div>
  </div>
</template>
