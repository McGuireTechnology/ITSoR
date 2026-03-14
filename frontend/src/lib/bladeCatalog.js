import { workspaceConfig } from './workspaceNav'

const iconByLabel = {
  Users: '👤',
  Groups: '👥',
  Tenants: '🏢',
  Workspaces: '🗂️',
  Namespaces: '📦',
  'Entity Types': '🧩',
  'Entity Records': '🗃️',
  OSCAL: '🛡️',
}

function decorateItems(items) {
  return items.map((item) => {
    const label = String(item?.label || '')

    return {
      ...item,
      icon: String(item?.icon || iconByLabel[label] || '📄'),
    }
  })
}

export function getWorkspaceLabel(workspaceKey) {
  return String(workspaceConfig[workspaceKey]?.label || 'Workspace')
}

export function getWorkspaceNamespaces(workspaceKey) {
  const namespaces = workspaceConfig[workspaceKey]?.namespaces || []
  return decorateItems(namespaces)
}

export function getCustomizationApps() {
  return [
    ...getWorkspaceNamespaces('customization'),
    {
      label: 'OSCAL',
      to: '/customization/oscal',
      icon: iconByLabel.OSCAL,
    },
  ]
}
