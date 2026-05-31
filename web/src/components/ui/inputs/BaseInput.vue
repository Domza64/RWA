<template>
  <div class="flex flex-col">
    <label :for="id" class="font-black uppercase text-sm mb-1">{{ label }}</label>

    <input
      :id="id"
      :type="type"
      :required="required"
      class="border-4 border-black p-2 bg-white focus:outline-none focus:bg-indigo-50 font-medium"
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
