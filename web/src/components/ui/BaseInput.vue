<template>
  <div class="flex flex-col mb-2">
    <label :for="id">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :required="required"
      class="border border-green-800 rounded p-1"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup>
defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  required: { type: Boolean, default: false },
  modelValue: { type: [String, Number], default: '' },
})
defineEmits(['update:modelValue'])
</script>
