<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useBoardStore } from '@/stores/board'

const route = useRoute()
const boardStore = useBoardStore()

const boards = computed(() => boardStore.boards())

function isActive(boardId: number) {
  return route.params.board_id === String(boardId)
    ? 'bg-black text-white hover:bg-black translate-x-1'
    : 'bg-white hover:bg-yellow-400 text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-none hover:translate-x-1 hover:translate-y-1'
}
</script>

<template>
  <div class="flex h-[calc(100vh-3.5rem)] overflow-hidden">
    <!-- Sidebar -->
    <aside
      v-if="route.path !== '/boards'"
      class="w-72 shrink-0 border-r-2 border-black px-4 py-6 overflow-y-auto bg-white flex flex-col z-10 shadow-[8px_0px_0px_0px_rgba(0,0,0,1)]"
    >
      <!-- Header -->
      <div class="mb-8 pb-4 border-b-4 border-black">
        <RouterLink
          to="/boards"
          class="text-2xl font-black uppercase tracking-widest text-black hover:text-indigo-600 transition-colors"
        >
          My Boards
        </RouterLink>
      </div>

      <!-- Loading -->
      <div
        v-if="boardStore.loading"
        class="text-xl font-black uppercase tracking-widest animate-pulse p-4 bg-yellow-400 border-4 border-black text-center shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
      >
        LOADING...
      </div>

      <!-- Boards list -->
      <div v-else class="space-y-4 flex-1 overflow-y-auto pr-2 pb-4">
        <RouterLink
          v-for="board in boards"
          :key="board.board_id"
          :to="`/boards/${board.board_id}`"
          class="block border-4 border-black p-3 transition-all font-black uppercase tracking-wider"
          :class="isActive(board.board_id)"
        >
          <div class="text-base line-clamp-1 mb-1">
            {{ board.name }}
          </div>

          <div class="text-xs opacity-80 line-clamp-2 font-bold normal-case tracking-normal">
            {{ board.description }}
          </div>
        </RouterLink>
      </div>

      <!-- Create board -->
      <div class="mt-4 pt-6 border-t-4 border-black">
        <RouterLink
          to="/boards/create"
          class="block text-center font-black uppercase tracking-widest bg-indigo-600 text-white border-4 border-black p-4 hover:bg-black hover:text-white transition-all shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1"
        >
          + New Board
        </RouterLink>
      </div>
    </aside>

    <!-- Main -->
    <div class="flex-1 overflow-hidden relative z-0">
      <RouterView :key="route.fullPath" />
    </div>
  </div>
</template>
