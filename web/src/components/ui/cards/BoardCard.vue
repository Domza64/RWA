<template>
  <div class="flex flex-col bg-gray-400 hover:bg-gray-500 transition-all duration-300 rounded p-4 shadow-md cursor-pointer">
    <span>{{ data.name }}</span>
    <span>{{ data.description }}</span>
  </div>
</template>

<script setup lang="ts">
import type { Board } from '@/types/board'

interface Props {
  data: Board
}

defineProps<Props>()
</script>
