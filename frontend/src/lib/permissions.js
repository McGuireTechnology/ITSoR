import { computed, ref, unref } from 'vue'

const permissionsDirtyTick = ref(0)

const readOnlyDomains = new Set([
  'auth_home',
  'idm_home',
  'customization_home',
  'grc_home',
])

function normalizeDomain(domain) {
  return String(domain || '').trim()
}

function resolveWritePermission(domain) {
  if (!domain) {
    return true
  }

  if (readOnlyDomains.has(domain)) {
    return false
  }

  return true
}

export function useDomainPermissions(domainRef) {
  const canWrite = computed(() => {
    permissionsDirtyTick.value
    const domain = normalizeDomain(unref(domainRef))
    return resolveWritePermission(domain)
  })

  return {
    canWrite,
  }
}

export function markPermissionsDirty() {
  permissionsDirtyTick.value += 1
}
