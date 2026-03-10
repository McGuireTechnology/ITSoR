<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  createNavigationModule,
  createNavigationResource,
  createNavigationView,
  deleteNavigationModule,
  deleteNavigationResource,
  deleteNavigationView,
  listNavigationTree,
  loadNavigationDefaults,
  listTenants,
  patchNavigationModule,
  patchNavigationResource,
  patchNavigationView,
  setNavigationDefault,
} from '../lib/api'

const TENANT_STORAGE_KEY = 'itsor.activeTenantId'

const loading = ref(true)
const error = ref('')
const activeMenu = ref('combined')
const navigationTree = ref([])
const tenants = ref([])
const selectedTenantId = ref('')
const savingKeys = ref(new Set())
const defaultSelection = ref({ module_id: '', resource_id: '', view_id: '' })
const dragPayload = ref(null)

const editModules = ref({})
const editResources = ref({})
const editViews = ref({})

const newModule = ref({ key: '', label: '', module_type: 'custom', icon: '🗂️', order: 0, enabled: true })
const newResource = ref({ key: '', label: '', module_id: '', list_route: '', icon: '📁', order: 0, enabled: true })
const newView = ref({ key: '', label: '', resource_id: '', route: '', view_type: 'list', icon: '📄', order: 0, enabled: true })

const modules = computed(() => (Array.isArray(navigationTree.value) ? navigationTree.value : []))
const resources = computed(() => modules.value.flatMap((module) => module.resources || []))
const views = computed(() => resources.value.flatMap((resource) => resource.views || []))

const defaultResourceOptions = computed(() =>
  resources.value.filter((item) => item.module_id === defaultSelection.value.module_id),
)

const defaultViewOptions = computed(() =>
  views.value.filter((item) => item.resource_id === defaultSelection.value.resource_id),
)

function iconFor(type, item) {
  if (item?.icon) {
    return item.icon
  }
  if (type === 'module') {
    return '🗂️'
  }
  if (type === 'resource') {
    return '📁'
  }
  return '📄'
}

function isSaving(key) {
  return savingKeys.value.has(key)
}

function markSaving(key, value) {
  const next = new Set(savingKeys.value)
  if (value) {
    next.add(key)
  } else {
    next.delete(key)
  }
  savingKeys.value = next
}

function getTenantFromStorage() {
  if (typeof window === 'undefined') {
    return ''
  }
  return String(window.localStorage.getItem(TENANT_STORAGE_KEY) || '')
}

function moduleDraft(module) {
  if (!editModules.value[module.id]) {
    editModules.value[module.id] = {
      label: module.label,
      order: Number(module.order || 0),
      enabled: Boolean(module.enabled),
      icon: module.icon || iconFor('module', module),
    }
  }
  return editModules.value[module.id]
}

function resourceDraft(resource) {
  if (!editResources.value[resource.id]) {
    editResources.value[resource.id] = {
      label: resource.label,
      module_id: resource.module_id,
      list_route: resource.list_route,
      order: Number(resource.order || 0),
      enabled: Boolean(resource.enabled),
      icon: resource.icon || iconFor('resource', resource),
    }
  }
  return editResources.value[resource.id]
}

function viewDraft(view) {
  if (!editViews.value[view.id]) {
    editViews.value[view.id] = {
      label: view.label,
      resource_id: view.resource_id,
      route: view.route,
      order: Number(view.order || 0),
      enabled: Boolean(view.enabled),
      icon: view.icon || iconFor('view', view),
    }
  }
  return editViews.value[view.id]
}

function resetDrafts() {
  editModules.value = {}
  editResources.value = {}
  editViews.value = {}
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const tenantId = selectedTenantId.value || undefined
    const [tree, tenantList] = await Promise.all([
      listNavigationTree({ tenantId, includeDisabled: true }),
      listTenants(),
    ])
    navigationTree.value = Array.isArray(tree) ? tree : []
    tenants.value = Array.isArray(tenantList) ? tenantList : []

    if (!newResource.value.module_id && modules.value.length) {
      newResource.value.module_id = modules.value[0].id
    }
    if (!newView.value.resource_id && resources.value.length) {
      newView.value.resource_id = resources.value[0].id
    }

    if (!defaultSelection.value.module_id && modules.value.length) {
      defaultSelection.value.module_id = modules.value[0].id
    }
    const selectedModuleResources = resources.value.filter((item) => item.module_id === defaultSelection.value.module_id)
    if (!selectedModuleResources.some((item) => item.id === defaultSelection.value.resource_id)) {
      defaultSelection.value.resource_id = selectedModuleResources[0]?.id || ''
    }
    const selectedResourceViews = views.value.filter((item) => item.resource_id === defaultSelection.value.resource_id)
    if (!selectedResourceViews.some((item) => item.id === defaultSelection.value.view_id)) {
      defaultSelection.value.view_id = selectedResourceViews[0]?.id || ''
    }
  } catch (loadError) {
    error.value = loadError.message || 'Failed to load navigation'
  } finally {
    loading.value = false
  }
}

