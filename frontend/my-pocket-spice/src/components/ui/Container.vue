<template>
  <div :class="containerClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { spacing } from '@/design-system/tokens'

interface Props {
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full'
  padding?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  maxWidth: 'xl',
  padding: true,
})

const containerClasses = computed(() => {
  const maxWidths = {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
    full: '100%',
  }

  return {
    width: '100%',
    maxWidth: maxWidths[props.maxWidth],
    margin: '0 auto',
    padding: props.padding ? `0 ${spacing[4]}` : '0',
  }
})
</script>

<style scoped>
div {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 768px) {
  div {
    padding: 0 2rem;
  }
}
</style>
