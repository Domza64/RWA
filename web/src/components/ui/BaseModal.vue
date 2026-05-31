<template>
  <section
    class="fixed inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm z-50"
    @click="handleClose"
  >
    <div
      class="relative bg-white p-6 rounded-lg shadow-md w-1/2 max-h-[90vh] overflow-y-auto"
      @click.stop
    >
      <button
        class="absolute top-4 right-4 text-2xl text-gray-500 hover:text-gray-800"
        @click="handleClose"
      >
        &times;
      </button>

      <h2 class="text-3xl font-bold mb-6">{{ title }}</h2>

      <slot></slot>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

function handleClose() {
  emit('close')
}
</script>