async function saveModule(module) {
  const key = `module:${module.id}`
  markSaving(key, true)
  error.value = ''
  try {
    await patchNavigationModule(module.id, {
      tenant_id: selectedTenantId.value || null,
      ...moduleDraft(module),
    })
    await loadData()
    resetDrafts()
  } catch (saveError) {
    error.value = saveError.message || 'Failed to save module'
  } finally {
    markSaving(key, false)
  }
}

async function saveResource(resource) {
  const key = `resource:${resource.id}`
  markSaving(key, true)
  error.value = ''
  try {
    await patchNavigationResource(resource.id, {
      tenant_id: selectedTenantId.value || null,
      ...resourceDraft(resource),
    })
    await loadData()
    resetDrafts()
  } catch (saveError) {
    error.value = saveError.message || 'Failed to save resource'
  } finally {
    markSaving(key, false)
  }
}

async function saveView(view) {
  const key = `view:${view.id}`
  markSaving(key, true)
  error.value = ''
  try {
    await patchNavigationView(view.id, {
      tenant_id: selectedTenantId.value || null,
      ...viewDraft(view),
    })
    await loadData()
    resetDrafts()
  } catch (saveError) {
    error.value = saveError.message || 'Failed to save view'
  } finally {
    markSaving(key, false)
  }
}

async function onCreateModule() {
  error.value = ''
  try {
    await createNavigationModule({
      ...newModule.value,
      tenant_id: selectedTenantId.value || null,
    })
    newModule.value = { key: '', label: '', module_type: 'custom', icon: '🗂️', order: 0, enabled: true }
    await loadData()
    resetDrafts()
  } catch (createError) {
    error.value = createError.message || 'Failed to create module'
  }
}

async function onCreateResource() {
  error.value = ''
  try {
    await createNavigationResource({
      ...newResource.value,
      tenant_id: selectedTenantId.value || null,
    })
    newResource.value = {
      key: '',
      label: '',
      module_id: modules.value[0]?.id || '',
      list_route: '',
      icon: '📁',
      order: 0,
      enabled: true,
    }
    await loadData()
    resetDrafts()
  } catch (createError) {
    error.value = createError.message || 'Failed to create resource'
  }
}

async function onCreateView() {
  error.value = ''
  try {
    await createNavigationView({
      ...newView.value,
      tenant_id: selectedTenantId.value || null,
    })
    newView.value = {
      key: '',
      label: '',
      resource_id: resources.value[0]?.id || '',
      route: '',
      view_type: 'list',
      icon: '📄',
      order: 0,
      enabled: true,
    }
    await loadData()
    resetDrafts()
  } catch (createError) {
    error.value = createError.message || 'Failed to create view'
  }
}

async function onDeleteModule(module) {
  if (!window.confirm(`Delete module ${module.label}?`)) {
    return
  }
  error.value = ''
  try {
    await deleteNavigationModule(module.id, selectedTenantId.value || null)
    await loadData()
    resetDrafts()
  } catch (deleteError) {
    error.value = deleteError.message || 'Failed to delete module'
  }
}

async function onDeleteResource(resource) {
  if (!window.confirm(`Delete resource ${resource.label}?`)) {
    return
  }
  error.value = ''
  try {
    await deleteNavigationResource(resource.id, selectedTenantId.value || null)
    await loadData()
    resetDrafts()
  } catch (deleteError) {
    error.value = deleteError.message || 'Failed to delete resource'
  }
}

async function onDeleteView(view) {
  if (!window.confirm(`Delete view ${view.label}?`)) {
    return
  }
  error.value = ''
  try {
    await deleteNavigationView(view.id, selectedTenantId.value || null)
    await loadData()
    resetDrafts()
  } catch (deleteError) {
    error.value = deleteError.message || 'Failed to delete view'
  }
}

