<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import {
  deleteOscalSubmoduleDocument,
  getOscalSubmoduleDocument,
  replaceOscalSubmoduleDocument,
} from '../../lib/api'
import { useBladeStack } from '../../lib/blades'
import { useDomainPermissions } from '../../lib/permissions'

const props = defineProps({
  bladeId: {
    type: String,
    required: true,
  },
  documentType: {
    type: String,
    required: true,
  },
  documentId: {
    type: String,
    required: true,
  },
  onSaved: {
    type: Function,
    default: null,
  },
  onDeleted: {
    type: Function,
    default: null,
  },
})

const bladeStack = useBladeStack()
const domain = ref('oscal')
const { canWrite } = useDomainPermissions(domain)

const document = ref(null)
const title = ref('')
const contentText = ref('{\n  \n}')
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const confirmingDelete = ref(false)
const error = ref('')
const status = ref('')

const canEdit = computed(() => canWrite.value && !loading.value)

function extractContent(payload) {
  if (!payload || typeof payload !== 'object') {
    return {}
  }
  if (payload.content && typeof payload.content === 'object' && !Array.isArray(payload.content)) {
    return payload.content
  }
  if (payload.content_json && typeof payload.content_json === 'object' && !Array.isArray(payload.content_json)) {
    return payload.content_json
  }
  return {}
}

function parseContent() {
  try {
    const parsed = JSON.parse(contentText.value)
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      throw new Error('OSCAL content must be a JSON object')
    }
    return parsed
  } catch {
    throw new Error('OSCAL content must be valid JSON object')
  }
}

async function loadDocument() {
  loading.value = true
  error.value = ''
  status.value = ''

  try {
    const loaded = await getOscalSubmoduleDocument(props.documentType, props.documentId)
    document.value = loaded
    title.value = loaded.title || ''
    contentText.value = JSON.stringify(extractContent(loaded), null, 2)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!document.value || !canEdit.value) {
    return
  }

  saving.value = true
  error.value = ''
  status.value = ''

  try {
    const updated = await replaceOscalSubmoduleDocument(props.documentType, props.documentId, {
      title: title.value.trim() || null,
      content: parseContent(),
    })

    document.value = updated
    title.value = updated.title || ''
    contentText.value = JSON.stringify(extractContent(updated), null, 2)

    if (typeof props.onSaved === 'function') {
      props.onSaved(updated)
    }

    status.value = 'OSCAL document updated'
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!document.value || !canEdit.value) {
    return
  }

  deleting.value = true
  error.value = ''
  status.value = ''

  try {
    await deleteOscalSubmoduleDocument(props.documentType, props.documentId)

    if (typeof props.onDeleted === 'function') {
      props.onDeleted(props.documentId)
    }

    bladeStack?.closeBlade(props.bladeId)
  } catch (deleteError) {
    error.value = deleteError.message
  } finally {
    deleting.value = false
  }
}

function startDeleteConfirmation() {
  confirmingDelete.value = true
}

function cancelDeleteConfirmation() {
  confirmingDelete.value = false
}

onMounted(loadDocument)

watch(
  () => [props.documentType, props.documentId],
  () => {
    confirmingDelete.value = false
    loadDocument()
  },
)
</script>

<template>
  <section>
    <p v-if="loading">Loading OSCAL document...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <template v-else>
      <p v-if="status" class="meta">{{ status }}</p>

      <form class="blade-form" @submit.prevent="handleSave">
        <label class="blade-field">
          <span>Title (optional)</span>
          <input v-model="title" type="text" :disabled="!canEdit || saving" />
        </label>

        <label class="blade-field">
          <span>Content JSON</span>
          <textarea v-model="contentText" rows="14" :disabled="!canEdit || saving" required />
        </label>

        <button class="btn btn-sm btn-primary" type="submit" :disabled="!canEdit || saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </form>

      <dl class="user-detail section-gap">
        <dt>ID</dt>
        <dd>{{ document.id }}</dd>
        <dt>Type</dt>
        <dd>{{ document.document_type }}</dd>
      </dl>

      <div v-if="canEdit" class="section-gap">
        <button
          v-if="!confirmingDelete"
          class="btn btn-sm btn-outline-secondary"
          type="button"
          :disabled="deleting"
          @click="startDeleteConfirmation"
        >
          Delete OSCAL Document
        </button>

        <div v-else class="confirm-row">
          <p class="error mb-0">Delete this OSCAL document?</p>
          <button class="btn btn-sm btn-primary" type="button" :disabled="deleting" @click="handleDelete">
            {{ deleting ? 'Deleting...' : 'Confirm Delete' }}
          </button>
          <button class="btn btn-sm btn-outline-secondary" type="button" :disabled="deleting" @click="cancelDeleteConfirmation">
            Cancel
          </button>
        </div>
      </div>
    </template>
  </section>
</template>
