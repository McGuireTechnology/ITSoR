<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { getCustomizationApps } from '../../lib/bladeCatalog'

const router = useRouter()
const apps = computed(() => getCustomizationApps())

function openApp(app) {
  if (!app?.to) {
    return
  }

  router.push(app.to)
}
</script>

<template>
  <section class="d-flex flex-column gap-2">
    <p class="meta mb-1">Custom apps</p>

    <button
      v-for="app in apps"
      :key="app.to"
      type="button"
      class="btn btn-sm btn-outline-secondary text-start"
      @click="openApp(app)"
    >
      <span class="me-2">{{ app.icon }}</span>
      <span>{{ app.label }}</span>
    </button>
  </section>
</template>