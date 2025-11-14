<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
})

defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => {
  return {
    [`button-${props.variant}`]: true,
    [`button-${props.size}`]: true,
    'button-disabled': props.disabled,
  }
})
</script>

<style scoped>
button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: 0.75rem;
  border: none;
  cursor: pointer;
  transition: color 200ms ease, background-color 200ms ease, border-color 200ms ease;
  outline: none;
  font-family: inherit;
}

button:focus-visible {
  outline: 2px solid #0a8961;
  outline-offset: 2px;
}

button:disabled {
  cursor: not-allowed;
}

/* Primary variant - Warm Pink */
.button-primary {
  background-color: #fed1f6;
  color: #0a0a0a;
}

.button-primary:hover:not(:disabled) {
  background-color: #fdb8f0;
}

.button-primary:disabled {
  background-color: #d9d9d9;
  color: #8a8a8a;
}

/* Secondary variant */
.button-secondary {
  background-color: #ffffff;
  color: #0a0a0a;
  border: 1px solid #e8e8e8;
}

.button-secondary:hover:not(:disabled) {
  background-color: #fffbfe;
  border-color: #fed1f6;
}

.button-secondary:disabled {
  background-color: #f5f5f5;
  color: #8a8a8a;
}

/* Accent variant - Green */
.button-accent {
  background-color: #0a8961;
  color: #ffffff;
}

.button-accent:hover:not(:disabled) {
  background-color: #066a4e;
}

.button-accent:disabled {
  background-color: #d9d9d9;
  color: #8a8a8a;
}

/* Ghost variant */
.button-ghost {
  background-color: transparent;
  color: #0a0a0a;
}

.button-ghost:hover:not(:disabled) {
  background-color: #fffbfe;
}

.button-ghost:disabled {
  color: #8a8a8a;
}

/* Sizes */
.button-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.button-md {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.button-lg {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}
</style>
