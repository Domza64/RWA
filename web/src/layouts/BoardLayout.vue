<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useBoardStore } from '@/stores/board'

const route = useRoute()
const boardStore = useBoardStore()

const boards = computed(() => boardStore.boards())

function isActive(boardId: number) {
  return route.params.board_id === String(boardId) ? 'bg-indigo-50 border-indigo-300' : ''
}
</script>

<template>
  <div class="flex h-[calc(100vh-2.5rem)] overflow-hidden">
    <!-- Sidebar -->
    <aside
      v-if="route.path !== '/boards'"
      class="w-64 shrink-0 border-r border-gray-300 px-3 py-4 overflow-y-auto bg-white"
    >
      <!-- Header -->
      <div class="mb-4">
        <RouterLink to="/boards" class="text-lg font-semibold text-gray-700 hover:text-gray-900">
          My boards
        </RouterLink>
      </div>

      <!-- Loading -->
      <div v-if="boardStore.loading" class="text-sm text-gray-400">Loading boards...</div>

      <!-- Boards list -->
      <div v-else class="space-y-2">
        <RouterLink
          v-for="board in boards"
          :key="board.board_id"
          :to="`/boards/${board.board_id}`"
          class="block rounded-md border border-gray-300 p-2"
          :class="isActive(board.board_id)"
        >
          <div class="text-sm font-medium text-gray-800">
            {{ board.name }}
          </div>

          <div class="text-xs text-gray-400 line-clamp-2">
            {{ board.description || 'No description' }}
          </div>
        </RouterLink>
      </div>

      <!-- Create board -->
      <div class="mt-4 pt-4 border-t border-gray-300">
        <RouterLink
          to="/boards/create"
          class="block text-sm font-medium text-indigo-600 hover:text-indigo-800"
        >
          + Create new board
        </RouterLink>
      </div>
    </aside>

    <!-- Main -->
    <div class="flex-1 overflow-hidden">
      <RouterView />
    </div>
  </div>
</template>
