<template>
  <Header />

  <div
    v-if="ui.loading"
    class="flex items-center justify-center min-h-[calc(100vh-3.5rem)] mt-14 bg-gray-100 px-4"
  >
    <div
      class="bg-yellow-400 text-black border-4 border-black p-8 md:p-16 shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] font-black uppercase tracking-widest text-3xl md:text-5xl flex items-center gap-4"
    >
      <span class="animate-bounce">Loading...</span>
    </div>
  </div>

  <main v-else class="mt-14">
    <RouterView />
  </main>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
</script>
