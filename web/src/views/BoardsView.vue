<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Board } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'
import { getBoards } from '@/services/boards'
import BoardCard from '@/components/ui/cards/BoardCard.vue'

const notificationStore = useNotificationStore()
const boards = ref<Board[]>([])
const loading = ref<boolean>(true)

async function loadData(): Promise<void> {
  loading.value = true
  try {
    const data = await getBoards()
    boards.value = data
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Error loading boards.')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <section
    class="max-w-7xl mx-auto px-4 py-12 flex flex-col items-center min-h-[calc(100vh-3.5rem)] bg-gray-100"
  >
    <div class="w-full flex justify-between items-end border-b-8 border-black pb-4 mb-12">
      <h1 class="text-5xl md:text-7xl font-black uppercase tracking-tighter">Your Boards</h1>
    </div>

    <div
      v-if="loading"
      class="text-3xl font-black uppercase animate-pulse my-12 tracking-widest bg-yellow-400 border-4 border-black px-8 py-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
    >
      Loading...
    </div>

    <div
      v-else-if="boards.length === 0"
      class="bg-yellow-400 border-4 border-black p-8 shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] text-xl font-bold uppercase my-12 text-center max-w-lg"
    >
      <p>No boards found.</p>
      <p class="text-sm mt-4 text-gray-800">
        You literally have zero boards. Are you even trying to organize?
      </p>
    </div>

    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 w-full mb-16"
    >
      <RouterLink
        v-for="board in boards"
        :key="board.board_id"
        :to="`/boards/${board.board_id}`"
        class="block w-full h-full"
      >
        <BoardCard :data="board" />
      </RouterLink>
    </div>

    <RouterLink
      to="/boards/create"
      class="mt-auto md:mt-8 bg-indigo-600 text-white border-4 border-black font-black uppercase tracking-widest px-8 md:px-16 py-4 md:py-6 hover:bg-black hover:text-white active:translate-x-1 active:translate-y-1 transition-all shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] active:shadow-none text-xl md:text-2xl text-center w-full md:w-auto"
    >
      + Create a New Board
    </RouterLink>
  </section>
</template>
