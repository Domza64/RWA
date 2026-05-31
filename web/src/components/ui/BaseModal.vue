<template>
  <Teleport to="body">
    <section
      class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-40"
      @click="handleClose"
    >
      <div
        class="relative bg-white border-4 border-black p-8 w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]"
        @click.stop
      >
        <button
          class="absolute top-4 right-4 font-black text-2xl leading-none border-4 border-black w-10 h-10 flex items-center justify-center hover:bg-black hover:text-white transition-colors"
          @click="handleClose"
        >
          &times;
        </button>

        <h2 class="text-3xl font-black uppercase tracking-tight mb-8 border-b-4 border-black pb-4">{{ title }}</h2>

        <slot></slot>
      </div>
    </section>
  </Teleport>
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
