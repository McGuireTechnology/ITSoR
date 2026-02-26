<script setup>
import { nextTick, ref, watch } from 'vue'

const props = defineProps({
  blades: {
    type: Array,
    required: true,
  },
  rootTitle: {
    type: String,
    default: 'Workspace',
  },
})

const emit = defineEmits(['close-top', 'close-to', 'update-blade'])

const bladeRefs = new Map()
const bladeContentRefs = new Map()
const rootSectionRef = ref(null)

function focusFirstFocusableInElement(element) {
  if (!(element instanceof HTMLElement)) {
    return false
  }

  const focusable = element.querySelector(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
  )

  if (focusable instanceof HTMLElement) {
    focusable.focus()
    return true
  }

  if (element.tabIndex >= 0) {
    element.focus()
    return true
  }

  return false
}

function setBladeRef(index, element) {
  if (element) {
    bladeRefs.set(index, element)
  } else {
    bladeRefs.delete(index)
  }
}

function setBladeContentRef(index, element) {
  if (element) {
    bladeContentRefs.set(index, element)
  } else {
    bladeContentRefs.delete(index)
  }
}

function focusFirstFocusable(index) {
  const bladeElement = bladeRefs.get(index)
  if (!bladeElement) {
    return
  }

  if (!focusFirstFocusableInElement(bladeElement)) {
    bladeElement.focus()
  }
}

function trapTabOnTopBlade(event) {
  if (props.blades.length === 0 || event.key !== 'Tab') {
    return
  }

  const topIndex = props.blades.length - 1
  const bladeElement = bladeRefs.get(topIndex)
  if (!bladeElement) {
    return
  }

  const focusable = Array.from(
    bladeElement.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    ),
  ).filter((element) => element instanceof HTMLElement && !element.hasAttribute('disabled'))

  if (focusable.length === 0) {
    return
  }

  const first = focusable[0]
  const last = focusable[focusable.length - 1]
  const active = document.activeElement

  if (event.shiftKey && active === first) {
    event.preventDefault()
    last.focus()
  } else if (!event.shiftKey && active === last) {
    event.preventDefault()
    first.focus()
  }
}

function handleKeydown(event) {
  if (event.key === 'Escape' && props.blades.length > 0) {
    event.preventDefault()
    emit('close-top')
    return
  }

  trapTabOnTopBlade(event)
}

function handleRootClick() {
  if (props.blades.length > 0) {
    emit('close-to', 0)
  }
}

function handleBladeClick(index) {
  if (index < props.blades.length - 1) {
    emit('close-to', index + 1)
  }
}

function handleBladeScroll(index, event) {
  emit('update-blade', {
    index,
    patch: {
      scrollTop: event.target.scrollTop,
    },
  })
}

watch(
  () => props.blades.length,
  async (nextLength, previousLength) => {
    if (nextLength > previousLength) {
      await nextTick()
      focusFirstFocusable(nextLength - 1)
    }

    if (nextLength > 0) {
      await nextTick()
      const topBlade = bladeContentRefs.get(nextLength - 1)
      const saved = props.blades[nextLength - 1]?.scrollTop || 0
      if (topBlade) {
        topBlade.scrollTop = saved
      }
    }

    if (nextLength < previousLength) {
      await nextTick()
      if (nextLength > 0) {
        focusFirstFocusable(nextLength - 1)
      } else {
        focusFirstFocusableInElement(rootSectionRef.value)
      }
    }
  },
)
</script>

<template>
  <div class="blade-viewport" @keydown="handleKeydown">
    <section ref="rootSectionRef" class="blade blade-root" aria-label="Root workspace" @click="handleRootClick">
      <header class="blade-header">
        <h2 class="blade-title">{{ rootTitle }}</h2>
      </header>
      <div class="blade-content">
        <slot />
      </div>
    </section>

    <section
      v-for="(blade, index) in blades"
      :key="blade.id"
      :ref="(element) => setBladeRef(index, element)"
      class="blade"
      role="dialog"
      aria-modal="false"
      :aria-labelledby="`blade-title-${blade.id}`"
      tabindex="-1"
      @click="handleBladeClick(index)"
    >
      <header class="blade-header">
        <div class="blade-heading">
          <h3 :id="`blade-title-${blade.id}`" class="blade-title">
            {{ blade.title }}
            <span v-if="blade.dirty" class="blade-dirty-dot" aria-label="Unsaved changes">●</span>
          </h3>
          <p v-if="blade.subtitle" class="blade-subtitle">{{ blade.subtitle }}</p>
        </div>
        <button
          v-if="blade.closable"
          type="button"
          class="blade-close"
          aria-label="Close blade"
          @click.stop="emit('close-to', index)"
        >
          ✕
        </button>
      </header>

      <div
        :ref="(element) => setBladeContentRef(index, element)"
        class="blade-content"
        @scroll="handleBladeScroll(index, $event)"
      >
        <component :is="blade.component" v-bind="blade.props" />
      </div>

      <footer v-if="blade.footerActions?.length" class="blade-footer">
        <button
          v-for="action in blade.footerActions"
          :key="action.label"
          type="button"
          :class="action.className || 'btn btn-sm btn-outline-secondary'"
          @click="action.onClick?.()"
        >
          {{ action.label }}
        </button>
      </footer>
    </section>
  </div>
</template>
