<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CommandBar from '../components/CommandBar.vue'
import ContextInspectorPane from '../components/ContextInspectorPane.vue'
import GlobalNavigationRail from '../components/GlobalNavigationRail.vue'
import PageHeader from '../components/PageHeader.vue'
import SectionNavigator from '../components/SectionNavigator.vue'
import TopBar from '../components/TopBar.vue'

defineProps({
  isAuthenticated: {
    type: Boolean,
    required: true,
  },
})

const route = useRoute()
const title = computed(() => route.meta.title || 'Workspace')
</script>

<template>
  <div class="admin-root">
    <TopBar />

    <div class="admin-shell">
      <aside class="admin-rail">
        <GlobalNavigationRail />
      </aside>

      <aside class="admin-section-nav">
        <SectionNavigator />
      </aside>

      <section class="admin-workspace">
        <PageHeader />
        <CommandBar />
        <main class="page-body">
          <slot />
        </main>
      </section>

      <aside class="admin-inspector">
        <ContextInspectorPane />
      </aside>
    </div>
  </div>
</template>
