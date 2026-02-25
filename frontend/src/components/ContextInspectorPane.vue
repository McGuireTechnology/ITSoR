<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const sectionTitle = computed(() => route.meta.title || 'Details')
const selectedId = computed(() => route.params.id || null)
const domain = computed(() => route.meta.domain || '')
const listPath = computed(() => (domain.value ? `/${domain.value}` : '/'))
</script>

<template>
  <div class="inspector-body">
    <h3>Inspector</h3>
    <dl class="inspector-detail">
      <dt>Section</dt>
      <dd>{{ sectionTitle }}</dd>
      <dt>Route</dt>
      <dd>{{ route.path }}</dd>
      <dt>Selected ID</dt>
      <dd>{{ selectedId || 'None selected' }}</dd>
    </dl>

    <div class="section-gap">
      <RouterLink :to="listPath">Open section list</RouterLink>
    </div>
  </div>
</template>
