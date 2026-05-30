<template>
  <div class="flex flex-col mb-2">
    <label :for="id">{{ label }}</label>

    <input
      :id="id"
      :type="type"
      :required="required"
      class="border border-indigo-800 rounded p-1"
      :value="modelValue"
      @input="onInput"
    />
  </div>
</template>

<script setup lang="ts">
defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  required: { type: Boolean, default: false },
  modelValue: { type: [String, Number], default: '' },
})

const emit = defineEmits(['update:modelValue'])

function onInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>
