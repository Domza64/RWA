<template>
  <div class="flex flex-col bg-white border-4 border-black p-6 hover:-translate-y-1 hover:-translate-x-1 hover:bg-yellow-400 transition-all shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] h-full min-h-[160px]">
    <h2 class="text-2xl font-black uppercase tracking-wider mb-2 line-clamp-1 border-b-4 border-black pb-2">{{ data.name }}</h2>
    <p class="font-bold text-gray-800 line-clamp-3 flex-1 mt-2">{{ data.description || 'No description provided.' }}</p>
  </div>
</template>

<script setup lang="ts">
import type { Board } from '@/types/board'

interface Props {
  data: Board
}

defineProps<Props>()
</script>
