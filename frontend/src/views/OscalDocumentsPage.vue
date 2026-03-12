<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  createOscalSubmoduleDocument,
  listOscalSubmoduleDocuments,
} from '../lib/api'
import OscalDocumentDetailBlade from '../components/blades/OscalDocumentDetailBlade.vue'
import { useBladeStack } from '../lib/blades'
import { useDomainPermissions } from '../lib/permissions'

const props = defineProps({
  fixedType: {
    type: String,
    default: '',
  },
  titleOverride: {
    type: String,
    default: 'OSCAL',
  },
  viewMode: {
    type: String,
    default: 'manage',
  },
})

const domain = ref('oscal_documents')
const { canWrite } = useDomainPermissions(domain)
const bladeStack = useBladeStack()

const documentTypes = [
  { value: 'catalog', label: 'Catalog' },
  { value: 'profile', label: 'Profile' },
  { value: 'mapping', label: 'Mapping' },
  { value: 'assessment-plan', label: 'Assessment Plan' },
  { value: 'assessment-results', label: 'Assessment Results' },
  { value: 'poam', label: 'POA&M' },
  { value: 'component-definition', label: 'Component Definition' },
  { value: 'system-security-plan', label: 'System Security Plan' },
]

const selectedType = ref(props.fixedType || 'catalog')
const documents = ref([])
const title = ref('')
const importFile = ref(null)
const importFileName = ref('')
const fileInputKey = ref(0)
const loading = ref(true)
const creating = ref(false)
const error = ref('')
const status = ref('')
const isListView = computed(() => props.viewMode === 'list')
const isCreateView = computed(() => props.viewMode === 'create')

function extractContent(document) {
  if (!document || typeof document !== 'object') {
    return {}
  }
  if (document.content && typeof document.content === 'object' && !Array.isArray(document.content)) {
    return document.content
  }
  if (document.content_json && typeof document.content_json === 'object' && !Array.isArray(document.content_json)) {
    return document.content_json
  }
  return {}
}

function inferTitleFromFileName(fileName) {
  if (!fileName) {
    return ''
  }

  return fileName.replace(/\.[^.]+$/, '').trim()
}

function clearCreateEditor() {
  title.value = ''
  importFile.value = null
  importFileName.value = ''
  fileInputKey.value += 1
}

function handleImportFileChange(event) {
  const [file] = event?.target?.files || []
  importFile.value = file || null
  importFileName.value = file?.name || ''

  if (!title.value.trim() && file?.name) {
    title.value = inferTitleFromFileName(file.name)
  }
}

async function readImportedContent() {
  if (!importFile.value) {
    throw new Error('Select an OSCAL JSON file to import')
  }

  const fileText = await importFile.value.text()

  let parsed = null
  try {
    parsed = JSON.parse(fileText)
  } catch {
    throw new Error('Imported OSCAL file must be valid JSON')
  }

  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error('Imported OSCAL content must be a JSON object')
  }

  return parsed
}

async function loadDocuments() {
  if (isCreateView.value) {
    documents.value = []
    loading.value = false
    return
  }

  loading.value = true
  error.value = ''
  status.value = ''

  try {
    documents.value = await listOscalSubmoduleDocuments(selectedType.value)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  if (!canWrite.value) {
    return
  }

  creating.value = true
  error.value = ''
  status.value = ''

  try {
    const importedContent = await readImportedContent()
    const created = await createOscalSubmoduleDocument(selectedType.value, {
      title: title.value.trim() || null,
      content: importedContent,
    })

    documents.value = [created, ...documents.value]
    clearCreateEditor()
    status.value = 'OSCAL document created'
    openDocumentBlade(created)
  } catch (saveError) {
    error.value = saveError.message
  } finally {
    creating.value = false
  }
}

function handleTypeChange() {
  if (props.fixedType) {
    selectedType.value = props.fixedType
  }
  clearCreateEditor()
  bladeStack?.clearBlades()
  loadDocuments()
}

function upsertDocument(updated) {
  const existingIndex = documents.value.findIndex((item) => String(item.id) === String(updated.id))
  if (existingIndex < 0) {
    documents.value = [updated, ...documents.value]
    return
  }

  documents.value = documents.value.map((item, index) => {
    return index === existingIndex ? updated : item
  })
}

function removeDocument(documentId) {
  documents.value = documents.value.filter((item) => String(item.id) !== String(documentId))
}

function openDocumentBlade(document) {
  const documentId = String(document.id)
  const bladeId = `oscal-${selectedType.value}-${documentId}`

  bladeStack?.closeBlade(bladeId)
  bladeStack?.openBlade({
    id: bladeId,
    type: 'detail',
    title: document.title || '(untitled OSCAL document)',
    subtitle: `${document.document_type} · ${document.id}`,
    component: OscalDocumentDetailBlade,
    props: {
      bladeId,
      documentType: selectedType.value,
      documentId,
      onSaved: (updated) => {
        upsertDocument(updated)
        bladeStack?.updateBladeState(bladeId, {
          title: updated.title || '(untitled OSCAL document)',
          subtitle: `${updated.document_type} · ${updated.id}`,
        })
      },
      onDeleted: (deletedId) => {
        removeDocument(deletedId)
        status.value = 'OSCAL document deleted'
      },
    },
  })
}

function handleSelectDocument(document) {
  openDocumentBlade(document)
  error.value = ''
  status.value = ''
}

onMounted(loadDocuments)
</script>

<template>
  <section class="panel card shadow-sm border-0 rounded-4 p-4 bg-brand-surface/70">
    <h2 class="h3 fw-bold mb-3 text-brand-deep">{{ titleOverride }}</h2>

    <form v-if="!fixedType" class="form section-gap" @submit.prevent="handleTypeChange">
      <label>
        OSCAL Document Family
        <select v-model="selectedType" @change="handleTypeChange">
          <option v-for="item in documentTypes" :key="item.value" :value="item.value">{{ item.label }}</option>
        </select>
      </label>
    </form>

    <p v-if="loading">Loading OSCAL documents...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="status" class="meta">{{ status }}</p>

    <div v-if="!isCreateView" class="section-gap">
      <h3 class="h5 text-brand-deep">Documents</h3>
      <ul class="user-list" v-if="documents.length > 0">
        <li v-for="document in documents" :key="document.id">
          <button class="btn btn-link p-0" type="button" @click="handleSelectDocument(document)">
            {{ document.title || '(untitled OSCAL document)' }}
          </button>
          <span class="meta">{{ document.id }} · {{ document.document_type }}</span>
        </li>
      </ul>
      <p v-else class="meta">No documents found for this OSCAL family.</p>
    </div>

    <form v-if="canWrite && !isListView" class="form section-gap" @submit.prevent="handleCreate">
      <h3 class="h5 text-brand-deep">Import OSCAL Document</h3>

      <label>
        Title (optional)
        <input v-model="title" type="text" />
      </label>

      <label>
        OSCAL File
        <input
          :key="fileInputKey"
          type="file"
          accept=".json,application/json"
          required
          @change="handleImportFileChange"
        />
      </label>

      <p v-if="importFileName" class="meta">Selected file: {{ importFileName }}</p>

      <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-primary bg-primary hover:bg-accent border-0" type="submit" :disabled="creating">
          {{ creating ? 'Importing...' : 'Import Document' }}
        </button>
        <button class="btn btn-outline-secondary border-brand-purple/50 text-brand-purple hover:bg-brand-pink hover:text-white" type="button" @click="clearCreateEditor">
          Clear
        </button>
      </div>
    </form>
  </section>
</template>
