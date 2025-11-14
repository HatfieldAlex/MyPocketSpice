<template>
  <span :class="badgeClasses">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'accent' | 'neutral'
  size?: 'sm' | 'md'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
})

const badgeClasses = computed(() => {
  return {
    [`badge-${props.variant}`]: true,
    [`badge-${props.size}`]: true,
  }
})
</script>

<style scoped>
span {
  display: inline-flex;
  align-items: center;
  border-radius: 9999px;
  font-weight: 500;
}

.badge-primary {
  background-color: #fff5fc;
  color: #0a0a0a;
  border: 1px solid #fed1f6;
}

.badge-accent {
  background-color: #e6f5f1;
  color: #066a4e;
  border: 1px solid #0a8961;
}

.badge-neutral {
  background-color: #f5f5f5;
  color: #4a4a4a;
  border: 1px solid #e8e8e8;
}

.badge-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.badge-md {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}
</style>
