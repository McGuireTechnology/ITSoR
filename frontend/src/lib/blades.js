import { inject, provide, ref } from 'vue'

const BLADE_STACK_KEY = Symbol('blade-stack')

export function createBladeStack() {
  const blades = ref([])

  function openBlade(blade) {
    if (!blade?.id) {
      return
    }

    blades.value = [
      ...blades.value,
      {
        closable: true,
        dirty: false,
        scrollTop: 0,
        ...blade,
      },
    ]
  }

  function closeBlade(bladeId) {
    blades.value = blades.value.filter((blade) => blade.id !== bladeId)
  }

  function closeTopBlade() {
    if (blades.value.length === 0) {
      return
    }

    blades.value = blades.value.slice(0, -1)
  }

  function clearBlades() {
    blades.value = []
  }

  function closeToBlade(lastIndexToKeep) {
    if (lastIndexToKeep < 0) {
      clearBlades()
      return
    }

    blades.value = blades.value.slice(0, lastIndexToKeep + 1)
  }

  function updateBladeState(target, patch) {
    const index = typeof target === 'number'
      ? target
      : blades.value.findIndex((blade) => blade.id === target)

    if (index < 0 || index >= blades.value.length || !patch || typeof patch !== 'object') {
      return
    }

    blades.value = blades.value.map((blade, bladeIndex) => {
      if (bladeIndex !== index) {
        return blade
      }

      return {
        ...blade,
        ...patch,
      }
    })
  }

  return {
    blades,
    openBlade,
    closeBlade,
    closeTopBlade,
    clearBlades,
    closeToBlade,
    updateBladeState,
  }
}

export function provideBladeStack(bladeStack) {
  provide(BLADE_STACK_KEY, bladeStack)
}

export function useBladeStack() {
  return inject(BLADE_STACK_KEY, null)
}