async function onLoadDefaults() {
  error.value = ''
  try {
    await loadNavigationDefaults(selectedTenantId.value || null)
    await loadData()
    resetDrafts()
  } catch (actionError) {
    error.value = actionError.message || 'Failed to load defaults'
  }
}

async function onSetDefaultMenu() {
  error.value = ''
  try {
    await setNavigationDefault({
      tenant_id: selectedTenantId.value || null,
      module_id: defaultSelection.value.module_id,
      resource_id: defaultSelection.value.resource_id || null,
      view_id: defaultSelection.value.view_id || null,
    })
    await loadData()
  } catch (actionError) {
    error.value = actionError.message || 'Failed to set default menu'
  }
}

function onTenantChange(event) {
  selectedTenantId.value = String(event.target.value || '')
  resetDrafts()
  loadData()
}

function onDragStart(type, item, parentId = null) {
  dragPayload.value = {
    type,
    id: item.id,
    parentId,
  }
}

function allowDrop(event) {
  event.preventDefault()
}

async function reorderModules(draggedId, targetId) {
  const ordered = [...modules.value].sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
  const dragged = ordered.find((item) => item.id === draggedId)
  const target = ordered.find((item) => item.id === targetId)
  if (!dragged || !target || dragged.id === target.id) {
    return
  }
  const filtered = ordered.filter((item) => item.id !== dragged.id)
  const targetIndex = filtered.findIndex((item) => item.id === target.id)
  filtered.splice(targetIndex, 0, dragged)

  for (let index = 0; index < filtered.length; index += 1) {
    const item = filtered[index]
    if (Number(item.order || 0) !== index) {
      await patchNavigationModule(item.id, {
        tenant_id: selectedTenantId.value || null,
        order: index,
      })
    }
  }
}

async function reorderResources(parentModuleId, draggedId, targetId) {
  const siblings = resources.value
    .filter((item) => item.module_id === parentModuleId)
    .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))

  const dragged = siblings.find((item) => item.id === draggedId)
  const target = siblings.find((item) => item.id === targetId)
  if (!dragged || !target || dragged.id === target.id) {
    return
  }

  const filtered = siblings.filter((item) => item.id !== dragged.id)
  const targetIndex = filtered.findIndex((item) => item.id === target.id)
  filtered.splice(targetIndex, 0, dragged)

  for (let index = 0; index < filtered.length; index += 1) {
    const item = filtered[index]
    if (Number(item.order || 0) !== index || item.module_id !== parentModuleId) {
      await patchNavigationResource(item.id, {
        tenant_id: selectedTenantId.value || null,
        module_id: parentModuleId,
        order: index,
      })
    }
  }
}

async function reorderViews(parentResourceId, draggedId, targetId) {
  const siblings = views.value
    .filter((item) => item.resource_id === parentResourceId)
    .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))

  const dragged = siblings.find((item) => item.id === draggedId)
  const target = siblings.find((item) => item.id === targetId)
  if (!dragged || !target || dragged.id === target.id) {
    return
  }

  const filtered = siblings.filter((item) => item.id !== dragged.id)
  const targetIndex = filtered.findIndex((item) => item.id === target.id)
  filtered.splice(targetIndex, 0, dragged)

  for (let index = 0; index < filtered.length; index += 1) {
    const item = filtered[index]
    if (Number(item.order || 0) !== index || item.resource_id !== parentResourceId) {
      await patchNavigationView(item.id, {
        tenant_id: selectedTenantId.value || null,
        resource_id: parentResourceId,
        order: index,
      })
    }
  }
}

async function onDropModule(targetModule) {
  if (!dragPayload.value) {
    return
  }

  const payload = dragPayload.value
  dragPayload.value = null
  error.value = ''

  try {
    if (payload.type === 'module') {
      await reorderModules(payload.id, targetModule.id)
    }

    if (payload.type === 'resource') {
      const moduleResources = resources.value
        .filter((item) => item.module_id === targetModule.id)
        .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
      await patchNavigationResource(payload.id, {
        tenant_id: selectedTenantId.value || null,
        module_id: targetModule.id,
        order: moduleResources.length,
      })
    }

    await loadData()
  } catch (dropError) {
    error.value = dropError.message || 'Failed to move item'
  }
}

