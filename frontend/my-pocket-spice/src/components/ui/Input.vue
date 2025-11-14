<template>
  <div class="input-wrapper">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
    </label>
    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      class="input"
      @input="handleInput"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string
  type?: string
  label?: string
  placeholder?: string
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
}>()

const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #0a0a0a;
}

.input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #0a0a0a;
  background-color: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 200ms ease, box-shadow 200ms ease;
  font-family: inherit;
}

.input:focus {
  border-color: #0a8961;
  box-shadow: 0 0 0 3px rgba(10, 137, 97, 0.1);
}

.input:disabled {
  background-color: #f5f5f5;
  color: #8a8a8a;
  cursor: not-allowed;
}

.input::placeholder {
  color: #8a8a8a;
}
</style>
