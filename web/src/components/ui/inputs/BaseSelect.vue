<template>
  <div class="flex flex-col mb-2">
    <label :for="id">{{ label }}</label>
    <select
      :id="id"
      :required="required"
      class="border border-indigo-800 rounded p-1 bg-white"
      :value="modelValue"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
export interface SelectOption {
  value: string | number
  label: string
}

withDefaults(defineProps<{
  id: string
  label: string
  options: SelectOption[]
  required?: boolean
  modelValue?: string | number | null
  placeholder?: string
}>(), {
  required: false,
  modelValue: null,
  placeholder: '',
})

defineEmits(['update:modelValue'])
</script>