async function onDropResource(targetResource) {
  if (!dragPayload.value) {
    return
  }

  const payload = dragPayload.value
  dragPayload.value = null
  error.value = ''

  try {
    if (payload.type === 'resource') {
      await reorderResources(targetResource.module_id, payload.id, targetResource.id)
    }

    if (payload.type === 'view') {
      const resourceViews = views.value
        .filter((item) => item.resource_id === targetResource.id)
        .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
      await patchNavigationView(payload.id, {
        tenant_id: selectedTenantId.value || null,
        resource_id: targetResource.id,
        order: resourceViews.length,
      })
    }

    await loadData()
  } catch (dropError) {
    error.value = dropError.message || 'Failed to move item'
  }
}

async function onDropView(targetView) {
  if (!dragPayload.value) {
    return
  }

  const payload = dragPayload.value
  dragPayload.value = null
  error.value = ''

  try {
    if (payload.type === 'view') {
      await reorderViews(targetView.resource_id, payload.id, targetView.id)
    }
    await loadData()
  } catch (dropError) {
    error.value = dropError.message || 'Failed to move item'
  }
}

onMounted(async () => {
  selectedTenantId.value = getTenantFromStorage()
  await loadData()
})
</script>

<template>
  <section class="dashboard-page bg-brand-surface rounded-3xl p-4 md:p-5">
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h2 class="text-brand-deep mb-0">Navigation</h2>
      <span class="meta">Manage Modules, Resources, and Views</span>
    </div>

    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <label class="meta mb-0" for="tenant-scope">Tenant scope</label>
      <select id="tenant-scope" class="form-select form-select-sm w-auto" :value="selectedTenantId" @change="onTenantChange">
        <option value="">System defaults</option>
        <option v-for="tenant in tenants" :key="tenant.id" :value="tenant.id">{{ tenant.name }} ({{ tenant.id }})</option>
      </select>
      <button class="btn btn-sm btn-outline-secondary" type="button" :disabled="loading" @click="loadData">Reload</button>
      <button class="btn btn-sm btn-outline-primary" type="button" :disabled="loading" @click="onLoadDefaults">Load Defaults</button>
    </div>

    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <span class="meta">Default menu</span>
      <select v-model="defaultSelection.module_id" class="form-select form-select-sm w-auto">
        <option v-for="module in modules" :key="module.id" :value="module.id">{{ module.label }}</option>
      </select>
      <select v-model="defaultSelection.resource_id" class="form-select form-select-sm w-auto">
        <option v-for="resource in defaultResourceOptions" :key="resource.id" :value="resource.id">{{ resource.label }}</option>
      </select>
      <select v-model="defaultSelection.view_id" class="form-select form-select-sm w-auto">
        <option v-for="view in defaultViewOptions" :key="view.id" :value="view.id">{{ view.label }}</option>
      </select>
      <button class="btn btn-sm btn-primary" type="button" :disabled="loading || !defaultSelection.module_id" @click="onSetDefaultMenu">Save Default</button>
    </div>

    <div class="d-flex flex-wrap gap-2 mb-3">
      <button class="btn btn-sm" :class="activeMenu === 'combined' ? 'btn-primary' : 'btn-outline-secondary'" type="button" @click="activeMenu = 'combined'">Combined</button>
      <button class="btn btn-sm" :class="activeMenu === 'modules' ? 'btn-primary' : 'btn-outline-secondary'" type="button" @click="activeMenu = 'modules'">Modules</button>
      <button class="btn btn-sm" :class="activeMenu === 'resources' ? 'btn-primary' : 'btn-outline-secondary'" type="button" @click="activeMenu = 'resources'">Resources</button>
      <button class="btn btn-sm" :class="activeMenu === 'views' ? 'btn-primary' : 'btn-outline-secondary'" type="button" @click="activeMenu = 'views'">Views</button>
    </div>

    <p v-if="loading">Loading…</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <div v-if="activeMenu === 'combined'" class="pane-combined">
        <p class="meta mb-2">Drag modules, resources, and views to reorder or re-parent. Icons are shown inline.</p>
        <div class="rail-submenu">
          <div v-for="module in modules" :key="`combo-module-${module.id}`" class="rail-resource-group">
            <div
              class="rail-link pane-link rail-primary-link combo-row"
              draggable="true"
              @dragstart="onDragStart('module', module)"
              @dragover="allowDrop"
              @drop="onDropModule(module)"
            >
              <span class="combo-drag">⋮⋮</span>
              <span class="rail-icon pane-icon">{{ iconFor('module', module) }}</span>
              <span class="rail-list-label">{{ module.label }}</span>
            </div>

            <div v-for="resource in (module.resources || [])" :key="`combo-resource-${resource.id}`" class="combo-indent-1">
              <div
                class="rail-link pane-link rail-sub-link combo-row"
                draggable="true"
                @dragstart="onDragStart('resource', resource, module.id)"
                @dragover="allowDrop"
                @drop="onDropResource(resource)"
              >
                <span class="combo-drag">⋮⋮</span>
                <span class="rail-icon pane-icon">{{ iconFor('resource', resource) }}</span>
                <span class="rail-list-label">{{ resource.label }}</span>
              </div>

              <div v-for="view in (resource.views || [])" :key="`combo-view-${view.id}`" class="combo-indent-2">
                <div
                  class="rail-link pane-link rail-sub-link rail-list-link combo-row"
                  draggable="true"
                  @dragstart="onDragStart('view', view, resource.id)"
                  @dragover="allowDrop"
                  @drop="onDropView(view)"
                >
                  <span class="combo-drag">⋮⋮</span>
                  <span class="rail-icon pane-icon">{{ iconFor('view', view) }}</span>
                  <span class="rail-list-label">{{ view.label }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeMenu === 'modules'">
        <h3 class="section-gap">Create Module</h3>
        <div class="d-flex flex-wrap gap-2 mb-3">
          <input v-model="newModule.key" class="form-control form-control-sm w-auto" placeholder="Key" />
          <input v-model="newModule.label" class="form-control form-control-sm w-auto" placeholder="Label" />
          <input v-model="newModule.icon" class="form-control form-control-sm w-auto" placeholder="Icon" />
          <select v-model="newModule.module_type" class="form-select form-select-sm w-auto">
            <option value="custom">custom</option>
            <option value="app">app</option>
            <option value="system">system</option>
          </select>
          <input v-model.number="newModule.order" class="form-control form-control-sm w-auto" type="number" min="0" placeholder="Order" />
          <label class="meta d-flex align-items-center gap-1 mb-0"><input v-model="newModule.enabled" type="checkbox" /> Enabled</label>
          <button class="btn btn-sm btn-primary" type="button" @click="onCreateModule">Create</button>
        </div>

        <table class="data-table">
          <thead>
            <tr><th>Icon</th><th>Key</th><th>Label</th><th>Type</th><th>Enabled</th><th>Order</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="module in modules" :key="module.id">
              <td><input v-model="moduleDraft(module).icon" class="form-control form-control-sm" /></td>
              <td>{{ module.key }}</td>
              <td><input v-model="moduleDraft(module).label" class="form-control form-control-sm" /></td>
              <td>{{ module.module_type }}</td>
              <td><input v-model="moduleDraft(module).enabled" type="checkbox" /></td>
              <td><input v-model.number="moduleDraft(module).order" class="form-control form-control-sm" type="number" min="0" /></td>
              <td class="d-flex gap-2">
                <button class="btn btn-sm btn-primary" type="button" :disabled="isSaving(`module:${module.id}`)" @click="saveModule(module)">Save</button>
                <button class="btn btn-sm btn-outline-danger" type="button" :disabled="isSaving(`module:${module.id}`)" @click="onDeleteModule(module)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeMenu === 'resources'">
        <h3 class="section-gap">Create Resource</h3>
        <div class="d-flex flex-wrap gap-2 mb-3">
          <input v-model="newResource.key" class="form-control form-control-sm w-auto" placeholder="Key" />
          <input v-model="newResource.label" class="form-control form-control-sm w-auto" placeholder="Label" />
          <input v-model="newResource.icon" class="form-control form-control-sm w-auto" placeholder="Icon" />
          <select v-model="newResource.module_id" class="form-select form-select-sm w-auto">
            <option v-for="module in modules" :key="module.id" :value="module.id">{{ module.label }}</option>
          </select>
          <input v-model="newResource.list_route" class="form-control form-control-sm w-auto" placeholder="List Route" />
          <input v-model.number="newResource.order" class="form-control form-control-sm w-auto" type="number" min="0" placeholder="Order" />
          <label class="meta d-flex align-items-center gap-1 mb-0"><input v-model="newResource.enabled" type="checkbox" /> Enabled</label>
          <button class="btn btn-sm btn-primary" type="button" @click="onCreateResource">Create</button>
        </div>

        <table class="data-table">
          <thead>
            <tr><th>Icon</th><th>Key</th><th>Label</th><th>Parent Module</th><th>List Route</th><th>Enabled</th><th>Order</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="resource in resources" :key="resource.id">
              <td><input v-model="resourceDraft(resource).icon" class="form-control form-control-sm" /></td>
              <td>{{ resource.key }}</td>
              <td><input v-model="resourceDraft(resource).label" class="form-control form-control-sm" /></td>
              <td>
                <select v-model="resourceDraft(resource).module_id" class="form-select form-select-sm">
                  <option v-for="module in modules" :key="module.id" :value="module.id">{{ module.label }}</option>
                </select>
              </td>
              <td><input v-model="resourceDraft(resource).list_route" class="form-control form-control-sm" /></td>
              <td><input v-model="resourceDraft(resource).enabled" type="checkbox" /></td>
              <td><input v-model.number="resourceDraft(resource).order" class="form-control form-control-sm" type="number" min="0" /></td>
              <td class="d-flex gap-2">
                <button class="btn btn-sm btn-primary" type="button" :disabled="isSaving(`resource:${resource.id}`)" @click="saveResource(resource)">Save</button>
                <button class="btn btn-sm btn-outline-danger" type="button" :disabled="isSaving(`resource:${resource.id}`)" @click="onDeleteResource(resource)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeMenu === 'views'">
        <h3 class="section-gap">Create View</h3>
        <div class="d-flex flex-wrap gap-2 mb-3">
          <input v-model="newView.key" class="form-control form-control-sm w-auto" placeholder="Key" />
          <input v-model="newView.label" class="form-control form-control-sm w-auto" placeholder="Label" />
          <input v-model="newView.icon" class="form-control form-control-sm w-auto" placeholder="Icon" />
          <select v-model="newView.resource_id" class="form-select form-select-sm w-auto">
            <option v-for="resource in resources" :key="resource.id" :value="resource.id">{{ resource.label }}</option>
          </select>
          <input v-model="newView.route" class="form-control form-control-sm w-auto" placeholder="Route" />
          <select v-model="newView.view_type" class="form-select form-select-sm w-auto">
            <option value="list">list</option>
            <option value="detail">detail</option>
            <option value="form">form</option>
            <option value="board">board</option>
            <option value="calendar">calendar</option>
            <option value="dashboard">dashboard</option>
          </select>
          <input v-model.number="newView.order" class="form-control form-control-sm w-auto" type="number" min="0" placeholder="Order" />
          <label class="meta d-flex align-items-center gap-1 mb-0"><input v-model="newView.enabled" type="checkbox" /> Enabled</label>
          <button class="btn btn-sm btn-primary" type="button" @click="onCreateView">Create</button>
        </div>

        <table class="data-table">
          <thead>
            <tr><th>Icon</th><th>Key</th><th>Label</th><th>Parent Resource</th><th>Route</th><th>Enabled</th><th>Order</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="view in views" :key="view.id">
              <td><input v-model="viewDraft(view).icon" class="form-control form-control-sm" /></td>
              <td>{{ view.key }}</td>
              <td><input v-model="viewDraft(view).label" class="form-control form-control-sm" /></td>
              <td>
                <select v-model="viewDraft(view).resource_id" class="form-select form-select-sm">
                  <option v-for="resource in resources" :key="resource.id" :value="resource.id">{{ resource.label }}</option>
                </select>
              </td>
              <td><input v-model="viewDraft(view).route" class="form-control form-control-sm" /></td>
              <td><input v-model="viewDraft(view).enabled" type="checkbox" /></td>
              <td><input v-model.number="viewDraft(view).order" class="form-control form-control-sm" type="number" min="0" /></td>
              <td class="d-flex gap-2">
                <button class="btn btn-sm btn-primary" type="button" :disabled="isSaving(`view:${view.id}`)" @click="saveView(view)">Save</button>
                <button class="btn btn-sm btn-outline-danger" type="button" :disabled="isSaving(`view:${view.id}`)" @click="onDeleteView(view)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </section>
</template>

<style scoped>
.pane-combined {
  border: 1px solid color-mix(in srgb, var(--itsor-purple) 20%, #cbd5e1);
  border-radius: 0.75rem;
  background: #ffffff;
  padding: 0.5rem;
}

.combo-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  border-radius: 0.5rem;
  margin-bottom: 0.25rem;
}

.combo-row:hover {
  background: color-mix(in srgb, var(--itsor-surface-tint) 75%, #ffffff);
}

.combo-drag {
  opacity: 0.6;
  font-size: 0.8rem;
}

.combo-indent-1 {
  padding-left: 1.25rem;
}

.combo-indent-2 {
  padding-left: 2.25rem;
}
</style>
