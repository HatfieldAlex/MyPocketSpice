<template>
  <article :class="cardClasses" @click="handleClick">
    <slot />
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  clickable?: boolean
  elevated?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  clickable: false,
  elevated: true,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    emit('click', event)
  }
}

const cardClasses = computed(() => ({
  'card-elevated': props.elevated,
  'card-clickable': props.clickable,
}))
</script>

<style scoped>
article {
  background-color: #ffffff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(10, 10, 10, 0.1), 0 2px 4px -1px rgba(10, 10, 10, 0.06);
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.card-clickable {
  cursor: pointer;
}

.card-clickable:hover {
  box-shadow: 0 10px 15px -3px rgba(10, 10, 10, 0.1), 0 4px 6px -2px rgba(10, 10, 10, 0.05);
  transform: translateY(-2px);
}

.card-elevated {
  box-shadow: 0 4px 6px -1px rgba(10, 10, 10, 0.1), 0 2px 4px -1px rgba(10, 10, 10, 0.06);
}
</style>
