<template>
  <section
    class="fixed inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm"
    @click="handleClose"
  >
    <div
      class="relative bg-white p-6 rounded-lg shadow-md w-1/2 h-1/2"
      @click.stop
    >
      <button
        class="absolute top-4 right-4 text-2xl"
        @click="handleClose"
      >
        x
      </button>

      <span class="text-4xl font-bold">Create ticket</span>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function handleClose(): void {
  router.back()
}
</script>