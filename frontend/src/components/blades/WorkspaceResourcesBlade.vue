<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { getWorkspaceLabel, getWorkspaceNamespaces } from '../../lib/bladeCatalog'
import { useBladeStack } from '../../lib/blades'
import CustomizationAppsBlade from './CustomizationAppsBlade.vue'

const props = defineProps({
  workspaceKey: {
    type: String,
    required: true,
  },
  bladeId: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const bladeStack = useBladeStack()

const workspaceLabel = computed(() => getWorkspaceLabel(props.workspaceKey))
const resources = computed(() => getWorkspaceNamespaces(props.workspaceKey))
const isCustomizationWorkspace = computed(() => props.workspaceKey === 'customization')

function openResource(item) {
  if (!item?.to) {
    return
  }

  router.push(item.to)
}

function openCustomizationAppsBlade() {
  if (!bladeStack || !isCustomizationWorkspace.value) {
    return
  }

  const appBladeId = `${props.bladeId}-apps`
  bladeStack.closeBlade(appBladeId)
  bladeStack.openBlade({
    id: appBladeId,
    parentId: props.bladeId,
    type: 'resource',
    title: 'Custom Apps',
    subtitle: 'Open app resources in the blade workspace',
    component: CustomizationAppsBlade,
    props: {
      bladeId: appBladeId,
    },
  })
}
</script>

<template>
  <section class="d-flex flex-column gap-2">
    <p class="meta mb-1">{{ workspaceLabel }} resources</p>

    <button
      v-for="item in resources"
      :key="item.to"
      type="button"
      class="btn btn-sm btn-outline-secondary text-start"
      @click="openResource(item)"
    >
      <span class="me-2">{{ item.icon }}</span>
      <span>{{ item.label }}</span>
    </button>

    <button
      v-if="isCustomizationWorkspace"
      type="button"
      class="btn btn-sm btn-primary mt-2"
      @click="openCustomizationAppsBlade"
    >
      Open Custom Apps Blade
    </button>
  </section>
</template>