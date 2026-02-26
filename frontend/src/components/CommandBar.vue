<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const domain = computed(() => route.meta.domain)
const selectedId = computed(() => route.params.id || null)
const contextSearch = ref(String(route.query.q || ''))

watch(
  () => route.query.q,
  (q) => {
    contextSearch.value = String(q || '')
  },
)

const listPath = computed(() => (domain.value ? `/${domain.value}` : '/'))

async function openList() {
  await router.push(listPath.value)
}

async function refreshPage() {
  await router.replace({
    path: route.path,
    query: {
      ...route.query,
      _refresh: String(Date.now()),
    },
  })
}

async function applyContextSearch() {
  await router.replace({
    path: route.path,
    query: {
      ...route.query,
      q: contextSearch.value || undefined,
    },
  })
}
</script>

<template>
  <div class="command-surface">
    <div class="command-primary">
      <button type="button" @click="openList"><span>＋</span><span>New</span></button>
      <button type="button"><span>✚</span><span>Create</span></button>
      <button type="button" :disabled="!selectedId"><span>✎</span><span>Edit</span></button>
      <button type="button" :disabled="!selectedId"><span>🗑</span><span>Delete</span></button>
      <button type="button"><span>⇩</span><span>Export</span></button>
      <button type="button" @click="refreshPage"><span>↻</span><span>Refresh</span></button>
    </div>

    <form class="command-search" @submit.prevent="applyContextSearch">
      <input v-model="contextSearch" type="search" placeholder="Search in this section" />
      <button type="submit">Apply</button>
    </form>
  </div>
</template>
