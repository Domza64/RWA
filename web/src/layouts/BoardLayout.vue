<template>
  <div class="flex h-[calc(100vh-2.5rem)] overflow-hidden">
    <!-- Hide on /boards -->
    <div
      v-if="route.path !== '/boards'"
      class="w-64 shrink-0 border-r border-gray-200 mr-3 px-3 py-4 overflow-y-auto"
    >
      <RouterLink to="/boards">
        My boards
      </RouterLink>

      <div v-if="boardStore.loading">
        Loading boards...
      </div>

      <div v-else v-for="board in boards" :key="board.board_id">
        {{ board.name }}
      </div>

      <RouterLink to="/boards/create">Create a new board</RouterLink>
    </div>

    <div class="flex-1 overflow-hidden">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useBoardStore } from '@/stores/board'

const route = useRoute()
const boardStore = useBoardStore()

// triggers lazy load on first access
const boards = computed(() => boardStore.boards().value)
</script>